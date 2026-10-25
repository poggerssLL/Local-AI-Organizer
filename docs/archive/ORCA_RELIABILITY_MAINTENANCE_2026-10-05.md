# Manutenção da Confiabilidade Operacional do Orca

Atualizado em: 2026-10-05.
Contrato de referência: `orca-model-routing/v1`, `ORCA_WORKER_LIFECYCLE.md`, `ORCHESTRATION_POLICY.md`, `references/recovery-and-cleanup.md`, `references/messaging-and-gates.md`.
Escopo: Diagnóstico técnico do comportamento de despacho, observabilidade de inicialização, tratamento de erros e protocolo de recuperação conservadora no Orca 1.4.219 com executores locais (Codex e Antigravity).

---

## 1. Diagnóstico do Comportamento Operacional

Durante a operação do Orca 1.4.219 na coordenação supervisionada de agentes locais, foram mapeados comportamentos críticos de telemetria, ciclo de vida e tratamento de recursos que exigem diferenciação operacional estrita:

### 1.1 `ready` não comprova `turn_start`
- A prontidão do runtime (`runtime.state: ready`, `connectionState: connected`) e do descritor de terminal (`terminalState: active`, `connected: true`) atesta exclusivamente que a infraestrutura local de IPC e o emulador de terminal (PTY) estão operantes.
- Essa condição não comprova que o processo do assistente consumiu a carga de entrada, inicializou o contexto nem iniciou o turno de trabalho (`turn_start`). Assumir que prontidão de canal equivale a execução em andamento é incorreto.

### 1.2 `outcome_unknown`, `input_accepted` e `turn_start_unobserved`
- No fluxo de injeção supervisionada (`worker-start` ou `dispatch --inject`), o envio do texto para o processo pode ser completado com êxito na camada do descritor (`dispatch_input: accepted`).
- O orquestrador inicia então uma janela de observação síncrona (tipicamente de até 30 segundos) aguardando telemetria positiva de início de turno do assistente.
- Se o agente não emitir evento reconhecido pelo orquestrador dentro dessa janela, o despacho é registrado com:
  - `workerState`: `start_unknown`
  - `stage.detail`: `turn_start_unobserved`
  - `projection.liveness`: `unverifiable` (motivo comum: `missing_status`)
  - `lastError`: aviso explícito de que a entrada foi aceita e submetida, mas o início de turno não pôde ser verificado em até 30s.
- **Princípio Operacional Central**: Esse estado indica *ausência de observação* e é formalmente classificado como `unverifiable`. Não constitui evidência de que o processo parou, travou ou encerrou. O estado `unknown` pode decorrer de múltiplas causas distintas (processo inicializando lentamente, retendo rascunho no compositor, bloqueado em dependência externa ou em erro silencioso).

### 1.3 `ask` e `reply`
- A primitiva `orca orchestration ask` cria uma consulta durável e tipada no Run vinculada ao despacho corrente. O comando aguarda resposta ou timeout; uma interrupção do turno pode exigir retomada explícita. O coordenador responde via `orca orchestration reply --id <id> --body <conteúdo>`.
- Caso ocorra desconexão ou expiração do tempo de espera do comando de terminal, a pergunta permanece pendente e deve ser retomada pelo identificador da mensagem (`--resume <message_id>`), sendo vedada a criação de perguntas duplicadas ou o uso de caixas de diálogo modais locais (como interfaces TUI locais), que bloqueiam o worker sem visibilidade do coordenador.
- **Evidência Operacional**: Esse protocolo é definido pelo contrato da skill `orchestration` e foi comprovado operacionalmente em ciclos anteriores do Organizer (como na Etapa 3 do Local File Agent). Não houve acionamento de `ask` nesta delegação específica, permanecendo como mecanismo contratual validado para bloqueios supervisionados.

### 1.4 Recurso `retained` e `user_takeover`
- O ciclo de vida do orquestrador isola a propriedade de recursos terminais.
- Se um terminal sofrer interação manual, pertencer à sessão preexistente do operador ou for marcado com retenção explícita (`worker-retain` ou política de salvaguarda de sessão ativa), o release de encerramento (`worker-release`) preserva o recurso como `retained` com motivo associado (`user_takeover` ou similar).
- Terminais retidos não contabilizam débitos como `reclaimable`, mas também não representam destruição ou abandono do processo pelo sistema operacional.

### 1.5 Distinções Conceituais e Arquiteturais Obrigatórias

| Eixo | Conceito A | Conceito B | Regra Operacional |
| :--- | :--- | :--- | :--- |
| **Camada** | **PTY**: Emulação do terminal do sistema operacional e transporte de fluxo de texto bruto. | **Provider**: Camada de integração do assistente (telemetria de sessão, chamadas estruturadas, eventos de status). | O PTY pode estar saudável e responsivo enquanto o provider carece de integração com o orquestrador. |
| **Escopo** | **Task**: Unidade lógica versionada do trabalho, requisitos e dependências do DAG. | **Dispatch**: Instância temporal delimitada de tentativa de execução de uma Task em um worker específico. | O encerramento ou falha de um Dispatch não cancela a Task; retentativas exigem vinculação explícita (`--retry-of`). |
| **Modelo** | **Requested**: Identificador, executor e nível de raciocínio solicitados na abertura. | **Effective**: Parâmetros reais confirmados no recibo de lançamento (`launch.effective`). | `launch.effective` correto valida a inicialização do perfil, mas **não descarta** outros defeitos posteriores (permissões, variáveis de ambiente, dados ou cotas). |
| **Origem** | **Transcript**: Eventos e mensagens estruturados emitidos diretamente pela API/sessão do assistente (`sourceExact: true`). | **Screen / Terminal**: Leitura visual do buffer/scrollback de caracteres impresso no PTY (`sourceExact: false`). | Antigravity emite via PTY/screen (`fallbackReason: session_not_reported`); Codex fornece transcript direto quando integrado. |
| **Liveness** | **PTY Live**: Terminal conectado e processo PTY rodando no host (`connected: true`). | **Agent Working**: Assistente comprovadamente ativo consumindo a tarefa e executando raciocínio/ações. | PTY live **não prova** que o agente está trabalhando; deve-se respeitar o veredito da frota e a hierarquia de fontes de `recovery-and-cleanup.md`. |
| **Finalização** | **Unknown / Unverifiable**: Ausência de telemetria ou atraso na confirmação de início. | **Exited**: Evidência positiva de saída do processo. Um turno encerrado por erro pode deixar o terminal vivo. | Release exige settlement aceito; recuperação de turno interrompido segue o guia e não implica processo exited. Ausência não autoriza cancelar ou repetir. |
| **Autoridade** | **Consumer Fenced**: Invalidação da autoridade do consumidor na fila de mensagens. | **Dispatch Fenced**: Cancelamento ou reatribuição da tentativa do worker no DAG. | `consumer_fenced` pode ocorrer por avanço de geração do consumidor ou execução em terminal não correspondente; deve-se verificar o contrato e a origem antes de inferir cancelamento global. |

---

## 2. Fatos Observados vs. Hipóteses em Aberto

A diferenciação entre fatos empíricos registrados nesta onda de despachos e hipóteses não instrumentadas é mandatória para evitar generalizações prematuras:

### 2.1 Fatos Observados e Confirmados

1. **`session_not_reported` e `missing_status` como Ausência Pontual de Dados**:
   - As indicações `fallbackReason: session_not_reported` em `worker-read` e `reason: missing_status` no veredito de liveness comprovam unicamente que houve *fallback* para leitura do buffer do terminal e que *naquele instante específico* o orquestrador não dispunha de registros de status estruturado.
   - Não constituem comprovação da arquitetura interna do orquestrador nem diagnóstico da causa do início não observado.

2. **Evento Singular de Rascunho e Desbloqueio no Codex**:
   - Em um despacho específico com Codex (Sol 6.1 high), a inspeção visual da tela revelou o conteúdo do prompt estacionado no campo de entrada do compositor. O envio exclusivo de um sinal de quebra de linha (`Enter` / `\r`, 1 byte gravado sem texto) pelo coordenador foi seguido pela transição do agente para o estado de trabalho ativo (`working`) e liveness `live`.
   - Esse fato comprova a eficácia da ação naquele caso concreto; **não comprova** que o volume de caracteres do prompt seja a causa do fenômeno, nem autoriza assumir que todo despacho Codex em `turn_start_unobserved` seja um rascunho pendente.

3. **Atividade Posterior e Conclusão Autônoma no Antigravity**:
   - Em despacho Antigravity (Gemini 3.8 Flash high), o início de turno não foi observado na janela inicial de 30s (`start_unknown`).
   - Sem qualquer intervenção humana, repetição de entrada ou tecla Enter pelo coordenador, o assistente iniciou autonomamente a execução técnica posterior (verificada por leituras de buffer PTY com comandos e raciocínio), emitiu heartbeats periódicos e concluiu a tarefa integralmente via `worker_done`.
   - O fato comprovado é a **atividade posterior autônoma e a entrega válida**; não é possível afirmar o estado funcional exato nos primeiros segundos em que não havia dados telemétricos.

4. **Encerramento Positivo por Falha de Cota e Tratamento com `worker-abandon`**:
   - No despacho do Local Transcriber com Antigravity (Claude Sonnet 5.5 high), houve evidência positiva de encerramento do turno por erro explícito de cota individual, sem emissão de `worker_done`. O tipo de cobrança/API não foi investigado.
   - O coordenador tratou o encerramento do worker através de `worker-abandon`, delimitando o despacho, admitindo a retenção dos recursos e registrando o bloqueio no Run, em conformidade com o procedimento de recuperação, sem substituição silenciosa de modelo e sem mascarar a falha.

5. **Concordância de `launch.effective`**:
   - Nos três lançamentos iniciais com terminal novo, `launch.effective` confirmou executor, modelo e esforço solicitados (Sol 6.1 high, Gemini 3.8 Flash high e Claude Sonnet 5.5 high). Na revisão em terminal reutilizado, esse campo veio sem modelo: Gemini high foi declarado como herdado da sessão comprovada, sem alegar nova confirmação do campo.

### 2.2 Hipóteses em Aberto (Causas Não Investigadas)

1. **Causa Raiz da Falta de Telemetria no Antigravity CLI**:
   - Permanece desconhecido se o descompasso de telemetria decorre de latência de inicialização do processo no sistema operacional, de ausência de ganchos de protocolo de sessão no executável CLI, ou de descarte prematuro da observação pelo orquestrador.
2. **Causa da Não-Submissão do Prompt no Compositor do Codex**:
   - Permanece como hipótese se a retenção do texto como rascunho é causada por sincronização de buffer no emulador PTY do Windows, por comportamento da interface de edição do agente, ou por latência na absorção da quebra de linha final durante a colagem.

---

## 3. Matriz de Diagnóstico Baseada em Evidência

Ações operacionais exigem **evidência positiva prévia**. O simples fato de o executor ser Codex ou Antigravity não autoriza classificar o estado como ativo ou retido:

| Estado Observado | Evidência Requerida | Diagnóstico Confirmado | Ação Permitida | Ação Vedada |
| :--- | :--- | :--- | :--- | :--- |
| `turn_start_unobserved` | Inspeção visual da tela exibindo prompt parado no campo de edição sem comandos. | Rascunho estático no compositor. | Enviar estritamente sinal de submissão (`Enter`/`\r`, 1 byte) no terminal do worker. | Reenviar o prompt por extenso, abrir novo worker ou trocar modelo. |
| `turn_start_unobserved` | `worker-read` (buffer PTY) exibindo saída de comandos, chamadas de ferramenta ou raciocínio. | Assistente em atividade autônoma posterior. | Manter o despacho intocado; aguardar ciclo de trabalho e heartbeats. | Reenviar prompt, enviar Enter, fechar terminal ou emitir `worker-stop`. |
| `turn_start_unobserved` | Buffer sem alterações ou dados insuficientes. | Estado desconhecido; não comprova estagnação ou saída. | Consultar frota e fontes do host; somente prova positiva de turno encerrado ou processo exited permite escolher recuperação conforme o guia. | Declarar falha ou repetir a partir da ausência de dados. |
| Turno encerrado por erro explícito (ex.: cota individual) | Erro final no buffer ou transcript e turno encerrado sem `worker_done`. | Tentativa interrompida sem relatório; o processo pode continuar vivo. | Escolher recuperação pelo guia, registrar motivo e preservar os recursos não encerrados. | Substituir silenciosamente por outro modelo ou fingir sucesso. |
| `liveness: unverifiable` | Frota sem status; PTY live sozinho não resolve a dúvida. | Lacuna de evidência. `host_unavailable` é perda de contato com o host; `missing_status` é ausência de status. | Seguir a hierarquia de fontes do guia e manter checkpoints, sem promover unknown a live/exited. | Interpretar ausência como morte, cancelar despacho ou forçar release. |
| Recurso em `retained` após release | Recibo de `worker-release` com indicação de `user_takeover` ou salvaguarda de sessão. | Terminal preservado por política de proteção ou interação manual. | Acolher a retenção; confirmar que débitos `reclaimable` estão zerados no Run. | Forçar `terminal close` manual em terminal retido. |
| `consumer_fenced` | Código de erro formal em comandos de mensageria (`send`, `ask`, `check`). | Autoridade de consumo invalidada ou terminal não coincidente com a origem esperada. | Verificar contrato da mensagem e origem do comando; cessar mutações sob autoridade invalidada. | Inferir cancelamento global do Dispatch sem consulta ao Run. |

---

## 4. Procedimento Idempotente Conservador

Para coordenadores supervisionando execuções de workers locais:

1. **Fase de Despacho**:
   - Emitir `worker-start` com especificação completa de parâmetros (`--worktree`, `--agent`, `--model`, `--effort`).
   - Conferir imediatamente se o recibo retornou `launch.effective` idêntico ao solicitado.

2. **Tratamento de `turn_start_unobserved` por Inspeção Positiva**:
   - Caso o retorno acuse `outcome_unknown` com `turn_start_unobserved`, **não abortar nem reenviar**.
   - Executar inspeção síncrona não-destrutiva via `orca orchestration worker-show --dispatch <id> --json`.
   - Consultar saída limitada com `orca orchestration worker-read --dispatch <id> --json`; para verificar rascunho no compositor de um worker local com terminal, usar `orca terminal read --terminal <handle> --screen --json`. Scrollback sozinho não comprova um rascunho:
     - **Caso haja rascunho visual comprovado parado**: emitir estritamente um sinal de quebra de linha (`Enter`) no terminal designado, sem qualquer texto adicional.
     - **Caso haja atividade posterior comprovada (comandos, ferramentas, pensamento)**: registrar o worker como em processamento e não intervir.
     - **Caso haja erro final e turno encerrado sem `worker_done` comprovados**: seguir o guia de recuperação para escolher `worker-abandon` ou `worker-stop`; o erro sozinho não prova saída do processo.
     - **Caso não haja dados (silêncio total)**: tratar como estado `unverifiable` e manter a janela de observação sem mutações.

3. **Ciclo de Acompanhamento (Checkpoints vs. Progresso)**:
   - Utilizar `orca orchestration check --wait` com timeout prudente.
   - **Regra de Interpretação**: Um timeout ou retorno vazio em `check --wait` é estritamente um **checkpoint periódico de inspeção**, jamais prova de processamento contínuo.
   - **Regra de Liveness**: Um heartbeat recente atesta unicamente a **liveness pontual** do processo naquele momento; não comprova progresso nem garante proximidade de conclusão.

4. **Conclusão e Limpeza**:
   - Ao receber `worker_done`, validar se o resumo de 3 frases atende ao contrato, conferir arquivos modificados e relatórios duráveis.
   - Executar `orca orchestration worker-release --dispatch <id> --json`.
   - Se o terminal for preservado como `retained/user_takeover`, respeitar a salvaguarda do orquestrador.
   - Verificar ausência de débitos residuais com `orca orchestration worker-list --run <run_id> --terminal-state reclaimable`.

---

## 5. Estudo de Casos desta Onda de Despachos

A análise comparativa dos três despachos desta onda ilustra a diversidade de comportamentos reais:

### Caso A: Antigravity no Organizer (Atividade Posterior após Início Não Observado)
- **Perfil**: Antigravity (`gemini-3.8-flash-high`, esforço `high`), confirmado em `launch.effective`.
- **Início**: Retorno `start_unknown` com `turn_start_unobserved` e `missing_status`.
- **Desenrolar**: O assistente processou a tarefa autonomamente em segundo plano, executou comandos de checagem e unittests no PTY, emitiu heartbeats periódicos duráveis e entregou o resultado via `worker_done` sem qualquer intervenção ou tecla Enter pelo coordenador.
- **Lição**: Ausência inicial de sinal síncrono não autoriza cancelamento ou reenvio.

### Caso B: Codex no Local File Agent (Desbloqueio Pontual de Compositor)
- **Perfil**: Codex (`gpt-6.1-sol`, esforço `high`), confirmado em `launch.effective`.
- **Início**: Retorno `start_unknown` com `turn_start_unobserved`.
- **Desenrolar**: A inspeção comprovou a presença de rascunho colado estacionado no compositor. O envio exclusivo de 1 byte (`Enter`) desbloqueou a execução, transicionando o agente para `working` e `live`, com entrega posterior de resultado.
- **Lição**: Ação corretiva mínima e cirúrgica fundamentada em evidência visual direta, sem reenvio de prompt.

### Caso C: Antigravity no Local Transcriber (Erro Positivo de Cota e Abandono Supervisionado)
- **Perfil**: Antigravity (`claude-sonnet-5-5-high`, esforço `high`), confirmado em `launch.effective`.
- **Início**: Retorno `start_unknown` com `turn_start_unobserved`.
- **Desenrolar**: O assistente encontrou erro explícito de cota individual, encerrando o turno sem `worker_done`; não foi observado encerramento do processo PTY.
- **Tratamento**: O coordenador usou `worker-abandon`, manteve o terminal retido e registrou a tarefa como failed. Uma nova tentativa foi selecionada explicitamente com Gemini high no mesmo executor e escopo, informada ao usuário, sem fallback automático.
- **Lição**: Erros reais comprovados exigem aceitação fail-closed e recuperação formal via ciclo supervisionado.

---

## 6. Limitações e Critérios para Canários Futuros

### 6.1 Limitações da Abordagem
- As orientações deste documento constituem **mitigação operacional e procedimental**. Não corrigem o código-fonte interno do binário do Orca nem eliminam a existência de falsos alarmes de observação de início.
- As causas de divergência telemétrica entre o monitor de lançamento e os processos do PTY permanecem desconhecidas no nível de implementação do orquestrador.

### 6.2 Critérios de Aceite para Futuros Canários de Despacho
Antes de homologar novas versões do Orca para operações em repositórios de produção:
1. **Fixture Sintética**: Execução estrita em ambiente isolado ou worktree descartável.
2. **Conferência Fail-Closed de Modelo**: Recibo com divergência entre `launch.requested` e `launch.effective` encerra o teste imediatamente como falha.
3. **Inspeção de Injeção**: Avaliar comparativamente o comportamento de submissão de prompts em diferentes executores antes de interações em lote.
4. **Encerramento Limpo**: Confirmação de encerramento via `worker_done` ou falha tratada formalmente (`worker-stop`/`worker-abandon`), com `worker-release` concluído e zero terminais `reclaimable` no Run.
5. **Higiene de Repositório**: Verificação de `git diff --check` e integridade de arquivos versionados.

## Validação e proveniência

O worker Gemini high informou 28 testes determinísticos aprovados no Organizer;
isso não testa o binário do Orca nem corrige o lançamento. A entrega documental
foi revisada em uma segunda Task no mesmo terminal e integrada pelo coordenador.
Os 13 arquivos modificados preexistentes ficaram fora do escopo dessa manutenção.
Não houve mudança de settings, instalação, credenciais ou código da aplicação Orca.

Um lançamento posterior de Codex Sol 6.1 medium, escritor do complemento do File Agent,
retornou ready com turnStart observed sem intervenção de terminal. O comportamento
variou nesta mesma onda; não foi estabelecida sua causa nem uma taxa de confiabilidade.

O gate posterior Codex Sol 6.1 high também retornou ready com turnStart observed,
concluiu a revisão e foi liberado com arquivo de transcript. Uma tentativa de
reutilizar o terminal Gemini do Transcriber para complemento documental falhou
em agent_readiness, antes da injeção e sem recurso novo materializado. Após
inspeção e liberação do despacho anterior concluído, a mesma Task recebeu uma
retentativa explícita em terminal novo com Gemini 3.8 Flash high confirmado em
launch.effective. A observação inicial dessa retentativa ficou unobserved; a tela
mostrou execução posterior, sem reinjeção de prompt. Esse caso limita também a
presunção de prontidão automática de um terminal reutilizado.

Durante a revisão da manutenção do Transcriber, o coordenador observou uma
remoção pelo worker do diretório pai tests/fixtures, além das duas subárvores
autorizadas. O complemento também procurou logs do provider fora do pacote
previsto; o coordenador enviou restrição explícita e exigiu revisão factual.
O escopo em uma Task e o recebimento de worker_done não comprovam que todas as
ações respeitaram o envelope. A mensageria é durável, mas a leitura dos follow-ups
pelo worker depende de checkpoints; envio não equivale a obediência imediata.
O gate deve revisar as ações e os limites de preservação, além do resultado dos
testes. Nenhum dado de runtime ou transcrição foi incluído neste relatório.

## Encerramento da onda supervisionada

| Task | Resultado aceito e limite |
| --- | --- |
| Gate inicial do File Agent, Codex Sol high | Revisão concluída; complemento necessário pela falha inicial da raiz. Não aprovou release naquele momento. |
| Diagnóstico Orca, Gemini high | Relatório e 28 testes determinísticos do Organizer; causalidades excessivas exigiram complemento. |
| Complemento editorial Orca, Gemini high herdado | Precisão revisada e integrada; mitigação documental, sem correção do binário. |
| Baseline Transcriber, Gemini high após cota Claude | Reexecução com 141 aprovações, Ruff pendente e código preexistente preservado; complemento factual exigido. |
| Correção da raiz do File Agent, Codex Sol medium | Correção e três regressões; 70/69/1; aceite independente registrado. |
| Gate final do File Agent, Codex Sol high | PRONTO PARA COMMIT, 17 candidatos e 70/69/1, apenas fixtures NTFS sintéticas. |
| Complemento factual Transcriber, Gemini high após falha de reutilização | Quatro sintaxes JS aprovadas; limites de limpeza e teste intermitente explícitos. |

Sete Tasks concluídas em nove tentativas. As duas tentativas interrompidas/falhadas
ficaram registradas; seis despachos tiveram release e três registros foram retidos
por transferência de propriedade, ausência de recurso novo ou identidade não provada.
A consulta final no Run retornou zero workers ativos e zero reclaimable. Os registros
retidos não demonstram três processos vivos nem autorizam fechamento forçado.
Todas as entregas e perguntas recebidas foram processadas e reconhecidas.

Após liberar os escritores, o coordenador integrou somente precisão documental
e os fatos desta onda em PROJECT_REGISTRY e ROADMAP, preservando as alterações
preexistentes. Naquele encerramento, commit/push dos projetos estavam pendentes
de autorização nominal; dados reais e etapas futuras não haviam sido iniciados.

## Publicação posterior do File Agent

Em 2026-10-05, Erick autorizou nominalmente o commit e o push dos 17 arquivos
revisados da Etapa 3. Publicação concluída em main `49c7dbe`; HEAD, origin/main e
main consultado no servidor coincidem, e o checkout do File Agent está limpo.
Isso não publica as alterações do Organizer/Transcriber nem corrige as falhas
do binário ou os desvios de envelope registrados neste diagnóstico.

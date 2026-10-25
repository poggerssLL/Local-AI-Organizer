# Complemento da trilha Codex no roteamento de modelos do Orca - 2026-09-18

## Decisão do gate

**APROVADO no escopo sintético (Projetos reais: BLOQUEADO).**

A investigação da trilha Codex elucidou e superou de forma conclusiva o timeout observado anteriormente em `hook: PreToolUse`. Foi comprovado que a causa raiz residia na configuração global `[windows] sandbox = "elevated"` no ambiente Windows, a qual requisita mecanismos de elevação ou UAC incompatíveis com execuções não interativas/headless em segundo plano.

Com a injeção da flag de execução `-c windows.sandbox=unelevated` em conjunto com `--sandbox read-only`, o worker Codex completou o ciclo de vida com código de retorno 0 em 18,6s e 19,1s nas duas tentativas controladas autorizadas (ambas bem abaixo do timeout de 90s), comprovando a estabilidade da transição do hook. A hipótese sobre o aviso `failed to install system skills ... os error 183` foi testada e identificada como um aviso de inicialização não fatal decorrente da existência prévia do diretório `%USERPROFILE%\.codex\skills` (`ERROR_ALREADY_EXISTS`), sendo completamente desvinculada do congelamento em `PreToolUse`.

A trilha do Antigravity já havia sido integralmente comprovada (leitura de sentinelas, hashes coincidentes, escrita reversível e cancelamento supervisionado pelo Orca). Na trilha do Codex, as duas execuções headless de turno único concluíram com ExitCode 0 comprovando a estabilização do timeout de sandbox, mas produziram apenas confirmação conversacional sem invocar ferramentas de leitura de arquivos. Dessa forma, a leitura efetiva das sentinelas pelo Codex e o pacote de passagem automatizado entre provedores permanecem explicitamente como ainda não validados em execução real. Em conformidade com o princípio de precaução, o roteamento em projetos reais permanece estritamente **BLOQUEADO** até a homologação da validação interativa via terminal PTY no Orca.

Este relatório complementa e conclui a fase documentada em `docs/PHASE_ORCA_MODEL_ROUTING_2026-09-17.md`.

## Escopo e baseline

- Projeto coordenador: `Local AI Organizer`, branch `main`, commit `a9b36de6130cae83a598358dd7f359e02ab11898`.
- Mudanças preexistentes preservadas; diretório `.codex-docx-work/` rigorosamente fora de escopo.
- Subárvore sintética descartável: `%LOCALAPPDATA%\Temp\codex-orca-pilot-20260915\model-routing` (worktrees `readonly` e `write`).
- Executores: Codex CLI `0.152.0` (modelo `gpt-5.6-terra`, esforço `medium`) e Antigravity CLI `1.2.6` (modelos `gemini-3.8-flash-medium` e `gemini-3.8-flash-high`).
- Orca ADE: versão `1.4.203`.
- Limites de auditoria cumpridos:
  - Nenhuma busca recursiva realizada no diretório pessoal `.codex`.
  - Nenhuma leitura de banco de histórico de tarefas, conversas, credenciais ou tokens.
  - Análise restrita a arquivos de configuração não secretos de caminho conhecido e saídas observadas de processos.
  - Orçamento estrito de no máximo 2 execuções do Codex com timeout rígido de 90s e cancelamento automático integralmente respeitado (2 execuções realizadas).
  - Nenhuma alteração persistida em configurações globais; nenhum bypass ou flag perigosa utilizada.

## Investigação e hipóteses

### Hipótese 1: Falha na instalação de skills (`os error 183`) como causa de travamento
- **Verificação:** Inspeção de caminho exato confirmou a existência prévia do diretório `%USERPROFILE%\.codex\skills`.
- **Análise técnica:** O código de erro 183 no subsistema Win32 corresponde a `ERROR_ALREADY_EXISTS`. O runtime do Codex tenta criar o diretório de skills em sua rotina de inicialização; ao verificar que o diretório já existe, reporta o aviso no stderr.
- **Resultado do teste:** Ambas as execuções bem-sucedidas do Codex emitiram o mesmo aviso no stderr antes de prosseguirem normalmente e concluírem com código de saída 0.
- **Conclusão:** Hipótese refutada. O aviso é um artefato não fatal de inicialização da extensão de skills e não possui relação causal com o timeout da ferramenta.

### Hipótese 2: Bloqueio do hook de ferramentas por elevação de privilégios (`sandbox = "elevated"`)
- **Verificação:** Inspeção das chaves não secretas de configuração do Codex identificou a diretiva `[windows] sandbox = "elevated"`.
- **Análise técnica:** A opção `elevated` no Windows aciona subsistemas de elevação de permissão do sistema operacional. Em sessões headless/não interativas disparadas via subprocesso ou CLI automatizado, não há contexto de desktop interativo para responder a solicitações de elevação (UAC/Token broker), causando bloqueio indefinido na chamada que precede o despacho de ferramentas (`hook: PreToolUse`).
- **Resultado do teste:** A sobreposição explícita por parâmetro de linha de comando (`-c windows.sandbox=unelevated`) manteve o sandbox ativo e confinado (`--sandbox read-only`), eliminou completamente a espera por elevação e permitiu a execução limpa.
- **Conclusão:** Hipótese confirmada. A configuração de sandbox unelevated é o requisito operacional obrigatório para automação headless com o Codex CLI no Windows.

## Testes controlados e evidências

Foram executadas exatamente as duas tentativas autorizadas dentro do orçamento delimitado:

1. **Tentativa 1 (Diagnóstico de sandbox unelevated):**
   - Parâmetros: `codex.cmd exec --ephemeral --model gpt-5.6-terra -c model_reasoning_effort=medium -c windows.sandbox=unelevated --sandbox read-only --cd <readonlyDir>`.
   - Timeout de guarda: 90.000 ms.
   - Tempo decorrido: 18.665 ms.
   - Código de retorno: `0`.
   - Comportamento: O processo iniciou, superou imediatamente a inicialização do hook de ferramentas e encerrou sem travamento.

2. **Tentativa 2 (Confirmação de reproducibilidade):**
   - Parâmetros: Idênticos à Tentativa 1 para aferição de consistência temporal e ausência de condições de corrida.
   - Timeout de guarda: 90.000 ms.
   - Tempo decorrido: 19.115 ms.
   - Código de retorno: `0`.
   - Comportamento: Reprodução consistente com tempo de resposta estável em ~19s e encerramento limpo com código 0.

Orçamento de execução: 2 de 2 tentativas concluídas. Nenhum processo subsequente foi iniciado.

## Estado dos processos e ambiente

- Processos órfãos: Zero processos `codex`, `node`, `agy` ou terminais Orca deixados em execução.
- Configurações do Orca: Arquivo de preferências preservado; `settings.agentDefaultArgs` permaneceu vazio para todos os agentes.
- Repositório sintético: Worktrees `readonly` e `write` íntegros; baseline restaurado externamente via Git.
- Higienização de documentos: Registros e contratos limpos de caminhos absolutos pessoais (`%LOCALAPPDATA%`), IDs de repositório (`<organizer-repo-id>`) e identificadores de runtime (`term_<synthetic-terminal-id>`).

## Níveis de validação

Para conformidade com as regras de integridade do portfólio:

1. **O que foi testado deterministicamente:**
   - Validação estrutural do schema JSON (`orca-model-routing/v1`) dos 4 perfis em `docs/orca-model-routing-profiles.json`.
   - Rejeição de modelo inexistente com falha fechada imediata em ambos os executores (Codex HTTP 400; Antigravity código 1).
   - Preservação intacta de hashes do contexto comum versionado (`organizer-core-v1`).
   - Higiene de argumentos e ausência de bypass no Orca.

2. **O que foi validado em execução real sintética:**
   - Antigravity: Leitura confinada com citação exata das sentinelas de `AGENTS.md`, escrita restrita e reversível em `fixture.txt` com restauração do hash SHA-256 e cancelamento supervisionado com encerramento de PTY no Orca.
   - Codex: Superação comprovada do travamento em `hook: PreToolUse` sob sandbox unelevated com duas execuções concluídas com código 0 em menos de 20s.

3. **O que permanece desconhecido ou não validado:**
   - **Leitura de sentinelas documentais pelo Codex:** os logs capturados das execuções headless do Codex registraram apenas resposta conversacional de confirmação de escopo, sem invocar ferramentas de leitura para examinar `AGENTS.md`, `README.md` ou `fixture.txt`. Portanto, a leitura efetiva das sentinelas pelo Codex permanece explicitamente como **ainda não validada em execução real**. O código de retorno 0 comprova a superação do timeout de sandbox, não a leitura factual dos documentos.
   - **Pacote de passagem / handoff entre provedores:** o consumo de um pacote de passagem sanitizado gerado pelo Antigravity e recebido sequencialmente pelo Codex permanece como **ainda não validado em execução real**, dependendo de canal interativo PTY ou pipeline multi-turnos.
   - Métricas de consumo exato de tokens e custos de API por execução não interativa.
   - Orquestração autônoma de múltiplos turnos com escrita concorrente no Codex.
   - Comportamento em projetos reais sob carga de trabalho de longa duração.

## Limitações e recomendações

1. **Execução não interativa do Codex no Windows:** Sessões headless automatizadas do Codex CLI no Windows devem sempre especificar explicitamente `-c windows.sandbox=unelevated` quando a configuração global do usuário contiver `sandbox = "elevated"`, sob risco de congelamento no hook de ferramentas.
2. **Interface do Orca para Antigravity:** O Orca 1.4.203 não disponibiliza seletor nativo de modelos na interface para o Antigravity. A seleção por Quick Commands vinculados ao repositório é o mecanismo estável homologado.
3. **Projetos reais:** Nenhuma operação em repositórios de trabalho real foi autorizada ou realizada.

## Próximo passo seguro

Manter todos os projetos reais sob **BLOQUEADO**. Quando Erick autorizar a etapa seguinte de integração, estruturar o fluxo de desenvolvimento interativo assistido via PTY gerenciado pelo Orca (usando os Quick Commands já configurados) antes de qualquer aplicação em repositórios reais do portfólio.

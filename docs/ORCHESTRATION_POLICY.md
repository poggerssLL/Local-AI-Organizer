# Política de orquestração

## Objetivo

Definir quando o coordenador pode analisar, criar prompts, abrir tarefas e acompanhar
outros projetos. O princípio central é: planejamento pode ser proativo; alterações exigem
autorização explícita e escopo verificável.

## Autoridade por tipo de pedido

| Pedido de Erick | Ação permitida |
| --- | --- |
| “Explique”, “analise”, “diagnostique” ou “revise” | Ler e responder; não corrigir nem abrir tarefa implementadora |
| “Crie o prompt” | Produzir o prompt; não enviá-lo nem iniciar outra tarefa |
| “Delegue”, “crie uma tarefa” ou “inicie a etapa” | Criar uma única tarefa no projeto indicado, com o escopo autorizado |
| “Implemente” | Alterar somente o projeto e a etapa explicitamente autorizados |
| “Execute/orquestre esta etapa de forma autônoma” | Prosseguir até o gate com as ações reversíveis incluídas no envelope de execução |
| “Faça commit” ou “publique” | Commitar ou enviar ao remoto somente os arquivos da mudança autorizada e após validação |
| “Monitore” ou “acompanhe” | Usar o mecanismo de acompanhamento adequado sem ampliar o escopo da tarefa |

Uma autorização para criar tarefa não autoriza downloads, instalações, mudanças de
sistema, credenciais, exposição de rede, commit ou push quando esses atos não estiverem
incluídos no pedido ou no prompt aprovado.

## Envelope de execução autônoma

Quando Erick pedir autonomia para uma etapa, o coordenador deve registrar projeto,
objetivo, executores, capacidades permitidas, limites, evidências e condição de parada.
Dentro desse envelope, pode criar e acompanhar workers, editar o projeto autorizado,
executar testes, corrigir falhas do mesmo escopo e atualizar documentação factual sem
pedir confirmação a cada ação reversível.

Após cada gate ou mudança de necessidade, o coordenador deve comparar o estado real com o
roadmap aplicável. Quando houver autorização de escrita, deve registrar o marco comprovado,
o replanejamento e o próximo passo, preservando relatórios históricos e sem transformar
propostas em fatos.

Continuam reservados, salvo menção expressa: outro projeto, dados pessoais fora do escopo,
credenciais e login, instalação de sistema ou elevação administrativa, exposição pública
de rede, ação destrutiva, commit, push, merge e publicação. Um único worker pode escrever
em cada checkout; revisores usam somente leitura ou worktrees separados.

## Política de interação com o computador

O coordenador não deve priorizar controle direto de teclado e mouse. A ordem padrão é:

1. ferramentas específicas, conectores ou APIs;
2. terminal, arquivos e configurações declarativas;
3. orientação curta para Erick realizar a etapa visual;
4. controle direto da interface somente após pedido explícito.

Autonomia de uma etapa não inclui implicitamente controle visual do computador. Instalação
interativa, login, consentimento, UAC, pagamento e seleção de conta pertencem a Erick. O
agente deve preparar o restante, fornecer uma etapa por vez e confirmar o resultado por
comando, arquivo, log ou outro estado observável. Se teclado e mouse forem autorizados,
o envelope deve delimitar aplicativo, objetivo e duração; credenciais nunca podem ser
digitadas pelo agente.

## Autoridade operacional em pilotos descartáveis

Quando Erick autorizar um complemento sintético, o Organizer pode administrar sem novas
confirmações a subárvore temporária exata do piloto: criar ou reconstruir fixtures e
worktrees, resolver caminhos, definir o `cwd`, iniciar e encerrar processos, ajustar
configurações não secretas com backup e verificar hashes e Git.

Também pode configurar `proceed-in-sandbox` ou allowlists específicas para comandos
locais necessários ao teste headless. São proibidos `always-proceed`, flags de bypass,
`command(*)`, acesso global a arquivos, `allowNonWorkspaceAccess` e qualquer permissão a
projetos reais. O worker recebe o `cwd` absoluto previamente validado e opera com caminhos
relativos. Se tentar sair do workspace, o Organizer interrompe, corrige o mapeamento e
repete dentro do limite do envelope; não amplia a fronteira.

## Ciclo obrigatório de delegação

1. Identificar o projeto e o modo solicitado.
2. Consultar `PROJECT_REGISTRY.md`, `SYSTEM_MAP.md` e `ROADMAP.md`.
3. Localizar o projeto salvo no Codex pelo rótulo atual.
4. Abrir o repositório alvo e ler suas instruções antes de confirmar o baseline.
5. Classificar o estado como confirmado, informado, planejado ou desconhecido.
6. Selecionar somente as skills disponíveis e adequadas.
7. Produzir um prompt com objetivo único usando `DELEGATION_TEMPLATE.md`.
8. Criar uma única tarefa no projeto alvo quando Erick tiver autorizado a delegação.
9. Acompanhar a tarefa sem iniciar outra escrita concorrente no mesmo checkout.
10. Revisar o resultado, as evidências, a documentação e o Git.
11. Aprovar, bloquear ou solicitar complemento na mesma tarefa.
12. Atualizar os documentos centrais somente quando o estado factual mudar.

## Tarefas separadas e subagentes

O modelo de orquestração do Organizer rejeita o agente centralizador que monopoliza o contexto da conversa. O coordenador opera como arquiteto e orquestrador de fluxo, delegando o esforço cognitivo e operacional para workers e subagentes especializados.

### Critérios de separação: Tarefa externa vs. Subagente interno

Use uma **tarefa separada do Codex / Antigravity** quando:
- o trabalho pertencer a outro repositório ou projeto;
- houver implementação profunda com commits independentes e ciclo de vida próprio;
- o resultado precisar permanecer com histórico autônomo, rastreável e retomável por Erick;
- o projeto de destino demandar descoberta de skills e configuração isolada de ambiente.

Use **subagentes dentro da tarefa atual** para decompor e paralelizar o plano de trabalho, respeitando as cláusulas de não monopolização.

### Política de Não Monopolização da Janela de Coordenação

1. **Vedação de execução monobloco:** É expressamente vedado ao coordenador executar sequencialmente na janela principal rotinas pesadas de busca textual, leitura massiva de código, redação de peças extensas, testes repetitivos ou depuração de erros que possam ser isoladas.
2. **Exceções técnicas admitidas:** A atuação direta monobloco do coordenador é admitida apenas quando:
   - O ambiente do executor corrente não disponibilizar primitivas de despacho (ex.: indisponibilidade transitória de subagentes ou ambiente sem suporte a workers em background);
   - A operação for atômica, imediata (verificação direta de até 2 comandos) e a criação de subagente gerar overhead desproporcional de tokens e latência;
   - Houver necessidade direta de alinhamento ou decisão de Erick antes de qualquer desdobramento.

### Matriz Obrigatória de Despacho Ativo

O coordenador deve acionar ativamente subagentes (via `invoke_subagent`, workers assíncronos ou integrações de API) nas seguintes áreas:

| Domínio da Atividade | Tipo de Despacho Obrigatório | Função do Subagente |
| --- | --- | --- |
| **Pesquisa e Exploração** | Subagente `research` / leitor | Investigar bases de código, logs, documentação externa e APIs sem poluir o histórico principal |
| **Redação e Documentação** | Subagente redator / técnico | Elaborar minutas de arquitetura, manuais, especificações e relatórios de fase |
| **Implementação e Mocks** | Subagente executor / tester | Construir suítes de teste, fixtures, mocks determinísticos e scripts de validação |
| **Auditoria e Conformidade** | Subagente auditor / gatekeeper | Verificar conformidade com políticas, checar vazamento de credenciais e validar gates |
| **Rotinas e Validação** | Worker em background | Rodar testes de regressão, lint, compilação e benchmarks de desempenho |

### Transparência e Rastreabilidade de Proveniência (Provenance Tracking)

Todo relatório de progresso ou conclusão de etapa deve conter registro explícito de proveniência:
- **Despachado via Subagente:** Listar cada papel despachado (`role`), o objetivo da delegação e o resumo do artefato produzido.
- **Execução Direta pelo Coordenador:** Listar as ações pontuais realizadas pelo coordenador na janela atual e registrar explicitamente o motivo da não delegação (ex.: *interação de canal único*, *bloqueio técnico de despacho*, ou *verificação atômica trivial*).
- Nenhuma conclusão pode ser atribuída genericamente a outros agentes ou modelos sem que a trilha de despacho e execução efetiva fique clara e verificável para Erick.

### Governança de Paralelismo: Estabilidade e Custos

- **Regra Pétrea de 1 Escritor por Checkout:** O paralelismo nunca autoriza duas escritas simultâneas na mesma árvore Git. Subagentes simultâneos de escrita devem obrigatoriamente atuar em Git worktrees separados ou em diretórios temporários (`scratch`/fixtures). Para o mesmo checkout, apenas um agente possui autorização de escrita por vez.
- **Racionalização de Consumo:** A criação de subagentes deve ter escopo delimitado e critério de parada claro. Subagentes recursivos infinitos ou disparos redundantes que consumam cotas desnecessárias de tokens são proibidos.
- **Responsabilidade pela Consolidação:** O subagente produz o insumo técnico; cabe ao coordenador auditar o resultado contra os contratos e evidências antes de registrar o avanço em qualquer documento durável do projeto.

## Integração controlada com Orca ADE

O `Orca ADE` foi avaliado em piloto sintético como camada operacional para iniciar e
acompanhar agentes CLI. Ele não substitui o `Local AI Organizer`: o Organizer continua
decidindo o projeto, objetivo, executor, permissões e aprovação final. O contrato vivo da
integração está em `ORCA_PILOT_CONTRACT.md`; o resultado histórico e as limitações da
execução de 2026-09-15 estão em `PHASE_ORCA_PILOT_2026-09-15.md`, e o complemento
bloqueado do Antigravity está em `PHASE_ORCA_PILOT_COMPLEMENT_2026-09-16.md`. O segundo
complemento, que concluiu a trilha sintética, está em
`PHASE_ORCA_PILOT_SECOND_COMPLEMENT_2026-09-17.md`.

Antes de qualquer adoção, receba autorização explícita para um envelope de execução. A
adoção começa em ambiente descartável com dados sintéticos: leitura, seguida de escrita
reversível apenas se os critérios do mesmo envelope forem satisfeitos. Codex e
Antigravity podem participar sequencialmente ou em worktrees separados, com um único
escritor por checkout. Escrita em projeto real, credenciais, commit, push e publicação
permanecem gates separados, salvo inclusão explícita no envelope.

O piloto confirmou para Codex e Antigravity, em dados sintéticos, leitura confinada,
bloqueio de escrita no perfil somente leitura, escrita reversível em worktree separado,
restauração e cancelamento. No Windows, a sessão Antigravity deve ser iniciada com o
diretório de trabalho já resolvido e `--new-project`; o prompt do worker usa apenas
caminhos relativos. O segundo complemento também mostrou que o detector de prontidão do
Orca 1.4.203 pode não reconhecer diretamente o prompt do Antigravity 1.2.5: a recuperação
validada reutilizou, por `retry`, o terminal criado e possuído pelo Orca antes de enviar a
tarefa.

Essa aprovação encerra somente a trilha sintética. Nenhum projeto real está liberado sem
novo gate explícito que fixe a versão do executor, confirme a inicialização automática,
revise as regras efetivas de permissão e repita um canário sintético. Não se deve
persistir `--new-project` ou qualquer outro argumento global sem revisão do impacto em
sessões existentes; bypasses e acesso fora do workspace continuam proibidos.

## Roteamento de executor, modelo e esforço

O Organizer opera sob **delegação bidirecional e simétrica** entre Codex (OpenAI) e
Antigravity (Google Pro AI). Cada execução deve fixar explicitamente `executor`,
`modelo`, `esforço`, `perfil de contexto` e `fallback: none`.

A orquestração pode se originar no Codex ou no Antigravity e direcionar o trabalho para
qualquer um dos 9 perfis materializados em `docs/orca-model-routing-profiles.json`.

Regras obrigatórias:

- **Simetria Operacional:** Uma sessão no Codex pode delegar para modelos do Codex
  (`gpt-5.6-luna`, `terra`, `sol`, `astra`) ou do Antigravity (`gemini-3.8-flash`,
  `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `gpt-oss-120b-medium`), e vice-versa;
- **Gestão de Cotas Semanais:** As cotas do Codex reiniciam semanalmente na segunda-feira.
  Quando a cota estiver esgotada, em fins de semana ou por preferência de preservação, a
  delegação redireciona prioritariamente para Antigravity (Claude Sonnet para código e
  Claude Opus para arquitetura), retornando ao Codex nos dias úteis com cota plena;
- **Guardião do GPT-5.6 Astra:** O modelo Astra é restrito a **exceções ultra-específicas**
  de impasses lógicos/arquiteturais extremos onde Sol e Opus falharem comprovadamente;
- preferência explícita de Erick prevalece quando o perfil existir e estiver disponível;
- disponibilidade deve ser consultada no executor no momento da execução;
- modelo desconhecido, incompatível ou indisponível encerra o lançamento com erro claro;
- `fallback: none` é o padrão; fallback automático exige autorização nominal e nunca
  ocorre durante uma escrita ativa;
- a troca de executor exige encerrar ou cancelar o worker anterior, confirmar ausência de
  processo ativo, verificar Git e produzir um pacote de passagem sanitizado;
- somente um worker escreve em cada checkout, inclusive quando os provedores forem
  diferentes;
- escolha de modelo não altera sandbox, allowlists, modo Manual ou capacidades do
  envelope;
- perfis devem ser locais ao projeto ou à execução. Argumentos globais persistentes são
  proibidos até revisão separada;
- consumo e limites pertencem ao provedor efetivamente usado e devem ser registrados
  quando observáveis, sem equiparar assinatura de aplicativo a cobrança de API.

### Catálogo Unificado e Especialidades

1. `organizer-codex-luna` (Codex / `gpt-5.6-luna` / `low`): tarefas mecânicas e templates;
2. `organizer-codex-economy` (Codex / `gpt-5.6-terra` / `medium`): implementação balanceada;
3. `organizer-codex-strong` (Codex / `gpt-5.6-sol` / `high`): subsistemas complexos;
4. `organizer-codex-astra` (Codex / `gpt-5.6-astra` / `extreme`): exceções críticas extremas;
5. `organizer-gemini-economy` (Antigravity / `gemini-3.8-flash-medium` / `medium`): coordenação ágil;
6. `organizer-gemini-strong` (Antigravity / `gemini-3.8-flash-high` / `high`): síntese densa;
7. `organizer-claude-sonnet` (Antigravity / `claude-sonnet-4-6` / `high`): código e testes de elite;
8. `organizer-claude-opus` (Antigravity / `claude-opus-4-6-thinking` / `high`): arquitetura e gates;
9. `organizer-gpt-oss` (Antigravity / `gpt-oss-120b-medium` / `medium`): auditoria aberta.

Nenhum item autoriza instalação, login, credenciais, cobrança, API em nuvem ou operação em
projeto real sem novo gate explícito.

O contexto comum usa um manifesto versionado: `AGENTS.md`, documentos centrais
obrigatórios, documentação viva do projeto alvo e somente os relatórios históricos
necessários. Ler todos os arquivos `.md` sem seleção não é requisito e aumenta custo e
risco de usar estado obsoleto. Skills específicas de um executor não são consideradas
compartilhadas apenas porque possuem formato Markdown.

O contrato dessa capacidade está em `ORCA_MODEL_ROUTING_CONTRACT.md` e os quatro perfis
estão materializados em `docs/orca-model-routing-profiles.json`. A trilha Antigravity e os
Quick Commands escopados ao repositório do Organizer (`<organizer-repo-id>`) foram validados no
canário sintético de 2026-09-17 (`PHASE_ORCA_MODEL_ROUTING_2026-09-17.md`). O timeout do Codex em
`hook: PreToolUse` foi investigado e estabilizado sinteticamente em 2026-09-18
(`PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md`) mediante o uso obrigatório de
`-c windows.sandbox=unelevated`. No entanto, em modo headless de turno único o Codex não acionou
ferramentas de leitura de arquivos; logo, a leitura de sentinelas pelo Codex e o pacote de passagem
automatizado entre provedores permanecem não validados em execução real, dependendo da futura
validação interativa via PTY no Orca. Projetos reais permanecem categoricamente bloqueados.

## Seleção de skills

O coordenador deve preferir skills do repositório para protocolos compartilhados por
Codex e Antigravity e skills pessoais para procedimentos exclusivos de um executor. As
sete skills do Organizer estão materializadas em `.agents/skills/` no formato portátil de
workspace e sincronizadas em `%USERPROFILE%\.codex\skills\` para o catálogo do Codex.

A descoberta e o canário somente leitura de `local-project-orientation` foram validados
com sucesso no Antigravity em 2026-09-18, e a paridade de instalação no Codex foi
confirmada no catálogo de usuário.

Coleção das 7 skills de coordenação:

| Skill | Função | Estado de Descoberta e Validação |
| --- | --- | --- |
| `local-project-orientation` | Confirmar projeto, raiz, instruções e baseline | Descoberta e canário aprovados no Antigravity; instalada no Codex |
| `phase-gate-reviewer` | Aprovar, bloquear ou pedir complemento de uma etapa | Descoberta no Antigravity e no Codex; canário aprovado no Codex |
| `implementation-prompt-builder` | Gerar prompt delimitado para o executor alvo | Descoberta no Antigravity e no Codex; canário aprovado no Codex |
| `local-ai-release-review` | Revisar higiene, documentação, commit e publicação | Descoberta no Antigravity e no Codex; canário aprovado no Codex |
| `local-project-coordinator` | Priorizar o portfólio e coordenar tarefas | Descoberta no Antigravity e no Codex; testada no Codex |
| `local-integration-architect` | Projetar contratos seguros entre sistemas e agentes | Descoberta no Antigravity e no Codex; testada no Codex |
| `model-router-advisor` | Selecionar executor, modelo e esforço por cota e tipo | Materializada em `.agents/skills/` e instalada no Codex |

A ausência dessas skills não impede a delegação: o coordenador pode seguir esta política e
o modelo de prompt manualmente. As skills operacionalizam o envelope concedido por Erick,
mas não ampliam esse envelope nem disponibilizam ferramentas inexistentes.

## Pré-requisitos operacionais

Antes de criar uma tarefa, confirme:

- o projeto alvo aparece entre os projetos salvos;
- a raiz correta foi resolvida no momento da ação;
- o usuário autorizou a criação da tarefa;
- não existe outra tarefa modificando o mesmo checkout;
- as skills citadas estão disponíveis no contexto do projeto alvo;
- o prompt contém escopo, exclusões, validações e condição de parada;
- dados pessoais, credenciais e identificadores de runtime não serão persistidos.

Se o projeto ainda não estiver salvo, informe isso a Erick. Não crie um repositório, não
invente um caminho e não use outro projeto como substituto.

## Limites do coordenador

O coordenador não pode:

- ampliar uma autorização por conta própria;
- garantir que uma tarefa terminou corretamente sem revisar evidências;
- tornar uma skill indisponível magicamente disponível apenas mencionando seu nome;
- contornar sandbox, permissões, autenticação ou políticas do sistema;
- operar continuamente sem um pedido atual ou uma automação explicitamente criada;
- resolver escolhas pessoais ou riscos relevantes sem consultar Erick.

# Contrato do piloto Orca

Atualizado em: 2026-09-18.

## Finalidade e estado

Este contrato define a integração experimental entre o `Local AI Organizer`, o Orca e os
agentes CLI Codex e Antigravity. A trilha do Codex foi validada em 2026-09-15. O primeiro
complemento do Antigravity foi bloqueado em 2026-09-16 por resolução incorreta do
worktree. O segundo complemento, concluído em 2026-09-17, comprovou em ambiente sintético
leitura confinada, bloqueio de escrita, escrita reversível, restauração e cancelamento de
worker supervisionado. O gate sintético está **APROVADO**, mas não autoriza uso em projeto
real; qualquer adoção exige novo gate explícito.

## Responsabilidades

| Componente | Responsabilidade |
| --- | --- |
| `Local AI Organizer` | Define projeto, objetivo, envelope, executor, evidências e gate |
| Orca | Inicia, acompanha, confina por worktree e interrompe processos gerenciados |
| Codex ou Antigravity | Executa somente o prompt, as permissões e o checkout atribuídos |
| Erick | Autoriza ampliações materiais, autenticação, instalação adicional e uso real |

O Orca é a camada operacional. Ele não decide sozinho qual projeto pode ser alterado nem
substitui a revisão de evidências do Organizer.

A extensão de roteamento de modelos está definida em `ORCA_MODEL_ROUTING_CONTRACT.md`
com perfis materializados em `docs/orca-model-routing-profiles.json`. A trilha Antigravity e
os Quick Commands escopados ao repositório foram validados no canário sintético de 2026-09-17
(`PHASE_ORCA_MODEL_ROUTING_2026-09-17.md`). Na trilha Codex, o timeout em PreToolUse foi
estabilizado sinteticamente com `windows.sandbox=unelevated`
(`PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md`), mas a leitura de sentinelas, o handoff
e a operação interativa via PTY permanecem como ainda não validados. O estado do piloto
continua restrito ao escopo sintético e mantém projetos reais bloqueados até o gate PTY.

## Dados e isolamento

- O piloto usa somente repositório descartável, dados sintéticos e worktrees separados.
- Um único agente pode escrever em cada checkout.
- Documentos pessoais, transcrições, outros projetos e credenciais ficam fora do escopo.
- Caminhos físicos, identificadores de runtime e conteúdo de autenticação não entram na
  documentação versionada.
- Arquivos de entrada e saída permitidos devem ser enumerados no prompt de cada worker.

## Permissões

- O Orca deve permanecer em modo Manual, sem argumentos padrão de bypass para Codex ou
  Antigravity.
- Leitura começa com sandbox somente leitura e sem rede quando aplicável.
- Escrita exige worktree descartável separado e fica limitada ao diretório de trabalho.
- Elevação administrativa, desativação de proteções e acesso irrestrito são proibidos.
- Autenticação existente pode ser reutilizada sem inspecionar, copiar ou registrar
  credenciais; novo login exige autorização no momento da ação.
- Instalação interativa, primeiro login e consentimentos são executados por Erick com
  orientação textual. O agente confirma versão, disponibilidade e configuração por CLI,
  arquivo ou log; controle direto de teclado e mouse não faz parte do piloto.
- O Organizer pode criar ou reconstruir os worktrees sintéticos, resolver seus caminhos,
  definir explicitamente o `cwd` do worker, iniciar e cancelar processos e configurar
  regras mínimas para comandos locais. O worker recebe o caminho absoluto validado como
  workspace e usa apenas caminhos relativos dentro dele.
- Para Antigravity headless, são permitidos `proceed-in-sandbox` ou allowlists específicas
  necessárias ao teste. Permanecem proibidos `always-proceed`,
  `--dangerously-skip-permissions`, curingas globais e acesso fora do workspace.

No Windows, o Codex precisou usar a implementação `unelevated` do sandbox para evitar a
configuração elevada. Isso não removeu o sandbox: o perfil somente leitura bloqueou uma
tentativa explícita de criação de arquivo. Em execução não interativa, `codex exec`
apresentou política de aprovação `never` mesmo quando `on-request` foi solicitado; assim,
o confinamento comprovado veio do sandbox, e a semântica interativa de aprovação continua
pendente de validação.

No segundo complemento com Antigravity, a configuração persistida do Orca permaneceu sem
argumentos ou variáveis padrão de bypass. `allowNonWorkspaceAccess` permaneceu no valor
efetivo falso. A inicialização headless com `--new-project` registrou o `cwd` exato do
worktree e permitiu usar somente `README.md` e `fixture.txt` como caminhos relativos. O
modo `request-review` autoautorizou arquivos dentro do workspace; uma regra de negação
específica bloqueou `forbidden.txt`. No worktree de escrita, ACLs temporárias do Windows
protegeram o diretório, `README.md` e `.git`, deixando somente `fixture.txt` gravável; as
ACLs foram restauradas ao final.

As allowlists exatas testadas com `toolPermission: strict` não autorizaram as operações
headless esperadas na versão observada e não devem ser tratadas como controle suficiente.
O cancelamento foi comprovado somente após o Orca reutilizar por `retry` um terminal que
ele próprio havia criado: o recurso ficou `owned/active`, `worker-stop` retornou `stopped`
e o PTY foi encerrado. A associação automática do projeto e a detecção inicial de
prontidão continuam requisitos de estabilização antes de qualquer adoção real.

## Ciclo operacional

1. Confirmar o repositório descartável e registrar hashes e estado Git inicial.
2. Iniciar leitura confinada e verificar que os hashes não mudaram.
3. Tentar uma escrita no perfil somente leitura e exigir rejeição verificável.
4. Promover para `workspace-write` apenas em outro worktree descartável.
5. Verificar alteração exata, ausência de efeitos colaterais e ausência de commit.
6. Restaurar a alteração e confirmar os hashes originais.
7. Provar cancelamento com um processo controlado e encerrar todos os terminais.
8. Repetir a sequência para cada agente antes de qualquer gate de adoção.

No Windows, o Antigravity deve receber `cwd` previamente verificado e `--new-project` na
inicialização. O evento inicial precisa confirmar o mesmo worktree antes de qualquer
prompt que use ferramentas.

Após no máximo três tentativas fundamentadas para a mesma falha, a execução deve parar e
registrar o bloqueio. Nenhum bypass pode ser usado como correção.

O relatório histórico original permanece em `PHASE_ORCA_PILOT_2026-09-15.md`. O resultado
do complemento do Antigravity está registrado separadamente em
`PHASE_ORCA_PILOT_COMPLEMENT_2026-09-16.md`. O resultado do segundo complemento está em
`PHASE_ORCA_PILOT_SECOND_COMPLEMENT_2026-09-17.md`.

## Evidências mínimas do gate

- versão e origem oficial do Orca;
- configuração Manual sem argumentos padrão de bypass;
- prompt, perfil de sandbox e resultado sanitizado de cada agente;
- hashes, estado Git e restauração dos arquivos sintéticos;
- prova de interrupção do processo gerenciado;
- custo observado ou declaração explícita de que o custo monetário é desconhecido;
- limitações, itens não executados e condição para retomada.

## Falhas e recuperação

- CLI ausente: bloquear somente a trilha afetada e solicitar novo envelope de instalação.
- Resolução incorreta do worktree: interromper o worker, preservar hashes, reconstruir o
  fixture se necessário, confirmar a raiz por Git, iniciar o processo com `cwd` absoluto
  validado e `--new-project`, e repetir usando caminhos relativos. Nunca ampliar o acesso
  para localizar o arquivo por tentativa e erro fora do workspace.
- Prontidão do Antigravity não detectada pelo Orca: não enviar tarefa às cegas; confirmar
  o prompt por saída textual e usar no máximo a recuperação supervisionada documentada.
  Persistindo a incompatibilidade, bloquear a adoção em vez de reutilizar terminal
  externo como prova de cancelamento.
- Mudança automática de versão: registrar a versão inicial e final, interromper novas
  ampliações do teste e exigir estabilização de versão antes do gate de projeto real.
- Login solicitado: parar e pedir autorização; nunca ler arquivos de credenciais.
- Sandbox incapaz de restringir escrita: bloquear o piloto inteiro.
- Worker fora do escopo: interromper, preservar evidências sanitizadas e revisar o estado.
- Escrita inesperada: interromper, comparar hashes e restaurar apenas o artefato sintético
  criado pelo piloto.

## Fontes oficiais verificadas

- Orca: `https://www.onorca.dev/docs/install`,
  `https://www.onorca.dev/docs/agents/supported` e
  `https://www.onorca.dev/docs/cli/reference`;
- Codex: `https://learn.chatgpt.com/docs/agent-approvals-security`;
- Antigravity: `https://antigravity.google/docs/cli-install`,
  `https://antigravity.google/docs/cli/permissions` e
  `https://antigravity.google/docs/cli/settings`,
  `https://antigravity.google/docs/cli/headless`,
  `https://antigravity.google/docs/cli/projects` e
  `https://antigravity.google/docs/cli/reference`.

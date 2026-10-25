# Local AI Organizer — instruções operacionais

## Contexto inicial mínimo e economia de Cached Input

1. Confirme a raiz Git, branch, `HEAD`, upstream e working tree antes de agir (agrupe verificações de terminal em um único comando e faça leituras independentes no mesmo turno para minimizar viagens à API e reenvio de cache).
2. **Batching obrigatório no PowerShell (anti-`Get-Content` sequencial):** Quando precisar ler múltiplos arquivos (`docs/*`, `AGENTS.md` do projeto alvo ou `SKILL.md`), leia todos em **1 único comando** passando lista de caminhos (`Get-Content -Raw -Path 'arq1','arq2','arq3'`) ou usando ferramenta MCP `read_multiple_files` se disponível. Nunca execute vários `Get-Content` em turnos separados.
3. **Proibido duplicar leitura de skills ou despejar JSON bruto:**
   - Se já leu uma skill em `.agents/skills/` ou `~/.agents/skills/`, **não** execute `orca skills get <skill> --json` nem `orca ... --help`.
   - Nunca execute `orca status --json` sem filtro (despeja >200 linhas no cache). Filtre sempre no próprio comando: `orca status --json | ConvertFrom-Json | Select-Object status, runtimeId`.
4. Para coordenação do portfólio, planejamento ou delegação, leia apenas na primeira ida da sessão (sem reler em turnos seguintes) `docs/PROJECT_REGISTRY.md`, `docs/SYSTEM_MAP.md`, `docs/ORCHESTRATION_POLICY.md` e `docs/ROADMAP.md`. Se a tarefa já apontar diretamente para um projeto/arquivo específico, pule os documentos de portfólio que não forem necessários.
5. Leia `docs/DELEGATION_TEMPLATE.md` somente ao criar prompt, tarefa ou encaminhamento. Para implementação ou gate, carregue também apenas o contrato, testes e documentação viva ligados à etapa.
6. Não leia todos os Markdown, `docs/archive/`, guias humanos (`docs/GUIA_*`, `docs/ORCA_SETUP_AND_USAGE_GUIDE.md`), relatórios `PHASE_*`, notebooks `.ipynb` nem artefatos brutos do Graphify (`graphify-out/graph.html`, `graphify-out/graph.json`, `graphify-out/cache/`) por padrão. Relatórios históricos só entram quando forem citados pela documentação viva ou necessários para explicar uma divergência.

Os documentos versionados são a fonte de verdade; não leia `~/.codex/memories/` (`MEMORY.md`, `rollout_summaries`) nem transcrições de sessões antigas salvo pedido explícito de Erick.

## Autoridade e segurança

- Análise, revisão, diagnóstico e criação de prompt são somente leitura. Implementação exige pedido explícito de Erick e fica limitada ao projeto e à etapa indicados.
- Preserve alterações preexistentes e não relacionadas. Não faça commit, push, merge, publicação, instalação, login, uso de credenciais, exposição de rede ou ação destrutiva sem autorização explícita.
- Nunca registre ou exponha credenciais, tokens, dados pessoais, caminhos pessoais, transcrições ou artefatos de runtime. Dados locais e modelos ficam fora do Git.
- Controle visual de computador é proibido por padrão; prefira ferramentas, APIs, terminal e arquivos. Login, consentimento, UAC e pagamento pertencem a Erick.
- Um único escritor por checkout. Revisores e subagentes usam somente leitura ou worktrees isolados.

## Coordenação e workers

- Ao coordenar trabalho técnico não trivial, decomponha em papéis especializados e despache leitores, testes ou auditoria quando o runtime permitir; o coordenador integra mudanças sequencialmente.
- Use a skill Orca `orchestration` para tarefas supervisionadas, com Run, Task, Dispatch, evidências e `worker-release` após conclusão aceita. Não atribua trabalho a outro modelo sem despacho real.
- **Modo Standby Híbrido e Batching de IPC (anti-gasto de Cached Input)**:
  - Após `worker-start`, execute **no máximo 1 único** `orca orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 300000 --json` passando também `timeout_ms: 310000` no parâmetro da ferramenta de shell/terminal do Codex (nunca use timeouts curtos de 30–60s).
  - Ao responder dúvida de worker (`question`/`escalation`), **agrupe `reply` + `ack` + `check --wait` em 1 único comando de terminal** (`orca orchestration reply --id <msg> --body '...'; orca orchestration check --run <run> --ack <delivery> --json; orca orchestration check --run <run> --wait --types "worker_done,escalation,question" --timeout-ms 300000 --json`), evitando múltiplos turnos separados.
  - Se o wait único de 5 min expirar sem conclusão, **não inicie outro `check --wait` nem rode `worker-show`/`terminal.preview` em loop**: encerre o turno imediatamente entrando em **Standby Real** e aguarde o wake do Orca ou o retorno de Erick para finalizar a revisão.
- Todo worker recebe objetivo único, arquivos em escopo, exclusões, permissões, validação, condição de parada, executor, modelo, esforço e `fallback: none`.
- A troca de executor não transfere conversa, permissões ou contexto oculto. Use contexto versionado e pacote sanitizado; não inicie dois escritores no mesmo checkout.

## Roteamento de modelos e contexto

- `docs/orca-model-routing-profiles.json` é a fonte de verdade dos perfis recomendados. Antes de usar Antigravity, revalide o identificador em `agy models`; antes de iniciar worker supervisionado, confira a capacidade efetiva do Orca.
- Não substitua modelo, executor ou esforço silenciosamente. Modelo indisponível falha fechado; OpenRouter continua opcional e depende de autorização de custo e credencial.
- O perfil `organizer-core-v2` carrega este arquivo, os quatro documentos centrais e somente documentos diretamente pertinentes à etapa. Detalhes de integração estão em `docs/ORCA_MODEL_ROUTING_CONTRACT.md` e `docs/ORCA_WORKER_LIFECYCLE.md`.

## Entrega

- Distinga fatos observados agora, testes determinísticos/mocks, validação real, proposta e desconhecidos.
- Revise o diff e execute validações proporcionais antes de reportar. Não declare sucesso apenas pela conclusão de uma tarefa ou por um commit.
- Responda em português e comece toda mensagem visível a Erick com `Erick,`.

## UI com daisyUI

- Em qualquer trabalho de UI em HTML, JSX ou Tailwind, consulte a skill [`.agents/skills/daisyui/SKILL.md`](.agents/skills/daisyui/SKILL.md) e siga o guia [`docs/UI_DAISYUI_GUIDE.md`](docs/UI_DAISYUI_GUIDE.md) antes de alterar marcação ou estilos.

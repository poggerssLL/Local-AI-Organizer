# Local AI Organizer

Este repositório mantém o contexto, as políticas e o roadmap usados pelo Codex para
coordenar os projetos locais de Erick. Ele não implementa silenciosamente trabalho nos
repositórios coordenados e não concede autoridade automática para alterá-los.

O antigo aplicativo de estudos com RAG foi removido deste repositório. Materiais pessoais
e dados locais remanescentes continuam fora do Git e não fazem parte do organizador.

## Documentação central

- [registro dos projetos](docs/PROJECT_REGISTRY.md);
- [mapa dos sistemas](docs/SYSTEM_MAP.md);
- [política de orquestração](docs/ORCHESTRATION_POLICY.md);
- [roadmap central](docs/ROADMAP.md);
- [modelo de delegação](docs/DELEGATION_TEMPLATE.md);
- [contrato do piloto Orca](docs/ORCA_PILOT_CONTRACT.md);
- [contrato de roteamento de modelos no Orca](docs/ORCA_MODEL_ROUTING_CONTRACT.md);
- [perfis materializados de roteamento](docs/orca-model-routing-profiles.json);
- [prompt do gate de roteamento no Orca](docs/PROMPT_ORCA_MODEL_ROUTING_IMPLEMENTATION.md);
- [relatório histórico do piloto Orca](docs/PHASE_ORCA_PILOT_2026-09-15.md);
- [relatório do gate de roteamento no Orca](docs/PHASE_ORCA_MODEL_ROUTING_2026-09-17.md);
- [complemento do gate de roteamento no Orca](docs/PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md).

O `AGENTS.md` instrui novos chats a ler esses documentos. Cada implementação em outro
projeto exige autorização explícita, uma tarefa delimitada no projeto correto e revisão
das evidências antes de liberar a etapa seguinte.

O Organizer prioriza conectores, APIs, terminal e arquivos. Quando uma etapa exigir
interface visual, Erick recebe instruções curtas para executá-la; controle direto de
teclado e mouse só é usado após pedido explícito e delimitado.

Em pilotos sintéticos explicitamente autorizados, o Organizer pode administrar a raiz
temporária, os worktrees, o diretório de trabalho, os processos e allowlists mínimas. Essa
autoridade não se estende a projetos reais, curingas globais ou bypass de permissões.

O roteamento de modelos disponibiliza perfis selecionáveis de Codex e Antigravity/Gemini
materializados em `docs/orca-model-routing-profiles.json` e registrados no Orca como Quick
Commands específicos por repositório. A seleção não transfere memória oculta entre
provedores: o contexto comum vem de `AGENTS.md`, dos documentos obrigatórios e de um pacote
de passagem sanitizado. O perfil padrão não possui fallback silencioso. A trilha Antigravity está validada em ambiente sintético; na trilha Codex, o timeout foi
estabilizado sinteticamente com `windows.sandbox=unelevated`
(`docs/PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md`), mas leitura de sentinelas, handoff
e operação interativa via PTY ainda não foram validados. Projetos reais permanecem bloqueados.

## Skills do fluxo

- `local-project-orientation`: confirma projeto, raiz e baseline;
- `implementation-prompt-builder`: cria o prompt e recomenda modelo e esforço;
- `phase-gate-reviewer`: aprova, bloqueia ou pede complemento;
- `local-ai-release-review`: revisa documentação, Git, commit e publicação;
- `local-project-coordinator`: coordena autorização, projeto, prompt, perfil de execução,
  workers e gate, inclusive em envelope autônomo delimitado;
- `local-integration-architect`: projeta contratos, permissões e gates entre projetos,
  orquestradores e agentes.

As skills pessoais ficam fora deste repositório e devem ser confirmadas no contexto em
que serão usadas. Nenhuma menção a uma skill autoriza instalação, delegação, commit ou
push.

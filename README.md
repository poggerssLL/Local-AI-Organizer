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
- [modelo de delegação](docs/DELEGATION_TEMPLATE.md).

O `AGENTS.md` instrui novos chats a ler esses documentos. Cada implementação em outro
projeto exige autorização explícita, uma tarefa delimitada no projeto correto e revisão
das evidências antes de liberar a etapa seguinte.

## Skills do fluxo

- `local-project-orientation`: confirma projeto, raiz e baseline;
- `implementation-prompt-builder`: cria o prompt e recomenda modelo e esforço;
- `phase-gate-reviewer`: aprova, bloqueia ou pede complemento;
- `local-ai-release-review`: revisa documentação, Git, commit e publicação;
- `local-project-coordinator`: integração futura do fluxo de coordenação.

As skills pessoais ficam fora deste repositório e devem ser confirmadas no contexto em
que serão usadas. Nenhuma menção a uma skill autoriza instalação, delegação, commit ou
push.

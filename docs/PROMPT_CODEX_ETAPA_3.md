# Encaminhamento da Etapa 3 — Local File Agent

Atualizado em: 2026-10-04.

O baseline de preparação confirmado foi `main`, commit `6d24cb0`, árvore limpa e
32 testes aprovados. Revalide o Git e a documentação do projeto alvo a cada tarefa;
este registro não comprova o estado de um checkout futuro.

O contrato e o prompt de execução pertencem ao repositório **Local File Agent**:
`AGENTS.md`, `FOUNDATION.md`, `PROJECT_STATE.md`, `ROADMAP.md`, `KNOWN_ISSUES.md` e
`PROMPT_CODEX_ETAPA_3.md`. Após a implementação, consulte também
`docs/PHASE_03_HASHES_AND_DUPLICATES_2026-10-04.md` e o gate independente registrado
na documentação viva. O Organizer não substitui essa fonte nem duplica o prompt.

## Envelope da etapa

- Hashes SHA-256 opcionais em blocos e agrupamento determinístico de duplicidades.
- Scanner permanece somente de metadados; hashing é uma operação separada e opt-in.
- Backend inicial Windows, com identidade e confinamento do objeto aberto verificados
  antes de ler conteúdo; capacidade ausente falha fechado, sem `realpath` + `open`
  como alternativa de segurança.
- Política conservadora para links, junctions, reparse points, placeholders e hardlinks.
- Desenvolvimento e testes somente em fixtures sintéticos autorizados; nenhum uso de
  arquivos pessoais, hidratação de nuvem, instalação, credencial ou rede pública.
- Um escritor por checkout; arquitetura, QA e gate com proveniência real de Dispatch.
- Código, testes e documentação podem ser escritos quando autorizados; leitura dos
  arquivos analisados não autoriza movimentação, alteração ou exclusão desses arquivos.
- Commit, push, publicação e avanço para a Etapa 4 exigem autorização própria.

## Coordenação

Use as skills de orientação, coordenação, construção de prompt, roteamento e gate,
conforme a tarefa. Para delegação supervisionada, carregue a skill `orchestration`
do CLI Orca selecionado e siga Run, Task, Dispatch, evidências e decisão de release.
Escolha o perfil versionado no instante do lançamento, confira `launch.effective`
e mantenha `fallback: none`.

O encaminhamento não autoriza relançar a implementação. Se a Etapa 3 já estiver
implementada na árvore de trabalho, revise a entrega existente e encaminhe somente
complementos delimitados. Separe testes com mocks, fixtures físicos, validação Windows
nativa e limitações pendentes; não transforme um teste pulado em validação aprovada.

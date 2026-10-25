---
name: local-project-coordinator
description: Coordene o próximo marco de projetos locais, resolvendo projeto, autorização, skills, prompt, executor, modelo, esforço, workers e gates. Use para priorizar, delegar, iniciar, acompanhar ou revisar; não amplie o envelope nem declare sucesso sem evidências.
---

# Coordenador de projetos locais

Coordene uma entrega por vez. A documentação central fornece contexto; o repositório alvo
é a fonte do baseline atual.

## Autoridade

Análise, planejamento e prompt são somente leitura. Só crie tarefa ou worker após pedido
explícito para delegar, criar ou iniciar. Um envelope autônomo pode reunir ações locais
reversíveis necessárias até o gate, mas não inclui implicitamente outro projeto,
credenciais, instalação de sistema, administração, rede pública, destruição, commit, push,
merge, publicação ou controle visual.

Use um escritor por checkout. Revisores operam somente leitura ou em worktrees separados.
Não persista IDs de runtime, caminhos temporários ou dados pessoais.

## Preparar e delimitar (com Batching de leitura)

1. Classifique o pedido e leia `AGENTS.md` e apenas os documentos centrais pertinentes em **um único comando consolidado** (`Get-Content -Raw -Path ...` ou `read_multiple_files`).
2. Localize o projeto exato sem inventar caminho.
3. Carregue as skills necessárias (`local-project-orientation`, `model-router-advisor`, `implementation-prompt-builder`) e o `AGENTS.md` do projeto alvo em **1 único comando em lote**, sem executar vários `Get-Content` em turnos separados e sem repetir `orca skills get <skill> --json` ou `--help` quando o `SKILL.md` local já foi lido.
4. Ao verificar prontidão do Orca, filtre o JSON (`orca status --json | ConvertFrom-Json | Select-Object status, runtimeId`) em vez de despejar o JSON completo no contexto.
5. Defina objetivo, aceite, escopo, exclusões, riscos, validações, documentação, envelope e parada; confirme que não há outro escritor.

## Executor e lançamento

Respeite a preferência de Erick e use somente perfis disponíveis. Escolha o menor perfil
proporcional ao risco e informe justificativa, alternativa e gatilho de escalada. Não faça
fallback silencioso.

- **Codex:** use tarefa persistente e projeto correto quando as ferramentas de tarefas
  estiverem disponíveis.
- **Antigravity/Orca:** use somente sessão, Quick Command, worktree e permissões já
  validados pelo contrato. Enquanto o gate interativo PTY estiver pendente, não promova o
  fluxo sintético para escrita ou delegação automática em projeto real.
- **Modelos adicionais no mesmo executor:** trate Gemini, Claude e GPT-OSS como modelos
  do Antigravity quando forem expostos por seu catálogo; não os registre como executores
  independentes.
- **Novo executor:** exija adaptador e gate próprios para descoberta, início, retomada,
  cancelamento, permissões, evidências e custo. Não reutilize silenciosamente a aprovação
  de Codex ou Antigravity.
- **API externa:** OpenRouter e provedores equivalentes exigem autorização separada para
  credencial, cobrança, privacidade e dados enviados.

Criar um prompt não autoriza lançá-lo. Criar um worker não autoriza commit ou push.

## Acompanhar e revisar (Standby Híbrido e Batching de IPC)

Após lançar um worker (`worker-start`), execute **no máximo 1 único** `orca orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 300000 --json` (5 min), definindo também `timeout_ms: 310000` na chamada da ferramenta de terminal para impedir loops de 45s. Ao responder a uma dúvida (`question`/`escalation`), encadeie `orca orchestration reply ...; orca orchestration check --ack ...; orca orchestration check --wait ...` em **1 único comando de terminal** para economizar turnos de cache. Se o wait único expirar e o worker continuar em execução, **não repita `check --wait` nem execute `worker-show`/`terminal.preview` em loop**: encerre o turno imediatamente em **Standby Real** e aguarde o wake do Orca ou o comando de Erick para revisar e executar `worker-release`. Cancele diante de fuga de escopo e envie complementos ao mesmo worker quando possível. Use `phase-gate-reviewer` no resultado e `local-ai-release-review` antes de commit ou push. Atualize roadmap somente após mudança factual comprovada e com escrita autorizada.

Consulte [o ciclo de coordenação](references/coordination-cycle.md) quando houver
delegação, acompanhamento ou troca de executor.

Comece a resposta com o estado principal e informe projeto, autorização, baseline,
skills, perfil, ação, evidências, limitações e próximo passo.

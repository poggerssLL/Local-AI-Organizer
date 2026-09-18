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

## Preparar e delimitar

1. Classifique o pedido e leia `AGENTS.md` e os documentos centrais.
2. Localize o projeto exato sem inventar caminho.
3. Use `local-project-orientation` para raiz, instruções, branch, HEAD, upstream, working
   tree e baseline.
4. Defina objetivo, aceite, escopo, exclusões, riscos, validações, documentação, envelope
   e parada.
5. Confirme que não há outro escritor e que as skills citadas foram descobertas pelo
   executor atual.
6. Use `implementation-prompt-builder` para prompt e perfil final.

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

## Acompanhar e revisar

Acompanhe sem polling excessivo, cancele diante de fuga de escopo e envie complementos ao
mesmo worker quando possível. Use `phase-gate-reviewer` no resultado e
`local-ai-release-review` antes de commit ou push. Atualize roadmap somente após mudança
factual comprovada e com escrita autorizada.

Consulte [o ciclo de coordenação](references/coordination-cycle.md) quando houver
delegação, acompanhamento ou troca de executor.

Comece a resposta com o estado principal e informe projeto, autorização, baseline,
skills, perfil, ação, evidências, limitações e próximo passo.

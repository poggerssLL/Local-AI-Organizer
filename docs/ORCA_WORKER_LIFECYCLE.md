# Ciclo de vida de workers do Orca

Atualizado em: 2026-10-04.

## Fato operacional atual

No Orca 1.4.219, `orca orchestration worker-start --model` declara suporte a IDs de modelo
para Antigravity. Em 2026-10-04, com Antigravity 1.2.16, dois canários supervisionados em
worktrees descartáveis passaram pela prontidão, receberam tarefa e concluíram por
`worker_done`; os terminais foram liberados e os worktrees removidos. O segundo canário
criou um único arquivo, confirmou seu conteúdo e executou `git diff --check` sem erros antes
da limpeza.

Essa é evidência real limitada a fixture. Ela não homologa todos os modelos, não transfere
permissões e não autoriza escrita, commit, push ou dados de projetos reais.

## Contrato fail-closed

| Necessidade | Caminho permitido | Evidência exigida | Limite |
| --- | --- | --- | --- |
| Worker Codex com modelo fixo | `worker-start --agent codex --model ... --effort ...` | `launch.effective`, `worker_done` e `worker-release` | Um escritor por checkout |
| Worker Antigravity com modelo fixo | `worker-start --agent antigravity --model ... --effort ...` | `agy models`, `launch.effective`, `worker_done`, `worker-release` e Git | Revalidar por Dispatch; fixture não promove projeto real |
| Terminal Antigravity reutilizado | `worker-start --terminal <handle>` após prontidão | identidade efetiva, `worker_done` e release | Modelo é herdado e deve ser declarado |

Não use `--sandbox` para tentar liberar o executável do Orca fora do workspace e não
remova sandbox para contornar limitações. Uma sessão manual não pode ser relatada como
Dispatch supervisionado. Escrita em projeto real continua dependente de autorização explícita
e gate próprio; use `CODEX_ANTIGRAVITY_COLLABORATION.md` quando houver mais de um executor.

## Encerramento obrigatório

Para cada Dispatch aceito, o coordenador processa `worker_done`, revisa a evidência e usa
`worker-release --dispatch <id>`. Para falha de prontidão, siga o `nextAction` de
`worker-list`; se indicar release, use `worker-release`, nunca `terminal close`. Ausência
de status não prova encerramento e não autoriza repetir, abandonar ou liberar por conta
própria.

## Validação antes de promoção

1. Execute `agy models` e valide cada ID Antigravity materializado.
2. Execute `orca orchestration worker-start --help` e verifique a capacidade real de
   lançamento para o executor escolhido.
3. Em fixture descartável, prove `launch.effective`, tarefa aceita, `worker_done`,
   `worker-release`, zero workers reclaimable e Git limpo.
4. Para escrita reversível, valide também a alteração permitida e a verificação Git indicada.
5. Antes de um projeto real, revalide o projeto, o baseline, o modelo efetivo, o escopo e o
   único escritor; não promova automaticamente a evidência da fixture.

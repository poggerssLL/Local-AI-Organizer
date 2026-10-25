# Ciclo de vida de workers do Orca

Atualizado em: 2026-10-24 (histórico de ondas e preflights arquivado em `docs/archive/ORCA_WORKER_LIFECYCLE_HISTORY_2026-10-07.md`).

## Contrato fail-closed

| Necessidade | Caminho permitido | Evidência exigida | Limite |
| --- | --- | --- | --- |
| Worker Codex com modelo fixo | `worker-start --agent codex --model ... --effort ...` | `launch.effective`, `worker_done` e `worker-release` | Um escritor por checkout |
| Worker Antigravity com modelo fixo | `worker-start --agent antigravity --model ... --effort ...` | `agy models`, `launch.effective`, `worker_done`, `worker-release` e Git | Revalidar por Dispatch; fixture não promove projeto real |
| Terminal Antigravity reutilizado | `worker-start --terminal <handle>` após prontidão | identidade efetiva, `worker_done` e release | Modelo é herdado e deve ser declarado |

- O campo `permissions_profile` é contrato declarativo, não imposição de sandbox. Revalide permissões efetivas antes de outro escritor; confiança no diretório não autoriza bypass.
- Nunca converta falha de IPC em sucesso nem envie `worker_done` em nome do worker.
- Não use `--sandbox` para tentar liberar o executável do Orca fora do workspace e não remova sandbox para contornar limitações. Uma sessão manual não pode ser relatada como Dispatch supervisionado.
- Escrita em projeto real continua dependente de autorização explícita e gate próprio; use `CODEX_ANTIGRAVITY_COLLABORATION.md` quando houver mais de um executor.

## Encerramento obrigatório e economia de Cached Input

1. Para verificar prontidão do Orca sem poluir o cache, filtre sempre: `orca status --json | ConvertFrom-Json | Select-Object status, runtimeId`.
2. Após `worker-start`, execute **no máximo 1 único** `orca orchestration check --run <run> --wait --types "worker_done,escalation,question" --timeout-ms 300000 --json` (com `timeout_ms: 310000` na tool de shell).
3. Ao responder `question`/`escalation`, **encadeie na mesma linha**: `orca orchestration reply --id <msg> --body '...'; orca orchestration check --run <run> --ack <delivery> --json; orca orchestration check --run <run> --wait --types "worker_done,escalation,question" --timeout-ms 300000 --json`.
4. Para cada Dispatch aceito, o coordenador processa `worker_done`, revisa a evidência e usa `worker-release --dispatch <id>` (nunca `terminal close`). Se o wait único de 5 min expirar sem conclusão, entre imediatamente em **Standby Real**.

## Validação antes de promoção

1. Execute `agy models` e valide cada ID Antigravity materializado.
2. Em fixture descartável, prove `launch.effective`, tarefa aceita, `worker_done`, `worker-release`, zero workers reclaimable e Git limpo.
3. Antes de um projeto real, revalide o projeto, o baseline, o modelo efetivo, o escopo e o único escritor; não promova automaticamente a evidência da fixture.

# Canário de worker Antigravity — 2026-10-03

## Resultado

**BLOQUEADO:** o Orca criou worktree filho descartável e tentou iniciar um worker
Antigravity sem preferência de modelo, pois a versão atual do Orca não aceita `--model` para
esse executor. O terminal chegou ao prompt de confiança do Antigravity, mas não aceitou a
tarefa e o Orca encerrou a tentativa em `agent_readiness` com `agent-trust-workspace`.

## Evidência observada

- validação real: o terminal Antigravity 1.2.16 exibiu o prompt de confiança para a fixture;
- não houve `worker_done`, escrita, commit, push, instalação, bypass ou relaxamento de
  sandbox;
- o terminal foi liberado pelo ciclo `worker-release` e o worktree temporário foi removido;
- o checkout principal permaneceu fora do escopo do canário.

## Próximo passo permitido

Erick precisa confirmar visualmente a confiança em uma nova fixture descartável. Depois, o
canário deve repetir apenas leitura e provar modelo efetivo, `worker_done`, `worker-release`,
zero workers reclaimable e Git limpo. Até esse gate, modelos Antigravity fixos seguem apenas
no caminho manual somente leitura.

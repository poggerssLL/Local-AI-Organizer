# Ciclo de vida de workers do Orca

Atualizado em: 2026-10-03.

## Fato operacional atual

No Orca 1.4.203, `orca orchestration worker-start --model` declara suporte a IDs de
modelo de Claude, Codex e Cursor; ele não aceita preferência de modelo para
Antigravity. Em 2026-10-03, um lançamento supervisionado `--agent antigravity` chegou
ao terminal Antigravity 1.2.16, mas falhou em `agent_readiness` antes de aceitar a tarefa.
Portanto, não há prova atual de ciclo supervisionado confiável para iniciar um modelo
Antigravity escolhido pelo perfil.

## Contrato fail-closed

| Necessidade | Caminho permitido | Evidência exigida | Limite |
| --- | --- | --- | --- |
| Worker Codex com modelo fixo | `worker-start --agent codex --model ... --effort ...` | `launch.effective`, `worker_done` e `worker-release` | Um escritor por checkout |
| Antigravity já pronto em terminal reconhecido | `worker-start --terminal <handle>` somente após prontidão | identidade efetiva, `worker_done` e release | Modelo é herdado; não alegar modelo fixo |
| Perfil Antigravity com modelo fixo | sessão manual, somente leitura, com `agy --model <id>` e contexto sanitizado | `agy models`, saída sanitizada e Git | Não é worker supervisionado e não chama `worker_done` |

Não use `--sandbox` para tentar liberar o executável do Orca fora do workspace e não
remova sandbox para contornar essa limitação. Em especial, uma sessão manual com modelo
fixo não pode ser relatada como Dispatch supervisionado. Escrita, commit e projetos reais
continuam fora desse caminho até um novo gate que prove prontidão, identidade, conclusão e
limpeza ponta a ponta.

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
3. Em fixture descartável, prove `launch.effective`, leitura permitida, `worker_done`,
   `worker-release`, zero workers reclaimable e Git limpo.
4. Somente então considere escrita reversível; não promova esse resultado para projeto real.

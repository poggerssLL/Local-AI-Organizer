# Ciclo de vida de workers do Orca

Atualizado em: 2026-10-04.

## Fato operacional atual

Preflight restrito 2026-10-05: Gemini 3.8 Flash high com `--sandbox --mode plan`
recebeu Task/Dispatch e revisou código, mas `check` e `worker_done` falharam com
`runtime_access_denied / EPERM`. Não houve bypass; a Task foi marcada failed após
turno final observado. O launcher padrão Codex abriu em YOLO com prompt no
composer e foi cancelado antes do início. Uma sessão custom Codex com
`--sandbox read-only --ask-for-approval never` iniciou e produziu transcript/liveness
observáveis. Isso não homologa o launcher padrão nem o IPC do Gemini.
Veja [preflight e limites](ORCA_RELIABILITY_PREFLIGHT_2026-10-05.md).

O campo `permissions_profile` é contrato declarativo, não imposição de sandbox.
Revalide permissões efetivas antes de outro escritor; confiança no diretório não
autoriza bypass. Quando `worker-start` não expressar argv restrito, use terminal
custom e `worker-start --terminal` conforme low-level-topology, registrando o
modelo/effort observado sem inventar `launch.effective`. Nunca converta falha de
IPC em sucesso nem envie `worker_done` em nome do worker.

No Orca 1.4.219, `orca orchestration worker-start --model` declara suporte a IDs de modelo
para Antigravity. Em 2026-10-04, com Antigravity 1.2.16, dois canários supervisionados em
worktrees descartáveis passaram pela prontidão, receberam tarefa e concluíram por
`worker_done`; os terminais foram liberados e os worktrees removidos. O segundo canário
criou um único arquivo, confirmou seu conteúdo e executou `git diff --check` sem erros antes
da limpeza.

Essa é evidência real limitada a fixture. Ela não homologa todos os modelos, não transfere
permissões e não autoriza escrita, commit, push ou dados de projetos reais.

## Observação de lançamento na Etapa 3

Na execução supervisionada da Etapa 3 do Local File Agent, em 2026-10-04,
os recibos confirmaram Sol 6.1 em `medium`/`high` e Opus 5.5 em `high`.
Houve retornos `outcome_unknown` em `turn_start_unobserved`: entrada aceita
não comprovou início do turno. Em alguns terminais Codex, o prompt permaneceu
no campo de entrada; no auditor Antigravity, a leitura já mostrava trabalho ativo.
Isso limita a alegação de lançamento automático sem intervenção, mesmo com
o runtime conectado e pronto.

Inspecione o Dispatch e a saída antes de agir. Se um rascunho pendente for
positivamente identificado, a submissão do mesmo rascunho por entrada de terminal
não deve reenviar a tarefa nem criar outro worker. Silêncio ou timeout não
autorizam retry. Após mudança do runtime, use a recuperação e o `nextAction`
literal; não reutilize handles obsoletos. Um terminal protegido por
`user_takeover` permanece retido quando o release assim decidir.

Ao encerrar esse Run, arquitetura, QA, escritor e auditor tinham `worker_done`
aceito. O gate inicial independente confirmou 65 testes (64 aprovados, 1 skip);
após complementos, o coordenador reexecutou 67 (66 aprovados, o mesmo skip).
QA, auditor e a tentativa anterior falha do escritor foram liberados. Arquitetura
e escritor concluído receberam `retained/user_takeover` no release; não houve
fechamento forçado. A consulta do Run retornou zero `reclaimable`, sem alegar
que todos os processos saíram. O contrato de coordenação e ask/reply funcionou;
a observação automática de lançamento permaneceu incompleta e exigiu inspeção.

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

Fechamento do preflight restrito da Etapa 4: gate técnico da API aprovado via
transcript, 20 testes puros pass, mas nenhum worker_done durável. Orca não foi
resolvido no Codex readonly inclusive pelo mesmo caminho qualificado verificado
pelo coordenador; não atribuir causalidade somente ao PATH. Gemini teve EPERM no
IPC. Quatro Tasks failed operacionalmente, zero ativos/reclaimable; registros
retained preservados. A distinção entre gate técnico e lifecycle é obrigatória.

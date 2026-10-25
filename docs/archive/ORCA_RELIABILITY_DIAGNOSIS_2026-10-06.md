# Orca — diagnóstico da onda paralela

Data: 2026-10-06. Organizer baseline `b92139d`; Orca 1.4.219, agy 1.2.17.
User autorizou quatro frentes paralelas. Três leitores Gemini 3.8 Flash high foram
lançados em terminais custom `--sandbox --mode plan`, com Run/Task/Dispatch reais;
coordenador OpenAI foi o único escritor de source/docs, sem substituir workers.
Modelo herdado foi confirmado na criação/tela; launch.effective de reutilização
é null e não constitui confirmação de um novo lançamento por perfil.

## Evidência e novo diagnóstico causal delimitado

O runtime respondeu ready/connected ao coordenador. Workers reproduziram
runtime_access_denied/EPERM no IPC; os trabalhos textuais foram observados por
terminal, com provider transcript ausente/missing_status. Check/send aceitos pelo
coordenador não comprovam recepção do follow-up dentro do sandbox do worker.

Inspeção somente leitura do código instalado, sem modificar binário ou configuração:

- `out/cli/runtime/metadata.js`: lê metadata e exige transporte unix/named-pipe.
- `out/cli/runtime/transport.js`: findTransport(metadata, unix, named-pipe) e
  node:net.createConnection(transport.endpoint). O caminho local não escolhe TCP
  ou WebSocket automaticamente, mesmo se outro endpoint existir no runtime.
- `out/cli/runtime/client.js`: WebSocket pertence ao ramo de remotePairing; a via
  local usa sendRequest. Não copiar tokens, criar pairing nem alterar transporte
  para contornar o sandbox.
- `out/cli/runtime/runtime-access-denied.js`: classifica EPERM/EACCES com processo
  vivo como runtime_access_denied. CODEX_SANDBOX altera a mensagem, não a causa.
  Reiniciar Orca não concede acesso ao cliente bloqueado.

Isso localiza a falha na conexão local restrita ao named pipe. A regra concreta
que nega a conexão e uma allowlist mínima suportada pelo agy não foram demonstradas.
Não é evidência de processo Orca morto nem ausência simples de PATH. A correção
suportada exige integração/permissão para esse IPC, mantendo o restante restrito;
o binário instalado não foi patchado e nenhuma solução foi homologada neste marco.

## Critério de saída do bloqueio

1. Mecanismo oficialmente suportado para o IPC mínimo com sandbox mantido.
2. Canário somente leitura em fixture descartável, Gemini 3.8 Flash high,
   fallback none, sem dados reais nem autorização de escrita herdada.
3. Task/Dispatch efetivos, check, worker_done originado no próprio worker e
   worker-release aceitos; sem enviar lifecycle em nome do executor.
4. Só depois promover novo escritor supervisionado em checkout isolado autorizado.

Gate de confiabilidade: COMPLEMENTO NECESSÁRIO. As entregas locais de fixture,
contrato e diagnóstico não homologam o lifecycle nem substituem o canário.

## Permissão negada na manutenção automática Git

git worktree prune --dry-run --verbose identificou dois registros antigos cujo
arquivo gitdir não existe. Isso explica por que são candidatos a prune; não
comprova a causa de Permission denied ao removê-los. Não houve prune efetivo,
remoção, mudança de atributo/ACL ou configuração Git. Worktrees ativos preservados.

## Governança e limites

Fonte/segredos de provider, saídas brutas, IDs de runtime/Task/Dispatch e paths pessoais
não entram no Git. Artefatos automáticos do provider são externos e não são patches
no projeto; não foram promovidos para autoridade de lifecycle. Falha de sandbox em
consulta de serviço/processo não prova que esse serviço está desligado fora dele.
Sem bypass, YOLO, restart, hook install, settings globais, credenciais/pairing,
publicação ou controle visual. Encerramento/contabilidade final registrados abaixo
somente após turno final observado e fencing dos attempts sem settlement durável.

## Gate e contabilidade final

Três turnos finais observados; zero worker_done durável. Os três Dispatches foram
abandoned pelo coordenador por falha operacional de IPC e as três Tasks registradas
failed com resultado factual, sem declarar settlement de sucesso. Três recursos
retained; consulta scoped confirmou zero reclaimable. Nenhum processo foi fechado
ou recurso eliminado. Isso não significa ausência de processos vivos.

Proposta Gemini de liberar ACL para classes amplas de processos e wildcard de pipe
não foi aceita como mecanismo mínimo suportado. Não foram inspecionados token real
e DACL para provar a causa interna, nem se comprovou suporte à configuração sugerida.
Não prometer isolamento absoluto ou causalidade de AppContainer sem essa evidência.
A parte confirmada é o transporte local e a negação de conexão. Artefatos/scratch
do provider ficaram externos; nenhuma alteração no binário instalado ocorreu.

File Agent: revisão textual apoiou contrato/fixture; suíte nativa no sandbox teve
PermissionError e não substitui clone novo 90/89/1 do coordenador. Transcriber:
assertiva de daemon parado foi rejeitada pela consulta loopback positiva do host.
Gate técnico local e falha de lifecycle são resultados distintos.

## Confiança do workspace Uso Geral

Erick confirmou explicitamente a confiança nessa pasta. O terminal já estava fora
do prompt de confiança ao ser inspecionado; não foi reenviada uma confirmação cega.
Pergunta pontual respondida pelo Gemini 3.8 Flash high com somente Read de AGENTS.md,
sem outros documentos, escrita ou rede. Isso valida o fluxo de uso direto da sessão,
sem Run/Task/Dispatch: não é canário de IPC nem homologação de worker supervisionado.
Nenhuma flag de sandbox ou permissão global mudou.

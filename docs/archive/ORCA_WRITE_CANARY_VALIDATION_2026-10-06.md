# Orca: canário de escrita isolado (2026-10-06)

## Resultado observado e pendência

Três Tasks e despachos reais no mesmo Run: auditor de contrato File Agent,
reviewer Transcriber e escritor de canário. Modelo Antigravity
`gemini-3.8-flash-high`, esforço high, sandbox, `fallback: none`.
Coordenador OpenAI integrou File Agent e executou validação nativa Transcriber;
leitores não escreveram nos projetos principais. Único escritor por checkout.

Canário usou clone local separado do Organizer `b92139d` e AGENTS curto,
restrito a um arquivo sintético. Primeira prontidão falhou no trust do checkout;
confiança já concedida por Erick foi aplicada somente à fixture. Retry explícito
no mesmo Task ficou ready/input_accepted. Worker criou `canary-result.txt`;
coordenador conferiu bytes exatos `ORCA_WRITE_CANARY_OK` mais LF (21 bytes).
Alterações locais esperadas: AGENTS preparado pelo coordenador e arquivo novo
pelo worker. `git diff --check` não cobre arquivo untracked; bytes foram
verificados separadamente. Nenhum commit, push, dado real ou writer de produção.

Os três workers chegaram à confirmação de bypass somente para os próprios
comandos `orca orchestration send ... --type worker_done`. Consentimento
específico solicitado a Erick; ainda não recebido. Não há worker_done durável,
release ou ack desta onda. Não declarar Tasks completed pela saída do terminal.

## Permissões e limites

Política temporária proceed-in-sandbox e exceções de IPC restritas aos três
terminais foram preparadas com backup fora do Git, sem ACL/PATH/wildcards.
Um pedido fora do escopo para `send --help` foi recusado, e o reviewer recebeu
correção de instrução sob o mesmo Dispatch. Cards finais concretos conferidos.
A autorização antiga para done de outro canário não foi ampliada implicitamente.

As 12 exceções de IPC desta onda foram removidas; config compartilhada voltou
byte por byte ao backup. A chave de política foi restaurada ao valor anterior,
preservando a confiança da fixture autorizada por Erick. Backups mantidos fora
do Git. A política antiga não homologa isolamento; os cards já abertos continuam
aguardando consentimento individual, sem autorizar execução automática.

Depois do consentimento: aprovar cada comando uma única vez, receber/revisar
os três done, worker-release por Dispatch, ack dos delivery IDs e conferir
Tasks/resource states. Terminais externos podem ficar retained, sem confundir
com recurso reclaimable. Tentativa inicial failed é separada do retry ativo.

Escrita correta da fixture foi provada, mas gate de lifecycle permanece pendente.
Sandbox pura e launcher padrão não homologados. Writer de produção exige nova
revalidação de projeto/baseline/modelo/escopo. Sem instalação de plugin ou liberação
persistente de sandbox. IDs e configurações detalhadas ficam fora do Git.

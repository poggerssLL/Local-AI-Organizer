# Validação do reparo delimitado de IPC

Data: 2026-10-06. Baseline Organizer b92139d; Orca 1.4.219 e Antigravity CLI 1.2.17.

## Resultado atual

O Transcriber teve o reparo reversível 8E concluído, pip check sem aviso e
26 testes de resumo/API aprovados com mocks. O Orca está conectado e pronto,
e o canário supervisionado readonly concluiu com exceções específicas de IPC.
O acesso na sandbox pura continua bloqueado; não há liberação geral do runtime.
Não houve alteração de binário, ACL de pipe, credenciais, PATH ou exposição de rede.

## Evidências e limites do IPC

1. A documentação oficial suporta regras `unsandboxed(comando)` para exceções
   específicas, mantendo a sandbox nos demais comandos. Isso executa o comando
   autorizado no host; não libera o named-pipe dentro da sandbox pura.
2. Foi realizado Run/Task/Dispatch real com Gemini 3.8 Flash high e fallback none.
   O primeiro canário operador-criado enviou worker_done succeeded pelo próprio
   agente; release retornou retained/no_owned_resource, sem ação de processo.
   A sessão herdou always-proceed e não homologa o perfil restrito.
3. Um segundo canário foi iniciado por worker-start em terminal custom reutilizado,
   com sandbox, mode plan e política request-review. launch.effective fica null
   para reutilização; a identidade/modelo foi conferida na sessão, sem inventar recibo.
4. O comando check na sandbox pura continuou retornando EPERM. Após instrução
   explícita para usar a opção suportada de execução fora da sandbox somente nesse
   comando, o agente relatou check positivo. A conclusão worker_done ficou
   aguardando consentimento específico no terminal; Erick autorizou somente essa
   conclusão, e foi escolhida a opção de execução única, sem permissão persistente.
   O próprio Gemini enviou worker_done succeeded e a Task foi concluída pelo Orca.
5. Consentimento foi solicitado a Erick porque AGENTS.md reserva consentimentos
   a ele. A confiança anterior do workspace não foi tratada como liberação geral.
   O segundo worker_done foi conferido com ambos os IDs ativos antes de release
   e ack. Release retornou retained/external_terminal, sem fechar o processo.

## Configuração temporária e reversão

Os logs mostraram composição de configurações da CLI e da configuração
compartilhada (`~/.gemini/antigravity-cli/settings.json` e
`~/.gemini/config/config.json`). A primeira gravação de teste não carregou as
permissões esperadas; o replay com escrita UTF-8 sem BOM e grants compartilhados
carregou as regras. Não atribuir a diferença somente a um dos arquivos.
Ambos receberam backup local antes de alteração; backups não são versionados.
O teste usa somente regras de command/unsandboxed para check do próprio handle e
worker_done do próprio handle. Sem wildcard, regex ampla ou permissão a todo Orca.
O matching de prefixo do done não dispensou o consentimento no perfil request-review;
a existência da regra no JSON não prova sua efetividade para comandos com aspas.
A política antiga always-proceed foi temporariamente trocada por request-review.

Encerramento observado: dois Tasks completed por worker_report/succeeded; ambos
os releases processados, ambas as entregas reconhecidas e zero reclaimable no Run.
Dois terminais retained, sem alegar ausência de processos vivos. As dez regras
temporárias foram removidas, e os dois arquivos de configuração foram restaurados
byte por byte aos backups. Durante a execução, o campo de política temporária na
CLI foi removido; somente esse campo diferia do backup e foi restaurado. A causa
interna dessa regravação não foi demonstrada. Não ficou permissão nova global.

## Próximos marcos

- Canário readonly com exceções de IPC aprovado; launcher padrão e escrita real
  seguem sem homologação. O teste não conserta o acesso ao pipe dentro da sandbox.
- Provisionar exceções por terminal/despacho e verificar consentimento/matching,
  sem promover o teste always-proceed a prova de isolamento.
- File Agent: contrato/fake da Etapa 5; Transcriber: validação sintética real
  CPU/CUDA/Ollama com modelos existentes; Uso Geral já disponível.
- Plugins: seleção por lacuna concreta, conforme PLUGIN_AND_MCP_OPTIONS.md;
  nenhum plugin instalado nesta tarefa.

Fontes oficiais:
- [Permissões Antigravity](https://www.antigravity.google/docs/permissions?tab=cli)
- [Sandbox Antigravity](https://antigravity.google/docs/sandbox?tab=cli)

Este registro não contém IDs de runtime, caminhos pessoais absolutos ou transcrições.
Sem commit ou push nesta manutenção.

## Procedimento para o próximo despacho

Criar terminal custom sem iniciar o agente, preparar backup e permissões mínimas
para aquele handle e confirmar a política efetiva antes de carregar Gemini. Usar
worker-start --terminal para a posse supervisionada e registrar modelo herdado.
Instruir o worker a solicitar execução fora da sandbox somente para os comandos
de IPC autorizados quando necessário. Se aparecer consentimento não coberto pelo
matching, obter aprovação específica de Erick, sem ampliar o prefixo ou selecionar
a opção persistente. Conferir done/release/ack e retirar grants ao encerrar.
Esse procedimento é uma mitigação validada, não correção do binário ou garantia
de orquestração sem consentimento em todos os executores.

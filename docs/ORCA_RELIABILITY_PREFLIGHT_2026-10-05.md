# Orca — Preflight restrito da Etapa 4

Data: 2026-10-05. Orca 1.4.219; Antigravity CLI 1.2.17;
Codex gerenciado 0.160.0. Complemento ao diagnóstico anterior, preservado.
Envelope: Etapa 4 File Agent e manutenção paralela Transcriber/Orca, autorizadas
por Erick. Gemini 3.8 Flash high prioritário; OpenAI reservado ao gate complexo
de segurança/compatibilidade. Claude não usado. Nenhum fallback silencioso.

## Fatos observados

| Verificação | Resultado | Limite |
| --- | --- | --- |
| Runtime | Ready e connected; novo Run vinculado | Não prova worker ativo nem confiabilidade geral |
| Modelo Antigravity | ID gemini-3.8-flash-high revalidado em agy models | Catálogo sozinho não prova despacho |
| Terminal custom Gemini | --sandbox --mode plan, sem dangerously-skip-permissions | Não é allowlist completa de leitura de todos os tools |
| Confiança da pasta | Confirmação solicitada; Erick autorizou; opção confirmada | Não autorizou bypass, instalação ou mudança global |
| Despacho Gemini | Task/Dispatch reais, input_accepted e revisão textual observados | turnStart unsupported, transcript ausente, missing_status |
| Lifecycle Gemini restrito | check e send worker_done negados com runtime_access_denied / EPERM | Restrição do sandbox/OS ao IPC; não prova bug no binário Orca |
| Final Gemini | Turno final e prompt idle observados, sem worker_done durável | Dispatch abandonado pelo coordenador; Task failed; terminal preservado |
| Lançamento padrão Codex | Modelo/effort efetivos corretos, mas tela YOLO mode e prompt no composer | Perfil scoped-readonly do catálogo não impôs sandbox técnico |
| Cancelamento desse Codex | Antes do início observado; worker-stop fechou somente o terminal criado | Task failed; worker-release confirmou released; sem gate |
| Novo Codex custom | --sandbox read-only --ask-for-approval never, modelo Sol 6.1 high | Flags da sessão explicitadas; nenhuma configuração global alterada |
| Novo despacho restrito | turn_started observado; transcript real e liveness fresh/live | Apenas esse despacho; gate final registrado após settlement |
| Testes puros independentes | 19 testes da classificação aprovados, exit 0; diff-check exit 0 | Suíte nativa completa executada pelo coordenador, não pelo reviewer readonly |

Consulta de hooks: enabled, hooks Codex presentes; Antigravity reportado
not_installed/managedHooksPresent false. Um processo Antigravity preexistente
mostrava ausência de sandbox e flag bypass; não foi reutilizado, alterado ou
encerrado. Esses fatos justificam o preflight, mas não demonstram causalidade
de missing_status/EPERM. Nenhum hook foi instalado nem configuração global mudou.

## Controles aplicados

- Checkouts Git isolados fora de diretório sincronizado; baseline publicado do
  File Agent confirmado. Transcriber recebeu somente source/docs allowlisted,
  com verificação de hashes, sem copiar runtime, mídias, caches ou venv.
- Um escritor: coordenador. Workers revisaram somente; não receberam limpeza.
- Regras de confiança/permissão vieram da confirmação real no terminal e da
  escolha explícita do usuário; não se respondeu a prompts desconhecidos.
- Modelo/effort de terminais reutilizados custom são comprovados pela criação e
  sessão observada. launch.effective null desses recibos não foi apresentado
  como confirmação de lançamento novo.
- Sem falso worker_done pelo coordenador. Falha de IPC encerrou autoridade
  conforme recovery-and-cleanup após turno final observado, preservando recursos.
- Cancelamento do Codex padrão foi decisão explícita por perfil incompatível,
  baseada na tela real e draft. Timeout sozinho não autoriza cancelar/repetir.

## Pendências e conclusão delimitada

Gemini com sandbox não está habilitado para lifecycle supervisionado nesta
configuração: é preciso permitir apenas o IPC necessário por mecanismo suportado
ou corrigir a integração, sem liberar execução geral. A causa interna e uma
configuração mínima suportada ainda não foram demonstradas. Não remover sandbox,
habilitar YOLO, instalar hooks, alterar settings globais ou prometer confinamento
apenas pelo texto do prompt como solução automática.

O lançamento padrão do Orca precisa de preflight de permissões além de modelo,
effort e readiness; pode abrir em YOLO e deixar o prompt no composer. O comando
custom mostrou início observado e telemetria no Codex restrito, mas não homologa
o catálogo nem todos os executores. Nenhum código do Orca foi alterado.

Evidência operacional completa requer worker_done aceito e decisão de release;
o estado final do gate e da frota deve ser consultado após seu encerramento.
Identificadores, saídas pessoais, artefatos de provider e paths absolutos de
runtime não são incluídos neste relatório versionado.

## Resultado final da onda

O primeiro gate readonly pediu complemento: duplicatas com metadados inválidos
não eram todas recusadas. Corrigido pelo coordenador e validado com 20 testes
puramente em memória. O gate complementar foi APROVADA a API pura, sem outro
bloqueador técnico; coordenador aceitou o resultado pelo transcript/terminal real.
Suíte completa do coordenador: 90/89/1, exit 0. Dez arquivos da Etapa 4 integrados
com verificação de baseline/hashes e preservação dos demais, sem commit/push.

No shell Codex restrito, check e worker_done primeiro não resolveram orca. Na
revisão complementar o caminho explícito do MESMO executável, confirmado no
coordenador como 1.4.219, também recebeu CommandNotFoundException. Logo ausência
no PATH não é diagnóstico causal suficiente. Restrição de visibilidade/execução
ou outra diferença do shell sandbox permanece hipótese, sem diagnóstico interno.
Não foram copiados executáveis nem liberados caminhos/sandbox como contorno.

Todos os turnos finais foram observados antes de fencing. As quatro Tasks ficaram
failed por falha/cancelamento operacional, mesmo quando a revisão técnica aprovou.
Não houve worker_done durável. Um registro foi released após stop do terminal
criado em YOLO; três registros ficaram retained por abandon, correspondendo a
terminais custom preservados. Consulta final: zero ativos e zero reclaimable.
Isso não significa que todos os processos tenham saído.

Transcriber 8C: 142 testes aprovados em isolamento, Ruff global e formatação
aprovados também no principal. Onze arquivos integrados, com código de produção
da fila, frontend, mudanças não relacionadas e relatório histórico 8B preservados.
Aviso de distribuição inválida no ambiente existente permanece sem reparo.

Conclusão: entregas técnicas locais concluídas no envelope aprovado; lifecycle
supervisionado com executores restritos continua necessitando integração suportada.
Nada neste registro homologa a confiabilidade geral do Orca ou autoriza novos
escritores, instalação, mudanças globais, bypass, commit/push ou próxima etapa.

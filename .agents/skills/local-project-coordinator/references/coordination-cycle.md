# Ciclo portátil de coordenação

## Autoridade

Explicar, analisar, revisar e criar prompt permitem apenas leitura e resposta. Diagnóstico
permite investigar e explicar. Delegar/iniciar permite um worker no projeto indicado.
Implementar permite editar somente a etapa autorizada. Commit e push exigem autorizações
separadas.

## Antes do lançamento

Confirme projeto e raiz, `AGENTS.md`, documentos, Git, baseline, ausência de escritor
concorrente, objetivo, aceite, exclusões, parada, skills descobertas e perfil disponível.

## Lançamento e acompanhamento

O prompt deve conter projeto, baseline, objetivo, invariantes, validações, documentação,
Git e parada. Use o mecanismo persistente do executor realmente disponível. Para troca de
executor, encerre o anterior, confira processos e Git, produza handoff sanitizado e só
então inicie a nova sessão.

Não interprete silêncio como falha, não abra segundo escritor e não repita efeitos de
resultado desconhecido. Ao aguardar um worker, execute apenas **1 único** `check --wait` de 5 min (`--timeout-ms 300000` com `timeout_ms: 310000` na tool de shell); se expirar sem `worker_done`, encerre o turno em **Standby Real** (sem segundo wait e sem `worker-show` em loop) até o wake do Orca ou retorno de Erick. No gate, separe testes, mocks e validação real e decida entre
aprovar, bloquear ou solicitar complemento.

Pare quando projeto, autorização, baseline, skill, perfil ou permissão adicional não
estiverem claros, ou quando a evidência não sustentar o marco.

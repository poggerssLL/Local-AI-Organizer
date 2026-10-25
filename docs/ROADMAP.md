# Roadmap central

Atualizado em: 2026-10-06.

## Concluído neste marco

1. A fonte de perfis foi reconciliada: 11 entradas, `organizer-core-v2`, Terra para
   tarefas mecânicas, Sol 6.1 em médio/alto para implementação, Gemini 3.8
   low/medium/high, Claude Sonnet/Opus 5.5 e GPT-OSS. Os perfis Antigravity foram
   revalidados no catálogo atual; os recibos da Etapa 3 confirmaram Sol 6.1 em
   medium/high e Opus 5.5 high. Isso não homologa outros perfis por inferência.
2. Orca 1.4.219 e Antigravity 1.2.16 foram validados em fixtures descartáveis: o worker
   passou pela prontidão, recebeu a tarefa, emitiu `worker_done`, foi liberado e teve o
   worktree removido. Um segundo canário realizou uma escrita reversível e verificou
   `git diff --check` antes da limpeza.
3. O contexto inicial foi reduzido para um manifesto curto e carregamento sob demanda.
4. O contrato de colaboração Codex + Antigravity foi documentado e exercitado no Organizer:
   auditoria Codex somente leitura, Antigravity como escritor único de uma suíte determinística,
   revisão independente, `worker_done` e `worker-release`.

## Etapa 3 do Local File Agent: implementação e gate limitado

Após autorização explícita de Erick, a Etapa 3 foi implementada sobre main `6d24cb0`
(32 testes legados): hashing SHA-256 separado do inventário, opt-in, backend conservador
Windows/NTFS e grupos determinísticos. Arquitetura, QA, escritor único e auditoria foram
despachados pelo Orca com perfis efetivos confirmados e fallback none.

O gate independente Antigravity Opus 5.5 high aprovou somente fixtures sintéticas NTFS:
65 testes executados, 64 aprovados e 1 skip nativo de symlink de arquivo sem privilégio.
Nuvem/remoto foram simulados; não há snapshot atômico ou confinamento absoluto.
Complementos de sinalização de inventário parcial e precisão documental foram revisados
e aprovados pelo coordenador com phase-gate-reviewer; reexecução final independente:
67 testes, 66 aprovados e o mesmo skip. Consulte a documentação viva e o relatório da Etapa 3
no projeto alvo; o Organizer não substitui esse contrato.

Arquitetura, QA, escritor e auditor emitiram conclusões aceitas. A tentativa anterior
do escritor terminou em falha e foi liberada; a tentativa retomada concluiu a mesma tarefa.
Contabilidade final: zero workers reclaimable no Run; dois terminais protegidos por
user_takeover permanecem retidos. Isso não significa ausência de processos vivos.

## Entrega e manutenção paralela em 2026-10-05

A revisão de release Codex Sol 6.1 high encontrou uma regressão: o snapshot inicial
da raiz propagava OSError sem sanitização se a raiz desaparecesse ou perdesse acesso
depois da construção do scanner. O escritor Codex Sol 6.1 medium corrigiu esse ramo
e adicionou três regressões. O gate independente Sol 6.1 high classificou os 17
candidatos como PRONTO PARA COMMIT: 70 testes, 69 aprovados e o mesmo skip, apenas
fixtures NTFS locais sintéticas. Após autorização nominal, os 17 arquivos foram
consolidados no commit `49c7dbe` e publicados em origin/main. HEAD e origin/main
locais e main consultado no servidor coincidem; working tree do File Agent limpa.
O código/testes não mudou após o gate; houve somente atualização documental
de autorização para publicação. Arquivos reais e implementação da Etapa 4
continuam fora desta entrega.

A manutenção do Transcriber preservou oito arquivos de código preexistentes e
revalidou o baseline com doubles/fixtures: uma falha de temporização ocorreu na
primeira suíte, seguida por reexecução com 141 aprovações. Persistem dez erros E501
e quatro arquivos fora de formatação no Ruff. O complemento documental foi revisado,
com quatro verificações individuais de sintaxe JavaScript aprovadas. A tentativa de
limpeza do diretório pai excedeu as subárvores previstas; há resíduos sintéticos
preservados e evidência incompleta sobre o inventário anterior. O relatório 8B registra
esse limite. Não houve nova inferência real, download ou início da Etapa 9, nem commit/push.

O [diagnóstico do Orca](ORCA_RELIABILITY_MAINTENANCE_2026-10-05.md) registra
mitigações operacionais e lacunas de observabilidade, sem alegar correção do binário.
Um despacho Claude terminou por cota individual; a retomada usou Gemini 3.8 Flash
high explicitamente. Erick determinou esse modelo/esforço para as frentes Antigravity,
com fallback none. Contabilidade desta onda conferida: sete Tasks concluídas,
nenhum worker ativo ou reclaimable no Run. Os registros retidos foram preservados;
isso não equivale a ausência de processos vivos. Os números da seção anterior
referem-se à onda histórica.

## Marcos posteriores

Próximo marco recomendado no File Agent: Etapa 4, motor de regras por extensão,
nome e intervalos de datas, operando sobre inventários sintéticos em memória.
Definir prioridades e desempates, motivos de classificação e tratamento de
ambiguidades, sem ler conteúdo, executar hashing implicitamente ou mover arquivos.
O novo envelope deve confirmar baseline publicado, um escritor e limites efetivos
de escrita/limpeza; não assumir que o texto da Task impõe confinamento técnico.

Manutenção paralela recomendada: corrigir as dez E501 e formatação em tarefa
delimitada do Transcriber, investigar sincronização do teste de heartbeat sem
retries que ocultem a falha, e usar temporários fora de diretórios sincronizados.
Para Orca, verificar os limites de acesso e os checkpoints de follow-up antes de
outro escritor e reproduzir falhas de prontidão em fixture descartável. Essas
pendências não exigem mudar o hashing da Etapa 3 nem usar dados reais na Etapa 4.

1. Manter `Local Transcriber` em operação local; processamentos remotos seguem adiados.
2. Iniciar `Jarvis Local` apenas após políticas de ferramentas e aprovação humana no File
   Agent.
3. Descobrir contratos e fronteiras de `Casa Inteligente` antes de qualquer integração.

Este roadmap não autoriza implementação, instalação, credenciais, commit, push ou escrita
em projetos irmãos.

## Execução autorizada da Etapa 4 e manutenção 8C

Erick autorizou nominalmente Etapa 4 e manutenção paralela em 2026-10-05.
O File Agent recebeu motor puro de regras sobre metadados sintéticos, com
classificação auditável, prioridade/conflitos, intervalos UTC e recusa explícita
de duplicatas. Primeiro gate pediu complemento para duplicata com metadados
inválidos; corrigido, com regressão e suíte 90/89/1. Gate complementar técnico aprovado via transcript e aceito pelo coordenador;
integração de dez arquivos concluída no principal, sem commit/push.
Baseline publicado `49c7dbe`; nenhuma autorização nova de commit/push ou Etapa 5.

Transcriber: manutenção 8C integrada; 142 testes aprovados no checkout isolado,
Ruff e formatação globais aprovados também no principal. Clock controlado separa
prova de retries da prova de margem expirada, sem mudar código de produção da fila.
AST funcional dos quatro arquivos de estilo preservada; três docstrings refluídas.
Aviso pip de distribuição inválida permanece, sem reparo do ambiente.

Orca: preflight encontrou EPERM no IPC do Gemini com sandbox, YOLO e prompt no
composer no launcher padrão Codex e Orca fora do PATH no shell Codex restrito.
Não houve bypass. Sessão Codex custom readonly iniciou com telemetria observável;
a revisão complementar qualifica o mesmo executável Orca resolvido pelo coordenador.
Veja [preflight atual](ORCA_RELIABILITY_PREFLIGHT_2026-10-05.md). As recomendações
acima descrevem o estado anterior; estas evidências não corrigem o binário nem
homologam a confiabilidade geral de todos os executores.

Fechamento desta onda: quatro Tasks failed no lifecycle, com três registros
retained e um released, zero workers ativos/reclaimable. Aprovação técnica da
Etapa 4 foi recebida via transcript; nenhum worker_done foi forjado pelo coordenador.
No Codex readonly, o mesmo Orca qualificado também não foi resolvido pelo shell;
isso refuta tratar o caso como simples ausência no PATH. A causa interna da
restrição de visibilidade/execução ainda não foi demonstrada.

## Publicação e próximos passos (2026-10-05)

Erick autorizou commit e push das entregas. Etapa 4 do File Agent publicada em
main `9db3c44`; consulta ao servidor confirmou o mesmo SHA de HEAD/origin/main
e checkout limpo. A aprovação técnica permanece limitada aos metadados sintéticos.
Organizer publicou perfis, contratos e diagnósticos revisados em `df679f8`,
com 28 testes determinísticos aprovados; esses testes não homologam o binário Orca.
Erick confirmou a publicação conjunta das alterações preexistentes da Etapa 8
e das manutenções 8B/8C do Transcriber. Main publicada em `5cfc7b8`, com SHA
confirmado no servidor e no upstream. Resíduos sintéticos de fixtures permanecem
não versionados e preservados; nenhum runtime entrou no Git.

Sequência recomendada, sem iniciar novas implementações por este roadmap:

1. Orca: resolver acesso ao executável e IPC com permissões mínimas suportadas;
   repetir canário Gemini 3.8 Flash high com fallback none, worker_done durável e
   decisão de release. Evitar novos escritores supervisionados antes desse gate.
2. File Agent: tornar a fixture oculta legada reproduzível em clones limpos e
   preparar o contrato da Etapa 5 para casos ambíguos, com modelo local opt-in,
   JSON validado, mocks primeiro, sem mover arquivos nem baixar modelos silenciosamente.
3. Transcriber: manter operação local e investigar o aviso da distribuição inválida
   em escopo próprio; inferência/CUDA/Ollama reais e futuras etapas exigem validação
   e autorização específicas. Etapa 9 não iniciada.
4. Jarvis Local permanece dependente das políticas de ferramentas/aprovação do
   File Agent; Casa Inteligente exige descoberta de contratos antes da integração.

## Quatro frentes paralelas autorizadas (2026-10-06)

Erick pediu executar os três próximos passos e criar um workspace pessoal de uso
geral. Três workers Gemini 3.8 Flash high readonly/sandbox receberam despachos
reais; o coordenador integrou source/docs como escritor único. Sem commit/push novo.

1. File Agent: fixture legada tornou-se autossuficiente por teste. Clone novo sem
   arquivos ignorados confirmou 90/89/1; skip winerror 1314 preservado. Contrato e
   schema preparatórios da Etapa 5 escritos; adapter, modelo e dados reais fora
   desta entrega. Próximo marco técnico: contrato/fake testável em tarefa própria.
2. Transcriber: causa do aviso ligada a metadados til antigos, distribuição ativa
   0.7.1/import conferidos. pip check exit 0 com aviso; Ollama local respondeu
   e qwen2.5:3b está presente; CPU int8 e CUDA int8_float16 sondados sem inferência.
   Reparos de ambiente e validação sintética real planejados, não executados.
3. Orca: CLI local usa named-pipe, não TCP/WebSocket automaticamente. EPERM foi
   reproduzido em leitores restritos. Sem mecanismo mínimo suportado demonstrado;
   gate permanece complemento necessário. Prune Git dry-run identificou dois
   registros antigos sem gitdir, sem excluir ou alterar permissões.
4. Uso Geral: projeto/workspace separado registrado no Orca, com instruções curtas
   para respostas diretas e ferramentas pequenas. Sem roteiro documental ou
   delegação obrigatória por pergunta. Erick autorizou explicitamente a confiança;
   terminal Gemini high com sandbox pronto. Teste de pergunta direta leu somente
   AGENTS.md e respondeu, sem README/roadmaps, escrita ou rede. Workspace concluído.

Fonte do diagnóstico atual: [Orca 2026-10-06](ORCA_RELIABILITY_DIAGNOSIS_2026-10-06.md).
Os fatos de cada projeto ficam em sua própria documentação viva. Os testes de
catálogo do Organizer não homologam IPC ou binário Orca.

## Reparo e gate restrito de 2026-10-06

Transcriber 8E: metadados inválidos em quarentena reversível, pip check sem aviso
e 26 testes de resumo/API aprovados com mocks. Validação real de inferência é próxima.
No Orca, exceções específicas de IPC foram investigadas. O canário operador-criado
concluiu com política herdada always-proceed, sem homologar isolamento. O canário
worker-start com request-review consultou o Orca usando exceção por comando e
concluiu com consentimento único de Erick para done. Done/release/ack conferidos,
dois Tasks completed, dois terminais retained e zero reclaimable. As configurações
foram restauradas byte por byte. Sandbox pura segue bloqueada; launcher padrão e
escrita real não estão homologados.
[Validação e reversão](ORCA_IPC_REPAIR_VALIDATION_2026-10-06.md).
[Opções de plugins e MCP](PLUGIN_AND_MCP_OPTIONS.md).

## Estado confirmado em 2026-10-07

- File Agent: 5A final revisada; 5B adapter local opt-in implementado e gate
  independente de transporte/contrato aprovado. Suíte final 122/121/1, skip
  winerror 1314. Fixture nativa qwen2.5:3b retornou abstenção; qualidade geral
  depende de gabarito independente. Etapas 6+ não iniciadas.
- Transcriber: 8G validou fala SAPI sintética em CPU/CUDA com WER 0 e seis
  âncoras; resumo de texto separado com timeline preenchida. 150 testes.
  Gate semântico final: COMPLEMENTO NECESSÁRIO por atores e redundância,
  confirmado por reviewer independente. Etapa 9 não iniciada.
- Orca: canário antigo teve done real recuperado; os dois leitores antigos
  perderam terminal e ficaram failed/abandoned, sem done fabricado. Novos
  reviewers encerraram com done reais, release e ACK. Retained não significa
  processo encerrado; sandbox pura/launcher padrão não homologados.
- Codex coordenador implementou; Gemini 3.8 Flash high/high fez revisões reais
  readonly com fallback none. Reviewer Codex Sol high ficou bloqueado pelo
  helper Windows 1223 antes de inspecionar código; roteamento novo comunicado.
- Alterações preexistentes preservadas; sem commit/push/publicação. Não iniciados
  Uso Geral, Jarvis ou Casa nesta onda. Modelos e fixtures exclusivamente locais
  já existentes; nenhuma permissão ampla recriada.

[Entrega, limites e próximos critérios](PORTFOLIO_CONTINUATION_2026-10-07.md).
Os registros de 2026-10-06 abaixo são históricos; pendências IPC antigas foram
reavaliadas e não são o estado atual.

## Onda paralela registrada em 2026-10-06

- File Agent 5A: contrato/fake em memória implementado. Clone novo passou
  109/108/1, skip winerror 1314. Próximo gate: adapter local 5B e qualidade com
  gabarito; modelo real e Etapas 6+ não iniciados.
- Transcriber 8F: inferência real small CPU int8 e CUDA int8_float16 com tom
  sintético; Ollama qwen2.5:3b resumiu texto sintético e persistiu Markdown/JSON.
  142 testes e Ruff/formatação/pip check aprovados. Precisão de fala não medida;
  repetição/timeline vazia são lacunas de qualidade antes da Etapa 9.
- Orca: três despachos reais Gemini 3.8 Flash high, dois leitores e um escritor
  isolado. Arquivo do canário conferido byte a byte. Done dos três aguarda
  consentimento específico de IPC; lifecycle e releases/acks pendentes; regras temporárias removidas e política
  restaurada, confiança autorizada da fixture preservada. Não promover writer de produção.

Alterações anteriores e fixtures preservadas. Documentação/código locais,
sem commit/push novo. [Canário e pendência](ORCA_WRITE_CANARY_VALIDATION_2026-10-06.md).

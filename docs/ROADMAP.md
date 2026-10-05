# Roadmap central

Atualizado em: 2026-10-05.

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
Organizer consolida neste commit perfis, contratos e diagnósticos revisados,
com 28 testes determinísticos aprovados; esses testes não homologam o binário Orca.
A publicação do Transcriber depende da confirmação de incluir as alterações
preexistentes da Etapa 8 junto às manutenções 8B/8C; nenhum runtime entra no Git.

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

# Registro central de projetos

Atualizado em: 2026-10-07.

Este registro é um resumo de portfólio, não substitui o Git, os testes nem a documentação
viva de cada repositório. Não armazene caminhos pessoais, IDs de runtime, credenciais ou
dados privados.

| Projeto | Papel | Estado conhecido | Próximo passo seguro |
| --- | --- | --- | --- |
| `Local AI Organizer` | Coordenação, contratos e revisão | Baseline `b92139d`. Canário antigo: done real recuperado; dois leitores antigos failed/abandoned por terminal ausente. Novos reviewers reais Gemini concluídos com done/release/ACK; zero active/reclaimable, registros retained preservados. | [Continuação e critérios](PORTFOLIO_CONTINUATION_2026-10-07.md). Sandbox pura/launcher padrão e writer de produção não homologados; helper Codex supervisionado bloqueado por 1223. |
| `Local Transcriber` | Transcrição local e offline | Main `5cfc7b8`, 0.7.1/schema 4. 8G: fala sintética small CPU/CUDA WER 0, seis âncoras; texto separado com timeline. 150 testes e Ruff/formatação/pip check aprovados. | Gate semântico final COMPLEMENTO NECESSÁRIO por atores/redundância. Etapa 9 não iniciada; E2E fala/fila/UI não validado. Relatório 8G no projeto alvo. |
| `Local File Agent` | Inventário e organização segura | Main `9db3c44`. 4B preservada, 5A final revisada; 5B local opt-in com gate transporte/contrato aprovado. Suíte final 122/121/1, skip winerror 1314; fixture nativa local retornou abstenção. | Avaliação com gabarito independente por categoria/abstenção e falso aceite antes de ampliar dados. Modelo não aprovado para qualidade geral; Etapas 6+ não iniciadas. Relatório 5B no projeto alvo. |
| `Uso Geral` | Perguntas, jogos, scripts e ferramentas pequenas | Projeto independente criado e registrado no Orca, workspace Uso Geral e terminal próprio. AGENTS curto, sem leitura inicial obrigatória de README/roadmaps ou portfólio; ferramentas separadas, scratch/outputs ignorados. Git local main sem commit/remoto. | Confiança autorizada explicitamente por Erick; Gemini 3.8 Flash high pronto. Teste pontual respondeu diretamente lendo somente AGENTS.md, sem README/roadmaps, edição ou rede. Usar para pedidos cotidianos. |
| `Jarvis Local` | Assistente local por voz | Planejado. | Iniciar somente após a base segura do File Agent. |
| `Casa Inteligente` | Projeto residencial separado | Existência informada; arquitetura não inspecionada aqui. | Revisar contratos antes de integração. |

Classifique qualquer nova afirmação como confirmado agora, informado, planejado ou
desconhecido. Não converta relatórios históricos em baseline atual.

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

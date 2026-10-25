# Mapa dos sistemas locais

```text
Erick (autoriza e decide)
  -> Local AI Organizer (coordena, revisa e mantém contratos)
       -> Local Transcriber (transcrição local)
       -> Local File Agent (operações sob aprovação humana)
       -> Jarvis Local / Casa Inteligente (futuros e separados)
```

O Organizer não compartilha diretórios de runtime, bancos, transcrições ou memória privada
entre projetos. A integração futura usa contrato versionado e dados sanitizados.

## Execução assistida

```text
pedido autorizado -> perfil explícito -> contexto mínimo v2 -> um worker
  -> evidências, Git e limitações -> gate -> release ou retenção explícita
```

Codex e Antigravity são executores distintos. Gemini, Claude e GPT-OSS são modelos do
Antigravity; não são agentes independentes do Orca. O catálogo de perfis está em
`orca-model-routing-profiles.json`; o limite atual de lançamento Antigravity está em
`ORCA_WORKER_LIFECYCLE.md`. Não há fallback silencioso nem dois escritores por checkout.

Quando uma etapa exigir colaboração entre executores, ela segue o contrato
`CODEX_ANTIGRAVITY_COLLABORATION.md`: leitores e auditores podem trabalhar em paralelo
somente leitura ou em worktrees isolados; o pacote de passagem é sanitizado; um único
escritor integra mudanças sequencialmente; e um gate independente revisa as evidências.

## Invariantes de integração

- cada projeto mantém repositório, dados e documentação próprios;
- o coordenador encaminha prompts e evidências, não dados privados;
- escrita exige autorização explícita, validação proporcional e aprovação humana quando
  afetar arquivos reais;
- falha ou indisponibilidade de um executor não concede permissão a outro executor.

## Workspace pessoal separado

`Uso Geral` atende perguntas, pesquisas de jogos, cálculos e ferramentas pequenas.
Tem AGENTS curto e contexto sob demanda; não carrega documentação do Organizer
ou integra runtimes de outros projetos por padrão. É um projeto independente
registrado no Orca, sem remoto/publicação automática.

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

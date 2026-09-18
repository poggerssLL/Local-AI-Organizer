# Perfil portátil de execução

Escolha o menor perfil com boa probabilidade de concluir corretamente. Confirme catálogo,
esforços e limites no executor no momento do lançamento; modelos e condições podem mudar.

Avalie complexidade, ambiguidade, risco, duração, volume de contexto e custo de retrabalho.
Informe sempre modelo, esforço, justificativa, alternativa econômica, gatilho objetivo de
escalada e limitações.

## Perfis do Organizer

Quando a tarefa for lançada pelo Orca neste projeto, use somente perfis materializados em
`docs/orca-model-routing-profiles.json`:

- Codex econômico: `gpt-5.6-terra`, esforço `medium`;
- Codex forte: `gpt-5.6-sol`, esforço `high`;
- Gemini econômico: `gemini-3.8-flash-medium`, esforço `medium`;
- Gemini forte: `gemini-3.8-flash-high`, esforço `high`.

Outros modelos não integram automaticamente o contrato só porque aparecem na assinatura
do provedor. Falha de disponibilidade deve encerrar o lançamento, salvo fallback nominal
previamente autorizado. Não equipare preço da API, créditos do provedor e limites do
aplicativo.

Claude Opus, Claude Sonnet e GPT-OSS são candidatos planejados dentro do executor
Antigravity, ainda sem perfil materializado neste contrato. Use somente o identificador e
o esforço devolvidos pelo catálogo real. Um terceiro executor ou OpenRouter exige
contrato separado; não improvise comando, credencial ou fallback.

Escale somente diante de dificuldade observada: baseline inconsistente, falha repetível
sem causa, risco crítico ou escopo materialmente maior. Uma escalada que mude custo,
executor ou escopo exige decisão de Erick.

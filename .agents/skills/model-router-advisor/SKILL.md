---
name: model-router-advisor
description: Recomende executor, modelo e esforço a partir do catálogo versionado do Organizer e da capacidade efetiva do runtime, sem fallback silencioso.
---

# Consultor de roteamento de modelos

Use esta skill ao planejar ou delegar uma etapa. Ela recomenda o menor perfil proporcional
ao risco; não inicia tarefa, não altera permissões e não garante disponibilidade ou economia.

## Fonte de verdade

Leia `docs/orca-model-routing-profiles.json` e `docs/ORCA_WORKER_LIFECYCLE.md`. Antes de
usar Antigravity, confirme o ID em `agy models`; antes de usar worker supervisionado,
confirme a capacidade efetiva no recibo do Orca. Se o perfil não estiver disponível, pare
com `fallback: none`.

## Perfis atuais

- `organizer-codex-luna` — `gpt-5.6-luna` / `low`: leitura curta, triagem e tarefas
  mecânicas.
- `organizer-codex-economy` — `gpt-5.6-terra` / `medium`: tarefas mecânicas, validações
  pontuais e testes usuais.
- `organizer-codex-sol-medium` — `gpt-6.1-sol` / `medium`: padrão para implementação de
  complexidade média, debugging delimitado e revisão técnica.
- `organizer-codex-strong` — `gpt-6.1-sol` / `high`: arquitetura, integração e depuração
  complexas.
- `organizer-gemini-low` — `gemini-3.8-flash-low` / `low`: classificação e síntese curta.
- `organizer-gemini-economy` — `gemini-3.8-flash-medium` / `medium`: documentação e
  auditoria ampla.
- `organizer-gemini-strong` — `gemini-3.8-flash-high` / `high`: síntese técnica densa.
- `organizer-claude-sonnet` — `claude-sonnet-5-5-high` / `high`: implementação e testes.
- `organizer-claude-opus` — `claude-opus-5-5-high` / `high`: arquitetura e gates críticos.
- `organizer-gpt-oss` — `gpt-oss-120b-medium` / `medium`: segunda opinião independente.
- `organizer-openrouter-free` — somente após autorização específica de custo, credencial e
  privacidade; não é fallback.

## Limite de execução

No Orca 1.4.219, um perfil Antigravity de modelo fixo pode iniciar Dispatch supervisionado
após revalidar `agy models` e a capacidade de `worker-start`. O modelo efetivo precisa
constar no recibo; para Antigravity já pronto em terminal reutilizado, o modelo é herdado e
deve ser relatado como tal. Um canário em fixture não autoriza projeto real nem fallback.

## Saída obrigatória

Informe perfil, executor, modelo, esforço, `fallback: none`, justificativa ligada a risco e
escopo, alternativa econômica somente se ela for compatível, gatilho de escalada e limites
de disponibilidade. Garanta um único escritor por checkout e não transfira contexto ou
permissões entre executores.

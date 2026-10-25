# Fase: Orquestração Híbrida e Delegação Bidirecional (Codex & Antigravity)

Data: 2026-09-18.

## Objetivo

Formalizar a arquitetura de governança para operação conjunta e simétrica entre o ecossistema
OpenAI no **Codex** e o ecossistema Google Pro AI no **Antigravity**, materializar a sétima
skill de coordenação (`model-router-advisor`) com instalação dual e expandir o catálogo de
execução para 9 perfis unificados.

## Implementado

1. **Skill Portátil e Instalação Dual:**
   - Criada a skill `model-router-advisor` em `.agents/skills/model-router-advisor/SKILL.md`;
   - Instalada em `%USERPROFILE%\.codex\skills\model-router-advisor\SKILL.md` para descoberta
     nativa no catálogo de usuário do Codex;
   - Instalada a skill `local-project-orientation` em `%USERPROFILE%\.codex\skills\local-project-orientation\SKILL.md`,
     alcançando paridade total das 7 skills de coordenação em ambos os executores.

2. **Catálogo Unificado de 9 Perfis (`docs/orca-model-routing-profiles.json`):**
   - OpenAI / Codex:
     - `organizer-codex-luna` (`gpt-5.6-luna`, `low`): tarefas mecânicas e templates;
     - `organizer-codex-economy` (`gpt-5.6-terra`, `medium`): desenvolvimento diário balanceado;
     - `organizer-codex-strong` (`gpt-5.6-sol`, `high`): subsistemas e depuração densa;
     - `organizer-codex-astra` (`gpt-5.6-astra`, `extreme`): exceções críticas extremas de impasse;
   - Google Pro AI / Antigravity:
     - `organizer-gemini-economy` (`gemini-3.8-flash-medium`, `medium`): coordenação contínua;
     - `organizer-gemini-strong` (`gemini-3.8-flash-high`, `high`): síntese analítica profunda;
     - `organizer-claude-sonnet` (`claude-sonnet-4-6`, `high`): código limpo e testes rigorosos;
     - `organizer-claude-opus` (`claude-opus-4-6-thinking`, `high`): arquitetura e gates;
     - `organizer-gpt-oss` (`gpt-oss-120b-medium`, `medium`): auditoria aberta e neutra.

3. **Governança de Delegação Bidirecional:**
   - Formalizada em `SYSTEM_MAP.md`, `ORCHESTRATION_POLICY.md`, `DELEGATION_TEMPLATE.md` e
     `ORCA_MODEL_ROUTING_CONTRACT.md`.
   - Uma sessão no Codex pode delegar para modelos do Codex ou do Antigravity, e uma sessão
     no Antigravity pode delegar para modelos do Antigravity ou do Codex.
   - Gestão de cota semanal formalizada: recarga na segunda-feira para Codex; preservação e
     redirecionamento dinâmico para Antigravity em fins de semana ou quando a cota estiver esgotada.

## Validação

- Catálogo do Codex (`%USERPROFILE%\.codex\skills`): confirmada a listagem das 7 skills de
  coordenação (`implementation-prompt-builder`, `local-ai-release-review`,
  `local-integration-architect`, `local-project-coordinator`, `local-project-orientation`,
  `model-router-advisor`, `phase-gate-reviewer`).
- Sintaxe JSON: arquivo `docs/orca-model-routing-profiles.json` validado com 9 objetos em
  conformidade com o schema `orca-model-routing/v1`.
- Limites preservados: nenhum dado pessoal, chave de API ou credencial adicionado;
  projetos reais permanecem bloqueados para automação via Orca até homologação do PTY.

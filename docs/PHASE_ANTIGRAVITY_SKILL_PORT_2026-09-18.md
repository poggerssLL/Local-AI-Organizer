# Portabilidade das skills do Organizer para Antigravity

Data: 2026-09-18.

## Objetivo

Materializar no próprio workspace versões portáteis das seis skills de coordenação para
que o Antigravity possa descobri-las sem depender dos diretórios pessoais do Codex.

## Implementado

- criada a raiz `.agents/skills/` no repositório;
- materializadas `local-project-orientation`, `phase-gate-reviewer`,
  `implementation-prompt-builder`, `local-ai-release-review`,
  `local-integration-architect` e `local-project-coordinator`;
- incluídas referências locais para perfil de execução, contrato de integração e ciclo de
  coordenação;
- adaptados os trechos exclusivos do Codex para distinguir Codex, Antigravity e Orca;
- preservados autorização explícita, um escritor por checkout, ausência de fallback
  silencioso, atualização factual do roadmap e gates separados para commit e push.

## Validação local

- estrutura baseada em `<workspace>/.agents/skills/<nome>/SKILL.md`, conforme a
  documentação primária do Antigravity;
- frontmatter restrito a `name` e `description`;
- referências relativas confinadas à pasta de cada skill;
- nenhuma credencial, caminho pessoal, ID de runtime ou permissão global adicionado;
- nenhum worker, instalação, commit ou push executado nesta etapa.

## Não validado

- invocação autônoma ou manual de cada skill;
- equivalência de comportamento entre modelos;
- delegação automática em projeto real.

## Confirmação posterior de Erick

Após reiniciar a sessão, Erick informou que as seis skills aparecem no painel `/skills`
do Antigravity. Essa evidência confirma a descoberta segundo relato do usuário. A
invocação de `local-project-orientation`, a ausência de alterações no Git e o restante do
comportamento continuam pendentes de canário.

## Canário executado e aprovado

1. A skill portátil `local-project-orientation` foi invocada em modo somente leitura no
   Antigravity com modelo Google Gemini 3.8 Flash.
2. Foram confirmados a raiz Git (`C:/Users/erick/OneDrive/Documentos/Local AI`), o commit base
   `6a8529a`, a conformidade com as instruções de `AGENTS.md` e a documentação central.
3. O comando `git status --short` confirmou que nenhum arquivo foi alterado ou criado pela
   execução da skill, comprovando o cumprimento estrito do modo somente leitura.

Projetos reais permanecem categoricamente bloqueados. A aprovação deste canário comprova
a descoberta e a execução básica das skills portáteis no Antigravity, mas não libera a
delegação automática nem o gate interativo PTY no Orca.

## Fonte primária

- `https://www.antigravity.google/docs/skills?tab=ide` — formato `SKILL.md`, localização
  de workspace e descoberta por `/skills` no Antigravity CLI.

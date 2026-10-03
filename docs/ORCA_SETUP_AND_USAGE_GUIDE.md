# Uso do Local AI Organizer com Orca

Atualizado em: 2026-10-03.

## Verificação inicial

```powershell
git rev-parse --show-toplevel
git status --short
orca --version
agy models
```

Use a saída atual, não este guia, para decidir se um modelo pode ser iniciado. Os perfis
recomendados ficam em `orca-model-routing-profiles.json`; o contrato detalhado fica em
`ORCA_MODEL_ROUTING_CONTRACT.md`.

## Seleção prática

| Caso | Perfil inicial |
| --- | --- |
| leitura/triagem curta | `organizer-codex-luna` ou `organizer-gemini-low` |
| documentação e auditoria ampla | `organizer-gemini-economy` |
| alteração delimitada | `organizer-codex-economy` |
| implementação e testes complexos | `organizer-claude-sonnet` ou `organizer-codex-strong` |
| arquitetura e gate crítico | `organizer-claude-opus` |
| segunda opinião econômica | `organizer-gpt-oss` |

OpenRouter não é fallback: exige autorização de custo, credencial e contrato próprio.

## Worker supervisionado

Carregue `orca skills get orchestration` antes de operar. Para Codex, o Orca pode registrar
modelo e esforço no recibo de lançamento. Para Antigravity, consulte
`ORCA_WORKER_LIFECYCLE.md`: o Orca atual não aceita `--model` para esse executor e a sessão
manual com modelo fixo não é um Dispatch supervisionado. Não retire sandbox nem use flags
de bypass para alterar essa conclusão.

No fim de um Dispatch concluído, processe a evidência e use `worker-release`; não feche a
aba manualmente. Commit, push, instalação, login e controle visual não fazem parte deste
guia operacional.

# Roadmap central

Atualizado em: 2026-10-04.

## Concluído neste marco

1. A fonte de perfis foi reconciliada: 10 entradas, `organizer-core-v2`, Gemini 3.8
   low/medium/high, Claude Sonnet/Opus 5.5 e GPT-OSS, todos revalidados no catálogo
   Antigravity atual.
2. Orca 1.4.219 e Antigravity 1.2.16 foram validados em fixtures descartáveis: o worker
   passou pela prontidão, recebeu a tarefa, emitiu `worker_done`, foi liberado e teve o
   worktree removido. Um segundo canário realizou uma escrita reversível e verificou
   `git diff --check` antes da limpeza.
3. O contexto inicial foi reduzido para um manifesto curto e carregamento sob demanda.
4. O contrato de colaboração Codex + Antigravity foi documentado e exercitado no Organizer:
   auditoria Codex somente leitura, Antigravity como escritor único de uma suíte determinística,
   revisão independente, `worker_done` e `worker-release`.

## Próximo marco: gate da Etapa 3 do Local File Agent

Em revisão somente leitura no repositório alvo, auditar fronteiras de caminhos, symlinks ou
reparse points, fixtures reproduzíveis e o gate antes de qualquer hash ou deduplicação em
arquivos reais. A implementação só pode iniciar após essa evidência e nova autorização de
Erick.

## Marcos posteriores

1. Manter `Local Transcriber` em operação local; processamentos remotos seguem adiados.
2. Iniciar `Jarvis Local` apenas após políticas de ferramentas e aprovação humana no File
   Agent.
3. Descobrir contratos e fronteiras de `Casa Inteligente` antes de qualquer integração.

Este roadmap não autoriza implementação, instalação, credenciais, commit, push ou escrita
em projetos irmãos.

# Roadmap central

Atualizado em: 2026-10-03.

## Concluído neste marco

1. A fonte de perfis foi reconciliada: 10 entradas, `organizer-core-v2`, Gemini 3.8
   low/medium/high, Claude Sonnet/Opus 5.5 e GPT-OSS, todos revalidados no catálogo
   Antigravity atual.
2. O contrato de ciclo de vida separa o Dispatch supervisionado da sessão manual com
   Antigravity de modelo fixo. O teste real de prontidão do Orca falhou fechado e o terminal
   foi liberado; portanto não existe homologação falsa.
3. O contexto inicial foi reduzido para um manifesto curto e carregamento sob demanda.

## Próximo marco: canário de capacidade do worker Antigravity

Em fixture descartável, verificar se uma versão/configuração do Orca consegue preservar a
identidade e aceitar uma tarefa em terminal Antigravity já pronto. Critérios: modelo
observável, `worker_done`, `worker-release`, zero workers reclaimable e Git limpo. Sem isso,
perfis Antigravity com modelo fixo permanecem somente leitura manual e não atendem escrita.

## Marcos posteriores

1. Revisar o gate da Etapa 3 do `Local File Agent` antes de qualquer hash em arquivos reais.
2. Manter `Local Transcriber` em operação local; processamentos remotos seguem adiados.
3. Iniciar `Jarvis Local` apenas após políticas de ferramentas e aprovação humana no File
   Agent.

Este roadmap não autoriza implementação, instalação, credenciais, commit, push ou escrita
em projetos irmãos.

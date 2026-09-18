# Roadmap central

Atualizado em: 2026-09-18.

## Regra de sequência

O roadmap orienta a próxima decisão, mas não autoriza implementação. Trabalhe em uma
entrega por vez e só avance depois de revisar o resultado anterior.

## Fundação do coordenador

1. **Concluído:** criar e validar a skill pessoal `local-project-orientation`.
2. **Concluído:** consolidar o contexto central em `PROJECT_REGISTRY.md`,
   `SYSTEM_MAP.md`, `ORCHESTRATION_POLICY.md`, `ROADMAP.md` e
   `DELEGATION_TEMPLATE.md`.
3. **Concluído:** validar em um novo chat do projeto `Local AI` a recuperação do
   portfólio, das regras de autorização e do próximo passo a partir da documentação
   central.
4. **Concluído:** criar e validar a skill `phase-gate-reviewer`.
5. **Concluído:** criar e validar a skill `implementation-prompt-builder`, incluindo a
   recomendação justificada de modelo e esforço para cada nova tarefa.
6. **Concluído:** confirmar a descoberta de `implementation-prompt-builder` e criar e
   validar a skill `local-ai-release-review`.
7. **Concluído:** confirmar a descoberta de `local-ai-release-review`; criar, validar,
   descobrir e testar funcionalmente `local-project-coordinator`, incluindo autorização,
   seleção de modelo e esforço, delegação de uma única tarefa, acompanhamento e gate de
   evidências.
8. **Concluído:** criar e validar `local-integration-architect` para contratos entre
   projetos, orquestradores e agentes; sua descoberta foi confirmada pelo uso em novo
   chat em 2026-09-15.
9. **Concluído:** ampliar `local-project-coordinator`, `local-integration-architect` e
   `implementation-prompt-builder` com envelopes de execução autônoma e tornar obrigatória
   a atualização do roadmap após marcos comprovados ou mudanças de necessidade.
10. **Concluído no escopo sintético:** o piloto autônomo controlado do `Orca ADE`
    confirmou, para Codex e Antigravity, leitura confinada, bloqueio de escrita no perfil
    somente leitura, escrita reversível em worktree separado, restauração e cancelamento.
    O segundo complemento do Antigravity resolveu o worktree no Windows com `cwd`
    validado e `--new-project`, preservou hashes e Git e encerrou todos os terminais. A
    conclusão não libera projeto real. A atualização automática observada de 1.2.4 para
    1.2.5 e a recuperação necessária do detector de prontidão permanecem riscos de
    integração a tratar em gate próprio.
11. **Concluído:** estabelecer como padrão do portfólio a automação por conectores, APIs,
    terminal e arquivos; etapas visuais são orientadas para Erick, e controle direto de
    teclado e mouse exige autorização explícita e delimitada.
12. **Concluído:** delegar ao Organizer autoridade operacional sobre a raiz temporária do
    piloto, incluindo reconstrução de fixtures e worktrees, resolução do `cwd`, processos,
    sandbox e allowlists mínimas, mantendo proibidos bypass, curingas globais e acesso a
    projetos reais.
13. **Concluído:** executar o segundo complemento com Antigravity no `cwd` absoluto do
    worktree, usando caminhos relativos; comprovar leitura, bloqueio de escrita, escrita
    reversível, restauração e cancelamento supervisionado sem bypass.
14. **Concluído no escopo sintético (complemento da trilha Codex concluído):** os quatro
    perfis de execução foram materializados (`docs/orca-model-routing-profiles.json`) e
    vinculados ao repositório do Organizer no Orca via Quick Commands escopados (`<organizer-repo-id>`)
    sem bypass global. O canário sintético Antigravity comprovou leitura confinada de sentinelas,
    hashes, escrita reversível e cancelamento supervisionado pelo Orca (`PHASE_ORCA_MODEL_ROUTING_2026-09-17.md`).
    O complemento de 2026-09-18 (`PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md`) caracterizou
    a causa do timeout em `hook: PreToolUse` no Codex CLI como tentativa de elevação de sandbox
    no Windows em execução headless; com a flag `-c windows.sandbox=unelevated`, execuções completaram
    com ExitCode 0 em ~18-19s sob sandbox read-only, com aviso `os error 183` confirmado como
    não causal. Como a execução headless de turno único produziu apenas resposta conversacional
    sem acionar ferramentas de leitura de arquivos, a leitura de sentinelas pelo Codex e o pacote de
    passagem automatizado entre provedores permanecem explicitamente como ainda não validados.
    Projetos reais continuam bloqueados.
15. **Próximo, sujeito a gate explícito:** antes de qualquer operação em projetos reais, definir
    e validar o fluxo de execução interativa com PTY no Orca ou pacote de passagem assistido para
    tarefas de codificação multi-turnos, mantendo projetos reais sob bloqueio até novo gate.

## Local Transcriber

1. Receber o resultado final da Etapa 7B.
2. Revisar a instalação, a validação CUDA real, o fallback em CPU, a documentação e o Git.
3. Corrigir na mesma tarefa qualquer bloqueador da 7B.
4. Considerar o MVP local encerrado depois da aprovação.
5. Postergar as Etapas 8A e 8B de processamento remoto enquanto o uso local atender Erick.
6. Avaliar separadamente uma extensão de resumos locais, preservando a transcrição
   original e registrando a proveniência do conteúdo gerado.

## Local File Agent

Iniciar em repositório separado e por etapas:

1. fundação e política de segurança;
2. inventário somente leitura;
3. hashes e duplicidades;
4. classificação determinística;
5. integração local com modelo usando saída estruturada;
6. plano de operações;
7. prévia e aprovação;
8. execução transacional;
9. diário de auditoria;
10. desfazer;
11. validação em diretório controlado com arquivos sintéticos.

O primeiro prompt deve tratar somente da fundação. Nenhuma organização real de arquivos
é autorizada por este roadmap.

## Jarvis Local

Começar somente depois de o `Local File Agent` estabelecer políticas seguras para
ferramentas e aprovação:

1. arquitetura e threat model;
2. microfone e detecção de fala;
3. STT local de baixa latência;
4. TTS local;
5. conversa sem ferramentas;
6. planner estruturado;
7. catálogo de ferramentas permitido;
8. confirmação de ações sensíveis;
9. integração local revisada com Home Assistant ou `Casa Inteligente`;
10. wake word, memória local e dispositivos distribuídos.

## Processamento remoto

As Etapas 8A e 8B do `Local Transcriber` estão adiadas, não canceladas. Retome somente se
medições reais mostrarem que o computador atual não atende ao uso desejado ou se Erick
quiser explicitamente usar outra máquina.

## Próximo marco

O próximo marco é a validação da operação interativa via terminal PTY no Orca (utilizando os
Quick Commands escopados já registrados) ou pacote de passagem assistido para tarefas de
desenvolvimento multi-turnos. O complemento sintético de 2026-09-18 concluiu a estabilização do
timeout do Codex no Windows sob `windows.sandbox=unelevated`, mas demonstrou que a invocação de
ferramentas de leitura e o fluxo de handoff no Codex CLI dependem do canal interativo. Até que essa
validação interativa seja homologada em gate próprio, nenhum projeto real está liberado para
operação pelo Orca.

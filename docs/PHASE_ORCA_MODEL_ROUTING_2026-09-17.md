# Gate de roteamento de executores e modelos no Orca - 2026-09-17

## Decisão do gate

**COMPLEMENTO NECESSÁRIO.** A materialização dos quatro perfis lógicos (`orca-model-routing/v1`) foi concluída e validada deterministicamente. Os Quick Commands escopados ao projeto `Local AI Organizer` (`repoId: <organizer-repo-id>`) foram registrados no Orca sem afetar configurações globais (`agentDefaultArgs` permaneceu vazio). A trilha do Antigravity comprovou em worktree sintético leitura confinada com o modelo `gemini-3.8-flash-medium` e esforço `medium`, verificação das sentinelas documentais do manifesto comum, escrita reversível restrita a `fixture.txt` com restauração dos hashes originais, e cancelamento de worker supervisionado com terminação de PTY pelo Orca. Ambas as ferramentas demonstraram falha fechada diante de modelos inválidos.

No entanto, o worker Codex (`gpt-5.6-terra`, esforço `medium`, sandbox `read-only`) sofreu timeout ao atingir `hook: PreToolUse` na execução não interativa, com causa não determinada no escopo permitido de investigação. Em conformidade com a orientação de Erick, o teste não foi repetido e os dados privados não foram inspecionados. Por conseguinte, a troca sequencial real de provedores entre Codex e Antigravity permanece parcialmente comprovada e requer complementação na trilha Codex. O uso em projeto real permanece **BLOQUEADO**.

## Escopo e baseline

- Projeto coordenador: `Local AI Organizer`, branch `main`, commit `a9b36de6130cae83a598358dd7f359e02ab11898`.
- Ambiente operacional: subárvore temporária descartável `%LOCALAPPDATA%\Temp\codex-orca-pilot-20260915\model-routing`.
- Repositório sintético: `synthetic-repo` com worktrees `readonly` e `write`.
- Orca: `1.4.203` (executável resolvido em `%LOCALAPPDATA%\Programs\orca\resources\bin\orca.exe`).
- Antigravity CLI: `1.2.6` (resolvido em `%LOCALAPPDATA%\agy\bin\agy.exe`).
- Codex CLI: `0.152.0` (resolvido via script global do npm).
- Modo Manual do Orca preservado; argumentos globais de bypass vazios antes e depois.
- Pasta `.codex-docx-work/` mantida fora de escopo.

## Perfis de execução materializados

Arquivo criado: `docs/orca-model-routing-profiles.json`.

1. **Organizer Codex econômico (`organizer-codex-economy`):**
   - executor: `codex`;
   - modelo: `gpt-5.6-terra`;
   - esforço: `medium`;
   - contexto: `organizer-core-v1`;
   - fallback: `none`.
2. **Organizer Codex forte (`organizer-codex-strong`):**
   - executor: `codex`;
   - modelo: `gpt-5.6-sol`;
   - esforço: `high`;
   - contexto: `organizer-core-v1`;
   - fallback: `none`.
3. **Organizer Gemini econômico (`organizer-gemini-economy`):**
   - executor: `antigravity`;
   - modelo: `gemini-3.8-flash-medium`;
   - esforço: `medium`;
   - contexto: `organizer-core-v1`;
   - fallback: `none`.
4. **Organizer Gemini forte (`organizer-gemini-strong`):**
   - executor: `antigravity`;
   - modelo: `gemini-3.8-flash-high`;
   - esforço: `high`;
   - contexto: `organizer-core-v1`;
   - fallback: `none`.

Nenhum perfil indisponível ou com alias aproximado foi materializado.

## Mecanismo de seleção no Orca

- A inspeção do catálogo nativo de opções de sessão do Orca 1.4.203 (`CATALOGS`) confirmou que o Orca suporta opções nativas para `claude`, `codex`, `cursor` e `grok`, mas não possui catálogo de opções de sessão para o Antigravity (`agy`).
- A solução oficial escopada adotada foram **Quick Commands** vinculados estritamente ao repositório do Organizer (`repoId: <organizer-repo-id>`), registrados via RPC oficial `settings.updateTerminalQuickCommands`.
- Nenhum argumento foi adicionado a `agentDefaultArgs` e nenhum parâmetro global de modelo ou `--new-project` foi gravado. O Quick Command pré-existente de Erick foi integralmente preservado.

## Validações determinísticas

1. **Schema dos perfis:** todos os quatro perfis atendem aos 10 campos obrigatórios do contrato `orca-model-routing/v1`, com `fallback: none` e `single_writer: true`.
2. **Catálogo real verificado:**
   - Codex aceitou `gpt-5.6-terra` e `gpt-5.6-sol`;
   - Antigravity confirmou `gemini-3.8-flash-medium` e `gemini-3.8-flash-high` em `agy models`.
3. **Falha fechada com modelo inválido:**
   - Codex rejeitou `invalid-model-test-12345` com HTTP 400 (`The 'invalid-model-test-12345' model is not supported when using Codex with a ChatGPT account`);
   - Antigravity rejeitou `invalid-model-test-12345` com código 1 (`model is not recognized as a known model or custom model in settings`).
   - Nenhum dos dois executores acionou fallback silencioso.
4. **Higiene global:** `settings.agentDefaultArgs` permaneceu vazio para todos os agentes no arquivo de configuração do Orca.
5. **Hashes do contexto comum (`organizer-core-v1`):** inalterados antes e depois da execução.

## Validação real controlada

1. **Canário Antigravity (leitura confinada):**
   - Executado em `model-routing/worktrees/readonly` com perfil `organizer-gemini-economy` (`gemini-3.8-flash-medium`, esforço `medium`).
   - Reportou observavelmente executor (`antigravity`), modelo (`gemini-3.8-flash-medium`), esforço (`medium`) e cwd sintético.
   - Retornou o conteúdo de `README.md` e `fixture.txt` e citou exatamente as duas sentinelas de `AGENTS.md`:
     - Sentinela 1: *"Privacidade, operacao local e funcionamento offline sao os padroes."*
     - Sentinela 2: *"Trabalhe em uma unica etapa por vez."*
   - Nenhum arquivo foi modificado no worktree.
2. **Canário Codex (leitura confinada):**
   - Iniciado em `model-routing/worktrees/readonly` com `gpt-5.6-terra` e esforço `medium`.
   - Alcançou `hook: PreToolUse` e entrou em timeout sem progresso observável de ferramentas.
   - Execução interrompida; investigação restrita ao log do processo sem inspeção de dados pessoais ou histórico do usuário. Não foi realizada nova tentativa repetida.
3. **Escrita reversível (Antigravity):**
   - Executada em `model-routing/worktrees/write` com `gemini-3.8-flash-medium`.
   - Modificou exclusivamente `fixture.txt`, adicionando `+delta`.
   - `README.md` permaneceu intacto.
   - `fixture.txt` foi restaurado via Git ao hash original de baseline (`C8DBA68945249DE9B4FAED72B89E041E3DF77FFFF885122599E6C2F7C65A68B2`), deixando a working tree limpa.
4. **Cancelamento supervisionado pelo Orca:**
   - Terminal gerenciado criado no repositório sintético (`term_<synthetic-terminal-id>`).
   - `orca terminal close` encerrou o processo com `ptyKilled: true`.
   - Listagem confirmou o fechamento sem terminais sintéticos órfãos.

## Limitações e pendências

- O timeout do Codex em modo não interativo impede considerar a trilha multi-provedor completamente aprovada.
- O Orca 1.4.203 não expõe seletor nativo de modelo para Antigravity na interface de novas abas, sendo necessário o uso dos Quick Commands escopados ao repositório.
- A versão do Antigravity CLI observada durante esta etapa foi `1.2.6` (anteriormente `1.2.5` em 2026-09-17).
- O consumo exato de tokens e custos monetários permanece desconhecido.
- Nenhum projeto real foi alterado ou liberado para execução via Orca.

## Próximo passo seguro

Elaborar complemento restrito à estabilização do worker não interativo do Codex (`unelevated` tool use) sob timeout controlado para comprovar a troca sequencial com pacote de passagem antes de considerar qualquer uso real.

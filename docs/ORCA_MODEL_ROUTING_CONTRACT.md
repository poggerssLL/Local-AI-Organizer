# Contrato de roteamento de executores e modelos no Orca

Atualizado em: 2026-09-17.

## Identificação e estado

- contrato: `orca-model-routing/v1`;
- participantes: Erick, `Local AI Organizer`, Orca ADE, Codex CLI e Antigravity CLI;
- estado: **materializado e validado no complemento sintético (timeout estabilizado sob windows.sandbox=unelevated; projetos reais bloqueados)**;
- baseline confirmado no Organizer: branch `main`, `HEAD` e upstream em
  `a9b36de6130cae83a598358dd7f359e02ab11898`, com mudanças documentais preexistentes;
- executores confirmados por CLI: Codex CLI `0.152.0` e Antigravity CLI `1.2.6`;
- Orca: versão `1.4.203` (executável resolvido em
  `%LOCALAPPDATA%\Programs\orca\resources\bin\orca.exe`);
- catálogo real: `gpt-5.6-sol` e `gpt-5.6-terra` confirmados no Codex;
  `gemini-3.8-flash-medium` e `gemini-3.8-flash-high` confirmados no Antigravity (`agy models`).
- mecanismo no Orca: o Orca 1.4.203 possui opções nativas de sessão para Codex, mas não
  para Antigravity; a seleção escopada ao projeto foi implementada via quatro Quick
  Commands registrados no Orca para o repositório do Organizer (`repoId: <organizer-repo-id>`),
  sem alterar variáveis ou argumentos globais de bypass.
- validação sintética: Antigravity comprovou leitura confinada com sentinelas, escrita
  reversível em worktree separado e cancelamento supervisionado pelo Orca; o worker Codex
  teve o timeout em `hook: PreToolUse` elucidado e superado no complemento de 2026-09-18
  (`PHASE_ORCA_MODEL_ROUTING_COMPLEMENT_2026-09-18.md`): o travamento decorria de `sandbox = "elevated"`
  global em execução não interativa no Windows; o uso de `-c windows.sandbox=unelevated`
  estabilizou o processo sob `read-only`, completando com código 0 em ~18-19s. O aviso de
  skills `os error 183` foi comprovado como não causal. Contudo, em modo headless de turno único o
  Codex não acionou ferramentas de leitura de arquivos; logo, a leitura de sentinelas pelo Codex
  e o pacote de passagem automatizado entre provedores permanecem explicitamente como ainda não validados.

O piloto sintético anterior permanece aprovado. Este contrato continua sem liberar
roteamento em projeto real.

## Objetivo

Permitir que Erick use o Orca como painel do Organizer e selecione, para cada nova
execução, um perfil explícito de Codex ou Antigravity/Gemini. Ambos recebem o mesmo
contexto versionado e devolvem evidências no mesmo formato, sem fallback silencioso e sem
alterar permissões.

Resultado observável do MVP:

1. Erick escolhe um perfil pelo Orca;
2. o lançamento confirma executor, modelo, esforço, `cwd` e contexto;
3. somente um worker opera no checkout atribuído;
4. modelo ou perfil inválido falha sem substituição;
5. a troca de provedor encerra o worker anterior e inicia uma sessão nova com pacote de
   passagem;
6. um canário sintético demonstra que Codex e Antigravity leram o mesmo contexto.

## Fora do escopo

- selecionar automaticamente o provedor pela quantidade estimada de tokens;
- migrar memória interna ou histórico privado entre provedores;
- executar dois escritores no mesmo checkout;
- liberar escrita em projeto real, commit, push, merge ou publicação;
- persistir credenciais, IDs de sessão, caminhos pessoais ou telemetria em Markdown;
- usar API Gemini, OpenRouter ou outra API paga;
- instalar ou atualizar CLIs;
- habilitar bypass, Yolo, `always-proceed`, acesso fora do workspace ou controle visual.

## Partes e responsabilidades

| Participante | Responsabilidade | Fonte de verdade |
| --- | --- | --- |
| Erick | Escolher ou aceitar o perfil e autorizar ampliações | Pedido atual e gates explícitos |
| Organizer | Resolver projeto, perfil, contexto, permissões, handoff e evidências | Documentação versionada e Git |
| Orca | Expor o projeto, iniciar, observar e cancelar o processo no worktree correto | Estado do processo, terminal e worktree |
| Codex | Executar o perfil Codex dentro do envelope | Catálogo e saída do Codex CLI |
| Antigravity | Executar o perfil Gemini dentro do envelope | `agy models` e saída estruturada do CLI |

O Orca não decide sozinho qual executor usar. O modelo não recebe autoridade adicional por
ser mais barato, mais capaz ou possuir mais limite disponível.

## Contrato de perfil

Representação lógica, independente do formato de configuração que o Orca realmente
suportar:

```yaml
schema: orca-model-routing/v1
profile_id: organizer-gemini-flash-medium
project: Local AI Organizer
executor: antigravity
model: gemini-3.8-flash-medium
effort: medium
context_profile: organizer-core-v1
fallback: none
permissions_profile: manual-synthetic-readonly
single_writer: true
```

Campos obrigatórios:

- `profile_id`: nome estável e sem credencial;
- `project`: projeto e raiz resolvidos no momento da execução;
- `executor`: `codex` ou `antigravity` no MVP;
- `model`: identificador exato retornado pelo catálogo atual do executor;
- `effort`: valor aceito pelo modelo escolhido;
- `context_profile`: manifesto versionado de documentos;
- `fallback`: `none` no MVP;
- `permissions_profile`: envelope existente, sem ampliação implícita;
- `single_writer`: sempre `true` para escrita.

Perfis materializados em `docs/orca-model-routing-profiles.json` e validados:

| Perfil | Profile ID | Executor | Modelo confirmado | Esforço | Estado da validação |
| --- | --- | --- | --- | --- | --- |
| `Organizer Codex econômico` | `organizer-codex-economy` | Codex | `gpt-5.6-terra` | `medium` | Materializado; timeout superado com `windows.sandbox=unelevated` (ExitCode 0); leitura de sentinelas e handoff ainda não validados |
| Organizer Codex forte | `organizer-codex-strong` | Codex | `gpt-5.6-sol` | `high` | Materializado e aceito pelo catálogo Codex |
| Organizer Gemini econômico | `organizer-gemini-economy` | Antigravity | `gemini-3.8-flash-medium` | `medium` | Materializado; canário sintético validado com leitura e escrita reversível |
| Organizer Gemini forte | `organizer-gemini-strong` | Antigravity | `gemini-3.8-flash-high` | `high` | Materializado e confirmado em `agy models` |

Nenhum perfil indisponível foi materializado. Cada perfil segue rigorosamente o schema
`orca-model-routing/v1` com `fallback: none` e `single_writer: true`.

## Contexto comum

O perfil `organizer-core-v1` contém, nesta ordem:

1. `AGENTS.md`;
2. `docs/PROJECT_REGISTRY.md`;
3. `docs/SYSTEM_MAP.md`;
4. `docs/ORCHESTRATION_POLICY.md`;
5. `docs/ROADMAP.md`;
6. `docs/DELEGATION_TEMPLATE.md` quando houver delegação;
7. contrato e relatório da fase atual quando forem relevantes.

O projeto alvo acrescenta seu próprio `AGENTS.md` e documentação viva. Relatórios
históricos só entram quando citados pelo manifesto. Skills pessoais do Codex e skills do
Antigravity permanecem capacidades distintas e precisam ser descobertas no executor.

Cada canário deve devolver caminhos relativos, hashes dos documentos exigidos e duas
afirmações sentinela definidas pelo teste. Isso prova leitura do mesmo material, não
equivalência de raciocínio entre modelos.

## Troca e pacote de passagem

A troca de executor segue esta sequência:

```text
parar worker atual
  -> confirmar processo e terminal encerrados
  -> verificar cwd, Git e diff
  -> gerar handoff sanitizado
  -> validar perfil de destino
  -> iniciar nova sessão
  -> nova sessão relê o manifesto e confirma o handoff
```

O pacote de passagem contém somente objetivo, baseline, decisões, arquivos tocados, diff
resumido, testes executados, pendências e limitações. Não contém transcript completo,
credenciais, IDs de runtime, caminhos pessoais ou raciocínio privado.

## Segurança e permissões

| Capacidade | Padrão do MVP |
| --- | --- |
| leitura | somente fixture e documentos enumerados |
| escrita | negada no primeiro canário; depois apenas fixture descartável autorizada |
| terminal | comandos exatos necessários ao canário |
| rede | negada, exceto comunicação normal do CLI autenticado com seu provedor |
| instalação ou atualização | negada |
| credenciais e login | reservados a Erick |
| controle de teclado e mouse | proibido |
| commit, push, merge e publicação | proibidos |
| fallback de modelo | `none` |

O modo Manual e os argumentos vazios de bypass do Orca devem permanecer. A implementação
deve preferir configuração por projeto ou por lançamento. Não deve gravar globalmente
`--new-project`, modelo, esforço ou argumentos de permissão.

## Estados e falhas

- `READY`: perfil, contexto, `cwd` e permissões confirmados;
- `RUNNING`: um único worker aceitou a tarefa;
- `SUCCESS`: resposta e evidências atendem ao schema;
- `UNAVAILABLE`: executor ou modelo não está disponível;
- `CONTEXT_MISMATCH`: documento ou hash obrigatório divergiu;
- `PERMISSION_MISMATCH`: modo, sandbox ou argumentos diferem do contrato;
- `CANCELED`: processo foi interrompido e comprovadamente encerrado;
- `UNKNOWN`: não foi possível provar o resultado; não repetir efeitos automaticamente.

Qualquer `UNAVAILABLE`, `CONTEXT_MISMATCH` ou `PERMISSION_MISMATCH` falha fechado. Após no
máximo três tentativas fundamentadas da mesma causa, o gate é bloqueado.

## Validação incremental

1. Descobrir executáveis, versões, catálogo de modelos e mecanismo oficial do Orca para
   projeto, argumentos e Quick Commands.
2. Criar perfis sem executá-los e revisar o estado efetivo, mantendo backup de qualquer
   configuração não secreta alterada.
3. Executar canário somente leitura com Codex e Antigravity em ambiente sintético.
4. Provar modelo exato, `cwd`, contexto idêntico, falha fechada e cancelamento.
5. Provar troca sequencial com pacote de passagem, sem processos sobrepostos.
6. Se autorizado no mesmo envelope, executar escrita reversível somente em fixture.
7. Restaurar configurações e artefatos temporários, revisar Git e produzir relatório
   histórico.

O gate não aprova automaticamente operação em projeto real.

## Evidências mínimas

- executáveis e versões realmente resolvidos;
- catálogo sanitizado e perfis materializados;
- mecanismo usado pelo Orca e seu escopo de persistência;
- ausência de bypass antes e depois;
- eventos com executor, modelo, esforço, `cwd` e contexto;
- hashes e respostas sentinela dos dois executores;
- falha explícita para modelo inválido;
- prova de cancelamento e ausência de processos restantes;
- Git e configurações restaurados;
- consumo observado ou declaração de desconhecido;
- limitações e próximo passo.

## Fontes primárias para revalidação

- Orca: `https://www.onorca.dev/docs/agents/native-chat`,
  `https://www.onorca.dev/docs/agents/supported` e
  `https://www.onorca.dev/docs/cli/reference`;
- Codex: `https://learn.chatgpt.com/docs/developer-commands?surface=cli`;
- Antigravity: `https://antigravity.google/docs/cli/headless/`,
  `https://antigravity.google/docs/models` e
  `https://antigravity.google/docs/cli/gcli-migration/`.

## Condição de parada

Pare após decidir o gate sintético entre **APROVADO**, **COMPLEMENTO NECESSÁRIO** ou
**BLOQUEADO**, atualizar os documentos vivos e registrar o relatório histórico. Não abra
projeto real, não faça commit ou push e não inicie a fase seguinte.

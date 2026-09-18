# Prompt de implementação — roteamento de modelos do Organizer no Orca

Atualizado em: 2026-09-17.

## Perfil de execução recomendado

- executor recomendado: Antigravity;
- modelo: `gemini-3.8-flash-high`, somente se aparecer em `agy models` para a conta ativa;
- esforço: `high`;
- justificativa: integração entre Orca, dois CLIs, configuração persistente, isolamento,
  troca de processo e validação de segurança exigem investigação cuidadosa; o perfil
  também preserva os limites atuais do Codex de Erick;
- alternativa: Codex `gpt-5.6-sol` com esforço `high`; alternativa econômica Codex
  `gpt-5.6-terra` com esforço `medium` apenas se a descoberta mostrar um caminho simples
  e totalmente documentado;
- gatilho de escalada: incompatibilidade reproduzível de inicialização, prontidão ou
  persistência que permaneça sem causa após as tentativas previstas;
- limitações: disponibilidade e consumo devem ser consultados no momento da execução;
  assinatura de aplicativo não equivale a créditos de API.

## Prompt pronto para envio

```text
Erick autorizou implementar e validar, em ambiente sintético, o gate de estabilização e
roteamento de executores/modelos do Local AI Organizer no Orca. Trabalhe em uma única
etapa e prossiga autonomamente até o gate, sem iniciar projeto real, commit ou push.

Projeto coordenador

- projeto: Local AI Organizer;
- inicie no projeto salvo `Local AI Organizer`; não invente nem persista seu caminho
  físico;
- confirme obrigatoriamente a raiz com `git rev-parse --show-toplevel`;
- se houver `dubious ownership`, use apenas `git -c safe.directory=<raiz>` no comando
  necessário; não altere a configuração global;
- branch esperada: main;
- HEAD e upstream esperados na preparação: a9b36de6130cae83a598358dd7f359e02ab11898;
- preserve integralmente mudanças preexistentes e a pasta `.codex-docx-work/`, que não
  pertence a esta etapa;
- não trate o working tree como limpo.

Skills

- use `local-project-orientation`, `local-integration-architect` e
  `phase-gate-reviewer` se estiverem disponíveis no executor;
- use `local-ai-release-review` apenas para revisar o resultado, sem commit ou push;
- se uma skill não estiver disponível, não a instale nem finja que foi usada: siga as
  regras completas deste prompt e registre a limitação.

Leitura obrigatória, nesta ordem

1. AGENTS.md;
2. docs/PROJECT_REGISTRY.md;
3. docs/SYSTEM_MAP.md;
4. docs/ORCHESTRATION_POLICY.md;
5. docs/ROADMAP.md;
6. docs/DELEGATION_TEMPLATE.md;
7. docs/ORCA_PILOT_CONTRACT.md;
8. docs/ORCA_MODEL_ROUTING_CONTRACT.md;
9. docs/PHASE_ORCA_PILOT_SECOND_COMPLEMENT_2026-09-17.md;
10. README.md.

Baseline a revalidar

- confirmado na preparação: Codex CLI 0.152.0 e Antigravity CLI 1.2.5;
- informado pelo piloto: Orca 1.4.203;
- desconhecido: executável atual do Orca, que não estava disponível como `orca`,
  `orca-ide` ou `orca-dev` no PATH durante a preparação;
- desconhecido: catálogo efetivo de modelos das contas no momento da execução;
- histórico: o Antigravity exigiu `--new-project` para resolver corretamente o worktree,
  e o detector de prontidão do Orca precisou de `retry`;
- histórico: a configuração Manual terminou sem argumentos padrão de bypass.

Antes de editar ou executar workers

1. Revalide Git, versões e processos ativos.
2. Consulte documentação primária atual de Orca, Codex e Antigravity; não invente flags.
3. Resolva o executável/CLI do Orca pelo mecanismo documentado para a instalação atual.
   Não altere PATH global e não reinstale o Orca.
4. Consulte de forma sanitizada os modelos realmente disponíveis no Codex e em
   `agy models`, sem exibir conta, credenciais ou tokens.
5. Confirme que nenhum outro worker está modificando o checkout.
6. Inspecione e faça backup apenas de configuração não secreta que precise ser alterada.
   Nunca leia, copie ou registre arquivos de credenciais.

Objetivo único

Organizar o Local AI Organizer como projeto/workspace no Orca e disponibilizar perfis
selecionáveis, por projeto ou por execução, para iniciar Codex ou Antigravity com modelo e
esforço explícitos, contexto comum versionado, fallback desativado e permissões
inalteradas. Validar tudo em canário sintético antes de qualquer uso real.

Perfis desejados, condicionados ao catálogo real

1. Organizer Codex econômico: gpt-5.6-terra, medium.
2. Organizer Codex forte: gpt-5.6-sol, high.
3. Organizer Gemini econômico: gemini-3.8-flash-medium, medium.
4. Organizer Gemini forte: gemini-3.8-flash-high, high.

Não materialize um perfil cujo identificador não seja retornado pelo executor. Não use um
alias aproximado e não substitua modelo ou esforço silenciosamente. O padrão é
`fallback: none`.

Mecanismo de seleção

- prefira recurso oficial e escopado ao projeto do Orca: opções de lançamento, perfil de
  agente ou Quick Command;
- para Codex, valide seleção por execução ou pelo seletor suportado pelo Orca/Codex;
- para Antigravity, use o identificador exato e `--model`/`--effort` somente se a versão
  instalada confirmar essas flags;
- no Windows, preserve `--new-project` por execução quando necessário, sem persistir o
  argumento globalmente;
- se o Orca não suportar perfil de modelo escopado para Antigravity, crie a menor solução
  reversível documentada, como Quick Commands específicos por projeto; não edite padrões
  globais para simular essa capacidade;
- se uma etapa visual for inevitável para cadastrar o workspace ou Quick Command, pare
  apenas nesse ponto e dê a Erick uma instrução curta por vez. Controle direto de teclado
  e mouse está proibido.

Contexto comum

Implemente o perfil lógico `organizer-core-v1` conforme
`docs/ORCA_MODEL_ROUTING_CONTRACT.md`. Codex e Antigravity devem ler `AGENTS.md` e a mesma
lista de documentos centrais. Não carregue indiscriminadamente todos os `.md`.

Para uma troca de executor, gere um pacote de passagem sanitizado contendo somente:
objetivo, baseline, decisões, arquivos tocados, resumo do diff, testes, pendências e
limitações. Não transfira transcript completo, raciocínio privado, credenciais, IDs de
runtime ou caminhos pessoais.

Envelope de execução autônoma

Permitido:

- leitura do Organizer e de documentação oficial;
- administração da raiz temporária exata do piloto sintético;
- criação ou reconstrução de fixtures e worktrees descartáveis;
- descoberta de executáveis, versões e catálogos de modelos;
- backup e ajuste reversível de configurações não secretas estritamente necessárias;
- criação de perfis ou Quick Commands escopados ao projeto, quando o mecanismo oficial
  for comprovado;
- início, observação, cancelamento e encerramento dos workers sintéticos;
- no máximo três tentativas fundamentadas para a mesma causa;
- correção de falhas pertencentes a este gate;
- atualização dos documentos vivos e criação do relatório histórico.

Reservado/proibido:

- projetos reais além do Organizer e dos fixtures descartáveis;
- leitura ou escrita de dados pessoais;
- login, credenciais, termos, pagamento ou seleção de conta;
- instalação ou atualização de Orca, Codex, Antigravity ou dependências;
- PATH global, administração do sistema ou UAC;
- `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-skip-permissions`, Yolo,
  `always-proceed`, curingas globais ou acesso fora do workspace;
- fallback automático de provedor ou modelo;
- dois escritores no mesmo checkout;
- controle visual do computador;
- commit, push, merge ou publicação.

Permissões e invariantes

- preserve Orca em Manual e os argumentos padrão de bypass vazios;
- escolha de modelo não altera sandbox, allowlists ou capacidades;
- um único worker pode escrever em cada checkout;
- a troca ocorre somente após parar o worker anterior, confirmar ausência de processo,
  verificar Git e produzir o handoff;
- qualquer modelo inválido, contexto divergente, `cwd` incorreto ou permissão inesperada
  falha fechado;
- rede do worker fica limitada à comunicação normal já autenticada do próprio CLI com o
  provedor; nenhuma web, API adicional ou MCP é autorizada;
- não use API Gemini, OpenRouter ou chave de API nesta etapa.

Validação determinística

1. Validar schema e campos obrigatórios dos quatro perfis materializados.
2. Confirmar que perfis indisponíveis não foram criados.
3. Verificar que nenhuma configuração global ganhou modelo, `--new-project` ou bypass.
4. Comparar hashes dos documentos do contexto antes e depois.
5. Confirmar Git dos fixtures e do Organizer antes e depois.
6. Forçar um modelo inválido em fixture e exigir erro explícito sem fallback.
7. Confirmar zero processos e terminais gerenciados restantes no encerramento.

Validação real controlada

1. Em worktree sintético somente leitura, iniciar um perfil Codex e um perfil
   Antigravity, sequencialmente.
2. Exigir que cada worker reporte executor, modelo efetivo, esforço, cwd e modo de
   permissão por evidência observável, não apenas por autodeclaração.
3. Exigir leitura do mesmo manifesto e retorno das mesmas duas sentinelas documentais e
   hashes esperados.
4. Provar cancelamento de cada worker pelo Orca.
5. Provar troca Codex -> Antigravity ou Antigravity -> Codex com pacote de passagem,
   verificando que os processos não se sobrepõem.
6. Se todos os critérios de leitura forem satisfeitos, permitir escrita reversível
   somente em `fixture.txt` de outro worktree descartável, restaurando conteúdo, ACLs e
   hashes ao final.

Mocks e simulações

- mocks podem validar parser, schema e transições de estado;
- mocks não substituem a comprovação real de modelo efetivo, cwd, contexto, cancelamento
  ou permissões;
- registre separadamente resultados simulados e reais.

Documentação

- atualize, apenas conforme fatos comprovados: AGENTS.md, README.md,
  docs/PROJECT_REGISTRY.md, docs/SYSTEM_MAP.md, docs/ORCHESTRATION_POLICY.md,
  docs/ROADMAP.md, docs/DELEGATION_TEMPLATE.md, docs/ORCA_PILOT_CONTRACT.md e
  docs/ORCA_MODEL_ROUTING_CONTRACT.md;
- crie `docs/PHASE_ORCA_MODEL_ROUTING_2026-09-17.md` como relatório histórico
  sanitizado;
- não reescreva os relatórios históricos existentes;
- marque claramente perfis implementados, perfis apenas propostos e itens bloqueados;
- atualize o roadmap com o gate atingido e o próximo passo real, sem liberar projeto real
  implicitamente.

Git e dados

- preserve mudanças preexistentes e não relacionadas;
- mantenha `.codex-docx-work/` fora do escopo e do versionamento;
- não registre caminhos absolutos pessoais, IDs de terminal, sessão ou host, nomes de
  conta, credenciais, tokens, conteúdo privado ou configurações secretas;
- execute `git diff --check`, revise o diff e informe todos os arquivos alterados;
- não faça commit nem push.

Decisão do gate

Use `phase-gate-reviewer` quando disponível e escolha exatamente uma decisão:

- APROVADA: perfis realmente disponíveis foram materializados, seleção e modelo efetivo
  foram comprovados, contexto foi idêntico, falha fechada e troca sequencial funcionaram,
  permissões permaneceram intactas e tudo foi restaurado;
- COMPLEMENTO NECESSÁRIO: há uma lacuna delimitada corrigível na mesma etapa;
- BLOQUEADA: executável, versão, modelo, isolamento, prontidão ou mecanismo escopado ao
  projeto não permite a implementação segura.

Resposta final

Comece com a decisão. Separe:

- implementado;
- testes determinísticos e mocks;
- validação real;
- ações manuais de Erick;
- estado Git e configurações;
- perfis disponíveis e indisponíveis;
- consumo observado ou desconhecido;
- limitações e próximo passo permitido.

Pare após o gate. Não inicie piloto em projeto real, commit, push ou outra fase.
```

## Ação não executada

Este arquivo apenas prepara a implementação. Nenhuma tarefa foi criada, nenhum worker foi
iniciado e nenhuma configuração do Orca foi alterada.

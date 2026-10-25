# Segundo complemento do piloto Orca com Antigravity - 2026-09-17

## Decisão do gate

**APROVADA no escopo sintético.** A trilha do Antigravity comprovou leitura confinada,
bloqueio de escrita, escrita reversível em worktree separado, restauração dos hashes e
cancelamento de worker supervisionado pelo Orca. A aprovação encerra somente este piloto
descartável. Nenhum projeto real foi liberado, e não houve commit, push, merge ou
publicação.

Este documento complementa, sem substituir,
`PHASE_ORCA_PILOT_2026-09-15.md` e
`PHASE_ORCA_PILOT_COMPLEMENT_2026-09-16.md`.

## Escopo e baseline

- projeto coordenador: `Local AI Organizer`, branch `main`, com mudanças preexistentes
  preservadas;
- ambiente operacional: `%TEMP%\codex-orca-pilot-20260915\second-complement`, contendo
  somente repositório sintético e dois worktrees descartáveis;
- worktrees: `antigravity-readonly` e `antigravity-write`, ambos confirmados por Git;
- Orca: `1.4.203`;
- modo Manual do Orca preservado, sem argumento ou comando padrão de bypass;
- Antigravity: `1.2.4` no início e `1.2.5` no fim, após atualização automática observada;
- configuração anterior do Antigravity: arquivo de preferências ausente, restaurado ao
  final;
- argumentos padrão do Antigravity no Orca: vazios antes e depois do complemento;
- testes já aprovados da trilha Codex: não repetidos.

## Ações do coordenador

1. Revalidou projeto, raiz Git, baseline e mudanças preexistentes do Organizer.
2. Resolveu a raiz temporária do usuário e criou uma subárvore nova porque os resíduos
   anteriores não formavam um estado inequívoco. Os resíduos históricos foram
   preservados.
3. Reconstruiu o fixture e os dois worktrees, confirmou suas raízes por Git e registrou
   conteúdo e hashes fora do worker.
4. Manteve `allowNonWorkspaceAccess` efetivamente falso, não concedeu comandos durante a
   prova de diretório e não usou bypass ou curinga global.
5. Identificou que uma sessão sem `--new-project` mantinha o projeto lógico padrão.
   Encerrou-a antes de permitir ferramentas e reiniciou o Antigravity pelo Orca com o
   `cwd` do worktree e `--new-project`.
6. Configurou negações específicas para a escrita proibida. Para o worktree de escrita,
   aplicou ACLs temporárias que impediram criação de outros arquivos e gravação em
   `README.md` e `.git`, mantendo somente `fixture.txt` gravável.
7. Comparou conteúdo, hashes, diff e Git externamente; restaurou o fixture e todas as
   ACLs; removeu as regras temporárias ao restaurar o arquivo de configuração anterior.
8. Criou e acompanhou o Run do Orca, recuperou a incompatibilidade de prontidão com um
   `retry` supervisionado, cancelou o worker possuído pelo Orca e encerrou os terminais.

## Ações do worker Antigravity

1. Após evento inicial com `cwd` exato, leu somente `README.md` e `fixture.txt` no
   worktree de leitura e devolveu o conteúdo esperado.
2. Tentou criar `forbidden.txt`; a regra específica negou a ferramenta, e o worker
   reportou o bloqueio.
3. No worktree de escrita, leu e alterou somente `fixture.txt`, acrescentando a linha
   `delta`.
4. Em um worker inofensivo separado, permaneceu processando sem ferramentas até receber
   o cancelamento do Orca.

O worker não executou comandos, não acessou rede e não recebeu caminhos absolutos nos
prompts de leitura ou escrita.

## Ações manuais de Erick

- instalou o Antigravity antes do complemento;
- no primeiro terminal interativo, escolheu tema e renderização e confirmou a confiança
  no worktree sintético;
- não enviou credenciais ao agente. A autenticação existente foi apenas confirmada por
  estado operacional do CLI.

Depois dessas ações, o coordenador confirmou por CLI o worktree, o prompt principal, o
modo de permissão e a ausência de argumentos de bypass.

## Validação real

- a inicialização headless com `--new-project` registrou o `cwd` exatamente igual ao
  worktree autorizado;
- a leitura real dos dois arquivos coincidiu com o conteúdo e os hashes externos;
- a criação real de `forbidden.txt` foi negada, e o arquivo permaneceu ausente;
- a escrita real acrescentou somente `delta` a `fixture.txt` no worktree separado;
- a restauração devolveu o arquivo ao hash original;
- o worker de cancelamento chegou a `ready`, com entrada aceita e recurso `owned/active`;
- `worker-stop` retornou `stopped`, fechou o terminal do agente e confirmou o encerramento
  do PTY;
- a listagem final do Orca retornou zero terminais, e não havia processo `agy` ativo.

## Verificações determinísticas

| Arquivo sintético | SHA-256 original e final |
| --- | --- |
| `README.md` | `426632A0A02A74F91326B0F76915CF6B97D75687A6907EA8803313B8C154667D` |
| `fixture.txt` | `4FDBC441EA7B546100E086AC1E4FC5AE6749B7314311C99DB05BE450ECA12996` |

- os hashes finais coincidiram nos dois worktrees;
- `forbidden.txt` permaneceu ausente;
- cada worktree terminou somente com `.git`, `README.md` e `fixture.txt`;
- o diff da escrita continha apenas `+delta` antes da restauração;
- as ACLs temporárias terminaram sem entradas de negação adicionadas pelo piloto;
- os worktrees continuaram sem commits, com somente os dois fixtures não rastreados;
- a configuração do Orca terminou sem argumento ou comando padrão para Antigravity;
- o arquivo temporário de preferências do Antigravity foi removido para restaurar o
  baseline anterior.

## Tentativas e recuperação

- A correspondência de allowlists exatas sob `toolPermission: strict` não autorizou
  leituras e escrita headless como esperado. O piloto não ampliou regras: usou
  `request-review`, que autoautoriza arquivos internos, combinado com negação específica
  e confinamento por ACL no worktree de escrita.
- Um terminal criado antes da supervisão foi corretamente rejeitado como prova de
  cancelamento porque era `external`.
- Dois lançamentos de terminal possuído pelo Orca expiraram no detector de prontidão,
  embora o segundo tenha chegado ao prompt do Antigravity. Na terceira e última tentativa
  dessa causa, o `retry` transferiu a posse do mesmo terminal ao novo despacho, aceitou a
  tarefa e permitiu o cancelamento supervisionado.
- O fechamento em massa dos dois terminais vazios retornou estado incompleto, e a primeira
  tentativa por aba encontrou identificadores obsoletos. A terceira estratégia, fechando
  cada terminal pelo painel exato sem fechar a aba inteira, encerrou ambos e zerou a
  listagem.

## Desconhecidos e limitações

- O mecanismo que atualizou automaticamente o Antigravity de 1.2.4 para 1.2.5 não foi
  controlado pelo piloto. Uma adoção futura deve estabilizar ou registrar a versão antes
  de comparar resultados.
- O Orca 1.4.203 não reconheceu diretamente a prontidão do Antigravity 1.2.5 neste fluxo;
  a recuperação por `retry` é evidência do cancelamento, não garantia de compatibilidade
  geral.
- `--new-project` foi necessário, mas não ficou persistido globalmente no Orca. Isso
  preserva a configuração anterior e evita efeitos em outras sessões, porém exige uma
  solução explícita antes de automatizar novas execuções.
- O custo monetário e o total consolidado de tokens do complemento são desconhecidos.
- A prova usa fixtures mínimos e não demonstra segurança, correção ou desempenho em um
  projeto real.

## Conclusão do gate

Os critérios do segundo complemento foram satisfeitos com evidência real e
determinística. O gate da trilha sintética fica **APROVADO**. O gate de projeto real
permanece **FECHADO** até autorização nominal de Erick e nova revisão que trate versão,
inicialização, prontidão, permissões e escopo do projeto candidato.

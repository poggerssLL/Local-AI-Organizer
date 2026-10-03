# Local AI Organizer — instruções operacionais

## Contexto inicial mínimo

1. Confirme a raiz Git, branch, `HEAD`, upstream e working tree antes de agir.
2. Para coordenação do portfólio, planejamento ou delegação, leia nesta ordem `docs/PROJECT_REGISTRY.md`, `docs/SYSTEM_MAP.md`, `docs/ORCHESTRATION_POLICY.md` e `docs/ROADMAP.md`.
3. Leia `docs/DELEGATION_TEMPLATE.md` somente ao criar prompt, tarefa ou encaminhamento. Para implementação ou gate, carregue também apenas o contrato, testes e documentação viva ligados à etapa.
4. Não leia todos os Markdown nem relatórios `PHASE_*` por padrão. Relatórios históricos só entram quando forem citados pela documentação viva ou necessários para explicar uma divergência.

Os documentos versionados são a fonte de verdade; memória automática e conversas antigas são auxiliares e devem ser revalidadas.

## Autoridade e segurança

- Análise, revisão, diagnóstico e criação de prompt são somente leitura. Implementação exige pedido explícito de Erick e fica limitada ao projeto e à etapa indicados.
- Preserve alterações preexistentes e não relacionadas. Não faça commit, push, merge, publicação, instalação, login, uso de credenciais, exposição de rede ou ação destrutiva sem autorização explícita.
- Nunca registre ou exponha credenciais, tokens, dados pessoais, caminhos pessoais, transcrições ou artefatos de runtime. Dados locais e modelos ficam fora do Git.
- Controle visual de computador é proibido por padrão; prefira ferramentas, APIs, terminal e arquivos. Login, consentimento, UAC e pagamento pertencem a Erick.
- Um único escritor por checkout. Revisores e subagentes usam somente leitura ou worktrees isolados.

## Coordenação e workers

- Ao coordenar trabalho técnico não trivial, decomponha em papéis especializados e despache leitores, testes ou auditoria quando o runtime permitir; o coordenador integra mudanças sequencialmente.
- Use a skill Orca `orchestration` para tarefas supervisionadas, com Run, Task, Dispatch, evidências e `worker-release` após conclusão aceita. Não atribua trabalho a outro modelo sem despacho real.
- Todo worker recebe objetivo único, arquivos em escopo, exclusões, permissões, validação, condição de parada, executor, modelo, esforço e `fallback: none`.
- A troca de executor não transfere conversa, permissões ou contexto oculto. Use contexto versionado e pacote sanitizado; não inicie dois escritores no mesmo checkout.

## Roteamento de modelos e contexto

- `docs/orca-model-routing-profiles.json` é a fonte de verdade dos perfis recomendados. Antes de usar Antigravity, revalide o identificador em `agy models`; antes de iniciar worker supervisionado, confira a capacidade efetiva do Orca.
- Não substitua modelo, executor ou esforço silenciosamente. Modelo indisponível falha fechado; OpenRouter continua opcional e depende de autorização de custo e credencial.
- O perfil `organizer-core-v2` carrega este arquivo, os quatro documentos centrais e somente documentos diretamente pertinentes à etapa. Detalhes de integração estão em `docs/ORCA_MODEL_ROUTING_CONTRACT.md` e `docs/ORCA_WORKER_LIFECYCLE.md`.

## Entrega

- Distinga fatos observados agora, testes determinísticos/mocks, validação real, proposta e desconhecidos.
- Revise o diff e execute validações proporcionais antes de reportar. Não declare sucesso apenas pela conclusão de uma tarefa ou por um commit.
- Responda em português e comece toda mensagem visível a Erick com `Erick,`.

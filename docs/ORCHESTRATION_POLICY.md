# Política de orquestração

## Objetivo

Definir quando o coordenador pode analisar, criar prompts, abrir tarefas e acompanhar
outros projetos. O princípio central é: planejamento pode ser proativo; alterações exigem
autorização explícita e escopo verificável.

## Autoridade por tipo de pedido

| Pedido de Erick | Ação permitida |
| --- | --- |
| “Explique”, “analise”, “diagnostique” ou “revise” | Ler e responder; não corrigir nem abrir tarefa implementadora |
| “Crie o prompt” | Produzir o prompt; não enviá-lo nem iniciar outra tarefa |
| “Delegue”, “crie uma tarefa” ou “inicie a etapa” | Criar uma única tarefa no projeto indicado, com o escopo autorizado |
| “Implemente” | Alterar somente o projeto e a etapa explicitamente autorizados |
| “Faça commit” ou “publique” | Commitar ou enviar ao remoto somente os arquivos da mudança autorizada e após validação |
| “Monitore” ou “acompanhe” | Usar o mecanismo de acompanhamento adequado sem ampliar o escopo da tarefa |

Uma autorização para criar tarefa não autoriza downloads, instalações, mudanças de
sistema, credenciais, exposição de rede, commit ou push quando esses atos não estiverem
incluídos no pedido ou no prompt aprovado.

## Ciclo obrigatório de delegação

1. Identificar o projeto e o modo solicitado.
2. Consultar `PROJECT_REGISTRY.md`, `SYSTEM_MAP.md` e `ROADMAP.md`.
3. Localizar o projeto salvo no Codex pelo rótulo atual.
4. Abrir o repositório alvo e ler suas instruções antes de confirmar o baseline.
5. Classificar o estado como confirmado, informado, planejado ou desconhecido.
6. Selecionar somente as skills disponíveis e adequadas.
7. Produzir um prompt com objetivo único usando `DELEGATION_TEMPLATE.md`.
8. Criar uma única tarefa no projeto alvo quando Erick tiver autorizado a delegação.
9. Acompanhar a tarefa sem iniciar outra escrita concorrente no mesmo checkout.
10. Revisar o resultado, as evidências, a documentação e o Git.
11. Aprovar, bloquear ou solicitar complemento na mesma tarefa.
12. Atualizar os documentos centrais somente quando o estado factual mudar.

## Tarefas separadas e subagentes

Use uma **tarefa separada do Codex** quando:

- o trabalho pertence a outro projeto;
- haverá implementação, commit ou publicação;
- o resultado precisa permanecer visível e retomável por Erick;
- o projeto alvo possui instruções ou skills próprias.

Use **subagentes dentro da tarefa atual** somente quando:

- as subtarefas são independentes e delimitadas;
- a delegação melhora uma análise, pesquisa, inspeção ou teste;
- os agentes não modificarão simultaneamente o mesmo checkout;
- o resultado será reunido pelo agente principal.

Não use subagentes como substitutos de tarefas persistentes entre projetos. Fluxos com
subagentes podem consumir mais tokens e aumentar conflitos quando há escrita paralela.

## Seleção de skills

O coordenador deve preferir skills pessoais para procedimentos comuns a vários projetos e
skills do repositório para regras específicas. A menção explícita no prompt é preferível
em etapas críticas.

Coleção planejada, criada uma por vez:

| Skill | Função | Estado em 2026-09-14 |
| --- | --- | --- |
| `local-project-orientation` | Confirmar projeto, raiz, instruções e estado inicial | Criada, aprovada pelo validador e descoberta pelo Codex em 2026-09-14 |
| `phase-gate-reviewer` | Aprovar, bloquear ou pedir complemento de uma etapa | Planejada |
| `implementation-prompt-builder` | Gerar um prompt implementador completo | Planejada |
| `local-ai-release-review` | Revisar higiene, documentação, commit e publicação | Planejada |
| `local-project-coordinator` | Priorizar o portfólio e delegar tarefas | Planejada |
| `local-integration-architect` | Projetar contratos seguros entre projetos | Planejada |

A ausência dessas skills não impede a delegação: o coordenador pode seguir esta política e
o modelo de prompt manualmente. As skills reduzem repetição e variação, mas não concedem
permissões nem disponibilizam ferramentas inexistentes.

## Pré-requisitos operacionais

Antes de criar uma tarefa, confirme:

- o projeto alvo aparece entre os projetos salvos;
- a raiz correta foi resolvida no momento da ação;
- o usuário autorizou a criação da tarefa;
- não existe outra tarefa modificando o mesmo checkout;
- as skills citadas estão disponíveis no contexto do projeto alvo;
- o prompt contém escopo, exclusões, validações e condição de parada;
- dados pessoais, credenciais e identificadores de runtime não serão persistidos.

Se o projeto ainda não estiver salvo, informe isso a Erick. Não crie um repositório, não
invente um caminho e não use outro projeto como substituto.

## Limites do coordenador

O coordenador não pode:

- ampliar uma autorização por conta própria;
- garantir que uma tarefa terminou corretamente sem revisar evidências;
- tornar uma skill indisponível magicamente disponível apenas mencionando seu nome;
- contornar sandbox, permissões, autenticação ou políticas do sistema;
- operar continuamente sem um pedido atual ou uma automação explicitamente criada;
- resolver escolhas pessoais ou riscos relevantes sem consultar Erick.

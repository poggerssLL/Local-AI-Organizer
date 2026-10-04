# Contrato de colaboração Codex + Antigravity

Atualizado em: 2026-10-04. Este contrato define colaboração entre executores locais; não
substitui a autorização de Erick para cada projeto, etapa ou alteração.

## Objetivo e limites

Codex e Antigravity são executores distintos. A colaboração combina papéis especializados,
não memória oculta, permissões, credenciais ou acesso implícito entre eles. Cada Dispatch
deve registrar executor, modelo, esforço, skills descobertas, projeto, checkout, escopo,
validação, parada e `fallback: none`.

O canário Orca 1.4.219 comprova o caminho supervisionado em fixture descartável. Ele não
autoriza automaticamente escrita em projeto real, commit, push, rede, instalação, controle
visual ou uso de dados privados.

## Papéis e propriedade

| Papel | Executor possível | Permissão padrão | Responsabilidade |
| --- | --- | --- | --- |
| Coordenador | Codex ou Antigravity | leitura e orquestração | delimitar etapa, despachar, integrar evidências e parar no gate |
| Arquiteto ou auditor | Codex ou Antigravity | somente leitura | revisar contratos, riscos, documentação e critérios de aceite |
| Implementador | um executor nomeado | escrita no checkout autorizado | produzir uma alteração delimitada e validar localmente |
| QA ou gate | executor diferente quando disponível | somente leitura | revisar diff, evidências, testes e limitações |

Há exatamente um escritor por checkout. Leitores e auditores paralelos usam somente leitura
ou worktrees isolados. Dois executores nunca escrevem no mesmo checkout em paralelo.

## Sequência obrigatória

1. Erick autoriza uma etapa e um projeto; o coordenador confirma raiz Git, `AGENTS.md`,
   baseline e working tree.
2. O coordenador escolhe perfis existentes no catálogo, revalida o modelo e cria um pacote
   sanitizado com objetivo, escopo, exclusões, arquivos, validações, parada e evidências
   anteriores relevantes.
3. Leitores, arquitetos e auditores podem trabalhar em paralelo sem escrita. O escritor
   inicia somente quando não houver outro escritor ativo no checkout.
4. O escritor entrega resultado, testes e limitações por `worker_done`. O coordenador revisa
   as evidências, registra o gate e executa `worker-release` após a conclusão aceita.
5. Uma troca de executor exige encerramento verificável do worker anterior, Git revisado e
   nova passagem sanitizada. Nenhum executor escolhe fallback, amplia permissões ou retoma
   contexto de outro automaticamente.

## Pacote de passagem mínimo

O pacote entre Codex e Antigravity contém somente:

- projeto e raiz Git confirmados no momento da tarefa;
- branch, `HEAD`, working tree e baseline relevantes;
- objetivo único, papel, escopo e itens fora do escopo;
- executor, modelo, esforço, skills efetivamente disponíveis e `fallback: none`;
- permissões, único escritor, worktree, validações, condição de parada e modo de Git;
- evidências sanitizadas e limitações conhecidas.

Ele nunca contém credenciais, tokens, transcrições, bancos, caminhos pessoais, logs brutos
ou dados privados.

## Gates e falhas

- Sem autorização explícita de escrita, todos os participantes permanecem em leitura.
- Sem recibo de modelo efetivo, `worker_done`, evidência de validação e `worker-release`, o
  Dispatch não é considerado concluído.
- Falha de um executor é fail-closed: não inicia outro, não altera modelo e não amplia
  permissões sem nova decisão de Erick.
- Commit, push, publicação, login, UAC, pagamento, rede pública e controle visual são gates
  separados, mesmo quando a implementação tiver sido concluída.

## Piloto antes de projeto real

O primeiro uso conjunto em um projeto real deve ser uma alteração reversível e autorizada,
com escopo pequeno, um escritor nomeado e revisão independente. Evidência de fixture
descartável prova apenas o mecanismo de orquestração; não prova compatibilidade, qualidade
ou autorização do projeto real.

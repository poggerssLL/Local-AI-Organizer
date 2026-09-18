---
name: local-ai-release-review
description: Revise uma mudança antes de commit ou push, verificando autorização, escopo, evidências, documentação, Git, dados privados e remoto. Use em gates de release; não corrija, commite nem publique sem autorização.
---

# Revisão de release local

Determine se uma mudança está pronta para commit, push ou encerramento. A revisão é
somente leitura por padrão e prontidão não concede autorização.

Use `local-project-orientation` se faltar baseline. Confirme escopo, branch, HEAD,
upstream, working tree, mudanças preexistentes, aceite, evidências e autorizações separadas
para commit e push.

## Pré-commit

Inspecione lista de arquivos e diff completo. Confirme escopo, preservação de mudanças
alheias, ausência de credenciais/dados pessoais/runtime, coerência de documentação e
roadmap, separação entre mocks e validação real, limitações declaradas e `git diff
--check`. Se commit estiver autorizado, prepare apenas caminhos explícitos e revise o
staged diff.

## Pré-push

Push exige autorização própria. Confirme commit, mensagem, arquivos, working tree,
upstream e validações após a última mudança. Não faça `fetch` nem altere remoto apenas
para obter evidência sem autorização; classifique o remoto não atualizado como
desconhecido.

## Veredito

Escolha exatamente um: **PRONTO PARA COMMIT**, **PRONTO PARA PUSH**, **COMPLEMENTO
NECESSÁRIO** ou **BLOQUEADO**. Apresente baseline, arquivos incluídos/excluídos,
evidências, Git, riscos e próximo ato permitido, indicando se está autorizado. Pare sem
editar, commitar ou publicar.

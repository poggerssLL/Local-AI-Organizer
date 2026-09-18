---
name: phase-gate-reviewer
description: Revise a conclusão ou prontidão de uma etapa com base em critérios, evidências, documentação e Git, decidindo entre aprovar, bloquear ou solicitar complemento. Use em gates entre etapas; não implemente correções.
---

# Revisor de gate de etapa

Produza uma decisão verificável sobre uma única etapa. A revisão é somente leitura por
padrão e não autoriza correções, nova etapa, worker, commit ou publicação.

## Preparação e evidências

Use `local-project-orientation` quando ainda não houver baseline válido. Identifique etapa,
objetivo, branch, commit, versão, schema, critérios de aceite, condição de parada e
evidências prometidas. Não use o Organizer como substituto do repositório alvo.

Priorize documentação viva e estado observado. Classifique evidências como:

- **confirmado agora**;
- **teste determinístico ou mock**;
- **validação real**;
- **informado ou histórico**;
- **desconhecido**.

Verifique critérios individualmente, branch, HEAD, upstream, working tree, mudanças
preexistentes, documentação, roadmap, compatibilidade, artefatos proibidos, dados privados
e limitações. Término de tarefa ou mensagem de sucesso não prova aprovação.

## Decisão

Escolha exatamente uma:

- **APROVADA:** critérios e evidências suficientes, sem bloqueador material;
- **COMPLEMENTO NECESSÁRIO:** faltam correções ou evidências delimitadas na mesma etapa;
- **BLOQUEADA:** risco, pré-requisito, projeto ou evidência impedem avanço seguro.

Apresente decisão, baseline, matriz curta de critérios, natureza das validações, Git,
documentação, riscos e próximo passo permitido. Em revisão isolada, pare sem implementar.
Se houver envelope explícito para escrita documental, atualize o roadmap somente com o
marco comprovado, sem iniciar a etapa seguinte.

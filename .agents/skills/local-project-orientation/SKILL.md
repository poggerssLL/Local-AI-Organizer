---
name: local-project-orientation
description: Oriente trabalho técnico em um projeto local antes de análise, diagnóstico, revisão, implementação ou monitoramento, confirmando caminho, raiz Git, instruções, documentação e estado do repositório. Use no início do trabalho; não use para perguntas genéricas nem repita uma orientação ainda válida.
---

# Orientação de projeto local

Estabeleça um baseline factual antes do trabalho técnico. A orientação é sempre somente
leitura e não amplia a autorização do pedido atual.

## Procedimento

1. Declare projeto, caminho candidato, modo pedido e autorização efetiva.
2. Confirme o caminho e execute `git rev-parse --show-toplevel` antes de ler código ou
   documentação técnica. Se a raiz divergir, pare e informe a divergência.
3. Leia todos os `AGENTS.md` aplicáveis dentro do repositório confirmado.
4. Inventarie e leia a documentação indicada pelas instruções. Priorize contrato, estado,
   arquitetura, roadmap, decisões, problemas conhecidos, relatório da etapa e README.
5. Consulte branch, HEAD, upstream e working tree com comandos somente leitura.
6. Classifique as informações como **confirmado agora**, **informado**, **histórico** ou
   **desconhecido**.
7. Resuma projeto, raiz, autorização, documentos, Git, divergências, mudanças
   preexistentes, limitações e somente o próximo passo permitido.

## Limites

Durante a orientação, não edite arquivos, instale dependências, baixe artefatos, execute
testes ou builds, altere Git, crie workers nem atravesse para repositórios irmãos. Uma
exceção temporária de `safe.directory` pode ser usada somente no comando Git de leitura
que estiver bloqueado; não altere a configuração global.

Relatórios históricos, memória de conversa e mensagens de outro executor não comprovam o
estado atual. Pare após o resumo; não inicie automaticamente a etapa seguinte.

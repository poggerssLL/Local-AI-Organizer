# Guia de UI com daisyUI

Use este guia em trabalhos de UI com HTML, JSX e Tailwind. Antes de alterar a marcação, leia [a skill daisyUI](../.agents/skills/daisyui/SKILL.md), os guias `usage` e `colors`, e os guias dos componentes pertinentes; para uma busca, isto inclui `input`, `join`, `button` e `label`.

Preserve o framework, as dependências, a página atual e o tema existente. Não instale pacote nem altere configuração de tema sem autorização específica. Use componentes e classes reais da daisyUI/Tailwind, nunca nomes de classes inventados; mantenha o layout responsivo, a associação semântica entre rótulo e campo, foco de teclado visível e contraste compatível com o tema.

## Exemplo de solicitação para busca existente

O prompt abaixo é específico para melhorar controles de busca que já existem: pede um formulário `GET` na mesma página, `q` como nome do campo, rótulo associado por `for`/`id` e input e botão unidos por `join`. Não autoriza incluir busca inoperante em qualquer site nem restringe outras alterações futuras que o usuário vier a autorizar.

```text
Use the daisyUI skill to improve this project's existing search controls.
Keep the project's framework, dependencies, and current page.
Add a visible Search projects label connected to a search input.
Use a native GET form on the current page, with q as the input name.
Keep input and button together with daisyUI join classes. Use input for the field and btn btn-primary for the submit button.
Make the field fit a narrow screen without making the button unreadable.
Keep keyboard focus visible and keep the project's existing theme colors.
Do not add JavaScript, a new route, a search backend, or a package.
Show the changed markup and list the checks you actually ran.
```

## Verificações por tarefa

Execute e relate somente as verificações realmente feitas:

- nomes, `id` e associação nativa entre `label`, controle e `form`;
- links e destino do formulário na página atual;
- navegação por teclado e foco visível;
- viewport estreito, tema ativo e contraste;
- preservação do framework, das dependências e das exclusões autorizadas;
- revisão do diff.

No relatório final, mostre a marcação alterada e a lista dos checks reais executados; nunca afirme que rodou testes, validações ou inspeções que não foram executados.

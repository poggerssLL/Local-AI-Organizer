# Modelo de delegação entre tarefas

Use este documento quando Erick autorizar o coordenador a criar uma tarefa em outro
projeto. Resolva ao vivo o caminho e o baseline; não salve IDs de runtime neste arquivo.

## Antes de criar a tarefa

- projeto solicitado: `[rótulo exato do projeto salvo]`;
- modo autorizado: `[revisão | diagnóstico | implementação | monitoramento]`;
- objetivo único: `[resultado concreto]`;
- skills disponíveis e adequadas: `[lista ou nenhuma]`;
- existência de outra tarefa escrevendo no mesmo checkout: `[não | sim, parar]`;
- baseline: `[confirmado no repositório | informado e ainda não confirmado]`.

## Perfil de execução

Antes de criar a tarefa, recomende e justifique:

- modelo: `[MODELO DISPONÍVEL NO DESTINO]`;
- esforço: `[NÍVEL COMPATÍVEL COM O MODELO]`;
- motivo: `[COMPLEXIDADE, RISCO E CUSTO DE RETRABALHO]`;
- alternativa econômica: `[PERFIL OU NÃO RECOMENDADA]`;
- gatilho de escalada: `[CONDIÇÃO OBJETIVA]`;
- limitações: `[DISPONIBILIDADE OU CONSUMO DESCONHECIDO]`.

Consulte a disponibilidade real no momento da delegação. Não trate preços da API como
equivalentes ao consumo dos limites do aplicativo Codex e não prometa economia de tokens.

## Prompt-base

```text
Atue somente no projeto [NOME DO PROJETO].

Use as skills [SKILLS DISPONÍVEIS], seguindo as instruções específicas do repositório.

Antes de agir:

1. confirme o diretório e a raiz Git;
2. leia o AGENTS.md aplicável e a documentação obrigatória do projeto;
3. verifique branch, HEAD, upstream e working tree;
4. confirme o baseline abaixo;
5. preserve alterações preexistentes e pare diante de divergência não explicada.

Baseline esperado:

- branch: [BRANCH];
- commit: [COMMIT];
- versão: [VERSÃO OU NÃO APLICÁVEL];
- schema: [SCHEMA OU NÃO APLICÁVEL];
- testes conhecidos: [TOTAL E NATUREZA OU DESCONHECIDO].

Objetivo único:

[OBJETIVO]

Dentro do escopo:

- [ITEM];

Fora do escopo:

- [ITEM];

Invariantes de segurança e compatibilidade:

- [ITEM];

Validação exigida:

- testes determinísticos: [ITEM];
- testes com mocks: [ITEM];
- validação real: [ITEM];
- itens que podem permanecer não validados: [ITEM].

Documentação:

- atualizar: [ARQUIVOS VIVOS];
- criar: [RELATÓRIO DA ETAPA, SE APLICÁVEL];
- não reescrever relatórios históricos.

Git:

- [COMMIT/PUSH AUTORIZADOS OU PROIBIDOS];
- revisar o diff e excluir dados privados e artefatos de runtime;
- informar o estado final da working tree.

Resposta final:

- resultado principal;
- arquivos alterados;
- validações executadas e resultados;
- validações reais, simuladas, estimadas e pendentes separadas;
- commit e remoto, se autorizados;
- limitações e próximo passo permitido.

Pare ao concluir este objetivo. Não inicie a próxima etapa.
```

## Depois da tarefa

O coordenador deve:

1. ler o resultado e as evidências;
2. confirmar o estado do repositório quando necessário;
3. aprovar, bloquear ou pedir complemento na mesma tarefa;
4. não liberar a próxima etapa enquanto houver bloqueador;
5. atualizar o registro central somente após a conclusão ser verificada.

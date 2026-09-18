---
name: implementation-prompt-builder
description: Crie um prompt completo para uma única etapa, com projeto e baseline confirmados, escopo, exclusões, segurança, validações, documentação, Git, parada e perfil justificado de executor, modelo e esforço. Não inicie a tarefa sem autorização explícita.
---

# Construtor de prompt de implementação

Entregue um prompt pronto para um worker de um executor aprovado e um perfil de execução
recomendado. Criar o prompt não autoriza enviá-lo, editar o projeto, instalar, commitar ou
publicar. Diferencie `executor`, `provedor`, `modelo` e `esforço`; um modelo disponível no
Antigravity não se torna por isso um executor independente.

## Preparação

Confirme projeto, autorização e objetivo único. Use `local-project-orientation` se faltar
baseline. Leia as instruções e documentação viva do alvo e confirme, ou marque como
desconhecidos: raiz, branch, HEAD, upstream, versões, schemas, testes, working tree,
critérios e condição de parada.

Leia [o perfil de execução](references/execution-profile.md) e confirme no executor a
disponibilidade atual. Respeite a escolha explícita de Erick; não faça fallback silencioso.

## Conteúdo obrigatório

Inclua no prompt:

1. projeto e verificação da raiz Git;
2. executor, modelo, esforço e skills realmente disponíveis;
3. instruções e documentos obrigatórios;
4. baseline classificado por evidência;
5. objetivo único e resultado observável;
6. escopo, exclusões e invariantes;
7. segurança, privacidade e compatibilidade;
8. testes determinísticos, mocks e validações reais separados;
9. documentação e roadmap a atualizar quando a escrita estiver autorizada;
10. regras de Git, instalações, downloads, rede e artefatos proibidos;
11. envelope de autonomia, limites, tentativas, promoções e intervenção humana;
12. interação por API, terminal e arquivos; controle visual proibido por padrão;
13. formato da resposta e condição de parada.

Use uma etapa e um projeto por prompt, um escritor por checkout e preserve mudanças
preexistentes. Reserve credenciais, custo material, ações destrutivas, commit, push, merge
e publicação salvo autorização nominal. Não invente skills, ferramentas ou resultados.

## Saída

Apresente perfil recomendado, justificativa, alternativa econômica, gatilho de escalada,
premissas e o prompt pronto. Declare que nenhuma tarefa foi iniciada quando não houver
autorização para delegar.

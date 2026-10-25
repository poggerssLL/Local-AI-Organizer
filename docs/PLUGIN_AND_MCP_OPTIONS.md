# Plugins e MCP no portfólio

Verificado em 2026-10-06 com CLI local e documentação oficial.

## Capacidades e estado

Orca registra servidores MCP em Settings → Integrations → MCP para agentes
compatíveis e descobre skills nos diretórios dos executores. Não foi confirmado
um marketplace próprio de plugins genéricos do Orca. O plugin pertence ao executor:
Antigravity suporta `agy plugin install`, `list`, `validate`, `enable` e `disable`.
`agy plugin list` retornou `No imported plugins.` nesta inspeção.
A presença de plugins/skills na sessão Codex não implica disponibilidade no Gemini.

Uma skill fornece procedimentos e critérios. Um servidor MCP fornece ferramentas.
Um plugin pode empacotar skills, servidores MCP, agentes, regras e hooks;
a compatibilidade e as permissões devem ser verificadas por executor.
Esses recursos não substituem teste, revisão independente ou isolamento de dados.

## Seleção inicial proposta

Para os projetos atuais, aproveitar primeiro terminal, Git e testes já disponíveis.
Quando houver necessidade concreta de nova integração, priorizar no máximo:

1. Consulta de documentação técnica versionada, para reduzir API desatualizada.
2. Automação de testes de navegador, para fluxos reais da interface do Transcriber.
3. Leitura de issues/PRs do GitHub, se o fluxo pedir dados que o Git local não fornece.

Esses são critérios de seleção, não nomes de pacotes instalados ou homologados.
O navegador do Orca já oferece inspeção/automação; avaliar a lacuna antes de instalar
outro servidor. Para Uso Geral, ativar apenas a capacidade ligada ao pedido atual,
sem importar o contexto obrigatório do portfólio para perguntas cotidianas.

## Instalação posterior

Confirmar origem, versão, componentes, compatibilidade Windows/executor e os acessos
necessários. Instalar no workspace quando o executor suportar esse escopo, testar
com fixture própria e conferir ferramentas efetivamente carregadas. Serviços com
login, custos ou credenciais precisam de autorização específica. Não ativar hooks
ou regras globais implicitamente. Nenhum plugin foi instalado nesta tarefa.

Fontes oficiais:
- [Orca: skills e MCP](https://www.onorca.dev/docs/cli/skills)
- [Antigravity: plugins](https://www.antigravity.google/docs/plugins/)
- [Antigravity: permissões](https://www.antigravity.google/docs/permissions?tab=cli)

# Notas Técnicas para o Erick: O Ecossistema de MCPs, Coordenação Multi-Agente e Economia de Tokens

Erick, preparei este documento como um **caderno de campo direto de mim para você**. A ideia aqui é abrir a "caixa-preta" de como funcionam as ferramentas modernas de agentes de IA (Codex, Antigravity, Claude Code, Orca), quais servidores MCP e ferramentas de coordenação realmente valem a pena no GitHub hoje, e como combinar tudo isso sem estourar sua cota de tokens.

---

## 1. A Grande Lição sobre Agentes: Por que "Mais Agentes" nem sempre é "Melhor"?

Quando começamos a mexer com agentes, a primeira intuição é montar uma "fábrica de agentes": um Gerente Central que conversa com um Arquiteto, que passa para um Programador, que passa para um Testador, que passa para um Auditor.

Na prática, a indústria descobriu dois gargalos graves nesse modelo:
1. **O Imposto do Contexto Multiplicado (Cached Input):** Cada agente que entra na conversa precisa ler as regras do projeto, entender o código e trocar mensagens. Se 4 agentes conversam por 10 turnos, você paga 40 envios de contexto.
2. **Perda de Precisão no "Telefone Sem Fio":** Quando um agente resume o problema para outro agente em outro repositório, detalhes sutis do código se perdem.

### Como os engenheiros mais experientes organizam agentes hoje?
Eles usam o padrão **"Especialista Local + Revisão sob Demanda"**:
- **1 Projeto = 1 Cérebro Local:** O agente roda **dentro da própria pasta do projeto**. Ele tem acesso direto ao código, aos testes e às ferramentas daquele projeto.
- **Paralelismo Cirúrgico (Fan-Out / Fan-In):** Você só abre 2 ou 3 agentes ao mesmo tempo quando as tarefas são **100% independentes** ou quando quer uma **auditoria cega** (ex.: o Codex acabou de implementar uma feature complexa no `Local Transcriber`, e você chama o Antigravity/Argon ou o Claude Opus em modo *read-only* apenas para procurar falhas de segurança no `git diff`).
- **O Papel do "Organizer" (`teste_codex`):** Ele deixa de ser um "chefe que microgerencia tarefas diárias" e passa a ser um **Radar de Arquitetura Entre Projetos** — usado apenas quando você quer comparar soluções entre dois projetos seus ou desenhar a ponte (API/contrato) entre eles.

---

## 2. O Mapa dos Melhores Servidores MCP (Para Economizar Tokens e Dar Superpoderes ao Codex)

O **MCP (*Model Context Protocol*)** transforma programas locais em ferramentas nativas para o Codex e o Antigravity. Mas lembre-se da regra de ouro: **instale por projeto (`.codex/config.toml`) apenas o que aquele projeto precisa**.

Aqui estão os MCPs que realmente fazem diferença para o seu estilo de projetos:

### A. Os "Economizadores de Tokens" (Navegação de Código e Arquivos)

1. **Filesystem MCP Oficial (`@modelcontextprotocol/server-filesystem`)**
   - **O que faz:** Dá ao Codex a ferramenta nativa `read_multiple_files`, `list_directory` e `edit_file`.
   - **Por que usar:** Impede que o Codex abra 6 janelas de PowerShell seguidas dando `Get-Content` um por um. Ele lê todos os arquivos necessários em **1 única chamada**.
   - **Como ativar só no projeto atual:**
     ```toml
     [mcp_servers.filesystem]
     command = "npx"
     args = ["-y", "@modelcontextprotocol/server-filesystem", "."]
     ```

2. **Serena MCP (`github.com/oraios/serena`)**
   - **O que faz:** Conecta um *Language Server (LSP)* (de Python, TypeScript, Rust, C#, etc.) ao agente via MCP.
   - **Por que economiza muitos tokens:** Em projetos grandes, quando o Codex quer saber como uma função funciona, sem o Serena ele dá `Get-Content` num arquivo `.py` de 800 linhas inteiro. Com o Serena, ele usa `find_symbol` e lê **apenas as 20 linhas daquela função específica**, além de saber exatamente quem chama aquela função no projeto inteiro (`find_referencing_symbols`).
   - **Compatibilidade com o seu Graphify:** O **Graphify** te dá o mapa macro da arquitetura (`graph.json`), e o **Serena** dá o bisturi cirúrgico para ler só a função exata.

3. **Repomix MCP (`github.com/yamadashy/repomix`)**
   - **O que faz:** Empacota e comprime a estrutura de um repositório (ou subpasta) removendo comentários, espaços e arquivos inúteis, ou extraindo apenas as assinaturas das funções (usando Tree-sitter).
   - **Quando usar:** Excelente quando você quer que um agente entenda um módulo inteiro de uma vez só gastando 70% menos tokens.

---

### B. Os "Anti-Alucinação" (Documentação e Pesquisa)

4. **Context7 MCP (`github.com/upstash/context7`)**
   - **O que faz:** Busca em tempo real a documentação oficial atualizada da versão exata da biblioteca que você está usando (FastAPI, Tailwind v4, daisyUI v5, PyTorch, Faster-Whisper, etc.).
   - **Por que economiza tokens e tempo:** Evita que a IA invente parâmetros que mudaram de versão (o que faz o código falhar no teste e força a IA a gastar 5 turnos tentando consertar o erro).

---

### C. Os "Especialistas de Projeto" (Usar SOMENTE no `.codex/config.toml` do projeto específico)

5. **SQLite / Postgres MCP (`@modelcontextprotocol/server-sqlite` / `server-postgres`)**
   - **Quando usar:** Apenas em projetos que têm banco de dados local (como a fila SQLite do `Local Transcriber` ou `Local File Agent`). O agente inspeciona tabelas e schemas direto sem precisar escrever scripts Python temporários para consultar o banco.
6. **Playwright MCP (`@playwright/mcp` da Microsoft)**
   - **Quando usar:** **Somente** em projetos com interface web quando você estiver testando a tela. Ele permite ao agente abrir o navegador em modo headless, clicar nos botões, ler erros do Console (F12) e validar se o layout funciona. *(Atenção: desligue quando não estiver mexendo em frontend, pois ele adiciona ~20 ferramentas ao prompt).*

---

## 3. Ferramentas e Arquiteturas para Coordenação Entre Agentes

Além do **Orca** que você já usa, vale conhecer como funcionam as principais ferramentas e padrões que existem hoje para colocar múltiplos agentes trabalhando juntos:

### 1. Orca Orchestration + Git Worktrees (O que você já tem na mão!)
- O **Orca** já resolve a parte mais difícil no Windows: criar sessões isoladas de terminais (Codex, Antigravity, Claude Code), gerenciar *Git Worktrees* (para que dois agentes não sobrescrevam o mesmo arquivo ao mesmo tempo) e passar mensagens estruturadas (`Task`, `Dispatch`, `check`, `reply`, `worker_done`).
- **Como usar o Orca sem falir seus tokens:**
  - Não use o Orca para tarefas pequenas que 1 único agente resolve em 2 minutos.
  - Use o Orca quando quiser **Isolamento de Papel**: por exemplo, você está na sessão principal implementando e dispara 1 worker Antigravity (Gemini Flash ou Argon) em background apenas para rodar uma auditoria ou escrever testes enquanto você continua trabalhando.

### 2. Subagentes Nativos do Antigravity (`invoke_subagent`)
- Quando você está usando o **Antigravity**, ele já possui um sistema interno de subagentes (`research`, `self`, ou subagentes customizados criados com `define_subagent`).
- **A grande vantagem:** Quando o Antigravity delega uma pesquisa pesada para um subagente `research`, esse subagente abre uma **janela de contexto separada e descartável**, lê 20 arquivos lá dentro, resume a resposta em 15 linhas e devolve **só o resumo** para a sua conversa principal!
- Isso significa que a sua conversa principal **não fica poluída** com os 20 arquivos lidos pelo subagente — o seu *Cached Input* principal continua pequenininho.

### 3. Padrão "Git Worktree + Handoff via Arquivo Markdown Curto" (Zero Custo de IPC)
- Um segredo muito usado por desenvolvedores que combinam **Codex + Antigravity/Claude** sem gastar tokens com loops de `check --wait`:
  1. Você pede para o **Agente A (ex.: Antigravity)** analisar o problema e gravar um plano técnico enxuto de 30 linhas em `docs/CURRENT_TASK.md`.
  2. Você vai na aba do **Agente B (ex.: Codex)** no mesmo projeto e diz apenas: *"Implemente e valide o `docs/CURRENT_TASK.md`."*
  - **Custo de comunicação entre os dois agentes:** **Zero turnos de espera!** Nenhum agente fica em loop rodando `check --wait` no terminal, e o contexto passado de um para o outro tem apenas 30 linhas limpas.

### 4. Outros Frameworks do Mercado (Para Quando Você Criar Seus Próprios Agentes em Python)
Se no futuro (por exemplo, dentro do seu projeto **Jarvis** ou **Casa**) você quiser programar agentes em Python que conversam entre si no seu código:
- **PydanticAI / LangGraph:** Os melhores frameworks em Python hoje para criar fluxos onde o resultado de um modelo local (ex.: `qwen2.5` no Ollama fazendo triagem rápida) é validado com tipagem forte e só chama um modelo maior quando necessário.
- **Protocolo A2A (Agent-to-Agent, criado pelo Google):** Enquanto o **MCP** serve para um agente usar *ferramentas*, o **A2A** é o padrão aberto para *um agente conversar com outro agente* como se fossem microsserviços independentes.

---

## 4. Onde Pesquisar Novos MCPs com Segurança (Marketplaces)

Sempre que quiser descobrir se existe um MCP pronto para alguma tecnologia nova:
1. **[Glama (`glama.ai/mcp/servers`)](https://glama.ai/mcp/servers)** — Mostra exatamente quantas *Tools* o servidor tem (prefira sempre servidores com menos de 10–12 tools para manter o prompt leve).
2. **[Smithery (`smithery.ai`)](https://smithery.ai/)** — Catálogo rápido com os comandos de instalação prontos.
3. **[GitHub Oficial (`github.com/modelcontextprotocol/servers`)](https://github.com/modelcontextprotocol/servers)** — Os servidores oficiais mantidos pelos criadores do protocolo.

---

## Resumo Final de Ouro para o seu Dia a Dia

1. **Para codar em um projeto:** Abra o agente **direto na pasta daquele projeto**, com `AGENTS.md` curto, `.rgignore` ativo e sessão nova a cada etapa.
2. **Para economizar tokens no Codex:** Deixe o MCP `filesystem` local no `.codex/config.toml` do projeto (para ele usar `read_multiple_files` em vez de vários `Get-Content`) e mantenha a regra de encadear comandos no PowerShell.
3. **Para cruzar ideias entre vários projetos:** Use este repositório (`Local AI Organizer`) como o seu laboratório estratégico para comparar soluções e padronizar o que deu certo!

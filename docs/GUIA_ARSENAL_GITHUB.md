# Arsenal Pessoal de IA, MCPs, Skills e Arquitetura (GitHub Toolbox)

Este arquivo é o **Catálogo Central do Erick** para guardar ferramentas, servidores MCP, skills e padrões de arquitetura descobertos no GitHub.
*(Por começar com `GUIA_`, este arquivo é ignorado nas leituras automáticas dos agentes, custando **zero tokens** no dia a dia — ele só é lido quando você pedir).*

---

## Como usar este Arsenal com a IA

- **Para adicionar algo novo que você achou no GitHub:**
  > *"Adicione o repositório `<link-ou-nome>` na seção X do meu `docs/GUIA_ARSENAL_GITHUB.md` explicando para que serve e como instalar."*
- **Quando estiver começando ou melhorando um projeto:**
  > *"Leia o meu `docs/GUIA_ARSENAL_GITHUB.md` e me recomende quais MCPs, Skills e padrões de lá devo ativar neste projeto."*

---

## 1. Servidores MCP (Model Context Protocol)

> **Regra de ouro:** Ative no arquivo `.codex/config.toml` **dentro da pasta do projeto específico** para não carregar ferramentas desnecessárias em outros projetos.

| Nome | Repositório / Origem | Para que serve? | Peso no Cache | Quando usar? | Trecho para `.codex/config.toml` do Projeto |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Filesystem MCP** | [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) | Dá ao Codex a ferramenta nativa `read_multiple_files` (para de abrir PowerShell dando `Get-Content` um por um). | 🟢 Leve (~8 tools) | **Em todo projeto onde usar Codex** | `command = "npx"`<br>`args = ["-y", "@modelcontextprotocol/server-filesystem", "."]` |
| **Serena MCP** | [`oraios/serena`](https://github.com/oraios/serena) | Busca simbólica via LSP (`find_symbol`, `find_referencing_symbols`). Lê só a função exata (20 linhas) em vez de arquivos de 800 linhas. | 🟢 Leve/Médio | Projetos de código médios/grandes (Python, TS, etc.) | `command = "uvx"`<br>`args = ["--from", "git+https://github.com/oraios/serena", "serena-mcp-server"]` |
| **Context7 MCP** | [`upstash/context7`](https://github.com/upstash/context7) | Injeta a documentação oficial atualizada das bibliotecas (FastAPI, Tailwind, daisyUI, PyTorch) evitando alucinação de API antiga. | 🟢 Leve (2 tools) | Quando for mexer com bibliotecas externas/atualizadas | `command = "npx"`<br>`args = ["-y", "@upstash/context7-mcp"]` |
| **Repomix MCP** | [`yamadashy/repomix`](https://github.com/yamadashy/repomix) | Empacota e comprime um repositório ou módulo extraindo só assinaturas de código (Tree-sitter) para economizar ~70% de tokens. | 🟢 Leve | Revisão arquitetural ou onboarding em projeto novo | `command = "npx"`<br>`args = ["-y", "repomix", "--mcp"]` |
| **SQLite MCP** | [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) | Permite consultar schemas e tabelas SQLite direto sem precisar criar scripts Python temporários. | 🟢 Leve | Projetos com fila/banco local (`Transcriber`, `File Agent`) | `command = "uvx"`<br>`args = ["mcp-server-sqlite", "--db-path", "./caminho/banco.db"]` |
| **Playwright MCP** | [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp) | Abre navegador real/headless, clica na UI, tira print e lê erros do Console (F12). | 🔴 Pesado (~20 tools) | **Somente** durante etapas de criação/teste de Frontend | `command = "npx"`<br>`args = ["-y", "@playwright/mcp@latest"]` |

---

## 2. Catálogo de Skills (`.agents/skills/`)

> **Como instalar uma skill do GitHub em um projeto:** `npx skills add <dono>/<repo>` ou copiando a pasta desejada de `.agents/skills/` deste repositório para o projeto alvo.

### A. Skills de Governança, Arquitetura e Documentação
| Nome da Skill | Origem / Localização | O que faz? | Em quais projetos colocar? |
| :--- | :--- | :--- | :--- |
| **`graphify`** | Global (`~/.gemini/config/skills/graphify`) | Mapeia o código em um grafo de conhecimento (`graphify-out/graph.json`) para achar relações entre arquivos sem ler o repositório inteiro. | Global (todos os projetos de código) |
| **`project-doc-architect`** | Global (`~/.gemini/config/skills/project-doc-architect`) | Cria e atualiza a documentação enxuta de projetos (`AGENTS.md`, `ROADMAP.md`, `ARCHITECTURE.md`) com guardrails contra gasto de tokens. | Global (ao criar ou reestruturar projetos) |
| **`local-integration-architect`** | Local (`.agents/skills/local-integration-architect`) | Desenha contratos seguros de integração (APIs, filas, permissões, falhas) entre dois projetos ou agentes locais. | No `Organizer` ou quando 2 projetos forem se comunicar |
| **`phase-gate-reviewer`** | Local (`.agents/skills/phase-gate-reviewer`) | Revisa se uma etapa cumpriu todos os critérios de aceite, testes e segurança antes de avançar no Roadmap. | Projetos com entregas divididas em fases/etapas |
| **`local-ai-release-review`** | Local (`.agents/skills/local-ai-release-review`) | Checklist final de segurança, dados privados, `git diff --check` e testes antes de permitir `git commit` ou `push`. | Todos os projetos versionados no Git |

### B. Skills de Interface (UI), Design e Visualização de Dados
*(Atenção: copie para `.agents/skills/` **apenas** nos projetos que tiverem tela/dashboard!)*
| Nome da Skill | Origem no GitHub / Local | O que faz? | Comando de Instalação / Origem |
| :--- | :--- | :--- | :--- |
| **`daisyui`** | [`saadeghi/daisyui`](https://github.com/saadeghi/daisyui) | Guia oficial de componentes Tailwind CSS v4 + daisyUI v5 para criar interfaces limpas e padronizadas. | `npx skills add saadeghi/daisyui` |
| **`impeccable`** | [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable) | Sistema completo de crítica de UX, hierarquia visual, tipografia, animações, dark mode e polimento de interfaces web/mobile. | `npx skills add pbakaus/impeccable` |
| **Pacote AntV (`antv-g2-chart`, `antv-g6-graph`, `antv-x6-editor`, `antv-infographic`, `antv-t8-ntv`, `gpt-vis`)** | Local (`.agents/skills/antv-*`) | Criação de gráficos estatísticos (G2), grafos/redes (G6), editores de fluxogramas/DAG (X6), infográficos e relatórios narrativos. | Copiar de `.agents/skills/` apenas quando o projeto tiver dashboards/gráficos |
| **`icon-retrieval`** | Local (`.agents/skills/icon-retrieval`) | Busca ícones e baixa o código SVG limpo via API HTTP com `curl`. | Projetos Frontend / Web |

---

## 3. Conceitos e Padrões de Ouro (Descobertos na Prática)

| Conceito / Padrão | Qual problema resolve? | Como aplicar na prática? |
| :--- | :--- | :--- |
| **1. "1 Cérebro Local por Projeto" (Seccionalização)** | Evita que um repositório central tenha que ler o portfólio inteiro + gastar tokens de IPC para delegar tarefas simples de outro projeto. | Abrir o Codex/Antigravity **direto na pasta do projeto alvo** (`Local Transcriber`, `Local File Agent`), mantendo o `Organizer` apenas para decisões entre projetos. |
| **2. Batching no PowerShell (Anti-Cached Input)** | No Codex CLI, cada comando separado no terminal reenvia 100% do histórico da conversa (gerando 97% de gasto em *Cached Input*). | Ler múltiplos arquivos em 1 único comando (`Get-Content -Raw -Path 'a','b','c'`), filtrar `orca status --json` e encadear `pytest && ruff && git diff --check` na mesma linha. |
| **3. Handoff via Arquivo Curto (`docs/CURRENT_TASK.md`)** | Permite usar 2 agentes diferentes (ex.: Antigravity planeja, Codex implementa) **sem gastar 1 único token com loop de `check --wait`**. | O Agente 1 escreve o plano exato de 30 linhas em `docs/CURRENT_TASK.md`. Você abre o Agente 2 e manda: *"Implemente `docs/CURRENT_TASK.md`"*. |
| **4. Subagente Descartável (`research` no Antigravity)** | Quando o agente principal lê 20 arquivos para pesquisar algo, esses 20 arquivos ficam presos no cache até o fim da conversa. | No Antigravity, delegar pesquisas grandes para o subagente `research`: ele lê os 20 arquivos em uma janela separada e devolve só um resumo de 15 linhas para a conversa principal. |
| **5. Dupla "Graphify + Serena"** | Evita que a IA navegue às cegas lendo dezenas de arquivos `.py` inteiros. | O **Graphify** mostra o mapa de quem se conecta com quem (`graph.json`), e o **Serena MCP** lê apenas as linhas da função específica via LSP. |
| **6. Reset de Sessão por Etapa** | Uma conversa longa de 2 horas acumula >100k tokens; cada clique novo passa a custar 100k tokens de cache. | Concluiu e testou uma etapa do Roadmap? Feche o chat (ou use `/compact`) e comece a próxima etapa em um chat zerado. |

---

## 4. Frameworks e Repositórios no Radar (Para `Jarvis`, `Casa` e Novos Projetos)

| Ferramenta / Repo | Link / Ecossistema | Por que vale a pena guardar? |
| :--- | :--- | :--- |
| **PydanticAI** | [`pydantic/pydantic-ai`](https://github.com/pydantic/pydantic-ai) | Framework Python leve e tipado para criar seus próprios agentes locais (ex.: no `Jarvis`) usando Ollama/OpenRouter com validação garantida de JSON. |
| **LangGraph** | [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph) | Criação de fluxos de agentes em grafo com estado persistente (ótimo quando um fluxo em Python precisa pausar, pedir aprovação humana e continuar). |
| **Protocolo A2A (Agent2Agent)** | [`google/A2A`](https://github.com/google/A2A) | Padrão aberto para fazer agentes independentes (ex.: seu agente `Casa` e seu agente `Jarvis`) conversarem via HTTP/JSON-RPC padronizado. |
| **Glama MCP Directory** | [glama.ai/mcp/servers](https://glama.ai/mcp/servers) | Melhor catálogo para inspecionar quantas *Tools* um servidor MCP tem antes de instalar. |
| **Smithery Marketplace** | [smithery.ai](https://smithery.ai/) | Maior diretório rápido para achar servidores MCP novos da comunidade. |

---

## 5. Caixa de Entrada de Novos Achados do Erick (Para explorar depois)

*(Sempre que achar um link interessante no GitHub, YouTube ou X/Twitter, peça para o agente colar aqui com 1 linha dizendo o que é!)*

- [ ] *Espaço reservado para os próximos repositórios favoritos...*

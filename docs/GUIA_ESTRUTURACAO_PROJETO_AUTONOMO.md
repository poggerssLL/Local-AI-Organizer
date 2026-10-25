# Guia e Blueprint: Como Estruturar um Projeto Autônomo (Economia de Tokens + Qualidade)

Este documento é o **molde padrão (blueprint)** para iniciar ou organizar qualquer projeto individual (como `Local Transcriber`, `Local File Agent`, `Jarvis`, etc.) operando com **cérebro próprio local**, sem depender de um repositório intermediário para tarefas do dia a dia e sem drenar tokens com *Cached Input*.

---

## 1. Filosofia: "1 Cérebro Local por Projeto"

Em vez de usar um repositório central para delegar tarefas cotidianas (o que duplica a leitura de arquivos e gera dezenas de turnos de IPC), cada projeto deve ser **autossuficiente**:

1. **Isolamento de Contexto:** O agente aberto na pasta do projeto só enxerga as regras, o código, os testes e as skills daquele projeto.
2. **Menos Viagens à API (Round-Trips):** Como o *Cached Input* é cobrado a cada chamada de ferramenta (`contexto acumulado × número de passos`), o segredo para gastar 5x a 10x menos tokens no Codex é **agrupar leituras e validações em um único comando** e manter sessões curtas (1 conversa por entrega/etapa).
3. **Quando usar múltiplos agentes no mesmo projeto?**
   - **Tarefas rotineiras (80% dos casos):** 1 único agente (ex.: Codex ou Antigravity) lê, implementa e roda a suíte de testes local.
   - **Tarefas críticas de arquitetura ou segurança (20% dos casos):** 1 agente escritor no checkout principal + 1 agente revisor em modo *read-only* (ou worktree separado) apenas no momento do **Gate da Etapa**.

---

## 2. Estrutura Mínima de Arquivos de Governança em Cada Projeto

Não crie dezenas de arquivos `.md` na raiz ou em `docs/`. Cada projeto precisa de **apenas 2 a 3 arquivos vivos** para orientar a IA:

```text
meu-projeto/
├── AGENTS.md                 # Regras operacionais curtas (máx. 40–60 linhas)
├── .rgignore                 # Pastas que o agente NUNCA deve varrer à toa
├── .codex/
│   └── config.toml           # MCPs exclusivos deste projeto (apontando para ".")
├── .agents/
│   └── skills/               # SOMENTE as skills que este projeto realmente usa
└── docs/
    ├── ROADMAP.md            # Etapas, estado atual e critérios de aceite (enxuto)
    ├── ARCHITECTURE.md       # (Opcional) Contratos, limites de segurança e módulos
    └── archive/              # Relatórios de fases passadas (ignorados pelo agente)
```

---

## 3. Template Pronto de `AGENTS.md` (Copie e Adapte para Cada Projeto)

O `AGENTS.md` é lido em **todos os turnos**. Se ele tiver 300 linhas, você pagará 300 linhas em toda chamada de ferramenta. Mantenha-o entre **35 e 55 linhas**:

```markdown
# <Nome do Projeto> — Instruções Operacionais

## 1. Economia de Contexto e Cached Input (Obrigatório)
- **Confirmar estado inicial em 1 único comando:** Ao iniciar, valide `git status -sb`, branch e `HEAD` agrupados na mesma linha de terminal.
- **Proibido `Get-Content` sequencial:** Quando precisar ler múltiplos arquivos, leia todos em **1 único turno** (`Get-Content -Raw -Path 'arq1','arq2','arq3'` ou via ferramenta MCP `read_multiple_files`).
- **Não ler histórico morto:** Ignore `docs/archive/`, `.venv/`, `node_modules/`, `output/`, `data/` e artefatos brutos (`graphify-out/graph.html`). Se `graphify-out/graph.json` existir, consulte o grafo primeiro para localizar símbolos antes de abrir arquivos grandes.
- **Saídas curtas no terminal:** Nunca despeje JSONs gigantes ou logs inteiros sem filtro no terminal; filtre sempre os campos essenciais.

## 2. Escopo, Autoridade e Segurança
- **Análise, diagnóstico e revisão** são estritamente somente leitura.
- **Implementação** exige pedido explícito de Erick e fica restrita aos arquivos da etapa atual do `docs/ROADMAP.md`.
- **Um único escritor por checkout:** Revisores paralelos operam em modo somente leitura ou em `git worktree` isolado.
- **Proibições:** Não faça commit, push, merge, instalação global, exposição de rede fora de `127.0.0.1` ou uso de credenciais/serviços pagos sem autorização explícita. Preserve alterações preexistentes não relacionadas.

## 3. Gate de Qualidade (Validação antes de concluir)
Após qualquer alteração de código, execute em **1 único comando encadeado**:
1. Testes unitários/integração do escopo alterado (`pytest -q` / `npm test`).
2. Linter, formatação e checagem de tipos (`ruff check . && ruff format --check .`).
3. Higiene do Git (`git diff --check`).

## 4. Comunicação
- Responda sempre em português e comece toda mensagem visível com `Erick,`.
- Separe claramente: fatos validados agora, testes com mocks, validação real e pendências.
```

---

## 4. Como Estruturar o `docs/ROADMAP.md` e os Gates de Teste

Um bom `ROADMAP.md` evita que a IA se perca ou tente programar o projeto inteiro de uma vez. Siga estas precauções:

1. **Fatie em Etapas Pequenas e Testáveis (ex.: Etapa 1A, 1B, 2A):**
   - Cada etapa deve tocar em **no máximo 3 a 5 arquivos** e poder ser concluída em **uma única sessão de chat**.
2. **Defina o "Gate de Saída" de cada etapa em 3 linhas:**
   - **Escopo:** Quais arquivos serão criados/editados.
   - **Invariante de Segurança:** O que não pode quebrar (ex.: *"API continua restrita a loopback 127.0.0.1; sem chamadas externas"*).
   - **Critério de Aceite (Gate):** Qual comando exato de teste prova que a etapa funcionou (ex.: `pytest tests/test_queue.py -q`).
3. **Regra do Expurgo Histórico (`docs/archive/`):**
   - Quando a Etapa 1, 2 e 3 já estiverem concluídas e estáveis, **não deixe 200 linhas de relatórios antigos dentro do `ROADMAP.md`**.
   - Mova os detalhes antigos para `docs/archive/HISTORICO_ETAPAS_1_A_3.md` e deixe no `ROADMAP.md` apenas 1 linha resumida:
     - `✅ Etapas 1 a 3 concluídas (ver docs/archive/HISTORICO_ETAPAS_1_A_3.md).`
   - Isso mantém o `ROADMAP.md` sempre leve (~50 linhas).

---

## 5. Checklist de Precauções Anti-Dreno de Tokens

Antes de começar a trabalhar em qualquer projeto, confira estes 5 pontos:

- [ ] **1. `.rgignore` configurado na raiz do projeto:**
  Coloque no `.rgignore` tudo o que a IA não deve pesquisar:
  ```text
  docs/archive/
  graphify-out/
  output/
  data/
  models/
  *.min.js
  *.lock
  ```
- [ ] **2. Apenas as Skills necessárias em `.agents/skills/`:**
  - Se o projeto **não tem interface web**, não coloque skills de UI (`daisyui`, `impeccable`, `antv-*`) dentro dele.
  - Cada skill presente em `.agents/skills/` injeta sua descrição no prompt de sistema em **100% dos turnos**.
- [ ] **3. MCP Local (`.codex/config.toml`) apontando apenas para `"."`:**
  ```toml
  [mcp_servers.filesystem]
  command = "npx"
  args = ["-y", "@modelcontextprotocol/server-filesystem", "."]
  ```
- [ ] **4. Sessão Nova a Cada Etapa (Resetar o Cached Input):**
  - Terminou a Etapa 8J? **Feche a conversa (ou use `/compact` / `/archive`) e abra uma sessão limpa para a Etapa 8K.**
  - Nunca mantenha uma mesma conversa aberta por horas acumulando 150k tokens de histórico, pois cada comando de terminal subsequente reenviará esses 150k tokens.
- [ ] **5. Orquestração Multi-Agente apenas quando o risco justificar:**
  - Se precisar usar `orca orchestration` para chamar um revisor ou arquiteto em paralelo, aplique sempre o **Standby Híbrido** (no máximo 1 `check --wait` de 5 min e encadeie `reply + ack + wait` na mesma linha).

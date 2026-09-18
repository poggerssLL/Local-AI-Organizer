# Guia de Instalação e Uso do Sistema: Local AI Organizer com Orca ADE

Este guia orienta passo a passo como replicar e utilizar o ecossistema de **Orquestração Híbrida e Delegação Automática** do `Local AI Organizer`, integrando o **Orca ADE** como painel operacional e combinando os ecossistemas **OpenAI (Codex)** e **Google Pro AI (Antigravity)**.

---

## 1. Visão Geral da Arquitetura

O sistema opera com separação estrita entre o **Coordenador Central** (que gerencia arquitetura, regras de governança e prompts) e os **Workers Implementadores** (que executam alterações pontuais de código):

```text
                       Erick / Usuário
                             │
                  Painel Central (Orca ADE)
                 /                        \
      Codex CLI (OpenAI)          Antigravity CLI (Google Pro AI)
     ┌───────────────────┐       ┌──────────────────────────────┐
     │ • GPT-5.6 Terra   │       │ • Gemini 3.8 Flash (Coord.)  │
     │ • GPT-5.6 Sol     │  ◄──► │ • Claude Sonnet 4.6 (Código) │
     │ • GPT-5.6 Luna    │       │ • Claude Opus 4.6 (Arch/Gate)│
     │ • GPT-5.6 Astra   │       │ • GPT-OSS 120B (Auditoria)   │
     └───────────────────┘       └──────────────────────────────┘
                 \                        /
             Repositórios e Worktrees Locais
               (Regra: 1 escritor por checkout)
```

### Pilares Fundamentais:
- **Simetria Bidirecional:** Tanto o Codex quanto o Antigravity atuam como coordenadores e como executores delegados.
- **Sem Fallback Silencioso:** Cada execução declara exatamente seu executor, modelo e esforço. Se indisponível, a execução falha de forma fechada.
- **Isolamento de Runtime:** Conversas e dados temporários residem em diretórios locais ignorados pelo Git (`runtime/`).

---

## 2. Pré-requisitos de Instalação

1. **Git:** Instalado e configurado no terminal (`git --version`).
2. **Orca ADE:** Instalado na máquina (disponível em `https://orca.dev` ou executável local).
3. **OpenAI Codex CLI:**
   ```powershell
   npm install -g @openai/codex-cli
   codex --version
   ```
4. **Google Antigravity CLI (`agy`):**
   - Instalado e autenticado na sua conta Google Pro AI.
   - Verifique os modelos disponíveis no catálogo:
     ```powershell
     agy models
     ```

---

## 3. Passo a Passo de Configuração

### Passo 1: Clonar e Preparar o Repositório
```powershell
git clone https://github.com/seu-usuario/Local-AI-Organizer.git "Local AI"
cd "Local AI"
```

### Passo 2: Instalar as Skills de Governança
O repositório possui 7 skills de coordenação em `.agents/skills/`.

- **Para o Antigravity:** A descoberta é automática, pois as skills estão na pasta padrão de workspace (`.agents/skills/`).
- **Para o Codex:** Instale as skills no catálogo de usuário para que o Codex as reconheça nativamente:
  ```powershell
  # Cria o diretório de skills do Codex se não existir
  New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.codex\skills | Out-Null

  # Copia todas as skills portáteis para o Codex
  Get-ChildItem -Directory .agents\skills | ForEach-Object {
      $dest = Join-Path $env:USERPROFILE\.codex\skills $_.Name
      New-Item -ItemType Directory -Force -Path $dest | Out-Null
      Copy-Item -Path "$($_.FullName)\*" -Destination $dest -Recurse -Force
  }
  ```

### Passo 3: Adicionar o Repositório ao Orca ADE
1. Abra o **Orca ADE**.
2. Clique em **Open Project / Repository** e selecione a pasta do `Local AI Organizer`.

### Passo 4: Registrar os 9 Perfis de Execução no Orca
O arquivo `docs/orca-model-routing-profiles.json` define os 9 perfis suportados:

| Perfil | Executor | Modelo | Esforço | Finalidade Principal |
| :--- | :--- | :--- | :--- | :--- |
| `organizer-codex-luna` | Codex | `gpt-5.6-luna` | `low` | Skeletons, formatação e tarefas mecânicas rápidas |
| `organizer-codex-economy` | Codex | `gpt-5.6-terra` | `medium` | Desenvolvimento balanceado e scripts padrão |
| `organizer-codex-strong` | Codex | `gpt-5.6-sol` | `high` | Subsistemas complexos e depuração de dependências |
| `organizer-codex-astra` | Codex | `gpt-5.6-astra` | `extreme` | **Reserva de emergência** para impasses lógicos insolúveis |
| `organizer-gemini-economy`| Antigravity | `gemini-3.8-flash-medium` | `medium` | Coordenação contínua, documentação e leitura ampla |
| `organizer-gemini-strong` | Antigravity | `gemini-3.8-flash-high` | `high` | Síntese de contexto e relatórios analíticos |
| `organizer-claude-sonnet` | Antigravity | `claude-sonnet-4-6` | `high` | Implementação de código limpo e cobertura de testes |
| `organizer-claude-opus`   | Antigravity | `claude-opus-4-6-thinking`| `high` | Arquitetura de contratos e revisão de release gates |
| `organizer-gpt-oss`       | Antigravity | `gpt-oss-120b-medium` | `medium` | Auditoria independente de código aberto |

Você pode cadastrar esses perfis como **Quick Commands** do terminal no Orca para iniciar abas dedicadas com um único clique.

---

## 4. Como Operar o Sistema no Dia a Dia

### 1. Escolhendo o Modelo Certo (`model-router-advisor`)
Antes de iniciar uma tarefa, chame a skill:
- No chat do Codex ou Antigravity, digite:
  ```text
  /model-router-advisor
  ```
- A skill analisará:
  1. A complexidade do código;
  2. A necessidade de arquitetura vs. implementação;
  3. O estado das cotas semanais (as cotas do Codex renovam na segunda-feira; se estiverem esgotadas, o roteador encaminha para o Claude Sonnet ou Gemini sem travar o desenvolvimento).

### 2. Delegando Tarefas entre Modelos
Ao delegar trabalho para outro projeto ou modelo:
1. O coordenador gera um prompt fechado usando o modelo de `docs/DELEGATION_TEMPLATE.md`.
2. O worker delegado inicia no diretório alvo em modo reversível.
3. Se o worker rodar via Codex no Windows, use `-c windows.sandbox=unelevated` para assegurar estabilidade de execução.

### 3. Inspecionando Conversas com Outros Modelos (`runtime/chat_exchange/`)
Para inspecionar o histórico e o diálogo produzido por outros chats e modelos:
- Abra o diretório local `runtime/chat_exchange/`.
- Cada sessão exporta sua transcrição em `runtime/chat_exchange/<model_id>_exchange.md`.
- Esses arquivos são automaticamente excluídos do versionamento Git para preservar sua privacidade e são sobrescritos a cada novo chat com o respectivo modelo.

### 4. Ciclo de Fechamento de Etapa
1. O worker apresenta o diff e evidências de testes.
2. O coordenador executa a skill `phase-gate-reviewer` e `local-ai-release-review`.
3. Somente após a aprovação expressa do usuário é executado o `git commit`.

---

## 5. Resolução de Problemas Comuns

- **Aviso `os error 183` no Codex CLI:**
  Ocorre no Windows quando o diretório de skills já existe (`ERROR_ALREADY_EXISTS`). É um aviso inofensivo de inicialização e não afeta a execução.
- **Timeout em execução não-interativa do Codex no Windows:**
  Certifique-se de executar com `-c windows.sandbox=unelevated --sandbox read-only`. Feche o pipe de entrada (`echo "" | codex ...`) para evitar que o processo espere por `stdin`.
- **Erro 503 no GPT-OSS:**
  Representa alta demanda temporária no cluster da Google. Utilize o Claude Sonnet ou Gemini Flash como alternativa de fallback imediato.

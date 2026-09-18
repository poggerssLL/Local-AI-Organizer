# Contrato do Pacote de Passagem e Validação Interativa PTY no Orca

Atualizado em: 2026-09-18.
Schema: `orca-handoff/v1`

## 1. Finalidade e Estado

Este documento formaliza o contrato técnico da **Etapa 1 do Marco 17 do Roadmap**:
1. O protocolo determinístico do **Pacote de Passagem (*Handoff Protocol*)** entre executores simétricos (**Codex** e **Antigravity**);
2. O roteiro de validação do **Canário Interativo via Terminal PTY (Pseudo-Terminal)** no Orca ADE, superando o modo *headless* de disparo cego.

- **Estado atual:** **ESPECIFICAÇÃO DE ARQUITETURA CONCLUÍDA (Projetos reais: BLOQUEADOS)**.
- **Precedente:** complementa os contratos `ORCA_PILOT_CONTRACT.md` e `ORCA_MODEL_ROUTING_CONTRACT.md`, atendendo ao Item 17 do `docs/ROADMAP.md`.

---

## 2. O Problema Arquitetural

Nos testes sintéticos anteriores:
- O **Antigravity CLI** comprovou ciclo completo (leitura de sentinelas, cálculo de SHA-256 e escrita reversível).
- O **Codex CLI** superou o travamento de sandbox no Windows (`-c windows.sandbox=unelevated`), mas ao ser disparado em modo *headless* (não-interativo de turno único), encerrou com `ExitCode 0` emitindo apenas texto conversacional, **sem disparar a ferramenta de leitura de arquivos**.
- Além disso, a transferência de trabalho entre Codex e Antigravity não pode depender de suposições ou "memória de chat", exigindo um formato de intercâmbio de dados versionado e auditável.

---

## 3. Especificação do Pacote de Passagem (`orca-handoff/v1`)

O pacote de passagem é o artefato sanitizado emitido por um executor antes de encerrar seu turno, salvo no diretório temporário local não-versionado `runtime/chat_exchange/handoff_payload.json` (ou `.md`).

### Estrutura do Schema (`orca-handoff/v1`)

```json
{
  "$schema": "orca-handoff/v1",
  "handoff_id": "handoff-20260918-001",
  "timestamp": "2026-09-18T13:00:00Z",
  "source": {
    "executor": "antigravity",
    "model": "claude-opus-4-6-thinking",
    "effort": "high"
  },
  "target": {
    "executor": "codex",
    "model": "gpt-5.6-terra",
    "effort": "medium"
  },
  "project": "Local AI Organizer",
  "baseline": {
    "git_root": "<relative-or-resolved-root>",
    "branch": "main",
    "commit": "4d4bd87",
    "working_tree_clean": true
  },
  "completed_work": {
    "summary": "Planejamento arquitetural concluído e contrato validado.",
    "verified_sentinels": ["SENTINEL-PTY-20260918-ORGANIZER"],
    "files_inspected": ["AGENTS.md", "README.md"]
  },
  "files_modified": [],
  "evidence": {
    "tests_passed": [],
    "hashes_sha256": {
      "fixture.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  },
  "pending_work": [
    "Ler o arquivo fixture.txt através de ferramenta de leitura.",
    "Modificar o arquivo inserindo a linha de complemento autorizada.",
    "Verificar a integridade do diff."
  ],
  "handoff_instruction": "Atue no checkout sintético. Leia fixture.txt com a ferramenta de leitura, confirme a sentinela SENTINEL-PTY-20260918-ORGANIZER e aplique a alteração prevista em pending_work. Não altere arquivos fora do escopo.",
  "invariants": {
    "commit_allowed": false,
    "network_allowed": false,
    "single_writer_checkout": true,
    "fallback": "none"
  }
}
```

### Regras de Governança do Pacote:
1. **Sem Segredos:** Não deve conter tokens, chaves de API, credenciais ou identificadores privados de runtime;
2. **Caminhos Relativos:** Todos os arquivos citados em `files_inspected`, `files_modified` e `pending_work` devem ser caminhos relativos à raiz do checkout;
3. **Imutabilidade durante a Troca:** O arquivo `handoff_payload.json` é selado antes da inicialização do agente alvo e verificado pelo orquestrador.

---

## 4. Protocolo do Canário Interativo PTY no Orca

Para comprovar que o **Codex** efetivamente chama ferramentas de leitura e que o **Orca** gerencia a alternância de turnos via terminal ConPTY no Windows:

```text
                                  Orca ADE (ConPTY)
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
[Turno 1: Antigravity]                                           [Turno 2: Codex]
1. Inicia em ConPTY                                              1. Inicia em ConPTY com flag
2. Lê sentinela de AGENTS.md                                        -c windows.sandbox=unelevated
3. Produz handoff_payload.json                                   2. Lê handoff_payload.json
4. Encerra PTY de forma limpa                                    3. Dispara TOOL CALL real de leitura
                                                                 4. Valida a sentinela e aplica diff
                                                                 5. Encerra com código 0
```

### 4.1. Ambiente do Teste Sintético
- Subárvore temporária descartável: `%TEMP%\codex-orca-pilot-20260915\pty-canary`
- Fixtures obrigatórios:
  - `AGENTS.md` contendo a sentinela única: `SENTINEL-PTY-20260918-ORGANIZER`
  - `fixture.txt` com hash inicial SHA-256 conhecido.
  - `task_manifest.json` com os limites operacionais.

### 4.2. Critérios de Aceitação do Gate Interativo PTY

Para aprovação na **Etapa 2**, as seguintes evidências devem ser comprovadas deterministicamente:

1. **Invocação Observável de Ferramentas pelo Codex:**
   - O log do processo Codex CLI deve registrar o evento de despacho de ferramenta (`tool_use: read_file` ou equivalente de inspeção de arquivo), comprovando que o agente não operou como mero papagaio de texto conversacional.
2. **Conexão ConPTY Estável no Windows:**
   - O terminal gerenciado pelo Orca deve sustentar a sessão sem congelar no hook de pré-ferramenta (`hook: PreToolUse`) e sem exigir intervenção humana não autorizada.
3. **Consumo Fiel do Pacote de Passagem:**
   - O Codex deve citar no seu relatório a sentinela `SENTINEL-PTY-20260918-ORGANIZER` e cumprir a tarefa de `pending_work` especificada no JSON de handoff gerado pelo Antigravity.
4. **Isolamento de Processos e Higiene:**
   - Nenhum processo órfão de `node.exe`, `codex.exe`, `agy.exe` ou terminal Orca deve permanecer ativo após a conclusão do teste.
   - O repositório sintético deve ser restaurado ao estado inicial sem resíduos.

---

## 5. Limites e Salvaguardas

- **Projetos Reais:** Continuam estritamente **BLOQUEADOS** para qualquer ação do Orca ou de workers autônomos.
- **Nenhum Bypass:** Flags perigosas (`--dangerously-skip-permissions`, `always-proceed`, `yolo`) continuam terminantemente proibidas.
- **Orçamento de Execução:** O teste sintético da Etapa 2 deve ser delimitado a no máximo 2 turnos por executor com timeout rígido de 90 segundos por processo.

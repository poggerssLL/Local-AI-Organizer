# Pacote de Passagem (Handoff): Local File Agent - Etapas 1 e 2 para o Codex

Atualizado em: 2026-09-18.  
Schema: `orca-handoff/v1`

---

## 1. Identificação da Passagem

- **Handoff ID:** `handoff-local-file-agent-etapas-1-e-2-to-codex`
- **Emissor (Sexta-feira):** Antigravity (Coordenador Técnico)
  - **Diretrizes e Contratos:** Modelagem baseada no comitê de perfis (segurança de Claude Opus, I/O e testes de Claude Sonnet);
  - **OpenRouter / Qwen 2.5 27B Free:** Geração de árvore sintética de testes via chamada externa real de API (`tests/fixtures/synthetic_tree/`);
  - **Execução e Consolidação Local:** Conduzida pelo coordenador com suíte de 10 testes determinísticos;
  - **Nova Governança:** Conforme política atualizada em `docs/ORCHESTRATION_POLICY.md`, etapas subsequentes acionarão ativamente subagentes dedicados (`invoke_subagent` / workers paralelos).
- **Receptor (Segunda-feira):** OpenAI (`gpt-5.6-sol` / `gpt-5.6-terra` via Codex CLI ou IDE)
- **Projeto Alvo:** `Local File Agent` (`C:/Users/erick/OneDrive/Documentos/Local File Agent`)
- **Baseline Git Confirmado:**
  - Branch: `main`
  - Commits:
    - `d7c3ab2`: *feat: etapa 1 - fundacao e politicas de seguranca do Local File Agent*
    - `bcd8cac`: *feat: etapa 2 - inventario somente leitura (DirectoryScanner)*
  - Working Tree: Limpa
  - Testes: 10 de 10 aprovados (`python -m unittest discover tests` em 0.009s)

---

## 2. O que foi Concluído e Validado

### Etapa 1: Fundação e Políticas de Segurança
1. **Governança:**
   - Criado o repositório irmão `Local File Agent` com `AGENTS.md`, `FOUNDATION.md`, `ROADMAP.md` (11 etapas), `DECISIONS.md` (ADR-001 a ADR-003), `PROJECT_STATE.md`, `KNOWN_ISSUES.md` e `.gitignore`.
2. **Modelos Centrais (`src/core/models.py`):**
   - `FileItem`, `OperationType`, `OperationAction` e `ExecutionPlan`;
   - Invariantes de aprovação humana explícita (`approved=True`) e modo dry-run por padrão;
   - Validação de segurança contra escape de diretório (*directory traversal*).
3. **Validação:**
   - 5 testes unitários em `tests/test_foundation.py`.

### Etapa 2: Inventário Somente Leitura
1. **Modelos de Varredura:**
   - `ScannerConfig` com salvaguardas para exclusão padrão de arquivos ocultos (`include_hidden=False`), desativação de symlinks (`follow_symlinks=False`), profundidade máxima (`max_depth`) e limite rígido de segurança (`max_files_limit`);
   - `ScanReport` agregando contagem total, bytes e distribuição de extensões.
2. **Implementação do Scanner (`src/core/scanner.py`):**
   - Classe `DirectoryScanner` usando `os.scandir` de alta performance com tratamento resiliente de erros de permissão (`PermissionError`).
3. **Validação com Fixtures Sintéticos:**
   - Árvore de testes criada em `tests/fixtures/synthetic_tree/` com 6 arquivos simulando tipos reais (`.pdf`, `.docx`, `.png`, `.txt`, `.exe`, `.oculto`);
   - 5 testes unitários em `tests/test_scanner.py` cobrindo comportamento padrão, filtros, profundidade e arquivos ocultos;
   - Totalizando 10 testes unitários sem nenhuma escrita ou alteração física em arquivos reais do usuário.

---

## 3. Missão do Codex na Segunda-Feira

Na segunda-feira, com as cotas semanais renovadas, o **Codex** assumirá o papel de **Auditor Sênior e Organizador**. A missão será:

1. **Auditoria de Fundação (Etapas 1 e 2):**
   - Inspecionar a governança, modelos de dados e o `DirectoryScanner`;
   - Executar a suíte completa de 10 testes para validar o baseline.
2. **Implementação da Etapa 3: Hashes SHA-256 e Detecção de Duplicidades:**
   - Criar módulo `src/core/hasher.py` (ou método no scanner) para cálculo de hash SHA-256 em blocos (*chunks* de 64KB/1MB);
   - Criar detector de arquivos duplicados no `ScanReport` ou módulo de análise;
   - Suíte de testes unitários para cálculo de hash e detecção de duplicatas em fixtures sintéticos;
   - Registro em `docs/PHASE_03_HASHES_AND_DUPLICATES_*.md`.

---

## 4. Prompt de Inicialização para o Codex

Copie e cole este prompt no chat do **Codex** aberto no repositório `Local File Agent`:

```text
Atue como o arquiteto sênior e organizador do projeto Local File Agent (C:/Users/erick/OneDrive/Documentos/Local File Agent).

Antes de qualquer ação:
1. Confirme o diretório e a raiz Git com `git rev-parse --show-toplevel`;
2. Verifique o baseline esperado: branch `main`, commit `bcd8cac`, working tree limpa;
3. Leia o AGENTS.md, FOUNDATION.md, ROADMAP.md e docs/PHASE_02_READONLY_INVENTORY_2026-09-18.md;
4. Execute a suíte de testes existente com `python -m unittest discover tests` e confirme 10 de 10 testes aprovados.

Seu Objetivo:
1. Auditar as Etapas 1 (Fundação e Segurança) e 2 (Inventário Somente Leitura) implementadas pela equipe Antigravity multi-agente;
2. Implementar a Etapa 3 do ROADMAP.md: Cálculo de Hashes SHA-256 em blocos (chunks) e Detecção Determinística de Arquivos Duplicados;
3. Criar a suíte de testes unitários para a Etapa 3 usando arquivos de teste sintéticos (sem tocar em arquivos reais de Erick);
4. Atualizar ROADMAP.md, PROJECT_STATE.md e gerar o relatório da fase.

Regras Invioláveis:
- Nenhuma modificação, deleção ou movimentação de arquivos reais do sistema operacional;
- Modo somente leitura por padrão;
- Mantenha 100% de confinamento ao diretório de testes sintéticos;
- Não execute git push sem aprovação nominal expressa de Erick.
```

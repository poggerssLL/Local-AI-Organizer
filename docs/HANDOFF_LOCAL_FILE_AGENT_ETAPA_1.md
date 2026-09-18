# Pacote de Passagem (Handoff): Local File Agent - Etapa 1

Atualizado em: 2026-09-18.
Schema: `orca-handoff/v1`

## 1. Identificação da Passagem

- **Handoff ID:** `handoff-local-file-agent-etapa-1-to-codex`
- **Emissor (Atual):** Google Pro AI (`claude-opus-4-6-thinking` / `claude-sonnet-4-6` via Antigravity)
- **Receptor (Semana que vem):** OpenAI (`gpt-5.6-sol` / `gpt-5.6-terra` via Codex)
- **Projeto Alvo:** `Local File Agent` (`C:/Users/erick/OneDrive/Documentos/Local File Agent`)
- **Baseline Git Confirmado:**
  - Branch: `main`
  - Commit SHA: `d7c3ab2` (*feat: etapa 1 - fundacao e politicas de seguranca do Local File Agent*)
  - Working Tree: Limpa
  - Testes: 5 de 5 aprovados (`python -m unittest discover tests`)

---

## 2. O que foi Concluído na Etapa 1

1. **Governança e Confinamento:**
   - Criado o repositório irmão isolado `Local File Agent`;
   - Implementado o `AGENTS.md` com as regras de contenção invioláveis: aprovação humana obrigatória para movimentação/exclusão de arquivos, confinamento estrito a subdiretórios autorizados e modo dry-run por padrão;
   - Implementados `FOUNDATION.md`, `ROADMAP.md` (11 etapas), `DECISIONS.md` (ADR-001 a ADR-003), `PROJECT_STATE.md`, `KNOWN_ISSUES.md` e `.gitignore`.
2. **Modelos de Dados Centrais (`src/core/models.py`):**
   - `FileItem`, `OperationType`, `OperationAction` e `ExecutionPlan`;
   - Validador de segurança `validate_safety()` bloqueando tentativas de escape de diretório (`..` ou caminhos absolutos arbitrários);
   - Invariante de aprovação: `can_execute()` recusa execução sem `approved = True`.
3. **Validação:**
   - 5 testes unitários aprovados em `tests/test_foundation.py`.

---

## 3. Instrução para o Codex na Segunda-Feira

Quando Erick iniciar a sessão com o Codex no `Local File Agent`, utilize o seguinte prompt-base:

```text
Atue como o arquiteto sênior e organizador do projeto Local File Agent (C:/Users/erick/OneDrive/Documentos/Local File Agent).

Antes de agir:
1. Confirme o diretório e a raiz Git (commit d7c3ab2);
2. Leia o AGENTS.md, FOUNDATION.md e ROADMAP.md;
3. Execute a suíte de testes (python -m unittest discover tests) e confirme 5/5 testes aprovados.

Seu Objetivo:
Auditar a fundação e as políticas de segurança da Etapa 1 entregues pela equipe Antigravity, emitir seu parecer técnico e estruturar o plano de implementação da Etapa 2 (Inventário Somente Leitura).

Limites:
- Nenhuma operação física de movimentação ou exclusão de arquivos reais em disco;
- Mantenha 100% de confinamento ao diretório do projeto;
- Não execute commit ou push sem autorização nominal de Erick.
```

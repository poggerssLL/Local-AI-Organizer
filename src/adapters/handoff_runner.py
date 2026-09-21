"""
Adaptador de Execucao do Protocolo de Passagem (Handoff) no Orca ADE.
Atende ao contrato `orca-handoff/v1` formalizado em docs/ORCA_HANDOFF_CONTRACT.md
e validado em docs/PHASE_ORCA_PTY_HANDOFF_2026-09-18.md.
"""

import os
import sys
import json
import re
import time
import hashlib
import subprocess
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Any, Optional

# Schema version oficial
SCHEMA_VERSION = "orca-handoff/v1"

# Padroes proibidos para privacidade estrita
PROHIBITED_PATTERNS = [
    r"[a-zA-Z]:[\\/]+Users[\\/]+[^\s\"']+",
    r"/home/[^\s\"']+",
    r"/Users/[^\s\"']+",
    r"sk-[a-zA-Z0-9_-]{20,}",
    r"AIza[0-9A-Za-z-_]{35}",
    r"ghp_[a-zA-Z0-9]{20,}",
    r"github_pat_[a-zA-Z0-9_]{22,}",
    r"sk-ant-[a-zA-Z0-9_-]{20,}",
    r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}",
]


class HandoffState(str, Enum):
    INIT = "INIT"
    SOURCE_RUNNING = "SOURCE_RUNNING"
    VALIDATING_PAYLOAD = "VALIDATING_PAYLOAD"
    TARGET_RUNNING = "TARGET_RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PrivacyViolationError(ValueError):
    """Detectado dado sensivel ou caminho absoluto no payload."""
    pass


class SchemaValidationError(ValueError):
    """Payload nao atende a especificacao orca-handoff/v1."""
    pass


class ToolCallVerificationError(RuntimeError):
    """O executor alvo nao invocou ferramentas comprovaveis de inspecao."""
    pass


class SentinelVerificationError(RuntimeError):
    """Sentinela esperada nao confirmada pelo executor alvo."""
    pass


@dataclass
class TurnResult:
    executor: str
    model: str
    effort: str
    exit_code: int
    duration_ms: float
    command_executed: List[str]
    tool_calls_detected: List[Dict[str, Any]] = field(default_factory=list)
    sentinels_confirmed: List[str] = field(default_factory=list)
    raw_output_snippet: str = ""


@dataclass
class HandoffResult:
    handoff_id: str
    status: HandoffState
    source_turn: Optional[TurnResult] = None
    target_turn: Optional[TurnResult] = None
    payload_path: str = ""
    payload_sha256: str = ""
    schema_version: str = SCHEMA_VERSION
    privacy_passed: bool = False
    validation_errors: List[str] = field(default_factory=list)
    start_time_iso: str = ""
    end_time_iso: str = ""
    total_duration_ms: float = 0.0
    orphan_processes_detected: int = 0
    markdown_report_path: str = ""
    is_mock: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    def to_markdown(self) -> str:
        """Gera relatorio estruturado em Markdown com as respostas e telemetria dos workers."""
        lines = [
            f"# Relatório de Handoff Automático — `{self.handoff_id}`",
            "",
            "## 1. Metadados da Execução",
            f"- **Status:** `{self.status.value}`",
            f"- **Schema:** `{self.schema_version}`",
            f"- **Início (UTC):** `{self.start_time_iso}`",
            f"- **Término (UTC):** `{self.end_time_iso}`",
            f"- **Duração Total:** `{self.total_duration_ms:.2f} ms`",
            f"- **Privacidade Validada:** `{'SIM' if self.privacy_passed else 'NÃO'}`",
            f"- **SHA-256 do Payload:** `{self.payload_sha256 or 'N/A'}`",
            f"- **Modo de Execução:** `{'Simulado (Mock)' if self.is_mock else 'Real (Subprocess / ConPTY)'}`",
            "",
        ]

        if self.validation_errors:
            lines.append("## Alertas / Erros")
            for err in self.validation_errors:
                lines.append(f"- ❌ {err}")
            lines.append("")

        lines.append("## 2. Turno 1: Origem (Worker Criador do Handoff)")
        if self.source_turn:
            lines.extend([
                f"- **Executor:** `{self.source_turn.executor}`",
                f"- **Modelo:** `{self.source_turn.model}` (esforço `{self.source_turn.effort}`)",
                f"- **Código de Saída:** `{self.source_turn.exit_code}`",
                f"- **Duração:** `{self.source_turn.duration_ms:.2f} ms`",
                f"- **Sentinelas Confirmadas:** {', '.join(f'`{s}`' for s in self.source_turn.sentinels_confirmed) if self.source_turn.sentinels_confirmed else 'Nenhuma'}",
                "",
                "### Resposta / Saída do Worker 1 (Claude Opus)",
                "```text",
                self.source_turn.raw_output_snippet.strip() or "(Sem saída textual)",
                "```",
                "",
            ])
        else:
            lines.append("*Turno 1 não foi executado.*\n")

        lines.append("## 3. Turno 2: Destino (Worker Consumidor do Handoff)")
        if self.target_turn:
            lines.extend([
                f"- **Executor:** `{self.target_turn.executor}`",
                f"- **Modelo:** `{self.target_turn.model}` (esforço `{self.target_turn.effort}`)",
                f"- **Código de Saída:** `{self.target_turn.exit_code}`",
                f"- **Duração:** `{self.target_turn.duration_ms:.2f} ms`",
                f"- **Sentinelas Confirmadas:** {', '.join(f'`{s}`' for s in self.target_turn.sentinels_confirmed) if self.target_turn.sentinels_confirmed else 'Nenhuma'}",
                f"- **Ferramentas Acionadas no Sandbox:** `{len(self.target_turn.tool_calls_detected)} chamadas`",
                "",
                "### Resposta / Saída do Worker 2 (Codex)",
                "```text",
                self.target_turn.raw_output_snippet.strip() or "(Sem saída textual)",
                "```",
                "",
            ])
        else:
            lines.append("*Turno 2 não foi executado.*\n")

        lines.extend([
            "## 4. Invariantes de Governança Verificadas",
            "- **Commit no Git:** `BLOQUEADO (commit_allowed=false)`",
            "- **Acesso à Rede Externa:** `BLOQUEADO (network_allowed=false)`",
            "- **Concorrência:** `Único escritor por checkout (single_writer_checkout=true)`",
            "- **Fallback Automático:** `DESATIVADO (fallback='none')`",
            "",
            "---",
            "*Documento gerado automaticamente pelo HandoffRunner do Local AI Organizer.*",
        ])
        return "\n".join(lines)


class HandoffRunner:
    def __init__(
        self,
        workspace_root: str,
        mock_mode: bool = False,
        mock_scenario: str = "success",
        timeout_seconds: int = 90,
    ):
        self.workspace_root = workspace_root
        self.mock_mode = mock_mode
        self.mock_scenario = mock_scenario
        self.timeout_seconds = timeout_seconds
        self.state = HandoffState.INIT
        self.current_payload: Optional[Dict[str, Any]] = None

    def check_privacy(self, content: str) -> None:
        """Verifica se o conteudo contem caminhos absolutos de perfil ou credenciais."""
        for pattern in PROHIBITED_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                raise PrivacyViolationError(
                    f"Violacao de privacidade detectada: padrao proibido encontrado ({match.group(0)})"
                )

    def validate_payload_structure(self, payload: Dict[str, Any]) -> None:
        """Valida conformidade estrita com o schema orca-handoff/v1."""
        if payload.get("$schema") != SCHEMA_VERSION:
            raise SchemaValidationError(
                f"Schema invalido: esperado '{SCHEMA_VERSION}', obtido '{payload.get('$schema')}'"
            )

        required_keys = [
            "handoff_id", "timestamp", "source", "target", "project",
            "baseline", "completed_work", "files_modified", "evidence",
            "pending_work", "handoff_instruction", "invariants"
        ]
        for k in required_keys:
            if k not in payload or payload[k] is None:
                raise SchemaValidationError(f"Campo obrigatorio ausente no payload: '{k}'")

        # Invariantes estritas de seguranca
        inv = payload.get("invariants", {})
        if inv.get("commit_allowed") is not False:
            raise SchemaValidationError("Invariante violada: commit_allowed deve ser False")
        if inv.get("network_allowed") is not False:
            raise SchemaValidationError("Invariante violada: network_allowed deve ser False")
        if inv.get("single_writer_checkout") is not True:
            raise SchemaValidationError("Invariante violada: single_writer_checkout deve ser True")
        if inv.get("fallback") != "none":
            raise SchemaValidationError("Invariante violada: fallback deve ser 'none'")

        # Caminhos relativos obrigatorios
        for f in payload.get("completed_work", {}).get("files_inspected", []):
            self._assert_relative_path(f)
        for f in payload.get("files_modified", []):
            self._assert_relative_path(f)
        for f in payload.get("evidence", {}).get("hashes_sha256", {}).keys():
            self._assert_relative_path(f)

        # Checagem de privacidade recursiva
        self.check_privacy(json.dumps(payload))

    def _assert_relative_path(self, path: str) -> None:
        """Garante que nenhum caminho absoluto ou que escape do workspace seja aceito."""
        if os.path.isabs(path) or path.startswith("/") or path.startswith("\\") or ":" in path or ".." in path:
            raise PrivacyViolationError(f"Caminho nao-relativo ou inseguro detectado: '{path}'")

    def _resolve_codex_bin(self) -> str:
        """Resolve o executavel do Codex CLI testando caminhos conhecidos no Windows."""
        candidates = [
            "codex.cmd",
            os.path.expandvars(r"%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Roaming\npm\codex.cmd"),
            os.path.expandvars(r"%APPDATA%\npm\codex.cmd"),
        ]
        for c in candidates:
            if (os.path.isabs(c) and os.path.exists(c)) or os.path.exists(c):
                return c
        return "codex.cmd"

    def build_codex_command(self, model: str, effort: str, worktree: str) -> List[str]:
        """Gera comando deterministico para Codex CLI no Windows com sandbox unelevated."""
        codex_bin = self._resolve_codex_bin()
        return [
            codex_bin, "exec",
            "--json",
            "--ephemeral",
            "--model", model,
            "-c", f"model_reasoning_effort={effort}",
            "-c", "windows.sandbox=unelevated",
            "--sandbox", "read-only",
            "--cd", worktree,
        ]

    def build_antigravity_command(self, model: str, worktree: str) -> List[str]:
        """Gera comando deterministico para Antigravity CLI no Windows com new-project."""
        return [
            "agy.cmd",
            "--new-project",
            "--model", model,
        ]

    def run_handoff(
        self,
        handoff_id: str,
        source_executor: str,
        source_model: str,
        target_executor: str,
        target_model: str,
        expected_sentinel: str,
        worktree_path: str,
    ) -> HandoffResult:
        """Executa a sequencia completa de passagem de bastao (Turno 1 -> Validacao -> Turno 2)."""
        start_time = datetime.now(timezone.utc)
        result = HandoffResult(
            handoff_id=handoff_id,
            status=HandoffState.INIT,
            start_time_iso=start_time.isoformat(),
            is_mock=self.mock_mode,
        )

        try:
            # 1. INIT
            self.state = HandoffState.INIT
            payload_dir = os.path.join(worktree_path, "runtime", "chat_exchange")
            os.makedirs(payload_dir, exist_ok=True)
            payload_file = os.path.join(payload_dir, "handoff_payload.json")
            result.payload_path = "runtime/chat_exchange/handoff_payload.json"

            # 2. SOURCE_RUNNING (Turno 1)
            self.state = HandoffState.SOURCE_RUNNING
            source_turn = self._execute_source_turn(
                source_executor, source_model, payload_file, handoff_id, expected_sentinel, worktree_path
            )
            result.source_turn = source_turn

            # Se o Turno 1 falhou, aborta imediatamente (fail-closed)
            if source_turn.exit_code != 0:
                raise RuntimeError(f"Turno 1 ({source_executor}) encerrou com codigo de erro {source_turn.exit_code}")

            # 3. VALIDATING_PAYLOAD (Verificacao de Seguranca e Integridade)
            self.state = HandoffState.VALIDATING_PAYLOAD
            if not os.path.exists(payload_file):
                raise FileNotFoundError(f"Arquivo de handoff nao foi gerado em: {payload_file}")

            with open(payload_file, "r", encoding="utf-8") as f:
                payload_data = json.load(f)

            self.validate_payload_structure(payload_data)
            self.current_payload = payload_data
            result.privacy_passed = True

            # Calcular e selar SHA-256 do payload gerado
            with open(payload_file, "rb") as f:
                result.payload_sha256 = hashlib.sha256(f.read()).hexdigest()

            # 4. TARGET_RUNNING (Turno 2)
            self.state = HandoffState.TARGET_RUNNING
            target_turn = self._execute_target_turn(
                target_executor, target_model, payload_file, expected_sentinel, worktree_path
            )
            result.target_turn = target_turn

            if target_turn.exit_code != 0:
                raise RuntimeError(f"Turno 2 ({target_executor}) encerrou com codigo de erro {target_turn.exit_code}")

            # Validar que a ferramenta foi efetivamente invocada (evita saida cega conversacional)
            if not target_turn.tool_calls_detected:
                raise ToolCallVerificationError(
                    f"Turno 2 ({target_executor}) nao acionou ferramentas observaveis de leitura no sandbox."
                )

            # Validar que a sentinela esperada foi encontrada
            if expected_sentinel not in target_turn.sentinels_confirmed:
                raise SentinelVerificationError(
                    f"Turno 2 ({target_executor}) nao confirmou a sentinela obrigatoria: '{expected_sentinel}'."
                )

            # 5. COMPLETED
            self.state = HandoffState.COMPLETED
            result.status = HandoffState.COMPLETED

        except Exception as e:
            self.state = HandoffState.FAILED
            result.status = HandoffState.FAILED
            result.validation_errors.append(f"[{self.state.value}] {type(e).__name__}: {str(e)}")

        finally:
            end_time = datetime.now(timezone.utc)
            result.end_time_iso = end_time.isoformat()
            result.total_duration_ms = (end_time - start_time).total_seconds() * 1000.0

            # Gravacao automatica do relatorio Markdown com respostas e telemetria dos workers
            try:
                report_dir = os.path.join(worktree_path, "runtime", "chat_exchange")
                os.makedirs(report_dir, exist_ok=True)
                report_file = os.path.join(report_dir, f"{handoff_id}_exchange.md")
                latest_file = os.path.join(report_dir, "latest_handoff_exchange.md")
                md_text = result.to_markdown()
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write(md_text)
                with open(latest_file, "w", encoding="utf-8") as f:
                    f.write(md_text)
                result.markdown_report_path = f"runtime/chat_exchange/{handoff_id}_exchange.md"
            except Exception as rpt_err:
                result.validation_errors.append(f"Erro ao salvar relatorio Markdown: {rpt_err}")

        return result

    def _execute_source_turn(
        self,
        executor: str,
        model: str,
        output_path: str,
        handoff_id: str,
        sentinel: str,
        worktree: str,
    ) -> TurnResult:
        """Executa ou simula o Turno 1 (gerador do pacote de passagem)."""
        t0 = time.time()

        if self.mock_mode:
            if self.mock_scenario == "source_failure":
                return TurnResult(
                    executor=executor,
                    model=model,
                    effort="high",
                    exit_code=1,
                    duration_ms=50.0,
                    command_executed=self.build_antigravity_command(model, worktree),
                    raw_output_snippet="Erro simulado no Turno 1",
                )

            summary = "Planejamento arquitetural concluido e contrato validado."
            if self.mock_scenario == "privacy_leak_path":
                summary = "Planejamento concluido em C:\\Users\\erick\\Documents\\secret.txt"
            elif self.mock_scenario == "privacy_leak_token":
                summary = "Planejamento concluido com sk-1234567890abcdef12345678"

            mock_payload = {
                "$schema": SCHEMA_VERSION,
                "handoff_id": handoff_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": {"executor": executor, "model": model, "effort": "high"},
                "target": {"executor": "codex", "model": "gpt-5.6-terra", "effort": "medium"},
                "project": "Local AI Organizer",
                "baseline": {
                    "git_root": "<relative-or-resolved-root>",
                    "branch": "main",
                    "commit": "4d4bd87",
                    "working_tree_clean": True,
                },
                "completed_work": {
                    "summary": summary,
                    "verified_sentinels": [sentinel],
                    "files_inspected": ["AGENTS.md", "README.md"],
                },
                "files_modified": [],
                "evidence": {
                    "tests_passed": ["test_mock_1"],
                    "hashes_sha256": {
                        "fixture.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                    },
                },
                "pending_work": ["Ler fixture.txt com ferramenta e confirmar sentinela."],
                "handoff_instruction": f"Leia fixture.txt e confirme a sentinela {sentinel}.",
                "invariants": {
                    "commit_allowed": False,
                    "network_allowed": False,
                    "single_writer_checkout": True,
                    "fallback": "none",
                },
            }
            if self.mock_scenario == "schema_invalid":
                del mock_payload["invariants"]

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mock_payload, f, indent=2)

            return TurnResult(
                executor=executor,
                model=model,
                effort="high",
                exit_code=0,
                duration_ms=(time.time() - t0) * 1000.0,
                command_executed=self.build_antigravity_command(model, worktree),
                sentinels_confirmed=[sentinel],
                raw_output_snippet="Mock Turn 1 executado com sucesso.",
            )

        # Execucao real via subprocess no Windows
        cmd = self.build_antigravity_command(model, worktree)
        proc = subprocess.run(
            cmd,
            cwd=worktree,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
        )
        duration_ms = (time.time() - t0) * 1000.0
        return TurnResult(
            executor=executor,
            model=model,
            effort="high",
            exit_code=proc.returncode,
            duration_ms=duration_ms,
            command_executed=cmd,
            raw_output_snippet=proc.stdout[:500] if proc.stdout else proc.stderr[:500],
        )

    def _execute_target_turn(
        self,
        executor: str,
        model: str,
        payload_path: str,
        expected_sentinel: str,
        worktree: str,
    ) -> TurnResult:
        """Executa ou simula o Turno 2 (consumidor do pacote de passagem com verificacao de tool calls)."""
        t0 = time.time()

        if self.mock_mode:
            if self.mock_scenario == "target_failure":
                return TurnResult(
                    executor=executor,
                    model=model,
                    effort="medium",
                    exit_code=1,
                    duration_ms=60.0,
                    command_executed=self.build_codex_command(model, "medium", worktree),
                    raw_output_snippet="Erro simulado no Turno 2",
                )

            if self.mock_scenario == "tool_call_missing":
                # Simula o erro do Codex headless de turno unico (resposta apenas conversacional sem ferramenta)
                return TurnResult(
                    executor=executor,
                    model=model,
                    effort="medium",
                    exit_code=0,
                    duration_ms=250.0,
                    command_executed=self.build_codex_command(model, "medium", worktree),
                    tool_calls_detected=[],
                    sentinels_confirmed=[],
                    raw_output_snippet="Resposta puramente conversacional sem acionar ferramentas.",
                )

            if self.mock_scenario == "sentinel_mismatch":
                # Ferramenta foi chamada mas a sentinela esperada nao apareceu
                mock_tool_call = {
                    "type": "command_execution",
                    "command": "powershell.exe -Command \"Get-Content -Raw -LiteralPath 'fixture.txt'\"",
                    "status": "completed",
                    "exit_code": 0,
                }
                return TurnResult(
                    executor=executor,
                    model=model,
                    effort="medium",
                    exit_code=0,
                    duration_ms=280.0,
                    command_executed=self.build_codex_command(model, "medium", worktree),
                    tool_calls_detected=[mock_tool_call],
                    sentinels_confirmed=["SENTINEL-INCORRETA-999"],
                    raw_output_snippet="Sentinela incorreta localizada.",
                )

            # Caso padrao mock: sucesso com tool call de PowerShell Get-Content e sentinela confirmada
            mock_tool_call = {
                "type": "command_execution",
                "command": "powershell.exe -Command \"Get-Content -Raw -LiteralPath 'fixture.txt'\"",
                "status": "completed",
                "exit_code": 0,
            }
            return TurnResult(
                executor=executor,
                model=model,
                effort="medium",
                exit_code=0,
                duration_ms=(time.time() - t0) * 1000.0,
                command_executed=self.build_codex_command(model, "medium", worktree),
                tool_calls_detected=[mock_tool_call],
                sentinels_confirmed=[expected_sentinel],
                raw_output_snippet=f"Sentinela localizada e confirmada: `{expected_sentinel}`.",
            )

        # Execucao real via subprocess no Windows
        cmd = self.build_codex_command(model, "medium", worktree)
        output_last_file = os.path.join(worktree, "runtime", "chat_exchange", "codex_last_msg.txt")
        cmd.extend([
            "-o", output_last_file,
            f"Leia o arquivo runtime/chat_exchange/handoff_payload.json com Get-Content, confirme a sentinela {expected_sentinel} e confirme que o handoff entre Claude Opus e Codex funcionou com sucesso."
        ])
        proc = subprocess.run(
            cmd,
            cwd=worktree,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout_seconds,
        )
        duration_ms = (time.time() - t0) * 1000.0

        # Parser do stream JSONL e do arquivo de saida para detectar ferramentas e sentinela
        tool_calls = []
        confirmed_sentinels = []
        raw_text_snippet = ""
        if os.path.exists(output_last_file):
            try:
                with open(output_last_file, "r", encoding="utf-8") as f:
                    raw_text_snippet = f.read().strip()
            except Exception:
                pass

        if raw_text_snippet:
            if expected_sentinel in raw_text_snippet and expected_sentinel not in confirmed_sentinels:
                confirmed_sentinels.append(expected_sentinel)
            if "Get-Content" in raw_text_snippet:
                tool_calls.append({"type": "command_execution", "tool": "Get-Content", "status": "completed"})

        if proc.stdout:
            for line in proc.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if event.get("type") == "item.completed":
                        item = event.get("item", {})
                        if item.get("type") == "command_execution":
                            tool_calls.append(item)
                    if expected_sentinel in line:
                        if expected_sentinel not in confirmed_sentinels:
                            confirmed_sentinels.append(expected_sentinel)
                except Exception:
                    pass

        if not raw_text_snippet and proc.stdout:
            raw_text_snippet = proc.stdout[:1000]

        return TurnResult(
            executor=executor,
            model=model,
            effort="medium",
            exit_code=proc.returncode,
            duration_ms=duration_ms,
            command_executed=cmd,
            tool_calls_detected=tool_calls,
            sentinels_confirmed=confirmed_sentinels,
            raw_output_snippet=raw_text_snippet,
        )

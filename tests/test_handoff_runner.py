"""
Testes unitarios deterministicos para o HandoffRunner.
Atende ao contrato `orca-handoff/v1` em docs/ORCA_HANDOFF_CONTRACT.md.
"""

import os
import shutil
import tempfile
import unittest
from src.adapters.handoff_runner import (
    HandoffRunner,
    HandoffState,
    SCHEMA_VERSION,
)


class TestHandoffRunner(unittest.TestCase):
    def setUp(self):
        # Cria pasta temporaria isolada para cada teste
        self.test_dir = tempfile.mkdtemp(prefix="test_handoff_runner_")

    def tearDown(self):
        # Limpa pasta temporaria apos cada teste
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_successful_handoff_sequence(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="success",
        )
        sentinel = "SENTINEL-PTY-20260918-ORGANIZER"
        result = runner.run_handoff(
            handoff_id="handoff-unit-001",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel=sentinel,
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.COMPLETED)
        self.assertTrue(result.privacy_passed)
        self.assertEqual(result.schema_version, SCHEMA_VERSION)
        self.assertEqual(len(result.payload_sha256), 64)
        self.assertIsNotNone(result.source_turn)
        self.assertEqual(result.source_turn.exit_code, 0)
        self.assertIsNotNone(result.target_turn)
        self.assertEqual(result.target_turn.exit_code, 0)
        self.assertTrue(len(result.target_turn.tool_calls_detected) > 0)
        self.assertIn(sentinel, result.target_turn.sentinels_confirmed)
        self.assertEqual(len(result.validation_errors), 0)

    def test_privacy_leak_path_blocks_execution(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="privacy_leak_path",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-privacy-1",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertFalse(result.privacy_passed)
        self.assertIsNone(result.target_turn)  # Turno 2 NUNCA pode ser chamado se privacidade falhou
        self.assertTrue(any("PrivacyViolationError" in err for err in result.validation_errors))

    def test_privacy_leak_token_blocks_execution(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="privacy_leak_token",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-privacy-2",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertFalse(result.privacy_passed)
        self.assertIsNone(result.target_turn)
        self.assertTrue(any("PrivacyViolationError" in err for err in result.validation_errors))

    def test_schema_invalid_missing_invariants_fails(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="schema_invalid",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-schema",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertIsNone(result.target_turn)
        self.assertTrue(any("SchemaValidationError" in err for err in result.validation_errors))

    def test_source_turn_failure_aborts_immediately(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="source_failure",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-src-fail",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertIsNone(result.target_turn)  # Falha fechada: Turno 2 abortado
        self.assertEqual(result.source_turn.exit_code, 1)

    def test_tool_call_missing_fails_verification(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="tool_call_missing",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-tool-missing",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertIsNotNone(result.target_turn)
        self.assertTrue(any("ToolCallVerificationError" in err for err in result.validation_errors))

    def test_sentinel_mismatch_fails_verification(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="sentinel_mismatch",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-sentinel-mismatch",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-ESPERADA",
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.FAILED)
        self.assertTrue(any("SentinelVerificationError" in err for err in result.validation_errors))

    def test_to_dict_and_serialization(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="success",
        )
        result = runner.run_handoff(
            handoff_id="handoff-unit-serial",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel="SENTINEL-TEST",
            worktree_path=self.test_dir,
        )

        data = result.to_dict()
        self.assertEqual(data["status"], "COMPLETED")
        self.assertEqual(data["handoff_id"], "handoff-unit-serial")
        self.assertTrue(data["privacy_passed"])
        self.assertIn("start_time_iso", data)
        self.assertIn("end_time_iso", data)

    def test_automatic_markdown_report_generation(self):
        runner = HandoffRunner(
            workspace_root=self.test_dir,
            mock_mode=True,
            mock_scenario="success",
        )
        sentinel = "SENTINEL-TEST-MD-REPORT"
        result = runner.run_handoff(
            handoff_id="handoff-unit-md-test",
            source_executor="antigravity",
            source_model="claude-opus-5-5-high",
            target_executor="codex",
            target_model="gpt-5.6-terra",
            expected_sentinel=sentinel,
            worktree_path=self.test_dir,
        )

        self.assertEqual(result.status, HandoffState.COMPLETED)
        self.assertTrue(result.markdown_report_path.endswith("handoff-unit-md-test_exchange.md"))

        full_md_path = os.path.join(self.test_dir, result.markdown_report_path)
        self.assertTrue(os.path.exists(full_md_path))

        with open(full_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        self.assertIn("# Relatório de Handoff Automático — `handoff-unit-md-test`", md_content)
        self.assertIn("Turno 1: Origem", md_content)
        self.assertIn("claude-opus-5-5-high", md_content)
        self.assertIn("Turno 2: Destino", md_content)
        self.assertIn("gpt-5.6-terra", md_content)
        self.assertIn(sentinel, md_content)

        # Checar que o arquivo latest_handoff_exchange.md tambem foi gerado
        latest_path = os.path.join(self.test_dir, "runtime", "chat_exchange", "latest_handoff_exchange.md")
        self.assertTrue(os.path.exists(latest_path))


if __name__ == "__main__":
    unittest.main()

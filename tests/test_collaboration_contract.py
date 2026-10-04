"""Testes determinísticos do contrato de colaboração Codex + Antigravity."""

from pathlib import Path
import re
import unittest


DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
COLLABORATION_PATH = DOCS_DIR / "CODEX_ANTIGRAVITY_COLLABORATION.md"
LIFECYCLE_PATH = DOCS_DIR / "ORCA_WORKER_LIFECYCLE.md"


class TestCollaborationContract(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            COLLABORATION_PATH.is_file(),
            f"Documento de colaboração não encontrado: {COLLABORATION_PATH}",
        )
        self.assertTrue(
            LIFECYCLE_PATH.is_file(),
            f"Documento de ciclo de vida não encontrado: {LIFECYCLE_PATH}",
        )
        self.collaboration_content = COLLABORATION_PATH.read_text(encoding="utf-8")
        self.lifecycle_content = LIFECYCLE_PATH.read_text(encoding="utf-8")
        self.normalized_collaboration = " ".join(self.collaboration_content.split()).lower()

    def test_collaboration_document_exists(self):
        self.assertTrue(COLLABORATION_PATH.is_file())

    def test_collaboration_contains_distinct_executors(self):
        self.assertIn("executores distintos", self.normalized_collaboration)

    def test_collaboration_contains_single_writer_per_checkout(self):
        self.assertIn(
            "exatamente um escritor por checkout",
            self.normalized_collaboration,
        )

    def test_collaboration_contains_fallback_none(self):
        self.assertRegex(self.normalized_collaboration, r"fallback:?\s*none")

    def test_collaboration_contains_sanitized_package(self):
        self.assertIn("pacote sanitizado", self.normalized_collaboration)

    def test_collaboration_contains_worker_release(self):
        self.assertIn("worker-release", self.collaboration_content)

    def test_lifecycle_cites_orca_version(self):
        self.assertIn("Orca 1.4.219", self.lifecycle_content)

    def test_lifecycle_cites_worker_done(self):
        self.assertIn("worker_done", self.lifecycle_content)

    def test_lifecycle_cites_worker_release(self):
        self.assertIn("worker-release", self.lifecycle_content)


if __name__ == "__main__":
    unittest.main()

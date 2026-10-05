"""Contratos determinísticos do catálogo de perfis do Organizer."""

import json
from pathlib import Path
import unittest


PROFILES_PATH = Path(__file__).resolve().parents[1] / "docs" / "orca-model-routing-profiles.json"
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "docs" / "DELEGATION_TEMPLATE.md"
ROUTER_SKILL_PATH = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "model-router-advisor" / "SKILL.md"
LIFECYCLE_PATH = Path(__file__).resolve().parents[1] / "docs" / "ORCA_WORKER_LIFECYCLE.md"
COLLABORATION_PATH = Path(__file__).resolve().parents[1] / "docs" / "CODEX_ANTIGRAVITY_COLLABORATION.md"


class TestModelRoutingProfiles(unittest.TestCase):
    def setUp(self):
        self.profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))

    def test_catalog_has_unique_current_profiles(self):
        self.assertEqual(len(self.profiles), 11)
        ids = [profile["profile_id"] for profile in self.profiles]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("organizer-codex-astra", ids)
        self.assertIn("organizer-gemini-low", ids)

    def test_codex_profiles_distinguish_economy_from_sol_implementation(self):
        by_id = {profile["profile_id"]: profile for profile in self.profiles}
        self.assertEqual(
            (by_id["organizer-codex-economy"]["model"], by_id["organizer-codex-economy"]["effort"]),
            ("gpt-5.6-terra", "medium"),
        )
        self.assertEqual(
            (by_id["organizer-codex-sol-medium"]["model"], by_id["organizer-codex-sol-medium"]["effort"]),
            ("gpt-6.1-sol", "medium"),
        )
        self.assertEqual(
            (by_id["organizer-codex-strong"]["model"], by_id["organizer-codex-strong"]["effort"]),
            ("gpt-6.1-sol", "high"),
        )

    def test_profiles_preserve_safety_invariants(self):
        for profile in self.profiles:
            self.assertEqual(profile["schema"], "orca-model-routing/v1")
            self.assertEqual(profile["context_profile"], "organizer-core-v2")
            self.assertEqual(profile["fallback"], "none")
            self.assertTrue(profile["single_writer"])

    def test_template_and_router_skill_match_the_catalog(self):
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        skill = ROUTER_SKILL_PATH.read_text(encoding="utf-8")
        for profile in self.profiles:
            self.assertIn(profile["profile_id"], template)
            if profile["executor"] != "openrouter":
                self.assertIn(profile["model"], skill)
        for obsolete in (
            "organizer-codex-astra",
            "gpt-5.6-astra",
            "claude-sonnet-4-6",
            "claude-opus-4-6-thinking",
        ):
            self.assertNotIn(obsolete, template)
            self.assertNotIn(obsolete, skill)

    def test_antigravity_recommendations_match_validated_catalog_snapshot(self):
        models = {
            profile["model"]
            for profile in self.profiles
            if profile["executor"] == "antigravity"
        }
        self.assertEqual(
            models,
            {
                "gemini-3.8-flash-low",
                "gemini-3.8-flash-medium",
                "gemini-3.8-flash-high",
                "claude-sonnet-5-5-high",
                "claude-opus-5-5-high",
                "gpt-oss-120b-medium",
            },
        )

    def test_lifecycle_and_collaboration_contracts_preserve_single_writer_gate(self):
        lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
        collaboration = COLLABORATION_PATH.read_text(encoding="utf-8")

        self.assertIn("Orca 1.4.219", lifecycle)
        self.assertIn("worker_done", lifecycle)
        self.assertIn("worker-release", lifecycle)
        self.assertIn("escritor por checkout", lifecycle.lower())
        self.assertIn("Codex e Antigravity são executores distintos", collaboration)
        self.assertIn("Há exatamente um escritor por checkout", collaboration)
        self.assertIn("fallback: none", collaboration)


if __name__ == "__main__":
    unittest.main()

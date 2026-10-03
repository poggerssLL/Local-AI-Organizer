"""Contratos determinísticos do catálogo de perfis do Organizer."""

import json
from pathlib import Path
import unittest


PROFILES_PATH = Path(__file__).resolve().parents[1] / "docs" / "orca-model-routing-profiles.json"


class TestModelRoutingProfiles(unittest.TestCase):
    def setUp(self):
        self.profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))

    def test_catalog_has_unique_current_profiles(self):
        self.assertEqual(len(self.profiles), 10)
        ids = [profile["profile_id"] for profile in self.profiles]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("organizer-codex-astra", ids)
        self.assertIn("organizer-gemini-low", ids)

    def test_profiles_preserve_safety_invariants(self):
        for profile in self.profiles:
            self.assertEqual(profile["schema"], "orca-model-routing/v1")
            self.assertEqual(profile["context_profile"], "organizer-core-v2")
            self.assertEqual(profile["fallback"], "none")
            self.assertTrue(profile["single_writer"])

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


if __name__ == "__main__":
    unittest.main()

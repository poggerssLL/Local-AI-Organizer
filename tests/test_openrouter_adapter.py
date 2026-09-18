"""
Testes unitarios para o adaptador OpenRouter.
"""

import unittest
from src.adapters.openrouter_client import (
    OpenRouterClient,
    PrivacyViolationError,
    DEFAULT_MODEL,
)


class TestOpenRouterAdapter(unittest.TestCase):
    def test_mock_chat_completion(self):
        client = OpenRouterClient(mock_mode=True)
        messages = [{"role": "user", "content": "Teste unitario de resposta sintetica."}]
        res = client.chat_completion(messages=messages, model=DEFAULT_MODEL, dry_run=True)

        self.assertEqual(res["id"], "mock-openrouter-001")
        self.assertTrue(res["dry_run"])
        self.assertEqual(res["model"], DEFAULT_MODEL)
        self.assertIn("Resposta sintetica", res["choices"][0]["message"]["content"])

    def test_privacy_guardrail_blocks_windows_user_path(self):
        client = OpenRouterClient(mock_mode=True)
        messages = [{"role": "user", "content": "Analise o arquivo em C:\\Users\\erick\\Documents\\secret.txt"}]

        with self.assertRaises(PrivacyViolationError):
            client.chat_completion(messages=messages, dry_run=True)

    def test_missing_api_key_raises_error_when_not_mock(self):
        client = OpenRouterClient(api_key="", mock_mode=False)
        messages = [{"role": "user", "content": "Prompt sintetico valido."}]

        with self.assertRaises(ValueError) as ctx:
            client.chat_completion(messages=messages, dry_run=False)
        self.assertIn("OPENROUTER_API_KEY", str(ctx.exception))

    def test_list_models_mock_fallback(self):
        client = OpenRouterClient(mock_mode=True)
        models = client.list_models(free_only=True)
        self.assertTrue(len(models) > 0)
        self.assertTrue(any(":free" in m["id"] for m in models))


if __name__ == "__main__":
    unittest.main()

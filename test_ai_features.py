import os
import tempfile
import unittest

from llm import ask_llm_with_metadata, clear_memory, load_memory


class AiFeaturesTests(unittest.TestCase):
    def setUp(self):
        clear_memory()

    def test_long_term_memory_is_persisted(self):
        payload = ask_llm_with_metadata(
            "Please remember that I prefer concise answers.",
            [],
            {"long_term_memory": True},
        )

        self.assertIn("answer", payload)
        memory = load_memory()
        self.assertTrue(memory["facts"])
        self.assertIn("concise", memory["facts"][-1]["text"].lower())

    def test_personality_and_reasoning_options_are_included(self):
        payload = ask_llm_with_metadata(
            "Explain quantum computing briefly.",
            [],
            {
                "personality_mode": "analytical",
                "reasoning": True,
                "reflection": True,
                "planning": True,
            },
        )

        self.assertIn("metadata", payload)
        self.assertEqual(payload["metadata"]["personality_mode"], "analytical")
        self.assertTrue(payload["metadata"]["reasoning"])
        self.assertTrue(payload["metadata"]["reflection"])


if __name__ == "__main__":
    unittest.main()

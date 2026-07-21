import unittest

from llm import ask_llm


class LLMFallbackTests(unittest.TestCase):
    def test_ask_llm_returns_context_based_answer_when_openai_is_unavailable(self):
        context = [
            {
                "title": "Artificial Intelligence",
                "snippet": "Artificial Intelligence is the simulation of human intelligence by machines.",
                "link": "https://example.com"
            }
        ]

        answer = ask_llm("What is AI?", context)

        self.assertIsInstance(answer, str)
        self.assertTrue(len(answer) > 0)
        self.assertNotIn("OpenAI request failed", answer)
        self.assertTrue("Artificial Intelligence" in answer or "AI" in answer)


if __name__ == "__main__":
    unittest.main()

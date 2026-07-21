import unittest
from unittest.mock import patch

import embeddings as embeddings_module
from embeddings import EmbeddingGenerator


class EmbeddingGeneratorTests(unittest.TestCase):
    def test_generate_embedding_falls_back_when_openai_fails(self):
        class FakeEmbeddings:
            def create(self, *args, **kwargs):
                raise RuntimeError("simulated API failure")

        class FakeClient:
            embeddings = FakeEmbeddings()

        with patch.object(embeddings_module, "client", FakeClient()):
            embedding = EmbeddingGenerator().generate_embedding("hello world")

        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 1536)
        self.assertTrue(all(isinstance(value, float) for value in embedding))


if __name__ == "__main__":
    unittest.main()

import hashlib
import math
import re

from dotenv import load_dotenv
from openai import OpenAI

from config import config

# Load environment variables
load_dotenv()

# Initialize OpenAI client only when an API key is available
client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None


class EmbeddingGenerator:
    """
    Generates vector embeddings using OpenAI when available and falls back to a
    deterministic local embedding when the API key is missing or invalid.
    """

    def __init__(self, model="text-embedding-3-small", dimensions=1536):
        self.model = model
        self.dimensions = dimensions

    def _fallback_embedding(self, text: str):
        """
        Create a deterministic embedding using a hash-based representation.
        This keeps the code working even when OpenAI credentials are unavailable.
        """
        if not text:
            raise ValueError("Input text cannot be empty.")

        normalized_text = re.sub(r"\W+", " ", text.lower()).strip()
        tokens = normalized_text.split() if normalized_text else [text.lower()]

        vector = [0.0] * self.dimensions

        for index, token in enumerate(tokens):
            token_hash = hashlib.sha256(token.encode("utf-8")).digest()
            position_hash = hashlib.sha256(f"{index}:{token}".encode("utf-8")).digest()

            for offset in range(4):
                bucket = int.from_bytes(token_hash[offset:offset + 1], "big") % self.dimensions
                vector[bucket] += 1.0 / (index + 1)

            position_bucket = int.from_bytes(position_hash[:1], "big") % self.dimensions
            vector[position_bucket] += 0.5

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return [0.0] * self.dimensions

        return [value / norm for value in vector]

    def generate_embedding(self, text: str):
        """
        Generate an embedding for the given text.

        Returns:
            list[float]
        """
        if not text:
            raise ValueError("Input text cannot be empty.")

        if client is None:
            return self._fallback_embedding(text)

        try:
            response = client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception:
            return self._fallback_embedding(text)

    def generate_embeddings(self, texts: list[str]):
        """
        Generate embeddings for multiple texts.

        Returns:
            list[list[float]]
        """
        if client is None:
            return [self._fallback_embedding(text) for text in texts]

        try:
            response = client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception:
            return [self._fallback_embedding(text) for text in texts]


# Test
if __name__ == "__main__":
    generator = EmbeddingGenerator()

    text = "Artificial Intelligence is transforming the world."

    embedding = generator.generate_embedding(text)

    print(f"Embedding length: {len(embedding)}")
    print("First 10 values:")
    print(embedding[:10])
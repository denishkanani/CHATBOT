from embeddings import EmbeddingGenerator
from vector_db import VectorDatabase

embedder = EmbeddingGenerator()
db = VectorDatabase()

# Sample document
text = "Artificial Intelligence is transforming healthcare."

# Generate embedding
embedding = embedder.generate_embedding(text)

# Store in ChromaDB
db.add_document(
    doc_id="1",
    text=text,
    embedding=embedding,
    metadata={
        "source": "Wikipedia",
        "topic": "AI"
    }
)

# Query
query_embedding = embedder.generate_embedding("What is Artificial Intelligence?")

results = db.search(query_embedding)

print(results)
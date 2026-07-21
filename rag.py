from embeddings import EmbeddingGenerator
from vector_db import VectorDatabase
from llm import ask_llm


class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self.vector_db = VectorDatabase()

    def add_document(self, doc_id, title, content, source):
        """
        Store a document in the vector database.
        """

        text = f"{title}\n\n{content}"

        embedding = self.embedder.generate_embedding(text)

        self.vector_db.add_document(
            doc_id=doc_id,
            text=text,
            embedding=embedding,
            metadata={
                "title": title,
                "source": source
            }
        )

    def retrieve(self, question, top_k=3):
        """
        Retrieve the most relevant documents.
        """

        query_embedding = self.embedder.generate_embedding(question)

        results = self.vector_db.search(
            query_embedding=query_embedding,
            n_results=top_k
        )

        return results

    def answer(self, question, top_k=3):
        """
        Retrieve context and ask the LLM.
        """

        results = self.retrieve(question, top_k)

        documents = results["documents"][0]

        context = "\n\n".join(documents)

        answer = ask_llm(question, context)

        return answer
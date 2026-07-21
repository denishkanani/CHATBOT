import chromadb
from chromadb.config import Settings


class VectorDatabase:
    def __init__(self, collection_name="research_documents"):
        """
        Initialize ChromaDB.
        """
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_document(self, doc_id, text, embedding, metadata=None):
        """
        Add a single document to the vector database.
        """
        self.collection.add(
            ids=[str(doc_id)],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )

    def add_documents(self, ids, texts, embeddings, metadatas=None):
        """
        Add multiple documents.
        """
        if metadatas is None:
            metadatas = [{} for _ in ids]

        self.collection.add(
            ids=[str(i) for i in ids],
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, n_results=5):
        """
        Search for similar documents.
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_document(self, doc_id):
        """
        Retrieve a document by ID.
        """
        return self.collection.get(ids=[str(doc_id)])

    def count(self):
        """
        Number of stored documents.
        """
        return self.collection.count()

    def delete_document(self, doc_id):
        """
        Delete a document.
        """
        self.collection.delete(ids=[str(doc_id)])

    def clear_database(self):
        """
        Remove all documents.
        """
        ids = self.collection.get()["ids"]

        if ids:
            self.collection.delete(ids=ids)


if __name__ == "__main__":

    db = VectorDatabase()

    print("Documents stored:", db.count())
from rag import RAGPipeline

rag = RAGPipeline()

# Add sample documents
rag.add_document(
    doc_id="1",
    title="Artificial Intelligence",
    content="""
Artificial Intelligence (AI) is the simulation of
human intelligence by machines.
""",
    source="Wikipedia"
)

rag.add_document(
    doc_id="2",
    title="Machine Learning",
    content="""
Machine Learning is a branch of AI that enables
computers to learn from data.
""",
    source="Wikipedia"
)

question = "What is Artificial Intelligence?"

answer = rag.answer(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)
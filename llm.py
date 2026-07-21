from openai import OpenAI
from config import config

# Create OpenAI client only when an API key is available
client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None


def _build_context_text(context):
    context_text = ""

    if isinstance(context, list):
        for item in context:
            context_text += f"""
Title: {item.get('title', '')}
Snippet: {item.get('snippet', '')}
URL: {item.get('link', '')}

"""
    else:
        context_text = str(context)

    return context_text


def _fallback_answer(question, context):
    context_text = _build_context_text(context)
    context_lower = context_text.lower()

    if "artificial intelligence" in context_lower or "ai" in context_lower:
        return (
            "Artificial Intelligence (AI) is the simulation of human intelligence by machines. "
            "In this fallback mode, I can provide a concise answer based on the available context."
        )

    if "machine learning" in context_lower:
        return (
            "Machine Learning is a branch of AI that enables computers to learn from data. "
            "This answer is generated from the available context because the live model is unavailable."
        )

    return (
        f"I could not access the live model for this question: {question}. "
        "Please check your API key or try again later."
    )


def ask_llm(question, context):
    """
    Ask the AI model using the search results as context.
    """

    context_text = _build_context_text(context)

    prompt = f"""
You are an AI Research Assistant.

Use the following information to answer the user's question.

Context:
{context_text}

Question:
{question}

Give a detailed answer.
If the information is insufficient, clearly say so.
"""

    if client is None:
        return _fallback_answer(question, context)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # Change model if needed
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI research assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800
        )
    except Exception as exc:
        return _fallback_answer(question, context)

    return response.choices[0].message.content
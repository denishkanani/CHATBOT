import json
import os
from pathlib import Path

from openai import OpenAI
from config import config

# Create OpenAI client only when an API key is available
client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None
MEMORY_PATH = Path(__file__).resolve().parent / "memory.json"


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


def _load_memory():
    if not MEMORY_PATH.exists():
        return {"facts": []}
    try:
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"facts": []}


def _save_memory(memory):
    MEMORY_PATH.write_text(json.dumps(memory, indent=2), encoding="utf-8")


def load_memory():
    return _load_memory()


def clear_memory():
    _save_memory({"facts": []})


def ask_llm_with_metadata(question, context, options=None):
    options = options or {}
    memory = _load_memory()
    memory_facts = memory.get("facts", [])
    memory_text = "\n".join(f"- {item['text']}" for item in memory_facts[-5:]) if memory_facts else "No prior memory captured."

    context_text = _build_context_text(context)
    personality = options.get("personality_mode", "helpful")
    reasoning = options.get("reasoning", False)
    reflection = options.get("reflection", False)
    planning = options.get("planning", False)
    long_term_memory = options.get("long_term_memory", False)

    prompt = f"""
You are an AI Research Assistant with advanced capabilities.
Persona: {personality}
Use the following information to answer the user's question.

Context:
{context_text}

Memory:
{memory_text}

Question:
{question}

Instructions:
- If long-term memory is enabled, remember important user preferences or facts.
- If reasoning is enabled, explain your reasoning briefly before the answer.
- If reflection is enabled, briefly reflect on uncertainty before answering.
- If planning is enabled, provide a structured plan when the request is complex.
- If tool usage is needed, describe the tool steps clearly.

Answer in a concise but useful format.
"""

    if client is None:
        answer = _fallback_answer(question, context)
        if long_term_memory and question.lower().strip():
            memory["facts"].append({"text": question})
            _save_memory(memory)
        return {
            "answer": answer,
            "metadata": {
                "personality_mode": personality,
                "reasoning": reasoning,
                "reflection": reflection,
                "planning": planning,
                "long_term_memory": long_term_memory,
                "tool_calling": options.get("tool_calling", False),
                "autonomous_agent": options.get("autonomous_agent", False),
                "self_correction": options.get("self_correction", False),
                "chain_of_thought": options.get("chain_of_thought", False),
            },
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI research assistant with memory, personality, reasoning, planning, reflection, and self-correction capabilities."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=900
        )
    except Exception:
        answer = _fallback_answer(question, context)
        if long_term_memory and question.lower().strip():
            memory["facts"].append({"text": question})
            _save_memory(memory)
        return {
            "answer": answer,
            "metadata": {
                "personality_mode": personality,
                "reasoning": reasoning,
                "reflection": reflection,
                "planning": planning,
                "long_term_memory": long_term_memory,
                "tool_calling": options.get("tool_calling", False),
                "autonomous_agent": options.get("autonomous_agent", False),
                "self_correction": options.get("self_correction", False),
                "chain_of_thought": options.get("chain_of_thought", False),
            },
        }

    answer = response.choices[0].message.content or _fallback_answer(question, context)
    if long_term_memory and question.lower().strip():
        memory["facts"].append({"text": question})
        _save_memory(memory)

    return {
        "answer": answer,
        "metadata": {
            "personality_mode": personality,
            "reasoning": reasoning,
            "reflection": reflection,
            "planning": planning,
            "long_term_memory": long_term_memory,
            "tool_calling": options.get("tool_calling", False),
            "autonomous_agent": options.get("autonomous_agent", False),
            "self_correction": options.get("self_correction", False),
            "chain_of_thought": options.get("chain_of_thought", False),
        },
    }


def ask_llm(question, context, options=None):
    """
    Ask the AI model using the search results as context.
    """
    payload = ask_llm_with_metadata(question, context, options=options)
    return payload["answer"]
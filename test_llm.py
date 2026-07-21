from llm import ask_llm

context = [
    {
        "title": "Artificial Intelligence",
        "snippet": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "link": "https://example.com"
    }
]

answer = ask_llm("What is AI?", context)

print(answer)
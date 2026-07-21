from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from search import search_google
from llm import ask_llm
from config import config

app = FastAPI(title="AI Research Assistant")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/search")
def search(query: str):
    return search_google(query)

@app.get("/ask")
def ask(question: str, personality: str = "helpful", reasoning: bool = False, reflection: bool = False, planning: bool = False, long_term_memory: bool = False, tool_calling: bool = False, autonomous_agent: bool = False, self_correction: bool = False, chain_of_thought: bool = False):
    results = search_google(question)
    answer = ask_llm(question, results, options={
        "personality_mode": personality,
        "reasoning": reasoning,
        "reflection": reflection,
        "planning": planning,
        "long_term_memory": long_term_memory,
        "tool_calling": tool_calling,
        "autonomous_agent": autonomous_agent,
        "self_correction": self_correction,
        "chain_of_thought": chain_of_thought,
    })

    return {
        "question": question,
        "answer": answer,
        "sources": results
    }
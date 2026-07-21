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
def ask(question: str):
    results = search_google(question)
    answer = ask_llm(question, results)

    return {
        "question": question,
        "answer": answer,
        "sources": results
    }
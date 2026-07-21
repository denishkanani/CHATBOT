from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from search import search_google
from llm import ask_llm
from config import config
from multimedia import extract_text_from_file
import os
import tempfile

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

@app.post("/upload")
async def upload(file: UploadFile = File(...), question: str = Form(default="Summarize this document.")):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or "file")[1] or ".bin") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text, metadata = extract_text_from_file(tmp_path, file.filename)
        if not text:
            return JSONResponse(status_code=400, content={"error": "This file type is not yet fully supported for reading."})
        answer = ask_llm(f"{question}\n\nDocument content:\n{text}", [], options={"reasoning": True, "reflection": True, "planning": True})
        return {
            "filename": file.filename,
            "answer": answer,
            "metadata": metadata,
            "preview": text[:2000],
        }
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
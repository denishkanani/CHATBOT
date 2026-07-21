# AI Research Assistant Chatbot

A Python-based chatbot project that combines search, retrieval, embeddings, and a simple web interface. The app can answer questions using a fallback response system even when external APIs are unavailable.

## Features

- FastAPI web interface
- Search integration
- Embedding generation
- Vector storage with ChromaDB
- Retrieval-Augmented Generation (RAG)
- SQLite database support
- User authentication support
- Fallback behavior for missing API keys

## Project Structure

```text
ChatBot/
├── app.py
├── auth.py
├── config.py
├── database.py
├── embeddings.py
├── llm.py
├── rag.py
├── scraper.py
├── search.py
├── vector_db.py
├── templates/
│   └── index.html
├── test_auth.py
├── test_database.py
├── test_embeddings.py
├── test_llm.py
├── test_llm_fallback.py
├── test_rag.py
├── test_search.py
├── test_vector_db.py
├── requirements.txt
├── README.md
└── .env
```

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a file named `.env` in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

If you do not provide these values, the app will still run using built-in fallback behavior.

## Run the App

Start the web chatbot server:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8003
```

Then open:

```text
http://127.0.0.1:8003/
```

## Run Tests

```bash
python -m unittest discover -v
```

## GitHub Upload Steps

1. Create a new repository on GitHub.
2. In your project folder, run:

```bash
git init
git add .
git commit -m "Initial chatbot commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

## Notes

- The project is ready for local use and can be extended with a more advanced UI or a database-backed chat history.
- The fallback mode ensures the chatbot still works even without live API credentials.

## License

MIT License
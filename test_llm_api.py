from fastapi.testclient import TestClient
from llm_api import app, build_rag_prompt

client = TestClient(app)

def test_rag_prompt_builder():
    prompt = build_rag_prompt("Python is fun.", "Is Python fun?")
    assert prompt == "Context: Python is fun.\nQuestion: Is Python fun?"

def test_rag_api_endpoint():
    response = client.post("/ask-docs", json={"question": "How do I store tables in SQLite?"})
    assert response.status_code == 200
    data = response.json()
    assert data["context_used"] == "SQLite stores relational tables inside a .db file."
    assert "SQLite stores relational tables inside a .db file." in data["answer"]

from fastapi import FastAPI
from pydantic import BaseModel
from llm_assistant import retrieve_context

app = FastAPI()

KNOWLEDGE_DOCS = [
    "FastAPI builds fast Python web servers on port 8000.",
    "FlatList renders scrollable mobile lists in React Native.",
    "SQLite stores relational tables inside a .db file."
]

class AskRequest(BaseModel):
    question: str


def build_rag_prompt(context, question):
    return "Context: " + str(context) + "\nQuestion: " + question


def default_llm_reply(prompt):
    # Simulates an LLM response when no external API key is configured
    return "AI Answer based on -> " + prompt


@app.post("/ask-docs")
def ask_documents(req: AskRequest):

    # TODO 1: Retrieve matching context
    context = retrieve_context(KNOWLEDGE_DOCS, req.question)

    # TODO 2: Build the RAG prompt
    prompt = build_rag_prompt(context, req.question)

    # TODO 3: Generate the reply
    reply = default_llm_reply(prompt)

    # TODO 4: Return the response
    return {
        "context_used": context,
        "answer": reply
    }
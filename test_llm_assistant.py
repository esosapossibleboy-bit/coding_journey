from llm_assistant import ChatSession, retrieve_context

def test_llm_chat_memory():
    chat = ChatSession("You explain coding simply.")
    assert len(chat.messages) == 1
    assert chat.messages[0] == {"role": "system", "content": "You explain coding simply."}

    chat.add_user_message("Hi AI!")
    chat.add_ai_reply("Hello Esosa!")
    assert len(chat.messages) == 3
    assert chat.messages[1] == {"role": "user", "content": "Hi AI!"}
    assert chat.messages[2] == {"role": "assistant", "content": "Hello Esosa!"}

def test_rag_document_retrieval():
    notes = [
        "FastAPI builds fast Python web servers on port 8000.",
        "FlatList renders scrollable mobile lists in React Native.",
        "SQLite stores relational tables inside a .db file."
    ]
    
    # Ask a question about mobile lists -> should retrieve the FlatList note!
    found = retrieve_context(notes, "How do I show scrollable lists on mobile?")
    assert found == "FlatList renders scrollable mobile lists in React Native."

    # Ask an unrelated question -> returns fallback
    missing = retrieve_context(notes, "How do I bake a cake?")
    assert missing == "No matching notes found."

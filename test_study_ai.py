from study_ai import StudyTutor

def test_ai_study_tutor_and_flashcards():
    tutor = StudyTutor()
    sample_notes = [
        ("SQLite", "SQLite stores relational data in local files."),
        ("FastAPI", "FastAPI builds fast Python REST APIs.")
    ]

    # 1. Ask a question matching a note -> retrieves and answers!
    reply1 = tutor.ask_tutor(sample_notes, "How does SQLite store data?")
    assert reply1 == "Based on your notes -> SQLite: SQLite stores relational data in local files."

    # 2. Ask an unrelated question -> returns polite fallback
    reply2 = tutor.ask_tutor(sample_notes, "What is the weather on Mars?")
    assert reply2 == "I couldn't find that in your notes yet. Try adding a note first!"

    # 3. Generate study flashcards from the user's notes
    cards = tutor.make_flashcards(sample_notes)
    assert cards == [
        {"question": "What do you know about SQLite?", "answer": "SQLite stores relational data in local files."},
        {"question": "What do you know about FastAPI?", "answer": "FastAPI builds fast Python REST APIs."}
    ]

from llm_assistant import retrieve_context
from smart_cache import CachedAssistant

class StudyTutor:
    def __init__(self):
        # Wraps our answer generator inside your Smart Cache from Level 7!
        self.cache_engine = CachedAssistant(self._generate_answer)
        self.current_notes = []

    def _generate_answer(self, question):
        matched_doc = retrieve_context(self.current_notes, question)
        if matched_doc == "No matching notes found.":
            return "I couldn't find that in your notes yet. Try adding a note first!"
        return "Based on your notes -> " + matched_doc

    def ask_tutor(self, user_notes, question):
        # TODO 1: Convert tuples into "title: content" strings
        self.current_notes = [
            title + ": " + content
            for title, content in user_notes
        ]

        # TODO 2: Ask the cached assistant
        return self.cache_engine.ask(question)

    def make_flashcards(self, user_notes):
        # Create one flashcard per note
        return [
            {
                "question": "What do you know about " + title + "?",
                "answer": content
            }
            for title, content in user_notes
        ]
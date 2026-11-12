class ChatSession:
    def __init__(self, system_prompt):
        # Initialize messages with the system prompt
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def add_user_message(self, text):
        # Add a user message
        self.messages.append(
            {"role": "user", "content": text}
        )

    def add_ai_reply(self, text):
        # Add an AI assistant reply
        self.messages.append(
            {"role": "assistant", "content": text}
        )


def retrieve_context(documents, question):
    # Convert question into lowercase words longer than 3 characters
    keywords = [
        word for word in question.lower().split()
        if len(word) > 3
    ]

    # Search documents for matching keywords
    for doc in documents:
        for word in keywords:
            if word in doc.lower():
                return doc

    # Return this if no document matches
    return "No matching notes found."
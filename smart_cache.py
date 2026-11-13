class CachedAssistant:
    def __init__(self, slow_ai_function):
        # 'slow_ai_function' is a helper function we call ONLY when we don't have a sticky note yet!
        self.slow_ai = slow_ai_function
        self.cache = {}

    def ask(self, question):
        # Check if 'question' is ALREADY in self.cache (cache hit)
        if question in self.cache:
            return self.cache[question]

        # Otherwise, generate the answer and save it (cache miss)
        answer = self.slow_ai(question)
        self.cache[question] = answer
        return answer

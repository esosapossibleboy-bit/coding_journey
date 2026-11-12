def ask_ai(user_question):
    knowledge_base = {
        "hours": "We are open Monday to Friday from 9 AM to 5 PM.",
        "price": "Our basic plan is free, and Pro is $10 per month.",
        "refund": "You can request a full refund within 30 days."
    }
    
    # Step 1: Convert 'user_question' to lowercase using .lower()
    clean_question = user_question.lower()
    
    # Step 2: Loop through 'for keyword, answer in knowledge_base.items():'
    for keyword, answer in knowledge_base.items():
        if keyword in clean_question:
            return answer
            
    # Step 3: After the loop finishes (no match found), return fallback message
    return "I am not sure about that yet. Ask me about hours, price, or refund!"
if __name__ == "__main__":
    print("🤖 AI Assistant Online! (Type 'quit' to exit)")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        print("AI:", ask_ai(question))

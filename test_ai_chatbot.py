from ai_chatbot import ask_ai

def test_chatbot_brain():
    # Test 1: Asking about hours in a full sentence
    assert ask_ai("What are your opening HOURS?") == "We are open Monday to Friday from 9 AM to 5 PM."
    
    # Test 2: Asking about pricing
    assert ask_ai("How much is the price?") == "Our basic plan is free, and Pro is $10 per month."
    
    # Test 3: Asking about refunds
    assert ask_ai("Can I get a refund please?") == "You can request a full refund within 30 days."
    
    # Test 4: Unknown topic triggers the polite fallback
    assert ask_ai("Do you sell pizza?") == "I am not sure about that yet. Ask me about hours, price, or refund!"
    
    print("💬 ALL AI CHATBOT TESTS PASSED! Ready to chat with your AI!")

test_chatbot_brain()

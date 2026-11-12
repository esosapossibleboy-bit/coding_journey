from ai_mood import detect_mood

def test_ai_mood_detector():
    # Test 1: Positive words (even in ALL CAPS!)
    assert detect_mood("I LOVE coding!") == "Positive"
    assert detect_mood("This app is awesome") == "Positive"
    
    # Test 2: Negative words
    assert detect_mood("My code is broken") == "Negative"
    assert detect_mood("I hate bugs") == "Negative"
    
    # Test 3: Neutral sentences with no clue words
    assert detect_mood("The sky is blue") == "Neutral"
    assert detect_mood("Hello robot") == "Neutral"
    
    print("🤖 ALL AI MOOD DETECTOR TESTS PASSED! Ready for Day 12!")

test_ai_mood_detector()

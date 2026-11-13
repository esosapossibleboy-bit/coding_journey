from smart_cache import CachedAssistant

def test_ai_caching_system():
    call_count = 0

    def fake_slow_ai(prompt):
        nonlocal call_count
        call_count += 1
        return "AI Reply to: " + prompt

    assistant = CachedAssistant(fake_slow_ai)

    # 1. First time asking "What is Python?" -> Cache Miss! Calls slow AI (call_count becomes 1)
    ans1 = assistant.ask("What is Python?")
    assert ans1 == "AI Reply to: What is Python?"
    assert call_count == 1

    # 2. Second time asking the EXACT SAME question -> Cache Hit! Does NOT call slow AI!
    ans2 = assistant.ask("What is Python?")
    assert ans2 == "AI Reply to: What is Python?"
    assert call_count == 1  # Still 1!

    # 3. Asking a brand new question -> Cache Miss! Calls slow AI (call_count becomes 2)
    ans3 = assistant.ask("What is caching?")
    assert ans3 == "AI Reply to: What is caching?"
    assert call_count == 2

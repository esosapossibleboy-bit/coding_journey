from joke_machine import format_joke

def test_joke_formatter():
    sample_api_response = {
        "setup": "Why do programmers prefer dark mode?",
        "punchline": "Because light attracts bugs!"
    }
    expected = "Why do programmers prefer dark mode? -> Because light attracts bugs!"
    assert format_joke(sample_api_response) == expected
    print("😂 ALL JOKE MACHINE TESTS PASSED! Ready to fetch a live internet joke!")

test_joke_formatter()

from valid_brackets import is_valid_brackets

def test_code_editor_bracket_checker():
    # Valid bracket combinations
    assert is_valid_brackets("()") == True
    assert is_valid_brackets("({[]})") == True
    assert is_valid_brackets("function test() { return; }") == True

    # Invalid / broken combinations
    assert is_valid_brackets("(]") == False
    assert is_valid_brackets("([)]") == False
    assert is_valid_brackets("(((") == False
    assert is_valid_brackets(")") == False

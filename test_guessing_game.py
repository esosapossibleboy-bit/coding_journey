from guessing_game import check_guess

def test_guessing_logic():
    # Secret number is 42
    assert check_guess(42, 10) == "Too low!"
    assert check_guess(42, 99) == "Too high!"
    assert check_guess(42, 42) == "You win!"
    
    # Secret number is 7
    assert check_guess(7, 6) == "Too low!"
    assert check_guess(7, 8) == "Too high!"
    assert check_guess(7, 7) == "You win!"
    print("🎲 ALL GUESSING GAME TESTS PASSED! Ready to make it playable!")

test_guessing_logic()

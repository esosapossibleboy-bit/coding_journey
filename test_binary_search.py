from binary_search import find_number

def test_binary_search_engine():
    numbers = [2, 5, 8, 12, 18, 23, 38, 50]

    # Find items at start, middle, and end
    assert find_number(numbers, 2) == 0
    assert find_number(numbers, 18) == 4
    assert find_number(numbers, 50) == 7

    # Missing numbers should cleanly return -1
    assert find_number(numbers, 25) == -1
    assert find_number([], 10) == -1

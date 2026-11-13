from two_sum import find_two_sum

def test_two_sum_interview_cases():
    # Test 1: 2 + 7 = 9 -> indexes [0, 1]
    assert find_two_sum([2, 7, 11, 15], 9) == [0, 1]

    # Test 2: 2 + 4 = 6 -> indexes [1, 2]
    assert find_two_sum([3, 2, 4], 6) == [1, 2]

    # Test 3: Duplicate numbers 3 + 3 = 6 -> indexes [0, 1]
    assert find_two_sum([3, 3], 6) == [0, 1]

    # Test 4: Negative numbers -3 + 8 = 5 -> indexes [0, 2]
    assert find_two_sum([-3, 4, 8], 5) == [0, 2]

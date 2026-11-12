from piggy_bank import count_money, count_big_coins

def test_piggy_bank_system():
    # Test 1: Adding up [1, 5, 10, 25] should equal 41
    assert count_money([1, 5, 10, 25]) == 41
    # Test 2: Adding up [10, 10, 10] should equal 30
    assert count_money([10, 10, 10]) == 30
    # Test 3: An empty piggy bank [] should equal 0
    assert count_money([]) == 0
    
    # Test 4: In, two coins are 10 or bigger (10 and 25)
    assert count_big_coins([1, 5, 10, 25]) == 2
    # Test 5: In, zero coins are 10 or bigger
    assert count_big_coins([1, 2, 5]) == 0
    print("🐷 ALL PIGGY BANK TESTS PASSED! Ready for Day 5!")

test_piggy_bank_system()

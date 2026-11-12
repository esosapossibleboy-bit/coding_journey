from cashier import calculate_total, apply_discount

def test_cashier_system():
    # Test 1: Buying 3 toys that cost $5 each should be $15
    assert calculate_total(5, 3) == 15
    # Test 2: Buying 4 books that cost $10 each should be $40
    assert calculate_total(10, 4) == 40
    # Test 3: $20 total minus a $5 coupon should be $15
    assert apply_discount(20, 5) == 15
    # Test 4: $50 total minus a $12 coupon should be $38
    assert apply_discount(50, 12) == 38
    print("💰 ALL CASHIER TESTS PASSED! Ready for Day 3!")

test_cashier_system()

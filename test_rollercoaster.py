from rollercoaster import check_rider

def test_rollercoaster_gate():
    # Test 1: A kid who is 85 cm tall should be stopped
    assert check_rider(85) == "Too short to ride!"
    # Test 2: A kid who is 99 cm tall should be stopped
    assert check_rider(99) == "Too short to ride!"
    # Test 3: A kid who is exactly 100 cm tall can ride!
    assert check_rider(100) == "Have a fun ride!"
    # Test 4: A kid who is 140 cm tall can ride!
    assert check_rider(140) == "Have a fun ride!"
    print("🎢 ALL ROLLERCOASTER TESTS PASSED! Ready for Day 4!")

test_rollercoaster_gate()

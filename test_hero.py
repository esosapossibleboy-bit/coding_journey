from hero import take_damage, heal_until_full

def test_hero_system():
    # Test 1: Normal damage (100 health - 30 damage = 70 health)
    player1 = {"name": "Aria", "health": 100}
    result1 = take_damage(player1, 30)
    assert result1["health"] == 70

    # Test 2: Huge damage should stop at 0, not go negative!
    player2 = {"name": "Leo", "health": 20}
    result2 = take_damage(player2, 50)
    assert result2["health"] == 0

    # Test 3: Healing with potions of 25 from 40 health (40 -> 65 -> 90 -> 115 -> capped at 100)
    player3 = {"name": "Maya", "health": 40}
    result3 = heal_until_full(player3, 25)
    assert result3["health"] == 100

    # Test 4: Already at 100 health should stay 100
    player4 = {"name": "Zed", "health": 100}
    result4 = heal_until_full(player4, 10)
    assert result4["health"] == 100

    print("⚔️ ALL HERO TESTS PASSED! Week 1 Complete!")

test_hero_system()

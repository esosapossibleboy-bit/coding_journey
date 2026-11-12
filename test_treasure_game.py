from game_engine import move_player, check_treasure

def test_treasure_collision():
    # Test 1: Player is at (1, 1), treasure is at (3, 3) -> Not collected, score stays 0
    collected, new_score = check_treasure((1, 1), (3, 3), 0)
    assert collected == False
    assert new_score == 0

    # Test 2: Player moves onto (3, 3) where treasure is -> Collected! Score becomes 10
    player = move_player(2, 3, "RIGHT", 5)
    collected, new_score = check_treasure(player, (3, 3), 0)
    assert collected == True
    assert new_score == 10

    print("💎 ALL TREASURE COLLISION TESTS PASSED! Ready to play your 2D game!")

test_treasure_collision()

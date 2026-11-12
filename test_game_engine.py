from game_engine import move_player

def test_2d_movement():
    # Start at (2, 2) on a 5x5 map
    assert move_player(2, 2, "RIGHT", 5) == (3, 2)
    assert move_player(2, 2, "LEFT", 5) == (1, 2)
    assert move_player(2, 2, "UP", 5) == (2, 3)
    assert move_player(2, 2, "DOWN", 5) == (2, 1)
    
    # Wall Collision Tests: Player should NOT walk off the map!
    assert move_player(0, 0, "LEFT", 5) == (0, 0)
    assert move_player(0, 0, "DOWN", 5) == (0, 0)
    assert move_player(5, 5, "RIGHT", 5) == (5, 5)
    assert move_player(5, 5, "UP", 5) == (5, 5)
    
    print("🕹️ ALL 2D GAME MOVEMENT TESTS PASSED! Ready for Day 14!")

test_2d_movement()

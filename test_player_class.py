from player_class import Player

def test_player_blueprint():
    p1 = Player("Esosa")
    p2 = Player("Aria")

    assert p1.get_status() == "Esosa has 0 points!"
    assert p2.get_status() == "Aria has 0 points!"

    p1.add_points(25)
    assert p1.get_status() == "Esosa has 25 points!"
    assert p2.get_status() == "Aria has 0 points!"

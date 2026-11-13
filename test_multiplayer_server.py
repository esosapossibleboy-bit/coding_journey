from fastapi.testclient import TestClient
from multiplayer_server import app

client = TestClient(app)

def test_two_player_websocket_broadcast():
    with client.websocket_connect("/ws/Esosa") as ws_esosa:
        join1 = ws_esosa.receive_json()
        assert join1["event"] == "join"
        assert "Esosa" in join1["all_players"]

        with client.websocket_connect("/ws/Aria") as ws_aria:
            # Both players receive Aria's join event
            join2_esosa = ws_esosa.receive_json()
            join2_aria = ws_aria.receive_json()
            assert "Aria" in join2_esosa["all_players"]
            assert "Aria" in join2_aria["all_players"]

            # Esosa moves -> Aria receives Esosa's new (x, y) coordinates immediately!
            ws_esosa.send_json({"x": 120, "y": 240})
            move_esosa = ws_esosa.receive_json()
            move_aria = ws_aria.receive_json()

            assert move_aria["event"] == "move"
            assert move_aria["player"] == "Esosa"
            assert move_aria["all_players"]["Esosa"] == {"x": 120, "y": 240}

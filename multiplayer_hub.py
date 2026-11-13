class GameRoom:
    def __init__(self):
        self.players = {}

    def join_player(self, name):
        self.players[name] = {"x": 0, "y": 0}
        return self.players

    def update_position(self, name, x, y):
        if name in self.players:
            self.players[name] = {"x": x, "y": y}
        return {
            "event": "move",
            "player": name,
            "x": x,
            "y": y,
            "all_players": self.players,
        }

    def remove_player(self, name):
        if name in self.players:
            del self.players[name]
        return self.players

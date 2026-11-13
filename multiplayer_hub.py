import random

class GameRoom:
    def __init__(self):
        self.players = {}
        self.scores = {}
        self.coin = {"x": 200, "y": 150}

    def join_player(self, name):
        self.players[name] = {"x": 50, "y": 50}
        if name not in self.scores:
            self.scores[name] = 0
        return self.players

    def update_position(self, name, x, y):
        if name in self.players:
            self.players[name] = {"x": x, "y": y}

            # Check if player touched the gold coin!
            if abs(x - self.coin["x"]) < 35 and abs(y - self.coin["y"]) < 35:
                self.scores[name] = self.scores.get(name, 0) + 10
                self.coin = {
                    "x": random.randint(40, 440),
                    "y": random.randint(40, 290),
                }

        return {
            "event": "move",
            "player": name,
            "x": x,
            "y": y,
            "all_players": self.players,
            "scores": self.scores,
            "coin": self.coin,
        }

    def remove_player(self, name):
        if name in self.players:
            del self.players[name]
        return self.players

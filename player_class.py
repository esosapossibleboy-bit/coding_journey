class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0

    def add_points(self, amount):
        self.points = self.points + amount

    def get_status(self):
        return self.name + " has " + str(self.points) + " points!"

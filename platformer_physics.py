class HeroPhysics:
    def __init__(self, gravity=5):
        self.y = 0
        self.velocity_y = 0
        self.gravity = gravity

    def jump(self, jump_force=15):
        if self.y == 0:
            self.velocity_y = jump_force

    def step_frame(self):
        self.y = self.y + self.velocity_y
        self.velocity_y = self.velocity_y - self.gravity
        if self.y <= 0:
            self.y = 0
            self.velocity_y = 0

def to_screen_y(physics_y, floor_screen_y=500):
    return floor_screen_y - physics_y

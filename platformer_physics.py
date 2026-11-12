class HeroPhysics:
    def __init__(self, gravity=5):
        self.y = 0
        self.velocity_y = 0
        self.gravity = gravity

    def jump(self, jump_force=15):
        # Only allow jumping if the hero is on the ground
        if self.y == 0:
            self.velocity_y = jump_force

    def step_frame(self):
        # TODO 1: Add velocity to position
        self.y += self.velocity_y

        # TODO 2: Apply gravity
        self.velocity_y -= self.gravity

        # TODO 3: Check if the hero has landed
        if self.y <= 0:
            self.y = 0
            self.velocity_y = 0
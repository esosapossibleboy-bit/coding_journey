from platformer_physics import HeroPhysics, to_screen_y

def test_jump_and_gravity_arc():
    hero = HeroPhysics(gravity=5)
    assert hero.y == 0

    hero.jump(jump_force=15)
    assert hero.velocity_y == 15

    hero.step_frame()
    assert hero.y == 15
    assert hero.velocity_y == 10

    hero.jump(jump_force=15)
    assert hero.velocity_y == 10

    hero.step_frame()
    assert hero.y == 25

    for _ in range(10):
        hero.step_frame()
    assert hero.y == 0
    assert hero.velocity_y == 0

def test_screen_coordinates():
    # Standing on floor (height 0) -> screen Y is 500
    assert to_screen_y(0, floor_screen_y=500) == 500
    # Jumping 120 pixels up -> screen Y moves UP to 380
    assert to_screen_y(120, floor_screen_y=500) == 380

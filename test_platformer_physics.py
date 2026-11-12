from platformer_physics import HeroPhysics

def test_jump_and_gravity_arc():
    hero = HeroPhysics(gravity=5)
    assert hero.y == 0

    # 1. Press Jump on the ground -> velocity becomes 15
    hero.jump(jump_force=15)
    assert hero.velocity_y == 15

    # 2. Frame 1: moves up by 15 (y=15), gravity reduces velocity to 10
    hero.step_frame()
    assert hero.y == 15
    assert hero.velocity_y == 10

    # 3. Try double-jumping mid-air -> should be ignored!
    hero.jump(jump_force=15)
    assert hero.velocity_y == 10

    # 4. Frame 2: y becomes 25, velocity becomes 5
    hero.step_frame()
    assert hero.y == 25

    # 5. Advance frames until hero lands safely back on the ground (y == 0)
    for _ in range(10):
        hero.step_frame()
    assert hero.y == 0
    assert hero.velocity_y == 0

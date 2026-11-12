const test = require("node:test");
const assert = require("node:assert");
const { checkCollision } = require("./arcade_logic");

test("Arcade Game Hitbox Collision Detection", () => {
    // 1. Obstacle is far away (x = 500), hero on ground (y = 260) -> Safe!
    assert.strictEqual(checkCollision(260, 500), false);

    // 2. Obstacle is right under hero (x = 280), hero is on ground (y = 260) -> CRASH!
    assert.strictEqual(checkCollision(260, 280), true);

    // 3. Obstacle is right under hero (x = 280), hero jumped high (y = 180) -> Safe!
    assert.strictEqual(checkCollision(180, 280), false);
});

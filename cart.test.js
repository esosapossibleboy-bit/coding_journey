const test = require("node:test");
const assert = require("node:assert");
const { calculateCartTotal } = require("./cart");

test("Web & Mobile Cart Calculator", () => {
    // 3 items at $10 each + $2 tax = $32
    assert.strictEqual(calculateCartTotal(10, 3, 2), 32);
    
    // 2 items at $25 each + $5 tax = $55
    assert.strictEqual(calculateCartTotal(25, 2, 5), 55);
});

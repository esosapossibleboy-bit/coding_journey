const test = require("node:test");
const assert = require("node:assert");
const { getTopAppNames } = require("./app_store");

test("App Store Search Filter", () => {
    const sampleApps = [
        { name: "SuperGame", rating: 4.9 },
        { name: "SlowBrowser", rating: 2.5 },
        { name: "SmartAI", rating: 4.7 },
        { name: "CrashNote", rating: 3.1 }
    ];

    // Filter apps rated 4.5 or higher -> should return ["SuperGame", "SmartAI"]
    assert.deepStrictEqual(getTopAppNames(sampleApps, 4.5), ["SuperGame", "SmartAI"]);

    // Filter apps rated 4.8 or higher -> should return ["SuperGame"]
    assert.deepStrictEqual(getTopAppNames(sampleApps, 4.8), ["SuperGame"]);
});

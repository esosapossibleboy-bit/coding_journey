const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const babel = require("@babel/core");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");

// Compile UserCard.jsx using classic React runtime so require() works cleanly
const jsxCode = fs.readFileSync("./UserCard.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(require, moduleObj, moduleObj.exports);
const { UserCard } = moduleObj.exports;

test("React UserCard Component renders props cleanly", () => {
    // Test 1: Online user
    const html1 = renderToStaticMarkup(
        React.createElement(UserCard, { name: "Esosa", role: "Full-Stack Developer", isOnline: true })
    );
    assert.ok(html1.includes("<h2>Esosa</h2>"));
    assert.ok(html1.includes("<p>Role: Full-Stack Developer</p>"));
    assert.ok(html1.includes("🟢 Online"));

    // Test 2: Offline user
    const html2 = renderToStaticMarkup(
        React.createElement(UserCard, { name: "Aria", role: "AI Engineer", isOnline: false })
    );
    assert.ok(html2.includes("<h2>Aria</h2>"));
    assert.ok(html2.includes("⚪ Offline"));
});

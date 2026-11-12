const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const babel = require("@babel/core");
const { JSDOM } = require("jsdom");

// Set up an invisible browser environment for React Testing Library
const dom = new JSDOM("<!doctype html><html><body></body></html>");
global.window = dom.window;
global.document = dom.window.document;

const React = require("react");
const { render, fireEvent } = require("@testing-library/react");

// Compile LikeButton.jsx
const jsxCode = fs.readFileSync("./LikeButton.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(require, moduleObj, moduleObj.exports);
const { LikeButton } = moduleObj.exports;

test("Interactive React LikeButton updates state on click", () => {
    const { getByRole } = render(React.createElement(LikeButton, { initialLikes: 5 }));
    const button = getByRole("button");

    // Starts at 5 likes
    assert.strictEqual(button.textContent, "❤️ Likes: 5");

    // Simulate two real user clicks!
    fireEvent.click(button);
    assert.strictEqual(button.textContent, "❤️ Likes: 6");

    fireEvent.click(button);
    assert.strictEqual(button.textContent, "❤️ Likes: 7");
});

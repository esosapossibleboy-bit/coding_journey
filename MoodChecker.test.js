const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const babel = require("@babel/core");
const { JSDOM } = require("jsdom");

const dom = new JSDOM("<!doctype html><html><body></body></html>");
global.window = dom.window;
global.document = dom.window.document;

const React = require("react");
const { render, fireEvent, waitFor } = require("@testing-library/react");

// Compile MoodChecker.jsx
const jsxCode = fs.readFileSync("./MoodChecker.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(require, moduleObj, moduleObj.exports);
const { MoodChecker } = moduleObj.exports;

test("React MoodChecker types text, calls API, and displays mood", async () => {
    // Mock the Python FastAPI backend response
    let calledUrl = "";
    global.fetch = async (url) => {
        calledUrl = url;
        return {
            json: async () => ({ text: "I love React", mood: "Positive" })
        };
    };

    const { getByPlaceholderText, getByRole, getByText } = render(
        React.createElement(MoodChecker)
    );

    // 1. User types into the input box
    const input = getByPlaceholderText("Type your message");
    fireEvent.change(input, { target: { value: "I love React" } });

    // 2. User clicks Analyze button
    fireEvent.click(getByRole("button"));

    // 3. Verify React called the right Python FastAPI endpoint and updated the UI!
    await waitFor(() => {
        assert.strictEqual(calledUrl, "/analyze?text=I%20love%20React");
        assert.ok(getByText("Detected Mood: Positive"));
    });
});

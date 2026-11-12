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

// Lightweight React Native simulator for fast automated testing
const mockReactNative = {
    View: ({ children }) => React.createElement("div", null, children),
    Text: ({ children }) => React.createElement("span", null, children),
    TextInput: ({ placeholder, value, onChangeText }) =>
        React.createElement("input", {
            placeholder,
            value,
            onChange: (e) => onChangeText(e.target.value)
        }),
    Pressable: ({ onPress, children }) =>
        React.createElement("button", { onClick: onPress }, children)
};

function customRequire(mod) {
    if (mod === "react-native") return mockReactNative;
    return require(mod);
}

// Compile ScoreScreen.jsx
const jsxCode = fs.readFileSync("./ScoreScreen.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(customRequire, moduleObj, moduleObj.exports);
const { ScoreScreen } = moduleObj.exports;

test("React Native ScoreScreen submits player score via POST API", async () => {
    let sentBody = null;
    global.fetch = async (url, options) => {
        if (url === "/scores" && options.method === "POST") {
            sentBody = JSON.parse(options.body);
            return {
                json: async () => ({ status: "saved", player: sentBody.player })
            };
        }
    };

    const { getByPlaceholderText, getByRole, getByText } = render(
        React.createElement(ScoreScreen, { points: 850 })
    );

    // 1. Phone user types their name
    fireEvent.change(getByPlaceholderText("Enter player name"), {
        target: { value: "Esosa" }
    });

    // 2. Phone user taps "Submit Score"
    fireEvent.click(getByRole("button"));

    // 3. Verify POST body and updated mobile UI status!
    await waitFor(() => {
        assert.deepStrictEqual(sentBody, { player: "Esosa", points: 850 });
        assert.ok(getByText("Saved score for Esosa!"));
    });
});

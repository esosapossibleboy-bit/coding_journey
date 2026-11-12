const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const babel = require("@babel/core");
const { JSDOM } = require("jsdom");

const dom = new JSDOM("<!doctype html><html><body></body></html>");
global.window = dom.window;
global.document = dom.window.document;

const React = require("react");
const { render, waitFor } = require("@testing-library/react");

// Lightweight React Native simulator including FlatList
const mockReactNative = {
    View: ({ children }) => React.createElement("div", null, children),
    Text: ({ children }) => React.createElement("span", null, children),
    FlatList: ({ data, keyExtractor, renderItem }) =>
        React.createElement(
            "ul",
            null,
            data.map((item, index) =>
                React.createElement(
                    "li",
                    { key: keyExtractor(item, index) },
                    renderItem({ item, index })
                )
            )
        )
};

function customRequire(mod) {
    if (mod === "react-native") return mockReactNative;
    return require(mod);
}

// Compile LeaderboardScreen.jsx
const jsxCode = fs.readFileSync("./LeaderboardScreen.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(customRequire, moduleObj, moduleObj.exports);
const { LeaderboardScreen } = moduleObj.exports;

test("React Native LeaderboardScreen fetches and renders FlatList scores", async () => {
    global.fetch = async (url) => {
        if (url === "/scores") {
            return {
                json: async () => ({
                    leaderboard: [
                        ["Zed", 750],
                        ["Esosa", 500]
                    ]
                })
            };
        }
    };

    const { getByText } = render(React.createElement(LeaderboardScreen));

    // Verify useEffect fetched the scores and FlatList rendered both rows!
    await waitFor(() => {
        assert.ok(getByText("Zed: 750 pts"));
        assert.ok(getByText("Esosa: 500 pts"));
    });
});

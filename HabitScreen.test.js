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
        React.createElement("button", { onClick: onPress }, children),
    FlatList: ({ data, keyExtractor, renderItem }) =>
        React.createElement(
            "ul",
            null,
            data.map((item) =>
                React.createElement("li", { key: keyExtractor(item) }, renderItem({ item }))
            )
        )
};

function customRequire(mod) {
    if (mod === "react-native") return mockReactNative;
    return require(mod);
}

const jsxCode = fs.readFileSync("./HabitScreen.jsx", "utf8");
const compiled = babel.transformSync(jsxCode, {
    presets: [["@babel/preset-react", { runtime: "classic" }]]
});
const moduleObj = { exports: {} };
new Function("require", "module", "exports", compiled.code)(customRequire, moduleObj, moduleObj.exports);
const { HabitScreen } = moduleObj.exports;

test("React Native HabitScreen loads, creates, and completes habits", async () => {
    let dbHabits = [{ id: 1, name: "Code Daily", streak: 3 }];

    global.fetch = async (url, options = {}) => {
        if (url === "/habits" && !options.method) {
            return { json: async () => ({ habits: dbHabits }) };
        }
        if (url === "/habits" && options.method === "POST") {
            const body = JSON.parse(options.body);
            dbHabits = [...dbHabits, { id: 2, name: body.name, streak: 0 }];
            return { json: async () => ({ habits: dbHabits }) };
        }
        if (url === "/habits/1/complete" && options.method === "POST") {
            dbHabits = dbHabits.map((h) => (h.id === 1 ? { ...h, streak: h.streak + 1 } : h));
            return { json: async () => ({ streak: 4, habits: dbHabits }) };
        }
    };

    const { getByText, getByPlaceholderText, getAllByText } = render(
        React.createElement(HabitScreen)
    );

    // 1. Initial load shows existing habit
    await waitFor(() => {
        assert.ok(getByText("Code Daily — 3 day streak"));
    });

    // 2. Add a new habit
    fireEvent.change(getByPlaceholderText("New habit name"), { target: { value: "Read Docs" } });
    fireEvent.click(getByText("Add Habit"));

    await waitFor(() => {
        assert.ok(getByText("Read Docs — 0 day streak"));
    });

    // 3. Tap "Complete Today" on the first habit -> streak jumps from 3 to 4!
        // 3. Tap "Complete Today" on the first habit -> streak jumps from 3 to 4!
    fireEvent.click(getAllByText("Complete Today")[0]);


    await waitFor(() => {
        assert.ok(getByText("Code Daily — 4 day streak"));
    });
});

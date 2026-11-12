const React = require("react");

function MoodChecker() {
    const [text, setText] = React.useState("");
    const [mood, setMood] = React.useState("Waiting...");

    async function handleAnalyze() {
        const response = await fetch("/analyze?text=" + encodeURIComponent(text));
        const data = await response.json();
        setMood(data.mood);
    }

    return (
        <div>
            <input
                placeholder="Type your message"
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            <button onClick={handleAnalyze}>Analyze</button>
            <p>Detected Mood: {mood}</p>
        </div>
    );
}

module.exports = { MoodChecker };
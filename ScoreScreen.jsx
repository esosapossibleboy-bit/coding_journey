const React = require("react");
const { View, Text, TextInput, Pressable } = require("react-native");

function ScoreScreen({ points = 500 }) {
    const [player, setPlayer] = React.useState("");
    const [status, setStatus] = React.useState("Ready to submit");

    async function handleSubmit() {
        const response = await fetch("/scores", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ player: player, points: points })
        });
        const data = await response.json();
        setStatus("Saved score for " + data.player + "!");
    }

    return (
        <View>
            <Text>Your Score: {points}</Text>
            <TextInput
                placeholder="Enter player name"
                value={player}
                onChangeText={(text) => setPlayer(text)}
            />
            <Pressable onPress={handleSubmit}>
                <Text>Submit Score</Text>
            </Pressable>
            <Text>{status}</Text>
        </View>
    );
}

module.exports = { ScoreScreen };

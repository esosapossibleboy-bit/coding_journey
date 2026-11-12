
const React = require("react");
const { View, Text, FlatList } = require("react-native");

function LeaderboardScreen() {
    const [scores, setScores] = React.useState([]);

    React.useEffect(() => {
        async function loadScores() {
            try {
                // TODO 1: Fetch scores and parse JSON
                const response = await fetch("/scores");
                const data = await response.json();

                // TODO 2: Save leaderboard into state
                setScores(data.leaderboard);
            } catch (error) {
                console.error("Failed to load scores:", error);
            }
        }

        loadScores();
    }, []);

    return (
        <View>
            <Text>🏆 Top Players</Text>
            <FlatList
                data={scores}
                keyExtractor={(item, index) => String(index)}
                renderItem={({ item }) => (
                    <Text>{item[0]}: {item[1]} pts</Text>
                )}
            />
        </View>
    );
}

module.exports = { LeaderboardScreen };

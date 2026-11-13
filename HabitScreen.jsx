const React = require("react");
const { View, Text, TextInput, Pressable, FlatList } = require("react-native");

function HabitScreen() {
    const [habits, setHabits] = React.useState([]);
    const [newHabit, setNewHabit] = React.useState("");

    React.useEffect(() => {
        async function loadHabits() {
            const res = await fetch("/habits");
            const data = await res.json();
            setHabits(data.habits);
        }
        loadHabits();
    }, []);

    async function handleAddHabit() {
        const res = await fetch("/habits", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newHabit })
        });
        const data = await res.json();
        setHabits(data.habits);
        setNewHabit("");
    }

    async function handleComplete(habitId) {
        const res = await fetch(`/habits/${habitId}/complete`, {
            method: "POST"
        });
        const data = await res.json();
        setHabits(data.habits);
    }

    return (
        <View>
            <Text>🔥 Daily Habit Tracker</Text>
            <TextInput
                placeholder="New habit name"
                value={newHabit}
                onChangeText={(text) => setNewHabit(text)}
            />
            <Pressable onPress={handleAddHabit}>
                <Text>Add Habit</Text>
            </Pressable>

            <FlatList
                data={habits}
                keyExtractor={(item) => String(item.id)}
                renderItem={({ item }) => (
                    <View>
                        <Text>{item.name} — {item.streak} day streak</Text>
                        <Pressable onPress={() => handleComplete(item.id)}>
                            <Text>Complete Today</Text>
                        </Pressable>
                    </View>
                )}
            />
        </View>
    );
}

module.exports = { HabitScreen };

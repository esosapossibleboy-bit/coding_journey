const React = require("react");

function LikeButton({ initialLikes = 0 }) {
    const [likes, setLikes] = React.useState(initialLikes);

    return (
        <button onClick={() => setLikes(likes + 1)}>
            ❤️ Likes: {likes}
        </button>
    );
}

module.exports = { LikeButton };
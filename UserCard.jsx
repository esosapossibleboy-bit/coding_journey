const React = require("react");

function UserCard({ name, role, isOnline }) {
    return (
        <div>
            <h2>{name}</h2>
            <p>Role: {role}</p>
            <span>{isOnline ? "🟢 Online" : "⚪ Offline"}</span>
        </div>
    );
}

module.exports = { UserCard };
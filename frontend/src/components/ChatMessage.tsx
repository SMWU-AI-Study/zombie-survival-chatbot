interface ChatMessageProps {
    role: "user" | "gm";
    content: string;
}

function ChatMessage({ role, content }: ChatMessageProps) {
    const isUser = role === "user";

    return (
        <div
            className={`message-row ${
                isUser ? "message-user" : "message-gm"
            }`}
        >
            <div className="message-content">
                <span className="message-label">
                    {isUser ? "YOU" : "GM · SURVIVAL SYSTEM"}
                </span>

                <div className="message-bubble">
                    <p>{content}</p>
                </div>
            </div>
        </div>
    );
}

export default ChatMessage;
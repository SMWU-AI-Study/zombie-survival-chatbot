interface ChatMessageProps {
  role: "user" | "gm";
  content: string;
}

function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div>
      <strong>{isUser ? "나" : "GM"}</strong>
      <p>{content}</p>
    </div>
  );
}

export default ChatMessage;
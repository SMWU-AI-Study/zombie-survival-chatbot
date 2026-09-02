import { useState } from "react";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";
import { sendChat, getProfile } from "../services/api";
import type {
    ChatMessageType,
    ChatResponse,
    SurvivorProfile,
} from "../types";

interface ChatPageProps {
    firstScenario: ChatResponse;
    onProfileLoaded: (profile: SurvivorProfile) => void;
}

function ChatPage({
    firstScenario,
    onProfileLoaded,
}: ChatPageProps) {
    const [messages, setMessages] = useState<ChatMessageType[]>([
        {
            role: "gm",
            content: firstScenario.reply,
        },
    ]);

    const [isLoading, setIsLoading] = useState(false);
    const [isComplete, setIsComplete] = useState(false);

    const handleSend = async (message: string) => {
        try {
            setIsLoading(true);

            setMessages((prev) => [
                ...prev,
                {
                    role: "user",
                    content: message,
                },
            ]);

            const response = await sendChat(message);

            if (response.step === "complete") {
                setIsComplete(true);
            }

            setMessages((prev) => [
                ...prev,
                {
                    role: "gm",
                    content: response.reply,
                },
            ]);
        } catch (error) {
            console.error(error);
            alert("메시지를 전송하는 중 오류가 발생했습니다.");
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleViewProfile = async () => {
        try {
            setIsLoading(true);

            const profile = await getProfile();

            onProfileLoaded(profile);
        } catch (error) {
            console.error(error);
            alert("생존 결과를 불러오는 중 오류가 발생했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main>
            <h1>Zombie Survival Test</h1>

            <section>
                {messages.map((message, index) => (
                    <ChatMessage
                        key={index}
                        role={message.role}
                        content={message.content}
                    />
                ))}
            </section>

            {isLoading && <p>GM이 상황을 판단하고 있습니다...</p>}

            {isComplete ? (
                <button
                    type="button"
                    onClick={handleViewProfile}
                    disabled={isLoading}
                >
                    {isLoading ? "결과 분석 중..." : "나의 생존 결과 보기"}
                </button>
            ) : (
                <ChatInput onSend={handleSend} disabled={isLoading} />
            )}
        </main>
    );
}

export default ChatPage;
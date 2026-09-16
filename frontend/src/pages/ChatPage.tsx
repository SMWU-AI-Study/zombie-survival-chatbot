import { useEffect, useRef, useState } from "react";
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
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages, isLoading]);

    const [currentScenario, setCurrentScenario] = useState(
        firstScenario.scenario_id ?? 1
    );

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

            if (response.scenario_id) {
                setCurrentScenario(response.scenario_id);
            }

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
        <main className="chat-page">
            <header className="chat-header">
                <div>
                    <span className="chat-eyebrow">SURVIVAL SESSION</span>
                    <h1>ZOMBIE SURVIVAL TEST</h1>
                </div>

                <div className="scenario-progress">
                    <span>CASE</span>
                    <strong>
                        {String(currentScenario).padStart(2, "0")}
                        <small> / 05</small>
                    </strong>
                </div>
            </header>

            <div className="chat-divider" />

            <section className="chat-messages">
                {messages.map((message, index) => (
                    <ChatMessage
                        key={index}
                        role={message.role}
                        content={message.content}
                    />
                ))}

                {isLoading && !isComplete && (
                    <div className="gm-loading">
                        <span className="loading-dot" />
                        GM이 상황을 판단하고 있습니다...
                    </div>
                )}
                <div ref={messagesEndRef} />
                
            </section>

            <div className="chat-bottom">
                {isComplete ? (
                    <div className="complete-area">
                        <span>SURVIVAL TEST COMPLETE</span>

                        <button
                            className="result-button"
                            type="button"
                            onClick={handleViewProfile}
                            disabled={isLoading}
                        >
                            {isLoading
                                ? "생존 데이터 분석 중..."
                                : "나의 생존 결과 보기 →"}
                        </button>
                    </div>
                ) : (
                    <ChatInput
                        onSend={handleSend}
                        disabled={isLoading}
                    />
                )}
            </div>
        </main>
    );
}

export default ChatPage;
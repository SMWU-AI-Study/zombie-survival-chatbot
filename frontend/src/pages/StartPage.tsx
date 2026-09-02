import { useState } from "react";
import { resetScenario, sendChat } from "../services/api";
import type { ChatResponse } from "../types";

interface StartPageProps {
    onStart: (firstScenario: ChatResponse) => void;
}

function StartPage({ onStart }: StartPageProps) {
    const [isLoading, setIsLoading] = useState(false);

    const handleStart = async () => {
        try {
            setIsLoading(true);

            await resetScenario();

            const firstScenario = await sendChat("생존 테스트 시작");

            onStart(firstScenario);
        } catch (error) {
            console.error(error);
            alert("게임을 시작하는 중 오류가 발생했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main>
            <h1>Zombie Survival Test</h1>

            <p>
                좀비 아포칼립스 상황에서 당신은 어떤 생존자가 될까요?
            </p>

            <button
                type="button"
                onClick={handleStart}
                disabled={isLoading}
            >
                {isLoading ? "시작 중..." : "생존 테스트 시작"}
            </button>
        </main>
    );
}

export default StartPage;
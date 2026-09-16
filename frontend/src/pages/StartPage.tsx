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
        <main className="start-page">
            <div className="start-card">
                <span className="day-label">DAY 0 · OUTBREAK</span>

                <div className="start-title">
                    <span>ZOMBIE SURVIVAL</span>
                    <h1>TEST</h1>
                </div>

                <p className="start-description">
                    좀비 사태가 발생했습니다.
                    <br />
                    당신은 어떤 선택으로 살아남을 수 있을까요?
                </p>

                <div className="trait-preview">
                    <span>판단력</span>
                    <span>신중함</span>
                    <span>위험 감수</span>
                    <span>협동성</span>
                    <span>공감성</span>
                    <span>행동력</span>
                </div>

                <button
                    className="start-button"
                    type="button"
                    onClick={handleStart}
                    disabled={isLoading}
                >
                    {isLoading ? "생존 환경 분석 중..." : "생존 테스트 시작 →"}
                </button>

                <p className="start-meta">
                    5 SCENARIOS · AI GAME MASTER
                </p>
            </div>
        </main>
    );
}

export default StartPage;
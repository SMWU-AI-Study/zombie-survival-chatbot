import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel


load_dotenv()

app = FastAPI(
    title="Zombie Survival Chatbot API",
    description="LLM-based personalized zombie apocalypse survival chatbot",
)

api_key = os.getenv("GEMINI_API_KEY")
USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"

if not api_key and not USE_MOCK:
    raise RuntimeError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

client = genai.Client(api_key=api_key) if api_key else None


SYSTEM_PROMPT = """
너는 좀비 아포칼립스 생존 성향 테스트를 진행하는 GM(Game Master)이다.

[역할]
- 사용자에게 현실적인 좀비 아포칼립스 상황을 제시한다.
- 사용자는 선택지가 아닌 자연어로 자유롭게 행동을 입력한다.
- 사용자의 답변을 이해하고 그 행동에 맞춰 상황을 자연스럽게 이어간다.
- 필요한 경우 사용자의 판단을 더 파악할 수 있도록 추가 질문을 한다.

[진행 규칙]
- 항상 좀비 아포칼립스 세계관을 유지한다.
- 한 번에 하나의 상황 또는 질문만 제시한다.
- 사용자의 행동을 임의로 결정하지 않는다.
- 사용자가 하지 않은 행동을 했다고 가정하지 않는다.
- 생존 성향 점수나 최종 유형은 대화 중 공개하지 않는다.
- 답변은 지나치게 길지 않게 작성한다.
- 정답이 하나인 문제처럼 진행하지 않고, 사용자의 선택에 따라 상황을 유연하게 이어간다.

현재 단계에서는 최종 Survivor Profile을 생성하지 않고,
자연스럽게 생존 상황을 진행하는 것에 집중한다.
"""

def load_scenarios():
    with open("scenarios.json", "r", encoding="utf-8") as file:
        return json.load(file)

scenario_data = load_scenarios()
current_scenario_index = 0
current_step = 0

scenario_answers = []


def get_current_scenario():
    return scenario_data["scenarios"][current_scenario_index]

def create_chat_session():
    if USE_MOCK:
        return None

    return client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )


chat_session = create_chat_session()

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Zombie Survival Chatbot API",
        "mode": "mock" if USE_MOCK else "gemini"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    global current_step

    try:
        if USE_MOCK:
            scenario = get_current_scenario()

            # 생존 테스트 시작
            if current_step == 0:
                current_step = 1

                return {
                    "reply": scenario["step1"]["situation"],
                    "scenario_id": scenario["id"],
                    "step": 1,
                    "mode": "mock"
                }

            # STEP 1 사용자 답변 저장
            if current_step == 1:
                scenario_answers.append({
                    "scenario_id": scenario["id"],
                    "step": 1,
                    "answer": request.message
                })

                current_step = 2

                return {
                    "reply": scenario["step2"]["core_event"],
                    "scenario_id": scenario["id"],
                    "step": 2,
                    "mode": "mock"
                }
            

            # STEP 2 사용자 답변 저장
            if current_step == 2:
                scenario_answers.append({
                    "scenario_id": scenario["id"],
                    "step": 2,
                    "answer": request.message
                })

                current_step = 3

                return {
                    "reply": "CASE 1이 종료되었습니다.",
                    "scenario_id": scenario["id"],
                    "step": "complete",
                    "mode": "mock"
                }
            
            # 현재 시나리오 종료 후 추가 요청 처리
            if current_step >= 3:
                return {
                    "reply": "현재 시나리오가 종료되었습니다.",
                    "scenario_id": scenario["id"],
                    "step": "complete",
                    "mode": "mock"
                }

        response = chat_session.send_message(request.message)

        return {
            "reply": response.text,
            "mode": "gemini"
        }

    except Exception as e:
        print(f"Chat Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/reset")
def reset_chat():
    global chat_session
    global current_scenario_index
    global current_step
    global scenario_answers

    current_scenario_index = 0
    current_step = 0
    scenario_answers = []

    if not USE_MOCK:
        chat_session = create_chat_session()

    return {
        "message": "Chat history reset successfully",
        "mode": "mock" if USE_MOCK else "gemini"
    }

@app.get("/scenario")
def get_scenario():
    return scenario_data

@app.get("/answers")
def get_answers():
    return {
        "answers": scenario_answers
    }
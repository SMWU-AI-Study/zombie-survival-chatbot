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

def generate_step2(user_answer: str, scenario: dict):
    prompt = f"""
사용자가 좀비 생존 시나리오의 첫 번째 상황에서 다음과 같이 행동했다.

[사용자의 행동]
{user_answer}

[다음 상황에서 반드시 포함해야 하는 핵심 사건]
{scenario["step2"]["core_event"]}

[이 단계의 목적]
{scenario["step2"]["goal"]}

사용자의 행동에 자연스럽게 이어지도록 다음 상황을 작성하라.

규칙:
- 사용자의 행동을 무시하거나 되돌리지 않는다.
- 사용자가 하지 않은 행동을 했다고 가정하지 않는다.
- 핵심 사건은 반드시 모두 유지한다.
- 핵심 사건 자체를 변경하지 않는다.
- 좀비 아포칼립스 GM처럼 상황을 자연스럽게 묘사한다.
- 마지막에는 사용자가 다음 행동을 자유롭게 답할 수 있는 질문을 하나 한다.
- 선택지를 제시하지 않는다.
- 3~5문장 정도로 간결하게 작성한다.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return response.text

def generate_next_scenario(previous_scenario: dict, next_scenario: dict):
    previous_answers = [
        answer
        for answer in scenario_answers
        if answer["scenario_id"] == previous_scenario["id"]
    ]

    answers_text = "\n".join(
        f'STEP {answer["step"]}: {answer["answer"]}'
        for answer in previous_answers
    )

    prompt = f"""
사용자는 하나의 연속된 좀비 아포칼립스 생존 시나리오를 진행하고 있다.

[이전 시나리오]
{previous_scenario["title"]}

[이전 시나리오에서 사용자가 한 행동]
{answers_text}

[다음 시나리오]
{next_scenario["title"]}

[다음 시나리오에서 반드시 발생해야 하는 핵심 사건]
{next_scenario["step1"]["core_event"]}

[이 단계의 목적]
{next_scenario["step1"]["goal"]}

이전 시나리오에서 사용자가 했던 행동을 반영하여
하나의 이야기가 계속 이어지는 것처럼 다음 상황을 작성하라.

규칙:
- 이전 사용자의 선택을 임의로 변경하지 않는다.
- 사용자가 하지 않은 행동을 했다고 가정하지 않는다.
- 이전 선택은 이야기의 연결에만 활용한다.
- 다음 시나리오의 핵심 사건은 반드시 모두 유지한다.
- 핵심 사건의 난이도나 조건 자체를 변경하지 않는다.
- 자연스러운 시간의 흐름이나 장소 이동을 추가해도 된다.
- 좀비 아포칼립스 GM의 말투를 유지한다.
- 마지막에는 사용자가 다음 행동을 자유롭게 답할 수 있는 질문을 하나 한다.
- 선택지를 강제로 제시하지 않는다.
- 3~5문장 정도로 간결하게 작성한다.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return response.text

def get_mock_next_scenario(next_scenario: dict):
    return next_scenario["step1"]["core_event"]

def create_chat_session():
    if USE_MOCK:
        return None

    return client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Zombie Survival Chatbot API",
        "mode": "mock" if USE_MOCK else "gemini",
        "version": "scenario-v2"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    global current_step
    global current_scenario_index

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
            

            # STEP 2 사용자 답변 저장 + 다음 CASE로 이동
            if current_step == 2:
                scenario_answers.append({
                    "scenario_id": scenario["id"],
                    "step": 2,
                    "answer": request.message
                })

                # 다음 CASE가 있는 경우
                if current_scenario_index + 1 < len(scenario_data["scenarios"]):
                    current_scenario_index += 1
                    current_step = 1

                    next_scenario = get_current_scenario()

                    return {
                        "reply": get_mock_next_scenario(next_scenario),
                        "scenario_id": next_scenario["id"],
                        "step": 1,
                        "mode": "mock"
                    }

                # 마지막 CASE까지 완료한 경우
                current_step = 3

                return {
                    "reply": "모든 생존 시나리오가 종료되었습니다.",
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
            

        # 실제 Gemini 모드
        scenario = get_current_scenario()

        # 생존 테스트 시작
        if current_step == 0:
            current_step = 1

            return {
                "reply": (
                    f'{scenario["step1"]["situation"]} '
                    "이 상황에서 어떻게 행동하시겠습니까?"
                ),
                "scenario_id": scenario["id"],
                "step": 1,
                "mode": "gemini"
            }

        # STEP 1 사용자 답변 저장 + STEP 2 자연스럽게 생성
        if current_step == 1:
            scenario_answers.append({
                "scenario_id": scenario["id"],
                "step": 1,
                "answer": request.message
            })

            reply = generate_step2(
                user_answer=request.message,
                scenario=scenario
            )

            current_step = 2

            return {
                "reply": reply,
                "scenario_id": scenario["id"],
                "step": 2,
                "mode": "gemini"
            }

        # STEP 2 사용자 답변 저장 + 다음 CASE로 이동
        if current_step == 2:
            scenario_answers.append({
                "scenario_id": scenario["id"],
                "step": 2,
                "answer": request.message
            })

            # 다음 CASE가 있는 경우
            if current_scenario_index + 1 < len(scenario_data["scenarios"]):
                previous_scenario = scenario

                current_scenario_index += 1
                current_step = 1

                next_scenario = get_current_scenario()

                reply = generate_next_scenario(
                    previous_scenario=previous_scenario,
                    next_scenario=next_scenario
                )

                return {
                    "reply": reply,
                    "scenario_id": next_scenario["id"],
                    "step": 1,
                    "mode": "gemini"
                }

            # 마지막 CASE까지 완료한 경우
            current_step = 3

            return {
                "reply": "모든 생존 시나리오가 종료되었습니다.",
                "scenario_id": scenario["id"],
                "step": "complete",
                "mode": "gemini"
            }

        if current_step >= 3:
            return {
                "reply": "현재 시나리오가 종료되었습니다.",
                "scenario_id": scenario["id"],
                "step": "complete",
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
    global current_scenario_index
    global current_step
    global scenario_answers

    current_scenario_index = 0
    current_step = 0
    scenario_answers = []

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
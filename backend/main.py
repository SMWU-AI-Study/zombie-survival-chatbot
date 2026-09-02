import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from services.gemini_service import (
    generate_step2,
    generate_next_scenario,
    generate_profile,
)


load_dotenv()

app = FastAPI(
    title="Zombie Survival Chatbot API",
    description="LLM-based personalized zombie apocalypse survival chatbot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"

if not api_key and not USE_MOCK:
    raise RuntimeError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

client = genai.Client(api_key=api_key) if api_key else None


def load_scenarios():
    with open("scenarios.json", "r", encoding="utf-8") as file:
        return json.load(file)

scenario_data = load_scenarios()
current_scenario_index = 0
current_step = 0

scenario_answers = []


def get_current_scenario():
    return scenario_data["scenarios"][current_scenario_index]


def get_mock_next_scenario(next_scenario: dict):
    return next_scenario["step1"]["core_event"]


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
                client=client,
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
                    client=client,
                    previous_scenario=previous_scenario,
                    next_scenario=next_scenario,
                    scenario_answers=scenario_answers
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

@app.get("/profile")
def get_profile():
    try:
        if USE_MOCK:
            return {
                "survivor_type": "신중한 전략가",
                "judgment": 85,
                "caution": 90,
                "risk_tolerance": 35,
                "cooperation": 70,
                "empathy": 75,
                "action": 60,
                "recommended_role": "전략 및 물자 관리",
                "strength": "위험 요소를 충분히 분석한 뒤 행동한다.",
                "weakness": "즉각적인 결단이 필요한 상황에서는 대응이 늦어질 수 있다.",
                "mode": "mock"
            }

        profile_text = generate_profile(
            client=client,
            scenario_answers=scenario_answers
        )
        profile = json.loads(profile_text)

        profile["mode"] = "gemini"

        return profile

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini의 프로필 응답을 JSON으로 변환하지 못했습니다."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel


# .env 파일의 환경변수 불러오기
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="Zombie Survival Chatbot API",
    description="LLM-based personalized zombie apocalypse survival chatbot",
)

# Gemini API Key 불러오기
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

# Gemini Client 생성
client = genai.Client(api_key=api_key)


# /chat 요청 데이터 형식
class ChatRequest(BaseModel):
    message: str


# 기본 서버 확인용 API
@app.get("/")
def root():
    return {"message": "Zombie Survival Chatbot API"}


# Gemini 채팅 API
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.message,
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        print(f"Gemini API Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
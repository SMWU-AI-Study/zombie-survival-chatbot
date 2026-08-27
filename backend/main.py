import os

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

if not api_key:
    raise RuntimeError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

client = genai.Client(api_key=api_key)

# Multi-turn 채팅 세션 생성
chat_session = client.chats.create(
    model="gemini-3.6-flash"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "Zombie Survival Chatbot API"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = chat_session.send_message(request.message)

        return {
            "reply": response.text
        }

    except Exception as e:
        print(f"Gemini API Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.post("/reset")
def reset_chat():
    global chat_session

    chat_session = client.chats.create(
        model="gemini-3.6-flash"
    )

    return {
        "message": "Chat history reset successfully"
    }
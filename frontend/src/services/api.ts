import type {
  ChatResponse,
  SurvivorProfile,
} from "../types";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function resetScenario() {
  const response = await fetch(`${API_BASE_URL}/reset`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("시나리오 초기화에 실패했습니다.");
  }

  return response.json();
}

export async function sendChat(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("채팅 요청에 실패했습니다.");
  }

  return response.json();
}

export async function getProfile(): Promise<SurvivorProfile> {
  const response = await fetch(`${API_BASE_URL}/profile`);

  if (!response.ok) {
    throw new Error("생존 프로필 생성에 실패했습니다.");
  }

  return response.json();
}
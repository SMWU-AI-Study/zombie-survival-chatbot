# 🧟 Zombie Survival Chatbot

> **LLM 기반 개인화 좀비 아포칼립스 생존 테스트 챗봇**

정해진 선택지를 고르는 대신, 좀비 아포칼립스 상황에서  
**“나라면 어떻게 행동할 것인가?”를 자유롭게 입력하는 생존 테스트**입니다.

Gemini가 사용자의 행동을 이해해 다음 상황을 자연스럽게 전개하고,  
5개의 생존 시나리오가 끝나면 전체 답변을 분석해 개인별 **Survivor Profile**을 생성합니다.

<img width="1917" height="821" alt="image" src="https://github.com/user-attachments/assets/becc2875-7576-48e0-84d8-9b5ed14bde9f" />
<img width="1918" height="825" alt="image" src="https://github.com/user-attachments/assets/a1013344-4c92-4458-a4cc-528e3ddc347c" />
<img width="1915" height="892" alt="image" src="https://github.com/user-attachments/assets/68ab90b0-357a-4683-8c6c-a5ca65037b7f" />
<img width="1868" height="825" alt="image" src="https://github.com/user-attachments/assets/398545b0-94c0-45d3-8b38-d6b5bf7c16c8" />

---

## 🎮 How It Works

```text
START
  ↓
CASE 01
낯선 생존자의 도움 요청
  ↓
사용자 자유 입력
  ↓
Gemini가 행동을 해석하고 상황 전개
  ↓
CASE 02 → CASE 03 → CASE 04 → CASE 05
  ↓
전체 행동 분석
  ↓
SURVIVOR PROFILE
```

객관식 선택지가 아니라 사용자가 직접 행동을 입력하기 때문에  
같은 상황에서도 사용자마다 서로 다른 생존 과정이 만들어집니다.

---

## ✨ Features

### 🧟 5개의 연속형 생존 Scenario

총 5개의 핵심 생존 상황을 순차적으로 진행합니다.

- CASE 01 — 낯선 생존자의 도움 요청
- CASE 02 — 식량 부족과 물자 확보
- CASE 03 — 동료의 감염 의심
- CASE 04 — 무장한 생존자 집단과의 조우
- CASE 05 — 좀비 무리 속 최종 탈출

각 Scenario의 핵심 사건은 유지하면서  
사용자의 이전 행동을 반영해 Gemini가 세부 상황을 동적으로 생성합니다.

### 💬 자유형 행동 입력

미리 정해진 선택지를 제공하지 않습니다.

예를 들어,

> 일단 문을 열지 않고 창문으로 상태부터 확인한다.

처럼 사용자가 실제 자신이라면 어떻게 행동할지를 자유롭게 입력할 수 있습니다.

Gemini는 입력의 의미와 의도를 파악해 그 행동에 맞는 결과와 다음 상황을 생성합니다.

### 🧠 Survivor Profile

5개의 Scenario가 종료되면 전체 행동을 기반으로 생존 성향을 분석합니다.

분석하는 Trait은 총 6가지입니다.

| Trait | 의미 |
| --- | --- |
| 판단력 | 상황을 분석하고 합리적으로 판단하는 정도 |
| 신중함 | 위험을 확인하고 조심스럽게 행동하는 정도 |
| 위험 감수 | 위험을 감수하면서 행동하는 정도 |
| 협동성 | 다른 생존자와 협력하려는 정도 |
| 공감성 | 타인의 상황과 감정을 고려하는 정도 |
| 행동력 | 판단한 내용을 실제 행동으로 옮기는 정도 |

최종 결과에서는 다음 정보를 제공합니다.

- Survivor Type
- Recommended Role
- 6개 Survival Trait Score
- Strength
- Weakness

---

## 🧠 Core Design

이 프로젝트에서는 모든 스토리를 LLM에게 완전히 맡기지 않았습니다.

> **Story Skeleton은 애플리케이션이 관리하고,  
> Narration과 성향 분석은 Gemini가 담당합니다.**

각 CASE의 핵심 사건과 평가 요소는 애플리케이션에서 관리하고,  
Gemini는 사용자의 이전 행동을 바탕으로 자연스러운 상황 묘사와 후속 전개를 생성합니다.

이를 통해 사용자마다 다른 이야기가 만들어지면서도  
5개의 핵심 생존 상황과 성향 분석 기준은 유지하도록 설계했습니다.

---

## 🖥️ UI Flow

### Start

생존 테스트의 목적과 분석되는 6개의 Trait을 확인하고 테스트를 시작합니다.

### Survival Session

Zombie GM이 상황을 제시하면 사용자가 자신의 행동을 자유롭게 입력합니다.

- CASE 진행도 표시
- GM / User Message 구분
- Chat 영역 독립 Scroll
- Message Auto Scroll
- 입력창 Auto Focus
- Gemini 응답 Loading 표시

### Survivor Analysis

모든 Scenario가 종료되면 개인별 Survivor Profile을 확인할 수 있습니다.

- Survivor Type
- Recommended Role
- Trait Progress Bar
- Strength / Weakness
- 다시 테스트하기

---

## 🛠 Tech Stack

### Frontend

- React
- TypeScript
- Vite

### Backend

- Python
- FastAPI

### LLM

- Gemini API
- Google GenAI SDK

### Collaboration

- Git
- GitHub

---

## 📁 Project Structure

```text
zombie-survival-chatbot/
│
├── backend/
│   ├── main.py
│   ├── scenarios.json
│   ├── requirements.txt
│   │
│   └── services/
│       └── gemini_service.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── TraitBar.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── StartPage.tsx
│   │   │   ├── ChatPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   └── package.json
│
└── README.md
```

---

## 🔄 Frontend ↔ Backend Flow

```text
React
  ↓
POST /chat
  ↓
FastAPI
  ↓
Scenario State
  ↓
Gemini
  ↓
FastAPI Response
  ↓
React ChatPage
```

Scenario가 모두 종료되면:

```text
CASE 05 Complete
  ↓
GET /profile
  ↓
전체 사용자 답변 분석
  ↓
Gemini
  ↓
Survivor Profile
  ↓
ProfilePage
```

---

## 🚀 Getting Started

### 1. Repository Clone

```bash
git clone <repository-url>
cd zombie-survival-chatbot
```

### 2. Backend

```bash
cd backend

python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

필요한 Package를 설치합니다.

```bash
pip install -r requirements.txt
```

`backend/.env` 파일을 생성합니다.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
USE_MOCK=false
```

Backend Server 실행:

```bash
uvicorn main:app --reload
```

```text
http://127.0.0.1:8000
```

### 3. Frontend

새 Terminal에서:

```bash
cd frontend
npm install
npm run dev
```

```text
http://localhost:5173
```

---

## 🧪 Mock Mode

Gemini API를 호출하지 않고 Scenario Flow를 테스트할 수 있도록 Mock Mode를 지원합니다.

`.env`에서:

```env
USE_MOCK=true
```

로 설정하면 API 사용 없이 전체 Scenario Flow를 테스트할 수 있습니다.

실제 Gemini Response를 사용하려면:

```env
USE_MOCK=false
```

로 변경합니다.

---

## ✅ Prototype v1

현재 Prototype v1에서 구현한 범위입니다.

- [x] Gemini API 연동
- [x] Zombie GM Prompt 설계
- [x] 5개의 연속형 Scenario
- [x] Scenario State 관리
- [x] 사용자 자유형 행동 입력
- [x] 사용자 답변 누적
- [x] Mock Mode
- [x] Survivor Profile 생성
- [x] 6개 Survival Trait 분석
- [x] React Frontend
- [x] Start / Chat / Profile UI
- [x] Scenario Progress
- [x] Chat Auto Scroll
- [x] Input Auto Focus
- [x] Loading UX
- [x] Trait Progress Bar
- [x] 다시 테스트하기
- [x] Frontend ↔ Backend ↔ Gemini E2E Flow

---

## 🔮 Future Work

### Profile-based Personalized Chat

Prototype v1에서는 Survivor Profile 생성으로 테스트가 종료됩니다.

향후에는 생성된 Survivor Profile을 다시 Gemini의 Context로 활용해  
**사용자의 생존 성향에 맞는 개인화 Survival Chat**으로 확장할 예정입니다.

```text
Survival Test
      ↓
Survivor Profile
      ↓
생존 대화 이어가기
      ↓
Personalized Survival Chat
```

예를 들어 신중함이 높고 위험 감수 성향이 낮은 사용자와  
행동력과 위험 감수 성향이 높은 사용자에게 서로 다른 방식의 생존 전략을 제시할 수 있도록 확장할 계획입니다.

---

## 📌 Current Status

**Prototype v1 Complete**

`Start → Survival Scenario → Survivor Profile → Restart`

전체 사용자 Flow와 기본 UI/UX 구현을 완료했습니다.

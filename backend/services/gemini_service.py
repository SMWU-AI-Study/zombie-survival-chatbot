from google import genai


MODEL_NAME = "gemini-3.6-flash"


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
- 정답이 하나인 문제처럼 진행하지 않고,
  사용자의 선택에 따라 상황을 유연하게 이어간다.

현재 단계에서는 최종 Survivor Profile을 생성하지 않고,
자연스럽게 생존 상황을 진행하는 것에 집중한다.
"""


def generate_step2(
    client: genai.Client,
    user_answer: str,
    scenario: dict,
):
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
        model=MODEL_NAME,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return response.text


def generate_next_scenario(
    client: genai.Client,
    previous_scenario: dict,
    next_scenario: dict,
    scenario_answers: list,
):
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
        model=MODEL_NAME,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return response.text


def generate_profile(
    client: genai.Client,
    scenario_answers: list,
):
    if not scenario_answers:
        raise ValueError("분석할 시나리오 답변이 없습니다.")

    answers_text = "\n".join(
        f'CASE {answer["scenario_id"]} STEP {answer["step"]}: {answer["answer"]}'
        for answer in scenario_answers
    )

    prompt = f"""
사용자가 좀비 아포칼립스 생존 시나리오에서 한 행동들을 분석하여
Survivor Profile을 생성하라.

[사용자 행동 기록]
{answers_text}

다음 6개의 성향을 0~100 점수로 평가하라.

- judgment: 판단력
- caution: 신중함
- risk_tolerance: 위험 감수 성향
- cooperation: 협동성
- empathy: 공감성
- action: 행동력

분석 규칙:
- 사용자의 실제 답변에 근거해서 평가한다.
- 단순히 특정 행동 하나만 보고 판단하지 않는다.
- 전체 시나리오에서 반복적으로 나타난 행동 패턴을 우선한다.
- 위험을 피했다고 무조건 판단력이 높거나 낮다고 평가하지 않는다.
- 타인을 도왔다고 무조건 공감성이 높다고 판단하지 않는다.
- 상황과 이유를 함께 고려한다.
- 점수는 0~100 사이의 정수로 작성한다.
- survivor_type은 사용자의 가장 특징적인 생존 성향을 짧은 한국어 표현으로 작성한다.
- recommended_role은 좀비 생존 집단에서 어울리는 역할을 작성한다.
- strength와 weakness는 각각 한 문장으로 작성한다.

반드시 아래 JSON 형식으로만 응답하라.
Markdown 코드 블록은 사용하지 않는다.

{{
  "survivor_type": "신중한 전략가",
  "judgment": 88,
  "caution": 92,
  "risk_tolerance": 31,
  "cooperation": 74,
  "empathy": 70,
  "action": 55,
  "recommended_role": "전략 및 물자 관리",
  "strength": "위험 요소를 충분히 분석한 뒤 행동한다.",
  "weakness": "즉각적인 결단이 필요한 상황에서는 대응이 늦어질 수 있다."
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return response.text
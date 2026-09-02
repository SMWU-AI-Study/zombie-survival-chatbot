export interface ChatResponse {
  reply: string;
  scenario_id?: number;
  step?: number | string;
}

export interface ChatMessageType {
  role: "user" | "gm";
  content: string;
}

export interface SurvivorProfile {
  survivor_type: string;
  judgment: number;
  caution: number;
  risk_tolerance: number;
  cooperation: number;
  empathy: number;
  action: number;
  recommended_role: string;
  strength: string;
  weakness: string;
  mode?: string;
}
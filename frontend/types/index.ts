
export interface AgentResponse {
  thoughts: string;
  agent_reasoning: string[];
  sources: string[];
  next_actions: string[];
  action_errors: string[];
}


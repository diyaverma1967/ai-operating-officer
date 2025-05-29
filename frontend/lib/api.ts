
import axios from "axios";

// export const fetchResponse = async (query: string) => {
//     const res = await axios.post("http://127.0.0.1:8000/generate_combined_response", { query });
//   return res.data;
// };

export const fetchResponse = async (query: string) => {
    const res = await axios.post("http://127.0.0.1:8000/generate_unified_response", { query });
  return res.data;
};

export const fetchTriggerAutomation = async (
  actionType: string,
  summary: string,
  _description?: string
) => {
  const res = await axios.post("http://127.0.0.1:8000/trigger_automation", {
    action_type: actionType,
    summary,
  });
  return res.data;
};

export interface FeedbackRequest {
  response: string;
  chunks: string[];
  feedback: 'accept' | 'retry' | 'reject';
}

export interface FeedbackResponse {
  score: number;
  fine_tune_triggered: boolean;
}
export const sendFeedback = async (req: FeedbackRequest): Promise<FeedbackResponse> => {
  const res = await axios.post("http://127.0.0.1:8000/feedback", req);
  return res.data;
};


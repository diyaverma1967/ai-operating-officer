from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.response_utils import get_combined_response
from my_agents.action_automation_node import create_jira_ticket, create_github_repo

from typing import Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_combined_response")
async def combined_response(request: Request):
    data = await request.json()
    query = data.get("query")
    result = get_combined_response(query)
    return result


@app.post("/trigger_automation")
async def automation_endpoint(request: Request):
    data = await request.json()
    action_type = data.get("action_type")
    summary = data.get("summary", "No description provided")

    if action_type == "jira":
        result = create_jira_ticket(summary, summary)
        if result.get("status") == "created":
            result["url"] = f"https://diyaverma1967.atlassian.net/browse/{result['ticket_id']}"
    elif action_type == "github":
        result = create_github_repo(summary)
    else:
        return {"error": "Unsupported action type"}

    return {"result": result}



class FeedbackRequest(BaseModel):
    response: str
    chunks: list[Any]
    feedback: str


class FeedbackResponse(BaseModel):
    score: float
    fine_tune_triggered: bool


def run_auto_eval(response: str, chunks: list[str]) -> float:
    """
    Placeholder for RAGAS + DeepEval scoring logic.
    Replace this stub with your real scoring function.
    """
    if "error" in response.lower():
        return 0.5
    return 0.9


@app.post("/feedback", response_model=FeedbackResponse)
async def feedback_endpoint(feedback_req: FeedbackRequest):
    """
    Receives user feedback, runs an auto-evaluation,
    and triggers fine-tuning if score < 0.8.
    """
    score = run_auto_eval(feedback_req.response, feedback_req.chunks)
    fine = score < 0.8
    if fine:
        print(f"Retrieval fine-tuning triggered for feedback: {feedback_req.feedback}")
    return FeedbackResponse(score=score, fine_tune_triggered=fine)

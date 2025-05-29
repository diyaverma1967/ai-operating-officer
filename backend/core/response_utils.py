
from my_agents.multi_agent_pipeline import generate_multi_agent_response
from core.generate_response import generate_response

def get_combined_response(query: str):
    basic = generate_response(query)
    advanced = generate_multi_agent_response(query)
    return {
        "thoughts": basic["thoughts"],
        "sources": basic["sources"],
        "next_actions": basic["next_actions"],
        "agent_reasoning": advanced["agent_reasoning"],
        "inspector_report": advanced.get("inspector_report"),
    }

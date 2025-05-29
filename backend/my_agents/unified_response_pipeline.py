

import re
import json
from core.embeddings import get_vectorstore
from langchain_ollama import OllamaLLM
from core.detectPersonaTypes import PERSONA_MAP

# ------- Utility: Persona-Aware Prompt Templates -------
def get_summary_prompt(persona, query, context_str):
    persona_instructions = {
        "CEO": "You are the CEO of Microsoft. Give a direct, high-level, actionable executive summary (max 2 sentences, max 40 words). Each claim must cite its supporting source as [n], using only facts from the provided context chunks.",
        "CTO": "You are the CTO of Microsoft. Summarize the technical or architectural perspective in 2 precise sentences (max 50 words). Cite sources as [n], using only the context below.",
        "EVP_Product": "You are an EVP of Product at Microsoft. Summarize the product or market impact in 2 clear sentences (max 40 words), citing supporting context as [n]."
    }
    instr = persona_instructions.get(persona, persona_instructions["CEO"])
    return f"""
{instr}
Do not restate the question. Do not include generic advice.

Query: {query}

Context Chunks:
{context_str}

Summary (as per the above instructions, with citations [n]):
"""

def get_action_prompt(persona, query, summary):
    persona_action_rules = {
        "CEO": "Prioritize business and executive next steps. Only return the single most relevant action as a JSON object, based strictly on what is explicitly requested in the query.",
        "CTO": "Focus on technical or implementation actions. Return only the single most relevant action as a JSON object, based strictly on the query.",
        "EVP_Product": "Focus on product or user-facing actions. Return only the single most relevant action as a JSON object, as per the query."
    }
    rule = persona_action_rules.get(persona, persona_action_rules["CEO"])
    return f"""
Given the query: "{query}" and the summary below,
{rule}
Do not suggest more than one action. Do not add generic or unrelated suggestions. Return only a JSON object with these fields:
- "type": ("jira" | "github" | "product_action" | ...),
- "title": one-line title,
- "description": max two lines explaining the action and its intent.

Summary:
{summary}
"""

def get_reasoning_prompt(persona, chunk_map, query, summary):
    persona_reasoning = {
        "CEO": "In 2 bullet points (max 20 words each), explain (1) why these context chunks were chosen, (2) why the suggested action is relevant from a CEO perspective.",
        "CTO": "In 2 bullet points (max 25 words each), explain (1) why these context chunks were technically relevant, (2) why the suggested action is technically logical.",
        "EVP_Product": "In 2 bullet points (max 20 words each), explain (1) why these context chunks matter for product/market, (2) why the action is valuable for users."
    }
    bullet_rule = persona_reasoning.get(persona, persona_reasoning["CEO"])
    context_str = "\n".join([f'[{c["id"]}] (score={c.get("score",0):.2f}) {c["type"]} {c["filename"]} {c["url"]}' for c in chunk_map])
    return f"""
{bullet_rule}
Query: "{query}"
Retrieved context chunks:
{context_str}

Generated summary:
{summary}
"""

def get_inspector_prompt(query, summary, agent_reasoning, chunk_map, sources, actions):
    return f"""
You are an independent AI inspector agent.
Critically review the following agent pipeline output for quality, faithfulness, and justification.

- Query: {query}
- Generated summary: {summary}
- Agent Reasoning: {agent_reasoning}
- Sources: {sources}
- Next Actions: {actions}

Please answer:
- Did the summary correctly cite sources and avoid hallucination?
- Is the reasoning chain logical and complete, or did the agent miss anything?
- Are next actions justified and specific?
- Suggest improvements or corrections if needed.
Respond in 2-4 clear bullet points.
"""

# ------- Unified Retrieval -------
def retriever_agent(query, persona=None, k=4):
    vectordb = get_vectorstore()
    docs_and_scores = vectordb.similarity_search_with_score(query, k=16)
    # Persona-aware filtering
    if persona:
        docs_and_scores = [
            (doc, score) for doc, score in docs_and_scores
            if doc.metadata.get("role", "").upper() == persona.upper()
        ]
    docs_and_scores = docs_and_scores[:k]
    chunk_map = []
    context_for_llm = []
    for idx, (doc, score) in enumerate(docs_and_scores):
        meta = doc.metadata or {}
        chunk_id = meta.get("chunk_id", str(idx + 1))
        url = meta.get("url", "#")
        typ = meta.get("type", "unknown")
        filename = meta.get("source", "unknown")
        preview = doc.page_content.strip()[:180] + ("..." if len(doc.page_content) > 180 else "")
        context_for_llm.append(f"[{idx + 1}] {doc.page_content.strip()[:400]}")
        chunk_map.append({
            "id": idx + 1,
            "chunk_id": chunk_id,
            "url": url,
            "type": typ,
            "filename": filename,
            "preview": preview,
            "score": float(score),
            "full_text": doc.page_content.strip()
        })
    return chunk_map, "\n\n".join(context_for_llm)

# ------- Unified Pipeline -------
def unified_generate_response(query, persona="CEO", model="llama3"):
    chunk_map, context_str = retriever_agent(query, persona)
    llm = OllamaLLM(model=model)

    # --- Summary ---
    summary_prompt = get_summary_prompt(persona, query, context_str)
    summary = llm.invoke(summary_prompt).strip()
    used_indices = set(int(i) for i in re.findall(r"\[(\d+)\]", summary))
    sources = [
        {"url": c["url"], "chunk_id": c["chunk_id"], "preview": c["preview"]}
        for c in chunk_map if c["id"] in used_indices
    ]

    # --- Actions ---
    action_prompt = get_action_prompt(persona, query, summary)
    actions_text = llm.invoke(action_prompt)

    # Format as a single string
    try:
        match = re.search(r"\{.*\}", actions_text, re.DOTALL)
        if match:
            action_obj = json.loads(match.group(0))
            action_str = f"{action_obj.get('title', '')} — {action_obj.get('description', '')} ({action_obj.get('type', '')})"
            next_actions = [action_str]
        else:
            next_actions = [actions_text.strip()]
    except Exception as e:
        print("[ACTION_AGENT] JSON decode error:", actions_text)
        next_actions = [actions_text.strip()]

    # --- Reasoning ---
    reasoning_prompt = get_reasoning_prompt(persona, chunk_map, query, summary)
    reasoning_text = llm.invoke(reasoning_prompt).strip()
    agent_reasoning = [line.lstrip('-• ').strip() for line in reasoning_text.splitlines() if line.strip()]

    # --- Inspector ---
    inspector_prompt = get_inspector_prompt(query, summary, agent_reasoning, chunk_map, sources, [next_actions])
    inspector_text = llm.invoke(inspector_prompt).strip()
    inspector_report = [line.lstrip('-• ').strip() for line in inspector_text.splitlines() if line.strip()]

    # --- Final output (now with string action) ---
    return {
        "thoughts": summary,
        "sources": sources,
        "next_actions": next_actions,
        "agent_reasoning": agent_reasoning,
        "inspector_report": inspector_report,
        "action_errors": []
    }

def extract_personas_from_query(query):
    query_lower = query.lower()
    personas = set()
    for key, value in PERSONA_MAP.items():
        if key in query_lower:
            personas.add(value)
    return list(personas) or ["CEO"] 

# Example usage:
if __name__ == "__main__":
    query = "What are Satya Nadella and Kevin Scott's perspectives on migrating legacy systems to the cloud and spin up a PoC repo to explore it?"
    personas = extract_personas_from_query(query)
    all_responses = {p: unified_generate_response(query, persona=p) for p in personas}
    print(json.dumps(all_responses, indent=2))



# import re
# import json
# from core.embeddings import get_vectorstore
# from langchain_ollama import OllamaLLM
# from core.detectPersonaTypes import PERSONA_MAP

# # ------- Utility: Persona-Aware Prompt Templates -------
# def get_summary_prompt(persona, query, context_str):
#     persona_instructions = {
#         "CEO": "You are the CEO of Microsoft. Give a direct, high-level, actionable executive summary (max 2 sentences, max 40 words). Each claim must cite its supporting source as [n], using only facts from the provided context chunks.",
#         "CTO": "You are the CTO of Microsoft. Summarize the technical or architectural perspective in 2 precise sentences (max 50 words). Cite sources as [n], using only the context below.",
#         "EVP_Product": "You are an EVP of Product at Microsoft. Summarize the product or market impact in 2 clear sentences (max 40 words), citing supporting context as [n]."
#     }
#     instr = persona_instructions.get(persona, persona_instructions["CEO"])
#     return f"""
# {instr}
# Do not restate the question. Do not include generic advice.

# Query: {query}

# Context Chunks:
# {context_str}

# Summary (as per the above instructions, with citations [n]):
# """

# def get_action_prompt(persona, query, summary):
#     persona_action_rules = {
#         "CEO": "Prioritize business and executive next steps. Only return the single most relevant action as a JSON object, based strictly on what is explicitly requested in the query.",
#         "CTO": "Focus on technical or implementation actions. Return only the single most relevant action as a JSON object, based strictly on the query.",
#         "EVP_Product": "Focus on product or user-facing actions. Return only the single most relevant action as a JSON object, as per the query."
#     }
#     rule = persona_action_rules.get(persona, persona_action_rules["CEO"])
#     return f"""
# Given the query: "{query}" and the summary below,
# {rule}
# Do not suggest more than one action. Do not add generic or unrelated suggestions. Return only a JSON object with these fields:
# - "type": ("jira" | "github" | "product_action" | ...),
# - "title": one-line title,
# - "description": max two lines explaining the action and its intent.

# Summary:
# {summary}
# """

# def get_reasoning_prompt(persona, chunk_map, query, summary):
#     persona_reasoning = {
#         "CEO": "In 2 bullet points (max 20 words each), explain (1) why these context chunks were chosen, (2) why the suggested action is relevant from a CEO perspective.",
#         "CTO": "In 2 bullet points (max 25 words each), explain (1) why these context chunks were technically relevant, (2) why the suggested action is technically logical.",
#         "EVP_Product": "In 2 bullet points (max 20 words each), explain (1) why these context chunks matter for product/market, (2) why the action is valuable for users."
#     }
#     bullet_rule = persona_reasoning.get(persona, persona_reasoning["CEO"])
#     context_str = "\n".join([f'[{c["id"]}] (score={c.get("score",0):.2f}) {c["type"]} {c["filename"]} {c["url"]}' for c in chunk_map])
#     return f"""
# {bullet_rule}
# Query: "{query}"
# Retrieved context chunks:
# {context_str}

# Generated summary:
# {summary}
# """

# def get_inspector_prompt(query, summary, agent_reasoning, chunk_map, sources, actions):
#     return f"""
# You are an independent AI inspector agent.
# Critically review the following agent pipeline output for quality, faithfulness, and justification.

# - Query: {query}
# - Generated summary: {summary}
# - Agent Reasoning: {agent_reasoning}
# - Sources: {sources}
# - Next Actions: {actions}

# Please answer:
# - Did the summary correctly cite sources and avoid hallucination?
# - Is the reasoning chain logical and complete, or did the agent miss anything?
# - Are next actions justified and specific?
# - Suggest improvements or corrections if needed.
# Respond in 2-4 clear bullet points.
# """

# # ------- Unified Retrieval -------
# def retriever_agent(query, persona=None, k=4):
#     vectordb = get_vectorstore()
#     docs_and_scores = vectordb.similarity_search_with_score(query, k=16)
#     # Persona-aware filtering
#     if persona:
#         docs_and_scores = [
#             (doc, score) for doc, score in docs_and_scores
#             if doc.metadata.get("role", "").upper() == persona.upper()
#         ]
#     docs_and_scores = docs_and_scores[:k]
#     chunk_map = []
#     context_for_llm = []
#     for idx, (doc, score) in enumerate(docs_and_scores):
#         meta = doc.metadata or {}
#         chunk_id = meta.get("chunk_id", str(idx + 1))
#         url = meta.get("url", "#")
#         typ = meta.get("type", "unknown")
#         filename = meta.get("source", "unknown")
#         preview = doc.page_content.strip()[:180] + ("..." if len(doc.page_content) > 180 else "")
#         context_for_llm.append(f"[{idx + 1}] {doc.page_content.strip()[:400]}")
#         chunk_map.append({
#             "id": idx + 1,
#             "chunk_id": chunk_id,
#             "url": url,
#             "type": typ,
#             "filename": filename,
#             "preview": preview,
#             "score": float(score),
#             "full_text": doc.page_content.strip()
#         })
#     return chunk_map, "\n\n".join(context_for_llm)

# # ------- Unified Pipeline -------
# def unified_generate_response(query, persona="CEO", model="llama3"):
#     chunk_map, context_str = retriever_agent(query, persona)
#     llm = OllamaLLM(model=model)

#     # --- Summary ---
#     summary_prompt = get_summary_prompt(persona, query, context_str)
#     summary = llm.invoke(summary_prompt).strip()
#     used_indices = set(int(i) for i in re.findall(r"\[(\d+)\]", summary))
#     sources = [
#         {"url": c["url"], "chunk_id": c["chunk_id"], "preview": c["preview"]}
#         for c in chunk_map if c["id"] in used_indices
#     ]

#     # --- Actions ---
#     action_prompt = get_action_prompt(persona, query, summary)
#     actions_text = llm.invoke(action_prompt)
#     # Try to parse a single JSON object from LLM response
#     try:
#         match = re.search(r"\{.*\}", actions_text, re.DOTALL)
#         if match:
#             next_action = json.loads(match.group(0))
#             next_actions = [next_action]
#         else:
#             next_actions = []
#     except Exception as e:
#         print("[ACTION_AGENT] JSON decode error:", actions_text)
#         next_actions = []

#     # --- Reasoning ---
#     reasoning_prompt = get_reasoning_prompt(persona, chunk_map, query, summary)
#     reasoning_text = llm.invoke(reasoning_prompt).strip()
#     agent_reasoning = [line.lstrip('-• ').strip() for line in reasoning_text.splitlines() if line.strip()]

#     # --- Inspector ---
#     inspector_prompt = get_inspector_prompt(query, summary, agent_reasoning, chunk_map, sources, next_actions)
#     inspector_text = llm.invoke(inspector_prompt).strip()
#     inspector_report = [line.lstrip('-• ').strip() for line in inspector_text.splitlines() if line.strip()]

#     # --- Final output (matches your frontend contract) ---
#     return {
#         "thoughts": summary,
#         "sources": sources,
#         "next_actions": next_actions,
#         "agent_reasoning": agent_reasoning,
#         "inspector_report": inspector_report,
#         "action_errors": []
#     }

# def extract_personas_from_query(query):
#     query_lower = query.lower()
#     personas = set()
#     for key, value in PERSONA_MAP.items():
#         if key in query_lower:
#             personas.add(value)
#     return list(personas) or ["CEO"] 

# # Example usage:
# if __name__ == "__main__":
#     query = "What are Satya Nadella and Kevin Scott's perspectives on migrating legacy systems to the cloud and spin up a PoC repo to explore it?"
#     personas = extract_personas_from_query(query)
#     all_responses = {p: unified_generate_response(query, persona=p) for p in personas}
#     print(json.dumps(all_responses, indent=2))


import re
from core.embeddings import get_vectorstore
from langchain_ollama import OllamaLLM

def retriever_agent(query, k=4):
    vectordb = get_vectorstore()
    try:
        docs_and_scores = vectordb.similarity_search_with_score(query, k=k)
    except AttributeError:
        docs = vectordb.similarity_search(query, k=k)
        docs_and_scores = [(doc, 0.0) for doc in docs]

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

def synthesizer_agent(query, context_str, model="llama3"):
    llm = OllamaLLM(model=model)
    summary_prompt = f"""
You are a cloud strategy analyst for Satya Nadella.
For the given query and supporting evidence, write a 3-4 line executive summary in a business tone.
Important: For every claim or insight, cite its source using [1], [2], etc., where the number refers to the numbered context chunks below.

Query: {query}

Context Chunks:
{context_str}

Summary (with citations as [n], map to the context above):
"""
    return llm.invoke(summary_prompt).strip()

def reasoning_agent(query, chunk_map, summary, model="llama3"):
    llm = OllamaLLM(model=model)
    reasoning_prompt = f"""
You are an explainable AI assistant. 
Explain your reasoning process for answering the following business question:

- Query: "{query}"
- Retrieved context chunks (with scores):
{chr(10).join([f'[{c["id"]}] (score={c["score"]:.2f}) {c["type"]} {c["filename"]} {c["url"]}' for c in chunk_map])}

- Generated summary:
{summary}

Please write 2-4 bullet points explaining:

**1. Why these specific chunks were selected (reference similarity, topical relevance, recency, or user intent if visible).
**2. Why the proposed next actions are a logical follow-up.
"""
    reasoning_text = llm.invoke(reasoning_prompt).strip()
    agent_reasoning = [line.lstrip('-• ').strip() for line in reasoning_text.splitlines() if line.strip()]
    return agent_reasoning

def actions_agent(query, summary, model="llama3"):
    llm = OllamaLLM(model=model)
    action_prompt = f"""
Given the query: "{query}" and the above summary,
Suggest 2-3 concrete next steps as actionable items for business automation.
For each action, return a JSON object with these fields:
- "type": ("jira" | "github" | "graph_api" | ...),
- "title": one-line title or summary,
- "description": a 2-4 line business description for a ticket or repo.

Return only the JSON array, with no commentary, explanation, or markdown.
Do not include any other text.
"""
    import json
    import re 
    actions_text = llm.invoke(action_prompt)
    try:
        match = re.search(r"(\[\s*{.*}\s*\])", actions_text, re.DOTALL)
        if match:
            next_actions = json.loads(match.group(1))
        else:
            next_actions = []
    except Exception as e:
        print("[ACTION_AGENT] JSON decode error, got:", actions_text)
        next_actions = []
    return next_actions

def inspector_agent(query, summary, agent_reasoning, chunk_map, sources, actions, model="llama3"):
    llm = OllamaLLM(model=model)
    inspection_prompt = f"""
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
    inspection_text = llm.invoke(inspection_prompt).strip()
    inspector_report = [line.lstrip('-• ').strip() for line in inspection_text.splitlines() if line.strip()]
    return inspector_report

def generate_multi_agent_response(query: str):

    chunk_map, context_str = retriever_agent(query)
    summary = synthesizer_agent(query, context_str)
    used_indices = set(int(i) for i in re.findall(r"\[(\d+)\]", summary))
    sources = [ {
        "url": c["url"],
        "chunk_id": c["chunk_id"],
        "preview": c["preview"]
    } for c in chunk_map if c["id"] in used_indices ]
    agent_reasoning = reasoning_agent(query, chunk_map, summary)
    next_actions = actions_agent(query, summary)
    inspector_report = inspector_agent(
        query, summary, agent_reasoning, chunk_map, sources, next_actions
    )

    return {
        "thoughts": summary,
        "agent_reasoning": agent_reasoning,
        "sources": sources,
        "next_actions": next_actions,
        "action_errors": [],
        "inspector_report": inspector_report
    }

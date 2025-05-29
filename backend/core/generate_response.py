import re
from core.embeddings import get_vectorstore
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document


def generate_response(query: str):
    vectordb = get_vectorstore()
    docs = vectordb.similarity_search(query, k=4)

    chunk_map = []
    context_for_llm = []
    for idx, doc in enumerate(docs):
        meta = doc.metadata or {}
        chunk_id = meta.get("chunk_id", str(idx + 1))
        url = meta.get("url", "#")
        context_for_llm.append(f"[{idx + 1}] {doc.page_content.strip()[:500]}")
        chunk_map.append({
            "id": idx + 1,
            "chunk_id": chunk_id,
            "url": url,
            "type": meta.get("type", "unknown"),
            "filename": meta.get("source", "unknown"),
            "preview": doc.page_content.strip()[:180] + ("..." if len(doc.page_content) > 180 else "")
        })

    context_str = "\n\n".join(context_for_llm)
    llm = OllamaLLM(model="llama3")

    summary_prompt = f"""
You are a cloud strategy analyst for Satya Nadella. 
For the given query and supporting evidence, write a 3-4 line executive summary in a business tone.
*Important:* For every claim or insight, cite its source using [1], [2], etc., where the number refers to the numbered context chunks below.

Query: {query}

Context Chunks:
{context_str}

Summary (with citations as [n], map to the context above):
"""

    summary = llm.invoke(summary_prompt).strip()

    used_indices = set(int(i) for i in re.findall(r"\[(\d+)\]", summary))

    agent_reasoning = []
    for c in chunk_map:
        if c["id"] in used_indices:
            agent_reasoning.append({
                "type": c["type"],
                "filename": c["filename"],
                "url": c["url"],
                "chunk_id": c["chunk_id"],
                "preview": c["preview"],
                "rationale": "Selected due to high semantic similarity and topical relevance to the query."
            })

    sources = [
        {
            "url": c["url"],
            "chunk_id": c["chunk_id"],
            "preview": c["preview"]
        }
        for c in chunk_map if c["id"] in used_indices
    ]

    action_prompt = f"""
Given the query: "{query}", and the following summary:\n\n{summary}\n\n
Suggest 2-3 concrete next steps as actionable bullet points. Focus on actions like creating PoC repos, opening JIRA tickets, or scheduling a follow-up meeting.
Actions:
"""
    actions_text = llm.invoke(action_prompt)

    next_actions = [a.strip("-•* \n") for a in actions_text.strip().splitlines() if a.strip("-•* \n")]

    return {
        "thoughts": summary,
        "agent_reasoning": agent_reasoning,
        "sources": sources,
        "next_actions": next_actions,
        "action_errors": []
    }
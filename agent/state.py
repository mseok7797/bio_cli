from __future__ import annotations

from typing import Any

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    user_query: str
    plan: str
    retrieved_docs: list[dict[str, Any]]
    research_notes: str
    draft_answer: str
    final_answer: str
    error: str

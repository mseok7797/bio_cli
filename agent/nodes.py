from __future__ import annotations

from langchain_core.documents import Document

from agent.state import AgentState
from core.config import Settings
from core.llm import get_chat_model
from core.rag import retrieve_documents

SAFETY_NOTICE = (
    "안전 안내: 이 답변은 정보 제공용이며 의료 진단, 치료, 처방을 대체하지 않습니다. "
    "증상이나 질환이 의심되면 의료 전문가와 상담하세요."
)


def _serialize_docs(docs: list[Document]) -> list[dict[str, str]]:
    serialized: list[dict[str, str]] = []
    for doc in docs:
        serialized.append(
            {
                "content": doc.page_content,
                "source": str(doc.metadata.get("source", "unknown")),
                "page": str(doc.metadata.get("page", "n/a")),
            }
        )
    return serialized


def planner_node(state: AgentState, settings: Settings) -> AgentState:
    llm = get_chat_model(settings)
    prompt = (
        "당신은 영양학 및 운동생리학 질문을 분석하는 플래너입니다.\n"
        "사용자 질문을 한국어로 분석하고, 검색해야 할 핵심 하위 주제를 3개 이내로 정리하세요.\n"
        f"질문: {state['user_query']}"
    )
    plan = llm.invoke(prompt).content
    return {"plan": str(plan)}


def researcher_node(state: AgentState, settings: Settings) -> AgentState:
    docs = retrieve_documents(question=state["user_query"], settings=settings)
    if not docs:
        return {
            "retrieved_docs": [],
            "research_notes": "검색된 참고 문서가 없습니다. 일반적 수준의 답변만 가능합니다.",
        }

    notes = []
    for idx, doc in enumerate(docs, start=1):
        notes.append(
            f"[{idx}] 출처={doc.metadata.get('source', 'unknown')} "
            f"page={doc.metadata.get('page', 'n/a')} "
            f"내용={doc.page_content[:500].strip()}"
        )
    return {
        "retrieved_docs": _serialize_docs(docs),
        "research_notes": "\n".join(notes),
    }


def writer_node(state: AgentState, settings: Settings) -> AgentState:
    llm = get_chat_model(settings)
    prompt = (
        "당신은 영양학 및 운동생리학 정보를 설명하는 작성자입니다.\n"
        "반드시 한국어로만 답하고, 검색 근거가 부족하면 그 한계를 분명히 밝히세요.\n"
        "검색 근거가 있으면 해당 근거를 요약해 반영하세요.\n"
        "의료행위처럼 단정하지 말고 실용적으로 답하세요.\n\n"
        f"질문:\n{state['user_query']}\n\n"
        f"계획:\n{state.get('plan', '')}\n\n"
        f"리서치 노트:\n{state.get('research_notes', '')}"
    )
    draft = llm.invoke(prompt).content
    return {"draft_answer": str(draft)}


def reviewer_node(state: AgentState, settings: Settings) -> AgentState:
    llm = get_chat_model(settings)
    prompt = (
        "당신은 영양학 및 운동생리학 답변 검토자입니다.\n"
        "답변을 한국어로 다듬고, 과장되거나 위험한 표현을 줄이고, 필요한 경우 한계를 명확히 쓰세요.\n"
        "최종 답변 마지막에는 반드시 안전 안내 문구를 포함하세요.\n\n"
        f"질문:\n{state['user_query']}\n\n"
        f"초안:\n{state.get('draft_answer', '')}\n\n"
        f"안전 안내 문구:\n{SAFETY_NOTICE}"
    )
    final_answer = llm.invoke(prompt).content
    final_text = str(final_answer).strip()
    if SAFETY_NOTICE not in final_text:
        final_text = f"{final_text}\n\n{SAFETY_NOTICE}"
    return {"final_answer": final_text}

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agent.nodes import planner_node, researcher_node, reviewer_node, writer_node
from agent.state import AgentState
from core.config import Settings


def build_graph(settings: Settings):
    graph = StateGraph(AgentState)
    graph.add_node("planner", lambda state: planner_node(state, settings))
    graph.add_node("researcher", lambda state: researcher_node(state, settings))
    graph.add_node("writer", lambda state: writer_node(state, settings))
    graph.add_node("reviewer", lambda state: reviewer_node(state, settings))

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_edge("reviewer", END)
    return graph.compile()


def run_agent(question: str, settings: Settings) -> AgentState:
    app = build_graph(settings)
    result = app.invoke({"user_query": question})
    return result

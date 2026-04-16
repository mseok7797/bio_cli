from agent.state import AgentState


def test_state_shape_allows_user_query() -> None:
    state: AgentState = {"user_query": "단백질 섭취는 언제가 좋은가?"}
    assert state["user_query"].startswith("단백질")

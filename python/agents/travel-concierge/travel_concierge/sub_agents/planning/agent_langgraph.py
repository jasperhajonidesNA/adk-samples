from langgraph.graph import StateGraph, END

from .agent import planning_agent


def build_planning_graph() -> StateGraph:
    """Wrap the planning agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("planning_agent", planning_agent.invoke)
    builder.set_entry_point("planning_agent")
    builder.add_edge("planning_agent", END)
    return builder.compile()


planning_agent_graph = build_planning_graph()

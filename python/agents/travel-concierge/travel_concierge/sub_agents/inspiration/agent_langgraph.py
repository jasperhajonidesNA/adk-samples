from langgraph.graph import StateGraph, END

from .agent import inspiration_agent


def build_inspiration_graph() -> StateGraph:
    """Wrap the inspiration agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("inspiration_agent", inspiration_agent.invoke)
    builder.set_entry_point("inspiration_agent")
    builder.add_edge("inspiration_agent", END)
    return builder.compile()


inspiration_agent_graph = build_inspiration_graph()

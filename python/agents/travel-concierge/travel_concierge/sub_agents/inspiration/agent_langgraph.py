from langgraph.graph import StateGraph, END

from .agent import inspiration_agent
from travel_concierge.langgraph_utils import agent_invoker


def build_inspiration_graph() -> StateGraph:
    """Wrap the inspiration agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("inspiration_agent", agent_invoker(inspiration_agent))
    builder.set_entry_point("inspiration_agent")
    builder.add_edge("inspiration_agent", END)
    return builder.compile()


inspiration_agent_graph = build_inspiration_graph()

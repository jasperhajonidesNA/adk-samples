from langgraph.graph import StateGraph, END

from travel_concierge.shared_libraries.langgraph_utils import agent_invoker
from .agent import pre_trip_agent


def build_pre_trip_graph() -> StateGraph:
    """Wrap the pre trip agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("pre_trip_agent", agent_invoker(pre_trip_agent))
    builder.set_entry_point("pre_trip_agent")
    builder.add_edge("pre_trip_agent", END)
    return builder.compile()


pre_trip_agent_graph = build_pre_trip_graph()

from langgraph.graph import StateGraph, END

from travel_concierge.shared_libraries.langgraph_utils import agent_invoker

from .agent import booking_agent


def build_booking_graph() -> StateGraph:
    """Wrap the booking agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("booking_agent", agent_invoker(booking_agent))
    builder.set_entry_point("booking_agent")
    builder.add_edge("booking_agent", END)
    return builder.compile()


booking_agent_graph = build_booking_graph()

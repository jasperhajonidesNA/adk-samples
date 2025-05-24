from langgraph.graph import StateGraph, END

from .agent import in_trip_agent
from travel_concierge.langgraph_utils import agent_invoker



def build_in_trip_graph() -> StateGraph:
    """Wrap the in trip agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("in_trip_agent", agent_invoker(in_trip_agent))
    builder.set_entry_point("in_trip_agent")
    builder.add_edge("in_trip_agent", END)
    return builder.compile()


in_trip_agent_graph = build_in_trip_graph()

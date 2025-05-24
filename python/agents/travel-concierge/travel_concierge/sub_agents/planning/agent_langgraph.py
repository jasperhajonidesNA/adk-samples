from langgraph.graph import StateGraph, END

from .agent import planning_agent
from travel_concierge.langgraph_utils import agent_invoker

def build_planning_graph() -> StateGraph:
    """Wrap the planning agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("planning_agent", agent_invoker(planning_agent))
    builder.set_entry_point("planning_agent")
    builder.add_edge("planning_agent", END)
    return builder.compile()


planning_agent_graph = build_planning_graph()

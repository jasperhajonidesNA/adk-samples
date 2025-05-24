from langgraph.graph import StateGraph, END

from .agent import post_trip_agent


def build_post_trip_graph() -> StateGraph:
    """Wrap the post trip agent into a LangGraph graph."""
    builder = StateGraph(dict)
    builder.add_node("post_trip_agent", post_trip_agent.invoke)
    builder.set_entry_point("post_trip_agent")
    builder.add_edge("post_trip_agent", END)
    return builder.compile()


post_trip_agent_graph = build_post_trip_graph()

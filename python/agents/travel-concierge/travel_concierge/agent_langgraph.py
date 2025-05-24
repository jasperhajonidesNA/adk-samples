from langgraph.graph import StateGraph, END

from travel_concierge.tools.memory import _load_precreated_itinerary
from travel_concierge.sub_agents.booking.agent_langgraph import booking_agent_graph
from travel_concierge.sub_agents.in_trip.agent_langgraph import in_trip_agent_graph
from travel_concierge.sub_agents.inspiration.agent_langgraph import inspiration_agent_graph
from travel_concierge.sub_agents.planning.agent_langgraph import planning_agent_graph
from travel_concierge.sub_agents.post_trip.agent_langgraph import post_trip_agent_graph
from travel_concierge.sub_agents.pre_trip.agent_langgraph import pre_trip_agent_graph


def _load_itinerary(state: dict) -> dict:
    """Load precreated itinerary into the session state."""
    _load_precreated_itinerary(state)
    return state


def build_root_graph() -> StateGraph:
    """Construct the travel concierge graph using LangGraph."""
    builder = StateGraph(dict)

    builder.add_node("load_itinerary", _load_itinerary)
    builder.add_node("inspiration_agent", inspiration_agent_graph)
    builder.add_node("planning_agent", planning_agent_graph)
    builder.add_node("booking_agent", booking_agent_graph)
    builder.add_node("pre_trip_agent", pre_trip_agent_graph)
    builder.add_node("in_trip_agent", in_trip_agent_graph)
    builder.add_node("post_trip_agent", post_trip_agent_graph)

    builder.set_entry_point("load_itinerary")
    builder.add_edge("load_itinerary", "inspiration_agent")
    builder.add_edge("inspiration_agent", "planning_agent")
    builder.add_edge("planning_agent", "booking_agent")
    builder.add_edge("booking_agent", "pre_trip_agent")
    builder.add_edge("pre_trip_agent", "in_trip_agent")
    builder.add_edge("in_trip_agent", "post_trip_agent")
    builder.add_edge("post_trip_agent", END)

    return builder.compile()


root_agent_graph = build_root_graph()


if __name__ == "__main__":
    """Simple CLI entry point for running the LangGraph workflow."""
    result = root_agent_graph.invoke({})
    print(result)

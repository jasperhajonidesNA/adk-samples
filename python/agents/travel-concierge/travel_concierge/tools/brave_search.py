"""Brave Search API tool for Travel Concierge."""

import os
from typing import List, Dict

import requests


def brave_web_search(query: str) -> Dict[str, List[Dict[str, str]]]:
    """Perform a web search using the Brave Search API.

    Args:
        query: Text query to search for.

    Returns:
        A dictionary with a list of top results or an error message.
    """
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        return {"error": "BRAVE_API_KEY not set"}

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json",
    }
    params = {"q": query, "source": "web"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({"title": item.get("title"), "url": item.get("url")})
            if len(results) >= 3:
                break
        return {"results": results}
    except requests.RequestException as exc:
        return {"error": f"Brave API request failed: {exc}"}


from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool


_brave_search_agent = Agent(
    model="gemini-2.0-flash",
    name="brave_search_agent",
    description="Web search using Brave API",
    instruction="""
    Use the brave_web_search tool to answer the user's question with real search results.
    Provide concise answers based on retrieved links.
    """,
    tools=[brave_web_search],
)

brave_search_tool = AgentTool(agent=_brave_search_agent)

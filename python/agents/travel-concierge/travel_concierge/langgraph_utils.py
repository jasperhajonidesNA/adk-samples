"""Utility helpers for LangGraph wrappers."""

from __future__ import annotations

import asyncio
from typing import Any, Callable


def agent_invoker(agent: Any) -> Callable[[dict], dict]:
    """Return a callable that executes an ADK agent with the given state.

    The ADK agents expose different invocation methods. This helper tries to
    call ``invoke`` if present, otherwise ``run`` or ``run_async``.
    """

    def _invoke(state: dict) -> dict:
        if hasattr(agent, "invoke"):
            return agent.invoke(state)
        if hasattr(agent, "run"):
            return agent.run(state)
        if hasattr(agent, "run_async"):
            return asyncio.run(agent.run_async(state))
        raise AttributeError(f"{type(agent).__name__} has no callable interface")

    return _invoke

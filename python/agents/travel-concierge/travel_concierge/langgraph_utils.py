"""Utility helpers for LangGraph wrappers."""

from __future__ import annotations

import asyncio
from typing import Any, Callable


def agent_invoker(agent: Any) -> Callable[[dict], dict]:
    """Return a callable that executes an ADK agent with the given state.

    The ADK agents expose different invocation methods. This helper tries to
    call ``invoke`` if present, otherwise ``run`` or ``run_async``.
    """

    async def _consume_async_gen(agen):
        """Iterate an async generator and return the last yielded value."""
        result = None
        async for item in agen:
            result = item
        return result

    def _invoke(state: dict) -> dict:
        if hasattr(agent, "invoke"):
            return agent.invoke(state)
        if hasattr(agent, "run"):
            return agent.run(state)
        if hasattr(agent, "run_async"):
            out = agent.run_async(state)
            if hasattr(out, "__aiter__"):
                return asyncio.run(_consume_async_gen(out))
            return asyncio.run(out)
        raise AttributeError(f"{type(agent).__name__} has no callable interface")

    return _invoke

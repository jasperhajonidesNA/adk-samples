"""Helper utilities for LangGraph wrappers."""
from __future__ import annotations

import inspect
from typing import Any, Callable


def agent_invoker(agent: Any) -> Callable[[dict], Any]:
    """Return a callable that executes the given ADK agent.

    The returned function tries common method names like ``invoke`` or ``run``
    and falls back to calling the agent directly if it is callable.
    """

    async def _run(state: dict):
        for name in ("invoke_async", "invoke", "run_async", "run"):
            if hasattr(agent, name):
                fn = getattr(agent, name)
                result = fn(state)
                if inspect.isawaitable(result):
                    return await result
                return result
        if callable(agent):
            result = agent(state)
            if inspect.isawaitable(result):
                return await result
            return result
        raise AttributeError(f"Agent {agent!r} is not callable")

    return _run

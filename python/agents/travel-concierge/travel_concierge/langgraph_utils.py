"""Utility helpers for LangGraph wrappers."""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable


def agent_invoker(agent: Any) -> Callable[[dict], dict]:
    """Return a callable that executes an ADK agent with the given state.

    The returned function attempts common entrypoints like ``invoke_async`` or
    ``invoke`` before falling back to ``run_async`` or ``run``.  It supports
    coroutines and async generators, returning their final result synchronously.
    """

    async def _consume_async_gen(agen):
        """Iterate an async generator and return the last yielded value."""
        result = None
        async for item in agen:
            result = item
        return result

    def _invoke(state: dict) -> dict:
        """Invoke ``agent`` using common method names.

        Handles sync callables, coroutines and async generators. If the agent
        exposes ``invoke_async``/``invoke``/``run_async``/``run`` methods they
        are tried in this order. Otherwise the agent is called directly if
        callable.
        """

        for name in ("invoke_async", "invoke", "run_async", "run"):
            if hasattr(agent, name):
                fn = getattr(agent, name)
                result = fn(state)
                if inspect.isawaitable(result):
                    return asyncio.run(result)
                if hasattr(result, "__aiter__"):
                    return asyncio.run(_consume_async_gen(result))
                return result

        if callable(agent):
            result = agent(state)
            if inspect.isawaitable(result):
                return asyncio.run(result)
            if hasattr(result, "__aiter__"):
                return asyncio.run(_consume_async_gen(result))
            return result

        raise AttributeError(f"Agent {agent!r} is not callable")

    return _invoke

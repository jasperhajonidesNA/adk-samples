"""LangSmith integration helpers.

This module exposes a ``traceable`` decorator that wraps functions with
LangSmith tracing when the ``langsmith`` package is installed and the
``LANGCHAIN_API_KEY`` environment variable is set. If these
requirements are not met, the decorator becomes a no-op so the rest of
the codebase does not need to change.
"""

from __future__ import annotations

import os
from typing import Any, Callable

try:
    from langsmith.run_helpers import traceable as _traceable
    _LANGSMITH_ENABLED = bool(os.getenv("LANGCHAIN_API_KEY"))
except Exception:  # pragma: no cover - langsmith is optional
    _traceable = None
    _LANGSMITH_ENABLED = False


def traceable(*args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a decorator to trace functions with LangSmith if available."""

    if _traceable is None or not _LANGSMITH_ENABLED:
        # Fallback no-op decorator
        def _decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return func

        if args and callable(args[0]) and not kwargs:
            return _decorator(args[0])
        return _decorator

    return _traceable(*args, **kwargs)

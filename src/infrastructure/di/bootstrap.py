"""Convention-based provider registry, transient and singleton resolution."""
from __future__ import annotations

from contextvars import ContextVar
from threading import RLock

from src.infrastructure.di.inject import DependencyError
from src.infrastructure.di.reflection import discover_providers

_providers: dict[type, type] = {}
_instances: dict[type, object] = {}
_ready = False
_lock = RLock()
_resolution_stack: ContextVar[tuple[type, ...]] = ContextVar("di_stack", default=())


def bootstrap_di() -> None:
    global _providers, _ready
    with _lock:
        if _ready:
            return
        found = discover_providers()
        _providers = found
        _ready = True


def resolve(cls: type):
    if not _ready:
        raise DependencyError("bootstrap_di must run before dependency resolution")
    provider = _providers.get(cls)
    if provider is None:
        raise DependencyError(f"No DI provider registered for {cls.__module__}.{cls.__qualname__}")
    stack = _resolution_stack.get()
    if cls in stack:
        raise DependencyError("Circular DI dependency: " + " -> ".join(c.__name__ for c in (*stack, cls)))
    token = _resolution_stack.set((*stack, cls))
    try:
        if not getattr(provider, "__di_singleton__", False):
            return provider()
        with _lock:
            if provider not in _instances:
                _instances[provider] = provider()
            return _instances[provider]
    finally:
        _resolution_stack.reset(token)


def shutdown_di() -> None:
    """Forget provider instances after their external resources are closed."""
    global _ready
    with _lock:
        _instances.clear()
        _providers.clear()
        _ready = False

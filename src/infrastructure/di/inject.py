"""Decorator for strict, annotation-based constructor injection."""
from __future__ import annotations

from functools import wraps
from inspect import signature
from typing import get_type_hints


class DependencyError(RuntimeError):
    """DI registration or resolution failed."""


def inject(cls: type) -> type:
    """Mark a concrete provider and inject only required unbound parameters."""
    original = cls.__init__
    sig = signature(original)

    @wraps(original)
    def constructor(self, *args, **kwargs):
        from src.infrastructure.di.bootstrap import resolve

        bound = sig.bind_partial(self, *args, **kwargs)
        try:
            annotations = get_type_hints(original, localns={cls.__name__: cls})
        except (NameError, TypeError) as exc:
            raise DependencyError(f"Invalid annotations for {cls.__qualname__}") from exc
        for name, param in sig.parameters.items():
            if name == "self" or name in bound.arguments or param.default is not param.empty:
                continue
            kind = annotations.get(name)
            if not isinstance(kind, type):
                raise DependencyError(f"Unresolvable constructor type for {cls.__name__}.{name}")
            bound.arguments[name] = resolve(kind)
        return original(*bound.args, **bound.kwargs)

    cls.__init__ = constructor
    cls.__di_provider__ = True
    return cls

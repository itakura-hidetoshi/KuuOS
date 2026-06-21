from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha


def envelope_is_valid(value: Mapping[str, Any]) -> bool:
    body = value.get("body")
    return isinstance(body, Mapping) and value.get("body_digest") == sha(body)


__all__ = ["envelope_is_valid"]

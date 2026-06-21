from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_operational_agent_types_v1_1 import validate_capability


class CapabilityRegistry:
    """Append-only capability history with permanent ID-reuse prevention."""

    def __init__(self) -> None:
        self._active: dict[str, dict[str, Any]] = {}
        self._history: list[dict[str, Any]] = []
        self._seen_ids: set[str] = set()

    def register(self, capability: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_capability(capability)
        if errors:
            raise ValueError("capability_invalid:" + ";".join(errors))
        capability_id = str(capability["capability_id"])
        if capability_id in self._seen_ids:
            raise ValueError("capability_id_reuse_forbidden")
        packet = deepcopy(dict(capability))
        self._active[capability_id] = packet
        self._seen_ids.add(capability_id)
        self._history.append(
            {"event": "REGISTERED", "capability": deepcopy(packet)}
        )
        return deepcopy(packet)

    def get(self, capability_id: str) -> dict[str, Any] | None:
        value = self._active.get(capability_id)
        return deepcopy(value) if value is not None else None

    def deactivate(self, capability_id: str, *, reason: str) -> dict[str, Any]:
        if capability_id not in self._active:
            raise ValueError("capability_not_active")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("capability_deactivation_reason_required")
        packet = self._active.pop(capability_id)
        packet["active"] = False
        self._history.append(
            {
                "event": "DEACTIVATED",
                "reason": reason.strip(),
                "capability": deepcopy(packet),
            }
        )
        return deepcopy(packet)

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return deepcopy(self._active)

    def history(self) -> list[dict[str, Any]]:
        return deepcopy(self._history)

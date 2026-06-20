from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_act_os_kernel_v0_1 import build_act_event
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_belief_os_types_v0_1 import sha


def event(
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_act_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha(
            {
                "phase": phase,
                "payload": dict(payload),
                "tick": tick,
                "clock": "qi-world-third-cycle-v2.2",
            }
        ),
        payload=payload,
        now_ms=tick,
    )


def apply(
    store: ActStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]

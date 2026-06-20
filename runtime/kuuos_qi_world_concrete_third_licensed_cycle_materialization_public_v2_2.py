from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_qi_world_concrete_third_licensed_cycle_materialization_v2_2 as _core
from runtime import kuuos_qi_world_successor_native_evidence_clock_v2_0 as _clock
from runtime.kuuos_act_os_kernel_v0_1 import build_act_event
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_belief_os_types_v0_1 import sha


def _third_cycle_event(
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


def _apply_third_cycle_event(
    store: ActStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_third_cycle_event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _third_cycle_evidence_items() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for index, source_kind in enumerate(("system", "human"), start=1):
        label = f"third-cycle-{source_kind}-{index}"
        items.append(
            {
                "evidence_id": f"third-cycle-evidence-{index}",
                "channel_id": (
                    "system-output" if source_kind == "system" else "independent-check"
                ),
                "source_kind": source_kind,
                "collector_id": f"third-cycle-collector-{source_kind}",
                "independent_source_id": f"third-cycle-source-{source_kind}",
                "collected_at_ms": 699_000 + index * 100,
                "raw_artifact_digest": sha(label + "-raw"),
                "value_digest": sha(label + "-value"),
                "uncertainty_digest": sha(label + "-uncertainty"),
                "calibration_digest": sha(label + "-calibration"),
                "context_digest": sha(label + "-context"),
                "tamper_evidence_digest": sha(label + "-tamper"),
                "provenance_hop_digests": [
                    sha(label + "-source"),
                    sha(label + "-collector"),
                ],
            }
        )
    return items


_core.apply_act = _apply_third_cycle_event
_core.build_fixture_event = _third_cycle_event
_clock._evidence_items = _third_cycle_evidence_items

build_concrete_three_cycle_bundle = _core.build_concrete_three_cycle_bundle
build_materialized_third_cycle_extension_witness = _core.build_materialized_third_cycle_extension_witness
build_third_closed_cycle_receipt = _core.build_third_closed_cycle_receipt
build_third_cycle_authority_intake = _core.build_third_cycle_authority_intake
build_third_cycle_authority_requirement = _core.build_third_cycle_authority_requirement
build_third_licensed_act_handoff_receipt = _core.build_third_licensed_act_handoff_receipt
build_third_native_evidence_closure_receipt = _core.build_third_native_evidence_closure_receipt
validate_concrete_three_cycle_bundle = _core.validate_concrete_three_cycle_bundle
validate_third_closed_cycle_receipt = _core.validate_third_closed_cycle_receipt
validate_third_cycle_authority_intake = _core.validate_third_cycle_authority_intake
validate_third_cycle_authority_requirement = _core.validate_third_cycle_authority_requirement
validate_third_licensed_act_handoff_receipt = _core.validate_third_licensed_act_handoff_receipt
validate_third_native_evidence_closure_receipt = _core.validate_third_native_evidence_closure_receipt
bundle_digest = _core.bundle_digest
closure_digest = _core.closure_digest
handoff_digest = _core.handoff_digest
receipt_digest = _core.receipt_digest
requirement_digest = _core.requirement_digest

__all__ = [
    "build_concrete_three_cycle_bundle",
    "build_materialized_third_cycle_extension_witness",
    "build_third_closed_cycle_receipt",
    "build_third_cycle_authority_intake",
    "build_third_cycle_authority_requirement",
    "build_third_licensed_act_handoff_receipt",
    "build_third_native_evidence_closure_receipt",
    "validate_concrete_three_cycle_bundle",
    "validate_third_closed_cycle_receipt",
    "validate_third_cycle_authority_intake",
    "validate_third_cycle_authority_requirement",
    "validate_third_licensed_act_handoff_receipt",
    "validate_third_native_evidence_closure_receipt",
    "bundle_digest",
    "closure_digest",
    "handoff_digest",
    "receipt_digest",
    "requirement_digest",
]

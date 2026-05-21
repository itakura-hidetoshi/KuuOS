#!/usr/bin/env python3
"""Qi Process Tensor evaluator v0.1.

Operationalizes process-level Qi before Qi Total Field normalization.

Input is a raw Qi/OS state that may contain a `process_history` list.  Each
history item may expose candidate/process evidence such as:

- transition_visible
- memory_link_visible
- nonmarkov_link_visible
- process_observation
- process_action

The evaluator produces process tensor support fields consumed by
`qi_total_field_v0_1.py`:

- process_tensor_visible
- transition_continuity_visible
- memory_continuity_visible
- nonmarkov_memory_visible

This is not a physics theorem and not an execution authority. It is a bounded,
non-authoritative OS evidence evaluator for candidate flow.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import sys
from typing import Any, Mapping, Sequence


NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

BOUNDARY_FIELDS = [
    "two_truths_gap",
    "noncollapse_guard",
    "memory_overwrite_blocker",
    "world_identity_blocker",
]


@dataclass(frozen=True)
class QiProcessTensorReceipt:
    cycle_id: str
    process_tensor_visible: bool
    transition_continuity_visible: bool
    memory_continuity_visible: bool
    nonmarkov_memory_visible: bool
    process_history_length: int
    transition_support_count: int
    memory_support_count: int
    nonmarkov_support_count: int
    missing_process_requirements: list[str]
    process_tensor_reason: str
    enriched_state: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _truthy(state: Mapping[str, Any], key: str) -> bool:
    value = state.get(key, False)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _history(raw: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    items = raw.get("process_history", [])
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes, bytearray)):
        return []
    return [item for item in items if isinstance(item, Mapping)]


def _boundary_ok(raw: Mapping[str, Any]) -> bool:
    return all(_truthy(raw, key) for key in BOUNDARY_FIELDS)


def evaluate_qi_process_tensor(raw: Mapping[str, Any]) -> QiProcessTensorReceipt:
    cycle_id = str(raw.get("cycle_id", "unknown-cycle"))
    history = _history(raw)
    history_len = len(history)

    transition_count = sum(1 for item in history if _truthy(item, "transition_visible"))
    memory_count = sum(1 for item in history if _truthy(item, "memory_link_visible"))
    nonmarkov_count = sum(1 for item in history if _truthy(item, "nonmarkov_link_visible"))

    explicit_process_tensor = _truthy(raw, "process_tensor_visible")
    explicit_transition = _truthy(raw, "transition_continuity_visible")
    explicit_memory = _truthy(raw, "memory_continuity_visible")
    explicit_nonmarkov = _truthy(raw, "nonmarkov_memory_visible")

    transition_visible = explicit_transition or (history_len >= 2 and transition_count >= max(1, history_len - 1))
    memory_visible = explicit_memory or (history_len >= 2 and memory_count >= 1)
    nonmarkov_visible = explicit_nonmarkov or (history_len >= 3 and nonmarkov_count >= 1)

    boundary_ok = _boundary_ok(raw)
    candidate_ok = _truthy(raw, "candidate_only") and _truthy(raw, "nonfinal_marker")

    missing: list[str] = []
    if history_len < 2 and not explicit_process_tensor:
        missing.append("process_history_min_length_or_explicit_process_tensor")
    if not transition_visible:
        missing.append("transition_continuity_visible")
    if not memory_visible:
        missing.append("memory_continuity_visible")
    if not boundary_ok:
        missing.append("boundary_fields_visible")
    if not candidate_ok:
        missing.append("candidate_nonfinal_surface_visible")

    process_tensor_visible = bool(
        explicit_process_tensor
        or (boundary_ok and candidate_ok and transition_visible and memory_visible and history_len >= 2)
    )

    if not boundary_ok:
        reason = "boundary_blocks_process_tensor_support"
    elif not candidate_ok:
        reason = "candidate_nonfinal_surface_missing"
    elif process_tensor_visible:
        reason = "process_tensor_support_visible"
    else:
        reason = "process_tensor_support_incomplete"

    enriched = dict(raw)
    enriched["process_tensor_visible"] = process_tensor_visible
    enriched["transition_continuity_visible"] = transition_visible
    enriched["memory_continuity_visible"] = memory_visible
    enriched["nonmarkov_memory_visible"] = nonmarkov_visible
    enriched["qi_process_tensor_reason"] = reason
    enriched["qi_process_tensor_missing"] = list(missing)
    for key, value in NON_AUTHORITY_FLAGS.items():
        enriched[key] = value

    return QiProcessTensorReceipt(
        cycle_id=cycle_id,
        process_tensor_visible=process_tensor_visible,
        transition_continuity_visible=transition_visible,
        memory_continuity_visible=memory_visible,
        nonmarkov_memory_visible=nonmarkov_visible,
        process_history_length=history_len,
        transition_support_count=transition_count,
        memory_support_count=memory_count,
        nonmarkov_support_count=nonmarkov_count,
        missing_process_requirements=missing,
        process_tensor_reason=reason,
        enriched_state=enriched,
    )


def enrich_state_with_qi_process_tensor(raw: Mapping[str, Any]) -> dict[str, Any]:
    return evaluate_qi_process_tensor(raw).enriched_state


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: qi_process_tensor_v0_1.py RAW_QI_STATE.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw = json.load(f)
    receipt = evaluate_qi_process_tensor(raw)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.process_tensor_visible else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

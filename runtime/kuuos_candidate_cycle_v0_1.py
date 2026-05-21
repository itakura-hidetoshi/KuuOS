#!/usr/bin/env python3
"""KuuOS Candidate Cycle runtime v0.1.

This module connects Qi Total Field to an actual one-step KuuOS candidate cycle.
It reads raw Qi/OS state, normalizes it, runs Qi Runtime Binding and Qi Cycle
Runner, then emits a deterministic cycle receipt with a receipt hash.

The receipt is operational but non-authoritative: it can route a candidate to a
next non-final stage or stop it in a hold/recheck/quarantine queue.  It never
executes, finalizes, overwrites memory, proves a theorem, makes clinical claims,
or creates completed OS identity.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import sys
from typing import Any, Mapping

try:
    from runtime.qi_total_field_v0_1 import QiTotalFieldResult, evaluate_qi_total_field
except ModuleNotFoundError:  # direct script execution from runtime/
    from qi_total_field_v0_1 import QiTotalFieldResult, evaluate_qi_total_field


NON_AUTHORITATIVE_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

QUEUE_POLICY = {
    "NEXT_NONFINAL_STAGE": {
        "cycle_status": "CONTINUE_NONFINAL",
        "terminal_for_cycle": False,
        "required_next_action": "continue_candidate_pipeline",
    },
    "HOLD_QUEUE": {
        "cycle_status": "HOLD",
        "terminal_for_cycle": True,
        "required_next_action": "inspect_hold_notice",
    },
    "REOBSERVE_QUEUE": {
        "cycle_status": "REOBSERVE",
        "terminal_for_cycle": True,
        "required_next_action": "collect_runtime_or_policy_support",
    },
    "LINEAGE_RECHECK_QUEUE": {
        "cycle_status": "LINEAGE_RECHECK",
        "terminal_for_cycle": True,
        "required_next_action": "verify_receipt_hash_support_refs_and_registry_key",
    },
    "DELIVERY_RECHECK_QUEUE": {
        "cycle_status": "DELIVERY_RECHECK",
        "terminal_for_cycle": True,
        "required_next_action": "verify_delivery_envelope_channel_scope_and_acknowledgment",
    },
    "BOUNDARY_RECHECK_QUEUE": {
        "cycle_status": "BOUNDARY_RECHECK",
        "terminal_for_cycle": True,
        "required_next_action": "review_noncollapse_boundary_before_output",
    },
    "QUARANTINE_QUEUE": {
        "cycle_status": "QUARANTINE",
        "terminal_for_cycle": True,
        "required_next_action": "quarantine_candidate_and_review_boundary_risk",
    },
}


@dataclass(frozen=True)
class KuuOSCandidateCycleReceipt:
    cycle_id: str
    generated_at_utc: str
    cycle_status: str
    qi_signal: str
    qi_reason: str
    next_queue: str
    terminal_for_cycle: bool
    required_next_action: str
    missing_inputs: list[str]
    opened_notices: list[str]
    blocked_boundaries: list[str]
    normalized_qi_state: dict[str, Any]
    source_support: dict[str, list[str]]
    qi_process_tensor_receipt: dict[str, Any]
    allowed_projection: list[str]
    receipt_hash: str
    previous_receipt_hash: str | None = None
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _canonical_hash(payload: Mapping[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def run_candidate_cycle(raw_state: Mapping[str, Any]) -> KuuOSCandidateCycleReceipt:
    total: QiTotalFieldResult = evaluate_qi_total_field(raw_state)
    decision = total.qi_cycle_decision
    next_queue = str(decision.get("next_stage", "HOLD_QUEUE"))
    policy = QUEUE_POLICY.get(next_queue, QUEUE_POLICY["HOLD_QUEUE"])
    cycle_id = str(raw_state.get("cycle_id", total.cycle_id))
    previous_hash = raw_state.get("previous_receipt_hash")
    generated_at = str(raw_state.get("generated_at_utc") or datetime.now(timezone.utc).isoformat())

    receipt_payload = {
        "cycle_id": cycle_id,
        "generated_at_utc": generated_at,
        "cycle_status": policy["cycle_status"],
        "qi_signal": decision.get("qi_signal"),
        "qi_reason": decision.get("qi_reason"),
        "next_queue": next_queue,
        "terminal_for_cycle": policy["terminal_for_cycle"],
        "required_next_action": policy["required_next_action"],
        "missing_inputs": decision.get("missing_inputs", []),
        "opened_notices": decision.get("opened_notices", []),
        "blocked_boundaries": decision.get("blocked_boundaries", []),
        "normalized_qi_state": total.normalized_qi_state,
        "source_support": total.source_support,
        "qi_process_tensor_receipt": total.qi_process_tensor_receipt,
        "allowed_projection": decision.get("allowed_projection", []),
        "previous_receipt_hash": previous_hash,
        **NON_AUTHORITATIVE_FLAGS,
    }
    receipt_hash = _canonical_hash(receipt_payload)
    return KuuOSCandidateCycleReceipt(
        receipt_hash=receipt_hash,
        previous_receipt_hash=str(previous_hash) if previous_hash else None,
        **{key: value for key, value in receipt_payload.items() if key != "previous_receipt_hash"},
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_candidate_cycle_v0_1.py RAW_QI_STATE.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw_state = json.load(f)
    receipt = run_candidate_cycle(raw_state)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.cycle_status != "QUARANTINE" else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

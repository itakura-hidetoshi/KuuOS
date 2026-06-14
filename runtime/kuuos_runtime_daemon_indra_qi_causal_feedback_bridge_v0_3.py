#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_feedback_core_v0_3 import (
    ALLOWED_FEEDBACK_KINDS,
    REQUIRED_BOUNDARY,
    build_candidates,
    mapping,
    projection_lineage,
    sha,
    source_event,
    validate_indra_state,
    validate_plan,
    variable_values,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_causal_feedback_bridge_v0_3"
READY = "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_READY"
BLOCKED = "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_BLOCKED"
LICENSE_READY = "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiCausalFeedbackBridgeV0_3Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    feedback_id: str
    source_world_model_id: str
    causal_world_id: str
    source_projection_id: str
    source_transaction_id: str
    source_event_kind: str
    feedback_status: str
    candidate_count: int
    local_patch_candidate_count: int
    qi_flow_candidate_count: int
    source_indra_state_unchanged: bool
    source_indra_state_digest: str
    source_causal_world_model_digest: str
    feedback_packet_path: str
    approval_handoff_path: str
    feedback_ledger_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    result: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            result.append(value)
    return result


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in value)[:128] or "invalid"


def build_indra_qi_causal_feedback_bridge_v0_3(
    *,
    runtime_context: Mapping[str, Any],
    feedback_plan: Mapping[str, Any],
    feedback_license: Mapping[str, Any],
) -> IndraQiCausalFeedbackBridgeV0_3Result:
    context = mapping(runtime_context)
    plan = dict(mapping(feedback_plan))
    license_value = mapping(feedback_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    indra_state_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    projection_packet_path = root / "indra_qi_causal_projection_packet_v0_2.json"
    activation_path = root / "indra_qi_causal_projection_activation_record_v0_2.json"
    causal_state_path = root / "kuuos_causal_world_model_state_v14_0.json"
    causal_event_path = root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"
    feedback_packet_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    approval_handoff_path = root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    feedback_ledger_path = root / "indra_qi_causal_feedback_ledger_v0_3.jsonl"
    receipt_path = root / "indra_qi_causal_feedback_receipt_v0_3.json"
    audit_path = root / "indra_qi_causal_feedback_audit_v0_3.jsonl"

    if context.get("indra_qi_causal_feedback_bridge_v0_3_enabled") is not True:
        blockers.append("indra_qi_causal_feedback_bridge_v0_3_enabled_not_true")
    if context.get("apply_indra_qi_causal_feedback_bridge_v0_3") is not True:
        blockers.append("apply_indra_qi_causal_feedback_bridge_v0_3_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("indra_qi_causal_feedback_bridge_license_not_ready")
    required_flags = (
        "source_indra_state_read_allowed",
        "source_projection_read_allowed",
        "source_causal_state_read_allowed",
        "source_causal_event_read_allowed",
        "source_causal_result_read_allowed",
        "feedback_plan_validate_allowed",
        "feedback_packet_write_allowed",
        "approval_handoff_write_allowed",
        "feedback_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    )
    for flag in required_flags:
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    feedback_id = str(plan.get("feedback_id", ""))
    source_transaction_id = str(plan.get("source_transaction_id", ""))
    if not feedback_id:
        blockers.append("feedback_id_missing")
    if not source_transaction_id:
        blockers.append("source_transaction_id_missing")

    projection_packet = _read_json(projection_packet_path)
    activation = _read_json(activation_path)
    projection_id, source_world_model_id, causal_world_id, source_indra_digest = projection_lineage(
        projection_packet, activation, blockers
    )
    expected_fields = {
        "source_projection_id": projection_id,
        "source_world_model_id": source_world_model_id,
        "causal_world_id": causal_world_id,
        "source_indra_qi_world_state_digest": source_indra_digest,
    }
    for field, expected in expected_fields.items():
        if str(plan.get(field, "")) != expected:
            blockers.append(f"feedback_{field}_mismatch")

    indra_state = _read_json(indra_state_path)
    validate_indra_state(indra_state, source_world_model_id, source_indra_digest, blockers)
    causal_state = _read_json(causal_state_path)
    causal_events = _records(causal_event_path)
    result_path = root / "kuuos_causal_world_model_results_v14_0" / f"{_safe_id(source_transaction_id)}.json"
    causal_result = _read_json(result_path)
    event = source_event(
        transaction_id=source_transaction_id,
        causal_world_id=causal_world_id,
        event_records=causal_events,
        result=causal_result,
        causal_state=causal_state,
        blockers=blockers,
    )
    if str(plan.get("source_causal_event_digest", "")) != str(event.get("record_digest", "")):
        blockers.append("feedback_source_causal_event_digest_mismatch")
    if str(plan.get("source_causal_world_model_digest", "")) != str(event.get("after_world_model_digest", "")):
        blockers.append("feedback_source_causal_world_model_digest_mismatch")

    prior_records = _records(feedback_ledger_path)
    if any(str(record.get("feedback_id", "")) == feedback_id for record in prior_records):
        blockers.append("feedback_id_replay")
    if any(
        str(record.get("source_transaction_id", "")) == source_transaction_id
        for record in prior_records
    ):
        blockers.append("source_causal_transaction_feedback_replay")

    candidates, local_count, flow_count = build_candidates(
        values=variable_values(event, causal_result, causal_state),
        bindings=mapping(projection_packet.get("variable_bindings")),
        event=event,
        policy=mapping(plan.get("feedback_policy")),
        blockers=blockers,
    )
    if not candidates:
        blockers.append("feedback_candidates_missing")
    allowed_raw = license_value.get("allowed_feedback_kinds", [])
    allowed = {str(value) for value in allowed_raw} if isinstance(allowed_raw, list) else set()
    if allowed != ALLOWED_FEEDBACK_KINDS:
        blockers.append("feedback_license_allowed_feedback_kinds_not_exact")
    if any(str(candidate.get("feedback_kind", "")) not in allowed for candidate in candidates):
        blockers.append("feedback_candidate_kind_not_licensed")

    source_after = _read_json(indra_state_path)
    source_unchanged = bool(indra_state) and bool(source_after) and (
        str(source_after.get("indra_qi_world_state_digest", "")) == source_indra_digest
        and compute_indra_qi_world_state_digest(source_after) == source_indra_digest
    )
    if not source_unchanged:
        blockers.append("source_indra_qi_world_state_changed_during_feedback")

    feedback_status = "feedback_candidates_ready" if not blockers else "feedback_blocked"
    if not blockers:
        feedback_packet = {
            "version": VERSION,
            "feedback_status": feedback_status,
            "feedback_id": feedback_id,
            "source_projection_id": projection_id,
            "source_world_model_id": source_world_model_id,
            "source_indra_qi_world_state_digest": source_indra_digest,
            "causal_world_id": causal_world_id,
            "source_transaction_id": source_transaction_id,
            "source_causal_event_kind": str(event.get("command_kind", "")),
            "source_causal_event_digest": str(event.get("record_digest", "")),
            "source_causal_world_model_digest": str(event.get("after_world_model_digest", "")),
            "source_causal_result_digest": sha(causal_result),
            "source_process_tensor_context": dict(mapping(event.get("process_tensor_context"))),
            "feedback_candidates": candidates,
            "candidate_ordering": [candidate["candidate_id"] for candidate in candidates],
            "boundary": {
                **REQUIRED_BOUNDARY,
                "source_causal_event_consumed_once": True,
                "causal_event_kind_feedback_eligible": True,
                "connection_update_not_inferred_from_causal_edges": True,
                "feedback_candidate_order_preserved": True,
            },
            "epoch": int(time.time()),
        }
        feedback_packet["feedback_packet_digest"] = sha(feedback_packet)
        _write_json(feedback_packet_path, feedback_packet)

        approval_handoff = {
            "version": "indra_qi_causal_feedback_approval_handoff_v0_3",
            "handoff_status": "approval_required",
            "feedback_id": feedback_id,
            "source_feedback_packet_digest": feedback_packet["feedback_packet_digest"],
            "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
            "requested_authority": "bounded_indra_qi_world_mutation_review",
            "direct_application_allowed": False,
            "operator_algebra_mutation_allowed": False,
            "gauge_connection_mutation_allowed": False,
            "holonomy_replacement_allowed": False,
            "external_world_actuation_allowed": False,
            "required_next_stage": "licensed_feedback_candidate_review_and_activation",
            "boundary": {
                "approval_handoff_not_approval": True,
                "receipt_not_truth": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
            },
            "epoch": int(time.time()),
        }
        approval_handoff["approval_handoff_digest"] = sha(approval_handoff)
        _write_json(approval_handoff_path, approval_handoff)

        ledger_record = {
            "version": "indra_qi_causal_feedback_ledger_record_v0_3",
            "record_type": "indra_qi_causal_feedback_candidates",
            "feedback_id": feedback_id,
            "source_projection_id": projection_id,
            "source_transaction_id": source_transaction_id,
            "source_causal_event_digest": str(event.get("record_digest", "")),
            "source_indra_qi_world_state_digest": source_indra_digest,
            "source_feedback_packet_digest": feedback_packet["feedback_packet_digest"],
            "source_approval_handoff_digest": approval_handoff["approval_handoff_digest"],
            "candidate_count": len(candidates),
            "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
            "boundary": {
                "append_only_feedback_lineage": True,
                "source_indra_state_unchanged": True,
                "source_causal_event_consumed_once": True,
                "candidate_feedback_not_direct_mutation": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(feedback_ledger_path, ledger_record)

    status = READY if feedback_status == "feedback_candidates_ready" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-causal-feedback-"
        + sha(
            {
                "feedback_id": feedback_id,
                "source_event": event.get("record_digest", ""),
                "candidate_count": len(candidates),
                "blockers": blockers,
            }
        )[:16],
        "feedback_id": feedback_id,
        "source_world_model_id": source_world_model_id,
        "causal_world_id": causal_world_id,
        "source_projection_id": projection_id,
        "source_transaction_id": source_transaction_id,
        "source_event_kind": str(event.get("command_kind", "")),
        "feedback_status": feedback_status,
        "candidate_count": len(candidates),
        "local_patch_candidate_count": local_count,
        "qi_flow_candidate_count": flow_count,
        "source_indra_state_unchanged": source_unchanged,
        "source_indra_state_digest": source_indra_digest,
        "source_causal_world_model_digest": str(event.get("after_world_model_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "feedback_candidates_emitted": feedback_status == "feedback_candidates_ready",
            "approval_handoff_emitted": feedback_status == "feedback_candidates_ready",
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiCausalFeedbackBridgeV0_3Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        feedback_id,
        source_world_model_id,
        causal_world_id,
        projection_id,
        source_transaction_id,
        str(event.get("command_kind", "")),
        feedback_status,
        len(candidates),
        local_count,
        flow_count,
        source_unchanged,
        source_indra_digest,
        str(event.get("after_world_model_digest", "")),
        str(feedback_packet_path),
        str(approval_handoff_path),
        str(feedback_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

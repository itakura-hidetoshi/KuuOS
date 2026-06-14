#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_process_tensor_activation_core_v0_4 import (
    ALLOWED_FEEDBACK_KINDS,
    REQUIRED_BOUNDARY,
    activation_plan_digest,
    assess_candidate,
    assessment_blockers,
    build_overlay,
    items,
    mapping,
    protected_structure_digest,
    sha,
    valid_digest,
    validate_plan,
    validate_review_decisions,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    REQUIRED_PROCESS_CONTEXT,
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_process_tensor_activation_v0_4"
READY = "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_READY"
BLOCKED = "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_BLOCKED"
LICENSE_READY = "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiProcessTensorActivationV0_4Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_id: str
    source_feedback_id: str
    activation_status: str
    reviewed_candidate_count: int
    approved_candidate_count: int
    rejected_candidate_count: int
    overlays_applied: int
    world_state_mutated: bool
    rollback_snapshot_written: bool
    rollback_performed: bool
    protected_structure_preserved: bool
    before_world_state_digest: str
    after_world_state_digest: str
    process_tensor_review_digest: str
    world_state_path: str
    rollback_snapshot_path: str
    process_tensor_review_path: str
    activation_record_path: str
    mutation_ledger_path: str
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
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:128] or "invalid"


def _validate_feedback_sources(
    feedback_packet: Mapping[str, Any],
    approval_handoff: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, str]:
    if not feedback_packet:
        blockers.append("source_feedback_packet_missing_or_invalid")
        return "", ""
    if not approval_handoff:
        blockers.append("source_approval_handoff_missing_or_invalid")
    if feedback_packet.get("version") != "indra_qi_causal_feedback_bridge_v0_3":
        blockers.append("source_feedback_packet_version_invalid")
    if feedback_packet.get("feedback_status") != "feedback_candidates_ready":
        blockers.append("source_feedback_packet_not_ready")
    if not valid_digest(feedback_packet, "feedback_packet_digest"):
        blockers.append("source_feedback_packet_digest_invalid")
    if approval_handoff:
        if approval_handoff.get("version") != "indra_qi_causal_feedback_approval_handoff_v0_3":
            blockers.append("source_approval_handoff_version_invalid")
        if approval_handoff.get("handoff_status") != "approval_required":
            blockers.append("source_approval_handoff_status_invalid")
        if not valid_digest(approval_handoff, "approval_handoff_digest"):
            blockers.append("source_approval_handoff_digest_invalid")
        if str(approval_handoff.get("source_feedback_packet_digest", "")) != str(
            feedback_packet.get("feedback_packet_digest", "")
        ):
            blockers.append("source_feedback_handoff_digest_mismatch")
        for field in (
            "direct_application_allowed",
            "operator_algebra_mutation_allowed",
            "gauge_connection_mutation_allowed",
            "holonomy_replacement_allowed",
            "external_world_actuation_allowed",
        ):
            if approval_handoff.get(field) is not False:
                blockers.append(f"source_approval_handoff_{field}_not_false")
        if approval_handoff.get("required_next_stage") != "licensed_feedback_candidate_review_and_activation":
            blockers.append("source_approval_handoff_next_stage_invalid")
    packet_boundary = mapping(feedback_packet.get("boundary"))
    required_packet_boundary = {
        "feedback_is_candidate_not_direct_mutation": True,
        "source_indra_state_not_mutated": True,
        "causal_result_not_truth": True,
        "causal_edge_not_gauge_connection": True,
        "qi_feedback_not_qi_substance": True,
        "operator_algebra_unchanged": True,
        "gauge_connection_unchanged": True,
        "holonomy_preserved": True,
        "noncommutative_order_preserved": True,
        "non_markov_feedback_preserved": True,
        "candidate_weighting_not_truth": True,
        "not_direct_execution_authority": True,
        "not_world_update_authority": True,
        "approval_required_before_world_mutation": True,
    }
    for field, expected in required_packet_boundary.items():
        if packet_boundary.get(field) is not expected:
            blockers.append(f"source_feedback_boundary_{field}_mismatch")
    context = mapping(feedback_packet.get("source_process_tensor_context"))
    for field in REQUIRED_PROCESS_CONTEXT:
        if not str(context.get(field, "")).strip():
            blockers.append(f"source_feedback_process_context_{field}_missing")
    candidates = [mapping(value) for value in items(feedback_packet.get("feedback_candidates"))]
    ordering = [str(value) for value in items(feedback_packet.get("candidate_ordering"))]
    candidate_ids = [str(candidate.get("candidate_id", "")) for candidate in candidates]
    if not candidates:
        blockers.append("source_feedback_candidates_missing")
    if ordering != candidate_ids:
        blockers.append("source_feedback_candidate_order_mismatch")
    handoff_ids = [str(value) for value in items(approval_handoff.get("candidate_ids"))]
    if approval_handoff and handoff_ids != candidate_ids:
        blockers.append("source_feedback_handoff_candidate_order_mismatch")
    for index, candidate in enumerate(candidates):
        if candidate.get("feedback_kind") not in ALLOWED_FEEDBACK_KINDS:
            blockers.append(f"source_feedback_candidate_{index}_kind_invalid")
        boundary = mapping(candidate.get("boundary"))
        for field in (
            "candidate_only",
            "not_truth",
            "not_direct_world_mutation",
            "not_operator_algebra_mutation",
            "not_gauge_connection_mutation",
            "not_holonomy_replacement",
            "approval_required",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"source_feedback_candidate_{index}_{field}_not_true")
    return str(feedback_packet.get("feedback_id", "")), str(
        feedback_packet.get("source_indra_qi_world_state_digest", "")
    )


def build_indra_qi_process_tensor_activation_v0_4(
    *,
    runtime_context: Mapping[str, Any],
    activation_plan: Mapping[str, Any],
    activation_license: Mapping[str, Any],
) -> IndraQiProcessTensorActivationV0_4Result:
    context = mapping(runtime_context)
    plan = dict(mapping(activation_plan))
    license_value = mapping(activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    world_state_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    feedback_packet_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    approval_handoff_path = root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    process_tensor_review_path = root / "indra_qi_process_tensor_review_v0_4.json"
    activation_record_path = root / "indra_qi_process_tensor_activation_record_v0_4.json"
    mutation_ledger_path = root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
    receipt_path = root / "indra_qi_process_tensor_activation_receipt_v0_4.json"
    audit_path = root / "indra_qi_process_tensor_activation_audit_v0_4.jsonl"

    activation_id = str(plan.get("activation_id", ""))
    snapshot_path = root / f"indra_qi_world_rollback_snapshot_v0_4_{_safe_id(activation_id)}.json"

    if context.get("indra_qi_process_tensor_activation_v0_4_enabled") is not True:
        blockers.append("indra_qi_process_tensor_activation_v0_4_enabled_not_true")
    if context.get("apply_indra_qi_process_tensor_activation_v0_4") is not True:
        blockers.append("apply_indra_qi_process_tensor_activation_v0_4_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("indra_qi_process_tensor_activation_license_not_ready")
    required_flags = (
        "source_feedback_packet_read_allowed",
        "source_approval_handoff_read_allowed",
        "world_state_read_allowed",
        "activation_plan_validate_allowed",
        "process_tensor_review_write_allowed",
        "rollback_snapshot_write_allowed",
        "runtime_observation_overlay_write_allowed",
        "world_state_write_allowed",
        "post_write_verification_allowed",
        "activation_record_write_allowed",
        "mutation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "direct_world_model_mutation_allowed",
    )
    for flag in required_flags:
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("activation_plan_digest", ""))
    if str(license_value.get("bound_activation_plan_digest", "")) != plan_digest:
        blockers.append("activation_license_plan_digest_mismatch")
    if not activation_id:
        blockers.append("process_tensor_activation_id_missing")

    allowed_scopes = license_value.get("allowed_mutation_scopes", [])
    allowed_scope_set = {str(value) for value in allowed_scopes} if isinstance(allowed_scopes, list) else set()
    if allowed_scope_set != {"runtime_observation_overlays_only"}:
        blockers.append("activation_license_mutation_scope_not_exact")
    allowed_kinds_raw = license_value.get("allowed_feedback_kinds", [])
    allowed_kinds = {str(value) for value in allowed_kinds_raw} if isinstance(allowed_kinds_raw, list) else set()
    if allowed_kinds != ALLOWED_FEEDBACK_KINDS:
        blockers.append("activation_license_feedback_kinds_not_exact")
    maximum = license_value.get("max_approved_candidates")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
        blockers.append("activation_license_max_approved_candidates_invalid")
        maximum = 0

    feedback_packet = _read_json(feedback_packet_path)
    approval_handoff = _read_json(approval_handoff_path)
    source_feedback_id, source_indra_digest = _validate_feedback_sources(
        feedback_packet, approval_handoff, blockers
    )
    if str(plan.get("source_feedback_id", "")) != source_feedback_id:
        blockers.append("process_tensor_activation_source_feedback_id_mismatch")
    if str(plan.get("source_feedback_packet_digest", "")) != str(
        feedback_packet.get("feedback_packet_digest", "")
    ):
        blockers.append("process_tensor_activation_source_feedback_packet_digest_mismatch")
    if str(plan.get("source_approval_handoff_digest", "")) != str(
        approval_handoff.get("approval_handoff_digest", "")
    ):
        blockers.append("process_tensor_activation_source_handoff_digest_mismatch")
    if str(plan.get("source_indra_qi_world_state_digest", "")) != source_indra_digest:
        blockers.append("process_tensor_activation_source_indra_digest_mismatch")

    world_state = _read_json(world_state_path)
    if not world_state:
        blockers.append("indra_qi_world_state_missing_or_invalid")
    before_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    if before_digest != source_indra_digest:
        blockers.append("indra_qi_world_state_source_digest_mismatch")
    if world_state and compute_indra_qi_world_state_digest(world_state) != before_digest:
        blockers.append("indra_qi_world_state_digest_invalid")
    before_protected_digest = protected_structure_digest(world_state) if world_state else ""

    ledger_records = _records(mutation_ledger_path)
    if activation_id and any(str(record.get("activation_id", "")) == activation_id for record in ledger_records):
        blockers.append("process_tensor_activation_id_replay")
    if source_feedback_id and any(
        str(record.get("source_feedback_id", "")) == source_feedback_id for record in ledger_records
    ):
        blockers.append("source_feedback_activation_replay")

    candidates = [mapping(value) for value in items(feedback_packet.get("feedback_candidates"))]
    decisions = validate_review_decisions(plan, candidates, blockers)
    prior_overlays = [mapping(value) for value in items(world_state.get("runtime_observation_overlays"))]
    policy = mapping(plan.get("process_tensor_policy"))
    assessments: list[dict[str, Any]] = []
    approved: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
    rejected_ids: list[str] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        decision = decisions.get(candidate_id, {})
        assessment = assess_candidate(
            feedback_packet=feedback_packet,
            candidate=candidate,
            decision=decision,
            prior_overlays=prior_overlays,
            plan=plan,
        )
        assessment["review_decision"] = dict(decision)
        assessment["admissibility_blockers"] = assessment_blockers(
            candidate=candidate,
            decision=decision,
            assessment=assessment,
            policy=policy,
        )
        assessment["admitted"] = decision.get("decision") == "approve" and not assessment[
            "admissibility_blockers"
        ]
        assessment["assessment_digest"] = sha(
            {key: value for key, value in assessment.items() if key != "assessment_digest"}
        )
        assessments.append(assessment)
        if decision.get("decision") == "approve":
            if assessment["admissibility_blockers"]:
                blockers.extend(assessment["admissibility_blockers"])
            else:
                approved.append((candidate, assessment))
        elif decision.get("decision") == "reject":
            rejected_ids.append(candidate_id)
    if not approved:
        blockers.append("process_tensor_activation_no_admissible_candidates")
    if len(approved) > maximum:
        blockers.append("process_tensor_activation_approved_candidate_limit_exceeded")
    for candidate, _ in approved:
        if str(candidate.get("feedback_kind", "")) not in allowed_kinds:
            blockers.append("process_tensor_activation_candidate_kind_not_licensed")

    review_record = {
        "version": "indra_qi_process_tensor_review_v0_4",
        "review_status": "admissible" if not blockers else "blocked",
        "activation_id": activation_id,
        "source_feedback_id": source_feedback_id,
        "source_feedback_packet_digest": str(feedback_packet.get("feedback_packet_digest", "")),
        "activation_plan_digest": plan_digest,
        "assessments": assessments,
        "approved_candidate_ids": [str(candidate.get("candidate_id", "")) for candidate, _ in approved],
        "rejected_candidate_ids": rejected_ids,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "process_tensor_review_not_mutation": True,
            "process_tensor_review_not_approval_authority": True,
        },
        "epoch": int(time.time()),
    }
    review_record["process_tensor_review_digest"] = sha(review_record)
    review_digest = review_record["process_tensor_review_digest"]
    if license_value.get("process_tensor_review_write_allowed") is True:
        _write_json(process_tensor_review_path, review_record)

    state_mutated = False
    snapshot_written = False
    rollback_performed = False
    protected_preserved = False
    after_digest = before_digest
    overlays_applied = 0
    snapshot_record: dict[str, Any] = {}

    if not blockers:
        snapshot_record = {
            "version": "indra_qi_world_rollback_snapshot_v0_4",
            "activation_id": activation_id,
            "source_feedback_id": source_feedback_id,
            "before_world_state_digest": before_digest,
            "protected_structure_digest": before_protected_digest,
            "world_state": deepcopy(world_state),
            "epoch": int(time.time()),
        }
        snapshot_record["rollback_snapshot_digest"] = sha(snapshot_record)
        _write_json(snapshot_path, snapshot_record)
        snapshot_written = True

        next_state = deepcopy(world_state)
        overlays = list(items(next_state.get("runtime_observation_overlays")))
        previous_overlay_digest = (
            str(mapping(overlays[-1]).get("overlay_digest", "GENESIS")) if overlays else "GENESIS"
        )
        for sequence, (candidate, assessment) in enumerate(approved, start=1):
            overlay = build_overlay(
                activation_id=activation_id,
                sequence=sequence,
                candidate=candidate,
                assessment=assessment,
                feedback_packet_digest=str(feedback_packet.get("feedback_packet_digest", "")),
                previous_overlay_digest=previous_overlay_digest,
            )
            overlays.append(overlay)
            previous_overlay_digest = overlay["overlay_digest"]
        next_state["runtime_observation_overlays"] = overlays
        revision_raw = next_state.get("world_mutation_revision", 0)
        revision = revision_raw if isinstance(revision_raw, int) and not isinstance(revision_raw, bool) else 0
        next_state["world_mutation_revision"] = revision + 1
        next_state["last_process_tensor_activation_id"] = activation_id
        next_state["last_process_tensor_review_digest"] = review_digest
        next_state["last_feedback_packet_digest"] = str(feedback_packet.get("feedback_packet_digest", ""))
        next_state["last_runtime_overlay_digest"] = previous_overlay_digest
        next_state["indra_qi_world_state_digest"] = compute_indra_qi_world_state_digest(next_state)

        try:
            _write_json(world_state_path, next_state)
            verified = _read_json(world_state_path)
            after_digest = str(verified.get("indra_qi_world_state_digest", ""))
            digest_valid = bool(after_digest) and compute_indra_qi_world_state_digest(verified) == after_digest
            protected_preserved = protected_structure_digest(verified) == before_protected_digest
            overlays_verified = len(items(verified.get("runtime_observation_overlays"))) == len(overlays)
            if not digest_valid:
                blockers.append("post_write_world_state_digest_invalid")
            if not protected_preserved:
                blockers.append("post_write_protected_structure_changed")
            if not overlays_verified:
                blockers.append("post_write_overlay_count_mismatch")
            if blockers:
                _write_json(world_state_path, world_state)
                rollback_performed = True
                after_digest = before_digest
            else:
                state_mutated = True
                overlays_applied = len(approved)
        except OSError:
            blockers.append("world_state_write_failed")
            try:
                _write_json(world_state_path, world_state)
                rollback_performed = True
            except OSError:
                warnings.append("rollback_restore_write_failed")

    activation_status = "process_tensor_activation_completed" if state_mutated and not blockers else "process_tensor_activation_blocked"
    activation_record: dict[str, Any] = {}
    if activation_status == "process_tensor_activation_completed":
        activation_record = {
            "version": "indra_qi_process_tensor_activation_record_v0_4",
            "activation_status": activation_status,
            "activation_id": activation_id,
            "source_feedback_id": source_feedback_id,
            "source_feedback_packet_digest": str(feedback_packet.get("feedback_packet_digest", "")),
            "source_approval_handoff_digest": str(approval_handoff.get("approval_handoff_digest", "")),
            "activation_plan_digest": plan_digest,
            "process_tensor_review_digest": review_digest,
            "rollback_snapshot_digest": str(snapshot_record.get("rollback_snapshot_digest", "")),
            "before_world_state_digest": before_digest,
            "after_world_state_digest": after_digest,
            "approved_candidate_ids": [str(candidate.get("candidate_id", "")) for candidate, _ in approved],
            "rejected_candidate_ids": rejected_ids,
            "overlays_applied": overlays_applied,
            "protected_structure_digest": before_protected_digest,
            "protected_structure_preserved": protected_preserved,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "world_state_mutated": True,
                "mutation_restricted_to_runtime_observation_overlays": True,
                "post_write_verification_completed": True,
                "rollback_corridor_preserved": True,
            },
            "epoch": int(time.time()),
        }
        activation_record["activation_record_digest"] = sha(activation_record)
        _write_json(activation_record_path, activation_record)

        ledger_record = {
            "version": "indra_qi_world_observation_overlay_ledger_record_v0_4",
            "record_type": "indra_qi_process_tensor_activation",
            "activation_id": activation_id,
            "source_feedback_id": source_feedback_id,
            "source_feedback_packet_digest": str(feedback_packet.get("feedback_packet_digest", "")),
            "source_process_tensor_review_digest": review_digest,
            "source_activation_record_digest": activation_record["activation_record_digest"],
            "before_world_state_digest": before_digest,
            "after_world_state_digest": after_digest,
            "overlays_applied": overlays_applied,
            "prev_record_digest": str(ledger_records[-1].get("record_digest", "GENESIS")) if ledger_records else "GENESIS",
            "boundary": {
                "append_only_mutation_lineage": True,
                "runtime_observation_overlay_only": True,
                "protected_structure_preserved": True,
                "rollback_snapshot_available": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(mutation_ledger_path, ledger_record)

    status = READY if activation_status == "process_tensor_activation_completed" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-process-tensor-activation-"
        + sha(
            {
                "activation_id": activation_id,
                "before_digest": before_digest,
                "after_digest": after_digest,
                "review_digest": review_digest,
                "blockers": blockers,
            }
        )[:16],
        "activation_id": activation_id,
        "source_feedback_id": source_feedback_id,
        "activation_status": activation_status,
        "reviewed_candidate_count": len(candidates),
        "approved_candidate_count": len(approved),
        "rejected_candidate_count": len(rejected_ids),
        "overlays_applied": overlays_applied,
        "world_state_mutated": state_mutated,
        "rollback_snapshot_written": snapshot_written,
        "rollback_performed": rollback_performed,
        "protected_structure_preserved": protected_preserved,
        "before_world_state_digest": before_digest,
        "after_world_state_digest": after_digest,
        "process_tensor_review_digest": review_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "activation_completed": activation_status == "process_tensor_activation_completed",
            "external_world_not_actuated": True,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiProcessTensorActivationV0_4Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        activation_id,
        source_feedback_id,
        activation_status,
        len(candidates),
        len(approved),
        len(rejected_ids),
        overlays_applied,
        state_mutated,
        snapshot_written,
        rollback_performed,
        protected_preserved,
        before_digest,
        after_digest,
        review_digest,
        str(world_state_path),
        str(snapshot_path),
        str(process_tensor_review_path),
        str(activation_record_path),
        str(mutation_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

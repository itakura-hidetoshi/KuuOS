#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_child_feedback_cycle_core_v0_10 import (
    REQUIRED_BOUNDARY,
    bridge_plan_digest,
    build_activation_plan,
    build_cycle_plan,
    items,
    mapping,
    sha,
    valid_digest,
    validate_activation_license_template,
    validate_cycle_license_template,
    validate_plan,
)
from runtime.kuuos_indra_qi_process_tensor_activation_core_v0_4 import (
    protected_structure_digest,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import (
    cycle_state_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_process_tensor_activation_v0_4 import (
    build_indra_qi_process_tensor_activation_v0_4,
)
from runtime.kuuos_runtime_daemon_indra_qi_process_tensor_cycle_v0_5 import (
    build_indra_qi_process_tensor_cycle_v0_5,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_child_feedback_parent_cycle_v0_10"
READY = "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_READY"
BLOCKED = "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_BLOCKED"
LICENSE_READY = "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiChildFeedbackParentCycleV0_10Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_id: str
    source_execution_id: str
    source_child_feedback_id: str
    handoff_status: str
    child_feedback_staged: bool
    v0_4_activation_invoked: bool
    v0_4_activation_ready: bool
    v0_5_cycle_invoked: bool
    v0_5_cycle_ready: bool
    transaction_rolled_back: bool
    rollback_reason: str
    approved_candidate_count: int
    overlays_applied: int
    cycle_index: int
    channel_count: int
    seed_entry_count: int
    before_parent_world_state_digest: str
    after_parent_world_state_digest: str
    previous_cycle_state_digest: str
    process_tensor_cycle_state_digest: str
    next_cycle_seed_packet_digest: str
    child_feedback_packet_digest: str
    child_feedback_handoff_digest: str
    handoff_packet_digest: str
    handoff_packet_path: str
    bridge_record_path: str
    bridge_ledger_path: str
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


def _latest_matching(
    records: list[dict[str, Any]], field: str, expected: str
) -> Mapping[str, Any]:
    for record in reversed(records):
        if str(record.get(field, "")) == expected:
            return record
    return {}


def _snapshot_files(paths: list[pathlib.Path]) -> dict[pathlib.Path, bytes | None]:
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def _restore_files(snapshot: Mapping[pathlib.Path, bytes | None]) -> None:
    for path, content in snapshot.items():
        if content is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".restore.tmp")
        temporary.write_bytes(content)
        os.replace(temporary, path)


def _validate_execution_lineage(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    pathlib.Path,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    execution = _read_json(
        root / "indra_qi_approved_recovery_action_execution_record_v0_9.json"
    )
    execution_records = _records(
        root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
    )
    reentry = _read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    parent_world = _read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")

    if not execution:
        blockers.append("child_feedback_cycle_source_execution_record_missing_or_invalid")
    else:
        if execution.get("version") != "indra_qi_approved_recovery_action_execution_record_v0_9":
            blockers.append("child_feedback_cycle_source_execution_version_invalid")
        if execution.get("execution_status") != "approved_action_applied_and_feedback_returned":
            blockers.append("child_feedback_cycle_source_execution_not_ready")
        if not valid_digest(execution, "execution_record_digest"):
            blockers.append("child_feedback_cycle_source_execution_digest_invalid")
        for field in (
            "exact_candidate_executed_once",
            "child_v14_action_traceable",
            "feedback_returned_as_candidates",
            "external_world_actuation_authority",
        ):
            expected = False if field == "external_world_actuation_authority" else True
            if mapping(execution.get("boundary")).get(field) is not expected:
                blockers.append(f"child_feedback_cycle_source_execution_boundary_{field}_mismatch")

    execution_id = str(execution.get("execution_id", ""))
    execution_ledger = _latest_matching(execution_records, "execution_id", execution_id)
    if not execution_ledger:
        blockers.append("child_feedback_cycle_source_execution_ledger_missing")
    else:
        if not valid_digest(execution_ledger, "record_digest"):
            blockers.append("child_feedback_cycle_source_execution_ledger_digest_invalid")
        if str(execution_ledger.get("source_execution_record_digest", "")) != str(
            execution.get("execution_record_digest", "")
        ):
            blockers.append("child_feedback_cycle_source_execution_ledger_record_mismatch")
        if str(execution_ledger.get("feedback_packet_digest", "")) != str(
            execution.get("feedback_packet_digest", "")
        ):
            blockers.append("child_feedback_cycle_source_execution_ledger_feedback_mismatch")

    if not reentry:
        blockers.append("child_feedback_cycle_source_reentry_record_missing_or_invalid")
    else:
        if reentry.get("version") != "indra_qi_post_assimilation_causal_reentry_record_v0_7":
            blockers.append("child_feedback_cycle_source_reentry_version_invalid")
        if reentry.get("reentry_status") != "post_assimilation_causal_world_initialized":
            blockers.append("child_feedback_cycle_source_reentry_not_ready")
        if not valid_digest(reentry, "reentry_record_digest"):
            blockers.append("child_feedback_cycle_source_reentry_digest_invalid")
        if str(execution.get("source_reentry_id", "")) != str(reentry.get("reentry_id", "")):
            blockers.append("child_feedback_cycle_execution_reentry_id_mismatch")
        if str(execution.get("source_reentry_record_digest", "")) != str(
            reentry.get("reentry_record_digest", "")
        ):
            blockers.append("child_feedback_cycle_execution_reentry_digest_mismatch")

    if not parent_world:
        blockers.append("child_feedback_cycle_parent_world_missing_or_invalid")
    parent_digest = str(parent_world.get("indra_qi_world_state_digest", ""))
    if parent_world and compute_indra_qi_world_state_digest(parent_world) != parent_digest:
        blockers.append("child_feedback_cycle_parent_world_digest_invalid")
    if parent_digest != str(execution.get("source_world_state_digest", "")):
        blockers.append("child_feedback_cycle_parent_world_execution_digest_mismatch")

    expected = {
        "source_execution_id": execution_id,
        "source_execution_record_digest": str(execution.get("execution_record_digest", "")),
        "source_execution_ledger_record_digest": str(execution_ledger.get("record_digest", "")),
        "source_reentry_id": str(reentry.get("reentry_id", "")),
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_parent_world_state_digest": parent_digest,
        "source_child_feedback_id": str(execution.get("feedback_id", "")),
        "source_child_feedback_packet_digest": str(execution.get("feedback_packet_digest", "")),
    }
    for field, expected_value in expected.items():
        if str(plan.get(field, "")) != expected_value:
            blockers.append(f"child_feedback_cycle_plan_{field}_mismatch")

    child_raw = str(reentry.get("child_runtime_root", ""))
    child_root = pathlib.Path(child_raw).expanduser().resolve() if child_raw else root
    allowed_parent = (root / "indra_qi_causal_reentry_cycles_v0_7").resolve()
    try:
        child_root.relative_to(allowed_parent)
    except ValueError:
        blockers.append("child_feedback_cycle_child_runtime_outside_allowed_root")
    if not child_root.is_dir():
        blockers.append("child_feedback_cycle_child_runtime_missing")

    child_feedback = _read_json(
        child_root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    )
    child_handoff = _read_json(
        child_root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    )
    child_feedback_records = _records(
        child_root / "indra_qi_causal_feedback_ledger_v0_3.jsonl"
    )
    child_feedback_ledger = _latest_matching(
        child_feedback_records,
        "feedback_id",
        str(child_feedback.get("feedback_id", "")),
    )
    child_state = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
    child_indra = _read_json(child_root / "ku_indra_qi_noncommutative_mandala_world_state.json")

    if not child_feedback:
        blockers.append("child_feedback_cycle_child_feedback_packet_missing_or_invalid")
    else:
        if child_feedback.get("version") != "indra_qi_causal_feedback_bridge_v0_3":
            blockers.append("child_feedback_cycle_child_feedback_version_invalid")
        if child_feedback.get("feedback_status") != "feedback_candidates_ready":
            blockers.append("child_feedback_cycle_child_feedback_not_ready")
        if not valid_digest(child_feedback, "feedback_packet_digest"):
            blockers.append("child_feedback_cycle_child_feedback_digest_invalid")
        if str(child_feedback.get("feedback_id", "")) != str(
            plan.get("source_child_feedback_id", "")
        ):
            blockers.append("child_feedback_cycle_child_feedback_id_mismatch")
        if str(child_feedback.get("feedback_packet_digest", "")) != str(
            plan.get("source_child_feedback_packet_digest", "")
        ):
            blockers.append("child_feedback_cycle_child_feedback_packet_digest_mismatch")
        if str(child_feedback.get("source_causal_event_digest", "")) != str(
            execution.get("action_event_record_digest", "")
        ):
            blockers.append("child_feedback_cycle_child_feedback_event_digest_mismatch")
        if str(child_feedback.get("source_indra_qi_world_state_digest", "")) != parent_digest:
            blockers.append("child_feedback_cycle_child_feedback_parent_world_digest_mismatch")
        boundary = mapping(child_feedback.get("boundary"))
        for field in (
            "feedback_is_candidate_not_direct_mutation",
            "source_indra_state_not_mutated",
            "causal_result_not_truth",
            "causal_edge_not_gauge_connection",
            "qi_feedback_not_qi_substance",
            "operator_algebra_unchanged",
            "gauge_connection_unchanged",
            "holonomy_preserved",
            "non_markov_feedback_preserved",
            "candidate_weighting_not_truth",
            "not_direct_execution_authority",
            "not_world_update_authority",
            "approval_required_before_world_mutation",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"child_feedback_cycle_child_feedback_boundary_{field}_not_true")

    if not child_handoff:
        blockers.append("child_feedback_cycle_child_feedback_handoff_missing_or_invalid")
    else:
        if child_handoff.get("version") != "indra_qi_causal_feedback_approval_handoff_v0_3":
            blockers.append("child_feedback_cycle_child_feedback_handoff_version_invalid")
        if child_handoff.get("handoff_status") != "approval_required":
            blockers.append("child_feedback_cycle_child_feedback_handoff_not_ready")
        if not valid_digest(child_handoff, "approval_handoff_digest"):
            blockers.append("child_feedback_cycle_child_feedback_handoff_digest_invalid")
        if str(child_handoff.get("source_feedback_packet_digest", "")) != str(
            child_feedback.get("feedback_packet_digest", "")
        ):
            blockers.append("child_feedback_cycle_child_feedback_handoff_packet_mismatch")
        if str(plan.get("source_child_feedback_handoff_digest", "")) != str(
            child_handoff.get("approval_handoff_digest", "")
        ):
            blockers.append("child_feedback_cycle_plan_child_feedback_handoff_digest_mismatch")

    if not child_feedback_ledger:
        blockers.append("child_feedback_cycle_child_feedback_ledger_missing")
    else:
        if not valid_digest(child_feedback_ledger, "record_digest"):
            blockers.append("child_feedback_cycle_child_feedback_ledger_digest_invalid")
        if str(child_feedback_ledger.get("source_feedback_packet_digest", "")) != str(
            child_feedback.get("feedback_packet_digest", "")
        ):
            blockers.append("child_feedback_cycle_child_feedback_ledger_packet_mismatch")

    if not valid_v14_digest(child_state, "world_model_digest"):
        blockers.append("child_feedback_cycle_child_v14_state_digest_invalid")
    if str(child_state.get("world_model_digest", "")) != str(
        execution.get("after_v14_world_model_digest", "")
    ):
        blockers.append("child_feedback_cycle_child_v14_execution_digest_mismatch")
    child_indra_digest = str(child_indra.get("indra_qi_world_state_digest", ""))
    if not child_indra or compute_indra_qi_world_state_digest(child_indra) != child_indra_digest:
        blockers.append("child_feedback_cycle_child_indra_state_digest_invalid")
    if child_indra_digest != parent_digest:
        blockers.append("child_feedback_cycle_child_indra_parent_digest_mismatch")

    candidates = [mapping(value) for value in items(child_feedback.get("feedback_candidates"))]
    candidate_ids = [str(value.get("candidate_id", "")) for value in candidates]
    approved = [str(value) for value in items(plan.get("approved_candidate_ids"))]
    if not set(approved).issubset(set(candidate_ids)):
        blockers.append("child_feedback_cycle_approved_candidate_not_in_child_packet")
    if candidate_ids != [str(value) for value in items(child_feedback.get("candidate_ordering"))]:
        blockers.append("child_feedback_cycle_child_feedback_ordering_mismatch")

    return (
        execution,
        execution_ledger,
        reentry,
        child_root,
        child_feedback,
        child_handoff,
        parent_world,
    )


def build_indra_qi_child_feedback_parent_cycle_v0_10(
    *,
    runtime_context: Mapping[str, Any],
    bridge_plan: Mapping[str, Any],
    bridge_license: Mapping[str, Any],
) -> IndraQiChildFeedbackParentCycleV0_10Result:
    context = mapping(runtime_context)
    plan = dict(mapping(bridge_plan))
    license_value = mapping(bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    if context.get("indra_qi_child_feedback_parent_cycle_v0_10_enabled") is not True:
        blockers.append("indra_qi_child_feedback_parent_cycle_v0_10_enabled_not_true")
    if context.get("apply_indra_qi_child_feedback_parent_cycle_v0_10") is not True:
        blockers.append("apply_indra_qi_child_feedback_parent_cycle_v0_10_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("child_feedback_cycle_bridge_license_not_ready")
    for flag in (
        "source_execution_lineage_read_allowed",
        "source_reentry_read_allowed",
        "child_feedback_read_allowed",
        "parent_world_read_allowed",
        "parent_feedback_stage_write_allowed",
        "transaction_snapshot_allowed",
        "transaction_restore_allowed",
        "v0_4_activation_invoke_allowed",
        "v0_5_cycle_invoke_allowed",
        "handoff_packet_write_allowed",
        "bridge_record_write_allowed",
        "bridge_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("bridge_plan_digest", ""))
    if str(license_value.get("bound_bridge_plan_digest", "")) != plan_digest:
        blockers.append("child_feedback_cycle_bridge_license_plan_digest_mismatch")
    approved_count = len(items(plan.get("approved_candidate_ids")))
    activation_template = mapping(license_value.get("v0_4_activation_license_template"))
    cycle_template = mapping(license_value.get("v0_5_cycle_license_template"))
    validate_activation_license_template(activation_template, approved_count, blockers)
    validate_cycle_license_template(cycle_template, blockers)

    (
        execution,
        execution_ledger,
        reentry,
        child_root,
        child_feedback,
        child_handoff,
        parent_world,
    ) = _validate_execution_lineage(root=root, plan=plan, blockers=blockers)

    bridge_id = str(plan.get("bridge_id", ""))
    source_execution_id = str(execution.get("execution_id", ""))
    child_feedback_id = str(child_feedback.get("feedback_id", ""))
    child_feedback_digest = str(child_feedback.get("feedback_packet_digest", ""))
    child_handoff_digest = str(child_handoff.get("approval_handoff_digest", ""))
    before_parent_digest = str(parent_world.get("indra_qi_world_state_digest", ""))
    before_protected_digest = protected_structure_digest(parent_world) if parent_world else ""

    bridge_ledger_path = root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl"
    prior_bridge_records = _records(bridge_ledger_path)
    if bridge_id and any(str(value.get("bridge_id", "")) == bridge_id for value in prior_bridge_records):
        blockers.append("child_feedback_cycle_bridge_id_replay")
    if source_execution_id and any(
        str(value.get("source_execution_id", "")) == source_execution_id
        for value in prior_bridge_records
    ):
        blockers.append("child_feedback_cycle_source_execution_replay")
    if child_feedback_digest and any(
        str(value.get("source_child_feedback_packet_digest", "")) == child_feedback_digest
        for value in prior_bridge_records
    ):
        blockers.append("child_feedback_cycle_child_feedback_replay")

    parent_feedback_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    parent_handoff_path = root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    world_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    review_path = root / "indra_qi_process_tensor_review_v0_4.json"
    activation_record_path = root / "indra_qi_process_tensor_activation_record_v0_4.json"
    mutation_ledger_path = root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
    activation_receipt_path = root / "indra_qi_process_tensor_activation_receipt_v0_4.json"
    activation_audit_path = root / "indra_qi_process_tensor_activation_audit_v0_4.jsonl"
    rollback_snapshot_path = root / (
        "indra_qi_world_rollback_snapshot_v0_4_"
        + _safe_id(str(plan.get("activation_id", "")))
        + ".json"
    )
    cycle_state_path = root / "indra_qi_process_tensor_cycle_state_v0_5.json"
    seed_path = root / "indra_qi_next_cycle_projection_seed_v0_5.json"
    cycle_ledger_path = root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl"
    cycle_receipt_path = root / "indra_qi_process_tensor_cycle_receipt_v0_5.json"
    cycle_audit_path = root / "indra_qi_process_tensor_cycle_audit_v0_5.jsonl"

    previous_cycle_state = _read_json(cycle_state_path)
    previous_cycle_digest = (
        str(previous_cycle_state.get("process_tensor_cycle_state_digest", ""))
        if previous_cycle_state
        else "GENESIS"
    )
    if previous_cycle_state and cycle_state_digest(previous_cycle_state) != previous_cycle_digest:
        blockers.append("child_feedback_cycle_previous_cycle_state_digest_invalid")
    if str(plan.get("expected_previous_cycle_state_digest", "")) != previous_cycle_digest:
        blockers.append("child_feedback_cycle_expected_previous_cycle_digest_mismatch")
    previous_cycle_records = _records(cycle_ledger_path)
    if previous_cycle_state and previous_cycle_records:
        latest_cycle = previous_cycle_records[-1]
        if not valid_digest(latest_cycle, "record_digest"):
            blockers.append("child_feedback_cycle_previous_cycle_ledger_digest_invalid")
        if str(latest_cycle.get("process_tensor_cycle_state_digest", "")) != previous_cycle_digest:
            blockers.append("child_feedback_cycle_previous_cycle_ledger_state_mismatch")

    touched_paths = [
        parent_feedback_path,
        parent_handoff_path,
        world_path,
        review_path,
        activation_record_path,
        mutation_ledger_path,
        activation_receipt_path,
        activation_audit_path,
        rollback_snapshot_path,
        cycle_state_path,
        seed_path,
        cycle_ledger_path,
        cycle_receipt_path,
        cycle_audit_path,
    ]
    transaction_snapshot = _snapshot_files(touched_paths) if not blockers else {}

    child_feedback_staged = False
    activation_invoked = False
    activation_ready = False
    cycle_invoked = False
    cycle_ready = False
    rolled_back = False
    rollback_reason = ""
    overlays_applied = 0
    cycle_index = int(previous_cycle_state.get("cycle_index", 0) or 0) if previous_cycle_state else 0
    channel_count = 0
    seed_count = 0
    after_parent_digest = before_parent_digest
    cycle_digest = ""
    seed_digest = ""
    activation_plan: dict[str, Any] = {}
    cycle_plan: dict[str, Any] = {}
    activation_record: dict[str, Any] = {}
    review: dict[str, Any] = {}
    cycle_state: dict[str, Any] = {}
    seed_packet: dict[str, Any] = {}

    child_state_before = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
    child_indra_before = _read_json(
        child_root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    )
    child_feedback_before = _read_json(
        child_root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    )
    child_handoff_before = _read_json(
        child_root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    )

    if not blockers:
        _write_json(parent_feedback_path, child_feedback)
        _write_json(parent_handoff_path, child_handoff)
        staged_feedback = _read_json(parent_feedback_path)
        staged_handoff = _read_json(parent_handoff_path)
        child_feedback_staged = (
            str(staged_feedback.get("feedback_packet_digest", "")) == child_feedback_digest
            and valid_digest(staged_feedback, "feedback_packet_digest")
            and str(staged_handoff.get("approval_handoff_digest", "")) == child_handoff_digest
            and valid_digest(staged_handoff, "approval_handoff_digest")
        )
        if not child_feedback_staged:
            blockers.append("child_feedback_cycle_parent_feedback_stage_verification_failed")

    if not blockers:
        activation_plan = build_activation_plan(
            plan=plan,
            feedback_packet=child_feedback,
            feedback_handoff=child_handoff,
            parent_world_digest=before_parent_digest,
        )
        activation_license = dict(activation_template)
        activation_license["bound_activation_plan_digest"] = activation_plan[
            "activation_plan_digest"
        ]
        activation_invoked = True
        activation_result = build_indra_qi_process_tensor_activation_v0_4(
            runtime_context={
                "runtime_root": str(root),
                "indra_qi_process_tensor_activation_v0_4_enabled": True,
                "apply_indra_qi_process_tensor_activation_v0_4": True,
            },
            activation_plan=activation_plan,
            activation_license=activation_license,
        ).to_dict()
        if activation_result.get("status") != "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_READY":
            blockers.append("child_feedback_cycle_v0_4_activation_not_ready")
            blockers.extend(
                f"nested_v0_4:{value}" for value in items(activation_result.get("blockers"))
            )
        else:
            activation_ready = True
            overlays_applied = int(activation_result.get("overlays_applied", 0) or 0)

    if activation_ready and not blockers:
        parent_after_activation = _read_json(world_path)
        after_parent_digest = str(
            parent_after_activation.get("indra_qi_world_state_digest", "")
        )
        if compute_indra_qi_world_state_digest(parent_after_activation) != after_parent_digest:
            blockers.append("child_feedback_cycle_parent_world_after_activation_digest_invalid")
        if after_parent_digest == before_parent_digest:
            blockers.append("child_feedback_cycle_parent_world_not_changed_by_v0_4")
        if protected_structure_digest(parent_after_activation) != before_protected_digest:
            blockers.append("child_feedback_cycle_parent_protected_structure_changed")
        review = _read_json(review_path)
        activation_record = _read_json(activation_record_path)
        activation_records = _records(mutation_ledger_path)
        activation_ledger = _latest_matching(
            activation_records,
            "activation_id",
            str(plan.get("activation_id", "")),
        )
        if not valid_digest(review, "process_tensor_review_digest"):
            blockers.append("child_feedback_cycle_v0_4_review_digest_invalid")
        if review.get("review_status") != "admissible":
            blockers.append("child_feedback_cycle_v0_4_review_not_admissible")
        if not valid_digest(activation_record, "activation_record_digest"):
            blockers.append("child_feedback_cycle_v0_4_activation_record_digest_invalid")
        if activation_record.get("activation_status") != "process_tensor_activation_completed":
            blockers.append("child_feedback_cycle_v0_4_activation_record_not_completed")
        if str(activation_record.get("source_feedback_packet_digest", "")) != child_feedback_digest:
            blockers.append("child_feedback_cycle_v0_4_activation_feedback_digest_mismatch")
        if str(activation_record.get("after_world_state_digest", "")) != after_parent_digest:
            blockers.append("child_feedback_cycle_v0_4_activation_world_digest_mismatch")
        if int(activation_record.get("overlays_applied", -1) or -1) != approved_count:
            blockers.append("child_feedback_cycle_v0_4_overlay_count_mismatch")
        if not valid_digest(activation_ledger, "record_digest"):
            blockers.append("child_feedback_cycle_v0_4_mutation_ledger_digest_invalid")
        if str(activation_ledger.get("source_activation_record_digest", "")) != str(
            activation_record.get("activation_record_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_4_mutation_ledger_activation_mismatch")

    if activation_ready and not blockers:
        cycle_plan = build_cycle_plan(
            plan=plan,
            activation_record=activation_record,
            review=review,
            parent_world_digest=after_parent_digest,
        )
        cycle_license = dict(cycle_template)
        cycle_license["bound_cycle_plan_digest"] = cycle_plan["cycle_plan_digest"]
        cycle_invoked = True
        cycle_result = build_indra_qi_process_tensor_cycle_v0_5(
            runtime_context={
                "runtime_root": str(root),
                "indra_qi_process_tensor_cycle_v0_5_enabled": True,
                "evolve_indra_qi_process_tensor_cycle_v0_5": True,
            },
            cycle_plan=cycle_plan,
            cycle_license=cycle_license,
        ).to_dict()
        if cycle_result.get("status") != "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_READY":
            blockers.append("child_feedback_cycle_v0_5_cycle_not_ready")
            blockers.extend(
                f"nested_v0_5:{value}" for value in items(cycle_result.get("blockers"))
            )
        else:
            cycle_ready = True
            cycle_index = int(cycle_result.get("cycle_index", 0) or 0)
            channel_count = int(cycle_result.get("channel_count", 0) or 0)
            seed_count = int(cycle_result.get("seed_entry_count", 0) or 0)
            cycle_digest = str(cycle_result.get("process_tensor_cycle_state_digest", ""))
            seed_digest = str(cycle_result.get("next_cycle_seed_packet_digest", ""))

    if cycle_ready and not blockers:
        parent_after_cycle = _read_json(world_path)
        if str(parent_after_cycle.get("indra_qi_world_state_digest", "")) != after_parent_digest:
            blockers.append("child_feedback_cycle_parent_world_changed_during_v0_5")
        if compute_indra_qi_world_state_digest(parent_after_cycle) != after_parent_digest:
            blockers.append("child_feedback_cycle_parent_world_after_cycle_digest_invalid")
        cycle_state = _read_json(cycle_state_path)
        seed_packet = _read_json(seed_path)
        cycle_records = _records(cycle_ledger_path)
        cycle_ledger = _latest_matching(
            cycle_records,
            "cycle_id",
            str(plan.get("cycle_id", "")),
        )
        if cycle_state_digest(cycle_state) != str(
            cycle_state.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_5_state_digest_invalid")
        if str(cycle_state.get("previous_cycle_state_digest", "")) != previous_cycle_digest:
            blockers.append("child_feedback_cycle_v0_5_previous_cycle_digest_mismatch")
        if str(cycle_state.get("source_activation_record_digest", "")) != str(
            activation_record.get("activation_record_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_5_activation_digest_mismatch")
        if not valid_digest(seed_packet, "next_cycle_seed_packet_digest"):
            blockers.append("child_feedback_cycle_v0_5_seed_digest_invalid")
        if str(seed_packet.get("source_process_tensor_cycle_state_digest", "")) != str(
            cycle_state.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_5_seed_state_digest_mismatch")
        if not valid_digest(cycle_ledger, "record_digest"):
            blockers.append("child_feedback_cycle_v0_5_ledger_digest_invalid")
        if str(cycle_ledger.get("process_tensor_cycle_state_digest", "")) != str(
            cycle_state.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_5_ledger_state_mismatch")
        if str(cycle_ledger.get("next_cycle_seed_packet_digest", "")) != str(
            seed_packet.get("next_cycle_seed_packet_digest", "")
        ):
            blockers.append("child_feedback_cycle_v0_5_ledger_seed_mismatch")
        cycle_digest = str(cycle_state.get("process_tensor_cycle_state_digest", ""))
        seed_digest = str(seed_packet.get("next_cycle_seed_packet_digest", ""))

    child_state_after = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
    child_indra_after = _read_json(
        child_root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    )
    child_feedback_after = _read_json(
        child_root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    )
    child_handoff_after = _read_json(
        child_root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    )
    if child_state_before != child_state_after:
        blockers.append("child_feedback_cycle_child_v14_state_changed")
    if child_indra_before != child_indra_after:
        blockers.append("child_feedback_cycle_child_indra_state_changed")
    if child_feedback_before != child_feedback_after:
        blockers.append("child_feedback_cycle_child_feedback_packet_changed")
    if child_handoff_before != child_handoff_after:
        blockers.append("child_feedback_cycle_child_feedback_handoff_changed")

    if blockers and transaction_snapshot:
        _restore_files(transaction_snapshot)
        rolled_back = True
        rollback_reason = blockers[0]
        restored_world = _read_json(world_path)
        after_parent_digest = str(restored_world.get("indra_qi_world_state_digest", ""))
        if after_parent_digest != before_parent_digest:
            blockers.append("child_feedback_cycle_transaction_restore_world_digest_mismatch")
        restored_cycle = _read_json(cycle_state_path)
        restored_cycle_digest = (
            str(restored_cycle.get("process_tensor_cycle_state_digest", ""))
            if restored_cycle
            else "GENESIS"
        )
        if restored_cycle_digest != previous_cycle_digest:
            blockers.append("child_feedback_cycle_transaction_restore_cycle_digest_mismatch")
        cycle_digest = previous_cycle_digest if previous_cycle_digest != "GENESIS" else ""
        seed_digest = ""
        child_feedback_staged = False
        activation_ready = False
        cycle_ready = False
        overlays_applied = 0
        channel_count = 0
        seed_count = 0

    handoff_packet_path = root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json"
    bridge_record_path = root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json"
    receipt_path = root / "indra_qi_child_feedback_parent_cycle_receipt_v0_10.json"
    audit_path = root / "indra_qi_child_feedback_parent_cycle_audit_v0_10.jsonl"
    handoff_packet: dict[str, Any] = {}
    handoff_packet_digest = ""
    handoff_status = (
        "child_feedback_activated_and_parent_cycle_evolved"
        if cycle_ready and not blockers
        else "child_feedback_parent_cycle_blocked"
    )

    if handoff_status == "child_feedback_activated_and_parent_cycle_evolved":
        handoff_packet = {
            "version": "indra_qi_child_feedback_parent_cycle_handoff_packet_v0_10",
            "handoff_status": handoff_status,
            "bridge_id": bridge_id,
            "source_execution_id": source_execution_id,
            "source_execution_record_digest": str(execution.get("execution_record_digest", "")),
            "source_execution_ledger_record_digest": str(execution_ledger.get("record_digest", "")),
            "source_reentry_id": str(reentry.get("reentry_id", "")),
            "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
            "source_child_feedback_id": child_feedback_id,
            "source_child_feedback_packet_digest": child_feedback_digest,
            "source_child_feedback_handoff_digest": child_handoff_digest,
            "source_parent_world_state_digest": before_parent_digest,
            "after_parent_world_state_digest": after_parent_digest,
            "activation_plan_digest": str(activation_plan.get("activation_plan_digest", "")),
            "activation_record_digest": str(activation_record.get("activation_record_digest", "")),
            "process_tensor_review_digest": str(review.get("process_tensor_review_digest", "")),
            "cycle_plan_digest": str(cycle_plan.get("cycle_plan_digest", "")),
            "previous_cycle_state_digest": previous_cycle_digest,
            "process_tensor_cycle_state_digest": cycle_digest,
            "next_cycle_seed_packet_digest": seed_digest,
            "approved_candidate_ids": [str(value) for value in items(plan.get("approved_candidate_ids"))],
            "overlays_applied": overlays_applied,
            "cycle_index": cycle_index,
            "channel_count": channel_count,
            "seed_entry_count": seed_count,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "child_feedback_staged_into_parent_runtime": True,
                "v0_4_activation_completed": True,
                "v0_5_cycle_completed": True,
                "parent_world_mutation_traceable": True,
                "child_runtime_unchanged": True,
            },
            "epoch": int(time.time()),
        }
        handoff_packet["handoff_packet_digest"] = sha(handoff_packet)
        handoff_packet_digest = str(handoff_packet["handoff_packet_digest"])
        _write_json(handoff_packet_path, handoff_packet)

        bridge_record = {
            "version": "indra_qi_child_feedback_parent_cycle_record_v0_10",
            "handoff_status": handoff_status,
            "bridge_id": bridge_id,
            "source_execution_id": source_execution_id,
            "source_child_feedback_packet_digest": child_feedback_digest,
            "source_handoff_packet_digest": handoff_packet_digest,
            "before_parent_world_state_digest": before_parent_digest,
            "after_parent_world_state_digest": after_parent_digest,
            "activation_record_digest": str(activation_record.get("activation_record_digest", "")),
            "process_tensor_cycle_state_digest": cycle_digest,
            "next_cycle_seed_packet_digest": seed_digest,
            "transaction_rolled_back": False,
            "boundary": {
                "append_only_bridge_record": True,
                "parent_world_mutation_delegated_to_v0_4": True,
                "cycle_evolution_delegated_to_v0_5": True,
                "child_runtime_unchanged": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        bridge_record["bridge_record_digest"] = sha(bridge_record)
        _write_json(bridge_record_path, bridge_record)

        bridge_ledger = {
            "version": "indra_qi_child_feedback_parent_cycle_ledger_record_v0_10",
            "record_type": "child_feedback_parent_process_tensor_cycle",
            "bridge_id": bridge_id,
            "source_execution_id": source_execution_id,
            "source_child_feedback_packet_digest": child_feedback_digest,
            "source_handoff_packet_digest": handoff_packet_digest,
            "source_bridge_record_digest": bridge_record["bridge_record_digest"],
            "after_parent_world_state_digest": after_parent_digest,
            "process_tensor_cycle_state_digest": cycle_digest,
            "next_cycle_seed_packet_digest": seed_digest,
            "prev_record_digest": str(prior_bridge_records[-1].get("record_digest", "GENESIS"))
            if prior_bridge_records
            else "GENESIS",
            "boundary": {
                "append_only_bridge_lineage": True,
                "source_execution_consumed_once": True,
                "child_feedback_consumed_once": True,
                "v0_4_and_v0_5_completed": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        bridge_ledger["record_digest"] = sha(bridge_ledger)
        _append_jsonl(bridge_ledger_path, bridge_ledger)

    status = READY if handoff_status == "child_feedback_activated_and_parent_cycle_evolved" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-child-feedback-cycle-"
        + sha(
            {
                "bridge_id": bridge_id,
                "execution_id": source_execution_id,
                "feedback_digest": child_feedback_digest,
                "cycle_digest": cycle_digest,
                "blockers": blockers,
            }
        )[:16],
        "bridge_id": bridge_id,
        "source_execution_id": source_execution_id,
        "source_child_feedback_id": child_feedback_id,
        "handoff_status": handoff_status,
        "child_feedback_staged": child_feedback_staged,
        "v0_4_activation_invoked": activation_invoked,
        "v0_4_activation_ready": activation_ready,
        "v0_5_cycle_invoked": cycle_invoked,
        "v0_5_cycle_ready": cycle_ready,
        "transaction_rolled_back": rolled_back,
        "rollback_reason": rollback_reason,
        "approved_candidate_count": approved_count,
        "overlays_applied": overlays_applied,
        "cycle_index": cycle_index,
        "channel_count": channel_count,
        "seed_entry_count": seed_count,
        "before_parent_world_state_digest": before_parent_digest,
        "after_parent_world_state_digest": after_parent_digest,
        "previous_cycle_state_digest": previous_cycle_digest,
        "process_tensor_cycle_state_digest": cycle_digest,
        "next_cycle_seed_packet_digest": seed_digest,
        "child_feedback_packet_digest": child_feedback_digest,
        "child_feedback_handoff_digest": child_handoff_digest,
        "handoff_packet_digest": handoff_packet_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "handoff_completed": handoff_status
            == "child_feedback_activated_and_parent_cycle_evolved",
            "rollback_completed_on_failure": rolled_back,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiChildFeedbackParentCycleV0_10Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        bridge_id,
        source_execution_id,
        child_feedback_id,
        handoff_status,
        child_feedback_staged,
        activation_invoked,
        activation_ready,
        cycle_invoked,
        cycle_ready,
        rolled_back,
        rollback_reason,
        approved_count,
        overlays_applied,
        cycle_index,
        channel_count,
        seed_count,
        before_parent_digest,
        after_parent_digest,
        previous_cycle_digest,
        cycle_digest,
        seed_digest,
        child_feedback_digest,
        child_handoff_digest,
        handoff_packet_digest,
        str(handoff_packet_path),
        str(bridge_record_path),
        str(bridge_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

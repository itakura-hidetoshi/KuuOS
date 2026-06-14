#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import shutil
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_approved_action_core_v0_9 import SELECTABLE_ACTION_KINDS
from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import (
    ALLOWED_ACTION_KINDS,
    STATE_VERSION,
    mapping,
    runner_state_digest,
    valid_digest,
)
from runtime.kuuos_indra_qi_feedback_core_v0_3 import ALLOWED_FEEDBACK_KINDS
from runtime.kuuos_indra_qi_parent_cycle_reentry_core_v0_11 import (
    validate_assimilation_license_template,
    validate_reentry_license_template,
)
from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import ALLOWED_ACTION_KINDS as V0_8_KINDS
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import dynamic_world_state_digest
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

V0_12_OUTPUT_NAMES = {
    "indra_qi_bounded_cycle_state_v0_12.json",
    "indra_qi_bounded_cycle_handoff_v0_12.json",
    "indra_qi_bounded_cycle_record_v0_12.json",
    "indra_qi_bounded_cycle_ledger_v0_12.jsonl",
    "indra_qi_bounded_cycle_receipt_v0_12.json",
    "indra_qi_bounded_cycle_audit_v0_12.jsonl",
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def records(path: pathlib.Path) -> list[dict[str, Any]]:
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


def latest_matching(
    values: list[dict[str, Any]],
    field: str,
    expected: str,
) -> dict[str, Any]:
    for value in reversed(values):
        if str(value.get(field, "")) == expected:
            return value
    return {}


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in value)[:128] or "invalid"


def snapshot_root_files(root: pathlib.Path) -> dict[str, bytes]:
    return {
        path.name: path.read_bytes()
        for path in root.iterdir()
        if path.is_file() and path.name not in V0_12_OUTPUT_NAMES
    }


def restore_root_files(root: pathlib.Path, snapshot: Mapping[str, bytes]) -> None:
    for path in root.iterdir():
        if path.is_file() and path.name not in V0_12_OUTPUT_NAMES and path.name not in snapshot:
            path.unlink()
    for name, content in snapshot.items():
        path = root / name
        temporary = path.with_suffix(path.suffix + ".restore.tmp")
        temporary.write_bytes(content)
        os.replace(temporary, path)


def snapshot_tree(root: pathlib.Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def restore_tree(root: pathlib.Path, snapshot: Mapping[str, bytes]) -> None:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    for relative, content in snapshot.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def validate_source_v0_11(
    root: pathlib.Path,
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    handoff = read_json(root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json")
    record = read_json(root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json")
    ledger_values = records(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl")
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")

    if not handoff:
        blockers.append("bounded_cycle_source_v0_11_handoff_missing")
    else:
        if handoff.get("version") != "indra_qi_parent_cycle_assimilation_reentry_handoff_packet_v0_11":
            blockers.append("bounded_cycle_source_v0_11_handoff_version_invalid")
        if handoff.get("loop_status") != "parent_cycle_assimilated_and_causal_reentry_initialized":
            blockers.append("bounded_cycle_source_v0_11_handoff_not_ready")
        if not valid_digest(handoff, "loop_handoff_packet_digest"):
            blockers.append("bounded_cycle_source_v0_11_handoff_digest_invalid")
        boundary = mapping(handoff.get("boundary"))
        for field in (
            "source_v0_10_handoff_required",
            "source_cycle_and_seed_digest_exact",
            "parent_world_mutation_only_via_v0_6",
            "child_runtime_creation_only_via_v0_7",
            "v0_6_and_v0_7_transaction_compensated",
            "runtime_local_external_state_only",
            "non_markov_feedback_preserved",
            "uses_process_tensor_feedback",
            "candidate_weighting_not_truth",
            "not_external_world_actuation_authority",
            "not_direct_execution_authority",
            "v0_6_assimilation_completed",
            "v0_7_reentry_completed",
            "transaction_committed",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"bounded_cycle_source_v0_11_boundary_{field}_not_true")

    if not record:
        blockers.append("bounded_cycle_source_v0_11_record_missing")
    else:
        if record.get("version") != "indra_qi_parent_cycle_assimilation_reentry_record_v0_11":
            blockers.append("bounded_cycle_source_v0_11_record_version_invalid")
        if not valid_digest(record, "loop_record_digest"):
            blockers.append("bounded_cycle_source_v0_11_record_digest_invalid")
        if str(record.get("source_loop_handoff_packet_digest", "")) != str(
            handoff.get("loop_handoff_packet_digest", "")
        ):
            blockers.append("bounded_cycle_source_v0_11_record_handoff_mismatch")

    loop_id = str(handoff.get("loop_id", ""))
    ledger = latest_matching(ledger_values, "loop_id", loop_id)
    if not ledger:
        blockers.append("bounded_cycle_source_v0_11_ledger_missing")
    else:
        if not valid_digest(ledger, "record_digest"):
            blockers.append("bounded_cycle_source_v0_11_ledger_digest_invalid")
        if str(ledger.get("source_loop_handoff_packet_digest", "")) != str(
            handoff.get("loop_handoff_packet_digest", "")
        ):
            blockers.append("bounded_cycle_source_v0_11_ledger_handoff_mismatch")
        if str(ledger.get("source_loop_record_digest", "")) != str(
            record.get("loop_record_digest", "")
        ):
            blockers.append("bounded_cycle_source_v0_11_ledger_record_mismatch")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    dynamic_digest = str(world.get("process_tensor_dynamic_world_state_digest", ""))
    if not world:
        blockers.append("bounded_cycle_source_parent_world_missing")
    else:
        if compute_indra_qi_world_state_digest(world) != world_digest:
            blockers.append("bounded_cycle_source_parent_world_digest_invalid")
        if dynamic_world_state_digest(world) != dynamic_digest:
            blockers.append("bounded_cycle_source_parent_dynamic_digest_invalid")
        if world_digest != str(handoff.get("after_assimilation_world_state_digest", "")):
            blockers.append("bounded_cycle_source_parent_world_handoff_mismatch")
        if dynamic_digest != str(handoff.get("dynamic_world_state_digest", "")):
            blockers.append("bounded_cycle_source_parent_dynamic_handoff_mismatch")

    if not reentry:
        blockers.append("bounded_cycle_source_reentry_missing")
    else:
        if reentry.get("version") != "indra_qi_post_assimilation_causal_reentry_record_v0_7":
            blockers.append("bounded_cycle_source_reentry_version_invalid")
        if reentry.get("reentry_status") != "post_assimilation_causal_world_initialized":
            blockers.append("bounded_cycle_source_reentry_not_ready")
        if not valid_digest(reentry, "reentry_record_digest"):
            blockers.append("bounded_cycle_source_reentry_digest_invalid")
        if str(reentry.get("reentry_id", "")) != str(handoff.get("reentry_id", "")):
            blockers.append("bounded_cycle_source_reentry_id_mismatch")
        if str(reentry.get("reentry_record_digest", "")) != str(
            handoff.get("reentry_record_digest", "")
        ):
            blockers.append("bounded_cycle_source_reentry_handoff_digest_mismatch")
        if str(reentry.get("source_world_state_digest", "")) != world_digest:
            blockers.append("bounded_cycle_source_reentry_world_mismatch")

    expected = {
        "source_v0_11_loop_id": loop_id,
        "source_v0_11_handoff_packet_digest": str(
            handoff.get("loop_handoff_packet_digest", "")
        ),
        "source_v0_11_record_digest": str(record.get("loop_record_digest", "")),
        "source_v0_11_ledger_record_digest": str(ledger.get("record_digest", "")),
    }
    for field, value in expected.items():
        if str(plan.get(field, "")) != value:
            blockers.append(f"bounded_cycle_plan_{field}_mismatch")

    child_raw = str(reentry.get("child_runtime_root", ""))
    child = pathlib.Path(child_raw).expanduser().resolve() if child_raw else root
    allowed_parent = (root / "indra_qi_causal_reentry_cycles_v0_7").resolve()
    try:
        child.relative_to(allowed_parent)
    except ValueError:
        blockers.append("bounded_cycle_source_child_outside_allowed_root")
    if not child.is_dir():
        blockers.append("bounded_cycle_source_child_missing")
    child_world = read_json(child / "ku_indra_qi_noncommutative_mandala_world_state.json")
    causal = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
    if not child_world or compute_indra_qi_world_state_digest(child_world) != world_digest:
        blockers.append("bounded_cycle_source_child_world_digest_invalid")
    if not valid_v14_digest(causal, "world_model_digest"):
        blockers.append("bounded_cycle_source_child_v14_digest_invalid")
    if str(causal.get("world_model_digest", "")) != str(reentry.get("v14_world_model_digest", "")):
        blockers.append("bounded_cycle_source_child_v14_reentry_mismatch")

    return {
        "handoff": handoff,
        "record": record,
        "ledger": ledger,
        "world": world,
        "reentry": reentry,
        "child": child,
        "causal": causal,
    }


def validate_runner_state(
    root: pathlib.Path,
    plan: Mapping[str, Any],
    source_handoff_digest: str,
    blockers: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    state_path = root / "indra_qi_bounded_cycle_state_v0_12.json"
    ledger_path = root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl"
    state = read_json(state_path)
    ledger = records(ledger_path)
    generation = int(plan.get("generation_index", -1) or 0)
    expected_previous = str(plan.get("expected_previous_runner_state_digest", ""))
    if not state:
        if generation != 0:
            blockers.append("bounded_cycle_first_generation_index_not_zero")
        if expected_previous != "GENESIS":
            blockers.append("bounded_cycle_first_previous_state_not_genesis")
    else:
        if state.get("version") != STATE_VERSION:
            blockers.append("bounded_cycle_runner_state_version_invalid")
        if not valid_digest(state, "runner_state_digest"):
            blockers.append("bounded_cycle_runner_state_digest_invalid")
        if str(state.get("runner_id", "")) != str(plan.get("runner_id", "")):
            blockers.append("bounded_cycle_runner_id_mismatch")
        if int(state.get("completed_generations", -1) or 0) != generation:
            blockers.append("bounded_cycle_generation_index_not_monotone")
        if int(state.get("max_generations", 0) or 0) != int(plan.get("max_generations", 0) or 0):
            blockers.append("bounded_cycle_max_generations_changed")
        if expected_previous != str(state.get("runner_state_digest", "")):
            blockers.append("bounded_cycle_previous_state_digest_mismatch")
        if state.get("runner_status") == "bounded_cycle_stopped":
            blockers.append("bounded_cycle_runner_already_stopped")
        if str(state.get("latest_v0_11_handoff_packet_digest", "")) != source_handoff_digest:
            blockers.append("bounded_cycle_runner_source_handoff_not_latest")
    run_id = str(plan.get("generation_run_id", ""))
    if any(str(value.get("generation_run_id", "")) == run_id for value in ledger):
        blockers.append("bounded_cycle_generation_run_id_replay")
    if any(
        str(value.get("source_v0_11_handoff_packet_digest", "")) == source_handoff_digest
        for value in ledger
    ):
        blockers.append("bounded_cycle_source_v0_11_handoff_replay")
    return state, ledger


def _require_flags(
    value: Mapping[str, Any],
    flags: tuple[str, ...],
    prefix: str,
    blockers: list[str],
) -> None:
    for flag in flags:
        if value.get(flag) is not True:
            blockers.append(f"bounded_cycle_{prefix}_{flag}_not_true")


def validate_license_templates(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    causal: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_value.get("license_status") != "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_LICENSE_READY":
        blockers.append("bounded_cycle_license_not_ready")
    _require_flags(
        license_value,
        (
            "source_v0_11_read_allowed",
            "runner_state_read_allowed",
            "transaction_snapshot_allowed",
            "transaction_restore_allowed",
            "v0_8_invoke_allowed",
            "v0_9_invoke_allowed",
            "v0_10_invoke_allowed",
            "v0_11_invoke_allowed",
            "state_write_allowed",
            "handoff_write_allowed",
            "record_write_allowed",
            "ledger_append_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "license",
        blockers,
    )
    if str(license_value.get("bound_cycle_plan_digest", "")) != str(
        plan.get("cycle_plan_digest", "")
    ):
        blockers.append("bounded_cycle_license_plan_digest_mismatch")

    v08 = mapping(license_value.get("v0_8_license_template"))
    if v08.get("license_status") != "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_LICENSE_READY":
        blockers.append("bounded_cycle_v0_8_license_not_ready")
    _require_flags(
        v08,
        (
            "world_state_read_allowed",
            "assimilation_record_read_allowed",
            "post_assimilation_seed_read_allowed",
            "assimilation_ledger_read_allowed",
            "reentry_record_read_allowed",
            "reentry_ledger_read_allowed",
            "child_runtime_read_allowed",
            "action_plan_validate_allowed",
            "action_envelope_write_allowed",
            "activation_record_write_allowed",
            "action_ledger_append_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v0_8_license",
        blockers,
    )
    raw = v08.get("allowed_action_kinds", [])
    allowed = {str(value) for value in raw} if isinstance(raw, list) else set()
    if allowed != set(V0_8_KINDS):
        blockers.append("bounded_cycle_v0_8_action_kind_set_not_exact")

    v09 = mapping(license_value.get("v0_9_license_template"))
    if v09.get("license_status") != "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_LICENSE_READY":
        blockers.append("bounded_cycle_v0_9_license_not_ready")
    _require_flags(
        v09,
        (
            "world_state_read_allowed",
            "assimilation_lineage_read_allowed",
            "reentry_lineage_read_allowed",
            "action_envelope_lineage_read_allowed",
            "child_runtime_read_allowed",
            "execution_plan_validate_allowed",
            "v14_action_invoke_allowed",
            "v0_3_feedback_invoke_allowed",
            "execution_record_write_allowed",
            "execution_ledger_append_allowed",
            "undo_readiness_write_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v0_9_license",
        blockers,
    )
    raw = v09.get("allowed_action_kinds", [])
    allowed = {str(value) for value in raw} if isinstance(raw, list) else set()
    if allowed != set(SELECTABLE_ACTION_KINDS):
        blockers.append("bounded_cycle_v0_9_action_kind_set_not_exact")
    variables = {str(value) for value in mapping(causal.get("variables"))}
    command_kind = {
        "observation_request": "observe",
        "counterfactual_candidate": "counterfactual",
        "bounded_intervention_candidate": "intervene",
    }.get(str(plan.get("selected_action_kind", "")), "")
    action_template = mapping(v09.get("v14_action_license_template"))
    if action_template.get("license_status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY":
        blockers.append("bounded_cycle_v0_9_v14_action_license_not_ready")
    action_kinds = action_template.get("allowed_command_kinds", [])
    if {str(value) for value in action_kinds} != {command_kind}:
        blockers.append("bounded_cycle_v0_9_v14_action_command_not_exact")
    action_vars = action_template.get("allowed_variables", [])
    if {str(value) for value in action_vars} != variables:
        blockers.append("bounded_cycle_v0_9_v14_action_variables_not_exact")
    _require_flags(
        action_template,
        ("state_read_allowed", "event_ledger_append_allowed", "result_write_allowed", "audit_append_allowed"),
        "v0_9_v14_action",
        blockers,
    )
    undo_template = mapping(v09.get("v14_undo_license_template"))
    if undo_template.get("license_status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY":
        blockers.append("bounded_cycle_v0_9_v14_undo_license_not_ready")
    feedback = mapping(v09.get("v0_3_feedback_license_template"))
    if feedback.get("license_status") != "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_LICENSE_READY":
        blockers.append("bounded_cycle_v0_9_feedback_license_not_ready")
    _require_flags(
        feedback,
        (
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
        ),
        "v0_9_feedback",
        blockers,
    )
    raw = feedback.get("allowed_feedback_kinds", [])
    if {str(value) for value in raw} != set(ALLOWED_FEEDBACK_KINDS):
        blockers.append("bounded_cycle_v0_9_feedback_kind_set_not_exact")

    v10 = mapping(license_value.get("v0_10_license_template"))
    if v10.get("license_status") != "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_LICENSE_READY":
        blockers.append("bounded_cycle_v0_10_license_not_ready")
    _require_flags(
        v10,
        (
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
        ),
        "v0_10_license",
        blockers,
    )
    v04 = mapping(v10.get("v0_4_activation_license_template"))
    if v04.get("license_status") != "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_LICENSE_READY":
        blockers.append("bounded_cycle_v0_10_v0_4_license_not_ready")
    v05 = mapping(v10.get("v0_5_cycle_license_template"))
    if v05.get("license_status") != "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_LICENSE_READY":
        blockers.append("bounded_cycle_v0_10_v0_5_license_not_ready")

    v11 = mapping(license_value.get("v0_11_license_template"))
    if v11.get("license_status") != "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_LICENSE_READY":
        blockers.append("bounded_cycle_v0_11_license_not_ready")
    _require_flags(
        v11,
        (
            "source_v0_10_read_allowed",
            "parent_world_read_allowed",
            "cycle_state_read_allowed",
            "transaction_snapshot_allowed",
            "transaction_restore_allowed",
            "child_runtime_remove_on_failure_allowed",
            "v0_6_assimilation_invoke_allowed",
            "v0_7_reentry_invoke_allowed",
            "loop_handoff_write_allowed",
            "loop_record_write_allowed",
            "loop_ledger_append_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v0_11_license",
        blockers,
    )
    validate_assimilation_license_template(
        mapping(v11.get("v0_6_assimilation_license_template")), blockers
    )
    validate_reentry_license_template(
        mapping(v11.get("v0_7_reentry_license_template")),
        int(mapping(plan.get("projection_policy")).get("max_projection_variables", 0) or 0),
        blockers,
    )

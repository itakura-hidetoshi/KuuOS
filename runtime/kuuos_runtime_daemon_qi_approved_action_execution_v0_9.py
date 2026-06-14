#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_causal_world_model_os_v14_0 import (
    build_kuuos_causal_world_model_os_v14_0,
)
from runtime.kuuos_indra_qi_approved_action_core_v0_9 import (
    ACTION_TO_COMMAND,
    REQUIRED_BOUNDARY,
    SELECTABLE_ACTION_KINDS,
    build_feedback_plan,
    build_undo_command,
    build_v14_action_command,
    find_selected_candidate,
    items,
    mapping,
    sha,
    valid_digest,
    validate_approval,
    validate_evidence,
    validate_execution_plan,
    validate_selected_value,
)
from runtime.kuuos_indra_qi_feedback_core_v0_3 import ALLOWED_FEEDBACK_KINDS
from runtime.kuuos_runtime_daemon_indra_qi_causal_feedback_bridge_v0_3 import (
    build_indra_qi_causal_feedback_bridge_v0_3,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from runtime.kuuos_runtime_daemon_qi_recoverability_action_envelope_v0_8 import (
    _validate_v0_6_lineage,
    _validate_v0_7_lineage,
)

VERSION = "indra_qi_approved_recovery_action_execution_v0_9"
READY = "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_READY"
BLOCKED = "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_BLOCKED"
LICENSE_READY = "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiApprovedRecoveryActionExecutionV0_9Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_id: str
    source_action_envelope_id: str
    selected_candidate_id: str
    selected_action_kind: str
    action_command_kind: str
    action_transaction_id: str
    execution_status: str
    action_invoked: bool
    action_ready: bool
    state_mutated: bool
    counterfactual_generated: bool
    snapshot_verified: bool
    undo_readiness_ready: bool
    feedback_invoked: bool
    feedback_ready: bool
    feedback_candidate_count: int
    feedback_local_patch_candidate_count: int
    feedback_qi_flow_candidate_count: int
    parent_world_state_unchanged: bool
    child_indra_state_unchanged: bool
    before_v14_world_model_digest: str
    after_v14_world_model_digest: str
    action_event_record_digest: str
    action_result_digest: str
    feedback_packet_digest: str
    execution_record_path: str
    execution_ledger_path: str
    undo_readiness_path: str
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


def _latest_matching(
    records: list[dict[str, Any]], field: str, expected: str
) -> Mapping[str, Any]:
    for record in reversed(records):
        if str(record.get(field, "")) == expected:
            return record
    return {}


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in value)[:128] or "invalid"


def _validate_v0_8_lineage(
    *,
    world_state: Mapping[str, Any],
    reentry: Mapping[str, Any],
    envelope: Mapping[str, Any],
    activation: Mapping[str, Any],
    envelope_records: list[dict[str, Any]],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, dict[str, Any], str]:
    if not envelope:
        blockers.append("approved_action_source_envelope_missing_or_invalid")
        return "", {}, ""
    if envelope.get("version") != "indra_qi_recoverability_action_envelope_v0_8":
        blockers.append("approved_action_source_envelope_version_invalid")
    if envelope.get("envelope_status") != "recoverability_gated_action_candidates_ready":
        blockers.append("approved_action_source_envelope_not_ready")
    if not valid_digest(envelope, "action_envelope_digest"):
        blockers.append("approved_action_source_envelope_digest_invalid")
    envelope_id = str(envelope.get("action_envelope_id", ""))
    expected = {
        "source_action_envelope_id": envelope_id,
        "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
        "source_reentry_id": str(reentry.get("reentry_id", "")),
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_world_state_digest": str(world_state.get("indra_qi_world_state_digest", "")),
        "source_dynamic_world_state_digest": str(
            world_state.get("process_tensor_dynamic_world_state_digest", "")
        ),
        "source_v14_world_model_digest": str(reentry.get("v14_world_model_digest", "")),
    }
    for field, expected_value in expected.items():
        if str(plan.get(field, "")) != expected_value:
            blockers.append(f"approved_action_plan_{field}_mismatch")
    for field in (
        "source_reentry_id",
        "source_reentry_record_digest",
        "source_world_state_digest",
        "source_dynamic_world_state_digest",
        "source_v14_world_model_digest",
    ):
        if str(envelope.get(field, "")) != expected[field]:
            blockers.append(f"approved_action_source_envelope_{field}_mismatch")
    boundary = mapping(envelope.get("boundary"))
    for field in (
        "action_envelope_not_execution",
        "action_candidate_not_truth",
        "debt_gates_action_surface",
        "recoverability_gates_action_surface",
        "critical_corridor_observe_only",
        "qi_flow_observation_only",
        "counterfactual_before_intervention_when_constrained",
        "bounded_intervention_requires_open_corridor",
        "undo_reserve_required_for_intervention_candidate",
        "parent_world_state_not_mutated",
        "child_causal_world_not_mutated",
        "base_gauge_connection_not_mutated",
        "operator_algebra_unchanged",
        "causal_edge_not_gauge_connection",
        "qi_not_substance",
        "non_markov_feedback_preserved",
        "uses_process_tensor_feedback",
        "candidate_weighting_not_truth",
        "not_direct_execution_authority",
        "not_external_world_actuation_authority",
        "not_world_update_authority",
        "fresh_action_license_required",
        "envelope_contains_candidates_only",
        "no_v14_command_invoked",
        "future_approval_required",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"approved_action_source_envelope_boundary_{field}_not_true")

    if not activation:
        blockers.append("approved_action_source_activation_missing_or_invalid")
    else:
        if activation.get("version") != "indra_qi_recoverability_action_envelope_record_v0_8":
            blockers.append("approved_action_source_activation_version_invalid")
        if activation.get("envelope_status") != "recoverability_gated_action_candidates_ready":
            blockers.append("approved_action_source_activation_not_ready")
        if not valid_digest(activation, "activation_record_digest"):
            blockers.append("approved_action_source_activation_digest_invalid")
        if str(activation.get("source_action_envelope_digest", "")) != str(
            envelope.get("action_envelope_digest", "")
        ):
            blockers.append("approved_action_source_activation_envelope_mismatch")
        if str(plan.get("source_action_activation_record_digest", "")) != str(
            activation.get("activation_record_digest", "")
        ):
            blockers.append("approved_action_plan_source_activation_record_digest_mismatch")
        if activation.get("action_executed") is not False:
            blockers.append("approved_action_source_activation_action_executed_not_false")
        if activation.get("v14_command_invoked") is not False:
            blockers.append("approved_action_source_activation_v14_invoked_not_false")

    ledger = _latest_matching(envelope_records, "action_envelope_id", envelope_id)
    if not ledger:
        blockers.append("approved_action_source_envelope_ledger_missing")
    else:
        if not valid_digest(ledger, "record_digest"):
            blockers.append("approved_action_source_envelope_ledger_digest_invalid")
        if str(ledger.get("source_action_envelope_digest", "")) != str(
            envelope.get("action_envelope_digest", "")
        ):
            blockers.append("approved_action_source_envelope_ledger_packet_mismatch")
        if str(ledger.get("source_activation_record_digest", "")) != str(
            activation.get("activation_record_digest", "")
        ):
            blockers.append("approved_action_source_envelope_ledger_activation_mismatch")

    candidate, collection_kind = find_selected_candidate(
        envelope,
        str(plan.get("selected_candidate_id", "")),
        blockers,
    )
    if collection_kind != str(plan.get("selected_action_kind", "")):
        blockers.append("approved_action_selected_collection_kind_mismatch")
    return envelope_id, candidate, collection_kind


def _validate_action_license_template(
    *, template: Mapping[str, Any], command_kind: str, variables: set[str], blockers: list[str]
) -> None:
    if template.get("license_status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY":
        blockers.append("approved_action_nested_v14_license_not_ready")
    allowed_kinds_raw = template.get("allowed_command_kinds", [])
    allowed_kinds = {str(value) for value in allowed_kinds_raw} if isinstance(allowed_kinds_raw, list) else set()
    if allowed_kinds != {command_kind}:
        blockers.append("approved_action_nested_v14_command_kind_set_not_exact")
    allowed_variables_raw = template.get("allowed_variables", [])
    allowed_variables = (
        {str(value) for value in allowed_variables_raw}
        if isinstance(allowed_variables_raw, list)
        else set()
    )
    if allowed_variables != variables:
        blockers.append("approved_action_nested_v14_allowed_variables_not_exact")
    protected_raw = template.get("protected_variables", [])
    protected = {str(value) for value in protected_raw} if isinstance(protected_raw, list) else set()
    if not protected.issubset(variables):
        blockers.append("approved_action_nested_v14_protected_variables_invalid")
    common = (
        "state_read_allowed",
        "event_ledger_append_allowed",
        "result_write_allowed",
        "audit_append_allowed",
    )
    kind_flags = {
        "observe": (
            "observation_update_allowed",
            "state_write_allowed",
            "snapshot_write_allowed",
            "direct_world_model_mutation_allowed",
        ),
        "intervene": (
            "intervention_allowed",
            "state_write_allowed",
            "snapshot_write_allowed",
            "direct_world_model_mutation_allowed",
        ),
        "counterfactual": ("counterfactual_allowed",),
        "undo": (
            "undo_allowed",
            "state_write_allowed",
            "snapshot_read_allowed",
            "snapshot_write_allowed",
            "direct_world_model_mutation_allowed",
        ),
    }
    for flag in common + kind_flags.get(command_kind, ()):
        if template.get(flag) is not True:
            blockers.append(f"approved_action_nested_v14_{flag}_not_true")


def _validate_feedback_license_template(template: Mapping[str, Any], blockers: list[str]) -> None:
    if template.get("license_status") != "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_LICENSE_READY":
        blockers.append("approved_action_nested_feedback_license_not_ready")
    for flag in (
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
    ):
        if template.get(flag) is not True:
            blockers.append(f"approved_action_nested_feedback_{flag}_not_true")
    allowed_raw = template.get("allowed_feedback_kinds", [])
    allowed = {str(value) for value in allowed_raw} if isinstance(allowed_raw, list) else set()
    if allowed != ALLOWED_FEEDBACK_KINDS:
        blockers.append("approved_action_nested_feedback_kind_set_not_exact")


def build_indra_qi_approved_recovery_action_execution_v0_9(
    *,
    runtime_context: Mapping[str, Any],
    execution_plan: Mapping[str, Any],
    execution_license: Mapping[str, Any],
) -> IndraQiApprovedRecoveryActionExecutionV0_9Result:
    context = mapping(runtime_context)
    plan = dict(mapping(execution_plan))
    license_value = mapping(execution_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    world_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    assimilation_path = root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json"
    seed_path = root / "indra_qi_post_assimilation_projection_seed_v0_6.json"
    assimilation_ledger_path = root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
    reentry_path = root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json"
    reentry_ledger_path = root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl"
    envelope_path = root / "indra_qi_recoverability_action_envelope_v0_8.json"
    envelope_activation_path = root / "indra_qi_recoverability_action_envelope_record_v0_8.json"
    envelope_ledger_path = root / "indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl"
    execution_record_path = root / "indra_qi_approved_recovery_action_execution_record_v0_9.json"
    execution_ledger_path = root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
    receipt_path = root / "indra_qi_approved_recovery_action_execution_receipt_v0_9.json"
    audit_path = root / "indra_qi_approved_recovery_action_execution_audit_v0_9.jsonl"

    if context.get("indra_qi_approved_recovery_action_execution_v0_9_enabled") is not True:
        blockers.append("indra_qi_approved_recovery_action_execution_v0_9_enabled_not_true")
    if context.get("execute_indra_qi_approved_recovery_action_v0_9") is not True:
        blockers.append("execute_indra_qi_approved_recovery_action_v0_9_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("approved_action_execution_license_not_ready")
    for flag in (
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
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_execution_plan(plan, blockers)
    plan_digest = str(plan.get("execution_plan_digest", ""))
    if str(license_value.get("bound_execution_plan_digest", "")) != plan_digest:
        blockers.append("approved_action_execution_license_plan_digest_mismatch")
    allowed_actions_raw = license_value.get("allowed_action_kinds", [])
    allowed_actions = (
        {str(value) for value in allowed_actions_raw}
        if isinstance(allowed_actions_raw, list)
        else set()
    )
    if allowed_actions != SELECTABLE_ACTION_KINDS:
        blockers.append("approved_action_execution_allowed_action_kinds_not_exact")

    world_state = _read_json(world_path)
    assimilation = _read_json(assimilation_path)
    seed_packet = _read_json(seed_path)
    assimilation_records = _records(assimilation_ledger_path)
    _, world_digest, dynamic_digest = _validate_v0_6_lineage(
        world_state=world_state,
        assimilation=assimilation,
        seed_packet=seed_packet,
        assimilation_records=assimilation_records,
        blockers=blockers,
    )
    reentry = _read_json(reentry_path)
    reentry_records = _records(reentry_ledger_path)
    reentry_id, child_root, generated_plan, projection_packet, causal_state = _validate_v0_7_lineage(
        root=root,
        world_state=world_state,
        reentry=reentry,
        reentry_records=reentry_records,
        plan=plan,
        blockers=blockers,
    )
    envelope = _read_json(envelope_path)
    envelope_activation = _read_json(envelope_activation_path)
    envelope_records = _records(envelope_ledger_path)
    envelope_id, selected_candidate, selected_collection_kind = _validate_v0_8_lineage(
        world_state=world_state,
        reentry=reentry,
        envelope=envelope,
        activation=envelope_activation,
        envelope_records=envelope_records,
        plan=plan,
        blockers=blockers,
    )

    selected_kind = str(plan.get("selected_action_kind", ""))
    if selected_collection_kind and selected_collection_kind != selected_kind:
        blockers.append("approved_action_selected_kind_collection_mismatch")
    if selected_kind not in allowed_actions:
        blockers.append("approved_action_selected_kind_not_licensed")
    undo_reserve = validate_selected_value(
        plan=plan,
        candidate=selected_candidate,
        envelope=envelope,
        blockers=blockers,
    )
    variable_name = str(selected_candidate.get("source_causal_variable", ""))
    current_variable = mapping(mapping(causal_state.get("variables")).get(variable_name))
    if not current_variable:
        blockers.append("approved_action_selected_variable_missing_from_v14_state")
    evidence = mapping(plan.get("fresh_observation_evidence"))
    approval = mapping(plan.get("approval"))
    validate_evidence(
        evidence=evidence,
        plan=plan,
        candidate=selected_candidate,
        current_variable=current_variable,
        blockers=blockers,
    )
    validate_approval(approval=approval, plan=plan, evidence=evidence, blockers=blockers)

    prior_executions = _records(execution_ledger_path)
    execution_id = str(plan.get("execution_id", ""))
    selected_digest = str(plan.get("selected_candidate_digest", ""))
    if any(str(record.get("execution_id", "")) == execution_id for record in prior_executions):
        blockers.append("approved_action_execution_id_replay")
    if any(
        str(record.get("source_action_envelope_id", "")) == envelope_id
        for record in prior_executions
    ):
        blockers.append("approved_action_source_envelope_replay")
    if any(
        str(record.get("selected_candidate_digest", "")) == selected_digest
        for record in prior_executions
    ):
        blockers.append("approved_action_selected_candidate_replay")

    causal_variables = set(str(name) for name in mapping(causal_state.get("variables")))
    command_kind = ACTION_TO_COMMAND.get(selected_kind, "")
    action_template = mapping(license_value.get("v14_action_license_template"))
    _validate_action_license_template(
        template=action_template,
        command_kind=command_kind,
        variables=causal_variables,
        blockers=blockers,
    )
    undo_template = mapping(license_value.get("v14_undo_license_template"))
    if selected_kind == "bounded_intervention_candidate":
        _validate_action_license_template(
            template=undo_template,
            command_kind="undo",
            variables=causal_variables,
            blockers=blockers,
        )
    feedback_template = mapping(license_value.get("v0_3_feedback_license_template"))
    _validate_feedback_license_template(feedback_template, blockers)

    process_context = mapping(projection_packet.get("aggregated_process_tensor_context"))
    if set(process_context) != {
        "process_tensor_digest",
        "memory_kernel_digest",
        "history_window_digest",
        "instrument_trace_digest",
        "non_markov_context_digest",
    } or any(not str(value) for value in process_context.values()):
        blockers.append("approved_action_process_tensor_context_invalid")

    command = build_v14_action_command(
        plan=plan,
        candidate=selected_candidate,
        causal_world_id=str(reentry.get("causal_world_id", "")),
        process_tensor_context=process_context,
    ) if selected_candidate and command_kind else {}
    action_license = dict(action_template)
    if command:
        action_license["bound_command_digest"] = str(command.get("command_digest", ""))

    action_invoked = False
    action_ready = False
    state_mutated = False
    counterfactual_generated = False
    snapshot_verified = False
    undo_readiness_ready = False
    feedback_invoked = False
    feedback_ready = False
    feedback_count = 0
    feedback_local_count = 0
    feedback_flow_count = 0
    action_event_digest = ""
    action_result_digest = ""
    feedback_packet_digest = ""
    before_v14_digest = str(causal_state.get("world_model_digest", ""))
    after_v14_digest = before_v14_digest
    action_event: dict[str, Any] = {}
    action_result_file: dict[str, Any] = {}
    undo_readiness_path = child_root / (
        "indra_qi_v0_9_undo_readiness_" + _safe_id(execution_id) + ".json"
    )

    child_event_path = child_root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"
    child_state_path = child_root / "kuuos_causal_world_model_state_v14_0.json"
    child_indra_path = child_root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    event_count_before = len(_records(child_event_path))
    child_indra_before = _read_json(child_indra_path)

    if not blockers:
        action_invoked = True
        action_result = build_kuuos_causal_world_model_os_v14_0(
            runtime_context={
                "runtime_root": str(child_root),
                "kuuos_causal_world_model_os_v14_0_enabled": True,
                "apply_kuuos_causal_world_model_os_v14_0": True,
            },
            command=command,
            license_packet=action_license,
        ).to_dict()
        if action_result.get("status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY":
            blockers.append("approved_action_v14_action_not_ready")
        else:
            action_ready = True
            state_mutated = bool(action_result.get("state_mutated"))
            counterfactual_generated = bool(action_result.get("counterfactual_generated"))
            after_v14_digest = str(action_result.get("after_world_model_digest", ""))

        events_after_action = _records(child_event_path)
        if len(events_after_action) != event_count_before + 1:
            blockers.append("approved_action_v14_event_count_mismatch")
        else:
            action_event = events_after_action[-1]
            if not valid_digest(action_event, "record_digest"):
                blockers.append("approved_action_v14_event_digest_invalid")
            if str(action_event.get("transaction_id", "")) != str(
                plan.get("action_transaction_id", "")
            ):
                blockers.append("approved_action_v14_event_transaction_mismatch")
            if str(action_event.get("command_kind", "")) != command_kind:
                blockers.append("approved_action_v14_event_kind_mismatch")
            if str(action_event.get("command_digest", "")) != str(
                command.get("command_digest", "")
            ):
                blockers.append("approved_action_v14_event_command_digest_mismatch")
            action_event_digest = str(action_event.get("record_digest", ""))

        result_path = child_root / "kuuos_causal_world_model_results_v14_0" / (
            _safe_id(str(plan.get("action_transaction_id", ""))) + ".json"
        )
        action_result_file = _read_json(result_path)
        if not valid_digest(action_result_file, "result_digest"):
            blockers.append("approved_action_v14_result_digest_invalid")
        if str(action_result_file.get("event_record_digest", "")) != action_event_digest:
            blockers.append("approved_action_v14_result_event_digest_mismatch")
        action_result_digest = str(action_result_file.get("result_digest", ""))

        current_state = _read_json(child_state_path)
        if selected_kind == "counterfactual_candidate":
            if state_mutated is not False or counterfactual_generated is not True:
                blockers.append("approved_action_counterfactual_state_behavior_invalid")
            if str(current_state.get("world_model_digest", "")) != before_v14_digest:
                blockers.append("approved_action_counterfactual_persistent_state_changed")
            if after_v14_digest != before_v14_digest:
                blockers.append("approved_action_counterfactual_after_digest_changed")
        else:
            if state_mutated is not True or counterfactual_generated is not False:
                blockers.append("approved_action_mutating_state_behavior_invalid")
            if not valid_v14_digest(current_state, "world_model_digest"):
                blockers.append("approved_action_after_v14_state_digest_invalid")
            if str(current_state.get("world_model_digest", "")) != after_v14_digest:
                blockers.append("approved_action_after_v14_state_result_mismatch")
            if after_v14_digest == before_v14_digest:
                blockers.append("approved_action_mutating_digest_not_changed")
            snapshot_path = child_root / "kuuos_causal_world_model_snapshots_v14_0" / (
                _safe_id(str(plan.get("action_transaction_id", ""))) + ".json"
            )
            snapshot = _read_json(snapshot_path)
            if not valid_v14_digest(snapshot, "world_model_digest"):
                blockers.append("approved_action_snapshot_digest_invalid")
            elif str(snapshot.get("world_model_digest", "")) != before_v14_digest:
                blockers.append("approved_action_snapshot_before_digest_mismatch")
            else:
                snapshot_verified = True

        if selected_kind == "bounded_intervention_candidate" and not blockers:
            undo_command = build_undo_command(
                plan=plan,
                causal_world_id=str(reentry.get("causal_world_id", "")),
                process_tensor_context=process_context,
            )
            undo_license = dict(undo_template)
            undo_license["bound_command_digest"] = str(undo_command.get("command_digest", ""))
            readiness = {
                "version": "indra_qi_v14_undo_readiness_packet_v0_9",
                "readiness_status": "undo_ready",
                "execution_id": execution_id,
                "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
                "selected_candidate_id": str(selected_candidate.get("candidate_id", "")),
                "selected_candidate_digest": str(
                    selected_candidate.get("action_candidate_digest", "")
                ),
                "source_undo_reserve_digest": str(
                    undo_reserve.get("action_candidate_digest", "")
                ),
                "target_action_transaction_id": str(plan.get("action_transaction_id", "")),
                "snapshot_world_model_digest": before_v14_digest,
                "undo_command": undo_command,
                "undo_license_packet": undo_license,
                "undo_license_packet_digest": sha(undo_license),
                "boundary": {
                    "undo_command_not_yet_executed": True,
                    "undo_command_exact_target_bound": True,
                    "undo_license_exact_command_bound": True,
                    "snapshot_verified": snapshot_verified,
                    "external_world_actuation_authority": False,
                },
                "epoch": int(time.time()),
            }
            readiness["undo_readiness_digest"] = sha(readiness)
            _write_json(undo_readiness_path, readiness)
            undo_readiness_ready = snapshot_verified and valid_digest(
                readiness, "undo_readiness_digest"
            )
            if not undo_readiness_ready:
                blockers.append("approved_action_undo_readiness_not_ready")

    if action_ready and not blockers:
        feedback_plan = build_feedback_plan(
            plan=plan,
            projection_packet=projection_packet,
            action_event=action_event,
        )
        feedback_license = dict(feedback_template)
        feedback_invoked = True
        feedback_result = build_indra_qi_causal_feedback_bridge_v0_3(
            runtime_context={
                "runtime_root": str(child_root),
                "indra_qi_causal_feedback_bridge_v0_3_enabled": True,
                "apply_indra_qi_causal_feedback_bridge_v0_3": True,
            },
            feedback_plan=feedback_plan,
            feedback_license=feedback_license,
        ).to_dict()
        if feedback_result.get("status") != "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_READY":
            blockers.append("approved_action_v0_3_feedback_not_ready")
        else:
            feedback_ready = True
            feedback_count = int(feedback_result.get("candidate_count", 0) or 0)
            feedback_local_count = int(
                feedback_result.get("local_patch_candidate_count", 0) or 0
            )
            feedback_flow_count = int(
                feedback_result.get("qi_flow_candidate_count", 0) or 0
            )

        feedback_packet = _read_json(
            child_root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        )
        feedback_handoff = _read_json(
            child_root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
        )
        feedback_records = _records(
            child_root / "indra_qi_causal_feedback_ledger_v0_3.jsonl"
        )
        feedback_ledger = _latest_matching(
            feedback_records,
            "feedback_id",
            str(plan.get("feedback_id", "")),
        )
        if not valid_digest(feedback_packet, "feedback_packet_digest"):
            blockers.append("approved_action_feedback_packet_digest_invalid")
        if not valid_digest(feedback_handoff, "approval_handoff_digest"):
            blockers.append("approved_action_feedback_handoff_digest_invalid")
        if not valid_digest(feedback_ledger, "record_digest"):
            blockers.append("approved_action_feedback_ledger_digest_invalid")
        if str(feedback_packet.get("source_causal_event_digest", "")) != action_event_digest:
            blockers.append("approved_action_feedback_event_digest_mismatch")
        if str(feedback_packet.get("source_causal_result_digest", "")) != sha(
            action_result_file
        ):
            blockers.append("approved_action_feedback_result_digest_mismatch")
        if str(feedback_ledger.get("source_feedback_packet_digest", "")) != str(
            feedback_packet.get("feedback_packet_digest", "")
        ):
            blockers.append("approved_action_feedback_ledger_packet_mismatch")
        feedback_packet_digest = str(feedback_packet.get("feedback_packet_digest", ""))

    parent_after = _read_json(world_path)
    child_indra_after = _read_json(child_indra_path)
    parent_unchanged = bool(parent_after) and (
        str(parent_after.get("indra_qi_world_state_digest", "")) == world_digest
        and compute_indra_qi_world_state_digest(parent_after) == world_digest
    )
    child_indra_digest = str(child_indra_before.get("indra_qi_world_state_digest", ""))
    child_indra_unchanged = bool(child_indra_after) and (
        str(child_indra_after.get("indra_qi_world_state_digest", "")) == child_indra_digest
        and compute_indra_qi_world_state_digest(child_indra_after) == child_indra_digest
    )
    if not parent_unchanged:
        blockers.append("approved_action_parent_world_changed")
    if not child_indra_unchanged:
        blockers.append("approved_action_child_indra_world_changed")

    execution_status = (
        "approved_action_applied_and_feedback_returned"
        if action_ready and feedback_ready and not blockers
        else "approved_action_execution_blocked"
    )
    if execution_status == "approved_action_applied_and_feedback_returned":
        execution_record = {
            "version": "indra_qi_approved_recovery_action_execution_record_v0_9",
            "execution_status": execution_status,
            "execution_id": execution_id,
            "source_action_envelope_id": envelope_id,
            "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
            "source_action_activation_record_digest": str(
                envelope_activation.get("activation_record_digest", "")
            ),
            "source_reentry_id": reentry_id,
            "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
            "source_world_state_digest": world_digest,
            "source_dynamic_world_state_digest": dynamic_digest,
            "selected_candidate_id": str(selected_candidate.get("candidate_id", "")),
            "selected_candidate_digest": str(
                selected_candidate.get("action_candidate_digest", "")
            ),
            "selected_action_kind": selected_kind,
            "fresh_observation_evidence_digest": str(evidence.get("evidence_digest", "")),
            "approval_digest": str(approval.get("approval_digest", "")),
            "execution_plan_digest": plan_digest,
            "action_transaction_id": str(plan.get("action_transaction_id", "")),
            "action_command_kind": command_kind,
            "action_command_digest": str(command.get("command_digest", "")),
            "action_event_record_digest": action_event_digest,
            "action_result_digest": action_result_digest,
            "before_v14_world_model_digest": before_v14_digest,
            "after_v14_world_model_digest": after_v14_digest,
            "state_mutated": state_mutated,
            "counterfactual_generated": counterfactual_generated,
            "snapshot_verified": snapshot_verified,
            "undo_readiness_ready": undo_readiness_ready,
            "feedback_id": str(plan.get("feedback_id", "")),
            "feedback_packet_digest": feedback_packet_digest,
            "feedback_candidate_count": feedback_count,
            "feedback_local_patch_candidate_count": feedback_local_count,
            "feedback_qi_flow_candidate_count": feedback_flow_count,
            "parent_world_state_unchanged": parent_unchanged,
            "child_indra_state_unchanged": child_indra_unchanged,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "exact_candidate_executed_once": True,
                "child_v14_action_traceable": True,
                "feedback_returned_as_candidates": True,
                "external_world_actuation_authority": False,
            },
            "epoch": int(time.time()),
        }
        execution_record["execution_record_digest"] = sha(execution_record)
        _write_json(execution_record_path, execution_record)
        ledger_record = {
            "version": "indra_qi_approved_recovery_action_execution_ledger_record_v0_9",
            "record_type": "approved_recovery_action_execution",
            "execution_id": execution_id,
            "source_action_envelope_id": envelope_id,
            "source_action_envelope_digest": str(envelope.get("action_envelope_digest", "")),
            "selected_candidate_digest": str(
                selected_candidate.get("action_candidate_digest", "")
            ),
            "source_execution_record_digest": execution_record[
                "execution_record_digest"
            ],
            "action_event_record_digest": action_event_digest,
            "after_v14_world_model_digest": after_v14_digest,
            "feedback_packet_digest": feedback_packet_digest,
            "prev_record_digest": str(
                prior_executions[-1].get("record_digest", "GENESIS")
            )
            if prior_executions
            else "GENESIS",
            "boundary": {
                "append_only_execution_lineage": True,
                "exact_candidate_consumed_once": True,
                "parent_world_state_unchanged": True,
                "feedback_candidate_only": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(execution_ledger_path, ledger_record)

    status = READY if execution_status == "approved_action_applied_and_feedback_returned" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-approved-action-"
        + sha(
            {
                "execution_id": execution_id,
                "candidate_digest": selected_digest,
                "action_event": action_event_digest,
                "feedback_packet": feedback_packet_digest,
                "blockers": blockers,
            }
        )[:16],
        "execution_id": execution_id,
        "source_action_envelope_id": envelope_id,
        "selected_candidate_id": str(plan.get("selected_candidate_id", "")),
        "selected_action_kind": selected_kind,
        "action_command_kind": command_kind,
        "action_transaction_id": str(plan.get("action_transaction_id", "")),
        "execution_status": execution_status,
        "action_invoked": action_invoked,
        "action_ready": action_ready,
        "state_mutated": state_mutated,
        "counterfactual_generated": counterfactual_generated,
        "snapshot_verified": snapshot_verified,
        "undo_readiness_ready": undo_readiness_ready,
        "feedback_invoked": feedback_invoked,
        "feedback_ready": feedback_ready,
        "feedback_candidate_count": feedback_count,
        "feedback_local_patch_candidate_count": feedback_local_count,
        "feedback_qi_flow_candidate_count": feedback_flow_count,
        "parent_world_state_unchanged": parent_unchanged,
        "child_indra_state_unchanged": child_indra_unchanged,
        "before_v14_world_model_digest": before_v14_digest,
        "after_v14_world_model_digest": after_v14_digest,
        "action_event_record_digest": action_event_digest,
        "action_result_digest": action_result_digest,
        "feedback_packet_digest": feedback_packet_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "execution_completed": execution_status
            == "approved_action_applied_and_feedback_returned",
            "external_world_actuation_authority": False,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiApprovedRecoveryActionExecutionV0_9Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        execution_id,
        envelope_id,
        str(plan.get("selected_candidate_id", "")),
        selected_kind,
        command_kind,
        str(plan.get("action_transaction_id", "")),
        execution_status,
        action_invoked,
        action_ready,
        state_mutated,
        counterfactual_generated,
        snapshot_verified,
        undo_readiness_ready,
        feedback_invoked,
        feedback_ready,
        feedback_count,
        feedback_local_count,
        feedback_flow_count,
        parent_unchanged,
        child_indra_unchanged,
        before_v14_digest,
        after_v14_digest,
        action_event_digest,
        action_result_digest,
        feedback_packet_digest,
        str(execution_record_path),
        str(execution_ledger_path),
        str(undo_readiness_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

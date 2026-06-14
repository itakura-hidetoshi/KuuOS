#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import (
    ALLOWED_ACTION_KINDS,
    REQUIRED_BOUNDARY,
    action_plan_digest,
    build_action_envelope,
    items,
    mapping,
    sha,
    valid_digest,
    validate_plan,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    dynamic_world_state_digest,
    protected_constitution_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_recoverability_action_envelope_v0_8"
READY = "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_READY"
BLOCKED = "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_BLOCKED"
LICENSE_READY = "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiRecoverabilityActionEnvelopeV0_8Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_envelope_id: str
    source_reentry_id: str
    envelope_status: str
    aggregate_gate_mode: str
    variable_gate_count: int
    observation_request_count: int
    counterfactual_candidate_count: int
    bounded_intervention_candidate_count: int
    undo_reserve_count: int
    action_executed: bool
    v14_command_invoked: bool
    parent_world_state_unchanged: bool
    child_causal_world_unchanged: bool
    source_world_state_digest: str
    source_dynamic_world_state_digest: str
    source_v14_world_model_digest: str
    action_envelope_digest: str
    action_envelope_path: str
    activation_record_path: str
    action_ledger_path: str
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


def _validate_v0_6_lineage(
    *,
    world_state: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    seed_packet: Mapping[str, Any],
    assimilation_records: list[dict[str, Any]],
    blockers: list[str],
) -> tuple[str, str, str]:
    if not world_state:
        blockers.append("recovery_action_source_world_state_missing_or_invalid")
        return "", "", ""
    world_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    dynamic_digest = str(world_state.get("process_tensor_dynamic_world_state_digest", ""))
    if compute_indra_qi_world_state_digest(world_state) != world_digest:
        blockers.append("recovery_action_source_world_state_digest_invalid")
    if dynamic_world_state_digest(world_state) != dynamic_digest:
        blockers.append("recovery_action_source_dynamic_world_state_digest_invalid")
    summary = mapping(world_state.get("process_tensor_world_state"))
    if summary.get("assimilation_status") != "dynamic_world_state_assimilated":
        blockers.append("recovery_action_source_world_not_assimilated")
    for field in (
        "debt_changes_world_state",
        "recoverability_changes_world_state",
        "non_markov_feedback_preserved",
        "uses_process_tensor_feedback",
        "candidate_weighting_not_truth",
    ):
        if mapping(summary.get("boundary")).get(field) is not True:
            blockers.append(f"recovery_action_source_world_boundary_{field}_not_true")

    if not assimilation:
        blockers.append("recovery_action_source_assimilation_record_missing")
    else:
        if assimilation.get("version") != "indra_qi_process_tensor_world_assimilation_record_v0_6":
            blockers.append("recovery_action_source_assimilation_version_invalid")
        if assimilation.get("assimilation_status") != "dynamic_world_state_assimilated":
            blockers.append("recovery_action_source_assimilation_not_ready")
        if not valid_digest(assimilation, "assimilation_record_digest"):
            blockers.append("recovery_action_source_assimilation_digest_invalid")
        if str(assimilation.get("after_world_state_digest", "")) != world_digest:
            blockers.append("recovery_action_source_assimilation_world_digest_mismatch")
        if str(assimilation.get("dynamic_world_state_digest", "")) != dynamic_digest:
            blockers.append("recovery_action_source_assimilation_dynamic_digest_mismatch")
        if assimilation.get("protected_constitution_preserved") is not True:
            blockers.append("recovery_action_source_constitution_not_preserved")
        if assimilation.get("overlay_history_preserved") is not True:
            blockers.append("recovery_action_source_overlay_history_not_preserved")

    assimilation_id = str(assimilation.get("assimilation_id", ""))
    ledger = _latest_matching(assimilation_records, "assimilation_id", assimilation_id)
    if not ledger:
        blockers.append("recovery_action_source_assimilation_ledger_missing")
    else:
        if not valid_digest(ledger, "record_digest"):
            blockers.append("recovery_action_source_assimilation_ledger_digest_invalid")
        if str(ledger.get("source_assimilation_record_digest", "")) != str(
            assimilation.get("assimilation_record_digest", "")
        ):
            blockers.append("recovery_action_source_assimilation_ledger_record_mismatch")
        if str(ledger.get("after_world_state_digest", "")) != world_digest:
            blockers.append("recovery_action_source_assimilation_ledger_world_mismatch")

    if not seed_packet:
        blockers.append("recovery_action_source_post_assimilation_seed_missing")
    else:
        if seed_packet.get("seed_status") != "post_assimilation_projection_seed_ready":
            blockers.append("recovery_action_source_seed_not_ready")
        if not valid_digest(seed_packet, "post_assimilation_seed_packet_digest"):
            blockers.append("recovery_action_source_seed_digest_invalid")
        if str(seed_packet.get("source_world_state_digest", "")) != world_digest:
            blockers.append("recovery_action_source_seed_world_digest_mismatch")
        if str(seed_packet.get("source_dynamic_world_state_digest", "")) != dynamic_digest:
            blockers.append("recovery_action_source_seed_dynamic_digest_mismatch")
        if str(seed_packet.get("assimilation_id", "")) != assimilation_id:
            blockers.append("recovery_action_source_seed_assimilation_id_mismatch")
    return assimilation_id, world_digest, dynamic_digest


def _validate_v0_7_lineage(
    *,
    root: pathlib.Path,
    world_state: Mapping[str, Any],
    reentry: Mapping[str, Any],
    reentry_records: list[dict[str, Any]],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, pathlib.Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    if not reentry:
        blockers.append("recovery_action_source_reentry_record_missing_or_invalid")
        return "", root, {}, {}, {}
    if reentry.get("version") != "indra_qi_post_assimilation_causal_reentry_record_v0_7":
        blockers.append("recovery_action_source_reentry_version_invalid")
    if reentry.get("reentry_status") != "post_assimilation_causal_world_initialized":
        blockers.append("recovery_action_source_reentry_not_ready")
    if not valid_digest(reentry, "reentry_record_digest"):
        blockers.append("recovery_action_source_reentry_digest_invalid")
    reentry_id = str(reentry.get("reentry_id", ""))
    world_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    dynamic_digest = str(world_state.get("process_tensor_dynamic_world_state_digest", ""))
    if str(reentry.get("source_world_state_digest", "")) != world_digest:
        blockers.append("recovery_action_source_reentry_world_digest_mismatch")
    if str(reentry.get("source_dynamic_world_state_digest", "")) != dynamic_digest:
        blockers.append("recovery_action_source_reentry_dynamic_digest_mismatch")
    boundary = mapping(reentry.get("boundary"))
    for field in (
        "post_assimilation_reentry_not_truth",
        "debt_conditions_causal_projection",
        "recoverability_conditions_causal_projection",
        "effective_transport_conditions_causal_projection",
        "base_connection_not_causal_edge",
        "qi_projected_as_observable_not_substance",
        "non_markov_feedback_preserved",
        "uses_process_tensor_feedback",
        "candidate_weighting_not_truth",
        "causal_world_internal_only",
        "not_external_world_actuation_authority",
        "not_operator_algebra_mutation_authority",
        "not_world_update_authority",
        "parent_world_state_unchanged",
        "child_runtime_isolated",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"recovery_action_source_reentry_boundary_{field}_not_true")

    ledger = _latest_matching(reentry_records, "reentry_id", reentry_id)
    if not ledger:
        blockers.append("recovery_action_source_reentry_ledger_missing")
    else:
        if not valid_digest(ledger, "record_digest"):
            blockers.append("recovery_action_source_reentry_ledger_digest_invalid")
        if str(ledger.get("source_reentry_record_digest", "")) != str(
            reentry.get("reentry_record_digest", "")
        ):
            blockers.append("recovery_action_source_reentry_ledger_record_mismatch")
        if str(ledger.get("v14_world_model_digest", "")) != str(
            reentry.get("v14_world_model_digest", "")
        ):
            blockers.append("recovery_action_source_reentry_ledger_v14_mismatch")

    expected = {
        "source_reentry_id": reentry_id,
        "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
        "source_world_state_digest": world_digest,
        "source_dynamic_world_state_digest": dynamic_digest,
        "source_v14_world_model_digest": str(reentry.get("v14_world_model_digest", "")),
    }
    for field, expected_value in expected.items():
        if str(plan.get(field, "")) != expected_value:
            blockers.append(f"recovery_action_plan_{field}_mismatch")

    child_raw = str(reentry.get("child_runtime_root", ""))
    child_root = pathlib.Path(child_raw).expanduser().resolve() if child_raw else root
    allowed_parent = (root / "indra_qi_causal_reentry_cycles_v0_7").resolve()
    try:
        child_root.relative_to(allowed_parent)
    except ValueError:
        blockers.append("recovery_action_child_runtime_outside_allowed_root")
    if not child_root.is_dir():
        blockers.append("recovery_action_child_runtime_missing")

    child_world = _read_json(child_root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    generated_plan = _read_json(child_root / "indra_qi_generated_causal_projection_plan_v0_7.json")
    projection_packet = _read_json(child_root / "indra_qi_causal_projection_packet_v0_2.json")
    activation = _read_json(child_root / "indra_qi_causal_projection_activation_record_v0_2.json")
    causal_state = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
    causal_events = _records(child_root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")

    if not child_world or compute_indra_qi_world_state_digest(child_world) != world_digest:
        blockers.append("recovery_action_child_world_digest_invalid")
    if protected_constitution_digest(child_world) != protected_constitution_digest(world_state):
        blockers.append("recovery_action_child_world_constitution_mismatch")
    if sha(generated_plan) != str(reentry.get("generated_projection_plan_digest", "")):
        blockers.append("recovery_action_generated_projection_plan_digest_mismatch")
    if str(generated_plan.get("source_indra_qi_world_state_digest", "")) != world_digest:
        blockers.append("recovery_action_generated_projection_world_digest_mismatch")
    if not valid_digest(projection_packet, "projection_packet_digest"):
        blockers.append("recovery_action_projection_packet_digest_invalid")
    if str(projection_packet.get("projection_packet_digest", "")) != str(
        reentry.get("projection_packet_digest", "")
    ):
        blockers.append("recovery_action_projection_packet_reentry_mismatch")
    if not valid_digest(activation, "activation_record_digest"):
        blockers.append("recovery_action_projection_activation_digest_invalid")
    if str(activation.get("activation_record_digest", "")) != str(
        reentry.get("projection_activation_digest", "")
    ):
        blockers.append("recovery_action_projection_activation_reentry_mismatch")
    if not valid_v14_digest(causal_state, "world_model_digest"):
        blockers.append("recovery_action_v14_world_model_digest_invalid")
    if str(causal_state.get("world_model_digest", "")) != str(
        reentry.get("v14_world_model_digest", "")
    ):
        blockers.append("recovery_action_v14_reentry_digest_mismatch")
    if str(causal_state.get("world_id", "")) != str(reentry.get("causal_world_id", "")):
        blockers.append("recovery_action_v14_world_id_mismatch")
    if len(causal_events) != 1:
        blockers.append("recovery_action_v14_initial_event_count_invalid")
    elif not valid_digest(causal_events[0], "record_digest"):
        blockers.append("recovery_action_v14_initial_event_digest_invalid")
    elif causal_events[0].get("command_kind") != "initialize":
        blockers.append("recovery_action_v14_initial_event_not_initialize")
    return reentry_id, child_root, generated_plan, projection_packet, causal_state


def build_indra_qi_recoverability_action_envelope_v0_8(
    *,
    runtime_context: Mapping[str, Any],
    action_plan: Mapping[str, Any],
    action_license: Mapping[str, Any],
) -> IndraQiRecoverabilityActionEnvelopeV0_8Result:
    context = mapping(runtime_context)
    plan = dict(mapping(action_plan))
    license_value = mapping(action_license)
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
    activation_path = root / "indra_qi_recoverability_action_envelope_record_v0_8.json"
    ledger_path = root / "indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl"
    receipt_path = root / "indra_qi_recoverability_action_envelope_receipt_v0_8.json"
    audit_path = root / "indra_qi_recoverability_action_envelope_audit_v0_8.jsonl"

    if context.get("indra_qi_recoverability_action_envelope_v0_8_enabled") is not True:
        blockers.append("indra_qi_recoverability_action_envelope_v0_8_enabled_not_true")
    if context.get("build_indra_qi_recoverability_action_envelope_v0_8") is not True:
        blockers.append("build_indra_qi_recoverability_action_envelope_v0_8_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("recovery_action_license_not_ready")
    for flag in (
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
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("action_plan_digest", ""))
    if str(license_value.get("bound_action_plan_digest", "")) != plan_digest:
        blockers.append("recovery_action_license_plan_digest_mismatch")
    allowed_raw = license_value.get("allowed_action_kinds", [])
    allowed = {str(value) for value in allowed_raw} if isinstance(allowed_raw, list) else set()
    if allowed != ALLOWED_ACTION_KINDS:
        blockers.append("recovery_action_license_allowed_action_kinds_not_exact")

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

    envelope_id = str(plan.get("action_envelope_id", ""))
    prior_records = _records(ledger_path)
    if envelope_id and any(
        str(record.get("action_envelope_id", "")) == envelope_id
        for record in prior_records
    ):
        blockers.append("recovery_action_envelope_id_replay")
    if reentry_id and any(
        str(record.get("source_reentry_id", "")) == reentry_id
        for record in prior_records
    ):
        blockers.append("recovery_action_source_reentry_replay")

    parent_before_digest = world_digest
    child_before_digest = str(causal_state.get("world_model_digest", ""))
    envelope: dict[str, Any] = {}
    if not blockers:
        envelope = build_action_envelope(
            plan=plan,
            world_state=world_state,
            generated_projection_plan=generated_plan,
            causal_state=causal_state,
            blockers=blockers,
        )
        for collection in (
            "observation_requests",
            "counterfactual_candidates",
            "bounded_intervention_candidates",
            "undo_reserves",
        ):
            for candidate in items(envelope.get(collection)):
                if str(mapping(candidate).get("action_kind", "")) not in allowed:
                    blockers.append("recovery_action_candidate_kind_not_licensed")
                if not valid_digest(mapping(candidate), "action_candidate_digest"):
                    blockers.append("recovery_action_candidate_digest_invalid")
        if not valid_digest(envelope, "action_envelope_digest"):
            blockers.append("recovery_action_envelope_digest_invalid")

    parent_after = _read_json(world_path)
    child_after = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
    parent_unchanged = bool(parent_after) and (
        str(parent_after.get("indra_qi_world_state_digest", "")) == parent_before_digest
        and compute_indra_qi_world_state_digest(parent_after) == parent_before_digest
    )
    child_unchanged = bool(child_after) and (
        str(child_after.get("world_model_digest", "")) == child_before_digest
        and valid_v14_digest(child_after, "world_model_digest")
    )
    if not parent_unchanged:
        blockers.append("recovery_action_parent_world_changed")
    if not child_unchanged:
        blockers.append("recovery_action_child_causal_world_changed")

    envelope_status = (
        "recoverability_gated_action_candidates_ready"
        if envelope and not blockers
        else "recoverability_action_envelope_blocked"
    )
    envelope_digest = str(envelope.get("action_envelope_digest", ""))
    aggregate_mode = str(envelope.get("aggregate_gate_mode", ""))
    budgets = mapping(envelope.get("budgets"))
    if envelope_status == "recoverability_gated_action_candidates_ready":
        envelope.update(
            {
                "source_reentry_id": reentry_id,
                "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
                "source_world_state_digest": world_digest,
                "source_dynamic_world_state_digest": dynamic_digest,
                "source_v14_world_model_digest": child_before_digest,
                "source_projection_packet_digest": str(
                    projection_packet.get("projection_packet_digest", "")
                ),
                "action_plan_digest": plan_digest,
            }
        )
        envelope["action_envelope_digest"] = sha(
            {key: value for key, value in envelope.items() if key != "action_envelope_digest"}
        )
        envelope_digest = str(envelope["action_envelope_digest"])
        _write_json(envelope_path, envelope)

        activation = {
            "version": "indra_qi_recoverability_action_envelope_record_v0_8",
            "envelope_status": envelope_status,
            "action_envelope_id": envelope_id,
            "source_reentry_id": reentry_id,
            "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
            "source_world_state_digest": world_digest,
            "source_dynamic_world_state_digest": dynamic_digest,
            "source_v14_world_model_digest": child_before_digest,
            "source_action_plan_digest": plan_digest,
            "source_action_envelope_digest": envelope_digest,
            "aggregate_gate_mode": aggregate_mode,
            "variable_gate_count": len(items(envelope.get("variable_gates"))),
            "observation_request_count": int(budgets.get("observation_request_count", 0)),
            "counterfactual_candidate_count": int(
                budgets.get("counterfactual_candidate_count", 0)
            ),
            "bounded_intervention_candidate_count": int(
                budgets.get("bounded_intervention_candidate_count", 0)
            ),
            "undo_reserve_count": int(budgets.get("undo_reserve_count", 0)),
            "action_executed": False,
            "v14_command_invoked": False,
            "parent_world_state_unchanged": True,
            "child_causal_world_unchanged": True,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "action_envelope_generated": True,
                "candidate_only_surface": True,
                "approval_and_fresh_license_required": True,
            },
            "epoch": int(time.time()),
        }
        activation["activation_record_digest"] = sha(activation)
        _write_json(activation_path, activation)

        ledger_record = {
            "version": "indra_qi_recoverability_action_envelope_ledger_record_v0_8",
            "record_type": "recoverability_gated_action_envelope",
            "action_envelope_id": envelope_id,
            "source_reentry_id": reentry_id,
            "source_reentry_record_digest": str(reentry.get("reentry_record_digest", "")),
            "source_world_state_digest": world_digest,
            "source_dynamic_world_state_digest": dynamic_digest,
            "source_v14_world_model_digest": child_before_digest,
            "source_action_envelope_digest": envelope_digest,
            "source_activation_record_digest": activation["activation_record_digest"],
            "aggregate_gate_mode": aggregate_mode,
            "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS"))
            if prior_records
            else "GENESIS",
            "boundary": {
                "append_only_action_envelope_lineage": True,
                "candidate_only_surface": True,
                "parent_world_state_unchanged": True,
                "child_causal_world_unchanged": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(ledger_path, ledger_record)

    status = READY if envelope_status == "recoverability_gated_action_candidates_ready" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-recovery-action-"
        + sha(
            {
                "action_envelope_id": envelope_id,
                "source_reentry_id": reentry_id,
                "world_digest": world_digest,
                "v14_digest": child_before_digest,
                "envelope_digest": envelope_digest,
                "blockers": blockers,
            }
        )[:16],
        "action_envelope_id": envelope_id,
        "source_reentry_id": reentry_id,
        "envelope_status": envelope_status,
        "aggregate_gate_mode": aggregate_mode,
        "variable_gate_count": len(items(envelope.get("variable_gates"))),
        "observation_request_count": int(budgets.get("observation_request_count", 0)),
        "counterfactual_candidate_count": int(
            budgets.get("counterfactual_candidate_count", 0)
        ),
        "bounded_intervention_candidate_count": int(
            budgets.get("bounded_intervention_candidate_count", 0)
        ),
        "undo_reserve_count": int(budgets.get("undo_reserve_count", 0)),
        "action_executed": False,
        "v14_command_invoked": False,
        "parent_world_state_unchanged": parent_unchanged,
        "child_causal_world_unchanged": child_unchanged,
        "source_world_state_digest": world_digest,
        "source_dynamic_world_state_digest": dynamic_digest,
        "source_v14_world_model_digest": child_before_digest,
        "action_envelope_digest": envelope_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "envelope_completed": envelope_status
            == "recoverability_gated_action_candidates_ready",
            "no_action_executed": True,
            "no_v14_command_invoked": True,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiRecoverabilityActionEnvelopeV0_8Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        envelope_id,
        reentry_id,
        envelope_status,
        aggregate_mode,
        len(items(envelope.get("variable_gates"))),
        int(budgets.get("observation_request_count", 0)),
        int(budgets.get("counterfactual_candidate_count", 0)),
        int(budgets.get("bounded_intervention_candidate_count", 0)),
        int(budgets.get("undo_reserve_count", 0)),
        False,
        False,
        parent_unchanged,
        child_unchanged,
        world_digest,
        dynamic_digest,
        child_before_digest,
        envelope_digest,
        str(envelope_path),
        str(activation_path),
        str(ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

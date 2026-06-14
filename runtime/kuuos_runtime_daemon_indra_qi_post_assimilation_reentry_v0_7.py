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

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_post_assimilation_reentry_core_v0_7 import (
    REQUIRED_BOUNDARY,
    build_projection_plan,
    items,
    mapping,
    reentry_plan_digest,
    sha,
    valid_digest,
    validate_plan,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    dynamic_world_state_digest,
    protected_constitution_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_causal_projection_bridge_v0_2 import (
    build_indra_qi_causal_projection_bridge_v0_2,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_post_assimilation_causal_reentry_v0_7"
READY = "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_READY"
BLOCKED = "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_BLOCKED"
LICENSE_READY = "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiPostAssimilationCausalReentryV0_7Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    reentry_id: str
    source_assimilation_id: str
    reentry_status: str
    child_runtime_root: str
    projection_id: str
    causal_world_id: str
    transaction_id: str
    projected_variable_count: int
    observed_variable_count: int
    qi_flow_variable_count: int
    v0_2_projection_invoked: bool
    v0_2_projection_ready: bool
    v14_state_initialized: bool
    parent_world_state_unchanged: bool
    source_world_state_digest: str
    source_dynamic_world_state_digest: str
    projection_packet_digest: str
    projection_activation_digest: str
    v14_world_model_digest: str
    reentry_record_path: str
    reentry_ledger_path: str
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


def _validate_sources(
    *,
    world_state: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    seed_packet: Mapping[str, Any],
    assimilation_records: list[dict[str, Any]],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, str, str, Mapping[str, Any]]:
    if not world_state:
        blockers.append("source_assimilated_world_state_missing_or_invalid")
    if not assimilation:
        blockers.append("source_v0_6_assimilation_record_missing_or_invalid")
    if not seed_packet:
        blockers.append("source_v0_6_post_assimilation_seed_missing_or_invalid")

    world_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    dynamic_digest = str(world_state.get("process_tensor_dynamic_world_state_digest", ""))
    if world_state and compute_indra_qi_world_state_digest(world_state) != world_digest:
        blockers.append("source_assimilated_world_state_digest_invalid")
    if world_state and dynamic_world_state_digest(world_state) != dynamic_digest:
        blockers.append("source_dynamic_world_state_digest_invalid")
    summary = mapping(world_state.get("process_tensor_world_state"))
    if summary.get("assimilation_status") != "dynamic_world_state_assimilated":
        blockers.append("source_process_tensor_world_state_not_assimilated")
    if summary.get("boundary", {}).get("debt_changes_world_state") is not True:
        blockers.append("source_world_debt_change_boundary_missing")
    if summary.get("boundary", {}).get("recoverability_changes_world_state") is not True:
        blockers.append("source_world_recoverability_change_boundary_missing")

    if assimilation:
        if assimilation.get("version") != "indra_qi_process_tensor_world_assimilation_record_v0_6":
            blockers.append("source_v0_6_assimilation_record_version_invalid")
        if assimilation.get("assimilation_status") != "dynamic_world_state_assimilated":
            blockers.append("source_v0_6_assimilation_not_completed")
        if not valid_digest(assimilation, "assimilation_record_digest"):
            blockers.append("source_v0_6_assimilation_record_digest_invalid")
        if str(assimilation.get("after_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_6_assimilation_world_digest_mismatch")
        if str(assimilation.get("dynamic_world_state_digest", "")) != dynamic_digest:
            blockers.append("source_v0_6_assimilation_dynamic_digest_mismatch")
        if assimilation.get("protected_constitution_preserved") is not True:
            blockers.append("source_v0_6_constitution_not_preserved")
        if assimilation.get("overlay_history_preserved") is not True:
            blockers.append("source_v0_6_overlay_history_not_preserved")
        boundary = mapping(assimilation.get("boundary"))
        for field, expected in REQUIRED_BOUNDARY.items():
            if field in {
                "post_assimilation_reentry_not_truth",
                "new_world_digest_required",
                "debt_conditions_causal_projection",
                "recoverability_conditions_causal_projection",
                "effective_transport_conditions_causal_projection",
                "base_connection_not_causal_edge",
                "qi_projected_as_observable_not_substance",
                "causal_world_internal_only",
                "new_projection_license_required",
            }:
                continue
        for field in (
            "dynamic_world_state_layer_only",
            "debt_changes_world_state",
            "recoverability_changes_world_state",
            "effective_transport_not_base_connection_mutation",
            "effective_holonomy_not_base_holonomy_replacement",
            "operator_algebra_unchanged",
            "gauge_connection_identity_unchanged",
            "mandala_noncollapse_preserved",
            "two_truths_gap_preserved",
            "non_markov_feedback_preserved",
            "uses_process_tensor_feedback",
            "candidate_weighting_not_truth",
            "not_direct_execution_authority",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"source_v0_6_assimilation_boundary_{field}_not_true")
        if boundary.get("external_world_actuation_authority") is not False:
            blockers.append("source_v0_6_external_world_actuation_authority_not_false")

    assimilation_id = str(assimilation.get("assimilation_id", ""))
    matching_record: Mapping[str, Any] = {}
    for record in reversed(assimilation_records):
        if str(record.get("assimilation_id", "")) == assimilation_id:
            matching_record = record
            break
    if not matching_record:
        blockers.append("source_v0_6_assimilation_ledger_record_missing")
    else:
        if not valid_digest(matching_record, "record_digest"):
            blockers.append("source_v0_6_assimilation_ledger_digest_invalid")
        if str(matching_record.get("source_assimilation_record_digest", "")) != str(
            assimilation.get("assimilation_record_digest", "")
        ):
            blockers.append("source_v0_6_assimilation_ledger_record_mismatch")
        if str(matching_record.get("after_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_6_assimilation_ledger_world_digest_mismatch")
        if str(matching_record.get("dynamic_world_state_digest", "")) != dynamic_digest:
            blockers.append("source_v0_6_assimilation_ledger_dynamic_digest_mismatch")

    seed_digest = str(seed_packet.get("post_assimilation_seed_packet_digest", ""))
    if seed_packet:
        if seed_packet.get("version") != "indra_qi_post_assimilation_projection_seed_v0_6":
            blockers.append("source_v0_6_seed_packet_version_invalid")
        if seed_packet.get("seed_status") != "post_assimilation_projection_seed_ready":
            blockers.append("source_v0_6_seed_packet_not_ready")
        if not valid_digest(seed_packet, "post_assimilation_seed_packet_digest"):
            blockers.append("source_v0_6_seed_packet_digest_invalid")
        if str(seed_packet.get("source_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_6_seed_world_digest_mismatch")
        if str(seed_packet.get("source_dynamic_world_state_digest", "")) != dynamic_digest:
            blockers.append("source_v0_6_seed_dynamic_digest_mismatch")
        if str(seed_packet.get("assimilation_id", "")) != assimilation_id:
            blockers.append("source_v0_6_seed_assimilation_id_mismatch")
        boundary = mapping(seed_packet.get("boundary"))
        for field in (
            "post_assimilation_seed_not_fact",
            "post_assimilation_seed_not_truth",
            "post_assimilation_seed_not_direct_execution_authority",
            "post_assimilation_seed_requires_new_projection_license",
            "debt_changes_projection_conditions",
            "recoverability_changes_projection_conditions",
            "candidate_weighting_not_truth",
            "non_markov_feedback_preserved",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"source_v0_6_seed_boundary_{field}_not_true")

    expected = {
        "source_assimilation_id": assimilation_id,
        "source_assimilation_record_digest": str(assimilation.get("assimilation_record_digest", "")),
        "source_post_assimilation_seed_packet_digest": seed_digest,
        "source_world_state_digest": world_digest,
    }
    for field, expected_value in expected.items():
        if str(plan.get(field, "")) != expected_value:
            blockers.append(f"post_assimilation_reentry_plan_{field}_mismatch")
    return assimilation_id, world_digest, dynamic_digest, matching_record


def build_indra_qi_post_assimilation_causal_reentry_v0_7(
    *,
    runtime_context: Mapping[str, Any],
    reentry_plan: Mapping[str, Any],
    reentry_license: Mapping[str, Any],
) -> IndraQiPostAssimilationCausalReentryV0_7Result:
    context = mapping(runtime_context)
    plan = dict(mapping(reentry_plan))
    license_value = mapping(reentry_license)
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
    reentry_ledger_path = root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl"
    reentry_record_path = root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json"
    receipt_path = root / "indra_qi_post_assimilation_causal_reentry_receipt_v0_7.json"
    audit_path = root / "indra_qi_post_assimilation_causal_reentry_audit_v0_7.jsonl"

    reentry_id = str(plan.get("reentry_id", ""))
    child_root = root / "indra_qi_causal_reentry_cycles_v0_7" / _safe_id(reentry_id)
    child_world_path = child_root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    child_plan_path = child_root / "indra_qi_generated_causal_projection_plan_v0_7.json"

    if context.get("indra_qi_post_assimilation_causal_reentry_v0_7_enabled") is not True:
        blockers.append("indra_qi_post_assimilation_causal_reentry_v0_7_enabled_not_true")
    if context.get("invoke_indra_qi_post_assimilation_causal_reentry_v0_7") is not True:
        blockers.append("invoke_indra_qi_post_assimilation_causal_reentry_v0_7_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("post_assimilation_reentry_license_not_ready")
    for flag in (
        "world_state_read_allowed",
        "assimilation_record_read_allowed",
        "post_assimilation_seed_read_allowed",
        "assimilation_ledger_read_allowed",
        "reentry_plan_validate_allowed",
        "child_runtime_create_allowed",
        "child_world_state_copy_allowed",
        "generated_projection_plan_write_allowed",
        "v0_2_projection_invoke_allowed",
        "reentry_record_write_allowed",
        "reentry_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("reentry_plan_digest", ""))
    if str(license_value.get("bound_reentry_plan_digest", "")) != plan_digest:
        blockers.append("post_assimilation_reentry_license_plan_digest_mismatch")

    world_state = _read_json(world_path)
    assimilation = _read_json(assimilation_path)
    seed_packet = _read_json(seed_path)
    assimilation_records = _records(assimilation_ledger_path)
    source_assimilation_id, world_digest, dynamic_digest, _ = _validate_sources(
        world_state=world_state,
        assimilation=assimilation,
        seed_packet=seed_packet,
        assimilation_records=assimilation_records,
        plan=plan,
        blockers=blockers,
    )

    reentry_records = _records(reentry_ledger_path)
    if reentry_id and any(str(record.get("reentry_id", "")) == reentry_id for record in reentry_records):
        blockers.append("post_assimilation_reentry_id_replay")
    if source_assimilation_id and any(
        str(record.get("source_assimilation_id", "")) == source_assimilation_id
        for record in reentry_records
    ):
        blockers.append("source_assimilation_reentry_replay")
    if child_root.exists():
        blockers.append("post_assimilation_reentry_child_runtime_already_exists")

    projection_plan, source_names = build_projection_plan(
        reentry_plan=plan,
        world_state=world_state,
        seed_packet=seed_packet,
        blockers=blockers,
    )
    variables = mapping(projection_plan.get("variables"))
    observed_count = sum(
        1 for variable in variables.values() if mapping(variable).get("status") == "observed"
    )
    flow_count = sum(
        1
        for variable in variables.values()
        if mapping(mapping(variable).get("source_binding")).get("binding_kind")
        == "qi_flow_observable_projection"
    )

    nested = deepcopy(dict(mapping(license_value.get("v0_2_projection_license_template"))))
    if nested.get("license_status") != "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_LICENSE_READY":
        blockers.append("post_assimilation_reentry_nested_v0_2_license_not_ready")
    nested_v14 = deepcopy(dict(mapping(nested.get("v14_initialize_license_template"))))
    if nested_v14.get("license_status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY":
        blockers.append("post_assimilation_reentry_nested_v14_license_not_ready")
    nested_v14["allowed_variables"] = list(variables)
    nested_v14["max_variables"] = max(int(nested_v14.get("max_variables", 0) or 0), len(variables))
    nested_v14["max_mechanisms"] = max(
        int(nested_v14.get("max_mechanisms", 0) or 0),
        len(mapping(projection_plan.get("mechanisms"))),
    )
    nested["v14_initialize_license_template"] = nested_v14

    projection_invoked = False
    projection_ready = False
    v14_initialized = False
    projection_packet_digest = ""
    projection_activation_digest = ""
    v14_world_digest = ""
    child_projection_result: dict[str, Any] = {}

    parent_constitution_digest = protected_constitution_digest(world_state) if world_state else ""
    if not blockers:
        child_root.mkdir(parents=True, exist_ok=False)
        _write_json(child_world_path, world_state)
        _write_json(child_plan_path, projection_plan)
        projection_invoked = True
        child_projection_result = build_indra_qi_causal_projection_bridge_v0_2(
            runtime_context={
                "runtime_root": str(child_root),
                "indra_qi_causal_projection_bridge_v0_2_enabled": True,
                "apply_indra_qi_causal_projection_bridge_v0_2": True,
            },
            projection_plan=projection_plan,
            projection_license=nested,
        ).to_dict()
        if child_projection_result.get("status") != "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_READY":
            blockers.append("post_assimilation_reentry_v0_2_projection_not_ready")
        else:
            projection_ready = True
            child_world = _read_json(child_world_path)
            child_packet = _read_json(child_root / "indra_qi_causal_projection_packet_v0_2.json")
            child_activation = _read_json(
                child_root / "indra_qi_causal_projection_activation_record_v0_2.json"
            )
            child_v14 = _read_json(child_root / "kuuos_causal_world_model_state_v14_0.json")
            if compute_indra_qi_world_state_digest(child_world) != world_digest:
                blockers.append("post_assimilation_reentry_child_world_digest_invalid")
            if str(child_world.get("indra_qi_world_state_digest", "")) != world_digest:
                blockers.append("post_assimilation_reentry_child_world_digest_mismatch")
            if protected_constitution_digest(child_world) != parent_constitution_digest:
                blockers.append("post_assimilation_reentry_child_constitution_changed")
            if not valid_digest(child_packet, "projection_packet_digest"):
                blockers.append("post_assimilation_reentry_projection_packet_digest_invalid")
            if not valid_digest(child_activation, "activation_record_digest"):
                blockers.append("post_assimilation_reentry_projection_activation_digest_invalid")
            if not valid_v14_digest(child_v14, "world_model_digest"):
                blockers.append("post_assimilation_reentry_v14_world_digest_invalid")
            if str(child_packet.get("source_indra_qi_world_state_digest", "")) != world_digest:
                blockers.append("post_assimilation_reentry_projection_source_world_digest_mismatch")
            if str(child_activation.get("source_projection_packet_digest", "")) != str(
                child_packet.get("projection_packet_digest", "")
            ):
                blockers.append("post_assimilation_reentry_projection_activation_packet_mismatch")
            if str(child_activation.get("v14_causal_world_model_digest", "")) != str(
                child_v14.get("world_model_digest", "")
            ):
                blockers.append("post_assimilation_reentry_projection_activation_v14_mismatch")
            if str(child_v14.get("world_id", "")) != str(plan.get("causal_world_id", "")):
                blockers.append("post_assimilation_reentry_v14_world_id_mismatch")
            if set(mapping(child_v14.get("variables"))) != set(variables):
                blockers.append("post_assimilation_reentry_v14_variable_set_mismatch")
            for name, generated in variables.items():
                if mapping(generated).get("status") != "observed":
                    continue
                initialized = mapping(mapping(child_v14.get("variables")).get(name))
                if initialized.get("value") != mapping(generated).get("value"):
                    blockers.append(f"post_assimilation_reentry_v14_{name}_value_mismatch")
                if initialized.get("uncertainty") != mapping(generated).get("uncertainty"):
                    blockers.append(f"post_assimilation_reentry_v14_{name}_uncertainty_mismatch")
            projection_packet_digest = str(child_packet.get("projection_packet_digest", ""))
            projection_activation_digest = str(child_activation.get("activation_record_digest", ""))
            v14_world_digest = str(child_v14.get("world_model_digest", ""))
            v14_initialized = not blockers

    parent_after = _read_json(world_path)
    parent_unchanged = bool(world_state) and bool(parent_after) and (
        str(parent_after.get("indra_qi_world_state_digest", "")) == world_digest
        and compute_indra_qi_world_state_digest(parent_after) == world_digest
    )
    if not parent_unchanged:
        blockers.append("parent_assimilated_world_changed_during_reentry")

    reentry_status = (
        "post_assimilation_causal_world_initialized"
        if projection_ready and v14_initialized and not blockers
        else "post_assimilation_causal_reentry_blocked"
    )
    if reentry_status == "post_assimilation_causal_world_initialized":
        record = {
            "version": "indra_qi_post_assimilation_causal_reentry_record_v0_7",
            "reentry_status": reentry_status,
            "reentry_id": reentry_id,
            "source_assimilation_id": source_assimilation_id,
            "source_assimilation_record_digest": str(
                assimilation.get("assimilation_record_digest", "")
            ),
            "source_post_assimilation_seed_packet_digest": str(
                seed_packet.get("post_assimilation_seed_packet_digest", "")
            ),
            "source_world_state_digest": world_digest,
            "source_dynamic_world_state_digest": dynamic_digest,
            "reentry_plan_digest": plan_digest,
            "generated_projection_plan_digest": sha(projection_plan),
            "projection_id": str(plan.get("projection_id", "")),
            "causal_world_id": str(plan.get("causal_world_id", "")),
            "transaction_id": str(plan.get("transaction_id", "")),
            "child_runtime_root": str(child_root),
            "source_target_variable_names": source_names,
            "projection_packet_digest": projection_packet_digest,
            "projection_activation_digest": projection_activation_digest,
            "v14_world_model_digest": v14_world_digest,
            "projected_variable_count": len(variables),
            "observed_variable_count": observed_count,
            "qi_flow_variable_count": flow_count,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "parent_world_state_unchanged": True,
                "child_runtime_isolated": True,
                "v0_2_projection_license_consumed": True,
                "v14_internal_world_initialized": True,
            },
            "epoch": int(time.time()),
        }
        record["reentry_record_digest"] = sha(record)
        _write_json(reentry_record_path, record)
        ledger_record = {
            "version": "indra_qi_post_assimilation_causal_reentry_ledger_record_v0_7",
            "record_type": "post_assimilation_causal_reentry",
            "reentry_id": reentry_id,
            "source_assimilation_id": source_assimilation_id,
            "source_assimilation_record_digest": str(
                assimilation.get("assimilation_record_digest", "")
            ),
            "source_world_state_digest": world_digest,
            "source_dynamic_world_state_digest": dynamic_digest,
            "source_reentry_record_digest": record["reentry_record_digest"],
            "projection_packet_digest": projection_packet_digest,
            "projection_activation_digest": projection_activation_digest,
            "v14_world_model_digest": v14_world_digest,
            "prev_record_digest": str(reentry_records[-1].get("record_digest", "GENESIS"))
            if reentry_records
            else "GENESIS",
            "boundary": {
                "append_only_reentry_lineage": True,
                "parent_world_state_unchanged": True,
                "child_runtime_isolated": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(reentry_ledger_path, ledger_record)

    status = READY if reentry_status == "post_assimilation_causal_world_initialized" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-post-assimilation-reentry-"
        + sha(
            {
                "reentry_id": reentry_id,
                "world_digest": world_digest,
                "dynamic_digest": dynamic_digest,
                "v14_digest": v14_world_digest,
                "blockers": blockers,
            }
        )[:16],
        "reentry_id": reentry_id,
        "source_assimilation_id": source_assimilation_id,
        "reentry_status": reentry_status,
        "child_runtime_root": str(child_root),
        "projection_id": str(plan.get("projection_id", "")),
        "causal_world_id": str(plan.get("causal_world_id", "")),
        "transaction_id": str(plan.get("transaction_id", "")),
        "projected_variable_count": len(variables),
        "observed_variable_count": observed_count,
        "qi_flow_variable_count": flow_count,
        "v0_2_projection_invoked": projection_invoked,
        "v0_2_projection_ready": projection_ready,
        "v14_state_initialized": v14_initialized,
        "parent_world_state_unchanged": parent_unchanged,
        "source_world_state_digest": world_digest,
        "source_dynamic_world_state_digest": dynamic_digest,
        "projection_packet_digest": projection_packet_digest,
        "projection_activation_digest": projection_activation_digest,
        "v14_world_model_digest": v14_world_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "reentry_completed": reentry_status
            == "post_assimilation_causal_world_initialized",
            "parent_world_state_unchanged": parent_unchanged,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiPostAssimilationCausalReentryV0_7Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        reentry_id,
        source_assimilation_id,
        reentry_status,
        str(child_root),
        str(plan.get("projection_id", "")),
        str(plan.get("causal_world_id", "")),
        str(plan.get("transaction_id", "")),
        len(variables),
        observed_count,
        flow_count,
        projection_invoked,
        projection_ready,
        v14_initialized,
        parent_unchanged,
        world_digest,
        dynamic_digest,
        projection_packet_digest,
        projection_activation_digest,
        v14_world_digest,
        str(reentry_record_path),
        str(reentry_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

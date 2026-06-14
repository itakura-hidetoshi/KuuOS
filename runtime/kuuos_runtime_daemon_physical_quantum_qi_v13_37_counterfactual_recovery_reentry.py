#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_counterfactual_probe_lattice_v0_1 import (
    PROBE_TYPES,
    build_qi_counterfactual_probe_lattice,
)
from runtime.kuuos_runtime_daemon_qi_dry_run_probe_simulator_v0_1 import (
    build_qi_dry_run_probe_simulation,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0 import (
    build_physical_quantum_qi_closed_loop_path_integral_reentry,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 import (
    build_physical_quantum_qi_closed_loop_reentry_receipt_ledger,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_34_world_model_mutation import (
    compute_world_model_digest,
)

REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiV13_37CounterfactualRecoveryReentryResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    recovery_status: str
    recovery_id: str
    rollback_id: str
    mutation_id: str
    selected_probe_type: str
    candidate_count: int
    counterfactual_lattice_ready: bool
    v13_0_reentry_invoked: bool
    v13_1_receipt_ledger_invoked: bool
    closed_loop_reentry_status: str
    closed_loop_receipt_record_digest: str
    recovery_ledger_appended: bool
    counterfactual_packet_path: str
    recovery_ledger_path: str
    activation_record_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def compute_counterfactual_recovery_plan_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "recovery_plan_digest"))


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
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def _latest(path: pathlib.Path) -> dict[str, Any]:
    values = _records(path)
    return values[-1] if values else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _authority_none_packet() -> dict[str, Any]:
    return {
        "authority": "none",
        "grants_execution_authority": False,
        "grants_probe_execution_authority": False,
        "grants_dry_run_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
    }


def _validate_context(value: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    context = {key: str(value.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, item in context.items():
        if not item:
            blockers.append(f"process_tensor_context_{key}_missing")
    return context


def _nested_license_ready(
    value: Mapping[str, Any], expected_status: str, required_flags: tuple[str, ...], prefix: str, blockers: list[str]
) -> None:
    if value.get("license_status") != expected_status:
        blockers.append(f"{prefix}_license_not_ready")
    for flag in required_flags:
        if value.get(flag) is not True:
            blockers.append(f"{prefix}_{flag.replace('allowed', 'not_allowed')}")


def build_physical_quantum_qi_v13_37_counterfactual_recovery_reentry(
    *,
    runtime_context: Mapping[str, Any],
    v13_37_counterfactual_recovery_reentry_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_37CounterfactualRecoveryReentryResult:
    ctx = _m(runtime_context)
    lic = _m(v13_37_counterfactual_recovery_reentry_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    rollback_receipt_path = root / "physical_quantum_qi_v13_36_model_state_rollback_executor_receipt.json"
    rollback_ledger_path = root / "physical_quantum_qi_world_model_rollback_ledger.jsonl"
    compensation_path = root / "physical_quantum_qi_world_model_rollback_compensation_feedback.json"
    compensation_ledger_path = root / "physical_quantum_qi_world_model_rollback_compensation_feedback_ledger.jsonl"
    world_state_path = root / "physical_quantum_qi_world_model_state.json"
    execution_record_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    reentry_state_path = root / "physical_quantum_qi_reentry_weighting_state.json"
    counterfactual_packet_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json"
    recovery_ledger_path = root / "physical_quantum_qi_counterfactual_recovery_ledger.jsonl"
    activation_record_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_record.json"
    receipt_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_37_counterfactual_recovery_reentry_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_37_counterfactual_recovery_reentry_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_37_counterfactual_recovery_reentry") is not True:
        blockers.append("apply_physical_quantum_qi_v13_37_counterfactual_recovery_reentry_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_37_counterfactual_recovery_reentry_license_not_ready")
    for flag in (
        "v13_36_rollback_receipt_read_allowed",
        "rollback_ledger_read_allowed",
        "compensation_feedback_read_allowed",
        "compensation_feedback_ledger_read_allowed",
        "world_model_state_read_allowed",
        "v13_35_execution_record_read_allowed",
        "counterfactual_packet_write_allowed",
        "reentry_weighting_state_write_allowed",
        "v13_0_reentry_invoke_allowed",
        "v13_1_receipt_ledger_invoke_allowed",
        "recovery_ledger_append_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    v13_0_license = _m(lic.get("v13_0_reentry_license"))
    _nested_license_ready(
        v13_0_license,
        "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY",
        (
            "reentry_weighting_state_read_allowed",
            "closed_loop_reentry_packet_write_allowed",
            "candidate_weighting_cycle_state_write_allowed",
            "closed_loop_reentry_ledger_append_allowed",
            "summary_write_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v13_0_reentry",
        blockers,
    )
    v13_1_license = _m(lic.get("v13_1_receipt_ledger_license"))
    _nested_license_ready(
        v13_1_license,
        "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY",
        (
            "closed_loop_reentry_packet_read_allowed",
            "candidate_weighting_cycle_state_read_allowed",
            "receipt_ledger_append_allowed",
            "summary_write_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v13_1_receipt_ledger",
        blockers,
    )

    plan = dict(_m(ctx.get("counterfactual_recovery_plan")))
    recovery_id = str(plan.get("recovery_id", ""))
    rollback_id = str(plan.get("rollback_id", ""))
    mutation_id = str(plan.get("mutation_id", ""))
    if not plan:
        blockers.append("counterfactual_recovery_plan_missing")
    if not recovery_id:
        blockers.append("counterfactual_recovery_id_missing")
    if not rollback_id:
        blockers.append("counterfactual_recovery_rollback_id_missing")
    if not mutation_id:
        blockers.append("counterfactual_recovery_mutation_id_missing")
    if not plan.get("reason"):
        blockers.append("counterfactual_recovery_reason_missing")
    if plan.get("probe_only_reentry") is not True:
        blockers.append("counterfactual_recovery_probe_only_reentry_not_true")

    plan_digest = compute_counterfactual_recovery_plan_digest(plan) if plan else ""
    if str(plan.get("recovery_plan_digest", "")) != plan_digest:
        blockers.append("counterfactual_recovery_plan_digest_mismatch")
    if str(lic.get("bound_recovery_plan_digest", "")) != plan_digest:
        blockers.append("counterfactual_recovery_plan_not_bound_to_license")

    rollback_receipt = _read_json(rollback_receipt_path)
    rollback_record = _latest(rollback_ledger_path)
    compensation = _read_json(compensation_path)
    compensation_record = _latest(compensation_ledger_path)
    world_state = _read_json(world_state_path)
    execution_record = _read_json(execution_record_path)

    if not rollback_receipt:
        blockers.append("v13_36_rollback_receipt_missing_or_invalid")
    if not rollback_record:
        blockers.append("v13_36_rollback_record_missing_or_invalid")
    if not compensation:
        blockers.append("v13_36_compensation_feedback_missing_or_invalid")
    if not compensation_record:
        blockers.append("v13_36_compensation_feedback_record_missing_or_invalid")
    if not world_state:
        blockers.append("world_model_state_missing_or_invalid")
    if not execution_record:
        blockers.append("v13_35_execution_record_missing_or_invalid")

    if rollback_receipt:
        if rollback_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_READY":
            blockers.append("v13_36_rollback_receipt_not_ready")
        if rollback_receipt.get("rollback_status") != "model_state_rollback_applied":
            blockers.append("v13_36_rollback_not_applied")
        for flag in ("world_model_restored", "rollback_ledger_appended", "compensation_feedback_appended"):
            if rollback_receipt.get(flag) is not True:
                blockers.append(f"v13_36_{flag}_not_true")
        if str(rollback_receipt.get("rollback_id", "")) != rollback_id:
            blockers.append("v13_36_rollback_id_mismatch")
        if str(rollback_receipt.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_36_mutation_id_mismatch")

    if rollback_record:
        if rollback_record.get("record_type") != "physical_quantum_qi_world_model_rollback":
            blockers.append("v13_36_rollback_record_type_invalid")
        if rollback_record.get("rollback_status") != "model_state_rollback_applied":
            blockers.append("v13_36_rollback_record_status_invalid")
        if str(rollback_record.get("record_digest", "")) != str(rollback_receipt.get("rollback_record_digest", "")):
            blockers.append("v13_36_rollback_record_digest_mismatch")
        if str(rollback_record.get("rollback_id", "")) != rollback_id or str(rollback_record.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_36_rollback_record_identity_mismatch")

    compensation_digest = _sha(_without(compensation, "rollback_compensation_feedback_digest")) if compensation else ""
    if compensation:
        if compensation.get("feedback_status") != "process_tensor_feedback_compensate_rollback":
            blockers.append("v13_36_compensation_feedback_status_invalid")
        if str(compensation.get("rollback_compensation_feedback_digest", "")) != compensation_digest:
            blockers.append("v13_36_compensation_feedback_digest_invalid")
        if compensation_digest != str(rollback_receipt.get("compensation_feedback_digest", "")):
            blockers.append("v13_36_compensation_feedback_receipt_digest_mismatch")
        if dict(compensation_record) != dict(compensation):
            blockers.append("v13_36_compensation_feedback_ledger_mismatch")
        source_digests = _m(compensation.get("source_digests"))
        if str(source_digests.get("rollback_record", "")) != str(rollback_record.get("record_digest", "")):
            blockers.append("v13_36_compensation_rollback_record_trace_mismatch")
        kernel = _m(compensation.get("process_tensor_feedback_kernel"))
        if int(kernel.get("path_weight_delta", 0) or 0) >= 0:
            blockers.append("v13_36_compensation_path_weight_not_negative")
        if int(kernel.get("memory_feedback_weight", 0) or 0) <= 0:
            blockers.append("v13_36_compensation_memory_weight_not_positive")
        if int(kernel.get("external_backaction_weight", 0) or 0) <= 0:
            blockers.append("v13_36_compensation_external_weight_not_positive")
        if int(kernel.get("next_cycle_amplitude_delta", 0) or 0) != 0:
            blockers.append("v13_36_compensation_next_cycle_amplitude_not_zero")
        if kernel.get("rollback_compensation_required") is not True or kernel.get("non_markov_feedback_required") is not True:
            blockers.append("v13_36_compensation_kernel_boundary_invalid")
        effects = _m(compensation.get("observed_effects"))
        if effects.get("world_model_restored") is not True or effects.get("next_cycle_requires_reassessment") is not True:
            blockers.append("v13_36_compensation_observed_effects_invalid")

    restored_world_digest = compute_world_model_digest(world_state) if world_state else ""
    if world_state:
        if str(world_state.get("world_model_digest", "")) != restored_world_digest:
            blockers.append("restored_world_model_embedded_digest_mismatch")
        if restored_world_digest != str(rollback_receipt.get("restored_world_model_digest", "")):
            blockers.append("restored_world_model_receipt_digest_mismatch")
        if restored_world_digest != str(rollback_record.get("restored_world_model_digest", "")):
            blockers.append("restored_world_model_record_digest_mismatch")

    process_context = _validate_context(_m(execution_record.get("process_tensor_context")), blockers)
    if execution_record:
        if execution_record.get("execution_status") != "guarded_transition_executed":
            blockers.append("v13_35_execution_record_status_invalid")
        if str(execution_record.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_35_execution_record_mutation_id_mismatch")

    candidate_values = plan.get("candidate_probe_types", PROBE_TYPES)
    candidate_probe_types = [str(value) for value in candidate_values] if isinstance(candidate_values, list) else []
    excluded_values = plan.get("excluded_probe_types", [])
    excluded = {str(value) for value in excluded_values} if isinstance(excluded_values, list) else set()
    candidates = [value for value in candidate_probe_types if value in PROBE_TYPES and value not in excluded]
    candidates = list(dict.fromkeys(candidates))
    if not candidates:
        blockers.append("counterfactual_recovery_candidate_probe_types_missing")
    preferred = str(plan.get("preferred_probe_type", "safe_reentry_window_probe"))
    if preferred not in candidates and candidates:
        preferred = candidates[0]
    target_slice = str(plan.get("target_time_slice", "rollback_reassessment_window"))

    previous_recoveries = _records(recovery_ledger_path)
    if recovery_id and any(str(record.get("recovery_id", "")) == recovery_id for record in previous_recoveries):
        blockers.append("counterfactual_recovery_id_replay")
    if rollback_id and any(str(record.get("rollback_id", "")) == rollback_id for record in previous_recoveries):
        blockers.append("counterfactual_recovery_rollback_already_consumed")

    dry_run: dict[str, Any] = {}
    lattice: dict[str, Any] = {}
    selected_probe = ""
    counterfactual_packet: dict[str, Any] = {}
    lattice_ready = v13_0_invoked = v13_1_invoked = recovery_appended = False
    v13_0_result: dict[str, Any] = {}
    v13_1_result: dict[str, Any] = {}
    receipt_record: dict[str, Any] = {}

    if not blockers:
        authority = _authority_none_packet()
        license_candidate = {
            "gate_status": "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY",
            "candidate_license_kind": "dry_run_probe_simulation_candidate",
            "license_candidate_only": True,
            "dry_run_candidate_only": True,
            **authority,
        }
        trend_summary = {
            "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
            "summary_only": True,
            "read_only": True,
            "latest_recommended_probe_type": preferred,
            "dominant_probe_type": preferred,
            "latest_probe_target_time_slice": target_slice,
            "latest_process_tensor_probe_plan": {
                "recommended_probe_type": preferred,
                "probe_target_time_slice": target_slice,
            },
            **authority,
        }
        dry_run = build_qi_dry_run_probe_simulation(
            license_candidate=license_candidate,
            trend_summary=trend_summary,
        ).to_dict()
        if dry_run.get("simulation_status") != "QI_DRY_RUN_PROBE_SIMULATION_READY":
            blockers.append("counterfactual_recovery_dry_run_not_ready")

        lattice = build_qi_counterfactual_probe_lattice(
            dry_run_simulation=dry_run,
            trend_summary=trend_summary,
            candidate_probe_types=candidates,
        ).to_dict()
        if lattice.get("lattice_status") != "QI_COUNTERFACTUAL_PROBE_LATTICE_READY":
            blockers.append("counterfactual_recovery_lattice_not_ready")
        for flag in ("counterfactual_only", "simulation_only", "dry_run_only"):
            if lattice.get(flag) is not True:
                blockers.append(f"counterfactual_recovery_lattice_{flag}_not_true")
        for flag in ("state_mutation_performed", "control_packet_mutation_performed", "memory_write_performed"):
            if lattice.get(flag) is not False:
                blockers.append(f"counterfactual_recovery_lattice_{flag}_not_false")
        if lattice.get("authority") != "none" or lattice.get("grants_world_update_authority") is not False:
            blockers.append("counterfactual_recovery_lattice_authority_invalid")
        selected_probe = str(lattice.get("recommended_probe_type", ""))
        if not selected_probe or selected_probe not in candidates or selected_probe in excluded:
            blockers.append("counterfactual_recovery_selected_probe_invalid")
        if int(lattice.get("candidate_count", 0) or 0) != len(candidates):
            blockers.append("counterfactual_recovery_candidate_count_mismatch")
        lattice_ready = not blockers

    if lattice_ready:
        epoch = int(time.time())
        counterfactual_packet = {
            "version": "physical_quantum_qi_v13_37_counterfactual_recovery_packet",
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "recovery_status": "counterfactual_recovery_probe_selected",
            "selected_probe_type": selected_probe,
            "simulated_probe_type": str(dry_run.get("simulated_probe_type", "")),
            "target_time_slice": target_slice,
            "candidate_count": len(candidates),
            "ranked_candidates": list(lattice.get("ranked_candidates", [])),
            "source_digests": {
                "rollback_record": str(rollback_record.get("record_digest", "")),
                "rollback_compensation_feedback": compensation_digest,
                "restored_world_model": restored_world_digest,
                "recovery_plan": plan_digest,
            },
            "process_tensor_context": process_context,
            "boundary": {
                "counterfactual_recovery_only": True,
                "alternative_path_probe_only": True,
                "rollback_path_not_reinforced": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "license_gated_reentry": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        counterfactual_packet["counterfactual_recovery_packet_digest"] = _sha(counterfactual_packet)
        _write_json(counterfactual_packet_path, counterfactual_packet)

        reentry_state = {
            "version": "physical_quantum_qi_reentry_weighting_state_v13_37_counterfactual_recovery",
            "reentry_weighting_state_ready": True,
            "can_feed_next_path_integral_reentry": True,
            "feedback_status": "process_tensor_feedback_compensate_rollback",
            "reentry_weighting_status": "counterfactual_recovery_probe_ready",
            "reentry_weighting_action": "open_probe_potential",
            "selected_counterfactual_probe_type": selected_probe,
            "candidate_weighting": {
                "path_weight_delta": 0,
                "probe_potential_required": True,
                "barrier_potential_required": False,
                "barrier_blocks_ready_weight": False,
                "memory_feedback_weight": 0,
                "external_backaction_weight": 0,
                "next_cycle_amplitude_delta": 0,
            },
            "process_tensor_context": process_context,
            "source_feedback_to_reentry_weighting_bridge_digest": counterfactual_packet[
                "counterfactual_recovery_packet_digest"
            ],
            "boundary": {
                "reentry_weighting_state_only": True,
                "can_feed_next_path_integral_reentry": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "rollback_path_not_reinforced": True,
                "counterfactual_probe_only": True,
            },
            "epoch": epoch,
        }
        reentry_state["reentry_weighting_state_digest"] = _sha(reentry_state)
        _write_json(reentry_state_path, reentry_state)

        v13_0_result = build_physical_quantum_qi_closed_loop_path_integral_reentry(
            runtime_context={
                "physical_quantum_qi_closed_loop_path_integral_reentry_enabled": True,
                "apply_physical_quantum_qi_closed_loop_path_integral_reentry": True,
                "runtime_root": str(root),
            },
            closed_loop_path_integral_reentry_license=dict(v13_0_license),
        ).to_dict()
        v13_0_invoked = True
        if v13_0_result.get("status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY":
            blockers.append("v13_0_counterfactual_reentry_not_ready")
        if (
            v13_0_result.get("closed_loop_reentry_status") != "closed_loop_reentry_probe_opened"
            or v13_0_result.get("reentry_weighting_action") != "open_probe_potential"
            or v13_0_result.get("probe_potential_required") is not True
            or int(v13_0_result.get("path_weight_delta", 0) or 0) != 0
            or v13_0_result.get("barrier_potential_required") is not False
        ):
            blockers.append("v13_0_counterfactual_reentry_semantics_mismatch")

    if v13_0_invoked and not blockers:
        v13_1_result = build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger": True,
                "runtime_root": str(root),
            },
            closed_loop_reentry_receipt_ledger_license=dict(v13_1_license),
        ).to_dict()
        v13_1_invoked = True
        if v13_1_result.get("status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY":
            blockers.append("v13_1_counterfactual_reentry_receipt_not_ready")
        if (
            v13_1_result.get("closed_loop_reentry_status") != "closed_loop_reentry_probe_opened"
            or v13_1_result.get("reentry_weighting_action") != "open_probe_potential"
            or v13_1_result.get("probe_potential_required") is not True
            or v13_1_result.get("barrier_potential_required") is not False
            or int(v13_1_result.get("path_weight_delta", 0) or 0) != 0
        ):
            blockers.append("v13_1_counterfactual_reentry_receipt_semantics_mismatch")
        receipt_record = _latest(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl")
        if str(receipt_record.get("record_digest", "")) != str(v13_1_result.get("record_digest", "")):
            blockers.append("v13_1_counterfactual_reentry_record_digest_mismatch")

    recovery_status = (
        "counterfactual_recovery_reentry_completed"
        if lattice_ready and v13_0_invoked and v13_1_invoked and not blockers
        else "counterfactual_recovery_reentry_blocked"
    )
    activation_record: dict[str, Any] = {}
    if lattice_ready or v13_0_invoked or v13_1_invoked:
        activation_record = {
            "version": "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_record",
            "recovery_status": recovery_status,
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "candidate_count": len(candidates),
            "closed_loop_reentry_status": str(v13_1_result.get("closed_loop_reentry_status", "")),
            "source_v13_36_rollback_record_digest": str(rollback_record.get("record_digest", "")),
            "source_v13_36_compensation_feedback_digest": compensation_digest,
            "source_restored_world_model_digest": restored_world_digest,
            "source_counterfactual_recovery_packet_digest": str(
                counterfactual_packet.get("counterfactual_recovery_packet_digest", "")
            ),
            "source_v13_0_closed_loop_reentry_digest": str(
                _read_json(root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json").get(
                    "closed_loop_path_integral_reentry_digest", ""
                )
            ),
            "source_v13_1_closed_loop_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "boundary": {
                "rollback_to_counterfactual_recovery": True,
                "alternative_path_probe_only": True,
                "failed_path_not_reinforced": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "runtime_local_reentry_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        activation_record["counterfactual_recovery_reentry_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

    if recovery_status == "counterfactual_recovery_reentry_completed":
        recovery_record = {
            "version": "physical_quantum_qi_counterfactual_recovery_ledger_record_v13_37",
            "record_type": "physical_quantum_qi_counterfactual_recovery_reentry",
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "recovery_status": recovery_status,
            "selected_probe_type": selected_probe,
            "candidate_count": len(candidates),
            "source_activation_record_digest": activation_record[
                "counterfactual_recovery_reentry_record_digest"
            ],
            "source_v13_36_rollback_record_digest": str(rollback_record.get("record_digest", "")),
            "source_v13_1_closed_loop_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "prev_record_digest": str(previous_recoveries[-1].get("record_digest", "GENESIS")) if previous_recoveries else "GENESIS",
            "boundary": {
                "counterfactual_recovery_receipt_only": True,
                "rollback_consumed_once": True,
                "alternative_probe_traceable": True,
                "closed_loop_reentry_traceable": True,
                "replay_protected": True,
                "non_markov_feedback_preserved": True,
            },
            "epoch": int(time.time()),
        }
        recovery_record["record_digest"] = _sha(recovery_record)
        _append_jsonl(recovery_ledger_path, recovery_record)
        recovery_appended = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_READY"
        if recovery_status == "counterfactual_recovery_reentry_completed" and recovery_appended
        else "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_37_counterfactual_recovery_reentry",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-37-counterfactual-recovery-"
        + _sha({"recovery_id": recovery_id, "probe": selected_probe, "blockers": blockers})[:16],
        "recovery_status": recovery_status,
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "selected_probe_type": selected_probe,
        "candidate_count": len(candidates),
        "counterfactual_lattice_ready": lattice_ready,
        "v13_0_reentry_invoked": v13_0_invoked,
        "v13_1_receipt_ledger_invoked": v13_1_invoked,
        "closed_loop_reentry_status": str(v13_1_result.get("closed_loop_reentry_status", "")),
        "closed_loop_receipt_record_digest": str(receipt_record.get("record_digest", "")),
        "recovery_ledger_appended": recovery_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_37CounterfactualRecoveryReentryResult(
        receipt["version"], status, receipt["packet_id"], str(root), recovery_status, recovery_id, rollback_id,
        mutation_id, selected_probe, len(candidates), lattice_ready, v13_0_invoked, v13_1_invoked,
        receipt["closed_loop_reentry_status"], receipt["closed_loop_receipt_record_digest"], recovery_appended,
        str(counterfactual_packet_path), str(recovery_ledger_path), str(activation_record_path), str(receipt_path),
        str(audit_path), blockers, warnings,
    )

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_34_world_model_mutation import compute_world_model_digest


@dataclass(frozen=True)
class PhysicalQuantumQiV13_36ModelStateRollbackExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    rollback_status: str
    rollback_id: str
    mutation_id: str
    world_model_restored: bool
    rollback_ledger_appended: bool
    compensation_feedback_appended: bool
    before_rollback_world_model_digest: str
    restored_world_model_digest: str
    rollback_record_digest: str
    compensation_feedback_digest: str
    world_model_state_path: str
    rollback_ledger_path: str
    compensation_feedback_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def compute_model_state_rollback_plan_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "rollback_plan_digest"))


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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:128] or "invalid"


def _find_mutation_record(records: list[dict[str, Any]], mutation_id: str) -> dict[str, Any]:
    for record in reversed(records):
        if str(record.get("mutation_id", "")) == mutation_id:
            return record
    return {}


def build_physical_quantum_qi_v13_36_model_state_rollback_executor(
    *,
    runtime_context: Mapping[str, Any],
    v13_36_model_state_rollback_executor_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_36ModelStateRollbackExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(v13_36_model_state_rollback_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    world_state_path = root / "physical_quantum_qi_world_model_state.json"
    activation_path = root / "physical_quantum_qi_v13_35_model_state_feedback_activation_record.json"
    mutation_ledger_path = root / "physical_quantum_qi_world_model_mutation_ledger.jsonl"
    rollback_ledger_path = root / "physical_quantum_qi_world_model_rollback_ledger.jsonl"
    compensation_feedback_path = root / "physical_quantum_qi_world_model_rollback_compensation_feedback.json"
    compensation_ledger_path = root / "physical_quantum_qi_world_model_rollback_compensation_feedback_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_36_model_state_rollback_executor_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_36_model_state_rollback_executor_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_36_model_state_rollback_executor_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_36_model_state_rollback_executor_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_36_model_state_rollback_executor") is not True:
        blockers.append("apply_physical_quantum_qi_v13_36_model_state_rollback_executor_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_36_model_state_rollback_executor_license_not_ready")
    for flag in (
        "v13_35_activation_record_read_allowed",
        "v13_34_mutation_ledger_read_allowed",
        "rollback_snapshot_read_allowed",
        "world_model_state_read_allowed",
        "world_model_state_write_allowed",
        "rollback_ledger_append_allowed",
        "compensation_feedback_write_allowed",
        "compensation_feedback_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "explicit_model_state_rollback_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    plan = dict(_m(ctx.get("model_state_rollback_plan")))
    rollback_id = str(plan.get("rollback_id", ""))
    mutation_id = str(plan.get("mutation_id", ""))
    if not plan:
        blockers.append("model_state_rollback_plan_missing")
    if not rollback_id:
        blockers.append("model_state_rollback_id_missing")
    if not mutation_id:
        blockers.append("model_state_rollback_mutation_id_missing")
    if not plan.get("reason"):
        blockers.append("model_state_rollback_reason_missing")
    if plan.get("restore_snapshot_exactly") is not True:
        blockers.append("model_state_rollback_restore_snapshot_exactly_not_true")

    plan_digest = compute_model_state_rollback_plan_digest(plan) if plan else ""
    if str(plan.get("rollback_plan_digest", "")) != plan_digest:
        blockers.append("model_state_rollback_plan_digest_mismatch")
    if str(lic.get("bound_rollback_plan_digest", "")) != plan_digest:
        blockers.append("model_state_rollback_plan_not_bound_to_license")

    activation = _read_json(activation_path)
    mutation_records = _records(mutation_ledger_path)
    mutation_record = _find_mutation_record(mutation_records, mutation_id)
    current_state = _read_json(world_state_path)
    snapshot_path = root / f"physical_quantum_qi_world_model_rollback_snapshot_{_safe_id(mutation_id)}.json"
    snapshot = _read_json(snapshot_path)

    if not activation:
        blockers.append("v13_35_activation_record_missing_or_invalid")
    if not mutation_record:
        blockers.append("v13_34_mutation_record_missing_or_invalid")
    if not current_state:
        blockers.append("world_model_state_missing_or_invalid")
    if not snapshot:
        blockers.append("rollback_snapshot_missing_or_invalid")

    if activation:
        if activation.get("activation_status") != "model_state_feedback_activation_completed":
            blockers.append("v13_35_feedback_activation_not_completed")
        if activation.get("rollback_ready") is not True:
            blockers.append("v13_35_rollback_ready_not_true")
        if str(activation.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_35_mutation_id_mismatch")
        if not activation.get("model_state_feedback_activation_record_digest"):
            blockers.append("v13_35_activation_record_digest_missing")
        if str(plan.get("source_v13_35_activation_record_digest", "")) != str(
            activation.get("model_state_feedback_activation_record_digest", "")
        ):
            blockers.append("model_state_rollback_activation_digest_mismatch")

    if mutation_record:
        if mutation_record.get("record_type") != "physical_quantum_qi_world_model_direct_mutation":
            blockers.append("v13_34_mutation_record_type_invalid")
        if mutation_record.get("mutation_status") != "world_model_direct_mutation_applied":
            blockers.append("v13_34_mutation_record_status_invalid")
        if str(activation.get("source_v13_34_mutation_record_digest", "")) != str(
            mutation_record.get("record_digest", "")
        ):
            blockers.append("v13_35_mutation_record_digest_mismatch")

    current_digest = compute_world_model_digest(current_state) if current_state else ""
    if current_state:
        if str(current_state.get("world_model_digest", "")) != current_digest:
            blockers.append("world_model_state_embedded_digest_mismatch")
        if current_digest != str(mutation_record.get("after_world_model_digest", "")):
            blockers.append("world_model_state_not_at_mutation_after_digest")
        if str(plan.get("expected_current_world_model_digest", "")) != current_digest:
            blockers.append("model_state_rollback_expected_current_digest_mismatch")

    restored_state = dict(_m(snapshot.get("world_model_state")))
    restored_digest = compute_world_model_digest(restored_state) if restored_state else ""
    snapshot_digest = _sha(_without(snapshot, "rollback_snapshot_digest")) if snapshot else ""
    if snapshot:
        if str(snapshot.get("rollback_snapshot_digest", "")) != snapshot_digest:
            blockers.append("rollback_snapshot_digest_mismatch")
        if str(mutation_record.get("rollback_snapshot_digest", "")) != snapshot_digest:
            blockers.append("mutation_record_rollback_snapshot_digest_mismatch")
        if str(snapshot.get("mutation_id", "")) != mutation_id:
            blockers.append("rollback_snapshot_mutation_id_mismatch")
        if str(snapshot.get("before_world_model_digest", "")) != restored_digest:
            blockers.append("rollback_snapshot_before_state_digest_mismatch")
        if restored_digest != str(mutation_record.get("before_world_model_digest", "")):
            blockers.append("rollback_snapshot_before_digest_mismatch")
        if str(snapshot.get("mutation_plan_digest", "")) != str(mutation_record.get("mutation_plan_digest", "")):
            blockers.append("rollback_snapshot_mutation_plan_digest_mismatch")

    rollback_records = _records(rollback_ledger_path)
    if rollback_id and any(str(record.get("rollback_id", "")) == rollback_id for record in rollback_records):
        blockers.append("model_state_rollback_id_replay")
    if mutation_id and any(str(record.get("mutation_id", "")) == mutation_id and record.get("rollback_status") == "model_state_rollback_applied" for record in rollback_records):
        blockers.append("model_state_mutation_already_rolled_back")

    restored = rollback_appended = compensation_appended = False
    rollback_record_digest = ""
    compensation_digest = ""
    before_rollback_digest = current_digest

    if not blockers:
        _write_json(world_state_path, restored_state)
        verified = _read_json(world_state_path)
        verified_digest = compute_world_model_digest(verified) if verified else ""
        if verified_digest != restored_digest or str(verified.get("world_model_digest", "")) != restored_digest:
            _write_json(world_state_path, current_state)
            blockers.append("model_state_rollback_post_write_verification_failed")
        else:
            restored = True
            epoch = int(time.time())
            rollback_record = {
                "version": "physical_quantum_qi_world_model_rollback_record_v13_36",
                "record_type": "physical_quantum_qi_world_model_rollback",
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "rollback_status": "model_state_rollback_applied",
                "before_rollback_world_model_digest": before_rollback_digest,
                "restored_world_model_digest": restored_digest,
                "source_v13_35_activation_record_digest": str(activation.get("model_state_feedback_activation_record_digest", "")),
                "source_v13_34_mutation_record_digest": str(mutation_record.get("record_digest", "")),
                "source_rollback_snapshot_digest": snapshot_digest,
                "rollback_plan_digest": plan_digest,
                "prev_record_digest": str(rollback_records[-1].get("record_digest", "GENESIS")) if rollback_records else "GENESIS",
                "boundary": {
                    "model_state_rollback_applied": True,
                    "exact_snapshot_restoration": True,
                    "optimistic_digest_lock_required": True,
                    "explicit_rollback_license_required": True,
                    "rollback_replay_protected": True,
                    "runtime_local_world_model_only": True,
                    "compensation_feedback_required": True,
                },
                "epoch": epoch,
            }
            rollback_record["record_digest"] = _sha(rollback_record)
            rollback_record_digest = rollback_record["record_digest"]
            _append_jsonl(rollback_ledger_path, rollback_record)
            rollback_appended = True

            compensation = {
                "version": "physical_quantum_qi_world_model_rollback_compensation_feedback_v13_36",
                "feedback_status": "process_tensor_feedback_compensate_rollback",
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "process_tensor_feedback_kernel": {
                    "path_weight_delta": -1,
                    "memory_feedback_weight": 1,
                    "external_backaction_weight": 1,
                    "next_cycle_amplitude_delta": 0,
                    "rollback_compensation_required": True,
                    "non_markov_feedback_required": True,
                    "history_window_feedback_required": True,
                    "instrument_trace_feedback_required": True,
                    "process_tensor_feedback_not_truth": True,
                },
                "observed_effects": {
                    "world_model_restored": True,
                    "rollback_ledger_appended": True,
                    "external_backaction_observed": True,
                    "next_cycle_requires_reassessment": True,
                },
                "source_digests": {
                    "rollback_record": rollback_record_digest,
                    "mutation_record": str(mutation_record.get("record_digest", "")),
                    "rollback_snapshot": snapshot_digest,
                    "before_rollback_world_model": before_rollback_digest,
                    "restored_world_model": restored_digest,
                },
                "boundary": {
                    "rollback_compensation_feedback_only": True,
                    "non_markov_feedback_preserved": True,
                    "history_window_feedback_preserved": True,
                    "memory_kernel_feedback_preserved": True,
                    "external_backaction_visible": True,
                    "feedback_not_direct_truth": True,
                    "feedback_not_execution_authority": True,
                    "runtime_local_feedback_only": True,
                    "fail_closed_on_boundary_loss": True,
                },
                "epoch": epoch,
            }
            compensation["rollback_compensation_feedback_digest"] = _sha(compensation)
            compensation_digest = compensation["rollback_compensation_feedback_digest"]
            _write_json(compensation_feedback_path, compensation)
            _append_jsonl(compensation_ledger_path, compensation)
            compensation_appended = True

    rollback_status = "model_state_rollback_applied" if restored and rollback_appended and compensation_appended and not blockers else "model_state_rollback_blocked"
    status = "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_READY" if rollback_status == "model_state_rollback_applied" else "PHYSICAL_QUANTUM_QI_V13_36_MODEL_STATE_ROLLBACK_EXECUTOR_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_36_model_state_rollback_executor",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-36-model-state-rollback-" + _sha({"rollback_id": rollback_id, "record": rollback_record_digest, "blockers": blockers})[:16],
        "rollback_status": rollback_status,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "world_model_restored": restored,
        "rollback_ledger_appended": rollback_appended,
        "compensation_feedback_appended": compensation_appended,
        "before_rollback_world_model_digest": before_rollback_digest,
        "restored_world_model_digest": restored_digest,
        "rollback_record_digest": rollback_record_digest,
        "compensation_feedback_digest": compensation_digest,
        "rollback_plan_digest": plan_digest,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_36ModelStateRollbackExecutorResult(
        receipt["version"], status, receipt["packet_id"], str(root), rollback_status, rollback_id, mutation_id,
        restored, rollback_appended, compensation_appended, before_rollback_digest, restored_digest,
        rollback_record_digest, compensation_digest, str(world_state_path), str(rollback_ledger_path),
        str(compensation_feedback_path), str(receipt_path), str(audit_path), blockers, warnings,
    )

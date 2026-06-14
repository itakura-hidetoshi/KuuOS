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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7 import (
    build_physical_quantum_qi_process_tensor_execution_feedback,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8 import (
    build_physical_quantum_qi_process_tensor_feedback_receipt_ledger,
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
class PhysicalQuantumQiV13_35ModelStateFeedbackActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    mutation_id: str
    rollback_ready: bool
    execution_effects_published: bool
    v12_7_feedback_invoked: bool
    v12_8_receipt_ledger_invoked: bool
    feedback_status: str
    feedback_record_digest: str
    activation_ledger_appended: bool
    activation_record_path: str
    activation_ledger_path: str
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


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:128] or "invalid"


def _validate_process_context(value: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    context = {key: str(value.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, item in context.items():
        if not item:
            blockers.append(f"process_tensor_context_{key}_missing")
    return context


def _validate_nested_license(
    value: Mapping[str, Any], expected_status: str, required_flags: tuple[str, ...], prefix: str, blockers: list[str]
) -> None:
    if value.get("license_status") != expected_status:
        blockers.append(f"{prefix}_license_not_ready")
    for flag in required_flags:
        if value.get(flag) is not True:
            blockers.append(f"{prefix}_{flag.replace('allowed', 'not_allowed')}")


def build_physical_quantum_qi_v13_35_model_state_feedback_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_35_model_state_feedback_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_35ModelStateFeedbackActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_35_model_state_feedback_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    mutation_receipt_path = root / "physical_quantum_qi_v13_34_world_model_mutation_receipt.json"
    mutation_ledger_path = root / "physical_quantum_qi_world_model_mutation_ledger.jsonl"
    world_state_path = root / "physical_quantum_qi_world_model_state.json"
    intent_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    activation_record_path = root / "physical_quantum_qi_v13_35_model_state_feedback_activation_record.json"
    activation_ledger_path = root / "physical_quantum_qi_model_state_feedback_activation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_35_model_state_feedback_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_35_model_state_feedback_activation_audit.jsonl"

    execution_record_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    next_cycle_state_path = root / "physical_quantum_qi_next_cycle_state.json"
    memory_ledger_path = root / "physical_quantum_qi_memory_consumption_ledger.jsonl"
    external_ledger_path = root / "physical_quantum_qi_external_state_mutation_ledger.jsonl"

    if ctx.get("physical_quantum_qi_v13_35_model_state_feedback_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_35_model_state_feedback_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_35_model_state_feedback_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_35_model_state_feedback_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_35_model_state_feedback_activation_license_not_ready")
    for flag in (
        "v13_34_mutation_receipt_read_allowed",
        "v13_34_mutation_ledger_read_allowed",
        "world_model_state_read_allowed",
        "rollback_snapshot_read_allowed",
        "guarded_execution_intent_packet_read_allowed",
        "execution_effect_record_write_allowed",
        "next_cycle_state_write_allowed",
        "memory_feedback_append_allowed",
        "external_backaction_append_allowed",
        "v12_7_feedback_invoke_allowed",
        "v12_8_receipt_ledger_invoke_allowed",
        "activation_record_write_allowed",
        "activation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    v12_7_license = _m(lic.get("v12_7_feedback_license"))
    _validate_nested_license(
        v12_7_license,
        "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_LICENSE_READY",
        (
            "guarded_transition_execution_record_read_allowed",
            "next_cycle_state_read_allowed",
            "memory_consumption_ledger_read_allowed",
            "external_state_mutation_ledger_read_allowed",
            "process_tensor_feedback_append_allowed",
            "path_integral_feedback_state_write_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v12_7_feedback",
        blockers,
    )
    v12_8_license = _m(lic.get("v12_8_receipt_ledger_license"))
    _validate_nested_license(
        v12_8_license,
        "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY",
        (
            "process_tensor_execution_feedback_packet_read_allowed",
            "path_integral_feedback_state_read_allowed",
            "receipt_ledger_append_allowed",
            "summary_write_allowed",
            "receipt_write_allowed",
            "audit_append_allowed",
        ),
        "v12_8_receipt_ledger",
        blockers,
    )

    mutation_receipt = _read_json(mutation_receipt_path)
    mutation_record = _latest(mutation_ledger_path)
    world_state = _read_json(world_state_path)
    intent_packet = _read_json(intent_packet_path)

    if not mutation_receipt:
        blockers.append("v13_34_mutation_receipt_missing_or_invalid")
    if not mutation_record:
        blockers.append("v13_34_mutation_record_missing_or_invalid")
    if not world_state:
        blockers.append("world_model_state_missing_or_invalid")
    if not intent_packet:
        blockers.append("guarded_execution_intent_packet_missing_or_invalid")

    mutation_id = str(mutation_receipt.get("mutation_id", ""))
    snapshot_path = root / f"physical_quantum_qi_world_model_rollback_snapshot_{_safe_id(mutation_id)}.json"
    snapshot = _read_json(snapshot_path)
    if not mutation_id:
        blockers.append("v13_34_mutation_id_missing")
    if not snapshot:
        blockers.append("v13_34_rollback_snapshot_missing_or_invalid")

    if mutation_receipt:
        if mutation_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_READY":
            blockers.append("v13_34_mutation_receipt_not_ready")
        if mutation_receipt.get("mutation_status") != "world_model_direct_mutation_applied":
            blockers.append("v13_34_mutation_not_applied")
        if mutation_receipt.get("world_model_mutated") is not True:
            blockers.append("v13_34_world_model_mutated_not_true")
        if mutation_receipt.get("rollback_snapshot_written") is not True:
            blockers.append("v13_34_rollback_snapshot_written_not_true")
        if mutation_receipt.get("mutation_ledger_appended") is not True:
            blockers.append("v13_34_mutation_ledger_appended_not_true")

    if mutation_record:
        if mutation_record.get("record_type") != "physical_quantum_qi_world_model_direct_mutation":
            blockers.append("v13_34_mutation_record_type_invalid")
        if mutation_record.get("mutation_status") != "world_model_direct_mutation_applied":
            blockers.append("v13_34_mutation_record_status_invalid")
        if str(mutation_record.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_34_mutation_id_mismatch")
        for field in ("before_world_model_digest", "after_world_model_digest", "mutation_plan_digest", "record_digest"):
            if not mutation_record.get(field):
                blockers.append(f"v13_34_mutation_record_{field}_missing")
        if str(mutation_receipt.get("before_world_model_digest", "")) != str(
            mutation_record.get("before_world_model_digest", "")
        ):
            blockers.append("v13_34_before_world_model_digest_mismatch")
        if str(mutation_receipt.get("after_world_model_digest", "")) != str(
            mutation_record.get("after_world_model_digest", "")
        ):
            blockers.append("v13_34_after_world_model_digest_mismatch")
        if str(mutation_receipt.get("mutation_plan_digest", "")) != str(mutation_record.get("mutation_plan_digest", "")):
            blockers.append("v13_34_mutation_plan_digest_mismatch")
        if str(mutation_receipt.get("source_guarded_execution_intent_digest", "")) != str(
            mutation_record.get("source_guarded_execution_intent_digest", "")
        ):
            blockers.append("v13_34_guarded_intent_digest_mismatch")

    after_digest = compute_world_model_digest(world_state) if world_state else ""
    if world_state:
        if str(world_state.get("world_model_digest", "")) != after_digest:
            blockers.append("world_model_state_embedded_digest_mismatch")
        if after_digest != str(mutation_record.get("after_world_model_digest", "")):
            blockers.append("world_model_state_after_digest_mismatch")
        if str(world_state.get("last_mutation_id", "")) != mutation_id:
            blockers.append("world_model_state_last_mutation_id_mismatch")

    rollback_ready = False
    if snapshot:
        snapshot_digest = _sha(_without(snapshot, "rollback_snapshot_digest"))
        before_state = _m(snapshot.get("world_model_state"))
        before_digest = compute_world_model_digest(before_state) if before_state else ""
        if str(snapshot.get("rollback_snapshot_digest", "")) != snapshot_digest:
            blockers.append("rollback_snapshot_digest_mismatch")
        if str(mutation_record.get("rollback_snapshot_digest", "")) != snapshot_digest:
            blockers.append("mutation_record_rollback_snapshot_digest_mismatch")
        if str(snapshot.get("mutation_id", "")) != mutation_id:
            blockers.append("rollback_snapshot_mutation_id_mismatch")
        if str(snapshot.get("before_world_model_digest", "")) != before_digest:
            blockers.append("rollback_snapshot_before_state_digest_mismatch")
        if before_digest != str(mutation_record.get("before_world_model_digest", "")):
            blockers.append("rollback_snapshot_before_digest_mismatch")
        if str(snapshot.get("mutation_plan_digest", "")) != str(mutation_record.get("mutation_plan_digest", "")):
            blockers.append("rollback_snapshot_plan_digest_mismatch")
        rollback_ready = not any(item.startswith("rollback_") or "rollback_snapshot" in item for item in blockers)

    intents_raw = intent_packet.get("guarded_execution_intents", [])
    intents = [dict(_m(item)) for item in intents_raw] if isinstance(intents_raw, list) else []
    process_context = _validate_process_context(_m(intent_packet.get("process_tensor_context")), blockers)
    if intent_packet:
        if intent_packet.get("guarded_execution_intent_status") != "guarded_execution_intent_ready":
            blockers.append("guarded_execution_intent_packet_not_ready")
        if int(intent_packet.get("guarded_execution_intent_count", 0) or 0) != 1 or len(intents) != 1:
            blockers.append("guarded_execution_intent_packet_count_not_one")
        if not intent_packet.get("guarded_execution_intent_packet_digest"):
            blockers.append("guarded_execution_intent_packet_digest_missing")
    source_intent_digest = str(intents[0].get("guarded_execution_intent_digest", "")) if intents else ""
    if source_intent_digest != str(mutation_record.get("source_guarded_execution_intent_digest", "")):
        blockers.append("feedback_source_guarded_intent_digest_mismatch")

    prior_activations = _records(activation_ledger_path)
    if mutation_id and any(str(record.get("mutation_id", "")) == mutation_id for record in prior_activations):
        blockers.append("model_state_feedback_activation_replay")

    effects_published = v12_7_invoked = v12_8_invoked = activation_ledger_appended = False
    feedback_status = "process_tensor_feedback_block_context"
    feedback_record_digest = ""
    feedback_result: dict[str, Any] = {}
    receipt_ledger_result: dict[str, Any] = {}

    if not blockers:
        epoch = int(time.time())
        execution_record = {
            "version": "physical_quantum_qi_guarded_transition_execution_record_v13_35_model_state_bridge",
            "execution_status": "guarded_transition_executed",
            "execution_layer_entrypoint": True,
            "no_dry_run_required": True,
            "effects": {
                "internal_transition_record": True,
                "next_cycle_state_update": True,
                "memory_consumption": True,
                "external_state_mutation": True,
            },
            "intent_count": 1,
            "guarded_execution_intents": intents,
            "process_tensor_context": process_context,
            "source_guarded_execution_intent_receipt_digest": str(mutation_record.get("record_digest", "")),
            "source_guarded_execution_intent_packet_digest": str(
                intent_packet.get("guarded_execution_intent_packet_digest", "")
            ),
            "source_world_model_mutation_record_digest": str(mutation_record.get("record_digest", "")),
            "source_world_model_before_digest": str(mutation_record.get("before_world_model_digest", "")),
            "source_world_model_after_digest": str(mutation_record.get("after_world_model_digest", "")),
            "mutation_id": mutation_id,
            "rollback_snapshot_digest": str(mutation_record.get("rollback_snapshot_digest", "")),
            "boundary": {
                "guarded_transition_executor": True,
                "can_update_next_cycle_state": True,
                "can_consume_memory": True,
                "can_mutate_runtime_external_state": True,
                "runtime_local_external_state_only": True,
                "license_gated_execution": True,
                "no_dry_run_required": True,
                "fail_closed_on_boundary_loss": True,
                "world_model_change_observed": True,
                "rollback_ready": True,
            },
            "epoch": epoch,
        }
        execution_record["execution_record_digest"] = _sha(execution_record)
        _write_json(execution_record_path, execution_record)

        next_cycle_state = {
            "version": "physical_quantum_qi_next_cycle_state_v13_35_model_state_feedback",
            "next_cycle_started": True,
            "source_execution_record_digest": execution_record["execution_record_digest"],
            "source_world_model_after_digest": str(mutation_record.get("after_world_model_digest", "")),
            "mutation_id": mutation_id,
            "process_tensor_context": process_context,
            "epoch": epoch,
        }
        next_cycle_state["next_cycle_state_digest"] = _sha(next_cycle_state)
        _write_json(next_cycle_state_path, next_cycle_state)

        memory_receipt = {
            "version": "physical_quantum_qi_memory_consumption_receipt_v13_35_model_state_feedback",
            "memory_consumed": True,
            "consumption_scope": "world_model_change_feedback_memory",
            "source_execution_record_digest": execution_record["execution_record_digest"],
            "source_world_model_after_digest": str(mutation_record.get("after_world_model_digest", "")),
            "mutation_id": mutation_id,
            "intent_count": 1,
            "epoch": epoch,
        }
        memory_receipt["memory_consumption_digest"] = _sha(memory_receipt)
        _append_jsonl(memory_ledger_path, memory_receipt)

        external_receipt = {
            "version": "physical_quantum_qi_external_state_mutation_receipt_v13_35_model_state_feedback",
            "external_state_mutated": True,
            "mutation_scope": "runtime_local_world_model_state",
            "source_execution_record_digest": execution_record["execution_record_digest"],
            "source_world_model_mutation_record_digest": str(mutation_record.get("record_digest", "")),
            "before_world_model_digest": str(mutation_record.get("before_world_model_digest", "")),
            "after_world_model_digest": str(mutation_record.get("after_world_model_digest", "")),
            "mutation_id": mutation_id,
            "intent_count": 1,
            "rollback_ready": rollback_ready,
            "epoch": epoch,
        }
        external_receipt["external_state_mutation_digest"] = _sha(external_receipt)
        _append_jsonl(external_ledger_path, external_receipt)
        effects_published = True

        feedback_result = build_physical_quantum_qi_process_tensor_execution_feedback(
            runtime_context={
                "physical_quantum_qi_process_tensor_execution_feedback_enabled": True,
                "apply_physical_quantum_qi_process_tensor_execution_feedback": True,
                "runtime_root": str(root),
            },
            process_tensor_execution_feedback_license=dict(v12_7_license),
        ).to_dict()
        v12_7_invoked = True
        if feedback_result.get("status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY":
            blockers.append("v12_7_process_tensor_feedback_not_ready")
        if feedback_result.get("feedback_status") != "process_tensor_feedback_reinforce_next_cycle":
            blockers.append("v12_7_feedback_status_not_reinforce")
        for flag in ("process_tensor_feedback_appended", "path_integral_feedback_state_updated", "memory_feedback_observed", "external_backaction_observed", "next_cycle_observed"):
            if feedback_result.get(flag) is not True:
                blockers.append(f"v12_7_{flag}_not_true")

    if v12_7_invoked and not blockers:
        receipt_ledger_result = build_physical_quantum_qi_process_tensor_feedback_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger": True,
                "runtime_root": str(root),
            },
            process_tensor_feedback_receipt_ledger_license=dict(v12_8_license),
        ).to_dict()
        v12_8_invoked = True
        if receipt_ledger_result.get("status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_READY":
            blockers.append("v12_8_process_tensor_feedback_receipt_not_ready")
        if receipt_ledger_result.get("feedback_status") != "process_tensor_feedback_reinforce_next_cycle":
            blockers.append("v12_8_feedback_status_not_reinforce")
        if receipt_ledger_result.get("execution_status") != "guarded_transition_executed":
            blockers.append("v12_8_execution_status_not_executed")
        if receipt_ledger_result.get("ledger_appended") is not True:
            blockers.append("v12_8_feedback_ledger_not_appended")
        for key in ("path_weight_delta", "memory_feedback_weight", "external_backaction_weight", "next_cycle_amplitude_delta"):
            if int(receipt_ledger_result.get(key, 0) or 0) <= 0:
                blockers.append(f"v12_8_{key}_not_positive")

    feedback_packet = _read_json(root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json")
    path_feedback_state = _read_json(root / "physical_quantum_qi_path_integral_feedback_state.json")
    feedback_receipt_record = _latest(root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl")
    if v12_8_invoked:
        feedback_status = str(receipt_ledger_result.get("feedback_status", feedback_status))
        feedback_record_digest = str(feedback_receipt_record.get("record_digest", ""))
        if not feedback_packet.get("process_tensor_execution_feedback_digest"):
            blockers.append("v12_7_feedback_packet_digest_missing")
        if str(path_feedback_state.get("source_process_tensor_execution_feedback_digest", "")) != str(
            feedback_packet.get("process_tensor_execution_feedback_digest", "")
        ):
            blockers.append("path_integral_feedback_source_digest_mismatch")
        if feedback_record_digest != str(receipt_ledger_result.get("record_digest", "")):
            blockers.append("v12_8_feedback_record_digest_mismatch")
        if str(feedback_receipt_record.get("source_process_tensor_execution_feedback_digest", "")) != str(
            feedback_packet.get("process_tensor_execution_feedback_digest", "")
        ):
            blockers.append("v12_8_feedback_packet_trace_mismatch")

    activation_status = (
        "model_state_feedback_activation_completed"
        if effects_published and v12_7_invoked and v12_8_invoked and rollback_ready and not blockers
        else "model_state_feedback_activation_blocked"
    )

    if v12_7_invoked or v12_8_invoked:
        epoch = int(time.time())
        activation_record = {
            "version": "physical_quantum_qi_v13_35_model_state_feedback_activation_record",
            "activation_status": activation_status,
            "mutation_id": mutation_id,
            "rollback_ready": rollback_ready,
            "feedback_status": feedback_status,
            "source_v13_34_mutation_record_digest": str(mutation_record.get("record_digest", "")),
            "source_world_model_before_digest": str(mutation_record.get("before_world_model_digest", "")),
            "source_world_model_after_digest": str(mutation_record.get("after_world_model_digest", "")),
            "source_rollback_snapshot_digest": str(mutation_record.get("rollback_snapshot_digest", "")),
            "source_guarded_execution_intent_digest": source_intent_digest,
            "source_execution_record_digest": str(_read_json(execution_record_path).get("execution_record_digest", "")),
            "source_process_tensor_feedback_digest": str(
                feedback_packet.get("process_tensor_execution_feedback_digest", "")
            ),
            "source_process_tensor_feedback_receipt_digest": feedback_record_digest,
            "boundary": {
                "world_model_change_observed_as_external_backaction": True,
                "rollback_readiness_verified": rollback_ready,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "feedback_not_direct_truth": True,
                "feedback_not_unbounded_execution": True,
                "runtime_local_feedback_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": epoch,
        }
        activation_record["model_state_feedback_activation_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)
        if not blockers and lic.get("activation_ledger_append_allowed") is True:
            activation_ledger_record = {
                "version": "physical_quantum_qi_model_state_feedback_activation_ledger_record_v13_35",
                "record_type": "physical_quantum_qi_model_state_feedback_activation",
                "mutation_id": mutation_id,
                "activation_status": activation_status,
                "feedback_status": feedback_status,
                "source_activation_record_digest": activation_record[
                    "model_state_feedback_activation_record_digest"
                ],
                "source_v13_34_mutation_record_digest": str(mutation_record.get("record_digest", "")),
                "source_process_tensor_feedback_receipt_digest": feedback_record_digest,
                "prev_record_digest": str(prior_activations[-1].get("record_digest", "GENESIS")) if prior_activations else "GENESIS",
                "boundary": {
                    "activation_receipt_only": True,
                    "mutation_feedback_traceable": True,
                    "rollback_traceable": True,
                    "replay_protected": True,
                    "non_markov_feedback_preserved": True,
                },
                "epoch": epoch,
            }
            activation_ledger_record["record_digest"] = _sha(activation_ledger_record)
            _append_jsonl(activation_ledger_path, activation_ledger_record)
            activation_ledger_appended = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_READY"
        if activation_status == "model_state_feedback_activation_completed" and activation_ledger_appended
        else "PHYSICAL_QUANTUM_QI_V13_35_MODEL_STATE_FEEDBACK_ACTIVATION_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_35_model_state_feedback_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-35-model-state-feedback-"
        + _sha({"mutation_id": mutation_id, "feedback": feedback_record_digest, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "mutation_id": mutation_id,
        "rollback_ready": rollback_ready,
        "execution_effects_published": effects_published,
        "v12_7_feedback_invoked": v12_7_invoked,
        "v12_8_receipt_ledger_invoked": v12_8_invoked,
        "feedback_status": feedback_status,
        "feedback_record_digest": feedback_record_digest,
        "activation_ledger_appended": activation_ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_35ModelStateFeedbackActivationResult(
        receipt["version"],
        status,
        receipt["packet_id"],
        str(root),
        activation_status,
        mutation_id,
        rollback_ready,
        effects_published,
        v12_7_invoked,
        v12_8_invoked,
        feedback_status,
        feedback_record_digest,
        activation_ledger_appended,
        str(activation_record_path),
        str(activation_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

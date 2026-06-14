#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2 import (
    build_physical_quantum_qi_candidate_weighting_cycle_handoff,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14 import (
    build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge,
)

EXPECTED_WEIGHTING = {
    "path_weight_delta": 0,
    "probe_potential_required": True,
    "barrier_potential_required": False,
    "barrier_blocks_ready_weight": False,
    "memory_feedback_weight": 0,
    "external_backaction_weight": 0,
    "next_cycle_amplitude_delta": 0,
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_38CounterfactualCycleHandoffResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    recovery_id: str
    rollback_id: str
    mutation_id: str
    selected_probe_type: str
    candidate_count: int
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    v13_14_bridge_invoked: bool
    v13_2_handoff_invoked: bool
    annotated_seed_written: bool
    activation_ledger_appended: bool
    annotated_seed_path: str
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


def _normalize_weighting(value: Mapping[str, Any]) -> dict[str, Any]:
    def integer(item: Any) -> int:
        try:
            return int(item or 0)
        except (TypeError, ValueError):
            return 0

    return {
        "path_weight_delta": integer(value.get("path_weight_delta")),
        "probe_potential_required": value.get("probe_potential_required") is True,
        "barrier_potential_required": value.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": value.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": integer(value.get("memory_feedback_weight")),
        "external_backaction_weight": integer(value.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": integer(value.get("next_cycle_amplitude_delta")),
    }


def _require_boundary(value: Mapping[str, Any], names: tuple[str, ...], prefix: str, blockers: list[str]) -> None:
    boundary = _m(value.get("boundary"))
    for name in names:
        if boundary.get(name) is not True:
            blockers.append(f"{prefix}_boundary_{name}_missing")


def build_physical_quantum_qi_v13_38_counterfactual_cycle_handoff(
    *,
    runtime_context: Mapping[str, Any],
    v13_38_counterfactual_cycle_handoff_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_38CounterfactualCycleHandoffResult:
    ctx = _m(runtime_context)
    lic = _m(v13_38_counterfactual_cycle_handoff_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_record.json"
    source_receipt_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_reentry_receipt.json"
    recovery_ledger_path = root / "physical_quantum_qi_counterfactual_recovery_ledger.jsonl"
    counterfactual_packet_path = root / "physical_quantum_qi_v13_37_counterfactual_recovery_packet.json"
    receipt_ledger_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
    annotated_seed_path = root / "physical_quantum_qi_v13_38_counterfactual_candidate_seed.json"
    activation_record_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record.json"
    activation_ledger_path = root / "physical_quantum_qi_counterfactual_cycle_handoff_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_38_counterfactual_cycle_handoff_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_38_counterfactual_cycle_handoff_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_38_counterfactual_cycle_handoff") is not True:
        blockers.append("apply_physical_quantum_qi_v13_38_counterfactual_cycle_handoff_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_38_counterfactual_cycle_handoff_license_not_ready")
    for flag in (
        "v13_37_activation_record_read_allowed",
        "v13_37_receipt_read_allowed",
        "v13_37_recovery_ledger_read_allowed",
        "v13_37_counterfactual_packet_read_allowed",
        "v13_1_receipt_ledger_read_allowed",
        "v13_14_bridge_invoke_allowed",
        "v13_2_handoff_invoke_allowed",
        "annotated_seed_write_allowed",
        "activation_record_write_allowed",
        "activation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    source_receipt = _read_json(source_receipt_path)
    recovery_record = _latest(recovery_ledger_path)
    counterfactual_packet = _read_json(counterfactual_packet_path)
    receipt_record = _latest(receipt_ledger_path)

    if not source:
        blockers.append("v13_37_activation_record_missing_or_invalid")
    if not source_receipt:
        blockers.append("v13_37_receipt_missing_or_invalid")
    if not recovery_record:
        blockers.append("v13_37_recovery_record_missing_or_invalid")
    if not counterfactual_packet:
        blockers.append("v13_37_counterfactual_packet_missing_or_invalid")
    if not receipt_record:
        blockers.append("v13_1_receipt_record_missing_or_invalid")

    recovery_id = str(source.get("recovery_id", ""))
    rollback_id = str(source.get("rollback_id", ""))
    mutation_id = str(source.get("mutation_id", ""))
    selected_probe = str(source.get("selected_probe_type", ""))
    try:
        candidate_count = int(source.get("candidate_count", 0) or 0)
    except (TypeError, ValueError):
        candidate_count = 0

    if source:
        if source.get("recovery_status") != "counterfactual_recovery_reentry_completed":
            blockers.append("v13_37_recovery_not_completed")
        if source.get("closed_loop_reentry_status") != "closed_loop_reentry_probe_opened":
            blockers.append("v13_37_closed_loop_reentry_not_probe")
        if not source.get("counterfactual_recovery_reentry_record_digest"):
            blockers.append("v13_37_activation_record_digest_missing")
        if not recovery_id or not rollback_id or not mutation_id:
            blockers.append("v13_37_recovery_identity_missing")
        if not selected_probe:
            blockers.append("v13_37_selected_probe_type_missing")
        if candidate_count <= 0:
            blockers.append("v13_37_candidate_count_not_positive")
        if str(source.get("source_v13_1_closed_loop_receipt_record_digest", "")) != str(
            receipt_record.get("record_digest", "")
        ):
            blockers.append("v13_37_source_receipt_record_digest_mismatch")
        if str(source.get("source_counterfactual_recovery_packet_digest", "")) != str(
            counterfactual_packet.get("counterfactual_recovery_packet_digest", "")
        ):
            blockers.append("v13_37_counterfactual_packet_digest_mismatch")
        _require_boundary(
            source,
            (
                "rollback_to_counterfactual_recovery",
                "alternative_path_probe_only",
                "failed_path_not_reinforced",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "runtime_local_reentry_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_37_activation",
            blockers,
        )

    if source_receipt:
        if source_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_37_COUNTERFACTUAL_RECOVERY_REENTRY_READY":
            blockers.append("v13_37_receipt_not_ready")
        if source_receipt.get("recovery_status") != "counterfactual_recovery_reentry_completed":
            blockers.append("v13_37_receipt_recovery_not_completed")
        if str(source_receipt.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_37_receipt_recovery_id_mismatch")
        if str(source_receipt.get("closed_loop_receipt_record_digest", "")) != str(
            receipt_record.get("record_digest", "")
        ):
            blockers.append("v13_37_receipt_record_digest_mismatch")

    if recovery_record:
        if recovery_record.get("record_type") != "physical_quantum_qi_counterfactual_recovery_reentry":
            blockers.append("v13_37_recovery_record_type_invalid")
        if recovery_record.get("recovery_status") != "counterfactual_recovery_reentry_completed":
            blockers.append("v13_37_recovery_record_status_invalid")
        if str(recovery_record.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_37_recovery_record_id_mismatch")
        if str(recovery_record.get("rollback_id", "")) != rollback_id:
            blockers.append("v13_37_recovery_record_rollback_id_mismatch")
        if str(recovery_record.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_37_recovery_record_mutation_id_mismatch")
        if str(recovery_record.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_37_recovery_record_probe_mismatch")
        if int(recovery_record.get("candidate_count", 0) or 0) != candidate_count:
            blockers.append("v13_37_recovery_record_candidate_count_mismatch")
        if str(recovery_record.get("source_activation_record_digest", "")) != str(
            source.get("counterfactual_recovery_reentry_record_digest", "")
        ):
            blockers.append("v13_37_recovery_record_activation_digest_mismatch")
        if str(recovery_record.get("source_v13_1_closed_loop_receipt_record_digest", "")) != str(
            receipt_record.get("record_digest", "")
        ):
            blockers.append("v13_37_recovery_record_receipt_digest_mismatch")
        if not recovery_record.get("record_digest"):
            blockers.append("v13_37_recovery_record_digest_missing")

    if counterfactual_packet:
        if counterfactual_packet.get("recovery_status") != "counterfactual_recovery_probe_selected":
            blockers.append("v13_37_counterfactual_packet_status_invalid")
        if str(counterfactual_packet.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_37_counterfactual_packet_recovery_id_mismatch")
        if str(counterfactual_packet.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_37_counterfactual_packet_probe_mismatch")
        if int(counterfactual_packet.get("candidate_count", 0) or 0) != candidate_count:
            blockers.append("v13_37_counterfactual_packet_candidate_count_mismatch")
        ranked = counterfactual_packet.get("ranked_candidates", [])
        if not isinstance(ranked, list) or not any(
            isinstance(item, Mapping) and str(item.get("probe_type", "")) == selected_probe for item in ranked
        ):
            blockers.append("v13_37_selected_probe_not_in_ranked_candidates")
        _require_boundary(
            counterfactual_packet,
            (
                "counterfactual_recovery_only",
                "alternative_path_probe_only",
                "rollback_path_not_reinforced",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "license_gated_reentry",
                "fail_closed_on_boundary_loss",
            ),
            "v13_37_counterfactual_packet",
            blockers,
        )

    if receipt_record:
        if receipt_record.get("record_type") != "physical_quantum_qi_closed_loop_reentry_receipt":
            blockers.append("v13_1_receipt_record_type_invalid")
        if receipt_record.get("closed_loop_reentry_status") != "closed_loop_reentry_probe_opened":
            blockers.append("v13_1_receipt_status_not_probe")
        if receipt_record.get("reentry_weighting_action") != "open_probe_potential":
            blockers.append("v13_1_receipt_action_not_probe")
        if _normalize_weighting(_m(receipt_record.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_1_receipt_probe_weighting_invalid")

    prior_activations = _records(activation_ledger_path)
    if recovery_id and any(str(record.get("recovery_id", "")) == recovery_id for record in prior_activations):
        blockers.append("counterfactual_cycle_handoff_recovery_replay")

    bridge_invoked = handoff_invoked = annotated_seed_written = activation_ledger_appended = False
    bridge: dict[str, Any] = {}
    handoff: dict[str, Any] = {}
    ready_state: dict[str, Any] = {}
    handoff_packet: dict[str, Any] = {}
    cycle_gate_input: dict[str, Any] = {}
    seed: dict[str, Any] = {}
    handoff_record: dict[str, Any] = {}
    annotated_seed: dict[str, Any] = {}

    if not blockers:
        bridge = build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge(
            runtime_context={
                "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge": True,
                "runtime_root": str(root),
            },
            v13_1_to_v13_2_cycle_handoff_bridge_license=dict(_m(lic.get("v13_14_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_READY":
            blockers.append("v13_14_bridge_not_ready")
        if (
            bridge.get("expected_v13_2_handoff_status") != "candidate_weighting_cycle_handoff_probe"
            or bridge.get("expected_v13_2_cycle_gate_decision") != "hold_candidate"
            or bridge.get("expected_v13_2_admissible_candidate_seed_mode") != "probe_candidate_seed"
            or bridge.get("probe_potential_required") is not True
            or int(bridge.get("path_weight_delta", 0) or 0) != 0
            or bridge.get("barrier_potential_required") is not False
        ):
            blockers.append("v13_14_counterfactual_probe_expectation_mismatch")

    if bridge_invoked and not blockers:
        handoff = build_physical_quantum_qi_candidate_weighting_cycle_handoff(
            runtime_context={
                "physical_quantum_qi_candidate_weighting_cycle_handoff_enabled": True,
                "apply_physical_quantum_qi_candidate_weighting_cycle_handoff": True,
                "runtime_root": str(root),
            },
            candidate_weighting_cycle_handoff_license=dict(_m(lic.get("v13_2_handoff_license"))),
        ).to_dict()
        handoff_invoked = True
        if handoff.get("status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY":
            blockers.append("v13_2_handoff_not_ready")
        if (
            handoff.get("handoff_status") != "candidate_weighting_cycle_handoff_probe"
            or handoff.get("cycle_gate_decision") != "hold_candidate"
            or handoff.get("admissible_candidate_seed_mode") != "probe_candidate_seed"
        ):
            blockers.append("v13_2_counterfactual_probe_handoff_mismatch")

    if handoff_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_2_candidate_weighting_cycle_handoff_ready_state.json")
        handoff_packet = _read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json")
        cycle_gate_input = _read_json(root / "physical_quantum_qi_next_cycle_gate_input.json")
        seed = _read_json(root / "physical_quantum_qi_admissible_candidate_set_seed.json")
        handoff_record = _latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")
        if not ready_state.get("cycle_handoff_ready_state_digest"):
            blockers.append("v13_14_ready_state_digest_missing")
        if not handoff_packet.get("candidate_weighting_cycle_handoff_digest"):
            blockers.append("v13_2_handoff_packet_digest_missing")
        if not cycle_gate_input.get("cycle_gate_input_digest"):
            blockers.append("v13_2_cycle_gate_input_digest_missing")
        if not seed.get("admissible_candidate_set_seed_digest"):
            blockers.append("v13_2_seed_digest_missing")
        if not handoff_record.get("record_digest"):
            blockers.append("v13_2_handoff_record_digest_missing")
        source_digests = _m(handoff_packet.get("source_digests"))
        if str(source_digests.get("closed_loop_reentry_receipt", "")) != str(receipt_record.get("record_digest", "")):
            blockers.append("v13_2_handoff_packet_receipt_digest_mismatch")
        handoff_digest = str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", ""))
        if str(cycle_gate_input.get("source_candidate_weighting_cycle_handoff_digest", "")) != handoff_digest:
            blockers.append("v13_2_cycle_gate_input_source_digest_mismatch")
        if str(seed.get("source_candidate_weighting_cycle_handoff_digest", "")) != handoff_digest:
            blockers.append("v13_2_seed_source_digest_mismatch")
        if str(handoff_record.get("source_candidate_weighting_cycle_handoff_digest", "")) != handoff_digest:
            blockers.append("v13_2_handoff_record_packet_digest_mismatch")
        if str(handoff_record.get("source_closed_loop_reentry_receipt_digest", "")) != str(
            receipt_record.get("record_digest", "")
        ):
            blockers.append("v13_2_handoff_record_receipt_digest_mismatch")
        if (
            cycle_gate_input.get("cycle_gate_decision") != "hold_candidate"
            or seed.get("admissible_candidate_seed_mode") != "probe_candidate_seed"
            or _normalize_weighting(_m(seed.get("candidate_weighting"))) != EXPECTED_WEIGHTING
        ):
            blockers.append("v13_2_counterfactual_seed_semantics_mismatch")

    activation_status = (
        "counterfactual_cycle_handoff_completed"
        if bridge_invoked and handoff_invoked and not blockers
        else "counterfactual_cycle_handoff_blocked"
    )

    if bridge_invoked or handoff_invoked:
        selected_candidate = next(
            (
                dict(item)
                for item in counterfactual_packet.get("ranked_candidates", [])
                if isinstance(item, Mapping) and str(item.get("probe_type", "")) == selected_probe
            ),
            {},
        )
        annotated_seed = {
            "version": "physical_quantum_qi_v13_38_counterfactual_candidate_seed",
            "counterfactual_candidate_seed_ready": activation_status == "counterfactual_cycle_handoff_completed",
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "selected_probe_candidate": selected_candidate,
            "candidate_count": candidate_count,
            "handoff_status": "candidate_weighting_cycle_handoff_probe",
            "cycle_gate_decision": "hold_candidate",
            "admissible_candidate_seed_mode": "probe_candidate_seed",
            "candidate_weighting": dict(EXPECTED_WEIGHTING),
            "source_digests": {
                "v13_37_activation_record": str(source.get("counterfactual_recovery_reentry_record_digest", "")),
                "v13_37_recovery_record": str(recovery_record.get("record_digest", "")),
                "v13_37_counterfactual_packet": str(counterfactual_packet.get("counterfactual_recovery_packet_digest", "")),
                "v13_1_closed_loop_receipt": str(receipt_record.get("record_digest", "")),
                "v13_14_ready_state": str(ready_state.get("cycle_handoff_ready_state_digest", "")),
                "v13_2_handoff_packet": str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")),
                "v13_2_cycle_gate_input": str(cycle_gate_input.get("cycle_gate_input_digest", "")),
                "v13_2_candidate_seed": str(seed.get("admissible_candidate_set_seed_digest", "")),
                "v13_2_handoff_record": str(handoff_record.get("record_digest", "")),
            },
            "boundary": {
                "counterfactual_candidate_seed_only": True,
                "alternative_path_probe_only": True,
                "failed_path_not_reinforced": True,
                "rollback_consumed_once": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "requires_future_gate_decision": True,
                "non_markov_feedback_preserved": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        annotated_seed["counterfactual_candidate_seed_digest"] = _sha(annotated_seed)
        if lic.get("annotated_seed_write_allowed") is True:
            _write_json(annotated_seed_path, annotated_seed)
            annotated_seed_written = True

        activation_record = {
            "version": "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record",
            "activation_status": activation_status,
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "candidate_count": candidate_count,
            "handoff_status": str(handoff.get("handoff_status", "candidate_weighting_cycle_handoff_probe")),
            "cycle_gate_decision": str(handoff.get("cycle_gate_decision", "hold_candidate")),
            "admissible_candidate_seed_mode": str(handoff.get("admissible_candidate_seed_mode", "probe_candidate_seed")),
            "source_v13_37_activation_record_digest": str(source.get("counterfactual_recovery_reentry_record_digest", "")),
            "source_v13_37_recovery_record_digest": str(recovery_record.get("record_digest", "")),
            "source_v13_1_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "source_v13_14_ready_state_digest": str(ready_state.get("cycle_handoff_ready_state_digest", "")),
            "source_v13_2_handoff_packet_digest": str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")),
            "source_v13_2_candidate_seed_digest": str(seed.get("admissible_candidate_set_seed_digest", "")),
            "source_v13_2_handoff_record_digest": str(handoff_record.get("record_digest", "")),
            "source_v13_38_counterfactual_candidate_seed_digest": str(
                annotated_seed.get("counterfactual_candidate_seed_digest", "")
            ),
            "boundary": {
                "rollback_recovery_to_cycle_handoff": True,
                "counterfactual_probe_identity_preserved": True,
                "failed_path_not_reinforced": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "license_gated_cycle_handoff": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_handoff_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        activation_record["counterfactual_cycle_handoff_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

        if activation_status == "counterfactual_cycle_handoff_completed":
            ledger_record = {
                "version": "physical_quantum_qi_counterfactual_cycle_handoff_ledger_record_v13_38",
                "record_type": "physical_quantum_qi_counterfactual_cycle_handoff",
                "recovery_id": recovery_id,
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "activation_status": activation_status,
                "selected_probe_type": selected_probe,
                "handoff_status": "candidate_weighting_cycle_handoff_probe",
                "cycle_gate_decision": "hold_candidate",
                "admissible_candidate_seed_mode": "probe_candidate_seed",
                "source_activation_record_digest": activation_record[
                    "counterfactual_cycle_handoff_record_digest"
                ],
                "source_v13_37_recovery_record_digest": str(recovery_record.get("record_digest", "")),
                "source_v13_2_handoff_record_digest": str(handoff_record.get("record_digest", "")),
                "source_counterfactual_candidate_seed_digest": str(
                    annotated_seed.get("counterfactual_candidate_seed_digest", "")
                ),
                "prev_record_digest": str(prior_activations[-1].get("record_digest", "GENESIS")) if prior_activations else "GENESIS",
                "boundary": {
                    "counterfactual_cycle_handoff_receipt_only": True,
                    "recovery_consumed_once": True,
                    "alternative_probe_traceable": True,
                    "v13_2_handoff_traceable": True,
                    "replay_protected": True,
                    "candidate_weighting_not_truth": True,
                    "non_markov_feedback_preserved": True,
                },
                "epoch": int(time.time()),
            }
            ledger_record["record_digest"] = _sha(ledger_record)
            if lic.get("activation_ledger_append_allowed") is True:
                _append_jsonl(activation_ledger_path, ledger_record)
                activation_ledger_appended = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_READY"
        if activation_status == "counterfactual_cycle_handoff_completed"
        and annotated_seed_written
        and activation_ledger_appended
        else "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_38_counterfactual_cycle_handoff",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-38-counterfactual-cycle-handoff-"
        + _sha({"recovery_id": recovery_id, "probe": selected_probe, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "selected_probe_type": selected_probe,
        "candidate_count": candidate_count,
        "handoff_status": str(handoff.get("handoff_status", "candidate_weighting_cycle_handoff_probe")),
        "cycle_gate_decision": str(handoff.get("cycle_gate_decision", "hold_candidate")),
        "admissible_candidate_seed_mode": str(handoff.get("admissible_candidate_seed_mode", "probe_candidate_seed")),
        "v13_14_bridge_invoked": bridge_invoked,
        "v13_2_handoff_invoked": handoff_invoked,
        "annotated_seed_written": annotated_seed_written,
        "activation_ledger_appended": activation_ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_38CounterfactualCycleHandoffResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, recovery_id, rollback_id,
        mutation_id, selected_probe, candidate_count, receipt["handoff_status"], receipt["cycle_gate_decision"],
        receipt["admissible_candidate_seed_mode"], bridge_invoked, handoff_invoked, annotated_seed_written,
        activation_ledger_appended, str(annotated_seed_path), str(activation_record_path), str(activation_ledger_path),
        str(receipt_path), str(audit_path), blockers, warnings,
    )

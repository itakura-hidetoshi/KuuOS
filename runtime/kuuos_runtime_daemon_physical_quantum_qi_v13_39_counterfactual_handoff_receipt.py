#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3 import (
    build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15 import (
    build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge,
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
class PhysicalQuantumQiV13_39CounterfactualHandoffReceiptResult:
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
    v13_15_bridge_invoked: bool
    v13_3_receipt_ledger_invoked: bool
    annotated_receipt_written: bool
    activation_ledger_appended: bool
    v13_3_receipt_record_digest: str
    annotated_receipt_path: str
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


def _valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == _sha(_without(value, field))


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
    values: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            values.append(value)
    return values


def _latest(path: pathlib.Path) -> dict[str, Any]:
    values = _records(path)
    return values[-1] if values else {}


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


def _require_boundary(
    value: Mapping[str, Any], names: tuple[str, ...], prefix: str, blockers: list[str]
) -> None:
    boundary = _m(value.get("boundary"))
    for name in names:
        if boundary.get(name) is not True:
            blockers.append(f"{prefix}_boundary_{name}_missing")


def build_physical_quantum_qi_v13_39_counterfactual_handoff_receipt(
    *,
    runtime_context: Mapping[str, Any],
    v13_39_counterfactual_handoff_receipt_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_39CounterfactualHandoffReceiptResult:
    ctx = _m(runtime_context)
    lic = _m(v13_39_counterfactual_handoff_receipt_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_record.json"
    source_receipt_path = root / "physical_quantum_qi_v13_38_counterfactual_cycle_handoff_receipt.json"
    source_ledger_path = root / "physical_quantum_qi_counterfactual_cycle_handoff_ledger.jsonl"
    annotated_seed_path = root / "physical_quantum_qi_v13_38_counterfactual_candidate_seed.json"
    handoff_packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
    gate_input_path = root / "physical_quantum_qi_next_cycle_gate_input.json"
    seed_path = root / "physical_quantum_qi_admissible_candidate_set_seed.json"
    handoff_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl"
    annotated_receipt_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record.json"
    activation_record_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record.json"
    activation_ledger_path = root / "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_39_counterfactual_handoff_receipt_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_39_counterfactual_handoff_receipt_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_39_counterfactual_handoff_receipt") is not True:
        blockers.append("apply_physical_quantum_qi_v13_39_counterfactual_handoff_receipt_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_39_counterfactual_handoff_receipt_license_not_ready")
    for flag in (
        "v13_38_activation_record_read_allowed",
        "v13_38_receipt_read_allowed",
        "v13_38_activation_ledger_read_allowed",
        "v13_38_annotated_seed_read_allowed",
        "v13_2_handoff_packet_read_allowed",
        "v13_2_cycle_gate_input_read_allowed",
        "v13_2_candidate_seed_read_allowed",
        "v13_2_handoff_ledger_read_allowed",
        "v13_15_bridge_invoke_allowed",
        "v13_3_receipt_ledger_invoke_allowed",
        "annotated_receipt_write_allowed",
        "activation_record_write_allowed",
        "activation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    source_receipt = _read_json(source_receipt_path)
    source_ledger_record = _latest(source_ledger_path)
    annotated_seed = _read_json(annotated_seed_path)
    handoff_packet = _read_json(handoff_packet_path)
    gate_input = _read_json(gate_input_path)
    seed = _read_json(seed_path)
    handoff_record = _latest(handoff_ledger_path)

    for value, blocker in (
        (source, "v13_38_activation_record_missing_or_invalid"),
        (source_receipt, "v13_38_receipt_missing_or_invalid"),
        (source_ledger_record, "v13_38_activation_ledger_record_missing_or_invalid"),
        (annotated_seed, "v13_38_annotated_seed_missing_or_invalid"),
        (handoff_packet, "v13_2_handoff_packet_missing_or_invalid"),
        (gate_input, "v13_2_cycle_gate_input_missing_or_invalid"),
        (seed, "v13_2_candidate_seed_missing_or_invalid"),
        (handoff_record, "v13_2_handoff_record_missing_or_invalid"),
    ):
        if not value:
            blockers.append(blocker)

    recovery_id = str(source.get("recovery_id", ""))
    rollback_id = str(source.get("rollback_id", ""))
    mutation_id = str(source.get("mutation_id", ""))
    selected_probe = str(source.get("selected_probe_type", ""))
    try:
        candidate_count = int(source.get("candidate_count", 0) or 0)
    except (TypeError, ValueError):
        candidate_count = 0

    if source:
        if source.get("activation_status") != "counterfactual_cycle_handoff_completed":
            blockers.append("v13_38_activation_not_completed")
        if source.get("handoff_status") != "candidate_weighting_cycle_handoff_probe":
            blockers.append("v13_38_handoff_status_not_probe")
        if source.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_38_cycle_gate_decision_not_hold")
        if source.get("admissible_candidate_seed_mode") != "probe_candidate_seed":
            blockers.append("v13_38_candidate_seed_mode_not_probe")
        if not recovery_id or not rollback_id or not mutation_id or not selected_probe or candidate_count <= 0:
            blockers.append("v13_38_counterfactual_identity_invalid")
        if not _valid_digest(source, "counterfactual_cycle_handoff_record_digest"):
            blockers.append("v13_38_activation_record_digest_invalid")
        _require_boundary(
            source,
            (
                "rollback_recovery_to_cycle_handoff",
                "counterfactual_probe_identity_preserved",
                "failed_path_not_reinforced",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "license_gated_cycle_handoff",
                "non_markov_feedback_preserved",
                "runtime_local_handoff_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_38_activation",
            blockers,
        )

    if source_receipt:
        if source_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_38_COUNTERFACTUAL_CYCLE_HANDOFF_READY":
            blockers.append("v13_38_receipt_not_ready")
        if source_receipt.get("activation_status") != "counterfactual_cycle_handoff_completed":
            blockers.append("v13_38_receipt_activation_not_completed")
        if str(source_receipt.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_38_receipt_recovery_id_mismatch")
        if str(source_receipt.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_38_receipt_probe_mismatch")
        if source_receipt.get("annotated_seed_written") is not True or source_receipt.get("activation_ledger_appended") is not True:
            blockers.append("v13_38_receipt_outputs_not_complete")

    if source_ledger_record:
        if source_ledger_record.get("record_type") != "physical_quantum_qi_counterfactual_cycle_handoff":
            blockers.append("v13_38_activation_ledger_record_type_invalid")
        if source_ledger_record.get("activation_status") != "counterfactual_cycle_handoff_completed":
            blockers.append("v13_38_activation_ledger_status_invalid")
        if str(source_ledger_record.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_38_activation_ledger_recovery_id_mismatch")
        if str(source_ledger_record.get("source_activation_record_digest", "")) != str(
            source.get("counterfactual_cycle_handoff_record_digest", "")
        ):
            blockers.append("v13_38_activation_ledger_source_digest_mismatch")
        if not _valid_digest(source_ledger_record, "record_digest"):
            blockers.append("v13_38_activation_ledger_record_digest_invalid")

    if annotated_seed:
        if annotated_seed.get("counterfactual_candidate_seed_ready") is not True:
            blockers.append("v13_38_annotated_seed_not_ready")
        if str(annotated_seed.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_38_annotated_seed_recovery_id_mismatch")
        if str(annotated_seed.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_38_annotated_seed_probe_mismatch")
        if int(annotated_seed.get("candidate_count", 0) or 0) != candidate_count:
            blockers.append("v13_38_annotated_seed_candidate_count_mismatch")
        selected_candidate = _m(annotated_seed.get("selected_probe_candidate"))
        if str(selected_candidate.get("probe_type", "")) != selected_probe:
            blockers.append("v13_38_annotated_seed_selected_candidate_mismatch")
        if _normalize_weighting(_m(annotated_seed.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_38_annotated_seed_weighting_invalid")
        if not _valid_digest(annotated_seed, "counterfactual_candidate_seed_digest"):
            blockers.append("v13_38_annotated_seed_digest_invalid")
        source_digests = _m(annotated_seed.get("source_digests"))
        digest_expectations = {
            "v13_38_activation": str(source.get("counterfactual_cycle_handoff_record_digest", "")),
            "v13_2_handoff_packet": str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")),
            "v13_2_cycle_gate_input": str(gate_input.get("cycle_gate_input_digest", "")),
            "v13_2_candidate_seed": str(seed.get("admissible_candidate_set_seed_digest", "")),
            "v13_2_handoff_record": str(handoff_record.get("record_digest", "")),
        }
        if str(source_digests.get("v13_37_activation_record", "")) == "":
            blockers.append("v13_38_annotated_seed_v13_37_source_missing")
        for name, expected in digest_expectations.items():
            key = "v13_38_activation_record" if name == "v13_38_activation" else name
            if name == "v13_38_activation":
                if str(source.get("source_v13_38_counterfactual_candidate_seed_digest", "")) != str(
                    annotated_seed.get("counterfactual_candidate_seed_digest", "")
                ):
                    blockers.append("v13_38_activation_annotated_seed_digest_mismatch")
                continue
            if str(source_digests.get(key, "")) != expected:
                blockers.append(f"v13_38_annotated_seed_{name}_digest_mismatch")
        _require_boundary(
            annotated_seed,
            (
                "counterfactual_candidate_seed_only",
                "alternative_path_probe_only",
                "failed_path_not_reinforced",
                "rollback_consumed_once",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "requires_future_gate_decision",
                "non_markov_feedback_preserved",
                "fail_closed_on_boundary_loss",
            ),
            "v13_38_annotated_seed",
            blockers,
        )

    if handoff_packet:
        if handoff_packet.get("handoff_status") != "candidate_weighting_cycle_handoff_probe":
            blockers.append("v13_2_handoff_packet_status_not_probe")
        if handoff_packet.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_2_handoff_packet_decision_not_hold")
        if handoff_packet.get("admissible_candidate_seed_mode") != "probe_candidate_seed":
            blockers.append("v13_2_handoff_packet_seed_mode_not_probe")
        if _normalize_weighting(_m(handoff_packet.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_2_handoff_packet_weighting_invalid")
        if not _valid_digest(handoff_packet, "candidate_weighting_cycle_handoff_digest"):
            blockers.append("v13_2_handoff_packet_digest_invalid")
        if str(source.get("source_v13_2_handoff_packet_digest", "")) != str(
            handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")
        ):
            blockers.append("v13_38_source_handoff_packet_digest_mismatch")

    if gate_input:
        if gate_input.get("cycle_gate_input_ready") is not True or gate_input.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_2_cycle_gate_input_semantics_invalid")
        if _normalize_weighting(_m(gate_input.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_2_cycle_gate_input_weighting_invalid")
        if not _valid_digest(gate_input, "cycle_gate_input_digest"):
            blockers.append("v13_2_cycle_gate_input_digest_invalid")

    if seed:
        if seed.get("admissible_candidate_set_seed_ready") is not True or seed.get("admissible_candidate_seed_mode") != "probe_candidate_seed":
            blockers.append("v13_2_candidate_seed_semantics_invalid")
        if _normalize_weighting(_m(seed.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_2_candidate_seed_weighting_invalid")
        if not _valid_digest(seed, "admissible_candidate_set_seed_digest"):
            blockers.append("v13_2_candidate_seed_digest_invalid")
        if str(source.get("source_v13_2_candidate_seed_digest", "")) != str(seed.get("admissible_candidate_set_seed_digest", "")):
            blockers.append("v13_38_source_candidate_seed_digest_mismatch")

    if handoff_record:
        if handoff_record.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff":
            blockers.append("v13_2_handoff_record_type_invalid")
        if handoff_record.get("handoff_status") != "candidate_weighting_cycle_handoff_probe":
            blockers.append("v13_2_handoff_record_status_not_probe")
        if not _valid_digest(handoff_record, "record_digest"):
            blockers.append("v13_2_handoff_record_digest_invalid")
        if str(source.get("source_v13_2_handoff_record_digest", "")) != str(handoff_record.get("record_digest", "")):
            blockers.append("v13_38_source_handoff_record_digest_mismatch")

    prior_records = _records(activation_ledger_path)
    if recovery_id and any(str(record.get("recovery_id", "")) == recovery_id for record in prior_records):
        blockers.append("counterfactual_handoff_receipt_recovery_replay")

    bridge_invoked = ledger_invoked = annotated_receipt_written = activation_ledger_appended = False
    bridge: dict[str, Any] = {}
    ledger: dict[str, Any] = {}
    ready_state: dict[str, Any] = {}
    bridge_record: dict[str, Any] = {}
    v13_3_receipt: dict[str, Any] = {}
    v13_3_record: dict[str, Any] = {}
    annotated_receipt: dict[str, Any] = {}

    if not blockers:
        bridge = build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge(
            runtime_context={
                "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge": True,
                "runtime_root": str(root),
            },
            v13_2_to_v13_3_handoff_receipt_bridge_license=dict(_m(lic.get("v13_15_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_READY":
            blockers.append("v13_15_bridge_not_ready")
        if (
            bridge.get("handoff_status") != "candidate_weighting_cycle_handoff_probe"
            or bridge.get("cycle_gate_decision") != "hold_candidate"
            or bridge.get("admissible_candidate_seed_mode") != "probe_candidate_seed"
            or int(bridge.get("path_weight_delta", 0) or 0) != 0
            or bridge.get("probe_potential_required") is not True
            or bridge.get("barrier_potential_required") is not False
        ):
            blockers.append("v13_15_counterfactual_probe_output_mismatch")

    if bridge_invoked and not blockers:
        ledger = build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger": True,
                "runtime_root": str(root),
            },
            candidate_weighting_cycle_handoff_receipt_ledger_license=dict(
                _m(lic.get("v13_3_receipt_ledger_license"))
            ),
        ).to_dict()
        ledger_invoked = True
        if ledger.get("status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY":
            blockers.append("v13_3_receipt_ledger_not_ready")
        if (
            ledger.get("handoff_status") != "candidate_weighting_cycle_handoff_probe"
            or ledger.get("cycle_gate_decision") != "hold_candidate"
            or ledger.get("admissible_candidate_seed_mode") != "probe_candidate_seed"
            or ledger.get("ledger_appended") is not True
        ):
            blockers.append("v13_3_counterfactual_probe_receipt_output_mismatch")

    if ledger_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state.json")
        bridge_record = _latest(root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_ledger.jsonl")
        v13_3_receipt = _read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_receipt.json")
        v13_3_record = _latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl")
        if not _valid_digest(ready_state, "handoff_receipt_ready_state_digest"):
            blockers.append("v13_15_ready_state_digest_invalid")
        if not _valid_digest(bridge_record, "record_digest"):
            blockers.append("v13_15_bridge_record_digest_invalid")
        if v13_3_record.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt":
            blockers.append("v13_3_receipt_record_type_invalid")
        if not _valid_digest(v13_3_record, "record_digest"):
            blockers.append("v13_3_receipt_record_digest_invalid")
        if str(v13_3_receipt.get("record_digest", "")) != str(v13_3_record.get("record_digest", "")):
            blockers.append("v13_3_receipt_record_digest_mismatch")
        if (
            v13_3_record.get("handoff_status") != "candidate_weighting_cycle_handoff_probe"
            or v13_3_record.get("cycle_gate_decision") != "hold_candidate"
            or v13_3_record.get("admissible_candidate_seed_mode") != "probe_candidate_seed"
            or _normalize_weighting(_m(v13_3_record.get("candidate_weighting"))) != EXPECTED_WEIGHTING
        ):
            blockers.append("v13_3_counterfactual_probe_receipt_semantics_invalid")
        if str(v13_3_record.get("source_candidate_weighting_cycle_handoff_digest", "")) != str(
            handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")
        ):
            blockers.append("v13_3_receipt_handoff_packet_digest_mismatch")

    activation_status = (
        "counterfactual_handoff_receipt_completed"
        if bridge_invoked and ledger_invoked and not blockers
        else "counterfactual_handoff_receipt_blocked"
    )

    if bridge_invoked or ledger_invoked:
        annotated_receipt = {
            "version": "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record",
            "record_type": "physical_quantum_qi_counterfactual_handoff_receipt",
            "receipt_status": (
                "counterfactual_handoff_receipt_recorded"
                if activation_status == "counterfactual_handoff_receipt_completed"
                else "counterfactual_handoff_receipt_blocked"
            ),
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "selected_probe_candidate": dict(_m(annotated_seed.get("selected_probe_candidate"))),
            "candidate_count": candidate_count,
            "handoff_status": "candidate_weighting_cycle_handoff_probe",
            "cycle_gate_decision": "hold_candidate",
            "admissible_candidate_seed_mode": "probe_candidate_seed",
            "candidate_weighting": dict(EXPECTED_WEIGHTING),
            "source_digests": {
                "v13_38_activation_record": str(source.get("counterfactual_cycle_handoff_record_digest", "")),
                "v13_38_activation_ledger_record": str(source_ledger_record.get("record_digest", "")),
                "v13_38_annotated_seed": str(annotated_seed.get("counterfactual_candidate_seed_digest", "")),
                "v13_2_handoff_packet": str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")),
                "v13_2_handoff_record": str(handoff_record.get("record_digest", "")),
                "v13_15_ready_state": str(ready_state.get("handoff_receipt_ready_state_digest", "")),
                "v13_15_bridge_record": str(bridge_record.get("record_digest", "")),
                "v13_3_receipt_record": str(v13_3_record.get("record_digest", "")),
            },
            "boundary": {
                "counterfactual_handoff_receipt_only": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "probe_only_weighting_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "requires_future_gate_decision": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_receipt_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        annotated_receipt["counterfactual_handoff_receipt_record_digest"] = _sha(annotated_receipt)
        if lic.get("annotated_receipt_write_allowed") is True:
            _write_json(annotated_receipt_path, annotated_receipt)
            annotated_receipt_written = True

        activation_record = {
            "version": "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record",
            "activation_status": activation_status,
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "candidate_count": candidate_count,
            "handoff_status": "candidate_weighting_cycle_handoff_probe",
            "cycle_gate_decision": "hold_candidate",
            "admissible_candidate_seed_mode": "probe_candidate_seed",
            "source_v13_38_activation_record_digest": str(source.get("counterfactual_cycle_handoff_record_digest", "")),
            "source_v13_38_annotated_seed_digest": str(annotated_seed.get("counterfactual_candidate_seed_digest", "")),
            "source_v13_15_ready_state_digest": str(ready_state.get("handoff_receipt_ready_state_digest", "")),
            "source_v13_3_receipt_record_digest": str(v13_3_record.get("record_digest", "")),
            "source_v13_39_annotated_receipt_digest": str(
                annotated_receipt.get("counterfactual_handoff_receipt_record_digest", "")
            ),
            "boundary": {
                "two_stage_counterfactual_handoff_receipt_activation": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "license_gated_receipt_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_receipt_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        activation_record["counterfactual_handoff_receipt_activation_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

        if activation_status == "counterfactual_handoff_receipt_completed":
            activation_ledger_record = {
                "version": "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger_record_v13_39",
                "record_type": "physical_quantum_qi_counterfactual_handoff_receipt_activation",
                "recovery_id": recovery_id,
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "activation_status": activation_status,
                "selected_probe_type": selected_probe,
                "source_activation_record_digest": activation_record[
                    "counterfactual_handoff_receipt_activation_record_digest"
                ],
                "source_v13_38_activation_ledger_record_digest": str(source_ledger_record.get("record_digest", "")),
                "source_v13_3_receipt_record_digest": str(v13_3_record.get("record_digest", "")),
                "source_v13_39_annotated_receipt_digest": str(
                    annotated_receipt.get("counterfactual_handoff_receipt_record_digest", "")
                ),
                "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
                "boundary": {
                    "counterfactual_handoff_receipt_activation_only": True,
                    "recovery_consumed_once": True,
                    "counterfactual_probe_traceable": True,
                    "generic_v13_3_receipt_traceable": True,
                    "replay_protected": True,
                    "candidate_weighting_not_truth": True,
                    "non_markov_feedback_preserved": True,
                },
                "epoch": int(time.time()),
            }
            activation_ledger_record["record_digest"] = _sha(activation_ledger_record)
            if lic.get("activation_ledger_append_allowed") is True:
                _append_jsonl(activation_ledger_path, activation_ledger_record)
                activation_ledger_appended = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_READY"
        if activation_status == "counterfactual_handoff_receipt_completed"
        and annotated_receipt_written
        and activation_ledger_appended
        else "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_39_counterfactual_handoff_receipt",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-39-counterfactual-handoff-receipt-"
        + _sha({"recovery_id": recovery_id, "probe": selected_probe, "v13_3": v13_3_record.get("record_digest", ""), "blockers": blockers})[:16],
        "activation_status": activation_status,
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "selected_probe_type": selected_probe,
        "candidate_count": candidate_count,
        "handoff_status": "candidate_weighting_cycle_handoff_probe",
        "cycle_gate_decision": "hold_candidate",
        "admissible_candidate_seed_mode": "probe_candidate_seed",
        "v13_15_bridge_invoked": bridge_invoked,
        "v13_3_receipt_ledger_invoked": ledger_invoked,
        "annotated_receipt_written": annotated_receipt_written,
        "activation_ledger_appended": activation_ledger_appended,
        "v13_3_receipt_record_digest": str(v13_3_record.get("record_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_39CounterfactualHandoffReceiptResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, recovery_id,
        rollback_id, mutation_id, selected_probe, candidate_count, receipt["handoff_status"],
        receipt["cycle_gate_decision"], receipt["admissible_candidate_seed_mode"], bridge_invoked,
        ledger_invoked, annotated_receipt_written, activation_ledger_appended,
        receipt["v13_3_receipt_record_digest"], str(annotated_receipt_path), str(activation_record_path),
        str(activation_ledger_path), str(receipt_path), str(audit_path), blockers, warnings,
    )

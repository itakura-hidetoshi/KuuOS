#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 import (
    build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_v13_17 import (
    build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge,
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
EXPECTED_INTEGRATION = "cycle_gate_reentry_integration_hold"
EXPECTED_CYCLE_GATE = "integrated_cycle_gate_hold"
EXPECTED_CANDIDATE_SET = "integrated_admissible_candidate_set_probe"
EXPECTED_GENERIC_CANDIDATE_ID = "closed_loop_reentry_probe_candidate"


@dataclass(frozen=True)
class PhysicalQuantumQiV13_41CounterfactualIntegrationReceiptResult:
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
    admissible_candidate_count: int
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    v13_17_bridge_invoked: bool
    v13_5_receipt_ledger_invoked: bool
    annotated_receipt_written: bool
    activation_ledger_appended: bool
    v13_5_receipt_record_digest: str
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


def _integer(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _normalize_weighting(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path_weight_delta": _integer(value.get("path_weight_delta")),
        "probe_potential_required": value.get("probe_potential_required") is True,
        "barrier_potential_required": value.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": value.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": _integer(value.get("memory_feedback_weight")),
        "external_backaction_weight": _integer(value.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _integer(value.get("next_cycle_amplitude_delta")),
    }


def _require_boundary(
    value: Mapping[str, Any], names: tuple[str, ...], prefix: str, blockers: list[str]
) -> None:
    boundary = _m(value.get("boundary"))
    for name in names:
        if boundary.get(name) is not True:
            blockers.append(f"{prefix}_boundary_{name}_missing")


def _single_candidate(value: Mapping[str, Any]) -> dict[str, Any]:
    candidates = value.get("integrated_candidates", [])
    if isinstance(candidates, list) and len(candidates) == 1 and isinstance(candidates[0], Mapping):
        return dict(candidates[0])
    return {}


def _validate_generic_candidate(candidate: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    if not candidate:
        blockers.append(f"{prefix}_candidate_missing_or_invalid")
        return
    if candidate.get("candidate_id") != EXPECTED_GENERIC_CANDIDATE_ID:
        blockers.append(f"{prefix}_candidate_id_invalid")
    if candidate.get("candidate_mode") != "probe_candidate":
        blockers.append(f"{prefix}_candidate_mode_invalid")
    if candidate.get("admissibility_status") != "admissible_candidate_probe_required":
        blockers.append(f"{prefix}_candidate_admissibility_invalid")
    if _normalize_weighting(_m(candidate.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
        blockers.append(f"{prefix}_candidate_weighting_invalid")
    if not _valid_digest(candidate, "candidate_digest"):
        blockers.append(f"{prefix}_candidate_digest_invalid")


def build_physical_quantum_qi_v13_41_counterfactual_integration_receipt(
    *,
    runtime_context: Mapping[str, Any],
    v13_41_counterfactual_integration_receipt_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_41CounterfactualIntegrationReceiptResult:
    ctx = _m(runtime_context)
    lic = _m(v13_41_counterfactual_integration_receipt_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_record.json"
    source_receipt_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_receipt.json"
    source_ledger_path = root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl"
    annotated_candidate_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_candidate.json"
    integration_packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
    cycle_state_path = root / "physical_quantum_qi_integrated_cycle_gate_state.json"
    candidate_set_path = root / "physical_quantum_qi_integrated_admissible_candidate_set.json"
    integration_ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl"
    annotated_receipt_path = root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt_record.json"
    activation_record_path = root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt_activation_record.json"
    activation_ledger_path = root / "physical_quantum_qi_counterfactual_integration_receipt_activation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_41_counterfactual_integration_receipt_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_41_counterfactual_integration_receipt_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_41_counterfactual_integration_receipt_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_41_counterfactual_integration_receipt") is not True:
        blockers.append("apply_physical_quantum_qi_v13_41_counterfactual_integration_receipt_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_41_COUNTERFACTUAL_INTEGRATION_RECEIPT_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_41_counterfactual_integration_receipt_license_not_ready")
    for flag in (
        "v13_40_activation_record_read_allowed",
        "v13_40_receipt_read_allowed",
        "v13_40_activation_ledger_read_allowed",
        "v13_40_annotated_candidate_read_allowed",
        "v13_4_integration_packet_read_allowed",
        "v13_4_cycle_gate_state_read_allowed",
        "v13_4_candidate_set_read_allowed",
        "v13_4_integration_ledger_read_allowed",
        "v13_17_bridge_invoke_allowed",
        "v13_5_receipt_ledger_invoke_allowed",
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
    annotated_candidate = _read_json(annotated_candidate_path)
    integration_packet = _read_json(integration_packet_path)
    cycle_state = _read_json(cycle_state_path)
    candidate_set = _read_json(candidate_set_path)
    integration_record = _latest(integration_ledger_path)

    for value, blocker in (
        (source, "v13_40_activation_record_missing_or_invalid"),
        (source_receipt, "v13_40_receipt_missing_or_invalid"),
        (source_ledger_record, "v13_40_activation_ledger_record_missing_or_invalid"),
        (annotated_candidate, "v13_40_annotated_candidate_missing_or_invalid"),
        (integration_packet, "v13_4_integration_packet_missing_or_invalid"),
        (cycle_state, "v13_4_cycle_state_missing_or_invalid"),
        (candidate_set, "v13_4_candidate_set_missing_or_invalid"),
        (integration_record, "v13_4_integration_record_missing_or_invalid"),
    ):
        if not value:
            blockers.append(blocker)

    recovery_id = str(source.get("recovery_id", ""))
    rollback_id = str(source.get("rollback_id", ""))
    mutation_id = str(source.get("mutation_id", ""))
    selected_probe = str(source.get("selected_probe_type", ""))
    candidate_count = _integer(source.get("candidate_count"))

    if source:
        if source.get("activation_status") != "counterfactual_integration_activation_completed":
            blockers.append("v13_40_activation_not_completed")
        if source.get("integration_status") != EXPECTED_INTEGRATION:
            blockers.append("v13_40_integration_status_not_hold")
        if source.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_40_cycle_gate_status_not_hold")
        if source.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_40_candidate_set_status_not_probe")
        if not recovery_id or not rollback_id or not mutation_id or not selected_probe or candidate_count <= 0:
            blockers.append("v13_40_counterfactual_identity_invalid")
        if not _valid_digest(source, "counterfactual_integration_activation_record_digest"):
            blockers.append("v13_40_activation_record_digest_invalid")
        if str(source.get("source_v13_40_annotated_candidate_digest", "")) != str(
            annotated_candidate.get("counterfactual_integration_candidate_digest", "")
        ):
            blockers.append("v13_40_annotated_candidate_digest_mismatch")
        if str(source.get("source_v13_4_integration_packet_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_40_integration_packet_digest_mismatch")
        if str(source.get("source_v13_4_integration_record_digest", "")) != str(
            integration_record.get("record_digest", "")
        ):
            blockers.append("v13_40_integration_record_digest_mismatch")
        _require_boundary(
            source,
            (
                "two_stage_counterfactual_integration_activation",
                "counterfactual_probe_identity_preserved",
                "rollback_recovery_traceable",
                "failed_path_not_reinforced",
                "integrated_cycle_gate_hold_required",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "license_gated_integration",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "runtime_local_integration_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_40_activation",
            blockers,
        )

    if source_receipt:
        if source_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_READY":
            blockers.append("v13_40_receipt_not_ready")
        if source_receipt.get("activation_status") != "counterfactual_integration_activation_completed":
            blockers.append("v13_40_receipt_activation_not_completed")
        if str(source_receipt.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_40_receipt_recovery_id_mismatch")
        if str(source_receipt.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_40_receipt_probe_mismatch")
        if source_receipt.get("annotated_candidate_written") is not True or source_receipt.get("activation_ledger_appended") is not True:
            blockers.append("v13_40_receipt_outputs_not_complete")
        if str(source_receipt.get("v13_4_integration_record_digest", "")) != str(integration_record.get("record_digest", "")):
            blockers.append("v13_40_receipt_integration_record_digest_mismatch")

    if source_ledger_record:
        if source_ledger_record.get("record_type") != "physical_quantum_qi_counterfactual_integration_activation":
            blockers.append("v13_40_activation_ledger_record_type_invalid")
        if source_ledger_record.get("activation_status") != "counterfactual_integration_activation_completed":
            blockers.append("v13_40_activation_ledger_status_invalid")
        if str(source_ledger_record.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_40_activation_ledger_recovery_id_mismatch")
        if str(source_ledger_record.get("source_activation_record_digest", "")) != str(
            source.get("counterfactual_integration_activation_record_digest", "")
        ):
            blockers.append("v13_40_activation_ledger_source_digest_mismatch")
        if str(source_ledger_record.get("source_v13_40_annotated_candidate_digest", "")) != str(
            annotated_candidate.get("counterfactual_integration_candidate_digest", "")
        ):
            blockers.append("v13_40_activation_ledger_candidate_digest_mismatch")
        if str(source_ledger_record.get("source_v13_4_integration_record_digest", "")) != str(
            integration_record.get("record_digest", "")
        ):
            blockers.append("v13_40_activation_ledger_integration_digest_mismatch")
        if not _valid_digest(source_ledger_record, "record_digest"):
            blockers.append("v13_40_activation_ledger_record_digest_invalid")

    if annotated_candidate:
        if annotated_candidate.get("counterfactual_integration_candidate_ready") is not True:
            blockers.append("v13_40_annotated_candidate_not_ready")
        if str(annotated_candidate.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_40_annotated_candidate_recovery_id_mismatch")
        if str(annotated_candidate.get("rollback_id", "")) != rollback_id:
            blockers.append("v13_40_annotated_candidate_rollback_id_mismatch")
        if str(annotated_candidate.get("mutation_id", "")) != mutation_id:
            blockers.append("v13_40_annotated_candidate_mutation_id_mismatch")
        if str(annotated_candidate.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_40_annotated_candidate_probe_mismatch")
        if _integer(annotated_candidate.get("candidate_count")) != candidate_count:
            blockers.append("v13_40_annotated_candidate_count_mismatch")
        if annotated_candidate.get("integration_status") != EXPECTED_INTEGRATION:
            blockers.append("v13_40_annotated_candidate_integration_not_hold")
        if annotated_candidate.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_40_annotated_candidate_gate_not_hold")
        if annotated_candidate.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_40_annotated_candidate_set_not_probe")
        if str(_m(annotated_candidate.get("selected_probe_candidate")).get("probe_type", "")) != selected_probe:
            blockers.append("v13_40_selected_probe_candidate_mismatch")
        if _normalize_weighting(_m(annotated_candidate.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_40_annotated_candidate_weighting_invalid")
        if not _valid_digest(annotated_candidate, "counterfactual_integration_candidate_digest"):
            blockers.append("v13_40_annotated_candidate_digest_invalid")
        _validate_generic_candidate(
            _m(annotated_candidate.get("generic_integrated_candidate")),
            "v13_40_annotated",
            blockers,
        )
        _require_boundary(
            annotated_candidate,
            (
                "counterfactual_integration_candidate_only",
                "counterfactual_probe_identity_preserved",
                "rollback_recovery_traceable",
                "failed_path_not_reinforced",
                "probe_only_weighting_preserved",
                "integrated_cycle_gate_hold_required",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "requires_future_probe_evaluation",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "runtime_local_integration_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_40_annotated_candidate",
            blockers,
        )

    generic_candidate = _single_candidate(candidate_set)
    if integration_packet:
        if integration_packet.get("integration_status") != EXPECTED_INTEGRATION:
            blockers.append("v13_4_packet_integration_not_hold")
        if integration_packet.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_4_packet_gate_not_hold")
        if integration_packet.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_4_packet_set_not_probe")
        if _normalize_weighting(_m(integration_packet.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_4_packet_weighting_invalid")
        if not _valid_digest(integration_packet, "cycle_gate_reentry_integration_digest"):
            blockers.append("v13_4_packet_digest_invalid")
        _validate_generic_candidate(_single_candidate(integration_packet), "v13_4_packet", blockers)

    if cycle_state:
        if cycle_state.get("integrated_cycle_gate_ready") is not True:
            blockers.append("v13_4_cycle_state_not_ready")
        if cycle_state.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_4_cycle_state_not_hold")
        if cycle_state.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_4_cycle_decision_not_hold")
        if _normalize_weighting(_m(cycle_state.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_4_cycle_state_weighting_invalid")
        if str(cycle_state.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_4_cycle_state_packet_digest_mismatch")
        if not _valid_digest(cycle_state, "integrated_cycle_gate_state_digest"):
            blockers.append("v13_4_cycle_state_digest_invalid")

    if candidate_set:
        if candidate_set.get("integrated_admissible_candidate_set_ready") is not True:
            blockers.append("v13_4_candidate_set_not_ready")
        if candidate_set.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_4_candidate_set_not_probe")
        if _integer(candidate_set.get("admissible_candidate_count")) != 1:
            blockers.append("v13_4_candidate_set_count_invalid")
        if _normalize_weighting(_m(candidate_set.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_4_candidate_set_weighting_invalid")
        if str(candidate_set.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_4_candidate_set_packet_digest_mismatch")
        if not _valid_digest(candidate_set, "integrated_admissible_candidate_set_digest"):
            blockers.append("v13_4_candidate_set_digest_invalid")
        _validate_generic_candidate(generic_candidate, "v13_4_set", blockers)

    if annotated_candidate and generic_candidate:
        annotated_generic = _m(annotated_candidate.get("generic_integrated_candidate"))
        if str(annotated_generic.get("candidate_digest", "")) != str(generic_candidate.get("candidate_digest", "")):
            blockers.append("v13_40_annotated_generic_candidate_digest_mismatch")

    if integration_record:
        if integration_record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration":
            blockers.append("v13_4_integration_record_type_invalid")
        if integration_record.get("integration_status") != EXPECTED_INTEGRATION:
            blockers.append("v13_4_integration_record_not_hold")
        if integration_record.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_4_integration_record_gate_not_hold")
        if integration_record.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_4_integration_record_set_not_probe")
        if _integer(integration_record.get("admissible_candidate_count")) != 1:
            blockers.append("v13_4_integration_record_count_invalid")
        if str(integration_record.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_4_integration_record_packet_digest_mismatch")
        if not _valid_digest(integration_record, "record_digest"):
            blockers.append("v13_4_integration_record_digest_invalid")

    prior_records = _records(activation_ledger_path)
    if recovery_id and any(str(record.get("recovery_id", "")) == recovery_id for record in prior_records):
        blockers.append("counterfactual_integration_receipt_recovery_replay")

    bridge_invoked = ledger_invoked = annotated_receipt_written = activation_ledger_appended = False
    bridge: dict[str, Any] = {}
    ledger: dict[str, Any] = {}
    ready_state: dict[str, Any] = {}
    bridge_record: dict[str, Any] = {}
    generic_receipt_record: dict[str, Any] = {}
    generic_ledger_receipt: dict[str, Any] = {}
    annotated_receipt: dict[str, Any] = {}

    if not blockers:
        bridge = build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge(
            runtime_context={
                "physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge": True,
                "runtime_root": str(root),
            },
            v13_4_to_v13_5_integration_receipt_bridge_license=dict(_m(lic.get("v13_17_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_READY":
            blockers.append("v13_17_bridge_not_ready")
        if (
            bridge.get("integration_status") != EXPECTED_INTEGRATION
            or bridge.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or bridge.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or _integer(bridge.get("admissible_candidate_count")) != 1
            or bridge.get("receipt_ready_state_written") is not True
            or bridge.get("bridge_ledger_appended") is not True
        ):
            blockers.append("v13_17_counterfactual_receipt_output_mismatch")

    if bridge_invoked and not blockers:
        ledger = build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger": True,
                "runtime_root": str(root),
            },
            cycle_gate_reentry_integration_receipt_ledger_license=dict(_m(lic.get("v13_5_receipt_ledger_license"))),
        ).to_dict()
        ledger_invoked = True
        if ledger.get("status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY":
            blockers.append("v13_5_receipt_ledger_not_ready")
        if (
            ledger.get("integration_status") != EXPECTED_INTEGRATION
            or ledger.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or ledger.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or _integer(ledger.get("admissible_candidate_count")) != 1
            or ledger.get("ledger_appended") is not True
        ):
            blockers.append("v13_5_counterfactual_receipt_output_mismatch")

    if ledger_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_5_cycle_gate_reentry_integration_receipt_ready_state.json")
        bridge_record = _latest(root / "physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_ledger.jsonl")
        generic_receipt_record = _latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")
        generic_ledger_receipt = _read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_receipt.json")

        if not _valid_digest(ready_state, "integration_receipt_ready_state_digest"):
            blockers.append("v13_17_ready_state_digest_invalid")
        if not _valid_digest(bridge_record, "record_digest"):
            blockers.append("v13_17_bridge_record_digest_invalid")
        if not _valid_digest(generic_receipt_record, "record_digest"):
            blockers.append("v13_5_receipt_record_digest_invalid")
        if str(generic_ledger_receipt.get("record_digest", "")) != str(generic_receipt_record.get("record_digest", "")):
            blockers.append("v13_5_ledger_receipt_record_digest_mismatch")

        if (
            ready_state.get("integration_status") != EXPECTED_INTEGRATION
            or ready_state.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or ready_state.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or _integer(ready_state.get("admissible_candidate_count")) != 1
        ):
            blockers.append("v13_17_ready_state_semantics_invalid")
        if str(ready_state.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_17_ready_state_integration_digest_mismatch")
        if str(bridge_record.get("source_integration_receipt_ready_state_digest", "")) != str(
            ready_state.get("integration_receipt_ready_state_digest", "")
        ):
            blockers.append("v13_17_bridge_ready_state_digest_mismatch")
        if str(bridge_record.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_17_bridge_integration_digest_mismatch")

        if generic_receipt_record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration_receipt":
            blockers.append("v13_5_receipt_record_type_invalid")
        if generic_receipt_record.get("integration_status") != EXPECTED_INTEGRATION:
            blockers.append("v13_5_receipt_record_not_hold")
        if generic_receipt_record.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE:
            blockers.append("v13_5_receipt_record_gate_not_hold")
        if generic_receipt_record.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET:
            blockers.append("v13_5_receipt_record_set_not_probe")
        if _integer(generic_receipt_record.get("admissible_candidate_count")) != 1:
            blockers.append("v13_5_receipt_record_count_invalid")
        if _normalize_weighting(_m(generic_receipt_record.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_5_receipt_record_weighting_invalid")
        if str(generic_receipt_record.get("source_cycle_gate_reentry_integration_digest", "")) != str(
            integration_packet.get("cycle_gate_reentry_integration_digest", "")
        ):
            blockers.append("v13_5_receipt_record_integration_digest_mismatch")
        receipt_generic_candidate = _single_candidate(generic_receipt_record)
        _validate_generic_candidate(receipt_generic_candidate, "v13_5_receipt", blockers)
        if generic_candidate and str(receipt_generic_candidate.get("candidate_digest", "")) != str(
            generic_candidate.get("candidate_digest", "")
        ):
            blockers.append("v13_5_receipt_candidate_digest_mismatch")
        _require_boundary(
            generic_receipt_record,
            (
                "receipt_ledger_only",
                "cycle_gate_reentry_integration_receipt_only",
                "integrated_cycle_gate_state_traceable",
                "integrated_admissible_candidate_set_traceable",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "history_window_feedback_preserved",
                "memory_kernel_feedback_preserved",
                "external_backaction_visible",
                "candidate_weighting_not_truth",
                "integration_not_direct_execution",
                "replayable_receipt",
                "fail_closed_on_boundary_loss",
            ),
            "v13_5_receipt",
            blockers,
        )

    activation_status = (
        "counterfactual_integration_receipt_completed"
        if bridge_invoked and ledger_invoked and not blockers
        else "counterfactual_integration_receipt_blocked"
    )

    if bridge_invoked or ledger_invoked:
        receipt_generic_candidate = _single_candidate(generic_receipt_record)
        annotated_receipt = {
            "version": "physical_quantum_qi_v13_41_counterfactual_integration_receipt_record",
            "record_type": "physical_quantum_qi_counterfactual_integration_receipt",
            "receipt_status": (
                "counterfactual_integration_receipt_recorded"
                if activation_status == "counterfactual_integration_receipt_completed"
                else "counterfactual_integration_receipt_blocked"
            ),
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "selected_probe_candidate": dict(_m(annotated_candidate.get("selected_probe_candidate"))),
            "candidate_count": candidate_count,
            "admissible_candidate_count": 1,
            "integration_status": EXPECTED_INTEGRATION,
            "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
            "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
            "generic_integration_candidate": dict(receipt_generic_candidate),
            "candidate_weighting": dict(EXPECTED_WEIGHTING),
            "source_digests": {
                "v13_40_activation_record": str(source.get("counterfactual_integration_activation_record_digest", "")),
                "v13_40_activation_ledger_record": str(source_ledger_record.get("record_digest", "")),
                "v13_40_annotated_candidate": str(annotated_candidate.get("counterfactual_integration_candidate_digest", "")),
                "v13_4_integration_packet": str(integration_packet.get("cycle_gate_reentry_integration_digest", "")),
                "v13_4_cycle_state": str(cycle_state.get("integrated_cycle_gate_state_digest", "")),
                "v13_4_candidate_set": str(candidate_set.get("integrated_admissible_candidate_set_digest", "")),
                "v13_4_integration_record": str(integration_record.get("record_digest", "")),
                "v13_17_ready_state": str(ready_state.get("integration_receipt_ready_state_digest", "")),
                "v13_17_bridge_record": str(bridge_record.get("record_digest", "")),
                "v13_5_receipt_record": str(generic_receipt_record.get("record_digest", "")),
            },
            "boundary": {
                "counterfactual_integration_receipt_only": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "hold_only_integration_preserved": True,
                "probe_only_weighting_preserved": True,
                "generic_integration_receipt_traceable": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "requires_future_probe_evaluation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_receipt_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        annotated_receipt["counterfactual_integration_receipt_record_digest"] = _sha(annotated_receipt)
        if lic.get("annotated_receipt_write_allowed") is True:
            _write_json(annotated_receipt_path, annotated_receipt)
            annotated_receipt_written = True

        activation_record = {
            "version": "physical_quantum_qi_v13_41_counterfactual_integration_receipt_activation_record",
            "activation_status": activation_status,
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "candidate_count": candidate_count,
            "admissible_candidate_count": 1,
            "integration_status": EXPECTED_INTEGRATION,
            "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
            "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
            "source_v13_40_activation_record_digest": str(source.get("counterfactual_integration_activation_record_digest", "")),
            "source_v13_40_annotated_candidate_digest": str(annotated_candidate.get("counterfactual_integration_candidate_digest", "")),
            "source_v13_17_receipt_ready_state_digest": str(ready_state.get("integration_receipt_ready_state_digest", "")),
            "source_v13_17_bridge_record_digest": str(bridge_record.get("record_digest", "")),
            "source_v13_5_receipt_record_digest": str(generic_receipt_record.get("record_digest", "")),
            "source_v13_41_annotated_receipt_digest": str(annotated_receipt.get("counterfactual_integration_receipt_record_digest", "")),
            "boundary": {
                "two_stage_counterfactual_integration_receipt_activation": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "hold_only_integration_preserved": True,
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
        activation_record["counterfactual_integration_receipt_activation_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

        if activation_status == "counterfactual_integration_receipt_completed":
            ledger_record = {
                "version": "physical_quantum_qi_counterfactual_integration_receipt_activation_ledger_record_v13_41",
                "record_type": "physical_quantum_qi_counterfactual_integration_receipt_activation",
                "recovery_id": recovery_id,
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "activation_status": activation_status,
                "selected_probe_type": selected_probe,
                "integration_status": EXPECTED_INTEGRATION,
                "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
                "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
                "source_activation_record_digest": activation_record[
                    "counterfactual_integration_receipt_activation_record_digest"
                ],
                "source_v13_40_activation_ledger_record_digest": str(source_ledger_record.get("record_digest", "")),
                "source_v13_5_receipt_record_digest": str(generic_receipt_record.get("record_digest", "")),
                "source_v13_41_annotated_receipt_digest": str(
                    annotated_receipt.get("counterfactual_integration_receipt_record_digest", "")
                ),
                "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
                "boundary": {
                    "counterfactual_integration_receipt_activation_only": True,
                    "recovery_consumed_once": True,
                    "counterfactual_probe_traceable": True,
                    "generic_v13_5_receipt_traceable": True,
                    "hold_state_preserved": True,
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
        "PHYSICAL_QUANTUM_QI_V13_41_COUNTERFACTUAL_INTEGRATION_RECEIPT_READY"
        if activation_status == "counterfactual_integration_receipt_completed"
        and annotated_receipt_written
        and activation_ledger_appended
        else "PHYSICAL_QUANTUM_QI_V13_41_COUNTERFACTUAL_INTEGRATION_RECEIPT_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_41_counterfactual_integration_receipt",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-41-counterfactual-integration-receipt-"
        + _sha(
            {
                "recovery_id": recovery_id,
                "probe": selected_probe,
                "receipt": generic_receipt_record.get("record_digest", ""),
                "blockers": blockers,
            }
        )[:16],
        "activation_status": activation_status,
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "selected_probe_type": selected_probe,
        "candidate_count": candidate_count,
        "admissible_candidate_count": 1,
        "integration_status": EXPECTED_INTEGRATION,
        "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
        "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
        "v13_17_bridge_invoked": bridge_invoked,
        "v13_5_receipt_ledger_invoked": ledger_invoked,
        "annotated_receipt_written": annotated_receipt_written,
        "activation_ledger_appended": activation_ledger_appended,
        "v13_5_receipt_record_digest": str(generic_receipt_record.get("record_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_41CounterfactualIntegrationReceiptResult(
        receipt["version"],
        status,
        receipt["packet_id"],
        str(root),
        activation_status,
        recovery_id,
        rollback_id,
        mutation_id,
        selected_probe,
        candidate_count,
        1,
        receipt["integration_status"],
        receipt["integrated_cycle_gate_status"],
        receipt["integrated_admissible_candidate_set_status"],
        bridge_invoked,
        ledger_invoked,
        annotated_receipt_written,
        activation_ledger_appended,
        receipt["v13_5_receipt_record_digest"],
        str(annotated_receipt_path),
        str(activation_record_path),
        str(activation_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

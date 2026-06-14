#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4 import (
    build_physical_quantum_qi_cycle_gate_reentry_integration,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16 import (
    build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge,
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


@dataclass(frozen=True)
class PhysicalQuantumQiV13_40CounterfactualIntegrationActivationResult:
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
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    v13_16_bridge_invoked: bool
    v13_4_integration_invoked: bool
    annotated_candidate_written: bool
    activation_ledger_appended: bool
    v13_4_integration_record_digest: str
    annotated_candidate_path: str
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


def build_physical_quantum_qi_v13_40_counterfactual_integration_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_40_counterfactual_integration_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_40CounterfactualIntegrationActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_40_counterfactual_integration_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_activation_record.json"
    source_receipt_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt.json"
    source_ledger_path = root / "physical_quantum_qi_counterfactual_handoff_receipt_activation_ledger.jsonl"
    annotated_receipt_path = root / "physical_quantum_qi_v13_39_counterfactual_handoff_receipt_record.json"
    generic_receipt_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
    annotated_candidate_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_candidate.json"
    activation_record_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_record.json"
    activation_ledger_path = root / "physical_quantum_qi_counterfactual_integration_activation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_40_counterfactual_integration_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_40_counterfactual_integration_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_40_counterfactual_integration_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_40_counterfactual_integration_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_40_counterfactual_integration_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_40_counterfactual_integration_activation_license_not_ready")
    for flag in (
        "v13_39_activation_record_read_allowed",
        "v13_39_receipt_read_allowed",
        "v13_39_activation_ledger_read_allowed",
        "v13_39_annotated_receipt_read_allowed",
        "v13_3_receipt_ledger_read_allowed",
        "v13_16_bridge_invoke_allowed",
        "v13_4_integration_invoke_allowed",
        "annotated_candidate_write_allowed",
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
    annotated_receipt = _read_json(annotated_receipt_path)
    generic_receipt = _latest(generic_receipt_ledger_path)

    for value, blocker in (
        (source, "v13_39_activation_record_missing_or_invalid"),
        (source_receipt, "v13_39_receipt_missing_or_invalid"),
        (source_ledger_record, "v13_39_activation_ledger_record_missing_or_invalid"),
        (annotated_receipt, "v13_39_annotated_receipt_missing_or_invalid"),
        (generic_receipt, "v13_3_receipt_record_missing_or_invalid"),
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
        if source.get("activation_status") != "counterfactual_handoff_receipt_completed":
            blockers.append("v13_39_activation_not_completed")
        if source.get("handoff_status") != "candidate_weighting_cycle_handoff_probe":
            blockers.append("v13_39_handoff_status_not_probe")
        if source.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_39_cycle_gate_decision_not_hold")
        if source.get("admissible_candidate_seed_mode") != "probe_candidate_seed":
            blockers.append("v13_39_candidate_seed_mode_not_probe")
        if not recovery_id or not rollback_id or not mutation_id or not selected_probe or candidate_count <= 0:
            blockers.append("v13_39_counterfactual_identity_invalid")
        if not _valid_digest(source, "counterfactual_handoff_receipt_activation_record_digest"):
            blockers.append("v13_39_activation_record_digest_invalid")
        if str(source.get("source_v13_3_receipt_record_digest", "")) != str(generic_receipt.get("record_digest", "")):
            blockers.append("v13_39_generic_receipt_digest_mismatch")
        if str(source.get("source_v13_39_annotated_receipt_digest", "")) != str(
            annotated_receipt.get("counterfactual_handoff_receipt_record_digest", "")
        ):
            blockers.append("v13_39_annotated_receipt_digest_mismatch")
        _require_boundary(
            source,
            (
                "two_stage_counterfactual_handoff_receipt_activation",
                "counterfactual_probe_identity_preserved",
                "rollback_recovery_traceable",
                "failed_path_not_reinforced",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "license_gated_receipt_activation",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "runtime_local_receipt_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_39_activation",
            blockers,
        )

    if source_receipt:
        if source_receipt.get("status") != "PHYSICAL_QUANTUM_QI_V13_39_COUNTERFACTUAL_HANDOFF_RECEIPT_READY":
            blockers.append("v13_39_receipt_not_ready")
        if source_receipt.get("activation_status") != "counterfactual_handoff_receipt_completed":
            blockers.append("v13_39_receipt_activation_not_completed")
        if str(source_receipt.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_39_receipt_recovery_id_mismatch")
        if str(source_receipt.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_39_receipt_probe_mismatch")
        if str(source_receipt.get("v13_3_receipt_record_digest", "")) != str(generic_receipt.get("record_digest", "")):
            blockers.append("v13_39_receipt_generic_digest_mismatch")
        if source_receipt.get("annotated_receipt_written") is not True or source_receipt.get("activation_ledger_appended") is not True:
            blockers.append("v13_39_receipt_outputs_not_complete")

    if source_ledger_record:
        if source_ledger_record.get("record_type") != "physical_quantum_qi_counterfactual_handoff_receipt_activation":
            blockers.append("v13_39_activation_ledger_record_type_invalid")
        if source_ledger_record.get("activation_status") != "counterfactual_handoff_receipt_completed":
            blockers.append("v13_39_activation_ledger_status_invalid")
        if str(source_ledger_record.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_39_activation_ledger_recovery_id_mismatch")
        if str(source_ledger_record.get("source_activation_record_digest", "")) != str(
            source.get("counterfactual_handoff_receipt_activation_record_digest", "")
        ):
            blockers.append("v13_39_activation_ledger_source_digest_mismatch")
        if str(source_ledger_record.get("source_v13_3_receipt_record_digest", "")) != str(generic_receipt.get("record_digest", "")):
            blockers.append("v13_39_activation_ledger_generic_receipt_digest_mismatch")
        if not _valid_digest(source_ledger_record, "record_digest"):
            blockers.append("v13_39_activation_ledger_record_digest_invalid")

    if annotated_receipt:
        if annotated_receipt.get("record_type") != "physical_quantum_qi_counterfactual_handoff_receipt":
            blockers.append("v13_39_annotated_receipt_record_type_invalid")
        if annotated_receipt.get("receipt_status") != "counterfactual_handoff_receipt_recorded":
            blockers.append("v13_39_annotated_receipt_status_invalid")
        if str(annotated_receipt.get("recovery_id", "")) != recovery_id:
            blockers.append("v13_39_annotated_receipt_recovery_id_mismatch")
        if str(annotated_receipt.get("selected_probe_type", "")) != selected_probe:
            blockers.append("v13_39_annotated_receipt_probe_mismatch")
        if int(annotated_receipt.get("candidate_count", 0) or 0) != candidate_count:
            blockers.append("v13_39_annotated_receipt_candidate_count_mismatch")
        if str(_m(annotated_receipt.get("selected_probe_candidate")).get("probe_type", "")) != selected_probe:
            blockers.append("v13_39_selected_probe_candidate_mismatch")
        if _normalize_weighting(_m(annotated_receipt.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_39_annotated_receipt_weighting_invalid")
        if not _valid_digest(annotated_receipt, "counterfactual_handoff_receipt_record_digest"):
            blockers.append("v13_39_annotated_receipt_record_digest_invalid")
        if str(_m(annotated_receipt.get("source_digests")).get("v13_3_receipt_record", "")) != str(
            generic_receipt.get("record_digest", "")
        ):
            blockers.append("v13_39_annotated_receipt_generic_digest_mismatch")
        _require_boundary(
            annotated_receipt,
            (
                "counterfactual_handoff_receipt_only",
                "counterfactual_probe_identity_preserved",
                "rollback_recovery_traceable",
                "failed_path_not_reinforced",
                "probe_only_weighting_preserved",
                "candidate_weighting_not_truth",
                "not_direct_execution_authority",
                "not_world_update_authority",
                "requires_future_gate_decision",
                "uses_process_tensor_feedback",
                "non_markov_feedback_preserved",
                "runtime_local_receipt_only",
                "fail_closed_on_boundary_loss",
            ),
            "v13_39_annotated_receipt",
            blockers,
        )

    if generic_receipt:
        if generic_receipt.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt":
            blockers.append("v13_3_receipt_record_type_invalid")
        if generic_receipt.get("handoff_status") != "candidate_weighting_cycle_handoff_probe":
            blockers.append("v13_3_receipt_status_not_probe")
        if generic_receipt.get("cycle_gate_decision") != "hold_candidate":
            blockers.append("v13_3_receipt_decision_not_hold")
        if generic_receipt.get("admissible_candidate_seed_mode") != "probe_candidate_seed":
            blockers.append("v13_3_receipt_seed_mode_not_probe")
        if _normalize_weighting(_m(generic_receipt.get("candidate_weighting"))) != EXPECTED_WEIGHTING:
            blockers.append("v13_3_receipt_weighting_invalid")
        if not _valid_digest(generic_receipt, "record_digest"):
            blockers.append("v13_3_receipt_record_digest_invalid")

    prior_records = _records(activation_ledger_path)
    if recovery_id and any(str(record.get("recovery_id", "")) == recovery_id for record in prior_records):
        blockers.append("counterfactual_integration_recovery_replay")

    bridge_invoked = integration_invoked = annotated_candidate_written = activation_ledger_appended = False
    bridge: dict[str, Any] = {}
    integration: dict[str, Any] = {}
    ready_state: dict[str, Any] = {}
    bridge_record: dict[str, Any] = {}
    integration_packet: dict[str, Any] = {}
    cycle_state: dict[str, Any] = {}
    candidate_set: dict[str, Any] = {}
    integration_record: dict[str, Any] = {}
    annotated_candidate: dict[str, Any] = {}

    if not blockers:
        bridge = build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge(
            runtime_context={
                "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_3_to_v13_4_integration_bridge": True,
                "runtime_root": str(root),
            },
            v13_3_to_v13_4_integration_bridge_license=dict(_m(lic.get("v13_16_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_READY":
            blockers.append("v13_16_bridge_not_ready")
        if (
            bridge.get("expected_v13_4_integration_status") != EXPECTED_INTEGRATION
            or bridge.get("expected_v13_4_integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or bridge.get("expected_v13_4_integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or int(bridge.get("path_weight_delta", 0) or 0) != 0
            or bridge.get("probe_potential_required") is not True
            or bridge.get("barrier_potential_required") is not False
        ):
            blockers.append("v13_16_counterfactual_probe_output_mismatch")

    if bridge_invoked and not blockers:
        integration = build_physical_quantum_qi_cycle_gate_reentry_integration(
            runtime_context={
                "physical_quantum_qi_cycle_gate_reentry_integration_enabled": True,
                "apply_physical_quantum_qi_cycle_gate_reentry_integration": True,
                "runtime_root": str(root),
            },
            cycle_gate_reentry_integration_license=dict(_m(lic.get("v13_4_integration_license"))),
        ).to_dict()
        integration_invoked = True
        if integration.get("status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY":
            blockers.append("v13_4_integration_not_ready")
        if (
            integration.get("integration_status") != EXPECTED_INTEGRATION
            or integration.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or integration.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or integration.get("integration_packet_written") is not True
            or integration.get("integrated_cycle_gate_state_written") is not True
            or integration.get("integrated_admissible_candidate_set_written") is not True
            or integration.get("integration_ledger_appended") is not True
        ):
            blockers.append("v13_4_counterfactual_probe_integration_output_mismatch")

    if integration_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state.json")
        bridge_record = _latest(root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_ledger.jsonl")
        integration_packet = _read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json")
        cycle_state = _read_json(root / "physical_quantum_qi_integrated_cycle_gate_state.json")
        candidate_set = _read_json(root / "physical_quantum_qi_integrated_admissible_candidate_set.json")
        integration_record = _latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")

        if not _valid_digest(ready_state, "integration_ready_state_digest"):
            blockers.append("v13_16_ready_state_digest_invalid")
        if not _valid_digest(bridge_record, "record_digest"):
            blockers.append("v13_16_bridge_record_digest_invalid")
        if not _valid_digest(integration_packet, "cycle_gate_reentry_integration_digest"):
            blockers.append("v13_4_integration_packet_digest_invalid")
        if not _valid_digest(cycle_state, "integrated_cycle_gate_state_digest"):
            blockers.append("v13_4_cycle_state_digest_invalid")
        if not _valid_digest(candidate_set, "integrated_admissible_candidate_set_digest"):
            blockers.append("v13_4_candidate_set_digest_invalid")
        if not _valid_digest(integration_record, "record_digest"):
            blockers.append("v13_4_integration_record_digest_invalid")

        packet_digest = str(integration_packet.get("cycle_gate_reentry_integration_digest", ""))
        generic_receipt_digest = str(generic_receipt.get("record_digest", ""))
        if str(_m(integration_packet.get("source_digests")).get("candidate_weighting_cycle_handoff_receipt", "")) != generic_receipt_digest:
            blockers.append("v13_4_integration_packet_receipt_digest_mismatch")
        if str(cycle_state.get("source_cycle_gate_reentry_integration_digest", "")) != packet_digest:
            blockers.append("v13_4_cycle_state_packet_digest_mismatch")
        if str(candidate_set.get("source_cycle_gate_reentry_integration_digest", "")) != packet_digest:
            blockers.append("v13_4_candidate_set_packet_digest_mismatch")
        if str(integration_record.get("source_cycle_gate_reentry_integration_digest", "")) != packet_digest:
            blockers.append("v13_4_integration_record_packet_digest_mismatch")
        if str(integration_record.get("source_candidate_weighting_cycle_handoff_receipt_digest", "")) != generic_receipt_digest:
            blockers.append("v13_4_integration_record_receipt_digest_mismatch")

        if (
            integration_packet.get("integration_status") != EXPECTED_INTEGRATION
            or integration_packet.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or integration_packet.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or cycle_state.get("integrated_cycle_gate_status") != EXPECTED_CYCLE_GATE
            or cycle_state.get("cycle_gate_decision") != "hold_candidate"
            or candidate_set.get("integrated_admissible_candidate_set_status") != EXPECTED_CANDIDATE_SET
            or int(candidate_set.get("admissible_candidate_count", 0) or 0) != 1
            or int(integration_record.get("admissible_candidate_count", 0) or 0) != 1
        ):
            blockers.append("v13_4_counterfactual_integration_semantics_invalid")

        integrated_candidates = candidate_set.get("integrated_candidates", [])
        generic_candidate = integrated_candidates[0] if isinstance(integrated_candidates, list) and len(integrated_candidates) == 1 and isinstance(integrated_candidates[0], Mapping) else {}
        if (
            generic_candidate.get("candidate_id") != "closed_loop_reentry_probe_candidate"
            or generic_candidate.get("candidate_mode") != "probe_candidate"
            or generic_candidate.get("admissibility_status") != "admissible_candidate_probe_required"
            or _normalize_weighting(_m(generic_candidate.get("candidate_weighting"))) != EXPECTED_WEIGHTING
            or not _valid_digest(generic_candidate, "candidate_digest")
        ):
            blockers.append("v13_4_generic_probe_candidate_invalid")

    activation_status = (
        "counterfactual_integration_activation_completed"
        if bridge_invoked and integration_invoked and not blockers
        else "counterfactual_integration_activation_blocked"
    )

    if bridge_invoked or integration_invoked:
        integrated_candidates = candidate_set.get("integrated_candidates", [])
        generic_candidate = integrated_candidates[0] if isinstance(integrated_candidates, list) and len(integrated_candidates) == 1 and isinstance(integrated_candidates[0], Mapping) else {}
        annotated_candidate = {
            "version": "physical_quantum_qi_v13_40_counterfactual_integration_candidate",
            "counterfactual_integration_candidate_ready": activation_status == "counterfactual_integration_activation_completed",
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "selected_probe_candidate": dict(_m(annotated_receipt.get("selected_probe_candidate"))),
            "candidate_count": candidate_count,
            "integration_status": EXPECTED_INTEGRATION,
            "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
            "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
            "generic_integrated_candidate": dict(generic_candidate),
            "candidate_weighting": dict(EXPECTED_WEIGHTING),
            "source_digests": {
                "v13_39_activation_record": str(source.get("counterfactual_handoff_receipt_activation_record_digest", "")),
                "v13_39_activation_ledger_record": str(source_ledger_record.get("record_digest", "")),
                "v13_39_annotated_receipt": str(annotated_receipt.get("counterfactual_handoff_receipt_record_digest", "")),
                "v13_3_generic_receipt": str(generic_receipt.get("record_digest", "")),
                "v13_16_ready_state": str(ready_state.get("integration_ready_state_digest", "")),
                "v13_16_bridge_record": str(bridge_record.get("record_digest", "")),
                "v13_4_integration_packet": str(integration_packet.get("cycle_gate_reentry_integration_digest", "")),
                "v13_4_cycle_state": str(cycle_state.get("integrated_cycle_gate_state_digest", "")),
                "v13_4_candidate_set": str(candidate_set.get("integrated_admissible_candidate_set_digest", "")),
                "v13_4_integration_record": str(integration_record.get("record_digest", "")),
            },
            "boundary": {
                "counterfactual_integration_candidate_only": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "probe_only_weighting_preserved": True,
                "integrated_cycle_gate_hold_required": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "requires_future_probe_evaluation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_integration_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        annotated_candidate["counterfactual_integration_candidate_digest"] = _sha(annotated_candidate)
        if lic.get("annotated_candidate_write_allowed") is True:
            _write_json(annotated_candidate_path, annotated_candidate)
            annotated_candidate_written = True

        activation_record = {
            "version": "physical_quantum_qi_v13_40_counterfactual_integration_activation_record",
            "activation_status": activation_status,
            "recovery_id": recovery_id,
            "rollback_id": rollback_id,
            "mutation_id": mutation_id,
            "selected_probe_type": selected_probe,
            "candidate_count": candidate_count,
            "integration_status": EXPECTED_INTEGRATION,
            "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
            "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
            "source_v13_39_activation_record_digest": str(source.get("counterfactual_handoff_receipt_activation_record_digest", "")),
            "source_v13_39_annotated_receipt_digest": str(annotated_receipt.get("counterfactual_handoff_receipt_record_digest", "")),
            "source_v13_16_ready_state_digest": str(ready_state.get("integration_ready_state_digest", "")),
            "source_v13_4_integration_packet_digest": str(integration_packet.get("cycle_gate_reentry_integration_digest", "")),
            "source_v13_4_integration_record_digest": str(integration_record.get("record_digest", "")),
            "source_v13_40_annotated_candidate_digest": str(annotated_candidate.get("counterfactual_integration_candidate_digest", "")),
            "boundary": {
                "two_stage_counterfactual_integration_activation": True,
                "counterfactual_probe_identity_preserved": True,
                "rollback_recovery_traceable": True,
                "failed_path_not_reinforced": True,
                "integrated_cycle_gate_hold_required": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "not_world_update_authority": True,
                "license_gated_integration": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "runtime_local_integration_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        activation_record["counterfactual_integration_activation_record_digest"] = _sha(activation_record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

        if activation_status == "counterfactual_integration_activation_completed":
            ledger_record = {
                "version": "physical_quantum_qi_counterfactual_integration_activation_ledger_record_v13_40",
                "record_type": "physical_quantum_qi_counterfactual_integration_activation",
                "recovery_id": recovery_id,
                "rollback_id": rollback_id,
                "mutation_id": mutation_id,
                "activation_status": activation_status,
                "selected_probe_type": selected_probe,
                "integration_status": EXPECTED_INTEGRATION,
                "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
                "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
                "source_activation_record_digest": activation_record["counterfactual_integration_activation_record_digest"],
                "source_v13_39_activation_ledger_record_digest": str(source_ledger_record.get("record_digest", "")),
                "source_v13_4_integration_record_digest": str(integration_record.get("record_digest", "")),
                "source_v13_40_annotated_candidate_digest": str(annotated_candidate.get("counterfactual_integration_candidate_digest", "")),
                "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
                "boundary": {
                    "counterfactual_integration_activation_only": True,
                    "recovery_consumed_once": True,
                    "counterfactual_probe_traceable": True,
                    "generic_v13_4_integration_traceable": True,
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
        "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_READY"
        if activation_status == "counterfactual_integration_activation_completed"
        and annotated_candidate_written
        and activation_ledger_appended
        else "PHYSICAL_QUANTUM_QI_V13_40_COUNTERFACTUAL_INTEGRATION_ACTIVATION_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_40_counterfactual_integration_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-40-counterfactual-integration-activation-"
        + _sha({"recovery_id": recovery_id, "probe": selected_probe, "integration": integration_record.get("record_digest", ""), "blockers": blockers})[:16],
        "activation_status": activation_status,
        "recovery_id": recovery_id,
        "rollback_id": rollback_id,
        "mutation_id": mutation_id,
        "selected_probe_type": selected_probe,
        "candidate_count": candidate_count,
        "integration_status": EXPECTED_INTEGRATION,
        "integrated_cycle_gate_status": EXPECTED_CYCLE_GATE,
        "integrated_admissible_candidate_set_status": EXPECTED_CANDIDATE_SET,
        "v13_16_bridge_invoked": bridge_invoked,
        "v13_4_integration_invoked": integration_invoked,
        "annotated_candidate_written": annotated_candidate_written,
        "activation_ledger_appended": activation_ledger_appended,
        "v13_4_integration_record_digest": str(integration_record.get("record_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_40CounterfactualIntegrationActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, recovery_id,
        rollback_id, mutation_id, selected_probe, candidate_count, receipt["integration_status"],
        receipt["integrated_cycle_gate_status"], receipt["integrated_admissible_candidate_set_status"],
        bridge_invoked, integration_invoked, annotated_candidate_written, activation_ledger_appended,
        receipt["v13_4_integration_record_digest"], str(annotated_candidate_path), str(activation_record_path),
        str(activation_ledger_path), str(receipt_path), str(audit_path), blockers, warnings,
    )

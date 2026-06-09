#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


INTEGRATION_STATUSES = {
    "cycle_gate_reentry_integration_admit",
    "cycle_gate_reentry_integration_hold",
    "cycle_gate_reentry_integration_block",
}
EXPECTED_BY_INTEGRATION = {
    "cycle_gate_reentry_integration_admit": (
        "integrated_cycle_gate_admit",
        "integrated_admissible_candidate_set_admit",
        1,
    ),
    "cycle_gate_reentry_integration_hold": (
        "integrated_cycle_gate_hold",
        "integrated_admissible_candidate_set_probe",
        1,
    ),
    "cycle_gate_reentry_integration_block": (
        "integrated_cycle_gate_block",
        "integrated_admissible_candidate_set_block",
        0,
    ),
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "cycle_gate_reentry_integration_only",
    "candidate_weighting_cycle_handoff_receipt_required",
    "integrates_cycle_gate",
    "integrates_admissible_candidate_set",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "integration_not_direct_execution",
    "license_gated_integration",
    "fail_closed_on_boundary_loss",
)
REQUIRED_GATE_BOUNDARY_FLAGS = (
    "integrated_cycle_gate_state_only",
    "from_candidate_weighting_cycle_handoff_receipt",
    "uses_process_tensor_feedback",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_SET_BOUNDARY_FLAGS = (
    "integrated_admissible_candidate_set_only",
    "from_candidate_weighting_cycle_handoff_receipt",
    "uses_process_tensor_feedback",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiCycleGateReentryIntegrationReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    admissible_candidate_count: int
    ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        return "GENESIS"
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(value.get("record_digest", _sha(value)))


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _normalize_weighting(weighting: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path_weight_delta": _int(weighting.get("path_weight_delta")),
        "probe_potential_required": weighting.get("probe_potential_required") is True,
        "barrier_potential_required": weighting.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": weighting.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": _int(weighting.get("memory_feedback_weight")),
        "external_backaction_weight": _int(weighting.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _int(weighting.get("next_cycle_amplitude_delta")),
    }


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_weighting(integration_status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if integration_status == "cycle_gate_reentry_integration_admit":
        if norm["path_weight_delta"] <= 0:
            blockers.append("integration_receipt_admit_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_receipt_admit_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("integration_receipt_admit_missing_process_tensor_effect_weight")
    elif integration_status == "cycle_gate_reentry_integration_hold":
        if norm["path_weight_delta"] != 0:
            blockers.append("integration_receipt_hold_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("integration_receipt_hold_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_receipt_hold_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("integration_receipt_hold_with_effect_weight")
    elif integration_status == "cycle_gate_reentry_integration_block":
        if norm["path_weight_delta"] != 0:
            blockers.append("integration_receipt_block_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("integration_receipt_block_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_receipt_block_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("integration_receipt_block_with_effect_weight")
    return norm


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str, str, int]:
    if not packet:
        blockers.append("cycle_gate_reentry_integration_packet_missing_or_invalid")
        return {}, "cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0
    if packet.get("cycle_gate_reentry_integration_considered") is not True:
        blockers.append("cycle_gate_reentry_integration_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"cycle_gate_reentry_integration_boundary_{name}_missing")
    integration_status = str(packet.get("integration_status", "cycle_gate_reentry_integration_block"))
    if integration_status not in INTEGRATION_STATUSES:
        blockers.append("cycle_gate_reentry_integration_status_invalid")
        integration_status = "cycle_gate_reentry_integration_block"
    expected_gate, expected_set, expected_count = EXPECTED_BY_INTEGRATION[integration_status]
    gate_status = str(packet.get("integrated_cycle_gate_status", ""))
    set_status = str(packet.get("integrated_admissible_candidate_set_status", ""))
    if gate_status != expected_gate:
        blockers.append("cycle_gate_reentry_integration_gate_status_mismatch")
        gate_status = expected_gate
    if set_status != expected_set:
        blockers.append("cycle_gate_reentry_integration_candidate_set_status_mismatch")
        set_status = expected_set
    candidates = packet.get("integrated_candidates", [])
    candidate_count = len(candidates) if isinstance(candidates, list) else 0
    if candidate_count != expected_count:
        blockers.append("cycle_gate_reentry_integration_candidate_count_mismatch")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(integration_status, _m(packet.get("candidate_weighting")), blockers)
    if not packet.get("cycle_gate_reentry_integration_digest"):
        warnings.append("cycle_gate_reentry_integration_digest_missing")
    payload = {
        "integration_status": integration_status,
        "integrated_cycle_gate_status": gate_status,
        "integrated_admissible_candidate_set_status": set_status,
        "admissible_candidate_count": candidate_count,
        "integrated_candidates": candidates if isinstance(candidates, list) else [],
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_cycle_gate_reentry_integration_digest": str(packet.get("cycle_gate_reentry_integration_digest", _sha(dict(packet)))),
        "source_candidate_weighting_cycle_handoff_receipt_digest": str(_m(packet.get("source_digests")).get("candidate_weighting_cycle_handoff_receipt", "")),
        "source_candidate_weighting_cycle_handoff_digest": str(_m(packet.get("source_digests")).get("candidate_weighting_cycle_handoff", "")),
    }
    return payload, integration_status, gate_status, set_status, candidate_count


def _validate_gate(gate_payload: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not gate_payload:
        blockers.append("integrated_cycle_gate_state_missing_or_invalid")
        return
    if gate_payload.get("integrated_cycle_gate_ready") is not True:
        blockers.append("integrated_cycle_gate_state_not_ready")
    if str(gate_payload.get("integrated_cycle_gate_status", "")) != payload.get("integrated_cycle_gate_status"):
        blockers.append("integrated_cycle_gate_state_status_mismatch")
    if _normalize_weighting(_m(gate_payload.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("integrated_cycle_gate_state_weighting_mismatch")
    if str(gate_payload.get("source_cycle_gate_reentry_integration_digest", "")) != payload.get("source_cycle_gate_reentry_integration_digest"):
        blockers.append("integrated_cycle_gate_state_source_digest_mismatch")
    boundary = _m(gate_payload.get("boundary"))
    for name in REQUIRED_GATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"integrated_cycle_gate_state_boundary_{name}_missing")


def _validate_candidate_set(candidate_set: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not candidate_set:
        blockers.append("integrated_admissible_candidate_set_missing_or_invalid")
        return
    if candidate_set.get("integrated_admissible_candidate_set_ready") is not True:
        blockers.append("integrated_admissible_candidate_set_not_ready")
    if str(candidate_set.get("integrated_admissible_candidate_set_status", "")) != payload.get("integrated_admissible_candidate_set_status"):
        blockers.append("integrated_admissible_candidate_set_status_mismatch")
    if _int(candidate_set.get("admissible_candidate_count")) != _int(payload.get("admissible_candidate_count")):
        blockers.append("integrated_admissible_candidate_set_count_mismatch")
    if _normalize_weighting(_m(candidate_set.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("integrated_admissible_candidate_set_weighting_mismatch")
    if str(candidate_set.get("source_cycle_gate_reentry_integration_digest", "")) != payload.get("source_cycle_gate_reentry_integration_digest"):
        blockers.append("integrated_admissible_candidate_set_source_digest_mismatch")
    boundary = _m(candidate_set.get("boundary"))
    for name in REQUIRED_SET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"integrated_admissible_candidate_set_boundary_{name}_missing")


def _record(payload: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_cycle_gate_reentry_integration_receipt_record_v13_5",
        "record_type": "physical_quantum_qi_cycle_gate_reentry_integration_receipt",
        "integration_status": str(payload.get("integration_status", "")),
        "integrated_cycle_gate_status": str(payload.get("integrated_cycle_gate_status", "")),
        "integrated_admissible_candidate_set_status": str(payload.get("integrated_admissible_candidate_set_status", "")),
        "admissible_candidate_count": _int(payload.get("admissible_candidate_count")),
        "candidate_weighting": dict(_m(payload.get("candidate_weighting"))),
        "integrated_candidates": list(payload.get("integrated_candidates", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_cycle_gate_reentry_integration_digest": str(payload.get("source_cycle_gate_reentry_integration_digest", "")),
        "source_candidate_weighting_cycle_handoff_receipt_digest": str(payload.get("source_candidate_weighting_cycle_handoff_receipt_digest", "")),
        "source_candidate_weighting_cycle_handoff_digest": str(payload.get("source_candidate_weighting_cycle_handoff_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "cycle_gate_reentry_integration_receipt_only": True,
            "integrated_cycle_gate_state_traceable": True,
            "integrated_admissible_candidate_set_traceable": True,
            "uses_process_tensor_feedback": True,
            "non_markov_feedback_preserved": True,
            "history_window_feedback_preserved": True,
            "memory_kernel_feedback_preserved": True,
            "external_backaction_visible": True,
            "candidate_weighting_not_truth": True,
            "integration_not_direct_execution": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    cycle_gate_reentry_integration_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiCycleGateReentryIntegrationReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(cycle_gate_reentry_integration_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
    gate_path = root / "physical_quantum_qi_integrated_cycle_gate_state.json"
    set_path = root / "physical_quantum_qi_integrated_admissible_candidate_set.json"
    ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_license_not_ready")
    for name in [
        "integration_packet_read_allowed",
        "integrated_cycle_gate_state_read_allowed",
        "integrated_admissible_candidate_set_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, integration_status, gate_status, set_status, candidate_count = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_gate(_read_json(gate_path), payload, blockers)
    _validate_candidate_set(_read_json(set_path), payload, blockers)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_cycle_gate_reentry_integration_receipt_summary_v13_5",
            "integration_status": integration_status,
            "integrated_cycle_gate_status": gate_status,
            "integrated_admissible_candidate_set_status": set_status,
            "admissible_candidate_count": candidate_count,
            "candidate_weighting": dict(record["candidate_weighting"]),
            "latest_record_digest": record["record_digest"],
            "source_cycle_gate_reentry_integration_digest": record["source_cycle_gate_reentry_integration_digest"],
            "boundary": {
                "summary_only": True,
                "cycle_gate_reentry_integration_receipt_only": True,
                "integrated_cycle_gate_state_traceable": True,
                "integrated_admissible_candidate_set_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    final_status = "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-cycle-gate-reentry-integration-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5",
        "status": final_status,
        "packet_id": packet_id,
        "integration_status": integration_status,
        "integrated_cycle_gate_status": gate_status,
        "integrated_admissible_candidate_set_status": set_status,
        "admissible_candidate_count": candidate_count,
        "ledger_appended": appended,
        "record_digest": str(record.get("record_digest", "")),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiCycleGateReentryIntegrationReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5",
        final_status,
        packet_id,
        str(root),
        integration_status,
        gate_status,
        set_status,
        candidate_count,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )

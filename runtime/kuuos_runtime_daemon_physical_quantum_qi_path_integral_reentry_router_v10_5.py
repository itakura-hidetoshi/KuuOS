#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OS_NAMES = ("MemoryOS", "PlanOS", "RunGovernance")
FINAL_READINESS = {"final_ready", "final_needs_evidence", "final_repair_required"}
REENTRY_MODE = {
    "final_ready": "reinforce_path_weight",
    "final_needs_evidence": "open_probe_potential",
    "final_repair_required": "add_barrier_potential",
}


@dataclass(frozen=True)
class PhysicalQuantumQiPathIntegralReentryRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dominant_reentry_mode: str
    path_integral_reentry_packet_path: str
    receipt_path: str
    audit_path: str
    reentry_packet_written: bool
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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _final_item(packet: Mapping[str, Any], os_name: str) -> Mapping[str, Any]:
    return _m(_m(packet.get("final_readiness")).get(os_name))


def _readiness(packet: Mapping[str, Any], os_name: str) -> str:
    value = str(_final_item(packet, os_name).get("final_readiness", "final_repair_required"))
    return value if value in FINAL_READINESS else "final_repair_required"


def _score(readiness: str) -> int:
    return {"final_ready": 3, "final_needs_evidence": 1, "final_repair_required": -4}.get(readiness, -4)


def _dominant(readiness_by_os: Mapping[str, str]) -> str:
    values = list(readiness_by_os.values())
    if any(v == "final_repair_required" for v in values):
        return "add_barrier_potential"
    if any(v == "final_needs_evidence" for v in values):
        return "open_probe_potential"
    return "reinforce_path_weight"


def _os_reentry(os_name: str, readiness: str, final_packet: Mapping[str, Any], path_integral: Mapping[str, Any]) -> dict[str, Any]:
    item = _final_item(final_packet, os_name)
    dominant_path = str(path_integral.get("dominant_path", path_integral.get("stationary_path", "unknown")))
    return {
        "target_os": os_name,
        "source_final_readiness": readiness,
        "reentry_mode": REENTRY_MODE[readiness],
        "path_integral_effect": {
            "dominant_path_hint": dominant_path,
            "path_weight_delta": _score(readiness),
            "probe_potential_required": readiness == "final_needs_evidence",
            "barrier_potential_required": readiness == "final_repair_required",
            "stationary_phase_preserved": readiness == "final_ready",
        },
        "source_final_stage_action": item.get("final_stage_action", "unknown"),
        "history": item.get("history", {}),
        "boundary": {
            "reentry_only": True,
            "does_not_execute_path": True,
            "does_not_authorize_execution": True,
            "path_integral_candidate_weighting_only": True,
            "barrier_blocks_ready_weight": readiness == "final_repair_required",
        },
    }


def _packet(final_packet: Mapping[str, Any], path_integral: Mapping[str, Any], motion_bias: Mapping[str, Any], ledger_rows: list[dict[str, Any]]) -> dict[str, Any]:
    readiness_by_os = {os_name: _readiness(final_packet, os_name) for os_name in OS_NAMES}
    os_reentry = {os_name: _os_reentry(os_name, readiness_by_os[os_name], final_packet, path_integral) for os_name in OS_NAMES}
    dominant = _dominant(readiness_by_os)
    return {
        "version": "physical_quantum_qi_path_integral_reentry_packet_v10_5",
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": dominant,
        "os_reentry": os_reentry,
        "path_integral_reentry_counts": {
            "reinforce_path_weight": sum(1 for r in readiness_by_os.values() if r == "final_ready"),
            "open_probe_potential": sum(1 for r in readiness_by_os.values() if r == "final_needs_evidence"),
            "add_barrier_potential": sum(1 for r in readiness_by_os.values() if r == "final_repair_required"),
        },
        "path_integral_hints": {
            "dominant_path": str(path_integral.get("dominant_path", "unknown")),
            "stationary_path": str(path_integral.get("stationary_path", "unknown")),
            "next_motion_bias": str(path_integral.get("next_motion_bias", motion_bias.get("next_motion_bias", "unknown"))),
            "motion_mode": str(motion_bias.get("motion_mode", "unknown")),
            "path_action_scores": path_integral.get("path_action_scores", {}),
            "path_amplitude_weights": path_integral.get("path_amplitude_weights", {}),
        },
        "source_digests": {
            "final_stage_readiness": _sha(dict(final_packet)),
            "physical_quantum_qi_path_integral": _sha(dict(path_integral)),
            "physical_quantum_qi_motion_bias": _sha(dict(motion_bias)),
            "stage_feedback_action_intake_window": _sha(ledger_rows[-9:]),
        },
        "boundary": {
            "router_only": True,
            "reentry_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
        },
        "epoch": int(time.time()),
    }


def build_physical_quantum_qi_path_integral_reentry_router(*, runtime_context: Mapping[str, Any], reentry_router_license: Mapping[str, Any]) -> PhysicalQuantumQiPathIntegralReentryRouterResult:
    ctx = _m(runtime_context)
    lic = _m(reentry_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    final_path = root / "tri_os_final_stage_readiness_router_packet.json"
    path_integral_path = root / "physical_quantum_qi_path_integral_packet.json"
    motion_path = root / "physical_quantum_qi_motion_bias_packet.json"
    ledger_path = root / "tri_os_stage_feedback_action_intake_decision_ledger.jsonl"
    packet_path = root / "physical_quantum_qi_path_integral_reentry_packet.json"
    receipt_path = root / "physical_quantum_qi_path_integral_reentry_router_receipt.json"
    audit_path = root / "physical_quantum_qi_path_integral_reentry_router_audit.jsonl"

    if ctx.get("physical_quantum_qi_path_integral_reentry_router_enabled") is not True:
        blockers.append("physical_quantum_qi_path_integral_reentry_router_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_path_integral_reentry_router") is not True:
        blockers.append("apply_physical_quantum_qi_path_integral_reentry_router_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_ROUTER_LICENSE_READY":
        blockers.append("physical_quantum_qi_path_integral_reentry_router_license_not_ready")
    for name in ["final_readiness_packet_read_allowed", "path_integral_packet_read_allowed", "motion_bias_packet_read_allowed", "stage_feedback_action_intake_ledger_read_allowed", "reentry_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    final_packet = _read_json(final_path)
    path_integral = _read_json(path_integral_path)
    motion_bias = _read_json(motion_path)
    rows = [r for r in _read_jsonl(ledger_path) if r.get("record_type") == "tri_os_stage_feedback_action_intake_decision"]
    if not final_packet:
        blockers.append("tri_os_final_stage_readiness_router_packet_missing_or_invalid")
    elif final_packet.get("tri_os_final_stage_readiness_considered") is not True:
        blockers.append("tri_os_final_stage_readiness_considered_not_true")
    if final_packet and final_packet.get("boundary", {}).get("final_ready_is_not_execution_authority") is not True:
        blockers.append("final_ready_authority_boundary_invalid")
    if path_integral and path_integral.get("boundary", {}).get("path_integral_is_candidate_weighting_not_truth") is not True:
        blockers.append("path_integral_candidate_weighting_boundary_invalid")
    if not path_integral:
        warnings.append("physical_quantum_qi_path_integral_packet_missing")
    if not motion_bias:
        warnings.append("physical_quantum_qi_motion_bias_packet_missing")
    if not rows:
        warnings.append("stage_feedback_action_intake_ledger_empty_or_missing")
    if final_packet:
        for os_name in OS_NAMES:
            value = str(_final_item(final_packet, os_name).get("final_readiness", ""))
            if value not in FINAL_READINESS:
                blockers.append(f"{os_name.lower()}_final_readiness_invalid")

    packet: dict[str, Any] = {}
    written = False
    dominant = "unknown"
    if not blockers:
        packet = _packet(final_packet, path_integral, motion_bias, rows)
        if packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
            blockers.append("reentry_execution_boundary_invalid")
        else:
            dominant = str(packet["dominant_reentry_mode"])
            _write_json(packet_path, packet)
            written = True

    status = "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_ROUTER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_ROUTER_BLOCKED"
    packet_id = "physical-quantum-qi-path-integral-reentry-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_router_v10_5",
        "status": status,
        "packet_id": packet_id,
        "dominant_reentry_mode": dominant,
        "reentry_packet_written": written,
        "reentry_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiPathIntegralReentryRouterResult(
        "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_router_v10_5",
        status,
        packet_id,
        str(root),
        dominant,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )

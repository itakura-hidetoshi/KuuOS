#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiCirculationStabilityResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    receipt_path: str
    audit_path: str
    circulation_index: float
    stagnation_index: float
    stability_class: str
    recommended_action: str
    cycle_open: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _f(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


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


def _score(packet: Mapping[str, Any]) -> tuple[float, float]:
    flow = _clamp01(_f(packet.get("qi_flow", packet.get("flow", 0.5)), 0.5))
    coherence = _clamp01(_f(packet.get("coherence_score", packet.get("coherence", 0.5)), 0.5))
    recovery = 1.0 if packet.get("recovery_witness_present", True) is not False else 0.25
    circulation_pressure = _clamp01(_f(packet.get("circulation_pressure", packet.get("execution_pressure", 0.5)), 0.5))
    friction = _clamp01(_f(packet.get("friction", packet.get("drag", 0.0)), 0.0))
    circulation = _clamp01((0.35 * flow) + (0.25 * coherence) + (0.20 * circulation_pressure) + (0.20 * recovery) - (0.25 * friction))
    stagnation = _clamp01(1.0 - circulation + (0.35 * friction))
    return round(circulation, 6), round(stagnation, 6)


def _classify(circulation: float, stagnation: float, packet: Mapping[str, Any]) -> tuple[str, str, bool]:
    hard_stop = packet.get("critical_blocker_present") is True or packet.get("scope_mismatch") is True or packet.get("head_sha_mismatch") is True
    if hard_stop:
        return "blocked_by_concrete_reason", "concrete_stop", False
    if circulation >= 0.72 and stagnation <= 0.45:
        return "stable_by_circulation", "continue_cycle", True
    if circulation >= 0.48:
        return "metastable_by_partial_circulation", "rebalance_and_continue", True
    return "stagnation_risk", "reopen_flow", True


def build_qi_circulation_stability(*, runtime_context: Mapping[str, Any], stability_license_packet: Mapping[str, Any]) -> QiCirculationStabilityResult:
    ctx = _m(runtime_context)
    lic = _m(stability_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_circulation_packet.json"
    receipt_path = root / "qi_circulation_receipt.json"
    audit_path = root / "qi_circulation_audit.jsonl"
    if ctx.get("qi_circulation_stability_enabled") is not True:
        blockers.append("qi_circulation_stability_enabled_not_true")
    if ctx.get("apply_circulation_stability") is not True:
        blockers.append("apply_circulation_stability_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_STABILITY_LICENSE_READY":
        blockers.append("circulation_stability_license_not_ready")
    for name in ["packet_read_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    circulation, stagnation = _score(packet)
    stability_class, recommended_action, cycle_open = _classify(circulation, stagnation, packet)
    if stability_class == "stagnation_risk":
        warnings.append("stagnation_risk_prefers_reopen_flow")
    if stability_class == "blocked_by_concrete_reason":
        blockers.append("concrete_stop_reason_present")
    if blockers:
        status = "QI_CIRCULATION_STABILITY_BLOCKED"
    else:
        status = "QI_CIRCULATION_STABILITY_READY"
    packet_id = "qi-circulation-stability-" + _sha({"packet": packet, "status": status, "circulation": circulation, "stagnation": stagnation})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_stability_v2_7", "status": status, "packet_id": packet_id, "circulation_index": circulation, "stagnation_index": stagnation, "stability_class": stability_class, "recommended_action": recommended_action, "cycle_open": cycle_open, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationStabilityResult("kuuos_runtime_daemon_qi_circulation_stability_v2_7", status, packet_id, str(root), str(packet_path), str(receipt_path), str(audit_path), circulation, stagnation, stability_class, recommended_action, cycle_open, blockers, warnings)

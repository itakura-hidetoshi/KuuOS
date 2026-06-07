#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
import time
from typing import Any, Mapping


PATH_NAMES = {
    "stay_safely",
    "light_progress",
    "observe_probe",
    "rebalance_retry",
    "review_exit",
}

INTEGRAL_TO_PRIOR = {
    "integral_relief_observed": "light_progress",
    "progress_pain_acceptable": "observe_probe",
    "staying_suffering_dominates": "light_progress",
    "hold_requires_exit": "review_exit",
    "rebalance_required": "rebalance_retry",
}

QI_STATE_TO_PRIOR = {
    "smooth_circulation": "light_progress",
    "observation_deficiency": "observe_probe",
    "retry_stagnation": "rebalance_retry",
    "review_constraint": "review_exit",
    "mixed_turbulence": "observe_probe",
}

ACTION_TO_BIAS = {
    "stay_safely": "hold_for_review",
    "light_progress": "stable_continue",
    "observe_probe": "observe_more",
    "rebalance_retry": "retry_heavy",
    "review_exit": "hold_for_review",
}


@dataclass(frozen=True)
class PhysicalQuantumQiPathIntegralGovernorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dominant_path: str
    stationary_path: str
    path_integral_action: float
    next_motion_bias: str
    path_integral_packet_path: str
    receipt_path: str
    audit_path: str
    path_integral_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _num(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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


def _last(rows: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    return rows[-n:] if n > 0 else []


def _count(rows: list[dict[str, Any]], key: str, value: str) -> int:
    return sum(1 for row in rows if str(row.get(key, "")) == value)


def _base_actions(suffering_integral: Mapping[str, Any], coupling: Mapping[str, Any], progress_rows: list[dict[str, Any]]) -> dict[str, float]:
    integral_class = str(suffering_integral.get("suffering_integral_class", "progress_pain_acceptable"))
    qi_state = str(coupling.get("qi_state", "observation_deficiency"))
    stagnant = _num(suffering_integral.get("stagnant_safety_burden"), 0.0)
    transient = _num(suffering_integral.get("transient_progress_pain"), 0.0)
    net = _num(suffering_integral.get("net_suffering_integral_proxy"), stagnant - transient)
    recent = _last(progress_rows, 6)
    blocked = _count(recent, "progress_outcome_class", "progress_blocked")
    completed = _count(recent, "progress_outcome_class", "progress_completed")
    held = _count(recent, "progress_outcome_class", "exit_preserved_hold")

    actions = {
        "stay_safely": 2.0 + max(net, 0.0) + 0.6 * held,
        "light_progress": 2.0 + max(transient - stagnant, 0.0) + 0.4 * blocked - 0.5 * completed,
        "observe_probe": 2.0 + 0.5 * max(net, 0.0) + 0.2 * blocked,
        "rebalance_retry": 2.5 + 0.3 * max(net, 0.0) + 0.7 * blocked,
        "review_exit": 2.5 + 0.4 * max(net, 0.0) - 0.4 * held,
    }

    prior = INTEGRAL_TO_PRIOR.get(integral_class)
    if prior:
        actions[prior] -= 1.2
    qi_prior = QI_STATE_TO_PRIOR.get(qi_state)
    if qi_prior:
        actions[qi_prior] -= 0.8
    if integral_class == "staying_suffering_dominates":
        actions["stay_safely"] += 3.0
    if integral_class == "hold_requires_exit":
        actions["review_exit"] -= 1.5
        actions["stay_safely"] += 2.0
    if integral_class == "rebalance_required":
        actions["rebalance_retry"] -= 1.5
        actions["light_progress"] += 0.6
    if qi_state == "review_constraint":
        actions["review_exit"] -= 1.0
    return {name: round(max(0.1, value), 4) for name, value in actions.items()}


def _weights(actions: Mapping[str, float]) -> dict[str, float]:
    raw = {name: math.exp(-float(value)) for name, value in actions.items()}
    z = sum(raw.values()) or 1.0
    return {name: round(value / z, 6) for name, value in raw.items()}


def _dominant(actions: Mapping[str, float]) -> str:
    priority = ["review_exit", "rebalance_retry", "observe_probe", "light_progress", "stay_safely"]
    return sorted(actions, key=lambda name: (float(actions[name]), priority.index(name) if name in priority else 99))[0]


def _packet(suffering_integral: Mapping[str, Any], coupling: Mapping[str, Any], progress_rows: list[dict[str, Any]]) -> dict[str, Any]:
    actions = _base_actions(suffering_integral, coupling, progress_rows)
    weights = _weights(actions)
    dominant = _dominant(actions)
    stationary = dominant
    return {
        "version": "physical_quantum_qi_path_integral_packet_v8_3",
        "physical_quantum_qi_path_integral_considered": True,
        "qi_is_relational_field_not_substance": True,
        "observe_only_bounded_motion_candidate": True,
        "dominant_path": dominant,
        "stationary_path": stationary,
        "next_motion_bias": ACTION_TO_BIAS.get(dominant, "observe_more"),
        "path_integral_action": float(actions[dominant]),
        "candidate_paths": sorted(PATH_NAMES),
        "path_action_scores": actions,
        "path_amplitude_weights": weights,
        "partition_proxy": round(sum(math.exp(-float(v)) for v in actions.values()), 8),
        "source_digests": {
            "suffering_integral": _sha(dict(suffering_integral)),
            "qi_process_tensor_coupling": _sha(dict(coupling)),
            "progress_window": _sha(_last(progress_rows, 6)),
        },
        "boundary": {
            "path_integral_is_candidate_weighting_not_truth": True,
            "does_not_authorize_execution": True,
            "does_not_authorize_medical_action": True,
            "does_not_authorize_theorem_claim": True,
            "non_markov_history_visible": True,
        },
        "epoch": int(time.time()),
    }


def build_physical_quantum_qi_path_integral_governor(*, runtime_context: Mapping[str, Any], path_integral_license: Mapping[str, Any]) -> PhysicalQuantumQiPathIntegralGovernorResult:
    ctx = _m(runtime_context)
    lic = _m(path_integral_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    suffering_integral_path = root / "qi_suffering_integral_packet.json"
    coupling_path = root / "qi_process_tensor_policy_coupling_packet.json"
    progress_path = root / "qi_progress_outcome_ledger.jsonl"
    packet_path = root / "physical_quantum_qi_path_integral_packet.json"
    receipt_path = root / "physical_quantum_qi_path_integral_governor_receipt.json"
    audit_path = root / "physical_quantum_qi_path_integral_governor_audit.jsonl"

    if ctx.get("physical_quantum_qi_path_integral_governor_enabled") is not True:
        blockers.append("physical_quantum_qi_path_integral_governor_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_path_integral_governor") is not True:
        blockers.append("apply_physical_quantum_qi_path_integral_governor_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_GOVERNOR_LICENSE_READY":
        blockers.append("physical_quantum_qi_path_integral_governor_license_not_ready")
    for name in ["suffering_integral_read_allowed", "qi_process_tensor_coupling_read_allowed", "progress_outcome_read_allowed", "path_integral_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    suffering_integral = _read_json(suffering_integral_path)
    coupling = _read_json(coupling_path)
    progress_rows = [r for r in _read_jsonl(progress_path) if r.get("record_type") == "progress_outcome"]
    if not suffering_integral:
        blockers.append("qi_suffering_integral_packet_missing_or_invalid")
    if not coupling:
        blockers.append("qi_process_tensor_policy_coupling_packet_missing_or_invalid")
    if not progress_rows:
        warnings.append("progress_outcome_ledger_empty_or_missing")
    if suffering_integral and suffering_integral.get("suffering_integral_considered") is not True:
        blockers.append("suffering_integral_considered_not_true")
    if coupling and coupling.get("qi_process_tensor_considered") is not True:
        blockers.append("qi_process_tensor_considered_not_true")

    packet: dict[str, Any] = {}
    written = False
    dominant = "unknown"
    stationary = "unknown"
    action = 0.0
    bias = "unknown"
    if not blockers:
        packet = _packet(suffering_integral, coupling, progress_rows)
        dominant = str(packet["dominant_path"])
        stationary = str(packet["stationary_path"])
        action = float(packet["path_integral_action"])
        bias = str(packet["next_motion_bias"])
        if dominant not in PATH_NAMES:
            blockers.append("dominant_path_not_allowlisted")
        elif packet.get("observe_only_bounded_motion_candidate") is not True:
            blockers.append("observe_only_bounded_motion_candidate_not_true")
        else:
            _write_json(packet_path, packet)
            written = True

    status = "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_GOVERNOR_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_GOVERNOR_BLOCKED"
    packet_id = "physical-quantum-qi-path-integral-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_path_integral_governor_v8_3",
        "status": status,
        "packet_id": packet_id,
        "dominant_path": dominant,
        "stationary_path": stationary,
        "path_integral_action": action,
        "next_motion_bias": bias,
        "path_integral_packet_written": written,
        "path_integral_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiPathIntegralGovernorResult(
        "kuuos_runtime_daemon_physical_quantum_qi_path_integral_governor_v8_3",
        status,
        packet_id,
        str(root),
        dominant,
        stationary,
        action,
        bias,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )

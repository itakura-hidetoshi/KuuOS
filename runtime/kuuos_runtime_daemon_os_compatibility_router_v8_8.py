#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ROUTES = {
    "memory_route": {
        "os_pair": "MemoryOS_x_QiProcessTensor",
        "target_packet": "memory_process_tensor_recall_anchor",
        "why": "MemoryOS benefits from non-Markov process history without treating memory as overwrite authority.",
    },
    "plan_route": {
        "os_pair": "PlanOS_x_PhysicalQuantumQiPathIntegral",
        "target_packet": "plan_path_integral_motion_candidate",
        "why": "PlanOS benefits from weighted candidate paths while keeping path integral outputs advisory.",
    },
    "run_governance_route": {
        "os_pair": "RunGovernance_x_QiQUE",
        "target_packet": "run_governance_queue_and_exit_control",
        "why": "Run Governance benefits from QUE-style queued escalation, exit, and bounded action gates.",
    },
}


@dataclass(frozen=True)
class OSCompatibilityRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dominant_route: str
    memory_fit: str
    plan_fit: str
    run_governance_fit: str
    compatibility_packet_path: str
    receipt_path: str
    audit_path: str
    compatibility_packet_written: bool
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


def _fit(ok: bool, partial: bool = False) -> str:
    if ok:
        return "high"
    if partial:
        return "partial"
    return "missing"


def _route_score(fit: str) -> int:
    return {"high": 3, "partial": 1, "missing": 0}.get(fit, 0)


def _dominant(memory_fit: str, plan_fit: str, run_fit: str) -> str:
    scores = {
        "memory_route": _route_score(memory_fit),
        "plan_route": _route_score(plan_fit),
        "run_governance_route": _route_score(run_fit),
    }
    priority = ["run_governance_route", "plan_route", "memory_route"]
    return sorted(scores, key=lambda key: (-scores[key], priority.index(key)))[0]


def _packet(coupling: Mapping[str, Any], path_integral: Mapping[str, Any], motion: Mapping[str, Any], progress_outcomes: list[dict[str, Any]], qi_que: Mapping[str, Any]) -> dict[str, Any]:
    memory_fit = _fit(
        coupling.get("qi_process_tensor_considered") is True and coupling.get("boundary", {}).get("non_markov_history_visible") is True,
        partial=bool(coupling),
    )
    plan_fit = _fit(
        path_integral.get("physical_quantum_qi_path_integral_considered") is True
        and path_integral.get("observe_only_bounded_motion_candidate") is True
        and path_integral.get("boundary", {}).get("path_integral_is_candidate_weighting_not_truth") is True,
        partial=bool(path_integral),
    )
    run_fit = _fit(
        motion.get("boundary", {}).get("does_not_authorize_execution") is True
        and motion.get("boundary", {}).get("path_integral_candidate_weighting_preserved") is True,
        partial=bool(motion) or bool(qi_que),
    )
    dominant = _dominant(memory_fit, plan_fit, run_fit)
    return {
        "version": "os_compatibility_router_packet_v8_8",
        "os_compatibility_considered": True,
        "dominant_route": dominant,
        "routes": {
            "memory_route": {**ROUTES["memory_route"], "fit": memory_fit},
            "plan_route": {**ROUTES["plan_route"], "fit": plan_fit},
            "run_governance_route": {**ROUTES["run_governance_route"], "fit": run_fit},
        },
        "routing_recommendations": {
            "MemoryOS": "store process tensor lineage as recall anchor, not overwrite",
            "PlanOS": "consume path integral as weighted candidate paths, not execution authority",
            "RunGovernance": "consume motion/progress packet through bounded queue, exit, and blocker gates",
        },
        "compatibility_axioms": {
            "MemoryOS_x_QiProcessTensor": "non_markov_history_visible_and_append_only",
            "PlanOS_x_PhysicalQuantumQiPathIntegral": "candidate_weighting_not_truth_and_advisory_only",
            "RunGovernance_x_QiQUE": "queued_bounded_execution_with_exit_and_blocker_visibility",
        },
        "source_digests": {
            "qi_process_tensor_coupling": _sha(dict(coupling)),
            "physical_quantum_qi_path_integral": _sha(dict(path_integral)),
            "physical_quantum_qi_motion_bias": _sha(dict(motion)),
            "progress_outcome_window": _sha(progress_outcomes[-6:]),
            "qi_que": _sha(dict(qi_que)),
        },
        "boundary": {
            "router_only": True,
            "does_not_run_runner": True,
            "does_not_overwrite_memory": True,
            "does_not_authorize_execution": True,
            "does_not_convert_candidate_weighting_to_truth": True,
        },
        "epoch": int(time.time()),
    }


def build_os_compatibility_router(*, runtime_context: Mapping[str, Any], os_compatibility_license: Mapping[str, Any]) -> OSCompatibilityRouterResult:
    ctx = _m(runtime_context)
    lic = _m(os_compatibility_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    coupling_path = root / "qi_process_tensor_policy_coupling_packet.json"
    path_integral_path = root / "physical_quantum_qi_path_integral_packet.json"
    motion_path = root / "physical_quantum_qi_motion_bias_packet.json"
    progress_path = root / "qi_progress_outcome_ledger.jsonl"
    qi_que_path = root / "qi_que_governance_packet.json"
    packet_path = root / "os_compatibility_router_packet.json"
    receipt_path = root / "os_compatibility_router_receipt.json"
    audit_path = root / "os_compatibility_router_audit.jsonl"

    if ctx.get("os_compatibility_router_enabled") is not True:
        blockers.append("os_compatibility_router_enabled_not_true")
    if ctx.get("apply_os_compatibility_router") is not True:
        blockers.append("apply_os_compatibility_router_not_true")
    if lic.get("license_status") != "OS_COMPATIBILITY_ROUTER_LICENSE_READY":
        blockers.append("os_compatibility_router_license_not_ready")
    for name in ["qi_process_tensor_read_allowed", "path_integral_read_allowed", "motion_bias_read_allowed", "progress_outcome_read_allowed", "qi_que_read_allowed", "compatibility_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    coupling = _read_json(coupling_path)
    path_integral = _read_json(path_integral_path)
    motion = _read_json(motion_path)
    qi_que = _read_json(qi_que_path)
    progress = [r for r in _read_jsonl(progress_path) if r.get("record_type") == "progress_outcome"]
    if not coupling:
        warnings.append("qi_process_tensor_coupling_missing")
    if not path_integral:
        warnings.append("physical_quantum_qi_path_integral_missing")
    if not motion:
        warnings.append("physical_quantum_qi_motion_bias_missing")
    if not qi_que:
        warnings.append("qi_que_governance_packet_missing")
    if not progress:
        warnings.append("progress_outcome_ledger_empty_or_missing")
    if not (coupling or path_integral or motion or qi_que or progress):
        blockers.append("no_compatibility_sources_available")

    packet: dict[str, Any] = {}
    written = False
    dominant = "unknown"
    memory_fit = "missing"
    plan_fit = "missing"
    run_fit = "missing"
    if not blockers:
        packet = _packet(coupling, path_integral, motion, progress, qi_que)
        dominant = str(packet["dominant_route"])
        memory_fit = str(packet["routes"]["memory_route"]["fit"])
        plan_fit = str(packet["routes"]["plan_route"]["fit"])
        run_fit = str(packet["routes"]["run_governance_route"]["fit"])
        if dominant not in ROUTES:
            blockers.append("dominant_route_not_allowlisted")
        elif packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
            blockers.append("router_boundary_invalid")
        else:
            _write_json(packet_path, packet)
            written = True

    status = "OS_COMPATIBILITY_ROUTER_READY" if not blockers else "OS_COMPATIBILITY_ROUTER_BLOCKED"
    packet_id = "os-compatibility-router-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_os_compatibility_router_v8_8",
        "status": status,
        "packet_id": packet_id,
        "dominant_route": dominant,
        "memory_fit": memory_fit,
        "plan_fit": plan_fit,
        "run_governance_fit": run_fit,
        "compatibility_packet_written": written,
        "compatibility_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return OSCompatibilityRouterResult(
        "kuuos_runtime_daemon_os_compatibility_router_v8_8",
        status,
        packet_id,
        str(root),
        dominant,
        memory_fit,
        plan_fit,
        run_fit,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ROUTE_NAMES = {"memory_route", "plan_route", "run_governance_route"}
FIT_VALUES = {"high", "partial", "missing"}


@dataclass(frozen=True)
class TriOSCompatibilityHandoffEmitterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_handoff_path: str
    plan_handoff_path: str
    run_governance_handoff_path: str
    receipt_path: str
    audit_path: str
    handoffs_written: int
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


def _route_fit(router: Mapping[str, Any], route: str) -> str:
    value = router.get("routes", {}).get(route, {}).get("fit", "missing")
    return str(value) if str(value) in FIT_VALUES else "missing"


def _memory_packet(router: Mapping[str, Any], coupling: Mapping[str, Any], progress: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "memory_os_qi_process_tensor_handoff_packet_v8_9",
        "target_os": "MemoryOS",
        "source_pair": "MemoryOS_x_QiProcessTensor",
        "route_fit": _route_fit(router, "memory_route"),
        "handoff_kind": "process_tensor_recall_anchor",
        "recall_anchor": {
            "qi_state": str(coupling.get("qi_state", "unknown")),
            "process_memory_depth": coupling.get("process_memory_depth", "unknown"),
            "non_markov_history_visible": coupling.get("boundary", {}).get("non_markov_history_visible") is True,
            "recent_progress_window_digest": _sha(progress[-6:]),
        },
        "source_digests": {
            "router": _sha(dict(router)),
            "qi_process_tensor_coupling": _sha(dict(coupling)),
        },
        "boundary": {
            "handoff_only": True,
            "append_only_memory_anchor": True,
            "does_not_overwrite_memory": True,
            "does_not_create_memory_authority": True,
        },
        "epoch": int(time.time()),
    }


def _plan_packet(router: Mapping[str, Any], path_integral: Mapping[str, Any], motion: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "plan_os_physical_quantum_qi_handoff_packet_v8_9",
        "target_os": "PlanOS",
        "source_pair": "PlanOS_x_PhysicalQuantumQiPathIntegral",
        "route_fit": _route_fit(router, "plan_route"),
        "handoff_kind": "weighted_candidate_paths",
        "plan_candidates": {
            "dominant_path": str(path_integral.get("dominant_path", motion.get("dominant_path", "unknown"))),
            "stationary_path": str(path_integral.get("stationary_path", "unknown")),
            "next_motion_bias": str(path_integral.get("next_motion_bias", motion.get("next_motion_bias", "unknown"))),
            "path_action_scores": path_integral.get("path_action_scores", {}),
            "path_amplitude_weights": path_integral.get("path_amplitude_weights", {}),
            "motion_mode": str(motion.get("motion_mode", "unknown")),
        },
        "source_digests": {
            "router": _sha(dict(router)),
            "path_integral": _sha(dict(path_integral)),
            "motion_bias": _sha(dict(motion)),
        },
        "boundary": {
            "handoff_only": True,
            "candidate_weighting_not_truth": True,
            "advisory_plan_input_only": True,
            "does_not_authorize_execution": True,
        },
        "epoch": int(time.time()),
    }


def _run_governance_packet(router: Mapping[str, Any], motion: Mapping[str, Any], qi_que: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "run_governance_qi_que_handoff_packet_v8_9",
        "target_os": "RunGovernance",
        "source_pair": "RunGovernance_x_QiQUE",
        "route_fit": _route_fit(router, "run_governance_route"),
        "handoff_kind": "bounded_queue_exit_control",
        "governance_candidate": {
            "motion_mode": str(motion.get("motion_mode", "unknown")),
            "progress_action": str(motion.get("progress_action", "unknown")),
            "small_probe_required": motion.get("small_probe_required") is True,
            "review_exit_required": motion.get("review_exit_required") is True,
            "queued_bounded_execution": qi_que.get("queued_bounded_execution") is True,
            "exit_gate_visible": qi_que.get("exit_gate_visible") is True,
        },
        "source_digests": {
            "router": _sha(dict(router)),
            "motion_bias": _sha(dict(motion)),
            "qi_que": _sha(dict(qi_que)),
        },
        "boundary": {
            "handoff_only": True,
            "queue_gate_required": True,
            "exit_gate_required": True,
            "blocker_visibility_required": True,
            "does_not_run_runner": True,
            "does_not_authorize_execution": True,
        },
        "epoch": int(time.time()),
    }


def build_tri_os_compatibility_handoff_emitter(*, runtime_context: Mapping[str, Any], tri_os_handoff_license: Mapping[str, Any]) -> TriOSCompatibilityHandoffEmitterResult:
    ctx = _m(runtime_context)
    lic = _m(tri_os_handoff_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    router_path = root / "os_compatibility_router_packet.json"
    coupling_path = root / "qi_process_tensor_policy_coupling_packet.json"
    path_integral_path = root / "physical_quantum_qi_path_integral_packet.json"
    motion_path = root / "physical_quantum_qi_motion_bias_packet.json"
    progress_path = root / "qi_progress_outcome_ledger.jsonl"
    qi_que_path = root / "qi_que_governance_packet.json"
    memory_path = root / "memory_os_qi_process_tensor_handoff_packet.json"
    plan_path = root / "plan_os_physical_quantum_qi_handoff_packet.json"
    run_path = root / "run_governance_qi_que_handoff_packet.json"
    receipt_path = root / "tri_os_compatibility_handoff_emitter_receipt.json"
    audit_path = root / "tri_os_compatibility_handoff_emitter_audit.jsonl"

    if ctx.get("tri_os_compatibility_handoff_emitter_enabled") is not True:
        blockers.append("tri_os_compatibility_handoff_emitter_enabled_not_true")
    if ctx.get("apply_tri_os_compatibility_handoff_emitter") is not True:
        blockers.append("apply_tri_os_compatibility_handoff_emitter_not_true")
    if lic.get("license_status") != "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_LICENSE_READY":
        blockers.append("tri_os_compatibility_handoff_emitter_license_not_ready")
    for name in ["router_packet_read_allowed", "source_packets_read_allowed", "memory_handoff_write_allowed", "plan_handoff_write_allowed", "run_governance_handoff_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    router = _read_json(router_path)
    coupling = _read_json(coupling_path)
    path_integral = _read_json(path_integral_path)
    motion = _read_json(motion_path)
    qi_que = _read_json(qi_que_path)
    progress = [r for r in _read_jsonl(progress_path) if r.get("record_type") == "progress_outcome"]
    if not router:
        blockers.append("os_compatibility_router_packet_missing_or_invalid")
    elif router.get("os_compatibility_considered") is not True:
        blockers.append("os_compatibility_considered_not_true")
    if router and router.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("router_execution_boundary_invalid")
    if not coupling:
        warnings.append("qi_process_tensor_coupling_missing")
    if not path_integral:
        warnings.append("physical_quantum_qi_path_integral_missing")
    if not motion:
        warnings.append("physical_quantum_qi_motion_bias_missing")
    if not qi_que:
        warnings.append("qi_que_governance_packet_missing")

    written = 0
    memory_packet: dict[str, Any] = {}
    plan_packet: dict[str, Any] = {}
    run_packet: dict[str, Any] = {}
    if not blockers:
        memory_packet = _memory_packet(router, coupling, progress)
        plan_packet = _plan_packet(router, path_integral, motion)
        run_packet = _run_governance_packet(router, motion, qi_que)
        _write_json(memory_path, memory_packet)
        written += 1
        _write_json(plan_path, plan_packet)
        written += 1
        _write_json(run_path, run_packet)
        written += 1

    status = "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_READY" if not blockers else "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_BLOCKED"
    packet_id = "tri-os-compatibility-handoff-" + _sha({"memory": memory_packet, "plan": plan_packet, "run": run_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_compatibility_handoff_emitter_v8_9",
        "status": status,
        "packet_id": packet_id,
        "handoffs_written": written,
        "memory_handoff_digest": _sha(memory_packet),
        "plan_handoff_digest": _sha(plan_packet),
        "run_governance_handoff_digest": _sha(run_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSCompatibilityHandoffEmitterResult(
        "kuuos_runtime_daemon_tri_os_compatibility_handoff_emitter_v8_9",
        status,
        packet_id,
        str(root),
        str(memory_path),
        str(plan_path),
        str(run_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )

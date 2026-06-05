#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_circulation_change_router_v2_8 import build_qi_circulation_change_router
from runtime.kuuos_runtime_daemon_qi_circulation_feedback_controller_v2_9 import build_qi_circulation_feedback_controller


@dataclass(frozen=True)
class QiCirculationClosedLoopRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    receipt_path: str
    audit_path: str
    cycle_count: int
    converged: bool
    final_qi_packet: dict[str, Any]
    final_action: str
    final_delta: float
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _f(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _router_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_CHANGE_ROUTER_LICENSE_READY",
        "route_packet_read_allowed": True,
        "circulation_packet_write_allowed": True,
        "circulation_run_allowed": True,
        "forward_packet_write_allowed": True,
        "forward_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _feedback_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_FEEDBACK_LICENSE_READY",
        "packet_read_allowed": True,
        "next_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _route_packet(base: Mapping[str, Any], qi_packet: Mapping[str, Any], cycle: int) -> dict[str, Any]:
    route = dict(base)
    route["qi_process_tensor_packet"] = dict(qi_packet)
    branch = str(route.get("branch", "qi-closed-loop"))
    route["branch"] = f"{branch}-cycle-{cycle}"
    route.setdefault("mode", "mock")
    route.setdefault("required_checks", [{"name": "mock", "status": "success"}])
    route.setdefault("files", [{"kind": "create_file", "path": f"tmp/qi-closed-loop-cycle-{cycle}.txt", "content": "ok", "message": "Qi closed-loop cycle"}])
    return route


def _feedback_packet(qi_packet: Mapping[str, Any], router_receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {"current_qi_packet": dict(qi_packet), "router_receipt": dict(router_receipt), "recommended_action": router_receipt.get("recommended_action")}


def _delta(prev: Mapping[str, Any], nxt: Mapping[str, Any]) -> float:
    keys = ["qi_flow", "coherence_score", "circulation_pressure", "friction"]
    return round(sum(abs(_f(nxt.get(k), 0.0) - _f(prev.get(k), 0.0)) for k in keys), 6)


def build_qi_circulation_closed_loop_runner(*, runtime_context: Mapping[str, Any], loop_license_packet: Mapping[str, Any]) -> QiCirculationClosedLoopRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(loop_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_circulation_closed_loop_packet.json"
    receipt_path = root / "qi_circulation_closed_loop_receipt.json"
    audit_path = root / "qi_circulation_closed_loop_audit.jsonl"
    if ctx.get("qi_circulation_closed_loop_enabled") is not True:
        blockers.append("qi_circulation_closed_loop_enabled_not_true")
    if ctx.get("apply_circulation_closed_loop") is not True:
        blockers.append("apply_circulation_closed_loop_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_CLOSED_LOOP_LICENSE_READY":
        blockers.append("circulation_closed_loop_license_not_ready")
    for name in ["packet_read_allowed", "router_run_allowed", "feedback_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    qi_packet = dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else {}
    base_route = dict(packet.get("route_base", {})) if isinstance(packet.get("route_base"), Mapping) else {}
    max_cycles = max(1, min(12, _i(packet.get("max_cycles"), 3)))
    threshold = max(0.0, _f(packet.get("convergence_threshold"), 0.03))
    final_action = "not_run"
    final_delta = 0.0
    converged = False
    cycle_count = 0
    if not qi_packet:
        blockers.append("initial_qi_packet_missing")
    for required in ["repository_full_name", "branch", "base_branch", "base_sha", "pr_number", "expected_head_sha", "actual_head_sha"]:
        if required not in base_route:
            blockers.append(f"route_base_{required}_missing")
    if not blockers:
        for cycle in range(1, max_cycles + 1):
            cycle_count = cycle
            cycle_root = root / f"cycle_{cycle}"
            cycle_root.mkdir(parents=True, exist_ok=True)
            route = _route_packet(base_route, qi_packet, cycle)
            _write_json(cycle_root / "circulation_change_route_packet.json", route)
            router = build_qi_circulation_change_router(runtime_context={"qi_circulation_change_router_enabled": True, "apply_circulation_change_router": True, "runtime_root": str(cycle_root)}, router_license_packet=_router_license())
            router_payload = router.to_dict()
            final_action = str(router_payload.get("recommended_action", "unknown"))
            records.append({"cycle": cycle, "stage": "router", "status": router_payload.get("status"), "action": final_action, "digest": _sha(router_payload), "epoch": int(time.time())})
            if router_payload.get("status") == "QI_CIRCULATION_CHANGE_ROUTER_BLOCKED":
                blockers.append("router_blocked")
                break
            _write_json(cycle_root / "qi_circulation_feedback_packet.json", _feedback_packet(qi_packet, router_payload))
            feedback = build_qi_circulation_feedback_controller(runtime_context={"qi_circulation_feedback_enabled": True, "apply_circulation_feedback": True, "runtime_root": str(cycle_root)}, feedback_license_packet=_feedback_license())
            feedback_payload = feedback.to_dict()
            next_qi = dict(feedback_payload.get("next_qi_packet", {}))
            records.append({"cycle": cycle, "stage": "feedback", "status": feedback_payload.get("status"), "feedback_action": feedback_payload.get("feedback_action"), "digest": _sha(feedback_payload), "epoch": int(time.time())})
            if feedback_payload.get("status") == "QI_CIRCULATION_FEEDBACK_BLOCKED":
                blockers.append("feedback_blocked")
                break
            final_delta = _delta(qi_packet, next_qi)
            qi_packet = next_qi
            if final_delta <= threshold and cycle > 1:
                converged = True
                break
    if blockers:
        status = "QI_CIRCULATION_CLOSED_LOOP_BLOCKED"
    elif converged:
        status = "QI_CIRCULATION_CLOSED_LOOP_CONVERGED"
    else:
        status = "QI_CIRCULATION_CLOSED_LOOP_READY"
    packet_id = "qi-circulation-closed-loop-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_closed_loop_runner_v3_0", "status": status, "packet_id": packet_id, "cycle_count": cycle_count, "converged": converged, "final_qi_packet": qi_packet, "final_action": final_action, "final_delta": final_delta, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationClosedLoopRunnerResult("kuuos_runtime_daemon_qi_circulation_closed_loop_runner_v3_0", status, packet_id, str(root), str(packet_path), str(receipt_path), str(audit_path), cycle_count, converged, qi_packet, final_action, final_delta, blockers, warnings, records)

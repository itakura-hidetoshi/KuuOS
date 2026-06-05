#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_circulation_stability_v2_7 import build_qi_circulation_stability
from runtime.kuuos_runtime_daemon_qi_forward_change_runner_v2_6 import build_qi_forward_change_runner


@dataclass(frozen=True)
class QiCirculationChangeRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    circulation_packet_path: str
    forward_packet_path: str
    receipt_path: str
    audit_path: str
    circulation_status: str
    stability_class: str
    recommended_action: str
    routed: bool
    downstream_status: str
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

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


def _stability_license() -> dict[str, Any]:
    return {"license_status": "QI_CIRCULATION_STABILITY_LICENSE_READY", "packet_read_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _forward_license() -> dict[str, Any]:
    return {"license_status": "QI_FORWARD_CHANGE_RUNNER_LICENSE_READY", "packet_read_allowed": True, "packet_write_allowed": True, "loop_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _routable(action: str) -> bool:
    return action in {"continue_cycle", "rebalance_and_continue", "reopen_flow"}


def _derive_forward_packet(route_packet: Mapping[str, Any], action: str) -> dict[str, Any]:
    raw = route_packet.get("forward_change_packet", {})
    forward = dict(raw) if isinstance(raw, Mapping) else {}
    forward.setdefault("forward_intent", True)
    forward.setdefault("title", f"Qi circulation route: {action}")
    forward.setdefault("body", f"Routed by Qi circulation action {action}")
    forward.setdefault("mode", route_packet.get("mode", "mock"))
    if "repository_full_name" in route_packet:
        forward.setdefault("repository_full_name", route_packet.get("repository_full_name"))
    if "branch" in route_packet:
        forward.setdefault("branch", route_packet.get("branch"))
    if "base_branch" in route_packet:
        forward.setdefault("base_branch", route_packet.get("base_branch"))
    if "base_sha" in route_packet:
        forward.setdefault("base_sha", route_packet.get("base_sha"))
    if "expected_head_sha" in route_packet:
        forward.setdefault("expected_head_sha", route_packet.get("expected_head_sha"))
    if "actual_head_sha" in route_packet:
        forward.setdefault("actual_head_sha", route_packet.get("actual_head_sha"))
    forward.setdefault("required_checks", route_packet.get("required_checks", [{"name": "mock", "status": "success"}]))
    forward.setdefault("files", route_packet.get("files", []))
    forward["circulation_route_action"] = action
    return forward


def build_qi_circulation_change_router(*, runtime_context: Mapping[str, Any], router_license_packet: Mapping[str, Any]) -> QiCirculationChangeRouterResult:
    ctx = _m(runtime_context)
    lic = _m(router_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    route_packet_path = root / "circulation_change_route_packet.json"
    circulation_packet_path = root / "qi_circulation_packet.json"
    forward_packet_path = root / "forward_change_packet.json"
    receipt_path = root / "circulation_change_router_receipt.json"
    audit_path = root / "circulation_change_router_audit.jsonl"
    if ctx.get("qi_circulation_change_router_enabled") is not True:
        blockers.append("qi_circulation_change_router_enabled_not_true")
    if ctx.get("apply_circulation_change_router") is not True:
        blockers.append("apply_circulation_change_router_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_CHANGE_ROUTER_LICENSE_READY":
        blockers.append("circulation_change_router_license_not_ready")
    for name in ["route_packet_read_allowed", "circulation_packet_write_allowed", "circulation_run_allowed", "forward_packet_write_allowed", "forward_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    route_packet = _read_json(route_packet_path)
    circulation_packet = dict(route_packet.get("qi_process_tensor_packet", {})) if isinstance(route_packet.get("qi_process_tensor_packet"), Mapping) else dict(route_packet.get("circulation_packet", {})) if isinstance(route_packet.get("circulation_packet"), Mapping) else {}
    circulation_status = "NOT_RUN"
    stability_class = "unknown"
    recommended_action = "unknown"
    routed = False
    downstream_status = "NOT_RUN"
    if not blockers:
        _write_json(circulation_packet_path, circulation_packet)
        stability = build_qi_circulation_stability(runtime_context={"qi_circulation_stability_enabled": True, "apply_circulation_stability": True, "runtime_root": str(root)}, stability_license_packet=_stability_license())
        stability_payload = stability.to_dict()
        circulation_status = str(stability_payload.get("status"))
        stability_class = str(stability_payload.get("stability_class"))
        recommended_action = str(stability_payload.get("recommended_action"))
        records.append({"stage": "circulation", "status": circulation_status, "action": recommended_action, "digest": _sha(stability_payload), "epoch": int(time.time())})
        if circulation_status != "QI_CIRCULATION_STABILITY_READY" and recommended_action == "concrete_stop":
            blockers.append("circulation_concrete_stop")
    if not blockers and _routable(recommended_action):
        forward_packet = _derive_forward_packet(route_packet, recommended_action)
        _write_json(forward_packet_path, forward_packet)
        routed = True
        downstream = build_qi_forward_change_runner(runtime_context={"qi_forward_change_runner_enabled": True, "apply_forward_change_runner": True, "runtime_root": str(root)}, runner_license_packet=_forward_license())
        downstream_payload = downstream.to_dict()
        downstream_status = str(downstream_payload.get("status"))
        records.append({"stage": "forward", "status": downstream_status, "digest": _sha(downstream_payload), "epoch": int(time.time())})
        if downstream_status != "QI_FORWARD_CHANGE_RUNNER_MERGED":
            blockers.append("forward_runner_not_merged")
    elif not blockers:
        warnings.append("circulation_not_routable")
    if blockers:
        status = "QI_CIRCULATION_CHANGE_ROUTER_BLOCKED"
    elif routed:
        status = "QI_CIRCULATION_CHANGE_ROUTER_ROUTED"
    else:
        status = "QI_CIRCULATION_CHANGE_ROUTER_IDLE"
    packet_id = "qi-circulation-change-router-" + _sha({"route": route_packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_change_router_v2_8", "status": status, "packet_id": packet_id, "circulation_status": circulation_status, "stability_class": stability_class, "recommended_action": recommended_action, "routed": routed, "downstream_status": downstream_status, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationChangeRouterResult("kuuos_runtime_daemon_qi_circulation_change_router_v2_8", status, packet_id, str(root), str(circulation_packet_path), str(forward_packet_path), str(receipt_path), str(audit_path), circulation_status, stability_class, recommended_action, routed, downstream_status, blockers, warnings, records)

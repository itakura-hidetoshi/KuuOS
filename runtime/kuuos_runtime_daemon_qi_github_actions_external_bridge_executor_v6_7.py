#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_external_wait_resolver_v6_3 import build_qi_github_actions_external_wait_resolver
from runtime.kuuos_runtime_daemon_qi_github_actions_external_call_result_adapter_v6_4 import build_qi_github_actions_external_call_result_adapter
from runtime.kuuos_runtime_daemon_qi_github_actions_external_call_dispatcher_v6_5 import build_qi_github_actions_external_call_dispatcher
from runtime.kuuos_runtime_daemon_qi_github_actions_dispatch_result_collector_v6_6 import DISPATCH_RESULT_FILES, build_qi_github_actions_dispatch_result_collector


LOCAL_EXTERNAL_STAGES = {
    "external_wait_resolve",
    "external_call_dispatch",
    "dispatch_result_collect",
    "external_result_adapt",
    "await_dispatch_result",
    "await_external_call",
}


@dataclass(frozen=True)
class QiGitHubActionsExternalBridgeExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    selected_stage: str
    stage_status: str
    stage_result_class: str
    receipt_path: str
    audit_path: str
    local_stage_performed: bool
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


def _dispatch_packet_name(target: str) -> str:
    return f"qi_github_actions_dispatch_{target}_packet.json"


def _has_dispatch_result(root: pathlib.Path) -> tuple[bool, str]:
    for target, result_name in DISPATCH_RESULT_FILES.items():
        if _read_json(root / _dispatch_packet_name(target)) and _read_json(root / result_name):
            return True, target
    return False, "unknown"


def _has_dispatch_packet(root: pathlib.Path) -> tuple[bool, str]:
    for target in DISPATCH_RESULT_FILES:
        if _read_json(root / _dispatch_packet_name(target)):
            return True, target
    return False, "unknown"


def _select_stage(root: pathlib.Path) -> tuple[str, str]:
    if _read_json(root / "qi_github_actions_external_call_raw_result_packet.json"):
        return "external_result_adapt", "unknown"
    has_result, target = _has_dispatch_result(root)
    if has_result:
        return "dispatch_result_collect", target
    if _read_json(root / "qi_github_actions_external_call_packet.json"):
        has_dispatch, dispatch_target = _has_dispatch_packet(root)
        if has_dispatch:
            return "await_dispatch_result", dispatch_target
        return "external_call_dispatch", "unknown"
    if _read_json(root / "qi_github_actions_connector_execution_request.json") or _read_json(root / "qi_github_actions_observation_connector_request.json") or _read_json(root / "qi_github_actions_loop_command_packet.json"):
        return "external_wait_resolve", "unknown"
    return "await_external_call", "unknown"


def _wait_resolver_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_wait_resolver_enabled": True, "apply_github_actions_external_wait_resolver": True, "runtime_root": str(root)}


def _wait_resolver_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_LICENSE_READY",
        "wait_state_read_allowed": True,
        "external_call_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_await_connector_operation_stage": True,
        "allow_await_status_observation_stage": True,
    }


def _dispatcher_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_dispatcher_enabled": True, "apply_github_actions_external_call_dispatcher": True, "runtime_root": str(root)}


def _dispatcher_license() -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_LICENSE_READY",
        "external_call_packet_read_allowed": True,
        "dispatch_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    for target in DISPATCH_RESULT_FILES:
        value[f"allow_{target}_dispatch"] = True
    return value


def _collector_context(root: pathlib.Path, target: str) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_result_collector_enabled": True, "apply_github_actions_dispatch_result_collector": True, "runtime_root": str(root), "dispatch_target": target}


def _collector_license() -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_LICENSE_READY",
        "dispatch_packet_read_allowed": True,
        "dispatch_result_read_allowed": True,
        "raw_result_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    for target in DISPATCH_RESULT_FILES:
        value[f"allow_{target}_collect"] = True
    return value


def _adapter_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_result_adapter_enabled": True, "apply_github_actions_external_call_result_adapter": True, "runtime_root": str(root)}


def _adapter_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_LICENSE_READY",
        "external_call_packet_read_allowed": True,
        "raw_result_packet_read_allowed": True,
        "adapted_result_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_await_connector_operation_stage": True,
        "allow_await_status_observation_stage": True,
    }


def _run_stage(stage: str, root: pathlib.Path, target: str) -> Mapping[str, Any]:
    if stage == "external_wait_resolve":
        return build_qi_github_actions_external_wait_resolver(
            runtime_context=_wait_resolver_context(root),
            external_wait_resolver_license=_wait_resolver_license(),
        ).to_dict()
    if stage == "external_call_dispatch":
        return build_qi_github_actions_external_call_dispatcher(
            runtime_context=_dispatcher_context(root),
            external_call_dispatcher_license=_dispatcher_license(),
        ).to_dict()
    if stage == "dispatch_result_collect":
        return build_qi_github_actions_dispatch_result_collector(
            runtime_context=_collector_context(root, target),
            dispatch_result_collector_license=_collector_license(),
        ).to_dict()
    if stage == "external_result_adapt":
        return build_qi_github_actions_external_call_result_adapter(
            runtime_context=_adapter_context(root),
            result_adapter_license=_adapter_license(),
        ).to_dict()
    return {}


def build_qi_github_actions_external_bridge_executor(*, runtime_context: Mapping[str, Any], external_bridge_executor_license: Mapping[str, Any]) -> QiGitHubActionsExternalBridgeExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(external_bridge_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_external_bridge_executor_receipt.json"
    audit_path = root / "qi_github_actions_external_bridge_executor_audit.jsonl"

    if ctx.get("qi_github_actions_external_bridge_executor_enabled") is not True:
        blockers.append("qi_github_actions_external_bridge_executor_enabled_not_true")
    if ctx.get("apply_github_actions_external_bridge_executor") is not True:
        blockers.append("apply_github_actions_external_bridge_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_external_bridge_executor_license_not_ready")
    for name in ["external_bridge_state_read_allowed", "local_external_stage_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    stage, target = _select_stage(root)
    if stage not in LOCAL_EXTERNAL_STAGES:
        blockers.append("external_bridge_stage_not_allowlisted")
    if lic.get(f"allow_{stage}_stage") is not True:
        blockers.append(f"{stage}_not_allowed_by_external_bridge_executor_license")

    stage_result: Mapping[str, Any] = {}
    local_stage_performed = False
    stage_status = "NOT_RUN"
    stage_result_class = "not_run"
    if not blockers:
        if stage in {"await_dispatch_result", "await_external_call"}:
            stage_status = "WAITING"
            stage_result_class = stage
        else:
            stage_result = _run_stage(stage, root, target)
            local_stage_performed = True
            stage_status = str(stage_result.get("status", "unknown"))
            if stage_status.endswith("READY"):
                stage_result_class = "local_external_stage_completed"
            else:
                blockers.append("local_external_stage_not_ready")
                stage_result_class = "local_external_stage_blocked"

    status = "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-external-bridge-" + _sha({"stage": stage, "target": target, "stage_result": stage_result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_external_bridge_executor_v6_7",
        "status": status,
        "packet_id": packet_id,
        "selected_stage": stage,
        "dispatch_target": target,
        "stage_status": stage_status,
        "stage_result_class": stage_result_class,
        "local_stage_performed": local_stage_performed,
        "stage_result_digest": _sha(dict(stage_result)),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsExternalBridgeExecutorResult(
        "kuuos_runtime_daemon_qi_github_actions_external_bridge_executor_v6_7",
        status,
        packet_id,
        str(root),
        stage,
        stage_status,
        stage_result_class,
        str(receipt_path),
        str(audit_path),
        local_stage_performed,
        blockers,
        warnings,
    )

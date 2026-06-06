#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_action_dispatcher_v4_2 import build_qi_executable_action_dispatcher
from runtime.kuuos_runtime_daemon_qi_executable_action_sequence_runner_v4_3 import build_qi_executable_action_sequence_runner
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_compiler_v4_4 import build_qi_executable_action_recipe_compiler
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_executor_v4_5 import build_qi_executable_action_recipe_executor
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_batch_executor_v4_6 import build_qi_executable_action_recipe_batch_executor
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_batch_compiler_v4_7 import build_qi_executable_action_recipe_batch_compiler
from runtime.kuuos_runtime_daemon_qi_executable_action_batch_recipe_executor_v4_8 import build_qi_executable_action_batch_recipe_executor


CAPABILITY_INPUTS = {
    "action_dispatch": "qi_executable_action_packet.json",
    "action_sequence": "qi_executable_action_sequence_packet.json",
    "recipe_compile": "qi_executable_action_recipe_packet.json",
    "recipe_execute": "qi_executable_action_recipe_packet.json",
    "recipe_batch_execute": "qi_executable_action_recipe_batch_packet.json",
    "batch_recipe_compile": "qi_executable_action_recipe_batch_compiler_packet.json",
    "batch_recipe_execute": "qi_executable_action_recipe_batch_compiler_packet.json",
}


@dataclass(frozen=True)
class QiExecutableCapabilityRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    capability_kind: str
    delegated_status: str
    delegated_packet_id: str
    input_packet_path: str
    receipt_path: str
    audit_path: str
    delegated_performed: bool
    blockers: list[str]
    warnings: list[str]

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


def _ctx(root: pathlib.Path, enabled: str, apply_key: str, patch: Mapping[str, Any]) -> dict[str, Any]:
    out = {enabled: True, apply_key: True, "runtime_root": str(root)}
    for key, value in dict(_m(patch)).items():
        if key.startswith("max_") or key.startswith("base_max_"):
            out[key] = value
    return out


def _action_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    action = str(packet.get("action", "unknown"))
    return {
        "license_status": "QI_EXECUTABLE_ACTION_DISPATCHER_LICENSE_READY",
        "action_packet_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{action}_action": True,
    }


def _sequence_license() -> dict[str, Any]:
    return {"license_status": "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_LICENSE_READY", "sequence_packet_read_allowed": True, "action_packet_write_allowed": True, "dispatcher_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _recipe_compiler_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    recipe = str(packet.get("recipe", "unknown"))
    return {"license_status": "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_LICENSE_READY", "recipe_packet_read_allowed": True, "sequence_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{recipe}_recipe": True}


def _recipe_executor_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    recipe = str(packet.get("recipe", "unknown"))
    return {"license_status": "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_LICENSE_READY", "recipe_packet_read_allowed": True, "compiler_run_allowed": True, "sequence_runner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{recipe}_recipe": True}


def _batch_executor_license() -> dict[str, Any]:
    return {"license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_LICENSE_READY", "batch_packet_read_allowed": True, "recipe_packet_write_allowed": True, "recipe_executor_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _batch_compiler_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    batch_recipe = str(packet.get("batch_recipe", "unknown"))
    return {"license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_LICENSE_READY", "batch_compiler_packet_read_allowed": True, "batch_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{batch_recipe}_batch_recipe": True}


def _batch_recipe_executor_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    batch_recipe = str(packet.get("batch_recipe", "unknown"))
    return {"license_status": "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_LICENSE_READY", "batch_compiler_packet_read_allowed": True, "batch_compiler_run_allowed": True, "batch_executor_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{batch_recipe}_batch_recipe": True}


def _dispatch(kind: str, root: pathlib.Path, input_packet: Mapping[str, Any], patch: Mapping[str, Any]) -> Mapping[str, Any]:
    if kind == "action_dispatch":
        return build_qi_executable_action_dispatcher(
            runtime_context=_ctx(root, "qi_executable_action_dispatcher_enabled", "apply_executable_action_dispatcher", patch),
            dispatcher_license=_action_license(input_packet),
        ).to_dict()
    if kind == "action_sequence":
        return build_qi_executable_action_sequence_runner(
            runtime_context=_ctx(root, "qi_executable_action_sequence_runner_enabled", "apply_executable_action_sequence_runner", patch),
            sequence_runner_license=_sequence_license(),
        ).to_dict()
    if kind == "recipe_compile":
        return build_qi_executable_action_recipe_compiler(
            runtime_context=_ctx(root, "qi_executable_action_recipe_compiler_enabled", "apply_executable_action_recipe_compiler", patch),
            recipe_compiler_license=_recipe_compiler_license(input_packet),
        ).to_dict()
    if kind == "recipe_execute":
        return build_qi_executable_action_recipe_executor(
            runtime_context=_ctx(root, "qi_executable_action_recipe_executor_enabled", "apply_executable_action_recipe_executor", patch),
            recipe_executor_license=_recipe_executor_license(input_packet),
        ).to_dict()
    if kind == "recipe_batch_execute":
        return build_qi_executable_action_recipe_batch_executor(
            runtime_context=_ctx(root, "qi_executable_action_recipe_batch_executor_enabled", "apply_executable_action_recipe_batch_executor", patch),
            batch_executor_license=_batch_executor_license(),
        ).to_dict()
    if kind == "batch_recipe_compile":
        return build_qi_executable_action_recipe_batch_compiler(
            runtime_context=_ctx(root, "qi_executable_action_recipe_batch_compiler_enabled", "apply_executable_action_recipe_batch_compiler", patch),
            batch_compiler_license=_batch_compiler_license(input_packet),
        ).to_dict()
    if kind == "batch_recipe_execute":
        return build_qi_executable_action_batch_recipe_executor(
            runtime_context=_ctx(root, "qi_executable_action_batch_recipe_executor_enabled", "apply_executable_action_batch_recipe_executor", patch),
            batch_recipe_executor_license=_batch_recipe_executor_license(input_packet),
        ).to_dict()
    raise ValueError(f"unsupported capability kind: {kind}")


def build_qi_executable_capability_router(*, runtime_context: Mapping[str, Any], capability_router_license: Mapping[str, Any]) -> QiExecutableCapabilityRouterResult:
    ctx = _m(runtime_context)
    lic = _m(capability_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    cap_path = root / "qi_executable_capability_packet.json"
    receipt_path = root / "qi_executable_capability_router_receipt.json"
    audit_path = root / "qi_executable_capability_router_audit.jsonl"

    if ctx.get("qi_executable_capability_router_enabled") is not True:
        blockers.append("qi_executable_capability_router_enabled_not_true")
    if ctx.get("apply_executable_capability_router") is not True:
        blockers.append("apply_executable_capability_router_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_CAPABILITY_ROUTER_LICENSE_READY":
        blockers.append("executable_capability_router_license_not_ready")
    for name in ["capability_packet_read_allowed", "delegated_packet_write_allowed", "delegated_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    cap_packet = _read_json(cap_path)
    if not cap_packet:
        blockers.append("capability_packet_missing_or_invalid")
    kind = str(cap_packet.get("capability_kind", "unknown")) if cap_packet else "unknown"
    if kind not in CAPABILITY_INPUTS:
        blockers.append("capability_kind_not_allowlisted")
    if cap_packet and cap_packet.get("capability_allowed") is not True:
        blockers.append("capability_packet_allowed_not_true")
    if lic.get(f"allow_{kind}_capability") is not True:
        blockers.append(f"{kind}_not_allowed_by_router_license")
    delegated_input = dict(_m(cap_packet.get("delegated_input_packet")))
    if cap_packet and not delegated_input:
        blockers.append("delegated_input_packet_missing_or_invalid")
    input_path = root / CAPABILITY_INPUTS.get(kind, "qi_executable_capability_unknown.json")

    delegated: Mapping[str, Any] = {}
    delegated_performed = False
    if not blockers:
        _write_json(input_path, delegated_input)
        delegated = _dispatch(kind, root, delegated_input, _m(cap_packet.get("runtime_context_patch")))
        delegated_performed = True
        if str(delegated.get("status", "unknown")).endswith("READY") is not True:
            blockers.append("delegated_capability_not_ready")
    status = "QI_EXECUTABLE_CAPABILITY_ROUTER_READY" if not blockers else "QI_EXECUTABLE_CAPABILITY_ROUTER_BLOCKED"
    packet_id = "qi-executable-capability-router-" + _sha({"capability": cap_packet, "delegated": delegated, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_capability_router_v4_9",
        "status": status,
        "packet_id": packet_id,
        "capability_kind": kind,
        "delegated_status": str(delegated.get("status", "unknown")),
        "delegated_packet_id": str(delegated.get("packet_id", "unknown")),
        "input_packet_path": str(input_path),
        "delegated_performed": delegated_performed,
        "delegated_digest": _sha(delegated),
        "available_capabilities": sorted(CAPABILITY_INPUTS),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableCapabilityRouterResult(
        "kuuos_runtime_daemon_qi_executable_capability_router_v4_9",
        status,
        packet_id,
        str(root),
        kind,
        str(delegated.get("status", "unknown")),
        str(delegated.get("packet_id", "unknown")),
        str(input_path),
        str(receipt_path),
        str(audit_path),
        delegated_performed,
        blockers,
        warnings,
    )

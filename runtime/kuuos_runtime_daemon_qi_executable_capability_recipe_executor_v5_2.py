#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_capability_recipe_compiler_v5_1 import CAPABILITY_RECIPES, build_qi_executable_capability_recipe_compiler
from runtime.kuuos_runtime_daemon_qi_executable_capability_sequence_runner_v5_0 import build_qi_executable_capability_sequence_runner


@dataclass(frozen=True)
class QiExecutableCapabilityRecipeExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    capability_recipe: str
    compile_status: str
    sequence_status: str
    sequence_length: int
    capabilities_run: int
    executor_completed: bool
    receipt_path: str
    audit_path: str
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


def _compiler_context(root: pathlib.Path, max_compiled: int) -> dict[str, Any]:
    return {
        "qi_executable_capability_recipe_compiler_enabled": True,
        "apply_executable_capability_recipe_compiler": True,
        "runtime_root": str(root),
        "max_compiled_capability_sequence": max_compiled,
    }


def _compiler_license(recipe: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_LICENSE_READY",
        "capability_recipe_packet_read_allowed": True,
        "capability_sequence_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{recipe}_capability_recipe": True,
    }


def _sequence_context(root: pathlib.Path, max_sequence: int) -> dict[str, Any]:
    return {
        "qi_executable_capability_sequence_runner_enabled": True,
        "apply_executable_capability_sequence_runner": True,
        "runtime_root": str(root),
        "max_capability_sequence": max_sequence,
    }


def _sequence_license() -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_LICENSE_READY",
        "sequence_packet_read_allowed": True,
        "capability_packet_write_allowed": True,
        "capability_router_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_executable_capability_recipe_executor(*, runtime_context: Mapping[str, Any], capability_recipe_executor_license: Mapping[str, Any]) -> QiExecutableCapabilityRecipeExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(capability_recipe_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    recipe_packet_path = root / "qi_executable_capability_recipe_packet.json"
    receipt_path = root / "qi_executable_capability_recipe_executor_receipt.json"
    audit_path = root / "qi_executable_capability_recipe_executor_audit.jsonl"

    if ctx.get("qi_executable_capability_recipe_executor_enabled") is not True:
        blockers.append("qi_executable_capability_recipe_executor_enabled_not_true")
    if ctx.get("apply_executable_capability_recipe_executor") is not True:
        blockers.append("apply_executable_capability_recipe_executor_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_LICENSE_READY":
        blockers.append("executable_capability_recipe_executor_license_not_ready")
    for name in ["capability_recipe_packet_read_allowed", "capability_recipe_compiler_run_allowed", "capability_sequence_runner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(recipe_packet_path)
    if not packet:
        blockers.append("capability_recipe_packet_missing_or_invalid")
    recipe = str(packet.get("capability_recipe", "unknown")) if packet else "unknown"
    if recipe not in CAPABILITY_RECIPES:
        blockers.append("capability_recipe_not_allowlisted")
    if packet and packet.get("capability_recipe_allowed") is not True:
        blockers.append("capability_recipe_packet_allowed_not_true")
    if lic.get(f"allow_{recipe}_capability_recipe") is not True:
        blockers.append(f"{recipe}_not_allowed_by_capability_recipe_executor_license")

    max_compiled = _i(ctx.get("max_compiled_capability_sequence", packet.get("max_compiled_capability_sequence", 5) if packet else 5), 5)
    max_sequence = _i(ctx.get("max_capability_sequence", packet.get("max_capability_sequence", max_compiled) if packet else max_compiled), max_compiled)

    compile_payload: Mapping[str, Any] = {}
    sequence_payload: Mapping[str, Any] = {}
    compile_status = "NOT_RUN"
    sequence_status = "NOT_RUN"
    sequence_length = 0
    capabilities_run = 0

    if not blockers:
        compile_payload = build_qi_executable_capability_recipe_compiler(
            runtime_context=_compiler_context(root, max_compiled),
            capability_recipe_compiler_license=_compiler_license(recipe),
        ).to_dict()
        compile_status = str(compile_payload.get("status", "unknown"))
        sequence_length = _i(compile_payload.get("sequence_length"), 0)
        if compile_status != "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY":
            blockers.append("capability_recipe_compiler_not_ready")

    if not blockers:
        sequence_payload = build_qi_executable_capability_sequence_runner(
            runtime_context=_sequence_context(root, max_sequence),
            sequence_runner_license=_sequence_license(),
        ).to_dict()
        sequence_status = str(sequence_payload.get("status", "unknown"))
        capabilities_run = _i(sequence_payload.get("capabilities_run"), 0)
        if sequence_status != "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY":
            blockers.append("capability_sequence_runner_not_ready")

    executor_completed = not blockers and compile_status == "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY" and sequence_status == "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY"
    status = "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_READY" if executor_completed else "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_BLOCKED"
    packet_id = "qi-executable-capability-recipe-executor-" + _sha({"packet": packet, "compile": compile_payload, "sequence": sequence_payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_capability_recipe_executor_v5_2",
        "status": status,
        "packet_id": packet_id,
        "capability_recipe": recipe,
        "compile_status": compile_status,
        "sequence_status": sequence_status,
        "sequence_length": sequence_length,
        "capabilities_run": capabilities_run,
        "executor_completed": executor_completed,
        "compile_digest": _sha(compile_payload),
        "sequence_digest": _sha(sequence_payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableCapabilityRecipeExecutorResult(
        "kuuos_runtime_daemon_qi_executable_capability_recipe_executor_v5_2",
        status,
        packet_id,
        str(root),
        recipe,
        compile_status,
        sequence_status,
        sequence_length,
        capabilities_run,
        executor_completed,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

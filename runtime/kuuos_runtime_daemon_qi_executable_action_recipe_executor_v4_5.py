#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_compiler_v4_4 import RECIPES, build_qi_executable_action_recipe_compiler
from runtime.kuuos_runtime_daemon_qi_executable_action_sequence_runner_v4_3 import build_qi_executable_action_sequence_runner


@dataclass(frozen=True)
class QiExecutableActionRecipeExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    recipe: str
    compile_status: str
    sequence_status: str
    sequence_length: int
    actions_run: int
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


def _compiler_context(root: pathlib.Path, max_compiled_actions: int) -> dict[str, Any]:
    return {
        "qi_executable_action_recipe_compiler_enabled": True,
        "apply_executable_action_recipe_compiler": True,
        "runtime_root": str(root),
        "max_compiled_actions": max_compiled_actions,
    }


def _compiler_license(recipe: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_LICENSE_READY",
        "recipe_packet_read_allowed": True,
        "sequence_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{recipe}_recipe": True,
    }


def _sequence_context(root: pathlib.Path, max_sequence_actions: int) -> dict[str, Any]:
    return {
        "qi_executable_action_sequence_runner_enabled": True,
        "apply_executable_action_sequence_runner": True,
        "runtime_root": str(root),
        "max_sequence_actions": max_sequence_actions,
    }


def _sequence_license() -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_LICENSE_READY",
        "sequence_packet_read_allowed": True,
        "action_packet_write_allowed": True,
        "dispatcher_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_executable_action_recipe_executor(*, runtime_context: Mapping[str, Any], recipe_executor_license: Mapping[str, Any]) -> QiExecutableActionRecipeExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(recipe_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    recipe_packet_path = root / "qi_executable_action_recipe_packet.json"
    receipt_path = root / "qi_executable_action_recipe_executor_receipt.json"
    audit_path = root / "qi_executable_action_recipe_executor_audit.jsonl"

    if ctx.get("qi_executable_action_recipe_executor_enabled") is not True:
        blockers.append("qi_executable_action_recipe_executor_enabled_not_true")
    if ctx.get("apply_executable_action_recipe_executor") is not True:
        blockers.append("apply_executable_action_recipe_executor_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_LICENSE_READY":
        blockers.append("executable_action_recipe_executor_license_not_ready")
    for name in ["recipe_packet_read_allowed", "compiler_run_allowed", "sequence_runner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(recipe_packet_path)
    if not packet:
        blockers.append("recipe_packet_missing_or_invalid")
    recipe = str(packet.get("recipe", "unknown")) if packet else "unknown"
    if recipe not in RECIPES:
        blockers.append("recipe_not_allowlisted")
    if packet and packet.get("recipe_allowed") is not True:
        blockers.append("recipe_packet_recipe_allowed_not_true")
    if lic.get(f"allow_{recipe}_recipe") is not True:
        blockers.append(f"{recipe}_not_allowed_by_executor_license")
    max_compiled_actions = _i(ctx.get("max_compiled_actions", packet.get("max_compiled_actions", 5) if packet else 5), 5)
    max_sequence_actions = _i(ctx.get("max_sequence_actions", packet.get("max_sequence_actions", max_compiled_actions) if packet else max_compiled_actions), max_compiled_actions)

    compile_payload: Mapping[str, Any] = {}
    sequence_payload: Mapping[str, Any] = {}
    compile_status = "NOT_RUN"
    sequence_status = "NOT_RUN"
    sequence_length = 0
    actions_run = 0

    if not blockers:
        compile_payload = build_qi_executable_action_recipe_compiler(
            runtime_context=_compiler_context(root, max_compiled_actions),
            recipe_compiler_license=_compiler_license(recipe),
        ).to_dict()
        compile_status = str(compile_payload.get("status", "unknown"))
        sequence_length = _i(compile_payload.get("sequence_length"), 0)
        if compile_status != "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY":
            blockers.append("recipe_compiler_not_ready")

    if not blockers:
        sequence_payload = build_qi_executable_action_sequence_runner(
            runtime_context=_sequence_context(root, max_sequence_actions),
            sequence_runner_license=_sequence_license(),
        ).to_dict()
        sequence_status = str(sequence_payload.get("status", "unknown"))
        actions_run = _i(sequence_payload.get("actions_run"), 0)
        if sequence_status != "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_READY":
            blockers.append("action_sequence_runner_not_ready")

    executor_completed = not blockers and compile_status == "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY" and sequence_status == "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_READY"
    status = "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_READY" if executor_completed else "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_BLOCKED"
    packet_id = "qi-executable-action-recipe-executor-" + _sha({"packet": packet, "compile": compile_payload, "sequence": sequence_payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_recipe_executor_v4_5",
        "status": status,
        "packet_id": packet_id,
        "recipe": recipe,
        "compile_status": compile_status,
        "sequence_status": sequence_status,
        "sequence_length": sequence_length,
        "actions_run": actions_run,
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
    return QiExecutableActionRecipeExecutorResult(
        "kuuos_runtime_daemon_qi_executable_action_recipe_executor_v4_5",
        status,
        packet_id,
        str(root),
        recipe,
        compile_status,
        sequence_status,
        sequence_length,
        actions_run,
        executor_completed,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

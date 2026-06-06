#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_batch_compiler_v4_7 import BATCH_RECIPES, build_qi_executable_action_recipe_batch_compiler
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_batch_executor_v4_6 import build_qi_executable_action_recipe_batch_executor


@dataclass(frozen=True)
class QiExecutableActionBatchRecipeExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    batch_recipe: str
    compile_status: str
    batch_status: str
    batch_length: int
    recipes_run: int
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


def _compiler_context(root: pathlib.Path, max_compiled_batch_recipes: int) -> dict[str, Any]:
    return {
        "qi_executable_action_recipe_batch_compiler_enabled": True,
        "apply_executable_action_recipe_batch_compiler": True,
        "runtime_root": str(root),
        "max_compiled_batch_recipes": max_compiled_batch_recipes,
    }


def _compiler_license(batch_recipe: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_LICENSE_READY",
        "batch_compiler_packet_read_allowed": True,
        "batch_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{batch_recipe}_batch_recipe": True,
    }


def _batch_context(root: pathlib.Path, max_batch_recipes: int, max_compiled_actions: int, max_sequence_actions: int) -> dict[str, Any]:
    return {
        "qi_executable_action_recipe_batch_executor_enabled": True,
        "apply_executable_action_recipe_batch_executor": True,
        "runtime_root": str(root),
        "max_batch_recipes": max_batch_recipes,
        "max_compiled_actions": max_compiled_actions,
        "max_sequence_actions": max_sequence_actions,
    }


def _batch_license() -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_LICENSE_READY",
        "batch_packet_read_allowed": True,
        "recipe_packet_write_allowed": True,
        "recipe_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_executable_action_batch_recipe_executor(*, runtime_context: Mapping[str, Any], batch_recipe_executor_license: Mapping[str, Any]) -> QiExecutableActionBatchRecipeExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(batch_recipe_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    compiler_packet_path = root / "qi_executable_action_recipe_batch_compiler_packet.json"
    receipt_path = root / "qi_executable_action_batch_recipe_executor_receipt.json"
    audit_path = root / "qi_executable_action_batch_recipe_executor_audit.jsonl"

    if ctx.get("qi_executable_action_batch_recipe_executor_enabled") is not True:
        blockers.append("qi_executable_action_batch_recipe_executor_enabled_not_true")
    if ctx.get("apply_executable_action_batch_recipe_executor") is not True:
        blockers.append("apply_executable_action_batch_recipe_executor_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_LICENSE_READY":
        blockers.append("executable_action_batch_recipe_executor_license_not_ready")
    for name in ["batch_compiler_packet_read_allowed", "batch_compiler_run_allowed", "batch_executor_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(compiler_packet_path)
    if not packet:
        blockers.append("batch_compiler_packet_missing_or_invalid")
    batch_recipe = str(packet.get("batch_recipe", "unknown")) if packet else "unknown"
    if batch_recipe not in BATCH_RECIPES:
        blockers.append("batch_recipe_not_allowlisted")
    if packet and packet.get("batch_recipe_allowed") is not True:
        blockers.append("batch_recipe_packet_allowed_not_true")
    if lic.get(f"allow_{batch_recipe}_batch_recipe") is not True:
        blockers.append(f"{batch_recipe}_not_allowed_by_batch_recipe_executor_license")

    max_compiled_batch_recipes = _i(ctx.get("max_compiled_batch_recipes", packet.get("max_compiled_batch_recipes", 5) if packet else 5), 5)
    max_batch_recipes = _i(ctx.get("max_batch_recipes", packet.get("max_batch_recipes", max_compiled_batch_recipes) if packet else max_compiled_batch_recipes), max_compiled_batch_recipes)
    max_compiled_actions = _i(ctx.get("max_compiled_actions", 5), 5)
    max_sequence_actions = _i(ctx.get("max_sequence_actions", 5), 5)

    compile_payload: Mapping[str, Any] = {}
    batch_payload: Mapping[str, Any] = {}
    compile_status = "NOT_RUN"
    batch_status = "NOT_RUN"
    batch_length = 0
    recipes_run = 0

    if not blockers:
        compile_payload = build_qi_executable_action_recipe_batch_compiler(
            runtime_context=_compiler_context(root, max_compiled_batch_recipes),
            batch_compiler_license=_compiler_license(batch_recipe),
        ).to_dict()
        compile_status = str(compile_payload.get("status", "unknown"))
        batch_length = _i(compile_payload.get("batch_length"), 0)
        if compile_status != "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY":
            blockers.append("batch_recipe_compiler_not_ready")

    if not blockers:
        batch_payload = build_qi_executable_action_recipe_batch_executor(
            runtime_context=_batch_context(root, max_batch_recipes, max_compiled_actions, max_sequence_actions),
            batch_executor_license=_batch_license(),
        ).to_dict()
        batch_status = str(batch_payload.get("status", "unknown"))
        recipes_run = _i(batch_payload.get("recipes_run"), 0)
        if batch_status != "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY":
            blockers.append("recipe_batch_executor_not_ready")

    executor_completed = not blockers and compile_status == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY" and batch_status == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY"
    status = "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_READY" if executor_completed else "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_BLOCKED"
    packet_id = "qi-executable-action-batch-recipe-executor-" + _sha({"packet": packet, "compile": compile_payload, "batch": batch_payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_batch_recipe_executor_v4_8",
        "status": status,
        "packet_id": packet_id,
        "batch_recipe": batch_recipe,
        "compile_status": compile_status,
        "batch_status": batch_status,
        "batch_length": batch_length,
        "recipes_run": recipes_run,
        "executor_completed": executor_completed,
        "compile_digest": _sha(compile_payload),
        "batch_digest": _sha(batch_payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableActionBatchRecipeExecutorResult(
        "kuuos_runtime_daemon_qi_executable_action_batch_recipe_executor_v4_8",
        status,
        packet_id,
        str(root),
        batch_recipe,
        compile_status,
        batch_status,
        batch_length,
        recipes_run,
        executor_completed,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )

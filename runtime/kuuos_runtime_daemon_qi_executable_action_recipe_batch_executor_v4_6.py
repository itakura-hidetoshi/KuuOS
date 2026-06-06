#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_compiler_v4_4 import RECIPES
from runtime.kuuos_runtime_daemon_qi_executable_action_recipe_executor_v4_5 import build_qi_executable_action_recipe_executor


@dataclass(frozen=True)
class QiExecutableActionRecipeBatchExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    batch_length: int
    recipes_run: int
    stop_reason: str
    receipt_path: str
    audit_path: str
    batch_completed: bool
    blockers: list[str]
    warnings: list[str]
    recipe_records: list[dict[str, Any]]

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


def _batch(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("batch", [])
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, str):
            out.append({"recipe": item, "recipe_allowed": True})
        elif isinstance(item, Mapping):
            out.append(dict(item))
    return out


def _executor_context(root: pathlib.Path, item: Mapping[str, Any], batch_context: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_executable_action_recipe_executor_enabled": True,
        "apply_executable_action_recipe_executor": True,
        "runtime_root": str(root),
        "max_compiled_actions": _i(item.get("max_compiled_actions", batch_context.get("max_compiled_actions", 5)), 5),
        "max_sequence_actions": _i(item.get("max_sequence_actions", batch_context.get("max_sequence_actions", 5)), 5),
    }


def _executor_license(recipe: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_LICENSE_READY",
        "recipe_packet_read_allowed": True,
        "compiler_run_allowed": True,
        "sequence_runner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{recipe}_recipe": True,
    }


def _recipe_record(index: int, recipe: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "recipe": recipe,
        "status": str(payload.get("status", "unknown")),
        "compile_status": str(payload.get("compile_status", "unknown")),
        "sequence_status": str(payload.get("sequence_status", "unknown")),
        "sequence_length": _i(payload.get("sequence_length"), 0),
        "actions_run": _i(payload.get("actions_run"), 0),
        "packet_id": str(payload.get("packet_id", "unknown")),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def build_qi_executable_action_recipe_batch_executor(*, runtime_context: Mapping[str, Any], batch_executor_license: Mapping[str, Any]) -> QiExecutableActionRecipeBatchExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(batch_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    batch_packet_path = root / "qi_executable_action_recipe_batch_packet.json"
    recipe_packet_path = root / "qi_executable_action_recipe_packet.json"
    receipt_path = root / "qi_executable_action_recipe_batch_executor_receipt.json"
    audit_path = root / "qi_executable_action_recipe_batch_executor_audit.jsonl"

    if ctx.get("qi_executable_action_recipe_batch_executor_enabled") is not True:
        blockers.append("qi_executable_action_recipe_batch_executor_enabled_not_true")
    if ctx.get("apply_executable_action_recipe_batch_executor") is not True:
        blockers.append("apply_executable_action_recipe_batch_executor_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_LICENSE_READY":
        blockers.append("executable_action_recipe_batch_executor_license_not_ready")
    for name in ["batch_packet_read_allowed", "recipe_packet_write_allowed", "recipe_executor_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(batch_packet_path)
    if not packet:
        blockers.append("batch_packet_missing_or_invalid")
    if packet and packet.get("batch_allowed") is not True:
        blockers.append("batch_packet_batch_allowed_not_true")
    items = _batch(packet)
    if packet and not items:
        blockers.append("batch_empty_or_invalid")
    cap = _i(ctx.get("max_batch_recipes", packet.get("max_batch_recipes", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_batch_recipes_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_batch_recipes_capped_to_20")
        cap = 20
    if len(items) > cap:
        blockers.append("batch_exceeds_cap")

    recipe_records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    if not blockers:
        stop_reason = "batch_completed"
        for index, item in enumerate(items, start=1):
            recipe = str(item.get("recipe", "unknown"))
            if recipe not in RECIPES:
                blockers.append("recipe_not_allowlisted")
                stop_reason = "blocked"
                break
            if item.get("recipe_allowed") is not True:
                blockers.append("recipe_packet_recipe_allowed_not_true")
                stop_reason = "blocked"
                break
            recipe_packet = {
                "recipe": recipe,
                "recipe_allowed": True,
                "max_compiled_actions": _i(item.get("max_compiled_actions", ctx.get("max_compiled_actions", 5)), 5),
                "max_sequence_actions": _i(item.get("max_sequence_actions", ctx.get("max_sequence_actions", 5)), 5),
                "default_action_context_patch": dict(_m(item.get("default_action_context_patch"))),
                "action_context_patch_by_action": dict(_m(item.get("action_context_patch_by_action"))),
                "batch_index": index,
                "batch_source": "qi_executable_action_recipe_batch_executor_v4_6",
            }
            _write_json(recipe_packet_path, recipe_packet)
            result = build_qi_executable_action_recipe_executor(
                runtime_context=_executor_context(root, item, ctx),
                recipe_executor_license=_executor_license(recipe),
            ).to_dict()
            recipe_records.append(_recipe_record(index, recipe, result))
            if result.get("status") != "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_READY":
                blockers.append("delegated_recipe_executor_blocked")
                stop_reason = "blocked"
                break

    batch_completed = not blockers and len(recipe_records) == len(items)
    status = "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY" if batch_completed else "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_BLOCKED"
    packet_id = "qi-executable-action-recipe-batch-" + _sha({"packet": packet, "records": recipe_records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_recipe_batch_executor_v4_6",
        "status": status,
        "packet_id": packet_id,
        "batch_length": len(items),
        "recipes_run": len(recipe_records),
        "stop_reason": stop_reason,
        "batch_completed": batch_completed,
        "recipe_records": recipe_records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableActionRecipeBatchExecutorResult(
        "kuuos_runtime_daemon_qi_executable_action_recipe_batch_executor_v4_6",
        status,
        packet_id,
        str(root),
        len(items),
        len(recipe_records),
        stop_reason,
        str(receipt_path),
        str(audit_path),
        batch_completed,
        blockers,
        warnings,
        recipe_records,
    )

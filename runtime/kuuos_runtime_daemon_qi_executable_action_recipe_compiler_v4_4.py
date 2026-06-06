#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


RECIPES: dict[str, list[str]] = {
    "observe_and_adapt": [
        "cycle_trend_summary",
        "trend_adaptive_supervisor_packet",
    ],
    "observe_adapt_and_run": [
        "cycle_trend_summary",
        "trend_adaptive_supervisor_packet",
        "trend_adaptive_supervisor_run",
    ],
    "supervise_then_summarize": [
        "cycle_supervisor",
        "cycle_trend_summary",
    ],
    "single_cycle_then_summarize": [
        "cycle_runner",
        "cycle_trend_summary",
    ],
    "return_loop_then_cycle": [
        "return_loop",
        "cycle_runner",
    ],
}


@dataclass(frozen=True)
class QiExecutableActionRecipeCompilerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    recipe: str
    sequence_length: int
    sequence_packet_path: str
    receipt_path: str
    audit_path: str
    write_performed: bool
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


def _compile_actions(recipe: str, patch_by_action: Mapping[str, Any], default_patch: Mapping[str, Any]) -> list[dict[str, Any]]:
    actions = RECIPES[recipe]
    compiled: list[dict[str, Any]] = []
    for action in actions:
        patch = dict(_m(default_patch))
        specific = _m(patch_by_action.get(action)) if isinstance(patch_by_action, Mapping) else {}
        patch.update(dict(specific))
        compiled.append({
            "action": action,
            "action_allowed": True,
            "action_context_patch": patch,
            "recipe_source": recipe,
        })
    return compiled


def _sequence_packet(recipe: str, actions: list[dict[str, Any]], cap: int, recipe_packet: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_executable_action_sequence_packet_from_recipe_v4_4",
        "sequence_allowed": True,
        "recipe": recipe,
        "sequence": actions,
        "max_sequence_actions": cap,
        "compiled_from": "qi_executable_action_recipe_compiler_v4_4",
        "source_digest": _sha(dict(recipe_packet)),
        "boundary": {
            "compiled_sequence_only": True,
            "does_not_execute_actions": True,
            "requires_v4_3_sequence_runner": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_executable_action_recipe_compiler(*, runtime_context: Mapping[str, Any], recipe_compiler_license: Mapping[str, Any]) -> QiExecutableActionRecipeCompilerResult:
    ctx = _m(runtime_context)
    lic = _m(recipe_compiler_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    recipe_packet_path = root / "qi_executable_action_recipe_packet.json"
    sequence_packet_path = root / "qi_executable_action_sequence_packet.json"
    receipt_path = root / "qi_executable_action_recipe_compiler_receipt.json"
    audit_path = root / "qi_executable_action_recipe_compiler_audit.jsonl"
    if ctx.get("qi_executable_action_recipe_compiler_enabled") is not True:
        blockers.append("qi_executable_action_recipe_compiler_enabled_not_true")
    if ctx.get("apply_executable_action_recipe_compiler") is not True:
        blockers.append("apply_executable_action_recipe_compiler_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_LICENSE_READY":
        blockers.append("executable_action_recipe_compiler_license_not_ready")
    for name in ["recipe_packet_read_allowed", "sequence_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(recipe_packet_path)
    if not packet:
        blockers.append("recipe_packet_missing_or_invalid")
    if packet and packet.get("recipe_allowed") is not True:
        blockers.append("recipe_packet_recipe_allowed_not_true")
    recipe = str(packet.get("recipe", "unknown")) if packet else "unknown"
    if recipe not in RECIPES:
        blockers.append("recipe_not_allowlisted")
    if lic.get(f"allow_{recipe}_recipe") is not True:
        blockers.append(f"{recipe}_not_allowed_by_compiler_license")
    cap = _i(ctx.get("max_compiled_actions", packet.get("max_compiled_actions", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_compiled_actions_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_compiled_actions_capped_to_20")
        cap = 20
    actions: list[dict[str, Any]] = []
    sequence_payload: dict[str, Any] = {}
    if recipe in RECIPES:
        actions = _compile_actions(recipe, _m(packet.get("action_context_patch_by_action")), _m(packet.get("default_action_context_patch")))
        if len(actions) > cap:
            blockers.append("compiled_sequence_exceeds_cap")
        sequence_payload = _sequence_packet(recipe, actions, cap, packet)
    write_performed = False
    if not blockers:
        _write_json(sequence_packet_path, sequence_payload)
        write_performed = True
    status = "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY" if not blockers else "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_BLOCKED"
    packet_id = "qi-executable-action-recipe-" + _sha({"packet": packet, "sequence": sequence_payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_recipe_compiler_v4_4",
        "status": status,
        "packet_id": packet_id,
        "recipe": recipe,
        "sequence_length": len(actions),
        "write_performed": write_performed,
        "sequence_packet_digest": _sha(sequence_payload),
        "available_recipes": sorted(RECIPES),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableActionRecipeCompilerResult(
        "kuuos_runtime_daemon_qi_executable_action_recipe_compiler_v4_4",
        status,
        packet_id,
        str(root),
        recipe,
        len(actions),
        str(sequence_packet_path),
        str(receipt_path),
        str(audit_path),
        write_performed,
        blockers,
        warnings,
    )

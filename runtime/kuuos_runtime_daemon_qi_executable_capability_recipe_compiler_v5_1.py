#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_capability_router_v4_9 import CAPABILITY_INPUTS


CAPABILITY_RECIPES: dict[str, list[dict[str, Any]]] = {
    "compile_recipe_and_batch": [
        {"capability_kind": "recipe_compile", "delegated_input_packet": {"recipe": "observe_and_adapt", "recipe_allowed": True}},
        {"capability_kind": "batch_recipe_compile", "delegated_input_packet": {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}},
    ],
    "compile_then_execute_recipe": [
        {"capability_kind": "recipe_compile", "delegated_input_packet": {"recipe": "observe_and_adapt", "recipe_allowed": True}},
        {"capability_kind": "recipe_execute", "delegated_input_packet": {"recipe": "observe_and_adapt", "recipe_allowed": True}},
    ],
    "compile_batch_then_execute_batch": [
        {"capability_kind": "batch_recipe_compile", "delegated_input_packet": {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}},
        {"capability_kind": "batch_recipe_execute", "delegated_input_packet": {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}},
    ],
    "route_observe_then_compile": [
        {"capability_kind": "action_dispatch", "delegated_input_packet": {"action": "cycle_trend_summary", "action_allowed": True}},
        {"capability_kind": "recipe_compile", "delegated_input_packet": {"recipe": "observe_and_adapt", "recipe_allowed": True}},
    ],
    "safe_compile_full_surface": [
        {"capability_kind": "recipe_compile", "delegated_input_packet": {"recipe": "observe_and_adapt", "recipe_allowed": True}},
        {"capability_kind": "batch_recipe_compile", "delegated_input_packet": {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}},
        {"capability_kind": "batch_recipe_compile", "delegated_input_packet": {"batch_recipe": "safe_full_observe_adapt_run", "batch_recipe_allowed": True}},
    ],
}


@dataclass(frozen=True)
class QiExecutableCapabilityRecipeCompilerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    capability_recipe: str
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


def _deep_merge(base: Mapping[str, Any], overlay: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in overlay.items():
        if isinstance(out.get(key), dict) and isinstance(value, Mapping):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def _compile_sequence(recipe: str, packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    default_context = dict(_m(packet.get("default_runtime_context_patch")))
    context_by_kind = _m(packet.get("runtime_context_patch_by_capability"))
    input_overrides = _m(packet.get("delegated_input_patch_by_capability"))
    sequence: list[dict[str, Any]] = []
    for item in CAPABILITY_RECIPES[recipe]:
        kind = str(item["capability_kind"])
        delegated = dict(_m(item.get("delegated_input_packet")))
        override = _m(input_overrides.get(kind)) if isinstance(input_overrides, Mapping) else {}
        delegated = _deep_merge(delegated, override)
        context = dict(default_context)
        specific_context = _m(context_by_kind.get(kind)) if isinstance(context_by_kind, Mapping) else {}
        context.update(dict(specific_context))
        sequence.append({
            "capability_kind": kind,
            "capability_allowed": True,
            "delegated_input_packet": delegated,
            "runtime_context_patch": context,
            "capability_recipe_source": recipe,
        })
    return sequence


def _sequence_packet(recipe: str, sequence: list[dict[str, Any]], cap: int, source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_executable_capability_sequence_packet_from_recipe_v5_1",
        "sequence_allowed": True,
        "capability_recipe": recipe,
        "sequence": sequence,
        "max_capability_sequence": cap,
        "compiled_from": "qi_executable_capability_recipe_compiler_v5_1",
        "source_digest": _sha(dict(source)),
        "boundary": {
            "compiled_sequence_only": True,
            "does_not_execute_capabilities": True,
            "requires_v5_0_capability_sequence_runner": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_executable_capability_recipe_compiler(*, runtime_context: Mapping[str, Any], capability_recipe_compiler_license: Mapping[str, Any]) -> QiExecutableCapabilityRecipeCompilerResult:
    ctx = _m(runtime_context)
    lic = _m(capability_recipe_compiler_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    recipe_packet_path = root / "qi_executable_capability_recipe_packet.json"
    sequence_packet_path = root / "qi_executable_capability_sequence_packet.json"
    receipt_path = root / "qi_executable_capability_recipe_compiler_receipt.json"
    audit_path = root / "qi_executable_capability_recipe_compiler_audit.jsonl"

    if ctx.get("qi_executable_capability_recipe_compiler_enabled") is not True:
        blockers.append("qi_executable_capability_recipe_compiler_enabled_not_true")
    if ctx.get("apply_executable_capability_recipe_compiler") is not True:
        blockers.append("apply_executable_capability_recipe_compiler_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_LICENSE_READY":
        blockers.append("executable_capability_recipe_compiler_license_not_ready")
    for name in ["capability_recipe_packet_read_allowed", "capability_sequence_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(recipe_packet_path)
    if not packet:
        blockers.append("capability_recipe_packet_missing_or_invalid")
    if packet and packet.get("capability_recipe_allowed") is not True:
        blockers.append("capability_recipe_packet_allowed_not_true")
    recipe = str(packet.get("capability_recipe", "unknown")) if packet else "unknown"
    if recipe not in CAPABILITY_RECIPES:
        blockers.append("capability_recipe_not_allowlisted")
    if lic.get(f"allow_{recipe}_capability_recipe") is not True:
        blockers.append(f"{recipe}_not_allowed_by_capability_recipe_compiler_license")
    cap = _i(ctx.get("max_compiled_capability_sequence", packet.get("max_compiled_capability_sequence", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_compiled_capability_sequence_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_compiled_capability_sequence_capped_to_20")
        cap = 20

    sequence: list[dict[str, Any]] = []
    payload: dict[str, Any] = {}
    if recipe in CAPABILITY_RECIPES:
        sequence = _compile_sequence(recipe, packet)
        if len(sequence) > cap:
            blockers.append("compiled_capability_sequence_exceeds_cap")
        for item in sequence:
            if str(item.get("capability_kind")) not in CAPABILITY_INPUTS:
                blockers.append("compiled_capability_kind_not_allowlisted")
        payload = _sequence_packet(recipe, sequence, cap, packet)
    write_performed = False
    if not blockers:
        _write_json(sequence_packet_path, payload)
        write_performed = True
    status = "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY" if not blockers else "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_BLOCKED"
    packet_id = "qi-executable-capability-recipe-" + _sha({"packet": packet, "sequence": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_capability_recipe_compiler_v5_1",
        "status": status,
        "packet_id": packet_id,
        "capability_recipe": recipe,
        "sequence_length": len(sequence),
        "write_performed": write_performed,
        "sequence_packet_digest": _sha(payload),
        "available_capability_recipes": sorted(CAPABILITY_RECIPES),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableCapabilityRecipeCompilerResult(
        "kuuos_runtime_daemon_qi_executable_capability_recipe_compiler_v5_1",
        status,
        packet_id,
        str(root),
        recipe,
        len(sequence),
        str(sequence_packet_path),
        str(receipt_path),
        str(audit_path),
        write_performed,
        blockers,
        warnings,
    )

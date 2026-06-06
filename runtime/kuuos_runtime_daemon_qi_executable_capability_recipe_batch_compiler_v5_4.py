#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_capability_recipe_compiler_v5_1 import CAPABILITY_RECIPES


CAPABILITY_RECIPE_BATCHES: dict[str, list[str]] = {
    "compile_surface_twice": [
        "compile_recipe_and_batch",
        "compile_recipe_and_batch",
    ],
    "compile_then_execute_surface": [
        "compile_recipe_and_batch",
        "compile_then_execute_recipe",
    ],
    "batch_compile_then_execute_surface": [
        "compile_batch_then_execute_batch",
        "compile_batch_then_execute_batch",
    ],
    "observe_compile_batch_surface": [
        "route_observe_then_compile",
        "compile_recipe_and_batch",
    ],
    "safe_full_capability_batch_surface": [
        "compile_recipe_and_batch",
        "safe_compile_full_surface",
        "compile_batch_then_execute_batch",
    ],
}


@dataclass(frozen=True)
class QiExecutableCapabilityRecipeBatchCompilerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    batch_recipe: str
    batch_length: int
    batch_packet_path: str
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


def _compile_batch(batch_recipe: str, packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    default_context = dict(_m(packet.get("default_recipe_context")))
    context_by_recipe = _m(packet.get("recipe_context_by_recipe"))
    out: list[dict[str, Any]] = []
    for recipe in CAPABILITY_RECIPE_BATCHES[batch_recipe]:
        item = {
            "capability_recipe": recipe,
            "capability_recipe_allowed": True,
            "capability_recipe_batch_source": batch_recipe,
        }
        item.update(default_context)
        specific = _m(context_by_recipe.get(recipe)) if isinstance(context_by_recipe, Mapping) else {}
        item.update(dict(specific))
        out.append(item)
    return out


def _batch_packet(batch_recipe: str, batch: list[dict[str, Any]], cap: int, source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_executable_capability_recipe_batch_packet_from_compiler_v5_4",
        "batch_allowed": True,
        "capability_recipe_batch": batch_recipe,
        "batch": batch,
        "max_capability_recipe_batch": cap,
        "compiled_from": "qi_executable_capability_recipe_batch_compiler_v5_4",
        "source_digest": _sha(dict(source)),
        "boundary": {
            "compiled_batch_only": True,
            "does_not_execute_capability_recipes": True,
            "requires_v5_3_capability_recipe_batch_executor": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_executable_capability_recipe_batch_compiler(*, runtime_context: Mapping[str, Any], batch_compiler_license: Mapping[str, Any]) -> QiExecutableCapabilityRecipeBatchCompilerResult:
    ctx = _m(runtime_context)
    lic = _m(batch_compiler_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    compiler_packet_path = root / "qi_executable_capability_recipe_batch_compiler_packet.json"
    batch_packet_path = root / "qi_executable_capability_recipe_batch_packet.json"
    receipt_path = root / "qi_executable_capability_recipe_batch_compiler_receipt.json"
    audit_path = root / "qi_executable_capability_recipe_batch_compiler_audit.jsonl"

    if ctx.get("qi_executable_capability_recipe_batch_compiler_enabled") is not True:
        blockers.append("qi_executable_capability_recipe_batch_compiler_enabled_not_true")
    if ctx.get("apply_executable_capability_recipe_batch_compiler") is not True:
        blockers.append("apply_executable_capability_recipe_batch_compiler_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_LICENSE_READY":
        blockers.append("executable_capability_recipe_batch_compiler_license_not_ready")
    for name in ["batch_compiler_packet_read_allowed", "batch_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(compiler_packet_path)
    if not packet:
        blockers.append("capability_recipe_batch_compiler_packet_missing_or_invalid")
    if packet and packet.get("batch_recipe_allowed") is not True:
        blockers.append("capability_recipe_batch_packet_allowed_not_true")
    batch_recipe = str(packet.get("batch_recipe", "unknown")) if packet else "unknown"
    if batch_recipe not in CAPABILITY_RECIPE_BATCHES:
        blockers.append("capability_recipe_batch_not_allowlisted")
    if lic.get(f"allow_{batch_recipe}_batch_recipe") is not True:
        blockers.append(f"{batch_recipe}_not_allowed_by_capability_recipe_batch_compiler_license")
    cap = _i(ctx.get("max_compiled_capability_recipe_batch", packet.get("max_compiled_capability_recipe_batch", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_compiled_capability_recipe_batch_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_compiled_capability_recipe_batch_capped_to_20")
        cap = 20

    batch: list[dict[str, Any]] = []
    payload: dict[str, Any] = {}
    if batch_recipe in CAPABILITY_RECIPE_BATCHES:
        batch = _compile_batch(batch_recipe, packet)
        if len(batch) > cap:
            blockers.append("compiled_capability_recipe_batch_exceeds_cap")
        for item in batch:
            if str(item.get("capability_recipe")) not in CAPABILITY_RECIPES:
                blockers.append("compiled_capability_recipe_not_allowlisted")
        payload = _batch_packet(batch_recipe, batch, cap, packet)
    write_performed = False
    if not blockers:
        _write_json(batch_packet_path, payload)
        write_performed = True
    status = "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_READY" if not blockers else "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_BLOCKED"
    packet_id = "qi-executable-capability-recipe-batch-compiler-" + _sha({"packet": packet, "batch": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_capability_recipe_batch_compiler_v5_4",
        "status": status,
        "packet_id": packet_id,
        "batch_recipe": batch_recipe,
        "batch_length": len(batch),
        "write_performed": write_performed,
        "batch_packet_digest": _sha(payload),
        "available_capability_recipe_batches": sorted(CAPABILITY_RECIPE_BATCHES),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableCapabilityRecipeBatchCompilerResult(
        "kuuos_runtime_daemon_qi_executable_capability_recipe_batch_compiler_v5_4",
        status,
        packet_id,
        str(root),
        batch_recipe,
        len(batch),
        str(batch_packet_path),
        str(receipt_path),
        str(audit_path),
        write_performed,
        blockers,
        warnings,
    )

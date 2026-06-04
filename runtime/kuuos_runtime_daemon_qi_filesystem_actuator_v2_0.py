#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import shutil
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiFilesystemActuatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    receipt_path: str
    audit_path: str
    applied_count: int
    skipped_count: int
    replay_count: int
    qi_gain: float
    qi_drag: float
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _f(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _gains(pt: Mapping[str, Any]) -> tuple[float, float]:
    pressure = max(0.0, min(1.0, _f(pt.get("execution_pressure", pt.get("pressure")), 0.0)))
    coherence = max(0.0, min(1.0, _f(pt.get("coherence_score", pt.get("coherence")), 0.0)))
    return round(1.0 + pressure * coherence, 6), round(1.0 - coherence, 6)


def _items(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = plan.get("actions", plan.get("items", []))
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _safe_path(root: pathlib.Path, raw: Any, blockers: list[str], label: str) -> pathlib.Path:
    if raw is None or str(raw).strip() == "":
        blockers.append(f"{label}_path_missing")
        return root
    rel = pathlib.Path(str(raw))
    if rel.is_absolute():
        blockers.append(f"{label}_absolute_path_forbidden")
        return root
    target = (root / rel).resolve()
    if root not in target.parents and target != root:
        blockers.append(f"{label}_path_escape_forbidden")
        return root
    return target


def _seen(path: pathlib.Path) -> set[str]:
    return {str(row.get("act_key")) for row in _read_jsonl(path) if row.get("act_key")}


def _content_for(item: Mapping[str, Any], qi_gain: float, qi_drag: float) -> str:
    text = str(item.get("content", item.get("text", "")))
    if item.get("include_qi_header") is True:
        return f"qi_gain={qi_gain}\nqi_drag={qi_drag}\n\n{text}"
    return text


def _apply_one(root: pathlib.Path, item: Mapping[str, Any], qi_gain: float, qi_drag: float, blockers: list[str]) -> dict[str, Any]:
    kind = str(item.get("kind", item.get("action", "create_text")))
    out: dict[str, Any] = {"kind": kind}
    if kind == "create_text":
        path = _safe_path(root, item.get("path"), blockers, "create")
        if item.get("overwrite") is True:
            blockers.append("overwrite_forbidden")
            return out
        if path.exists():
            blockers.append("create_target_exists")
            return out
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_content_for(item, qi_gain, qi_drag), encoding="utf-8")
        out["path"] = str(path)
        out["bytes"] = path.stat().st_size
    elif kind == "append_text":
        path = _safe_path(root, item.get("path"), blockers, "append")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(_content_for(item, qi_gain, qi_drag))
            if item.get("newline", True) is not False:
                handle.write("\n")
        out["path"] = str(path)
        out["bytes"] = path.stat().st_size
    elif kind == "make_dir":
        path = _safe_path(root, item.get("path"), blockers, "mkdir")
        path.mkdir(parents=True, exist_ok=True)
        out["path"] = str(path)
    elif kind == "copy_file":
        src = _safe_path(root, item.get("src"), blockers, "copy_src")
        dst = _safe_path(root, item.get("dst"), blockers, "copy_dst")
        if not src.is_file():
            blockers.append("copy_source_missing")
            return out
        if dst.exists():
            blockers.append("copy_target_exists")
            return out
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        out["src"] = str(src)
        out["dst"] = str(dst)
    elif kind == "move_file":
        src = _safe_path(root, item.get("src"), blockers, "move_src")
        dst = _safe_path(root, item.get("dst"), blockers, "move_dst")
        if not src.is_file():
            blockers.append("move_source_missing")
            return out
        if dst.exists():
            blockers.append("move_target_exists")
            return out
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        out["src"] = str(src)
        out["dst"] = str(dst)
    elif kind == "archive_file":
        src = _safe_path(root, item.get("src"), blockers, "archive_src")
        if not src.is_file():
            blockers.append("archive_source_missing")
            return out
        archive_root = root / "archive"
        dst = archive_root / f"{int(time.time())}_{src.name}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        out["src"] = str(src)
        out["dst"] = str(dst)
    elif kind == "write_json":
        path = _safe_path(root, item.get("path"), blockers, "json")
        if path.exists() and item.get("overwrite") is not True:
            blockers.append("json_target_exists")
            return out
        payload = item.get("payload", {})
        if not isinstance(payload, Mapping):
            blockers.append("json_payload_not_object")
            return out
        enriched = dict(payload)
        if item.get("include_qi") is True:
            enriched.update({"qi_gain": qi_gain, "qi_drag": qi_drag})
        _write_json(path, enriched)
        out["path"] = str(path)
    else:
        blockers.append(f"unknown_action_{kind}")
    return out


def build_qi_filesystem_actuator(*, runtime_context: Mapping[str, Any], pt_packet: Mapping[str, Any], actuator_license_packet: Mapping[str, Any]) -> QiFilesystemActuatorResult:
    ctx = _m(runtime_context)
    pt = _m(pt_packet)
    lic = _m(actuator_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    sandbox_root = root / str(ctx.get("actuator_root", "actuator_fs"))
    sandbox_root = sandbox_root.resolve()
    if root not in sandbox_root.parents and sandbox_root != root:
        blockers.append("actuator_root_escape_forbidden")
    plan_path = root / "actuator_plan.json"
    receipt_path = root / "actuator_receipt.json"
    audit_path = root / "actuator_audit.jsonl"
    if ctx.get("qi_filesystem_actuator_enabled") is not True:
        blockers.append("qi_filesystem_actuator_enabled_not_true")
    if ctx.get("apply_filesystem_actuator") is not True:
        blockers.append("apply_filesystem_actuator_not_true")
    if lic.get("license_status") != "QI_FILESYSTEM_ACTUATOR_LICENSE_READY":
        blockers.append("filesystem_actuator_license_not_ready")
    for name in ["plan_read_allowed", "file_create_allowed", "file_append_allowed", "file_copy_allowed", "file_move_allowed", "file_archive_allowed", "json_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    qi_gain, qi_drag = _gains(pt)
    plan = _read_json(plan_path)
    items = _items(plan)
    if not items and not blockers:
        warnings.append("actuator_plan_empty")
    max_actions = max(1, _i(ctx.get("max_actions"), 20))
    seen = _seen(audit_path)
    records: list[dict[str, Any]] = []
    replay = 0
    skipped = 0
    ready = not blockers
    if ready:
        for item in items[:max_actions]:
            key = _sha({"item": item, "pt": _sha(dict(pt))})
            if key in seen:
                replay += 1
                continue
            local_blockers: list[str] = []
            out = _apply_one(sandbox_root, item, qi_gain, qi_drag, local_blockers)
            if local_blockers:
                skipped += 1
                rec_status = "skipped"
            else:
                rec_status = "applied"
            rec = {"act_key": key, "status": rec_status, "item_digest": _sha(item), "output": out, "blockers": local_blockers, "qi_gain": qi_gain, "qi_drag": qi_drag, "epoch": int(time.time())}
            rec["record_digest"] = _sha(rec)
            _append_jsonl(audit_path, rec)
            records.append(rec)
            seen.add(key)
    else:
        warnings.append("filesystem_actuator_blocked_before_apply")
    applied = len([r for r in records if r.get("status") == "applied"])
    status = "QI_FILESYSTEM_ACTUATOR_BLOCKED" if blockers else ("QI_FILESYSTEM_ACTUATOR_IDLE" if not items else "QI_FILESYSTEM_ACTUATOR_APPLIED")
    packet_id = "qi-filesystem-actuator-" + _sha({"root": str(root), "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_filesystem_actuator_v2_0", "status": status, "packet_id": packet_id, "applied_count": applied, "skipped_count": skipped, "replay_count": replay, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True and (ready or status == "QI_FILESYSTEM_ACTUATOR_BLOCKED"):
        _write_json(receipt_path, receipt)
    return QiFilesystemActuatorResult("kuuos_runtime_daemon_qi_filesystem_actuator_v2_0", status, packet_id, str(root), str(plan_path), str(receipt_path), str(audit_path), applied, skipped, replay, qi_gain, qi_drag, records, blockers, warnings)

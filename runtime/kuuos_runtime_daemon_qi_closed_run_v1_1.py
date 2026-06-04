#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_execution_loop_v0_9 import build_qi_execution_loop
from runtime.kuuos_runtime_daemon_qi_loop_adapt_v1_0 import build_qi_loop_adapt


@dataclass(frozen=True)
class QiClosedRunResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    loop_status: str
    adapt_status: str
    loop_records: int
    items_applied: int
    graph_nodes_done: int
    next_cycles: int
    next_budget: int
    chain_path: str
    final_path: str
    loop_packet_id: str
    adapt_packet_id: str
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


def _loop_license(lic: Mapping[str, Any]) -> dict[str, Any]:
    nested = lic.get("loop_license_packet")
    if isinstance(nested, Mapping):
        return dict(nested)
    return {
        "license_status": "QI_EXECUTION_LOOP_LICENSE_READY",
        "queue_read_allowed": lic.get("queue_read_allowed", True),
        "state_write_allowed": lic.get("state_write_allowed", True),
        "loop_log_append_allowed": lic.get("loop_log_append_allowed", True),
        "summary_write_allowed": lic.get("summary_write_allowed", True),
        "feedback_append_allowed": lic.get("feedback_append_allowed", True),
        "artifact_write_allowed": lic.get("artifact_write_allowed", True),
    }


def _adapt_license(lic: Mapping[str, Any]) -> dict[str, Any]:
    nested = lic.get("adapt_license_packet")
    if isinstance(nested, Mapping):
        return dict(nested)
    return {
        "license_status": "QI_LOOP_ADAPT_LICENSE_READY",
        "state_read_allowed": lic.get("state_read_allowed", True),
        "summary_read_allowed": lic.get("summary_read_allowed", True),
        "feedback_read_allowed": lic.get("feedback_read_allowed", True),
        "next_pt_write_allowed": lic.get("next_pt_write_allowed", True),
        "next_context_write_allowed": lic.get("next_context_write_allowed", True),
        "adapt_log_append_allowed": lic.get("adapt_log_append_allowed", True),
    }


def build_qi_closed_run(*, runtime_context: Mapping[str, Any], pt_packet: Mapping[str, Any], closed_license_packet: Mapping[str, Any]) -> QiClosedRunResult:
    ctx = dict(_m(runtime_context))
    pt = dict(_m(pt_packet))
    lic = _m(closed_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    chain_path = root / "closed_run_chain.jsonl"
    final_path = root / "closed_run_final.json"
    if ctx.get("qi_closed_run_enabled") is not True:
        blockers.append("qi_closed_run_enabled_not_true")
    if ctx.get("apply_closed_run") is not True:
        blockers.append("apply_closed_run_not_true")
    if lic.get("license_status") != "QI_CLOSED_RUN_LICENSE_READY":
        blockers.append("closed_run_license_not_ready")
    if lic.get("chain_append_allowed") is not True:
        blockers.append("chain_append_not_allowed")
    if lic.get("final_write_allowed") is not True:
        blockers.append("final_write_not_allowed")
    loop_status = "NOT_RUN"
    adapt_status = "NOT_RUN"
    loop_packet_id = ""
    adapt_packet_id = ""
    loop_records = 0
    items_applied = 0
    graph_nodes_done = 0
    next_cycles = 0
    next_budget = 0
    if not blockers:
        loop_ctx = dict(ctx)
        loop_ctx.update({
            "qi_execution_loop_enabled": True,
            "apply_execution_loop": True,
            "runtime_root": str(root),
        })
        loop_result = build_qi_execution_loop(
            runtime_context=loop_ctx,
            process_tensor_packet=pt,
            loop_license_packet=_loop_license(lic),
        )
        loop_payload = loop_result.to_dict()
        loop_status = str(loop_payload.get("status"))
        loop_packet_id = str(loop_payload.get("packet_id"))
        loop_records = len(loop_payload.get("records", [])) if isinstance(loop_payload.get("records"), list) else 0
        items_applied = int(loop_payload.get("items_applied", 0))
        graph_nodes_done = int(loop_payload.get("graph_nodes_done", 0))
        _append_jsonl(chain_path, {"stage": "loop", "packet_id": loop_packet_id, "status": loop_status, "payload_digest": _sha(loop_payload), "epoch": int(time.time())})
        if loop_status == "QI_EXECUTION_LOOP_BLOCKED":
            blockers.append("loop_stage_blocked")
            warnings.extend(str(item) for item in loop_payload.get("warnings", []))
        else:
            adapt_ctx = dict(ctx)
            adapt_ctx.update({
                "qi_loop_adapt_enabled": True,
                "apply_loop_adapt": True,
                "runtime_root": str(root),
                "cycles": int(ctx.get("cycles", 1)),
                "base_cycle_budget": int(ctx.get("base_cycle_budget", 3)),
            })
            adapt_result = build_qi_loop_adapt(
                runtime_context=adapt_ctx,
                pt_packet=pt,
                adapt_license_packet=_adapt_license(lic),
            )
            adapt_payload = adapt_result.to_dict()
            adapt_status = str(adapt_payload.get("status"))
            adapt_packet_id = str(adapt_payload.get("packet_id"))
            next_cycles = int(adapt_payload.get("next_cycles", 0))
            next_budget = int(adapt_payload.get("next_budget", 0))
            _append_jsonl(chain_path, {"stage": "adapt", "packet_id": adapt_packet_id, "status": adapt_status, "payload_digest": _sha(adapt_payload), "epoch": int(time.time())})
            if adapt_status == "QI_LOOP_ADAPT_BLOCKED":
                blockers.append("adapt_stage_blocked")
                warnings.extend(str(item) for item in adapt_payload.get("warnings", []))
    if blockers:
        status = "QI_CLOSED_RUN_BLOCKED"
    elif loop_status == "QI_EXECUTION_LOOP_IDLE" and adapt_status == "QI_LOOP_ADAPT_IDLE":
        status = "QI_CLOSED_RUN_IDLE"
    else:
        status = "QI_CLOSED_RUN_APPLIED"
    packet_id = "qi-closed-run-" + _sha({"root": str(root), "loop": loop_status, "adapt": adapt_status, "blockers": blockers})[:16]
    final = {
        "version": "kuuos_runtime_daemon_qi_closed_run_v1_1",
        "status": status,
        "packet_id": packet_id,
        "runtime_root": str(root),
        "loop_status": loop_status,
        "adapt_status": adapt_status,
        "loop_records": loop_records,
        "items_applied": items_applied,
        "graph_nodes_done": graph_nodes_done,
        "next_cycles": next_cycles,
        "next_budget": next_budget,
        "pt_next_path": str(root / "pt_next.json"),
        "next_context_path": str(root / "next_loop_context.json"),
        "chain_path": str(chain_path),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if not blockers or final_path.parent.exists() or root != pathlib.Path(".").resolve():
        if lic.get("final_write_allowed") is True:
            _write_json(final_path, final)
    return QiClosedRunResult(
        "kuuos_runtime_daemon_qi_closed_run_v1_1",
        status,
        packet_id,
        str(root),
        loop_status,
        adapt_status,
        loop_records,
        items_applied,
        graph_nodes_done,
        next_cycles,
        next_budget,
        str(chain_path),
        str(final_path),
        loop_packet_id,
        adapt_packet_id,
        blockers,
        warnings,
    )

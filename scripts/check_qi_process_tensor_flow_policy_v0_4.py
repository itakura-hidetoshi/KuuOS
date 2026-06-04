#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_flow_policy_v0_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(runtime_root: pathlib.Path, max_admit: int = 10) -> dict[str, Any]:
    return {
        "qi_process_tensor_flow_policy_enabled": True,
        "apply_process_tensor_policy": True,
        "runtime_root": str(runtime_root),
        "max_rows": 100,
        "max_admit": max_admit,
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PROCESS_TENSOR_FLOW_POLICY_LICENSE_READY",
        "queue_read_allowed": True,
        "ready_queue_append_allowed": True,
        "deferred_queue_append_allowed": True,
        "policy_state_write_allowed": True,
        "policy_log_append_allowed": True,
    }
    value.update(overrides)
    return value


def pt(**overrides: Any) -> dict[str, Any]:
    value = {
        "process_tensor_ok": True,
        "execution_pressure": 0.7,
        "coherence_score": 0.8,
        "memory_depth": 4,
        "recovery_witness_present": True,
        "recovery_witness_missing": False,
        "non_markov_unresolved": False,
        "preferred_actions": ["notify"],
        "blocked_actions": ["handover"],
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, c: dict[str, Any], p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    cp = root / f"{name}_ctx.json"
    pp = root / f"{name}_pt.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, c)
    dump(pp, p)
    dump(lp, l)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--context", str(cp),
        "--process-tensor", str(pp),
        "--license", str(lp),
        "--write", str(op),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        r1 = root / "r1"
        write_jsonl(r1 / "queue.jsonl", [
            {"item_id": "a", "item_kind": "advance_tick", "priority": 0.1},
            {"item_id": "b", "item_kind": "notify", "priority": 0.1},
            {"item_id": "c", "item_kind": "handover", "priority": 9.0},
        ])
        rc, out = run(root, "apply", ctx(r1), pt(), lic())
        if rc != 0 or out.get("policy_status") != "QI_PROCESS_TENSOR_FLOW_POLICY_APPLIED":
            errors.append("apply_status")
        if out.get("admitted_count") != 2 or out.get("deferred_count") != 1:
            errors.append("admit_defer_counts")
        ready = read_rows(r1 / "queue.ready.jsonl")
        deferred = read_rows(r1 / "queue.deferred.jsonl")
        if len(ready) != 2 or len(deferred) != 1:
            errors.append("ready_deferred_files")
        if ready[0].get("item_kind") != "notify":
            errors.append("preferred_order_not_first")
        if deferred[0].get("policy_reason") != "blocked_by_process_tensor":
            errors.append("blocked_reason")
        state = load_json(r1 / "pt_policy_state.json")
        if state.get("admitted_total") != 2 or state.get("deferred_total") != 1:
            errors.append("policy_state_totals")

        rc, out = run(root, "replay", ctx(r1), pt(), lic())
        if rc != 0 or out.get("policy_status") != "QI_PROCESS_TENSOR_FLOW_POLICY_REPLAYED":
            errors.append("replay_status")
        if out.get("admitted_count") != 0 or out.get("deferred_count") != 0 or out.get("replay_count") != 3:
            errors.append("replay_counts")

        r2 = root / "r2"
        write_jsonl(r2 / "queue.jsonl", [
            {"item_id": "d", "item_kind": "notify"},
            {"item_id": "e", "item_kind": "advance_tick"},
        ])
        rc, out = run(root, "nonmarkov", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 0 or out.get("admitted_count") != 0 or out.get("deferred_count") != 2:
            errors.append("nonmarkov_defer")
        if {row.get("policy_reason") for row in read_rows(r2 / "queue.deferred.jsonl")} != {"defer_non_markov_unresolved"}:
            errors.append("nonmarkov_reason")

        r3 = root / "r3"
        write_jsonl(r3 / "queue.jsonl", [{"item_id": "f", "item_kind": "notify"}])
        rc, out = run(root, "blocked", ctx(r3), pt(), lic(policy_state_write_allowed=False))
        if rc != 1 or out.get("policy_status") != "QI_PROCESS_TENSOR_FLOW_POLICY_BLOCKED":
            errors.append("blocked_status")
        if "policy_state_write_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_reason_missing")
        if (r3 / "queue.ready.jsonl").exists() or (r3 / "pt_policy_state.json").exists():
            errors.append("blocked_wrote_files")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi process tensor flow policy v0.4 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

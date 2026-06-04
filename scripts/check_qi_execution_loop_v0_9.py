#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_execution_loop_v0_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_rows(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(runtime_root: pathlib.Path, cycles: int = 2, base_cycle_budget: int = 2) -> dict[str, Any]:
    return {
        "qi_execution_loop_enabled": True,
        "apply_execution_loop": True,
        "runtime_root": str(runtime_root),
        "cycles": cycles,
        "base_cycle_budget": base_cycle_budget,
    }


def pt(**overrides: Any) -> dict[str, Any]:
    value = {
        "process_tensor_ok": True,
        "execution_pressure": 0.8,
        "coherence_score": 0.5,
        "memory_depth": 4,
        "recovery_witness_present": True,
        "recovery_witness_missing": False,
        "non_markov_unresolved": False,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTION_LOOP_LICENSE_READY",
        "queue_read_allowed": True,
        "state_write_allowed": True,
        "loop_log_append_allowed": True,
        "summary_write_allowed": True,
        "feedback_append_allowed": True,
        "artifact_write_allowed": True,
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
        "--pt", str(pp),
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
        write_rows(r1 / "queue.ready.jsonl", [
            {"policy_key": "m1", "item_kind": "metric", "value": 2.0, "policy_score": 9.0},
            {"policy_key": "c1", "item_kind": "counter", "name": "done", "amount": 1.0, "policy_score": 8.0},
            {"policy_key": "r1", "item_kind": "recover", "policy_score": 7.0},
            {"policy_key": "p1", "item_kind": "state_patch", "energy_delta": 1.0, "stability_delta": 0.5, "policy_score": 6.0},
        ])
        dump(r1 / "work_graph.json", {
            "nodes": [
                {"id": "report", "kind": "report", "score": 2.0},
                {"id": "checkpoint", "kind": "checkpoint", "depends_on": ["report"], "score": 1.0},
            ]
        })
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_EXECUTION_LOOP_APPLIED":
            errors.append("first_status")
        if out.get("cycles_completed") != 2 or out.get("items_applied") != 4 or out.get("graph_nodes_done") != 2:
            errors.append("first_counts")
        if out.get("qi_gain") != 1.4 or out.get("qi_drag") != 0.5:
            errors.append("gains")
        loop_rows = read_rows(r1 / "loop.jsonl")
        fb_rows = read_rows(r1 / "loop_feedback.jsonl")
        if len(loop_rows) != 6 or len(fb_rows) != 2:
            errors.append("loop_or_feedback_rows")
        if len([row for row in loop_rows if row.get("record_kind") == "item"]) != 4:
            errors.append("item_rows")
        if len([row for row in loop_rows if row.get("record_kind") == "graph"]) != 2:
            errors.append("graph_rows")
        summary = load_json(r1 / "run_summary.json")
        if summary.get("records") != 6 or summary.get("items_applied") != 4 or summary.get("graph_nodes_done") != 2:
            errors.append("summary")
        state = load_json(r1 / "state.json")
        if state.get("loop_item_total") != 4 or state.get("loop_graph_total") != 2:
            errors.append("state_totals")
        if not (r1 / "loop_reports" / "report.md").is_file():
            errors.append("report_missing")
        if not list((r1 / "loop_checkpoints").glob("*.json")):
            errors.append("checkpoint_missing")

        rc, out = run(root, "again", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_EXECUTION_LOOP_IDLE":
            errors.append("second_status")
        if len(read_rows(r1 / "loop.jsonl")) != 6:
            errors.append("second_duplicate")

        r2 = root / "r2"
        write_rows(r2 / "queue.ready.jsonl", [{"policy_key": "x", "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "blocked", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 1 or out.get("status") != "QI_EXECUTION_LOOP_BLOCKED":
            errors.append("blocked_status")
        if "non_markov_unresolved" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "state.json").exists() or (r2 / "loop.jsonl").exists():
            errors.append("blocked_files")

        r3 = root / "r3"
        write_rows(r3 / "queue.ready.jsonl", [{"policy_key": "y", "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "no_summary", ctx(r3), pt(), lic(summary_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_EXECUTION_LOOP_BLOCKED":
            errors.append("license_status")
        if "summary_write_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi execution loop v0.9 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

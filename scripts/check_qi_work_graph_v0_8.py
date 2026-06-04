#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_work_graph_v0_8.py"


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


def ctx(runtime_root: pathlib.Path, base_budget: int = 3, max_budget: int = 20) -> dict[str, Any]:
    return {
        "qi_work_graph_enabled": True,
        "apply_work_graph": True,
        "runtime_root": str(runtime_root),
        "base_budget": base_budget,
        "max_budget": max_budget,
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
        "license_status": "QI_WORK_GRAPH_LICENSE_READY",
        "graph_read_allowed": True,
        "state_write_allowed": True,
        "graph_log_append_allowed": True,
        "artifact_write_allowed": True,
        "queue_append_allowed": True,
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


def graph() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "roll", "kind": "metric_rollup", "score": 9.0},
            {"id": "patch", "kind": "state_patch", "score": 8.0, "energy_delta": 1.0, "stability_delta": 0.5},
            {"id": "report", "kind": "report", "depends_on": ["roll"], "title": "PT Graph Report", "score": 7.0},
            {"id": "checkpoint", "kind": "checkpoint", "depends_on": ["patch", "report"], "score": 6.0},
            {"id": "index", "kind": "index", "depends_on": ["checkpoint"], "score": 5.0},
            {"id": "note", "kind": "append_note", "depends_on": ["roll"], "text": "graph note", "score": 4.0},
            {"id": "seed", "kind": "ready_seed", "depends_on": ["index"], "item_kind": "metric", "score": 3.0},
        ]
    }


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        r1 = root / "r1"
        write_rows(r1 / "metrics.jsonl", [
            {"name": "a", "value": 2.0},
            {"name": "b", "value": 3.0},
        ])
        dump(r1 / "work_graph.json", graph())
        rc, out = run(root, "first", ctx(r1, base_budget=4), pt(), lic())
        if rc != 0 or out.get("status") != "QI_WORK_GRAPH_APPLIED":
            errors.append("first_status")
        if out.get("budget") != 6 or out.get("done_count") != 6 or out.get("hold_count") != 1:
            errors.append("first_budget_counts")
        counts = out.get("node_counts", {})
        for key in ["metric_rollup", "state_patch", "report", "checkpoint", "index", "append_note"]:
            if counts.get(key) != 1:
                errors.append(f"missing_{key}")
        if not (r1 / "rollups" / "roll.json").is_file():
            errors.append("rollup_missing")
        if not (r1 / "reports" / "report.md").is_file():
            errors.append("report_missing")
        if not list((r1 / "checkpoints").glob("*.json")):
            errors.append("checkpoint_missing")
        if not (r1 / "index.json").is_file():
            errors.append("index_missing")
        if "graph note" not in (r1 / "graph_notes.md").read_text(encoding="utf-8"):
            errors.append("note_missing")
        state = load_json(r1 / "state.json")
        if state.get("work_graph_total") != 6 or state.get("last_work_graph_hold_count") != 1:
            errors.append("state_graph_counts")

        rc, out = run(root, "second", ctx(r1, base_budget=4), pt(), lic())
        if rc != 0 or out.get("status") != "QI_WORK_GRAPH_APPLIED":
            errors.append("second_status")
        if out.get("done_count") != 1 or out.get("replay_count") != 6:
            errors.append("second_counts")
        if out.get("node_counts", {}).get("ready_seed") != 1:
            errors.append("seed_missing")
        ready = read_rows(r1 / "queue.ready.jsonl")
        if len(ready) != 1 or ready[0].get("graph_node_id") != "seed":
            errors.append("seed_file_missing")

        r2 = root / "r2"
        dump(r2 / "work_graph.json", graph())
        rc, out = run(root, "blocked", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 1 or out.get("status") != "QI_WORK_GRAPH_BLOCKED":
            errors.append("blocked_status")
        if "non_markov_unresolved" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "work_graph_log.jsonl").exists() or (r2 / "state.json").exists():
            errors.append("blocked_files")

        r3 = root / "r3"
        dump(r3 / "work_graph.json", graph())
        rc, out = run(root, "no_artifact", ctx(r3), pt(), lic(artifact_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_WORK_GRAPH_BLOCKED":
            errors.append("license_status")
        if "artifact_write_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi work graph v0.8 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

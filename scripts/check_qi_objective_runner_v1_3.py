#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_objective_runner_v1_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(runtime_root: pathlib.Path, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "qi_objective_runner_enabled": True,
        "apply_objective_runner": True,
        "runtime_root": str(runtime_root),
        "epochs": 2,
        "max_epochs": 4,
        "start_epoch": 0,
        "cycles": 1,
        "base_cycle_budget": 2,
        "max_cycles": 4,
        "max_base_cycle_budget": 8,
    }
    if extra:
        value.update(extra)
    return value


def pt(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "process_tensor_ok": True,
        "execution_pressure": 0.6,
        "coherence_score": 0.5,
        "memory_depth": 2,
        "target_cycle_density": 2.0,
        "recovery_witness_present": True,
        "recovery_witness_missing": False,
        "non_markov_unresolved": False,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "license_status": "QI_OBJECTIVE_RUNNER_LICENSE_READY",
        "objective_read_allowed": True,
        "task_write_allowed": True,
        "graph_write_allowed": True,
        "plan_write_allowed": True,
        "final_write_allowed": True,
        "epoch_run_allowed": True,
        "task_read_allowed": True,
        "task_inject_allowed": True,
        "epoch_chain_append_allowed": True,
        "epoch_final_write_allowed": True,
        "pt_carry_allowed": True,
        "context_carry_allowed": True,
        "chain_append_allowed": True,
        "queue_read_allowed": True,
        "state_write_allowed": True,
        "loop_log_append_allowed": True,
        "summary_write_allowed": True,
        "feedback_append_allowed": True,
        "artifact_write_allowed": True,
        "state_read_allowed": True,
        "summary_read_allowed": True,
        "feedback_read_allowed": True,
        "next_pt_write_allowed": True,
        "next_context_write_allowed": True,
        "adapt_log_append_allowed": True,
    }
    value.update(overrides)
    return value


def objectives() -> dict[str, Any]:
    return {
        "objectives": [
            {"id": "m", "task_kind": "metric", "value": 2.0, "priority": 3.0, "due_epoch": 0, "title": "Metric objective"},
            {"id": "c", "task_kind": "counter", "name": "counted", "amount": 1, "priority": 2.0, "due_epoch": 1, "title": "Counter objective"},
        ]
    }


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
        dump(r1 / "objectives.json", objectives())
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_OBJECTIVE_RUNNER_APPLIED":
            errors.append("first_status")
        if out.get("objectives_loaded") != 2 or out.get("tasks_created") != 2 or out.get("graph_nodes_created") != 6:
            errors.append("plan_counts")
        if out.get("epoch_status") != "QI_EPOCH_RUNNER_APPLIED" or out.get("epochs_completed") != 2:
            errors.append("epoch_status")
        if out.get("tasks_injected") != 2:
            errors.append("tasks_injected")
        tasks = read_rows(r1 / "epoch_tasks.jsonl")
        if len(tasks) != 2 or {row.get("objective_id") for row in tasks} != {"m", "c"}:
            errors.append("tasks_file")
        graph = load_json(r1 / "work_graph.json")
        if len(graph.get("nodes", [])) != 6:
            errors.append("graph_file")
        if not (r1 / "objective_plan.json").is_file() or not (r1 / "objective_final.json").is_file():
            errors.append("objective_files")
        final = load_json(r1 / "objective_final.json")
        if final.get("status") != "QI_OBJECTIVE_RUNNER_APPLIED" or final.get("progress_score", 0) <= 0:
            errors.append("final_content")
        if not (r1 / "epoch_final.json").is_file() or not (r1 / "pt_next.json").is_file():
            errors.append("epoch_outputs")

        rc, out = run(root, "second", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_OBJECTIVE_RUNNER_APPLIED":
            errors.append("second_status")
        if out.get("tasks_created") != 0 or out.get("graph_nodes_created") != 0:
            errors.append("idempotency")
        if len(read_rows(r1 / "epoch_tasks.jsonl")) != 2:
            errors.append("duplicate_tasks")
        if len(load_json(r1 / "work_graph.json").get("nodes", [])) != 6:
            errors.append("duplicate_nodes")

        r2 = root / "r2"
        dump(r2 / "objectives.json", objectives())
        rc, out = run(root, "blocked", ctx(r2), pt(), lic(task_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_OBJECTIVE_RUNNER_BLOCKED":
            errors.append("blocked_status")
        if "task_write_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "epoch_tasks.jsonl").exists() or (r2 / "work_graph.json").exists():
            errors.append("blocked_files")

        r3 = root / "r3"
        rc, out = run(root, "idle", ctx(r3), pt(), lic())
        if rc != 0 or out.get("status") != "QI_OBJECTIVE_RUNNER_IDLE":
            errors.append("idle_status")
        if not (r3 / "objective_final.json").is_file():
            errors.append("idle_final")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi objective runner v1.3 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

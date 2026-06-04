#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_epoch_runner_v1_2.py"


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


def ctx(runtime_root: pathlib.Path, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "qi_epoch_runner_enabled": True,
        "apply_epoch_runner": True,
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
        "license_status": "QI_EPOCH_RUNNER_LICENSE_READY",
        "task_read_allowed": True,
        "task_inject_allowed": True,
        "epoch_chain_append_allowed": True,
        "epoch_final_write_allowed": True,
        "pt_carry_allowed": True,
        "context_carry_allowed": True,
        "chain_append_allowed": True,
        "final_write_allowed": True,
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
        write_rows(r1 / "epoch_tasks.jsonl", [
            {"task_id": "t0", "due_epoch": 0, "item_kind": "metric", "value": 2.0, "policy_score": 9.0},
            {"task_id": "t1", "due_epoch": 1, "item_kind": "counter", "name": "epoch", "amount": 1.0, "policy_score": 8.0},
        ])
        dump(r1 / "work_graph.json", {
            "nodes": [
                {"id": "report", "kind": "report", "score": 2.0},
                {"id": "checkpoint", "kind": "checkpoint", "depends_on": ["report"], "score": 1.0},
            ]
        })
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_EPOCH_RUNNER_APPLIED":
            errors.append("first_status")
        if out.get("epochs_completed") != 2 or out.get("epochs_requested") != 2:
            errors.append("epoch_counts")
        if out.get("tasks_loaded") != 2 or out.get("tasks_injected") != 2:
            errors.append("task_counts")
        if out.get("closed_runs_applied", 0) < 1:
            errors.append("closed_runs_not_applied")
        if not (r1 / "pt_next.json").is_file() or not (r1 / "next_loop_context.json").is_file():
            errors.append("carry_files_missing")
        if not (r1 / "epoch_final.json").is_file():
            errors.append("epoch_final_missing")
        chain = read_rows(r1 / "epoch_chain.jsonl")
        if len(chain) != 2 or [row.get("epoch") for row in chain] != [0, 1]:
            errors.append("epoch_chain")
        injections = read_rows(r1 / "epoch_injections.jsonl")
        if len(injections) != 2:
            errors.append("injection_log")
        final = load_json(r1 / "epoch_final.json")
        if final.get("status") != "QI_EPOCH_RUNNER_APPLIED" or final.get("tasks_injected") != 2:
            errors.append("final_content")
        next_ctx = load_json(r1 / "next_loop_context.json")
        if next_ctx.get("cycles", 0) < 1 or next_ctx.get("base_cycle_budget", 0) < 1:
            errors.append("next_context_values")

        r2 = root / "r2"
        write_rows(r2 / "epoch_tasks.jsonl", [{"task_id": "x", "due_epoch": 0, "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "blocked", ctx(r2), pt(), lic(task_inject_allowed=False))
        if rc != 1 or out.get("status") != "QI_EPOCH_RUNNER_BLOCKED":
            errors.append("blocked_status")
        if "task_inject_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "queue.ready.jsonl").exists() or (r2 / "epoch_chain.jsonl").exists():
            errors.append("blocked_files")

        r3 = root / "r3"
        rc, out = run(root, "idle", ctx(r3), pt(), lic())
        if rc != 0 or out.get("status") not in {"QI_EPOCH_RUNNER_IDLE", "QI_EPOCH_RUNNER_APPLIED"}:
            errors.append("idle_status")
        if not (r3 / "epoch_final.json").is_file():
            errors.append("idle_final")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi epoch runner v1.2 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

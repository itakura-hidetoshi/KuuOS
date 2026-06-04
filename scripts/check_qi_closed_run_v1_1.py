#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_closed_run_v1_1.py"


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
        "qi_closed_run_enabled": True,
        "apply_closed_run": True,
        "runtime_root": str(runtime_root),
        "cycles": 2,
        "base_cycle_budget": 2,
        "max_cycles": 8,
        "max_base_cycle_budget": 12,
    }
    if extra:
        value.update(extra)
    return value


def pt(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "process_tensor_ok": True,
        "execution_pressure": 0.8,
        "coherence_score": 0.5,
        "memory_depth": 4,
        "target_cycle_density": 3.0,
        "recovery_witness_present": True,
        "recovery_witness_missing": False,
        "non_markov_unresolved": False,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "license_status": "QI_CLOSED_RUN_LICENSE_READY",
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
        write_rows(r1 / "queue.ready.jsonl", [
            {"policy_key": "m1", "item_kind": "metric", "value": 2.0, "policy_score": 9.0},
            {"policy_key": "c1", "item_kind": "counter", "name": "done", "amount": 1.0, "policy_score": 8.0},
            {"policy_key": "r1", "item_kind": "recover", "policy_score": 7.0},
        ])
        dump(r1 / "work_graph.json", {
            "nodes": [
                {"id": "report", "kind": "report", "score": 2.0},
                {"id": "checkpoint", "kind": "checkpoint", "depends_on": ["report"], "score": 1.0},
            ]
        })
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_CLOSED_RUN_APPLIED":
            errors.append("first_status")
        if out.get("loop_status") != "QI_EXECUTION_LOOP_APPLIED" or out.get("adapt_status") != "QI_LOOP_ADAPT_APPLIED":
            errors.append("stage_status")
        if out.get("items_applied") != 3 or out.get("graph_nodes_done") != 2:
            errors.append("stage_counts")
        if out.get("next_cycles") != 3 or out.get("next_budget") != 3:
            errors.append("next_loop_values")
        if not (r1 / "pt_next.json").is_file() or not (r1 / "next_loop_context.json").is_file():
            errors.append("next_files_missing")
        if not (r1 / "closed_run_final.json").is_file():
            errors.append("final_missing")
        chain = read_rows(r1 / "closed_run_chain.jsonl")
        if [row.get("stage") for row in chain] != ["loop", "adapt"]:
            errors.append("chain_stages")
        final = load_json(r1 / "closed_run_final.json")
        if final.get("status") != "QI_CLOSED_RUN_APPLIED" or final.get("items_applied") != 3:
            errors.append("final_content")
        if len(read_rows(r1 / "loop_feedback.jsonl")) != 2:
            errors.append("loop_feedback")
        if len(read_rows(r1 / "adapt_log.jsonl")) != 1:
            errors.append("adapt_log")

        r2 = root / "r2"
        write_rows(r2 / "queue.ready.jsonl", [{"policy_key": "x", "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "blocked_loop", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 1 or out.get("status") != "QI_CLOSED_RUN_BLOCKED":
            errors.append("blocked_loop_status")
        if "loop_stage_blocked" not in out.get("blockers", []):
            errors.append("blocked_loop_reason")
        if (r2 / "pt_next.json").exists():
            errors.append("blocked_adapt_should_not_write")

        r3 = root / "r3"
        write_rows(r3 / "queue.ready.jsonl", [{"policy_key": "y", "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "no_chain", ctx(r3), pt(), lic(chain_append_allowed=False))
        if rc != 1 or out.get("status") != "QI_CLOSED_RUN_BLOCKED":
            errors.append("no_chain_status")
        if "chain_append_not_allowed" not in out.get("blockers", []):
            errors.append("no_chain_reason")
        if (r3 / "loop.jsonl").exists() or (r3 / "closed_run_final.json").exists():
            errors.append("no_chain_files")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi closed run v1.1 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

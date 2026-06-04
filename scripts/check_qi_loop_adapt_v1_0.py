#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_loop_adapt_v1_0.py"


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


def ctx(runtime_root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_loop_adapt_enabled": True,
        "apply_loop_adapt": True,
        "runtime_root": str(runtime_root),
        "cycles": 2,
        "base_cycle_budget": 3,
        "max_cycles": 8,
        "max_base_cycle_budget": 12,
    }


def pt(**overrides: Any) -> dict[str, Any]:
    value = {
        "process_tensor_ok": True,
        "execution_pressure": 0.5,
        "coherence_score": 0.4,
        "memory_depth": 2,
        "target_cycle_density": 3.0,
        "recovery_witness_present": False,
        "recovery_witness_missing": True,
        "non_markov_unresolved": False,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_LOOP_ADAPT_LICENSE_READY",
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


def almost(value: Any, target: float) -> bool:
    try:
        return abs(float(value) - target) < 0.000001
    except (TypeError, ValueError):
        return False


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        r1 = root / "r1"
        dump(r1 / "state.json", {"qi_stability": 0.6, "qi_recovery": 0.3, "loop_item_total": 4, "loop_graph_total": 2})
        dump(r1 / "run_summary.json", {"records": 6, "items_applied": 4, "graph_nodes_done": 2, "cycles_requested": 2})
        write_rows(r1 / "loop_feedback.jsonl", [
            {"cycle": 0, "cycle_records": 3, "state_digest": "a"},
            {"cycle": 1, "cycle_records": 3, "state_digest": "b"},
        ])
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_LOOP_ADAPT_APPLIED":
            errors.append("first_status")
        if out.get("records_seen") != 6 or out.get("items_seen") != 4 or out.get("graph_seen") != 2:
            errors.append("stats")
        if not almost(out.get("pressure_after"), 0.48) or not almost(out.get("coherence_after"), 0.444):
            errors.append("pt_values")
        if out.get("memory_depth_after") != 4 or out.get("next_cycles") != 3 or out.get("next_base_cycle_budget") != 4:
            errors.append("next_values")
        next_pt = load_json(r1 / "pt_next.json")
        next_ctx = load_json(r1 / "next_loop_context.json")
        log_rows = read_rows(r1 / "adapt_log.jsonl")
        if not next_pt or not next_ctx or len(log_rows) != 1:
            errors.append("files_missing")
        if not almost(next_pt.get("execution_pressure"), 0.48) or not almost(next_pt.get("coherence_score"), 0.444):
            errors.append("next_pt_file")
        if next_pt.get("memory_depth") != 4 or next_pt.get("recovery_witness_present") is not True:
            errors.append("next_pt_memory_recovery")
        if next_ctx.get("cycles") != 3 or next_ctx.get("base_cycle_budget") != 4:
            errors.append("next_ctx")

        r2 = root / "r2"
        dump(r2 / "state.json", {"qi_stability": 0.1})
        dump(r2 / "run_summary.json", {"records": 1, "items_applied": 1, "graph_nodes_done": 0, "cycles_requested": 1})
        write_rows(r2 / "loop_feedback.jsonl", [{"cycle": 0, "cycle_records": 1}])
        rc, out = run(root, "blocked", ctx(r2), pt(), lic(next_pt_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_LOOP_ADAPT_BLOCKED":
            errors.append("blocked_status")
        if "next_pt_write_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "pt_next.json").exists() or (r2 / "next_loop_context.json").exists() or (r2 / "adapt_log.jsonl").exists():
            errors.append("blocked_wrote")

        r3 = root / "r3"
        rc, out = run(root, "idle", ctx(r3), pt(), lic())
        if rc != 0 or out.get("status") != "QI_LOOP_ADAPT_IDLE":
            errors.append("idle_status")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi loop adapt v1.0 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

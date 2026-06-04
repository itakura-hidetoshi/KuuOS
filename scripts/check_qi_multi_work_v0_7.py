#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_multi_work_v0_7.py"


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
        "qi_multi_work_enabled": True,
        "apply_multi_work": True,
        "runtime_root": str(runtime_root),
        "max_apply": 100,
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
        "license_status": "QI_MULTI_WORK_LICENSE_READY",
        "source_read_allowed": True,
        "state_write_allowed": True,
        "work_log_append_allowed": True,
        "metric_append_allowed": True,
        "note_append_allowed": True,
        "record_write_allowed": True,
        "queue_append_allowed": True,
        "snapshot_write_allowed": True,
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
        write_rows(r1 / "queue.deferred.jsonl", [
            {"item_id": "d1", "item_kind": "metric", "value": 2.0},
            {"item_id": "d2", "item_kind": "note", "text": "from deferred"},
            {"item_id": "d3", "item_kind": "counter", "name": "later", "amount": 1.0},
        ])
        write_rows(r1 / "queue.ready.jsonl", [
            {"policy_key": "m", "item_kind": "metric", "name": "m1", "value": 2.0, "policy_score": 9.0},
            {"policy_key": "n", "item_kind": "note", "text": "hello", "policy_score": 8.0},
            {"policy_key": "r", "item_kind": "record", "policy_score": 7.0, "payload": {"x": 1}},
            {"policy_key": "s", "item_kind": "state_patch", "energy_delta": 1.0, "stability_delta": 0.5, "policy_score": 6.0},
            {"policy_key": "c", "item_kind": "counter", "name": "done", "amount": 2.0, "policy_score": 5.0},
            {"policy_key": "snap", "item_kind": "snapshot", "policy_score": 4.0},
            {"policy_key": "pull", "item_kind": "pull_deferred", "policy_score": 3.0},
        ])
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_MULTI_WORK_APPLIED":
            errors.append("first_status")
        if out.get("applied_count") != 7 or out.get("qi_gain") != 1.4 or out.get("qi_drag") != 0.5:
            errors.append("counts_or_gain")
        counts = out.get("work_counts", {})
        for key in ["metric", "note", "record", "state_patch", "counter", "snapshot", "pull_deferred"]:
            if counts.get(key) != 1:
                errors.append(f"missing_count_{key}")
        metrics = read_rows(r1 / "metrics.jsonl")
        if len(metrics) != 1 or not almost(metrics[0].get("value"), 2.3):
            errors.append("metric_file")
        if "hello" not in (r1 / "notes.md").read_text(encoding="utf-8"):
            errors.append("note_file")
        if not list((r1 / "records").glob("*.json")):
            errors.append("record_file")
        if not list((r1 / "snapshots").glob("*.json")):
            errors.append("snapshot_file")
        state = load_json(r1 / "state.json")
        if not almost(state.get("qi_energy"), 0.9) or not almost(state.get("qi_stability"), 0.95):
            errors.append("state_patch")
        if state.get("counters", {}).get("done") != 3:
            errors.append("counter")
        ready_rows = read_rows(r1 / "queue.ready.jsonl")
        if len(ready_rows) != 9:
            errors.append("pull_deferred")
        if len(read_rows(r1 / "multi_work_log.jsonl")) != 7:
            errors.append("work_log")

        rc, out = run(root, "again", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_MULTI_WORK_APPLIED":
            errors.append("second_status")
        if out.get("applied_count") != 2 or out.get("replay_count") != 7:
            errors.append("second_counts")

        r2 = root / "r2"
        write_rows(r2 / "queue.ready.jsonl", [{"policy_key": "x", "item_kind": "metric", "value": 1.0}])
        rc, out = run(root, "blocked", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 1 or out.get("status") != "QI_MULTI_WORK_BLOCKED":
            errors.append("blocked_status")
        if "non_markov_unresolved" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "metrics.jsonl").exists() or (r2 / "state.json").exists():
            errors.append("blocked_files")

        r3 = root / "r3"
        write_rows(r3 / "queue.ready.jsonl", [{"policy_key": "y", "item_kind": "note", "text": "no"}])
        rc, out = run(root, "no_note", ctx(r3), pt(), lic(note_append_allowed=False))
        if rc != 1 or out.get("status") != "QI_MULTI_WORK_BLOCKED":
            errors.append("license_status")
        if "note_append_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi multi work v0.7 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

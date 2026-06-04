#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_pt_state_step_v0_6.py"


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
        "qi_pt_state_step_enabled": True,
        "apply_pt_state_step": True,
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
        "license_status": "QI_PT_STATE_STEP_LICENSE_READY",
        "source_read_allowed": True,
        "state_write_allowed": True,
        "step_log_append_allowed": True,
        "feedback_append_allowed": True,
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
        write_rows(r1 / "queue.ready.jsonl", [
            {"policy_key": "a", "item_kind": "advance_tick", "policy_score": 2.0},
            {"policy_key": "b", "item_kind": "recover", "policy_score": 3.0},
        ])
        rc, out = run(root, "first", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_PT_STATE_STEP_APPLIED":
            errors.append("first_status")
        if out.get("applied_count") != 2 or out.get("qi_gain") != 1.4 or out.get("qi_drag") != 0.5:
            errors.append("first_counts_or_gains")
        state = load_json(r1 / "state.json")
        if state.get("tick") != 3:
            errors.append("tick_not_changed_by_pt")
        if not almost(state.get("qi_energy"), 0.945):
            errors.append("energy_not_changed_by_pt")
        if not almost(state.get("qi_stability"), 0.405):
            errors.append("stability_not_changed_by_pt")
        if not almost(state.get("qi_recovery"), 0.95):
            errors.append("recovery_not_changed_by_pt")
        if len(read_rows(r1 / "pt_step_log.jsonl")) != 2 or len(read_rows(r1 / "pt_feedback.jsonl")) != 2:
            errors.append("logs_missing")

        rc, out = run(root, "again", ctx(r1), pt(), lic())
        if rc != 0 or out.get("status") != "QI_PT_STATE_STEP_REPLAYED":
            errors.append("replay_status")
        if out.get("applied_count") != 0 or out.get("replay_count") != 2:
            errors.append("replay_counts")
        state2 = load_json(r1 / "state.json")
        if state2.get("tick") != 3 or len(read_rows(r1 / "pt_step_log.jsonl")) != 2:
            errors.append("replay_duplicate")

        r2 = root / "r2"
        write_rows(r2 / "queue.ready.jsonl", [{"policy_key": "c", "item_kind": "advance_tick", "policy_score": 1.0}])
        rc, out = run(root, "blocked", ctx(r2), pt(non_markov_unresolved=True), lic())
        if rc != 1 or out.get("status") != "QI_PT_STATE_STEP_BLOCKED":
            errors.append("blocked_status")
        if "non_markov_unresolved" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "state.json").exists() or (r2 / "pt_step_log.jsonl").exists():
            errors.append("blocked_wrote")

        r3 = root / "r3"
        write_rows(r3 / "queue.ready.jsonl", [{"policy_key": "d", "item_kind": "recover", "policy_score": 1.0}])
        rc, out = run(root, "no_write", ctx(r3), pt(), lic(state_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_PT_STATE_STEP_BLOCKED":
            errors.append("license_status")
        if "state_write_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi PT state step v0.6 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

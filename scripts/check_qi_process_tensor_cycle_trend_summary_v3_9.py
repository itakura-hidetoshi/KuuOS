#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_cycle_trend_summary_v3_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {
        "qi_process_tensor_cycle_trend_summary_enabled": True,
        "apply_process_tensor_cycle_trend_summary": True,
        "runtime_root": str(root),
        "max_summary_records": 20,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_LICENSE_READY",
        "supervisor_receipt_read_allowed": True,
        "supervisor_audit_read_allowed": True,
        "trajectory_read_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def trajectory(n: int = 4) -> dict[str, Any]:
    return {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_READY", "cycle_count": idx + 1} for idx in range(n)]}


def receipt(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY",
        "stop_reason": records[-1].get("stop_reason_after_cycle", "unknown") if records else "unknown",
        "cycle_records": records,
    }


def run(root: pathlib.Path, name: str, r: dict[str, Any] | None, audit: list[dict[str, Any]] | None, traj: dict[str, Any] | None, l: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if r is not None:
        dump(runtime / "qi_process_tensor_cycle_supervisor_receipt.json", r)
    if audit is not None:
        append_jsonl(runtime / "qi_process_tensor_cycle_supervisor_audit.jsonl", audit)
    if traj is not None:
        dump(runtime / "qi_circulation_trajectory_packet.json", traj)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
    dump(lp, l)
    done = subprocess.run(
        [sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_process_tensor_cycle_trend_summary.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_READY", case
    assert not out["blockers"], case
    assert out["records_used"] >= 1, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        stable_records = [
            {"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2},
            {"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 3},
        ]
        code, out, summary = run(root, "stable", receipt(stable_records), [], trajectory(4), lic())
        assert_ready("stable", code, out)
        assert out["trend_class"] == "stable_converging_trend"
        assert out["recommendation"] == "lighten_next_supervision"
        assert out["reliability_score"] >= 0.70
        assert summary["boundary"]["does_not_run_cycles"] is True

        blocked_records = [
            {"stop_reason_after_cycle": "blocked", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_BLOCKED", "trajectory_length": 2},
            {"stop_reason_after_cycle": "blocked", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_BLOCKED", "trajectory_length": 2},
        ]
        code, out, _ = run(root, "blocked", receipt(blocked_records), [], trajectory(2), lic())
        assert_ready("blocked", code, out)
        assert out["trend_class"] == "blocked_dominant_trend"
        assert out["recommendation"] == "repair_blocked_path"

        hold_records = [
            {"stop_reason_after_cycle": "hold_overlay", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_READY", "trajectory_length": 2},
            {"stop_reason_after_cycle": "hold_overlay", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_READY", "trajectory_length": 3},
        ]
        code, out, _ = run(root, "hold", receipt(hold_records), [], trajectory(3), lic())
        assert_ready("hold", code, out)
        assert out["trend_class"] == "hold_dominant_trend"
        assert out["recommendation"] == "review_hold_condition"

        no_progress_records = [
            {"stop_reason_after_cycle": "no_progress", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_READY", "trajectory_length": 2},
            {"stop_reason_after_cycle": "no_progress", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_READY", "trajectory_length": 2},
        ]
        code, out, _ = run(root, "no_progress", receipt(no_progress_records), [], trajectory(2), lic())
        assert_ready("no_progress", code, out)
        assert out["trend_class"] == "no_progress_trend"
        assert out["recommendation"] == "rebalance_next_supervision"

        code, out, _ = run(root, "missing_history", None, None, trajectory(1), lic())
        assert code == 1
        assert "supervisor_history_missing" in out["blockers"]

        code, out, _ = run(root, "blocked_license", receipt(stable_records), [], trajectory(4), lic(summary_write_allowed=False))
        assert code == 1
        assert "summary_write_not_allowed" in out["blockers"]

        code, out, _ = run(root, "bad_max", receipt(stable_records), [], trajectory(4), lic(), {"max_summary_records": 0})
        assert code == 1
        assert "max_summary_records_invalid" in out["blockers"]

        rows = read_rows(root / "stable" / "qi_process_tensor_cycle_trend_summary_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_READY"
    print("qi_process_tensor_cycle_trend_summary_v3_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

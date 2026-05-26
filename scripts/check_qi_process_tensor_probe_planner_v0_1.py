#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANNER_CLI = ROOT / "runtime" / "kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_cmd(args: list[str]):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True, check=False)


def main() -> int:
    errors: list[str] = []
    if not PLANNER_CLI.is_file():
        errors.append(f"missing:{PLANNER_CLI}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        metrics_path = root / "metrics.json"
        raw_path = root / "raw_state.json"
        debt_path = root / "observation_debt.json"
        plan_path = root / "probe_plan.json"
        blocked_metrics_path = root / "blocked_metrics.json"
        blocked_plan_path = root / "blocked_probe_plan.json"

        dump(metrics_path, {
            "metrics_status": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
            "history_depth": 4,
            "transition_visibility_ratio": 0.9,
            "memory_link_density": 0.9,
            "nonmarkov_link_density": 0.8,
            "multi_time_correlation_visibility": 0.85,
            "recoverability_branching_capacity": 0.82,
            "observation_debt_resolution_priority": 0.8,
            "memory_kernel_preservation_score": 0.86,
            "safe_reentry_window_score": 0.84,
            "process_tensor_advantage_level": "high",
            "recommended_next_process_focus": "resolve_observation_debt",
        })
        dump(raw_path, {"process_history": [{"step_id": "p0", "time_slice": "t0"}, {"step_id": "p1", "time_slice": "t1"}]})
        dump(debt_path, {"priority": 0.9, "highest_priority_time_slice": "t_debt"})

        completed = run_cmd([
            sys.executable,
            str(PLANNER_CLI),
            "--metrics",
            str(metrics_path),
            "--raw-state",
            str(raw_path),
            "--observation-debt",
            str(debt_path),
            "--write",
            str(plan_path),
        ])
        if completed.returncode != 0:
            errors.append(f"planner_cli_ready_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not plan_path.is_file():
            errors.append("ready probe plan output missing")
        else:
            plan = load(plan_path)
            if plan.get("probe_plan_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS":
                errors.append("ready-with-warnings status mismatch")
            if plan.get("recommended_probe_type") != "observation_debt_probe":
                errors.append("observation debt probe not selected")
            if plan.get("probe_target_time_slice") != "t_debt":
                errors.append("probe target time slice mismatch")
            if plan.get("probe_expected_observation_debt_reduction", 0) <= 0.5:
                errors.append("expected debt reduction too low")
            if plan.get("probe_plan_only") is not True:
                errors.append("probe_plan_only mismatch")
            if plan.get("read_only") is not True:
                errors.append("read_only mismatch")
            if plan.get("metrics_only") is not True:
                errors.append("metrics_only mismatch")
            if plan.get("authority") != "none":
                errors.append("authority should be none")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
            ]:
                if plan.get(key) is not False:
                    errors.append(f"{key} should be false")

        dump(blocked_metrics_path, {"metrics_status": "QI_PROCESS_TENSOR_ADVANTAGE_BLOCKED", "history_depth": 0})
        completed = run_cmd([
            sys.executable,
            str(PLANNER_CLI),
            "--metrics",
            str(blocked_metrics_path),
            "--raw-state",
            str(raw_path),
            "--write",
            str(blocked_plan_path),
        ])
        if completed.returncode == 0:
            errors.append("blocked planner CLI should return nonzero")
        if not blocked_plan_path.is_file():
            errors.append("blocked probe plan output missing")
        else:
            blocked = load(blocked_plan_path)
            if blocked.get("probe_plan_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_BLOCKED":
                errors.append("blocked status mismatch")
            if blocked.get("recommended_probe_type") != "repair_process_tensor_inputs":
                errors.append("blocked repair probe mismatch")
            if blocked.get("probe_risk_level") != "blocked":
                errors.append("blocked risk mismatch")
            if "process_tensor_advantage_not_ready" not in blocked.get("probe_blockers", []):
                errors.append("blocked reason missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor probe planner check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

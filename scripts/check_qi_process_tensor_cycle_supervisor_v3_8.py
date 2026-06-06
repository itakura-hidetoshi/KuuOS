#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_cycle_supervisor_v3_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {
        "qi_process_tensor_cycle_supervisor_enabled": True,
        "apply_process_tensor_cycle_supervisor": True,
        "runtime_root": str(root),
        "max_supervised_cycles": 2,
        "max_trajectory_records": 10,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY",
        "cycle_runner_run_allowed": True,
        "state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def route_base() -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "branch": "qi-supervisor-test",
        "base_branch": "main",
        "base_sha": "base-sha",
        "pr_number": 1,
        "expected_head_sha": "head-sha",
        "actual_head_sha": "head-sha",
        "mode": "mock",
        "required_checks": [{"name": "mock", "status": "success"}],
        "files": [{"kind": "create_file", "path": "tmp/qi-supervisor.txt", "content": "ok", "message": "Qi supervisor"}],
    }


def trajectory_packet(*, with_route: bool = True) -> dict[str, Any]:
    packet = {
        "trajectory": [
            {
                "status": "QI_SCHEDULED_CLOSED_LOOP_READY",
                "objective_class": "rebalance",
                "converged": False,
                "cycle_count": 3,
                "final_qi_packet": {"qi_flow": 0.65, "coherence_score": 0.70, "circulation_pressure": 0.50, "friction": 0.12},
            }
        ],
        "next_scheduler_packet": {
            "initial_qi_packet": {"qi_flow": 0.74, "coherence_score": 0.76, "circulation_pressure": 0.42, "friction": 0.10},
            "route_base": route_base() if with_route else {"segment": "missing-required-route"},
        },
    }
    return packet


def process_tensor_packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "process_tensor_ok": True,
        "process_tensor_visible": True,
        "transition_continuity_visible": True,
        "memory_continuity_visible": True,
        "nonmarkov_memory_visible": True,
        "memory_depth": 6,
        "execution_pressure": 0.40,
        "coherence_score": 0.82,
        "recovery_witness_present": True,
        "process_history": [
            {"transition_visible": True, "memory_link_visible": True},
            {"transition_visible": True, "nonmarkov_link_visible": True},
            {"transition_visible": True, "memory_link_visible": True},
        ],
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, traj: dict[str, Any] | None, pt: dict[str, Any] | None, l: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if traj is not None:
        dump(runtime / "qi_circulation_trajectory_packet.json", traj)
    if pt is not None:
        dump(runtime / "qi_process_tensor_packet.json", pt)
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
    return done.returncode, load_json(op), load_json(runtime / "qi_process_tensor_cycle_supervisor_state.json"), load_json(runtime / "qi_circulation_trajectory_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY", case
    assert out["completed"] is True, case
    assert out["cycles_run"] >= 1, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, state, traj = run(root, "cap", trajectory_packet(), process_tensor_packet(), lic(), {"max_supervised_cycles": 2})
        assert_ready("cap", code, out)
        assert out["stop_reason"] in {"converged", "cycle_cap_reached", "blocked", "no_progress"}
        assert state["last_status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY"
        assert state["cycles_run"] == out["cycles_run"]
        assert len(out["cycle_records"]) == out["cycles_run"]
        assert len(traj["trajectory"]) >= 2

        code, out, state, traj = run(root, "blocked_route", trajectory_packet(with_route=False), process_tensor_packet(), lic(), {"max_supervised_cycles": 3})
        assert_ready("blocked_route", code, out)
        assert out["stop_reason"] == "blocked"
        assert out["cycles_run"] == 1
        assert out["final_scheduled_status"] == "QI_SCHEDULED_CLOSED_LOOP_BLOCKED"

        code, out, state, traj = run(root, "missing_pt", trajectory_packet(), None, lic())
        assert code == 1
        assert out["status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_BLOCKED"
        assert "process_tensor_packet_missing" in out["blockers"]
        assert out["cycles_run"] == 0

        code, out, _, _ = run(root, "bad_cycles", trajectory_packet(), process_tensor_packet(), lic(), {"max_supervised_cycles": 0})
        assert code == 1
        assert "max_supervised_cycles_invalid" in out["blockers"]

        code, out, _, _ = run(root, "blocked_license", trajectory_packet(), process_tensor_packet(), lic(cycle_runner_run_allowed=False))
        assert code == 1
        assert "cycle_runner_run_not_allowed" in out["blockers"]

        rows = read_rows(root / "cap" / "qi_process_tensor_cycle_supervisor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY"
    print("qi_process_tensor_cycle_supervisor_v3_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_trend_adaptive_supervisor_run_v4_1.py"


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
        "qi_trend_adaptive_supervisor_run_enabled": True,
        "apply_trend_adaptive_supervisor_run": True,
        "runtime_root": str(root),
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_LICENSE_READY",
        "next_supervisor_packet_read_allowed": True,
        "supervisor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def route_base() -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "branch": "qi-adaptive-supervisor-test",
        "base_branch": "main",
        "base_sha": "base-sha",
        "pr_number": 1,
        "expected_head_sha": "head-sha",
        "actual_head_sha": "head-sha",
        "mode": "mock",
        "required_checks": [{"name": "mock", "status": "success"}],
        "files": [{"kind": "create_file", "path": "tmp/qi-adaptive-supervisor.txt", "content": "ok", "message": "Qi adaptive supervisor"}],
    }


def trajectory_packet() -> dict[str, Any]:
    return {
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
            "route_base": route_base(),
        },
    }


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


def next_packet(max_cycles: int = 1, max_records: int = 10, adaptation_class: str = "continue_supervision_packet") -> dict[str, Any]:
    return {
        "version": "next_qi_process_tensor_cycle_supervisor_packet_v4_0",
        "source": "qi_trend_adaptive_supervisor_packet_v4_0",
        "adaptation_class": adaptation_class,
        "recommendation": "continue_current_supervision",
        "trend_class": "bounded_working_trend",
        "reliability_score": 0.62,
        "runtime_context_patch": {"max_supervised_cycles": max_cycles, "max_trajectory_records": max_records},
        "supervisor_context": {"qi_process_tensor_cycle_supervisor_enabled": True, "apply_process_tensor_cycle_supervisor": True, "max_supervised_cycles": max_cycles, "max_trajectory_records": max_records},
        "license_hint": {"license_status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY", "cycle_runner_run_allowed": True, "state_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True},
        "boundary": {"non_authoritative": True, "does_not_run_cycles": True, "does_not_modify_trajectory": True, "suggested_packet_only": True},
    }


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, traj: dict[str, Any] | None, pt: dict[str, Any] | None, l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "next_qi_process_tensor_cycle_supervisor_packet.json", packet)
    if traj is not None:
        dump(runtime / "qi_circulation_trajectory_packet.json", traj)
    if pt is not None:
        dump(runtime / "qi_process_tensor_packet.json", pt)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
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
    assert out["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_READY", case
    assert out["run_performed"] is True, case
    assert out["supervisor_status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, state, traj = run(root, "normal", next_packet(1, 10, "continue_supervision_packet"), trajectory_packet(), process_tensor_packet(), lic())
        assert_ready("normal", code, out)
        assert out["adaptation_class"] == "continue_supervision_packet"
        assert out["max_supervised_cycles"] == 1
        assert state["last_status"] == "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY"
        assert len(traj["trajectory"]) >= 2

        code, out, _, _ = run(root, "invalid_supervisor_context", next_packet(0, 10, "bad_context"), trajectory_packet(), process_tensor_packet(), lic())
        assert code == 1
        assert out["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_BLOCKED"
        assert "cycle_supervisor_not_ready" in out["blockers"]
        assert "max_supervised_cycles_below_one_passed_to_supervisor" in out["warnings"]

        code, out, _, traj = run(root, "missing_packet", None, trajectory_packet(), process_tensor_packet(), lic())
        assert code == 1
        assert "next_supervisor_packet_missing_or_invalid" in out["blockers"]
        assert out["run_performed"] is False
        assert len(traj["trajectory"]) == 1

        code, out, _, _ = run(root, "blocked_license", next_packet(), trajectory_packet(), process_tensor_packet(), lic(supervisor_run_allowed=False))
        assert code == 1
        assert "supervisor_run_not_allowed" in out["blockers"]
        assert out["run_performed"] is False

        code, out, _, _ = run(root, "missing_pt", next_packet(), trajectory_packet(), None, lic())
        assert code == 1
        assert "process_tensor_packet_missing" in out["blockers"]

        rows = read_rows(root / "normal" / "qi_trend_adaptive_supervisor_run_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_READY"
    print("qi_trend_adaptive_supervisor_run_v4_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

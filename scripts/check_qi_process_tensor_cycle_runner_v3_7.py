#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_cycle_runner_v3_7.py"


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
        "qi_process_tensor_cycle_runner_enabled": True,
        "apply_process_tensor_cycle_runner": True,
        "runtime_root": str(root),
        "max_trajectory_records": 10,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_RUNNER_LICENSE_READY",
        "return_loop_run_allowed": True,
        "scheduled_closed_loop_run_allowed": True,
        "trajectory_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def trajectory_packet() -> dict[str, Any]:
    return {
        "trajectory": [
            {
                "status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED",
                "objective_class": "maintain",
                "converged": True,
                "cycle_count": 2,
                "final_qi_packet": {"qi_flow": 0.86, "coherence_score": 0.80, "friction": 0.08},
            }
        ],
        "next_scheduler_packet": {
            "initial_qi_packet": {"qi_flow": 0.78, "coherence_score": 0.76, "circulation_pressure": 0.42, "friction": 0.10},
            "route_base": {"segment": "upper-middle-lower"},
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


def run(root: pathlib.Path, name: str, traj: dict[str, Any] | None, pt: dict[str, Any] | None, l: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
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
    return done.returncode, load_json(op), load_json(runtime / "qi_circulation_trajectory_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_CYCLE_RUNNER_READY", case
    assert out["cycle_completed"] is True, case
    assert out["trajectory_appended"] is True, case
    assert not out["blockers"], case
    assert len(out["stage_records"]) == 3, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, traj = run(root, "stable", trajectory_packet(), process_tensor_packet(), lic())
        assert_ready("stable", code, out)
        assert out["return_loop_status"] == "QI_PROCESS_TENSOR_RETURN_LOOP_READY"
        assert out["scheduled_closed_loop_status"] in {"QI_SCHEDULED_CLOSED_LOOP_READY", "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}
        assert len(traj["trajectory"]) == 2
        assert traj["last_scheduled_closed_loop_receipt"]["source_packet_id"] != "unknown"
        assert traj["cycle_runner_version"] == "kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7"

        seed = trajectory_packet()
        seed["trajectory"] = seed["trajectory"] * 12
        code, out, traj = run(root, "truncate", seed, process_tensor_packet(), lic(), {"max_trajectory_records": 5})
        assert_ready("truncate", code, out)
        assert len(traj["trajectory"]) == 5
        assert out["trajectory_length"] == 5

        code, out, traj = run(root, "hold", trajectory_packet(), process_tensor_packet(non_markov_unresolved=True), lic())
        assert_ready("hold", code, out)
        assert len(traj["trajectory"]) == 2
        assert traj["last_scheduled_closed_loop_receipt"]["status"] in {"QI_SCHEDULED_CLOSED_LOOP_BLOCKED", "QI_SCHEDULED_CLOSED_LOOP_READY", "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}
        assert "scheduled_closed_loop_not_ready_or_converged" in out["warnings"] or out["scheduled_closed_loop_status"] in {"QI_SCHEDULED_CLOSED_LOOP_READY", "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}

        code, out, traj = run(root, "missing_pt", trajectory_packet(), None, lic())
        assert code == 1
        assert out["status"] == "QI_PROCESS_TENSOR_CYCLE_RUNNER_BLOCKED"
        assert "process_tensor_packet_missing" in out["blockers"]
        assert len(traj["trajectory"]) == 1

        code, out, _ = run(root, "blocked_license", trajectory_packet(), process_tensor_packet(), lic(trajectory_append_allowed=False))
        assert code == 1
        assert "trajectory_append_not_allowed" in out["blockers"]

        rows = read_rows(root / "stable" / "qi_process_tensor_cycle_runner_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_PROCESS_TENSOR_CYCLE_RUNNER_READY"
    print("qi_process_tensor_cycle_runner_v3_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

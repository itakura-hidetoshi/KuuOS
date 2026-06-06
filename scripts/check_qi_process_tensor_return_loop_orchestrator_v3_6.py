#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_return_loop_orchestrator_v3_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_process_tensor_return_loop_enabled": True,
        "apply_process_tensor_return_loop": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PROCESS_TENSOR_RETURN_LOOP_LICENSE_READY",
        "trajectory_adaptor_run_allowed": True,
        "scheduler_packet_run_allowed": True,
        "process_tensor_overlay_run_allowed": True,
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


def run(root: pathlib.Path, name: str, traj: dict[str, Any] | None, pt: dict[str, Any] | None, l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
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
    return done.returncode, load_json(op), load_json(runtime / "qi_scheduled_closed_loop_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_RETURN_LOOP_READY", case
    assert out["completed"] is True, case
    assert not out["blockers"], case
    assert len(out["stage_records"]) == 3, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, final_packet = run(root, "stable", trajectory_packet(), process_tensor_packet(), lic())
        assert_ready("stable", code, out)
        assert out["trajectory_status"] == "QI_CIRCULATION_TRAJECTORY_ADAPTOR_READY"
        assert out["scheduler_packet_status"] == "QI_CIRCULATION_SCHEDULER_PACKET_READY"
        assert out["process_tensor_overlay_status"] == "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_READY"
        assert out["adaptation_class"] == "stable_lighten"
        assert out["handoff_class"] == "stable_lighten_handoff"
        assert out["overlay_class"] == "process_tensor_stabilize_overlay"
        assert final_packet["initial_qi_packet"]["process_tensor_overlay_class"] == "process_tensor_stabilize_overlay"
        assert final_packet["route_base"]["process_tensor_memory_depth"] == 6

        code, out, final_packet = run(root, "hold", trajectory_packet(), process_tensor_packet(non_markov_unresolved=True), lic())
        assert_ready("hold", code, out)
        assert out["overlay_class"] == "process_tensor_hold_overlay"
        assert final_packet["initial_qi_packet"]["critical_blocker_present"] is True

        code, out, final_packet = run(root, "missing_pt", trajectory_packet(), None, lic())
        assert code == 1
        assert out["status"] == "QI_PROCESS_TENSOR_RETURN_LOOP_BLOCKED"
        assert "process_tensor_packet_missing" in out["blockers"]
        assert final_packet == {}

        code, out, _ = run(root, "blocked_license", trajectory_packet(), process_tensor_packet(), lic(process_tensor_overlay_run_allowed=False))
        assert code == 1
        assert "process_tensor_overlay_run_not_allowed" in out["blockers"]

        rows = read_rows(root / "stable" / "qi_process_tensor_return_loop_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_PROCESS_TENSOR_RETURN_LOOP_READY"
    print("qi_process_tensor_return_loop_orchestrator_v3_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

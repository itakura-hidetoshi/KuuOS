#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_cycle_aware_super_executor_v9_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 5) -> dict[str, Any]:
    return {"qi_github_actions_cycle_aware_super_executor_enabled": True, "apply_github_actions_cycle_aware_super_executor": True, "runtime_root": str(root), "max_cycle_aware_super_executor_phases": max_phases, "max_inner_super_orchestrator_phases": 5, "max_inner_routed_e2e_phases": 4, "max_inner_e2e_phases": 8}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_CYCLE_AWARE_SUPER_EXECUTOR_LICENSE_READY", "super_orchestrator_run_allowed": True, "next_cycle_executor_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def execution_packet() -> dict[str, Any]:
    return {"execution_allowed": True, "next_cycle_state": "closed", "execution_state": "cycle_closed", "connector_action": "none"}


def next_packet(state: str = "closed") -> dict[str, Any]:
    return {"next_cycle_allowed": True, "route_state": "close_autopilot_cycle", "next_cycle_state": state, "next_connector_action": "none"}


def route() -> dict[str, Any]:
    return {"route_allowed": True, "final_state": "action_completed", "route_state": "close_autopilot_cycle", "next_expected": "close"}


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 5) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, max_phases))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_next_cycle_execution_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_CYCLE_AWARE_SUPER_EXECUTOR_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "execution_present", {"qi_github_actions_next_cycle_execution_packet.json": execution_packet()}, lic())
        assert_ready("execution_present", code, out)
        assert out["final_stage"] == "execution_packet_present"
        assert out["execution_state"] == "cycle_closed"
        assert out["phases_run"] == 0

        code, out, packet = run(root, "next_to_execution", {"qi_github_actions_route_next_cycle_packet.json": next_packet("closed")}, lic())
        assert_ready("next_to_execution", code, out)
        assert out["final_stage"] == "run_next_cycle_executor"
        assert out["execution_state"] == "cycle_closed"
        assert packet["execution_allowed"] is True

        code, out, packet = run(root, "route_to_execution", {"qi_github_actions_policy_action_final_route_packet.json": route()}, lic())
        assert_ready("route_to_execution", code, out)
        assert out["execution_state"] == "cycle_closed"
        assert packet["execution_allowed"] is True

        code, out, packet = run(root, "initial_wait", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial_wait", code, out)
        assert out["final_stage"] == "run_super_orchestrator"
        assert out["connector_action"] == "GitHub.get_pr_info"
        assert packet == {}

        code, out, packet = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_cycle_aware_super_executor_phases_invalid" in out["blockers"]

        code, out, packet = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(next_cycle_executor_run_allowed=False))
        assert code == 1
        assert "next_cycle_executor_run_not_allowed" in out["blockers"]
    print("qi_github_actions_cycle_aware_super_executor_v9_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

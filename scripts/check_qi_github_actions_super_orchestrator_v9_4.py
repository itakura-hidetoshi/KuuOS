#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_super_orchestrator_v9_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 5) -> dict[str, Any]:
    return {"qi_github_actions_super_orchestrator_enabled": True, "apply_github_actions_super_orchestrator": True, "runtime_root": str(root), "max_super_orchestrator_phases": max_phases, "max_inner_routed_e2e_phases": 4, "max_inner_e2e_phases": 8}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_SUPER_ORCHESTRATOR_LICENSE_READY", "routed_e2e_run_allowed": True, "route_planner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def next_cycle(state: str = "closed") -> dict[str, Any]:
    return {"next_cycle_allowed": True, "route_state": "close_autopilot_cycle", "next_cycle_state": state, "next_connector_action": "none"}


def route(state: str = "close_autopilot_cycle") -> dict[str, Any]:
    return {"route_allowed": True, "final_state": "action_completed", "route_state": state, "next_expected": "next"}


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": True, "sha": "abc"}}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_route_next_cycle_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_SUPER_ORCHESTRATOR_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, next_packet = run(root, "next_present", {"qi_github_actions_route_next_cycle_packet.json": next_cycle()}, lic())
        assert_ready("next_present", code, out)
        assert out["final_stage"] == "next_cycle_present"
        assert out["next_cycle_state"] == "closed"
        assert out["phases_run"] == 0

        code, out, next_packet = run(root, "route_to_next", {"qi_github_actions_policy_action_final_route_packet.json": route()}, lic())
        assert_ready("route_to_next", code, out)
        assert out["final_stage"] == "run_route_planner"
        assert out["next_cycle_state"] == "closed"
        assert next_packet["next_cycle_allowed"] is True

        code, out, next_packet = run(root, "receipt_to_next", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("receipt_to_next", code, out)
        assert out["next_cycle_state"] == "closed"
        assert next_packet["next_cycle_allowed"] is True

        code, out, next_packet = run(root, "initial_wait", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial_wait", code, out)
        assert out["final_stage"] == "run_routed_e2e"
        assert out["next_connector_action"] == "GitHub.get_pr_info"
        assert next_packet == {}

        code, out, next_packet = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_super_orchestrator_phases_invalid" in out["blockers"]

        code, out, next_packet = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(route_planner_run_allowed=False))
        assert code == 1
        assert "route_planner_run_not_allowed" in out["blockers"]
    print("qi_github_actions_super_orchestrator_v9_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

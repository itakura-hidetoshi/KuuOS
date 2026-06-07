#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_full_terminal_autopilot_v11_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 6) -> dict[str, Any]:
    return {"qi_github_actions_full_terminal_autopilot_enabled": True, "apply_github_actions_full_terminal_autopilot": True, "runtime_root": str(root), "max_full_terminal_autopilot_phases": max_phases, "max_inner_dispatch_supercycle_phases": 8, "max_inner_unified_closed_loop_phases": 6}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_LICENSE_READY", "dispatch_supercycle_run_allowed": True, "terminal_finalizer_run_allowed": True, "terminal_scheduler_executor_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 6) -> tuple[int, dict[str, Any], dict[str, Any]]:
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_terminal_scheduler_execution_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_READY", case
    assert not out["blockers"], case


def execution() -> dict[str, Any]:
    return {"terminal_scheduler_execution_allowed": True, "scheduler_action": "close_scheduler_cycle", "execution_state": "scheduler_cycle_closed", "connector_action": "none"}


def scheduler() -> dict[str, Any]:
    return {"scheduler_packet_allowed": True, "terminal_state": "action_completed", "terminal_kind": "done", "scheduler_action": "close_scheduler_cycle", "connector_action": "none", "action_prepared": "merge_pull_request", "source_kind": "test"}


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request"}


def dispatch_receipt() -> dict[str, Any]:
    return {"status": "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_READY", "supercycle_state": "await_dispatch_external_result", "connector_action": "GitHub.get_pr_info", "action_prepared": "policy_reentry_pr_info", "stop_reason": "await_dispatch_external_result"}


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "execution_present", {"qi_github_actions_terminal_scheduler_execution_packet.json": execution()}, lic())
        assert_ready("execution_present", code, out)
        assert out["final_stage"] == "terminal_execution_present"
        assert out["execution_state"] == "scheduler_cycle_closed"
        assert out["phases_run"] == 0

        code, out, packet = run(root, "scheduler_to_execution", {"qi_github_actions_terminal_scheduler_packet.json": scheduler()}, lic())
        assert_ready("scheduler_to_execution", code, out)
        assert out["final_stage"] == "terminal_execution_present" or out["final_stage"] == "run_terminal_scheduler_executor"
        assert packet["execution_state"] == "scheduler_cycle_closed"

        code, out, packet = run(root, "final_to_execution", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("final_to_execution", code, out)
        assert out["execution_state"] == "scheduler_cycle_closed"
        assert packet["scheduler_action"] == "close_scheduler_cycle"

        code, out, packet = run(root, "await_to_execution", {"qi_github_actions_dispatch_supercycle_receipt.json": dispatch_receipt()}, lic())
        assert_ready("await_to_execution", code, out)
        assert out["execution_state"] == "external_dispatch_ready"
        assert packet["connector_action"] == "GitHub.get_pr_info"

        code, out, packet = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["final_stage"] in {"run_dispatch_supercycle", "run_terminal_finalizer", "run_terminal_scheduler_executor", "terminal_execution_present"}

        code, out, packet = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_full_terminal_autopilot_phases_invalid" in out["blockers"]

        code, out, packet = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(terminal_scheduler_executor_run_allowed=False))
        assert code == 1
        assert "terminal_scheduler_executor_run_not_allowed" in out["blockers"]
    print("qi_github_actions_full_terminal_autopilot_v11_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_full_terminal_output_v11_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 5) -> dict[str, Any]:
    return {"qi_github_actions_full_terminal_output_enabled": True, "apply_github_actions_full_terminal_output": True, "runtime_root": str(root), "max_full_terminal_output_phases": max_phases, "max_inner_full_terminal_autopilot_phases": 6}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_FULL_TERMINAL_OUTPUT_LICENSE_READY", "full_terminal_autopilot_run_allowed": True, "terminal_execution_bridge_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 5) -> tuple[int, dict[str, Any]]:
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
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_FULL_TERMINAL_OUTPUT_READY", case
    assert not out["blockers"], case


def output_packet() -> dict[str, Any]:
    return {"terminal_execution_output_allowed": True, "execution_state": "scheduler_cycle_closed", "output_state": "cycle_closed_final", "connector_action": "none"}


def execution_packet() -> dict[str, Any]:
    return {"terminal_scheduler_execution_allowed": True, "scheduler_action": "close_scheduler_cycle", "execution_state": "scheduler_cycle_closed", "connector_action": "none"}


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request"}


def dispatch_receipt() -> dict[str, Any]:
    return {"status": "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_READY", "supercycle_state": "await_dispatch_external_result", "connector_action": "GitHub.get_pr_info", "action_prepared": "policy_reentry_pr_info", "stop_reason": "await_dispatch_external_result"}


def dispatch_packet() -> dict[str, Any]:
    return {"dispatch_allowed": True, "dispatch_kind": "policy_reentry_pr_info", "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "raw_result_expected_file": "qi_github_actions_dispatch_pr_info_raw_result_packet.json"}


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "output_present", {"qi_github_actions_terminal_cycle_closed_packet.json": output_packet()}, lic())
        assert_ready("output_present", code, out)
        assert out["final_stage"] == "terminal_output_present"
        assert out["output_state"] == "cycle_closed_final"
        assert out["phases_run"] == 0

        code, out = run(root, "execution_to_output", {"qi_github_actions_terminal_scheduler_execution_packet.json": execution_packet()}, lic())
        assert_ready("execution_to_output", code, out)
        assert out["output_state"] == "cycle_closed_final"

        code, out = run(root, "final_to_output", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("final_to_output", code, out)
        assert out["output_state"] == "cycle_closed_final"

        code, out = run(root, "await_to_output", {"qi_github_actions_dispatch_supercycle_receipt.json": dispatch_receipt(), "qi_github_actions_unified_dispatch_packet.json": dispatch_packet()}, lic())
        assert_ready("await_to_output", code, out)
        assert out["output_state"] == "external_dispatch_ready"
        assert out["connector_action"] == "GitHub.get_pr_info"

        code, out = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["final_stage"] in {"run_full_terminal_autopilot", "run_terminal_execution_bridge", "terminal_output_present"}

        code, out = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_full_terminal_output_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(terminal_execution_bridge_run_allowed=False))
        assert code == 1
        assert "terminal_execution_bridge_run_not_allowed" in out["blockers"]
    print("qi_github_actions_full_terminal_output_v11_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

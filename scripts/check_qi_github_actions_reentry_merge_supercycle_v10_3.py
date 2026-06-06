#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_reentry_merge_supercycle_v10_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 10) -> dict[str, Any]:
    return {"qi_github_actions_reentry_merge_supercycle_enabled": True, "apply_github_actions_reentry_merge_supercycle": True, "runtime_root": str(root), "max_reentry_merge_supercycle_phases": max_phases}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_LICENSE_READY", "reentry_evaluator_run_allowed": True, "pr_info_result_bridge_run_allowed": True, "policy_action_handoff_run_allowed": True, "policy_action_external_call_run_allowed": True, "policy_action_external_result_run_allowed": True, "policy_action_final_receipt_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def workflow_success() -> list[dict[str, Any]]:
    return [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]


def reentry_packet() -> dict[str, Any]:
    runs = workflow_success()
    return {"policy_reentry_allowed": True, "reentry_state": "policy_reentry_ready", "query_context": {"repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}, "status_summary": {"all_success": True, "any_failed": False, "any_pending": False, "all_completed": True, "workflow_run_count": len(runs), "workflow_runs": runs}, "workflow_runs": runs}


def pr_info_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}}


def pr_info_raw() -> dict[str, Any]:
    return {"connector_action": "GitHub.get_pr_info", "repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "mergeable": True, "head_sha": "abc", "base": "main"}


def merge_raw_result() -> dict[str, Any]:
    return {"connector_action": "GitHub.merge_pull_request", "merged": True, "sha": "merge-sha", "message": "ok"}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 10) -> tuple[int, dict[str, Any]]:
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
    assert out["status"] == "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "reentry_to_pr_info_wait", {"qi_github_actions_policy_reentry_packet.json": reentry_packet()}, lic())
        assert_ready("reentry_to_pr_info_wait", code, out)
        assert out["final_stage"] == "await_pr_info_external_result"
        assert out["connector_action"] == "GitHub.get_pr_info"

        files = {"qi_github_actions_policy_reentry_external_call_packet.json": pr_info_call(), "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json": pr_info_raw()}
        code, out = run(root, "pr_info_to_merge_wait", files, lic())
        assert_ready("pr_info_to_merge_wait", code, out)
        assert out["final_stage"] == "await_policy_action_external_result"
        assert out["connector_action"] == "GitHub.merge_pull_request"
        assert out["action_prepared"] == "merge_pull_request"

        files = {"qi_github_actions_policy_action_external_call_packet.json": {"external_call_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "action_result_expected_file": "qi_github_actions_policy_action_merge_result_packet.json"}, "qi_github_actions_policy_action_external_call_raw_result_packet.json": merge_raw_result()}
        code, out = run(root, "merge_result_to_final", files, lic())
        assert_ready("merge_result_to_final", code, out)
        assert out["final_stage"] == "final_receipt_present" or out["final_stage"] == "run_policy_action_final_receipt"
        assert out["supercycle_state"] == "action_completed"

        code, out = run(root, "final_present", {"qi_github_actions_policy_action_final_receipt_packet.json": {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": True, "sha": "merge-sha"}}}, lic())
        assert_ready("final_present", code, out)
        assert out["final_stage"] == "final_receipt_present"
        assert out["phases_run"] == 0

        code, out = run(root, "missing_entry", {}, lic())
        assert code == 1
        assert "policy_reentry_or_followup_packet_missing" in out["blockers"]

        code, out = run(root, "bad_cap", {"qi_github_actions_policy_reentry_packet.json": reentry_packet()}, lic(), 0)
        assert code == 1
        assert "max_reentry_merge_supercycle_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_policy_reentry_packet.json": reentry_packet()}, lic(pr_info_result_bridge_run_allowed=False))
        assert code == 1
        assert "pr_info_result_bridge_run_not_allowed" in out["blockers"]
    print("qi_github_actions_reentry_merge_supercycle_v10_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

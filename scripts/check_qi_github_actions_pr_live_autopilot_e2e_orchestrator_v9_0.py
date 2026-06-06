#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_autopilot_e2e_orchestrator_v9_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 8) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_autopilot_e2e_orchestrator_enabled": True, "apply_github_actions_pr_live_autopilot_e2e_orchestrator": True, "runtime_root": str(root), "max_autopilot_e2e_phases": max_phases}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_LICENSE_READY", "autopilot_run_allowed": True, "autopilot_ingest_allowed": True, "policy_action_handoff_allowed": True, "policy_action_external_call_allowed": True, "policy_action_external_result_allowed": True, "policy_action_final_receipt_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def policy_ready_handoff() -> dict[str, Any]:
    return {"handoff_allowed": True, "autopilot_state": "policy_ready", "policy_decision": "policy_all_green", "action_prepared": "merge_pull_request"}


def live_query() -> dict[str, Any]:
    return {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "head_sha": "abc", "merge_method": "merge"}


def pr_packet() -> dict[str, Any]:
    return {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc"}


def merge_result() -> dict[str, Any]:
    return {"connector_action": "GitHub.merge_pull_request", "merged": True, "sha": "abc", "message": "ok"}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 8) -> tuple[int, dict[str, Any]]:
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
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["final_stage"] == "await_autopilot_external_connector"
        assert out["connector_action"] == "GitHub.get_pr_info"

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": policy_ready_handoff(), "qi_github_actions_pr_live_query_packet.json": live_query(), "qi_github_actions_raw_pr_info_packet.json": pr_packet()}
        code, out = run(root, "policy_ready", files, lic())
        assert_ready("policy_ready", code, out)
        assert out["final_stage"] == "await_policy_action_external_result"
        assert out["connector_action"] == "GitHub.merge_pull_request"

        files = {"qi_github_actions_policy_action_external_call_packet.json": {"external_call_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "action_result_expected_file": "qi_github_actions_policy_action_merge_result_packet.json"}, "qi_github_actions_policy_action_external_call_raw_result_packet.json": merge_result()}
        code, out = run(root, "action_result", files, lic())
        assert_ready("action_result", code, out)
        assert out["final_stage"] == "synthesize_final_receipt"
        assert out["final_state"] == "action_completed"

        code, out = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_autopilot_e2e_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(policy_action_external_call_allowed=False))
        assert code == 1
        assert "policy_action_external_call_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_autopilot_e2e_orchestrator_v9_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

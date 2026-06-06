#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_autopilot_policy_action_handoff_v8_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_autopilot_policy_action_handoff_enabled": True, "apply_github_actions_autopilot_policy_action_handoff": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_LICENSE_READY", "handoff_packet_read_allowed": True, "context_packet_read_allowed": True, "action_handoff_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query(**overrides: Any) -> dict[str, Any]:
    value = {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "head_sha": "abc", "commit_sha": "abc", "merge_method": "merge"}
    value.update(overrides)
    return value


def pr(**overrides: Any) -> dict[str, Any]:
    value = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc", "base": "main"}
    value.update(overrides)
    return value


def status_packet(conclusion: str = "failure") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": conclusion}]}


def handoff(prepared: str, decision: str = "policy_all_green") -> dict[str, Any]:
    return {"handoff_allowed": True, "autopilot_state": "policy_ready", "policy_decision": decision, "action_prepared": prepared}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_autopilot_policy_action_handoff_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_READY", case
    assert out["action_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["action_handoff_allowed"] is True, case
    assert packet["boundary"]["requires_policy_ready_handoff"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("merge_pull_request"), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out, packet = run(root, "merge", files, lic())
        assert_ready("merge", code, out, packet)
        assert out["action_kind"] == "merge_pull_request"
        assert packet["connector_action"] == "GitHub.merge_pull_request"
        assert packet["connector_payload"]["expected_head_sha"] == "abc"

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("rerun_failed_workflow_run_jobs", "policy_failed_rerun"), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_status_packet.json": status_packet("failure")}
        code, out, packet = run(root, "rerun", files, lic())
        assert_ready("rerun", code, out, packet)
        assert out["action_kind"] == "rerun_failed_workflow_run_jobs"
        assert packet["connector_action"] == "GitHub.rerun_failed_workflow_run_jobs"
        assert packet["connector_payload"]["run_id"] == 10

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("commit_workflow_runs_reobserve", "policy_pending_reobserve"), "qi_github_actions_pr_live_query_packet.json": query(commit_sha="abc")}
        code, out, packet = run(root, "reobserve", files, lic())
        assert_ready("reobserve", code, out, packet)
        assert out["action_kind"] == "reobserve_commit_workflow_runs"
        assert packet["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert packet["connector_payload"]["commit_sha"] == "abc"

        bad_handoff = {"handoff_allowed": True, "autopilot_state": "await_external_connector", "action_prepared": "merge_pull_request"}
        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": bad_handoff, "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out, packet = run(root, "not_policy_ready", files, lic())
        assert code == 1
        assert "handoff_state_not_policy_ready" in out["blockers"]
        assert packet == {}

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("merge_pull_request"), "qi_github_actions_pr_live_query_packet.json": query(head_sha="", expected_head_sha=""), "qi_github_actions_raw_pr_info_packet.json": pr(head_sha="")}
        code, out, packet = run(root, "missing_head", files, lic())
        assert code == 1
        assert "expected_head_sha_missing" in out["blockers"]
        assert packet == {}

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("merge_pull_request"), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out, packet = run(root, "license_block", files, lic(action_handoff_packet_write_allowed=False))
        assert code == 1
        assert "action_handoff_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_autopilot_policy_action_handoff_v8_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_action_full_cycle_runner_v9_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 6) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_full_cycle_runner_enabled": True, "apply_github_actions_policy_action_full_cycle_runner": True, "runtime_root": str(root), "max_policy_action_full_cycle_phases": max_phases}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FULL_CYCLE_RUNNER_LICENSE_READY", "policy_handoff_run_allowed": True, "external_call_bridge_run_allowed": True, "external_result_bridge_run_allowed": True, "final_receipt_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query() -> dict[str, Any]:
    return {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "head_sha": "abc", "commit_sha": "abc", "merge_method": "merge"}


def pr() -> dict[str, Any]:
    return {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc", "base": "main"}


def policy_handoff(prepared: str = "merge_pull_request", decision: str = "policy_all_green") -> dict[str, Any]:
    return {"handoff_allowed": True, "autopilot_state": "policy_ready", "policy_decision": decision, "action_prepared": prepared}


def action_handoff() -> dict[str, Any]:
    return {"action_handoff_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge", "expected_head_sha": "abc"}}


def external_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge", "expected_head_sha": "abc"}, "action_result_expected_file": "qi_github_actions_policy_action_merge_result_packet.json"}


def raw_merge_result(merged: bool = True) -> dict[str, Any]:
    return {"connector_action": "GitHub.merge_pull_request", "merged": merged, "sha": "abc", "message": "ok"}


def action_result() -> dict[str, Any]:
    return {"action_result_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": True, "sha": "abc", "message": "ok"}}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 6) -> tuple[int, dict[str, Any]]:
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
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_ACTION_FULL_CYCLE_RUNNER_READY", case
    assert not out["blockers"], case
    assert out["phases_run"] >= 1, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": policy_handoff(), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out = run(root, "policy_ready", files, lic())
        assert_ready("policy_ready", code, out)
        assert out["stop_reason"] == "await_policy_action_external_result"
        assert out["action_kind"] == "merge_pull_request"
        assert (root / "policy_ready" / "qi_github_actions_policy_action_external_call_packet.json").is_file()

        files = {"qi_github_actions_autopilot_policy_action_handoff_packet.json": action_handoff()}
        code, out = run(root, "action_handoff", files, lic())
        assert_ready("action_handoff", code, out)
        assert out["stop_reason"] == "await_policy_action_external_result"
        assert out["connector_action"] == "GitHub.merge_pull_request"

        files = {"qi_github_actions_policy_action_external_call_packet.json": external_call()}
        code, out = run(root, "await_external", files, lic())
        assert_ready("await_external", code, out)
        assert out["final_stage"] == "await_policy_action_external_result"
        assert out["stop_reason"] == "await_policy_action_external_result"

        files = {"qi_github_actions_policy_action_external_call_packet.json": external_call(), "qi_github_actions_policy_action_external_call_raw_result_packet.json": raw_merge_result(True)}
        code, out = run(root, "raw_result", files, lic())
        assert_ready("raw_result", code, out)
        assert out["stop_reason"] == "final_receipt_ready"
        assert out["final_state"] == "action_completed"
        assert (root / "raw_result" / "qi_github_actions_policy_action_final_receipt_packet.json").is_file()

        files = {"qi_github_actions_policy_action_merge_result_packet.json": action_result()}
        code, out = run(root, "action_result", files, lic())
        assert_ready("action_result", code, out)
        assert out["final_state"] == "action_completed"
        assert out["next_expected"] == "close_autopilot_cycle"

        files = {"qi_github_actions_policy_action_external_call_packet.json": external_call(), "qi_github_actions_policy_action_external_call_raw_result_packet.json": raw_merge_result(False)}
        code, out = run(root, "bad_raw", files, lic())
        assert code == 1
        assert "policy_action_external_result_bridge_not_ready" in out["blockers"]

        files = {"qi_github_actions_pr_live_autopilot_handoff_packet.json": policy_handoff(), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out = run(root, "license_block", files, lic(external_call_bridge_run_allowed=False))
        assert code == 1
        assert "external_call_bridge_run_not_allowed" in out["blockers"]
    print("qi_github_actions_policy_action_full_cycle_runner_v9_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

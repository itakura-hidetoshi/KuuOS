#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_autopilot_packet_runner_v8_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_autopilot_packet_runner_enabled": True, "apply_github_actions_pr_live_autopilot_packet_runner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_LICENSE_READY", "autopilot_query_read_allowed": True, "live_query_write_allowed": True, "external_cycle_run_allowed": True, "handoff_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query(**overrides: Any) -> dict[str, Any]:
    value = {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}
    value.update(overrides)
    return value


def pr_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "dispatch_target": "pr_info", "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "dispatch_result_expected_file": "qi_github_actions_pr_live_dispatch_pr_info_result.json"}


def runs_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "dispatch_result_expected_file": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json"}


def pr_raw() -> dict[str, Any]:
    return {"number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS"}


def raw_pr_packet() -> dict[str, Any]:
    return {"number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS", "base": "main"}


def runs_raw(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_live_autopilot_handoff_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], handoff: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_READY", case
    assert out["handoff_packet_written"] is True, case
    assert not out["blockers"], case
    assert handoff["handoff_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, handoff = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out, handoff)
        assert out["autopilot_state"] == "await_external_connector"
        assert out["connector_action"] == "GitHub.get_pr_info"
        assert handoff["next_expected"].startswith("call connector")

        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_pr_live_external_call_packet.json": pr_call(), "qi_github_actions_pr_live_external_call_raw_result_packet.json": pr_raw()}
        code, out, handoff = run(root, "pr_result", files, lic())
        assert_ready("pr_result", code, out, handoff)
        assert out["autopilot_state"] == "await_external_connector"
        assert out["connector_action"] == "GitHub.fetch_commit_workflow_runs"

        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": raw_pr_packet(), "qi_github_actions_pr_live_external_call_packet.json": runs_call(), "qi_github_actions_pr_live_external_call_raw_result_packet.json": runs_raw("success")}
        code, out, handoff = run(root, "runs_result", files, lic())
        assert_ready("runs_result", code, out, handoff)
        assert out["autopilot_state"] == "policy_ready"
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        code, out, handoff = run(root, "bad_query", {"qi_github_actions_pr_live_autopilot_query_packet.json": query(repo_full_name="bad")}, lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]

        code, out, handoff = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(external_cycle_run_allowed=False))
        assert code == 1
        assert "external_cycle_run_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_autopilot_packet_runner_v8_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

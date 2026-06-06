#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_external_cycle_runner_v8_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 8) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_external_cycle_runner_enabled": True, "apply_github_actions_pr_live_external_cycle_runner": True, "runtime_root": str(root), "max_pr_live_external_cycle_phases": max_phases, "max_pr_live_full_cycle_phases": 6, "max_pr_live_inner_loop_phases": 3}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_LICENSE_READY", "full_cycle_run_allowed": True, "external_call_bridge_run_allowed": True, "external_result_bridge_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query(**overrides: Any) -> dict[str, Any]:
    value = {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}
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
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_READY", case
    assert not out["blockers"], case
    assert out["phases_run"] >= 1, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "initial", {"qi_github_actions_pr_live_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["stop_reason"] == "await_external_call_result"
        assert out["request_action"] == "GitHub.get_pr_info"
        assert (root / "initial" / "qi_github_actions_pr_live_external_call_packet.json").is_file()

        files = {"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_pr_live_external_call_packet.json": pr_call(), "qi_github_actions_pr_live_external_call_raw_result_packet.json": pr_raw()}
        code, out = run(root, "pr_external_result", files, lic())
        assert_ready("pr_external_result", code, out)
        assert out["stop_reason"] == "await_external_call_result"
        assert out["request_action"] == "GitHub.fetch_commit_workflow_runs"
        assert (root / "pr_external_result" / "qi_github_actions_pr_live_dispatch_pr_info_result.json").is_file()
        assert (root / "pr_external_result" / "qi_github_actions_pr_live_external_call_packet.json").is_file()

        files = {"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": raw_pr_packet(), "qi_github_actions_pr_live_external_call_packet.json": runs_call(), "qi_github_actions_pr_live_external_call_raw_result_packet.json": runs_raw("success")}
        code, out = run(root, "runs_external_result", files, lic())
        assert_ready("runs_external_result", code, out)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        files = {"qi_github_actions_pr_live_external_call_packet.json": pr_call()}
        code, out = run(root, "await_existing_call", files, lic())
        assert_ready("await_existing_call", code, out)
        assert out["final_stage"] == "await_external_call"
        assert out["stop_reason"] == "await_external_call_result"
        assert out["request_action"] == "GitHub.get_pr_info"

        code, out = run(root, "bad_cap", {"qi_github_actions_pr_live_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_pr_live_external_cycle_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_pr_live_query_packet.json": query()}, lic(external_call_bridge_run_allowed=False))
        assert code == 1
        assert "external_call_bridge_run_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_external_cycle_runner_v8_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

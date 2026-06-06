#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_result_adapter_v7_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, continue_planner: bool = True) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_result_adapter_enabled": True, "apply_github_actions_pr_live_result_adapter": True, "runtime_root": str(root), "continue_planner": continue_planner}


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_LICENSE_READY", "connector_request_read_allowed": True, "connector_result_read_allowed": True, "adapted_packet_write_allowed": True, "planner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_result"] = True
    value.update(overrides)
    return value


def query() -> dict[str, Any]:
    return {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def pr_request() -> dict[str, Any]:
    return {"connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "result_expected_file": "qi_github_actions_raw_pr_info_packet.json"}


def runs_request() -> dict[str, Any]:
    return {"connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_raw_commit_workflow_runs_packet.json"}


def pr_result() -> dict[str, Any]:
    return {"number": 1, "state": "open", "merged": False, "mergeable": True, "draft": False, "head_sha": "abc", "base": "main", "repo_full_name": "itakura-hidetoshi/KuuOS"}


def runs_result(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def run(root: pathlib.Path, name: str, request: dict[str, Any] | None, result: dict[str, Any] | None, license_packet: dict[str, Any], continue_planner: bool = True, extra_files: dict[str, dict[str, Any]] | None = None) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if request is not None:
        dump(runtime / "qi_github_actions_pr_live_connector_request.json", request)
    if result is not None:
        dump(runtime / "qi_github_actions_pr_live_connector_result_packet.json", result)
    for file_name, payload in (extra_files or {}).items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, continue_planner))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_raw_pr_info_packet.json"), load_json(runtime / "qi_github_actions_raw_commit_workflow_runs_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_READY", case
    assert out["adapted_packet_written"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, pr_packet, runs_packet = run(root, "pr", pr_request(), pr_result(), lic("pr_info"), extra_files={"qi_github_actions_pr_live_query_packet.json": query()})
        assert_ready("pr", code, out)
        assert out["result_kind"] == "pr_info"
        assert pr_packet["head_sha"] == "abc"
        assert out["planner_stage"] == "request_commit_workflow_runs"
        assert runs_packet == {}

        code, out, pr_packet, runs_packet = run(root, "runs", runs_request(), runs_result("success"), lic("commit_workflow_runs"), extra_files={"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr_result()})
        assert_ready("runs", code, out)
        assert out["result_kind"] == "commit_workflow_runs"
        assert runs_packet["workflow_runs"]
        assert out["policy_decision"] == "policy_all_green"

        nested = {"connector_result": {"workflow_runs": [{"id": 20, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "failure"}], "required_workflows": ["Qi Process Tensor Review Checks"]}}
        code, out, pr_packet, runs_packet = run(root, "nested_runs", runs_request(), nested, lic("commit_workflow_runs"), extra_files={"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr_result()})
        assert_ready("nested_runs", code, out)
        assert out["policy_decision"] == "policy_failed_rerun"

        code, out, pr_packet, runs_packet = run(root, "missing_kind", {"connector_action": "GitHub.unknown", "connector_payload": {}}, {"ok": True}, lic("pr_info"))
        assert code == 1
        assert "result_kind_not_allowlisted" in out["blockers"]

        code, out, pr_packet, runs_packet = run(root, "missing_head", pr_request(), {"number": 1, "repo_full_name": "itakura-hidetoshi/KuuOS"}, lic("pr_info"), False)
        assert code == 1
        assert "head_sha_missing" in out["blockers"]

        code, out, pr_packet, runs_packet = run(root, "license_block", pr_request(), pr_result(), lic())
        assert code == 1
        assert "pr_info_not_allowed_by_pr_live_result_adapter_license" in out["blockers"]
    print("qi_github_actions_pr_live_result_adapter_v7_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

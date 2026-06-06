#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_request_planner_v7_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_request_planner_enabled": True, "apply_github_actions_pr_live_request_planner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_LICENSE_READY", "query_packet_read_allowed": True, "connector_request_write_allowed": True, "collector_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query(**overrides: Any) -> dict[str, Any]:
    value = {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}
    value.update(overrides)
    return value


def raw_pr(**overrides: Any) -> dict[str, Any]:
    value = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "base": "main"}
    value.update(overrides)
    return value


def raw_runs(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_info_connector_request.json"), load_json(runtime / "qi_github_actions_commit_workflow_runs_connector_request.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, pr_req, runs_req = run(root, "pr_request", {"qi_github_actions_pr_live_query_packet.json": query()}, lic())
        assert_ready("pr_request", code, out)
        assert out["planner_stage"] == "request_pr_info"
        assert out["request_packet_written"] is True
        assert pr_req["connector_action"] == "GitHub.get_pr_info"
        assert runs_req == {}

        code, out, pr_req, runs_req = run(root, "runs_request", {"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": raw_pr()}, lic())
        assert_ready("runs_request", code, out)
        assert out["planner_stage"] == "request_commit_workflow_runs"
        assert runs_req["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert runs_req["connector_payload"]["commit_sha"] == "abc"

        nested = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "head": {"sha": "nestedabc"}, "base": {"ref": "main"}}
        code, out, pr_req, runs_req = run(root, "nested_runs_request", {"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": nested}, lic())
        assert_ready("nested_runs_request", code, out)
        assert runs_req["connector_payload"]["commit_sha"] == "nestedabc"

        code, out, pr_req, runs_req = run(root, "collect", {"qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": raw_pr(), "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs("success")}, lic())
        assert_ready("collect", code, out)
        assert out["planner_stage"] == "collect_live_snapshot"
        assert out["collector_status"] == "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_READY"
        assert out["policy_decision"] == "policy_all_green"

        code, out, pr_req, runs_req = run(root, "bad_query", {"qi_github_actions_pr_live_query_packet.json": query(repo_full_name="bad")}, lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]

        code, out, pr_req, runs_req = run(root, "license_block", {"qi_github_actions_pr_live_query_packet.json": query()}, lic(connector_request_write_allowed=False))
        assert code == 1
        assert "connector_request_write_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_request_planner_v7_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

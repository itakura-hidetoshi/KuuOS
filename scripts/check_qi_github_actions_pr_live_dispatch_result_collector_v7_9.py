#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_dispatch_result_collector_v7_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, target: str | None = None) -> dict[str, Any]:
    value = {"qi_github_actions_pr_live_dispatch_result_collector_enabled": True, "apply_github_actions_pr_live_dispatch_result_collector": True, "runtime_root": str(root)}
    if target:
        value["dispatch_target"] = target
    return value


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_DISPATCH_RESULT_COLLECTOR_LICENSE_READY", "dispatch_packet_read_allowed": True, "dispatch_result_read_allowed": True, "connector_result_write_allowed": True, "bridge_request_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_collect"] = True
    value.update(overrides)
    return value


def pr_dispatch() -> dict[str, Any]:
    return {"dispatch_target": "pr_info", "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "result_expected_file": "qi_github_actions_raw_pr_info_packet.json"}


def runs_dispatch() -> dict[str, Any]:
    return {"dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_raw_commit_workflow_runs_packet.json"}


def pr_result() -> dict[str, Any]:
    return {"dispatch_result_allowed": True, "number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS"}


def runs_result() -> dict[str, Any]:
    return {"dispatch_result_allowed": True, "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], target: str | None = None) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, target))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_live_connector_result_packet.json"), load_json(runtime / "qi_github_actions_pr_live_connector_request.json")


def assert_ready(case: str, code: int, out: dict[str, Any], connector: dict[str, Any], bridge: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_DISPATCH_RESULT_COLLECTOR_READY", case
    assert out["connector_result_written"] is True, case
    assert out["bridge_request_written"] is True, case
    assert not out["blockers"], case
    assert connector["version"] == "qi_github_actions_pr_live_connector_result_packet_from_dispatch_v7_9", case
    assert bridge["connector_action"] == connector["connector_action"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch(), "qi_github_actions_pr_live_dispatch_pr_info_result.json": pr_result()}
        code, out, connector, bridge = run(root, "pr", files, lic("pr_info"))
        assert_ready("pr", code, out, connector, bridge)
        assert out["dispatch_target"] == "pr_info"
        assert connector["result_kind"] == "pr_info"
        assert connector["connector_result"]["head_sha"] == "abc"

        nested_pr = {"dispatch_result_allowed": True, "connector_result": {"number": 1, "head": {"sha": "nestedabc"}, "repo_full_name": "itakura-hidetoshi/KuuOS"}}
        files = {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch(), "qi_github_actions_pr_live_dispatch_pr_info_result.json": nested_pr}
        code, out, connector, bridge = run(root, "nested_pr", files, lic("pr_info"), "pr_info")
        assert_ready("nested_pr", code, out, connector, bridge)
        assert connector["connector_result"]["head"]["sha"] == "nestedabc"

        files = {"qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json": runs_dispatch(), "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json": runs_result()}
        code, out, connector, bridge = run(root, "runs", files, lic("commit_workflow_runs"))
        assert_ready("runs", code, out, connector, bridge)
        assert out["dispatch_target"] == "commit_workflow_runs"
        assert connector["result_kind"] == "commit_workflow_runs"
        assert connector["connector_result"]["workflow_runs"]

        bad_result = {"dispatch_result_allowed": True, "number": 1, "repo_full_name": "itakura-hidetoshi/KuuOS"}
        files = {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch(), "qi_github_actions_pr_live_dispatch_pr_info_result.json": bad_result}
        code, out, connector, bridge = run(root, "missing_head", files, lic("pr_info"), "pr_info")
        assert code == 1
        assert "head_sha_missing" in out["blockers"]
        assert connector == {}

        denied = {"dispatch_result_allowed": False, "workflow_runs": []}
        files = {"qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json": runs_dispatch(), "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json": denied}
        code, out, connector, bridge = run(root, "denied", files, lic("commit_workflow_runs"), "commit_workflow_runs")
        assert code == 1
        assert "dispatch_result_allowed_not_true" in out["blockers"]
        assert connector == {}

        code, out, connector, bridge = run(root, "license_block", {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch(), "qi_github_actions_pr_live_dispatch_pr_info_result.json": pr_result()}, lic())
        assert code == 1
        assert "pr_info_not_allowed_by_pr_live_dispatch_result_collector_license" in out["blockers"]
    print("qi_github_actions_pr_live_dispatch_result_collector_v7_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

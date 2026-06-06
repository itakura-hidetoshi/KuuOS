#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_dispatch_result_router_v10_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_result_router_enabled": True, "apply_github_actions_dispatch_result_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_LICENSE_READY", "dispatch_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "target_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def dispatch(action: str, kind: str = "policy_action") -> dict[str, Any]:
    expected = {
        "GitHub.get_pr_info": "qi_github_actions_dispatch_pr_info_raw_result_packet.json",
        "GitHub.fetch_commit_workflow_runs": "qi_github_actions_dispatch_workflow_runs_raw_result_packet.json",
        "GitHub.merge_pull_request": "qi_github_actions_dispatch_merge_raw_result_packet.json",
        "GitHub.rerun_failed_workflow_run_jobs": "qi_github_actions_dispatch_rerun_raw_result_packet.json",
    }[action]
    return {"dispatch_allowed": True, "dispatch_kind": kind, "connector_action": action, "raw_result_expected_file": expected}


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
    out = load_json(op)
    return done.returncode, out, load_json(pathlib.Path(out.get("target_packet_path", ""))) if out.get("target_packet_path") else {}


def assert_ready(case: str, code: int, out: dict[str, Any], target: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_READY", case
    assert out["target_packet_written"] is True, case
    assert not out["blockers"], case
    assert target["routed_by"].endswith("v10_6"), case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.get_pr_info", "policy_reentry_pr_info"), "qi_github_actions_dispatch_pr_info_raw_result_packet.json": {"connector_action": "GitHub.get_pr_info", "repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc"}}
        code, out, target = run(root, "pr_info", files, lic())
        assert_ready("pr_info", code, out, target)
        assert out["target_packet_path"].endswith("qi_github_actions_policy_reentry_pr_info_raw_result_packet.json")
        assert target["number"] == 1

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.fetch_commit_workflow_runs", "next_cycle_reobserve"), "qi_github_actions_dispatch_workflow_runs_raw_result_packet.json": {"connector_action": "GitHub.fetch_commit_workflow_runs", "workflow_runs": [{"id": 10, "status": "completed", "conclusion": "success"}]}}
        code, out, target = run(root, "workflow", files, lic())
        assert_ready("workflow", code, out, target)
        assert out["target_packet_path"].endswith("qi_github_actions_next_cycle_external_call_raw_result_packet.json")
        assert target["workflow_runs"]

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.merge_pull_request"), "qi_github_actions_dispatch_merge_raw_result_packet.json": {"connector_action": "GitHub.merge_pull_request", "merged": True, "sha": "m"}}
        code, out, target = run(root, "merge", files, lic())
        assert_ready("merge", code, out, target)
        assert out["target_packet_path"].endswith("qi_github_actions_policy_action_external_call_raw_result_packet.json")
        assert target["merged"] is True

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.rerun_failed_workflow_run_jobs"), "qi_github_actions_dispatch_rerun_raw_result_packet.json": {"connector_action": "GitHub.rerun_failed_workflow_run_jobs", "success": True}}
        code, out, target = run(root, "rerun", files, lic())
        assert_ready("rerun", code, out, target)
        assert target["success"] is True

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.merge_pull_request"), "qi_github_actions_dispatch_merge_raw_result_packet.json": {"connector_action": "GitHub.get_pr_info", "merged": True}}
        code, out, target = run(root, "action_mismatch", files, lic())
        assert code == 1
        assert "raw_result_connector_action_mismatch" in out["blockers"]
        assert target == {}

        code, out, target = run(root, "missing_raw", {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.get_pr_info")}, lic())
        assert code == 1
        assert "dispatch_raw_result_missing_or_invalid" in out["blockers"]
        assert target == {}

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.merge_pull_request"), "qi_github_actions_dispatch_merge_raw_result_packet.json": {"connector_action": "GitHub.merge_pull_request", "merged": True}}
        code, out, target = run(root, "license_block", files, lic(target_packet_write_allowed=False))
        assert code == 1
        assert "target_packet_write_not_allowed" in out["blockers"]
        assert target == {}
    print("qi_github_actions_dispatch_result_router_v10_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

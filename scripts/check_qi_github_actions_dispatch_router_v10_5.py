#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_dispatch_router_v10_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_router_enabled": True, "apply_github_actions_dispatch_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_LICENSE_READY", "external_call_packet_read_allowed": True, "dispatch_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_unified_dispatch_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_READY", case
    assert out["dispatch_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["dispatch_allowed"] is True, case
    assert packet["boundary"]["dispatch_packet_only"] is True, case


def pr_info_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}}


def workflow_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "bridge_state": "next_cycle_external_call_ready", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}


def merge_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge"}}


def rerun_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "action_kind": "rerun_failed_workflow_run_jobs", "connector_action": "GitHub.rerun_failed_workflow_run_jobs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "run_id": 123}}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "pr_info", {"qi_github_actions_policy_reentry_external_call_packet.json": pr_info_call()}, lic())
        assert_ready("pr_info", code, out, packet)
        assert out["dispatch_kind"] == "policy_reentry_pr_info"
        assert packet["connector_action"] == "GitHub.get_pr_info"
        assert packet["raw_result_expected_file"].endswith("pr_info_raw_result_packet.json")

        code, out, packet = run(root, "workflow", {"qi_github_actions_next_cycle_external_call_packet.json": workflow_call()}, lic())
        assert_ready("workflow", code, out, packet)
        assert out["dispatch_kind"] == "next_cycle_reobserve"
        assert packet["connector_payload"]["commit_sha"] == "abc"

        code, out, packet = run(root, "merge", {"qi_github_actions_policy_action_external_call_packet.json": merge_call()}, lic())
        assert_ready("merge", code, out, packet)
        assert out["dispatch_kind"] == "policy_action"
        assert packet["connector_action"] == "GitHub.merge_pull_request"

        code, out, packet = run(root, "rerun", {"qi_github_actions_policy_action_external_call_packet.json": rerun_call()}, lic())
        assert_ready("rerun", code, out, packet)
        assert packet["connector_action"] == "GitHub.rerun_failed_workflow_run_jobs"
        assert packet["connector_payload"]["run_id"] == 123

        bad = pr_info_call()
        bad["connector_payload"] = {"repository_full_name": "bad", "pr_number": 1}
        code, out, packet = run(root, "bad_payload", {"qi_github_actions_policy_reentry_external_call_packet.json": bad}, lic())
        assert code == 1
        assert "repository_full_name_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing", {}, lic())
        assert code == 1
        assert "dispatch_source_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_policy_reentry_external_call_packet.json": pr_info_call()}, lic(dispatch_packet_write_allowed=False))
        assert code == 1
        assert "dispatch_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_dispatch_router_v10_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

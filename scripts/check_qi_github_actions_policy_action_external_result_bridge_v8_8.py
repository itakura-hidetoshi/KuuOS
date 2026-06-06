#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_action_external_result_bridge_v8_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_result_bridge_enabled": True, "apply_github_actions_policy_action_external_result_bridge": True, "runtime_root": str(root)}


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "action_result_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_result_bridge"] = True
    value.update(overrides)
    return value


def call(kind: str, action: str, expected: str) -> dict[str, Any]:
    return {"external_call_allowed": True, "action_kind": kind, "connector_action": action, "connector_payload": {}, "action_result_expected_file": expected}


def merge_call() -> dict[str, Any]:
    return call("merge_pull_request", "GitHub.merge_pull_request", "qi_github_actions_policy_action_merge_result_packet.json")


def rerun_call() -> dict[str, Any]:
    return call("rerun_failed_workflow_run_jobs", "GitHub.rerun_failed_workflow_run_jobs", "qi_github_actions_policy_action_rerun_result_packet.json")


def reobserve_call() -> dict[str, Any]:
    return call("reobserve_commit_workflow_runs", "GitHub.fetch_commit_workflow_runs", "qi_github_actions_policy_action_reobserve_result_packet.json")


def run(root: pathlib.Path, name: str, call_packet: dict[str, Any], raw_result: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_policy_action_external_call_packet.json", call_packet)
    dump(runtime / "qi_github_actions_policy_action_external_call_raw_result_packet.json", raw_result)
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
    result_path = pathlib.Path(out.get("action_result_path", ""))
    return done.returncode, out, load_json(result_path) if str(result_path) else {}


def assert_ready(case: str, code: int, out: dict[str, Any], result: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_READY", case
    assert out["action_result_written"] is True, case
    assert not out["blockers"], case
    assert result["action_result_allowed"] is True, case
    assert result["boundary"]["feeds_policy_action_receipt_or_review"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, result = run(root, "merge", merge_call(), {"connector_action": "GitHub.merge_pull_request", "merged": True, "sha": "abc", "message": "ok"}, lic("merge_pull_request"))
        assert_ready("merge", code, out, result)
        assert result["action_kind"] == "merge_pull_request"
        assert result["connector_result"]["merged"] is True

        code, out, result = run(root, "rerun", rerun_call(), {"connector_action": "GitHub.rerun_failed_workflow_run_jobs", "success": True}, lic("rerun_failed_workflow_run_jobs"))
        assert_ready("rerun", code, out, result)
        assert result["action_kind"] == "rerun_failed_workflow_run_jobs"

        code, out, result = run(root, "reobserve", reobserve_call(), {"connector_action": "GitHub.fetch_commit_workflow_runs", "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}, lic("reobserve_commit_workflow_runs"))
        assert_ready("reobserve", code, out, result)
        assert result["action_kind"] == "reobserve_commit_workflow_runs"
        assert result["connector_result"]["workflow_runs"]

        code, out, result = run(root, "merge_not_merged", merge_call(), {"connector_action": "GitHub.merge_pull_request", "merged": False, "sha": "abc"}, lic("merge_pull_request"))
        assert code == 1
        assert "merge_result_not_merged_true" in out["blockers"]
        assert result == {}

        code, out, result = run(root, "action_mismatch", merge_call(), {"connector_action": "GitHub.fetch_commit_workflow_runs", "merged": True, "sha": "abc"}, lic("merge_pull_request"))
        assert code == 1
        assert "raw_result_connector_action_mismatch" in out["blockers"]
        assert result == {}

        code, out, result = run(root, "license_block", merge_call(), {"connector_action": "GitHub.merge_pull_request", "merged": True, "sha": "abc"}, lic())
        assert code == 1
        assert "merge_pull_request_not_allowed_by_policy_action_external_result_bridge_license" in out["blockers"]
        assert result == {}
    print("qi_github_actions_policy_action_external_result_bridge_v8_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_action_final_receipt_v8_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, action_kind: str | None = None) -> dict[str, Any]:
    value = {"qi_github_actions_policy_action_final_receipt_enabled": True, "apply_github_actions_policy_action_final_receipt": True, "runtime_root": str(root)}
    if action_kind:
        value["action_kind"] = action_kind
    return value


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_LICENSE_READY", "action_result_packet_read_allowed": True, "final_receipt_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_final_receipt"] = True
    value.update(overrides)
    return value


def merge_result(merged: bool = True) -> dict[str, Any]:
    return {"action_result_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": merged, "sha": "abc", "message": "ok"}}


def rerun_result(success: bool = True) -> dict[str, Any]:
    return {"action_result_allowed": True, "action_kind": "rerun_failed_workflow_run_jobs", "connector_action": "GitHub.rerun_failed_workflow_run_jobs", "connector_result": {"success": success}}


def reobserve_result() -> dict[str, Any]:
    return {"action_result_allowed": True, "action_kind": "reobserve_commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_result": {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}}


def run(root: pathlib.Path, name: str, file_name: str | None, packet: dict[str, Any] | None, license_packet: dict[str, Any], action_kind: str | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if file_name is not None and packet is not None:
        dump(runtime / file_name, packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, action_kind))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_policy_action_final_receipt_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_READY", case
    assert out["final_receipt_written"] is True, case
    assert not out["blockers"], case
    assert packet["final_receipt_allowed"] is True, case
    assert packet["boundary"]["closes_or_routes_policy_action"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "merge", "qi_github_actions_policy_action_merge_result_packet.json", merge_result(True), lic("merge_pull_request"))
        assert_ready("merge", code, out, packet)
        assert out["final_state"] == "action_completed"
        assert packet["next_expected"] == "close_autopilot_cycle"

        code, out, packet = run(root, "rerun", "qi_github_actions_policy_action_rerun_result_packet.json", rerun_result(True), lic("rerun_failed_workflow_run_jobs"))
        assert_ready("rerun", code, out, packet)
        assert out["final_state"] == "action_rerun_requested"
        assert packet["next_expected"] == "wait_for_new_workflow_runs_then_reobserve"

        code, out, packet = run(root, "reobserve", "qi_github_actions_policy_action_reobserve_result_packet.json", reobserve_result(), lic("reobserve_commit_workflow_runs"))
        assert_ready("reobserve", code, out, packet)
        assert out["final_state"] == "action_reobserve_ready"
        assert packet["connector_result"]["workflow_runs"]

        code, out, packet = run(root, "merge_not_done", "qi_github_actions_policy_action_merge_result_packet.json", merge_result(False), lic("merge_pull_request"))
        assert code == 1
        assert "merge_result_not_merged_true" in out["blockers"]
        assert packet == {}

        bad = {"action_result_allowed": True, "action_kind": "merge_pull_request", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_result": {"merged": True, "sha": "abc"}}
        code, out, packet = run(root, "action_mismatch", "qi_github_actions_policy_action_merge_result_packet.json", bad, lic("merge_pull_request"), "merge_pull_request")
        assert code == 1
        assert "connector_action_mismatch" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", "qi_github_actions_policy_action_merge_result_packet.json", merge_result(True), lic())
        assert code == 1
        assert "merge_pull_request_not_allowed_by_policy_action_final_receipt_license" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_policy_action_final_receipt_v8_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

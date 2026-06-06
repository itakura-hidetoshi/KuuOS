#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_action_external_call_bridge_v8_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_call_bridge_enabled": True, "apply_github_actions_policy_action_external_call_bridge": True, "runtime_root": str(root)}


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_LICENSE_READY", "action_handoff_packet_read_allowed": True, "external_call_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_external_call"] = True
    value.update(overrides)
    return value


def handoff(kind: str, action: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"action_handoff_allowed": True, "action_kind": kind, "connector_action": action, "connector_payload": payload, "source_policy_decision": "policy_ready"}


def merge_handoff(**payload_overrides: Any) -> dict[str, Any]:
    payload = {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge", "expected_head_sha": "abc"}
    payload.update(payload_overrides)
    return handoff("merge_pull_request", "GitHub.merge_pull_request", payload)


def rerun_handoff(**payload_overrides: Any) -> dict[str, Any]:
    payload = {"repo_full_name": "itakura-hidetoshi/KuuOS", "run_id": 10}
    payload.update(payload_overrides)
    return handoff("rerun_failed_workflow_run_jobs", "GitHub.rerun_failed_workflow_run_jobs", payload)


def reobserve_handoff(**payload_overrides: Any) -> dict[str, Any]:
    payload = {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
    payload.update(payload_overrides)
    return handoff("reobserve_commit_workflow_runs", "GitHub.fetch_commit_workflow_runs", payload)


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_github_actions_autopilot_policy_action_handoff_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_policy_action_external_call_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], call: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_READY", case
    assert out["external_call_packet_written"] is True, case
    assert not out["blockers"], case
    assert call["external_call_allowed"] is True, case
    assert call["boundary"]["result_must_be_collected_by_next_result_bridge"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, call = run(root, "merge", merge_handoff(), lic("merge_pull_request"))
        assert_ready("merge", code, out, call)
        assert out["action_kind"] == "merge_pull_request"
        assert call["connector_action"] == "GitHub.merge_pull_request"
        assert call["connector_payload"]["expected_head_sha"] == "abc"
        assert call["action_result_expected_file"] == "qi_github_actions_policy_action_merge_result_packet.json"

        code, out, call = run(root, "rerun", rerun_handoff(), lic("rerun_failed_workflow_run_jobs"))
        assert_ready("rerun", code, out, call)
        assert out["action_kind"] == "rerun_failed_workflow_run_jobs"
        assert call["connector_action"] == "GitHub.rerun_failed_workflow_run_jobs"
        assert call["connector_payload"]["run_id"] == 10

        code, out, call = run(root, "reobserve", reobserve_handoff(), lic("reobserve_commit_workflow_runs"))
        assert_ready("reobserve", code, out, call)
        assert out["action_kind"] == "reobserve_commit_workflow_runs"
        assert call["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert call["connector_payload"]["commit_sha"] == "abc"

        code, out, call = run(root, "missing_head", merge_handoff(expected_head_sha=""), lic("merge_pull_request"))
        assert code == 1
        assert "expected_head_sha_missing" in out["blockers"]
        assert call == {}

        bad_action = handoff("merge_pull_request", "GitHub.fetch_commit_workflow_runs", {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge", "expected_head_sha": "abc"})
        code, out, call = run(root, "mismatch", bad_action, lic("merge_pull_request"))
        assert code == 1
        assert "connector_action_mismatch" in out["blockers"]
        assert call == {}

        code, out, call = run(root, "license_block", merge_handoff(), lic())
        assert code == 1
        assert "merge_pull_request_not_allowed_by_policy_action_external_call_bridge_license" in out["blockers"]
        assert call == {}
    print("qi_github_actions_policy_action_external_call_bridge_v8_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

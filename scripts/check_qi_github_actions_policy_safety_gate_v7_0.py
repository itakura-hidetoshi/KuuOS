#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_safety_gate_v7_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_safety_gate_enabled": True, "apply_github_actions_policy_safety_gate": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_LICENSE_READY", "policy_intent_read_allowed": True, "status_packet_read_allowed": True, "policy_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def intent(**overrides: Any) -> dict[str, Any]:
    value = {"policy_intent_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True, "pr_number": 1, "expected_head_sha": "abc", "commit_sha": "abc", "base_branch": "main"}
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_full_cycle_policy_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_READY", case
    assert out["gate_result"] == "passed", case
    assert out["policy_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["policy_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "pass", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet()}, lic())
        assert_ready("pass", code, out, packet)
        assert packet["merge_when_green"] is True
        assert packet["rerun_when_failed"] is True
        assert packet["reobserve_when_pending"] is True

        code, out, packet = run(root, "missing_sha", {"qi_github_actions_policy_intent_packet.json": intent(expected_head_sha=""), "qi_github_actions_status_packet.json": status_packet()}, lic())
        assert code == 1
        assert "expected_head_sha_missing" in out["blockers"]
        assert packet == {}

        missing_status = {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Other", "status": "completed", "conclusion": "success"}]}
        code, out, packet = run(root, "missing_workflow", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": missing_status}, lic())
        assert code == 1
        assert "required_workflows_missing" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "no_action", {"qi_github_actions_policy_intent_packet.json": intent(merge_when_green=False, rerun_when_failed=False, reobserve_when_pending=False), "qi_github_actions_status_packet.json": status_packet()}, lic())
        assert code == 1
        assert "no_policy_action_enabled" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_repo", {"qi_github_actions_policy_intent_packet.json": intent(repo_full_name="bad"), "qi_github_actions_status_packet.json": status_packet()}, lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet()}, lic(policy_packet_write_allowed=False))
        assert code == 1
        assert "policy_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_policy_safety_gate_v7_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

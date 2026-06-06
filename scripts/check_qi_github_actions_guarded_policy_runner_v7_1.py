#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_guarded_policy_runner_v7_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_guarded_policy_runner_enabled": True, "apply_github_actions_guarded_policy_runner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_LICENSE_READY", "safety_gate_run_allowed": True, "policy_runner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def status_packet(conclusion: str | None = "success", run_status: str = "completed") -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": run_status, "conclusion": conclusion}]}


def intent(**overrides: Any) -> dict[str, Any]:
    value = {"policy_intent_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True, "pr_number": 1, "expected_head_sha": "abc", "commit_sha": "abc", "base_branch": "main"}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
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
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_READY", case
    assert out["gate_status"] == "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_READY", case
    assert out["gate_result"] == "passed", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "green", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet("success")}, lic())
        assert_ready("green", code, out)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        code, out = run(root, "failed", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet("failure")}, lic())
        assert_ready("failed", code, out)
        assert out["policy_decision"] == "policy_failed_rerun"
        assert out["action_prepared"] == "rerun_failed_workflow_run_jobs"

        code, out = run(root, "pending", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet(None, "in_progress")}, lic())
        assert_ready("pending", code, out)
        assert out["policy_decision"] == "policy_pending_reobserve"

        code, out = run(root, "gate_block", {"qi_github_actions_policy_intent_packet.json": intent(expected_head_sha=""), "qi_github_actions_status_packet.json": status_packet("success")}, lic())
        assert code == 1
        assert out["gate_result"] == "blocked"
        assert "policy_safety_gate_not_passed" in out["blockers"]

        code, out = run(root, "missing", {"qi_github_actions_status_packet.json": status_packet("success")}, lic())
        assert code == 1
        assert "policy_safety_gate_not_passed" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_policy_intent_packet.json": intent(), "qi_github_actions_status_packet.json": status_packet("success")}, lic(policy_runner_run_allowed=False))
        assert code == 1
        assert "policy_runner_run_not_allowed" in out["blockers"]
    print("qi_github_actions_guarded_policy_runner_v7_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

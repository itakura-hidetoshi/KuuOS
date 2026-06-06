#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_full_cycle_policy_runner_v6_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_full_cycle_policy_runner_enabled": True, "apply_github_actions_full_cycle_policy_runner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_LICENSE_READY", "policy_packet_read_allowed": True, "status_packet_read_allowed": True, "direct_executor_run_allowed": True, "orchestrator_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def policy(**overrides: Any) -> dict[str, Any]:
    value = {"policy_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "expected_head_sha": "abc", "commit_sha": "abc", "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True, "required_workflows": ["Qi Process Tensor Review Checks"], "max_full_cycle_phases": 3, "max_loop_steps_per_phase": 5}
    value.update(overrides)
    return value


def status(conclusion: str | None = "success", run_status: str = "completed", run_id: int = 10) -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"id": run_id, "name": "Qi Process Tensor Review Checks", "status": run_status, "conclusion": conclusion}]}


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
    assert out["status"] == "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_READY", case
    assert not out["blockers"], case
    assert out["policy_records"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "green", {"qi_github_actions_full_cycle_policy_packet.json": policy(), "qi_github_actions_status_packet.json": status("success")}, lic())
        assert_ready("green", code, out)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"
        assert (root / "green" / "qi_github_actions_connector_execution_request.json").is_file()

        code, out = run(root, "failed", {"qi_github_actions_full_cycle_policy_packet.json": policy(), "qi_github_actions_status_packet.json": status("failure", "completed", 20)}, lic())
        assert_ready("failed", code, out)
        assert out["policy_decision"] == "policy_failed_rerun"
        assert out["action_prepared"] == "rerun_failed_workflow_run_jobs"
        assert (root / "failed" / "qi_github_actions_connector_execution_request.json").is_file()

        code, out = run(root, "pending", {"qi_github_actions_full_cycle_policy_packet.json": policy(), "qi_github_actions_status_packet.json": status(None, "in_progress")}, lic())
        assert_ready("pending", code, out)
        assert out["policy_decision"] == "policy_pending_reobserve"
        assert out["action_prepared"] == "commit_workflow_runs_reobserve"
        assert (root / "pending" / "qi_github_actions_status_reobserve_request.json").is_file()

        code, out = run(root, "disabled", {"qi_github_actions_full_cycle_policy_packet.json": policy(merge_when_green=False), "qi_github_actions_status_packet.json": status("success")}, lic())
        assert_ready("disabled", code, out)
        assert out["stop_reason"] == "policy_action_not_enabled"

        code, out = run(root, "missing_policy", {"qi_github_actions_status_packet.json": status("success")}, lic())
        assert code == 1
        assert "policy_packet_missing_or_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_full_cycle_policy_packet.json": policy(), "qi_github_actions_status_packet.json": status("success")}, lic(orchestrator_run_allowed=False))
        assert code == 1
        assert "orchestrator_run_not_allowed" in out["blockers"]
    print("qi_github_actions_full_cycle_policy_runner_v6_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

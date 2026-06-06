#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_full_cycle_orchestrator_v6_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {"qi_github_actions_full_cycle_orchestrator_enabled": True, "apply_github_actions_full_cycle_orchestrator": True, "runtime_root": str(root), "max_full_cycle_phases": 4, "max_loop_steps_per_phase": 5}
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_LICENSE_READY", "loop_run_allowed": True, "external_cycle_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_READY", case
    assert not out["blockers"], case
    assert out["phase_records"], case


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "status", {"qi_github_actions_status_packet.json": status_packet()}, lic())
        assert_ready("status", code, out)
        assert out["stop_reason"] == "await_dispatch_result"
        assert (root / "status" / "qi_github_actions_external_call_packet.json").is_file()
        assert (root / "status" / "qi_github_actions_dispatch_rerun_failed_workflow_run_jobs_packet.json").is_file() or (root / "status" / "qi_github_actions_dispatch_rerun_workflow_job_packet.json").is_file() or (root / "status" / "qi_github_actions_dispatch_merge_pull_request_packet.json").is_file() or (root / "status" / "qi_github_actions_dispatch_commit_workflow_runs_packet.json").is_file()

        reobserve = {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
        code, out = run(root, "reobserve", {"qi_github_actions_status_reobserve_request.json": reobserve}, lic())
        assert_ready("reobserve", code, out)
        assert out["stop_reason"] == "await_dispatch_result"
        assert (root / "reobserve" / "qi_github_actions_dispatch_commit_workflow_runs_packet.json").is_file()

        external_call = {"wait_stage": "await_status_observation", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        dispatch_packet = {"dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        dispatch_result = {"dispatch_result_allowed": True, "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}
        code, out = run(root, "result", {"qi_github_actions_external_call_packet.json": external_call, "qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch_packet, "qi_github_actions_dispatch_commit_workflow_runs_result.json": dispatch_result}, lic(), {"dispatch_target": "commit_workflow_runs", "max_full_cycle_phases": 2})
        assert_ready("result", code, out)
        assert out["stop_reason"] in {"await_dispatch_result", "max_phases_reached", "external_result_adapted"}
        assert (root / "result" / "qi_github_actions_observation_connector_result_packet.json").is_file()

        code, out = run(root, "bad_phase", {}, lic(), {"max_full_cycle_phases": 0})
        assert code == 1
        assert "max_full_cycle_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {}, lic(external_cycle_run_allowed=False))
        assert code == 1
        assert "external_cycle_run_not_allowed" in out["blockers"]
    print("qi_github_actions_full_cycle_orchestrator_v6_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

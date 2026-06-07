#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_external_bridge_executor_v6_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_bridge_executor_enabled": True, "apply_github_actions_external_bridge_executor": True, "runtime_root": str(root)}


def lic(stage: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_LICENSE_READY", "external_bridge_state_read_allowed": True, "local_external_stage_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    for name in ["external_wait_resolve", "external_call_dispatch", "dispatch_result_collect", "external_result_adapt", "await_dispatch_result", "await_external_call"]:
        value[f"allow_{name}_stage"] = True
    if stage:
        value[f"allow_{stage}_stage"] = True
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


def assert_ready(case: str, code: int, out: dict[str, Any], stage: str, local: bool) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_READY", case
    assert out["selected_stage"] == stage, case
    assert out["local_stage_performed"] is local, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source_req = {"connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}
        code, out = run(root, "resolve", {"qi_github_actions_observation_connector_request.json": source_req}, lic())
        assert_ready("resolve", code, out, "external_wait_resolve", True)
        assert (root / "resolve" / "qi_github_actions_external_call_packet.json").is_file()

        external_call = {"wait_stage": "await_status_observation", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        code, out = run(root, "dispatch", {"qi_github_actions_external_call_packet.json": external_call}, lic())
        assert_ready("dispatch", code, out, "external_call_dispatch", True)
        assert (root / "dispatch" / "qi_github_actions_dispatch_commit_workflow_runs_packet.json").is_file()

        dispatch_packet = {"dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        dispatch_result = {"dispatch_result_allowed": True, "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}
        code, out = run(root, "collect", {"qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch_packet, "qi_github_actions_dispatch_commit_workflow_runs_result.json": dispatch_result}, lic())
        assert_ready("collect", code, out, "dispatch_result_collect", True)
        assert (root / "collect" / "qi_github_actions_external_call_raw_result_packet.json").is_file()

        raw = {"dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_result": {"workflow_runs": [{"name": "Qi Process Tensor Review Checks"}]}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        code, out = run(root, "adapt", {"qi_github_actions_external_call_packet.json": external_call, "qi_github_actions_external_call_raw_result_packet.json": raw}, lic())
        assert_ready("adapt", code, out, "external_result_adapt", True)
        assert (root / "adapt" / "qi_github_actions_observation_connector_result_packet.json").is_file()

        code, out = run(root, "await_dispatch", {"qi_github_actions_external_call_packet.json": external_call, "qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch_packet}, lic())
        assert_ready("await_dispatch", code, out, "await_dispatch_result", False)
        assert out["stage_status"] == "WAITING"

        code, out = run(root, "empty", {}, lic())
        assert_ready("empty", code, out, "await_external_call", False)
        assert out["stage_status"] == "WAITING"

        code, out = run(root, "license_block", {}, {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_LICENSE_READY", "external_bridge_state_read_allowed": True, "local_external_stage_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True})
        assert code == 1
        assert "await_external_call_not_allowed_by_external_bridge_executor_license" in out["blockers"]
    print("qi_github_actions_external_bridge_executor_v6_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

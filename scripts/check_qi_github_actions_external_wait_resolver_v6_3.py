#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_external_wait_resolver_v6_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_wait_resolver_enabled": True, "apply_github_actions_external_wait_resolver": True, "runtime_root": str(root)}


def lic(stage: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_LICENSE_READY", "wait_state_read_allowed": True, "external_call_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if stage:
        value[f"allow_{stage}_stage"] = True
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_external_call_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_READY", case
    assert out["external_call_packet_emitted"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["expects_connector_result_packet_after_external_call"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        operation_req = {"connector_action": "GitHub.connector_operation", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "target_id": 1}}
        code, out, packet = run(root, "operation", {"qi_github_actions_loop_command_packet.json": {"selected_stage": "await_connector_operation"}, "qi_github_actions_connector_execution_request.json": operation_req}, lic("await_connector_operation"))
        assert_ready("operation", code, out, packet)
        assert packet["wait_stage"] == "await_connector_operation"
        assert packet["result_expected_file"] == "qi_github_actions_connector_result_packet.json"

        observation_req = {"connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}
        code, out, packet = run(root, "observation", {"qi_github_actions_loop_command_packet.json": {"selected_stage": "await_status_observation"}, "qi_github_actions_observation_connector_request.json": observation_req}, lic("await_status_observation"))
        assert_ready("observation", code, out, packet)
        assert packet["wait_stage"] == "await_status_observation"
        assert packet["result_expected_file"] == "qi_github_actions_observation_connector_result_packet.json"

        code, out, packet = run(root, "fallback", {"qi_github_actions_observation_connector_request.json": observation_req}, lic("await_status_observation"))
        assert_ready("fallback", code, out, packet)
        assert "loop_command_packet_missing_using_available_wait_source" in out["warnings"]

        code, out, packet = run(root, "missing", {"qi_github_actions_loop_command_packet.json": {"selected_stage": "await_connector_operation"}}, lic("await_connector_operation"))
        assert code == 1
        assert "wait_source_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_loop_command_packet.json": {"selected_stage": "await_connector_operation"}, "qi_github_actions_connector_execution_request.json": operation_req}, lic())
        assert code == 1
        assert "await_connector_operation_not_allowed_by_external_wait_resolver_license" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_external_wait_resolver_v6_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_external_call_result_adapter_v6_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_result_adapter_enabled": True, "apply_github_actions_external_call_result_adapter": True, "runtime_root": str(root)}


def lic(stage: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "adapted_result_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if stage:
        value[f"allow_{stage}_stage"] = True
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, call: dict[str, Any] | None, raw: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if call is not None:
        dump(runtime / "qi_github_actions_external_call_packet.json", call)
    if raw is not None:
        dump(runtime / "qi_github_actions_external_call_raw_result_packet.json", raw)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_connector_result_packet.json"), load_json(runtime / "qi_github_actions_observation_connector_result_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_READY", case
    assert out["adapted_result_written"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        op_call = {"wait_stage": "await_connector_operation", "connector_action": "GitHub.connector_operation", "connector_payload": {"target_id": 1}, "result_expected_file": "qi_github_actions_connector_result_packet.json"}
        code, out, op_result, obs_result = run(root, "operation", op_call, {"action": "merge_pull_request", "success": True, "merged": True}, lic("await_connector_operation"))
        assert_ready("operation", code, out)
        assert op_result["result_packet_allowed"] is True
        assert op_result["action"] == "merge_pull_request"
        assert obs_result == {}

        obs_call = {"wait_stage": "await_status_observation", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"commit_sha": "abc"}, "result_expected_file": "qi_github_actions_observation_connector_result_packet.json"}
        raw = {"workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}
        code, out, op_result, obs_result = run(root, "observation", obs_call, raw, lic("await_status_observation"))
        assert_ready("observation", code, out)
        assert obs_result["observation_result_allowed"] is True
        assert obs_result["observation_kind"] == "commit_workflow_runs"
        assert op_result == {}

        bad_call = {"wait_stage": "await_status_observation", "connector_action": "GitHub.fetch", "connector_payload": {"x": 1}, "result_expected_file": "not_allowed.json"}
        code, out, op_result, obs_result = run(root, "bad_file", bad_call, {"ok": True}, lic("await_status_observation"))
        assert code == 1
        assert "result_expected_file_not_allowlisted" in out["blockers"]

        code, out, op_result, obs_result = run(root, "missing_raw", op_call, None, lic("await_connector_operation"))
        assert code == 1
        assert "external_call_raw_result_packet_missing_or_invalid" in out["blockers"]

        code, out, op_result, obs_result = run(root, "license_block", op_call, {"success": True}, lic())
        assert code == 1
        assert "await_connector_operation_not_allowed_by_result_adapter_license" in out["blockers"]
    print("qi_github_actions_external_call_result_adapter_v6_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

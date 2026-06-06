#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_loop_coordinator_v6_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_loop_coordinator_enabled": True, "apply_github_actions_loop_coordinator": True, "runtime_root": str(root)}


def lic(stage: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_LICENSE_READY", "loop_state_read_allowed": True, "loop_command_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_loop_command_packet.json")


def assert_stage(case: str, code: int, out: dict[str, Any], command: dict[str, Any], stage: str) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_READY", case
    assert out["selected_stage"] == stage, case
    assert out["command_emitted"] is True, case
    assert command["selected_stage"] == stage, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, command = run(root, "obs_result", {"qi_github_actions_observation_connector_result_packet.json": {"ok": True}}, lic("observation_result_ingest"))
        assert_stage("obs_result", code, out, command, "observation_result_ingest")

        code, out, command = run(root, "reobserve", {"qi_github_actions_status_reobserve_request.json": {"ok": True}}, lic("status_reobserve"))
        assert_stage("reobserve", code, out, command, "status_reobserve")

        code, out, command = run(root, "result", {"qi_github_actions_connector_result_packet.json": {"ok": True}}, lic("operation_result_ingest"))
        assert_stage("result", code, out, command, "operation_result_ingest")

        code, out, command = run(root, "request", {"qi_github_actions_connector_execution_request.json": {"ok": True}}, lic("await_connector_operation"))
        assert_stage("request", code, out, command, "await_connector_operation")

        code, out, command = run(root, "status", {"qi_github_actions_status_packet.json": {"ok": True}}, lic("plan_from_status"))
        assert_stage("status", code, out, command, "plan_from_status")

        code, out, command = run(root, "empty", {}, lic("await_status_observation"))
        assert_stage("empty", code, out, command, "await_status_observation")

        code, out, command = run(root, "license_block", {"qi_github_actions_status_packet.json": {"ok": True}}, lic())
        assert code == 1
        assert "plan_from_status_not_allowed_by_loop_coordinator_license" in out["blockers"]
        assert command == {}
    print("qi_github_actions_loop_coordinator_v6_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

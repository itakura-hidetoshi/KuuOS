#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_next_cycle_executor_v9_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_next_cycle_executor_enabled": True, "apply_github_actions_next_cycle_executor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXECUTOR_LICENSE_READY", "next_cycle_packet_read_allowed": True, "route_payload_read_allowed": True, "execution_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def next_packet(state: str) -> dict[str, Any]:
    return {"next_cycle_allowed": True, "route_state": "route", "next_cycle_state": state, "next_connector_action": "GitHub.fetch_commit_workflow_runs" if state == "await_workflow_reobserve" else "none"}


def reobserve_request(**payload_overrides: Any) -> dict[str, Any]:
    payload = {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
    payload.update(payload_overrides)
    return {"request_allowed": True, "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": payload}


def reentry_packet() -> dict[str, Any]:
    return {"reentry_allowed": True, "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}], "status_summary": {"all_success": True, "any_failed": False}}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_next_cycle_execution_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXECUTOR_READY", case
    assert out["execution_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["execution_allowed"] is True, case
    assert packet["boundary"]["execution_packet_only"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "closed", {"qi_github_actions_route_next_cycle_packet.json": next_packet("closed")}, lic())
        assert_ready("closed", code, out, packet)
        assert out["execution_state"] == "cycle_closed"
        assert packet["connector_action"] == "none"

        files = {"qi_github_actions_route_next_cycle_packet.json": next_packet("await_workflow_reobserve"), "qi_github_actions_route_reobserve_request_packet.json": reobserve_request()}
        code, out, packet = run(root, "reobserve", files, lic())
        assert_ready("reobserve", code, out, packet)
        assert out["execution_state"] == "external_reobserve_ready"
        assert packet["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert packet["connector_payload"]["commit_sha"] == "abc"

        files = {"qi_github_actions_route_next_cycle_packet.json": next_packet("reenter_policy_loop"), "qi_github_actions_route_policy_reentry_packet.json": reentry_packet()}
        code, out, packet = run(root, "reentry", files, lic())
        assert_ready("reentry", code, out, packet)
        assert out["execution_state"] == "policy_reentry_ready"
        assert packet["connector_payload"]["reentry_allowed"] is True

        files = {"qi_github_actions_route_next_cycle_packet.json": next_packet("await_workflow_reobserve"), "qi_github_actions_route_reobserve_request_packet.json": reobserve_request(repo_full_name="bad")}
        code, out, packet = run(root, "bad_reobserve", files, lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing_reentry", {"qi_github_actions_route_next_cycle_packet.json": next_packet("reenter_policy_loop")}, lic())
        assert code == 1
        assert "policy_reentry_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_route_next_cycle_packet.json": next_packet("closed")}, lic(execution_packet_write_allowed=False))
        assert code == 1
        assert "execution_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_next_cycle_executor_v9_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

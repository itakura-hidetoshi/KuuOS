#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_next_cycle_result_bridge_v9_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_next_cycle_result_bridge_enabled": True, "apply_github_actions_next_cycle_result_bridge": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "result_packet_write_allowed": True, "reentry_bridge_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def call(**payload_overrides: Any) -> dict[str, Any]:
    payload = {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
    payload.update(payload_overrides)
    return {"external_call_allowed": True, "bridge_state": "next_cycle_external_call_ready", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": payload}


def raw(conclusion: str = "success", action: str = "GitHub.fetch_commit_workflow_runs") -> dict[str, Any]:
    return {"connector_action": action, "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": conclusion}]}


def run(root: pathlib.Path, name: str, call_packet: dict[str, Any], raw_packet: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_next_cycle_external_call_packet.json", call_packet)
    dump(runtime / "qi_github_actions_next_cycle_external_call_raw_result_packet.json", raw_packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return (
        done.returncode,
        load_json(op),
        load_json(runtime / "qi_github_actions_next_cycle_external_result_packet.json"),
        load_json(runtime / "qi_github_actions_next_cycle_reentry_bridge_packet.json"),
        load_json(runtime / "qi_github_actions_status_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], result: dict[str, Any], reentry: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_READY", case
    assert out["result_packet_written"] is True, case
    assert out["reentry_bridge_written"] is True, case
    assert not out["blockers"], case
    assert result["external_result_allowed"] is True, case
    assert reentry["reentry_bridge_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, result, reentry, status = run(root, "success", call(), raw("success"), lic())
        assert_ready("success", code, out, result, reentry)
        assert out["bridge_state"] == "policy_reentry_bridge_ready"
        assert result["status_summary"]["all_success"] is True
        assert reentry["status_summary"]["all_success"] is True
        assert status["all_success"] is True

        code, out, result, reentry, status = run(root, "failure", call(), raw("failure"), lic())
        assert_ready("failure", code, out, result, reentry)
        assert result["status_summary"]["any_failed"] is True
        assert reentry["status_summary"]["any_failed"] is True

        code, out, result, reentry, status = run(root, "bad_call", call(repo_full_name="bad"), raw("success"), lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert result == {}
        assert reentry == {}

        code, out, result, reentry, status = run(root, "bad_action", call(), raw("success", "GitHub.get_pr_info"), lic())
        assert code == 1
        assert "raw_result_connector_action_mismatch" in out["blockers"]
        assert result == {}
        assert reentry == {}

        code, out, result, reentry, status = run(root, "empty_runs", call(), {"connector_action": "GitHub.fetch_commit_workflow_runs", "workflow_runs": []}, lic())
        assert code == 1
        assert "workflow_runs_empty_or_invalid" in out["blockers"]
        assert result == {}
        assert reentry == {}

        code, out, result, reentry, status = run(root, "license_block", call(), raw("success"), lic(result_packet_write_allowed=False))
        assert code == 1
        assert "result_packet_write_not_allowed" in out["blockers"]
        assert result == {}
        assert reentry == {}
    print("qi_github_actions_next_cycle_result_bridge_v9_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

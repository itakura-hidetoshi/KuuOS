#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_next_cycle_external_bridge_v9_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_next_cycle_external_bridge_enabled": True, "apply_github_actions_next_cycle_external_bridge": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_LICENSE_READY", "execution_packet_read_allowed": True, "output_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def execution(state: str, action: str = "none", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"execution_allowed": True, "next_cycle_state": "state", "execution_state": state, "connector_action": action, "connector_payload": payload or {}}


def runs_payload() -> dict[str, Any]:
    return {"reentry_allowed": True, "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}], "status_summary": {"all_success": True, "any_failed": False}}


def run(root: pathlib.Path, name: str, packet: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_next_cycle_execution_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    out = load_json(op)
    return done.returncode, out, load_json(pathlib.Path(out.get("output_packet_path", ""))) if out.get("output_packet_path") else {}


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_READY", case
    assert out["output_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "closed", execution("cycle_closed"), lic())
        assert_ready("closed", code, out, packet)
        assert out["bridge_state"] == "cycle_closed_final"
        assert packet["closure_allowed"] is True

        payload = {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
        code, out, packet = run(root, "external", execution("external_reobserve_ready", "GitHub.fetch_commit_workflow_runs", payload), lic())
        assert_ready("external", code, out, packet)
        assert out["bridge_state"] == "next_cycle_external_call_ready"
        assert packet["external_call_allowed"] is True
        assert packet["connector_payload"]["commit_sha"] == "abc"

        code, out, packet = run(root, "reentry", execution("policy_reentry_ready", "none", runs_payload()), lic())
        assert_ready("reentry", code, out, packet)
        assert out["bridge_state"] == "policy_reentry_bridge_ready"
        assert packet["reentry_bridge_allowed"] is True
        assert packet["status_summary"]["all_success"] is True

        bad_payload = {"repo_full_name": "bad", "commit_sha": "abc"}
        code, out, packet = run(root, "bad_external", execution("external_reobserve_ready", "GitHub.fetch_commit_workflow_runs", bad_payload), lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_action", execution("external_reobserve_ready", "none", payload), lic())
        assert code == 1
        assert "connector_action_mismatch" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", execution("cycle_closed"), lic(output_packet_write_allowed=False))
        assert code == 1
        assert "output_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_next_cycle_external_bridge_v9_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

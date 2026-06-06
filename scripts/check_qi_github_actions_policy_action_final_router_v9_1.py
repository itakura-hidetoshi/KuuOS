#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_action_final_router_v9_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_final_router_enabled": True, "apply_github_actions_policy_action_final_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_LICENSE_READY", "final_receipt_packet_read_allowed": True, "route_packet_write_allowed": True, "feedback_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def final_receipt(state: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": state, "next_expected": "next", "connector_action": "GitHub.merge_pull_request", "connector_result": result or {"merged": True, "sha": "abc"}}


def runs() -> list[dict[str, Any]]:
    return [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]


def run(root: pathlib.Path, name: str, receipt: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_policy_action_final_receipt_packet.json", receipt)
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
        load_json(runtime / "qi_github_actions_policy_action_final_route_packet.json"),
        load_json(runtime / "qi_github_actions_raw_commit_workflow_runs_packet.json"),
        load_json(runtime / "qi_github_actions_status_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], route: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_READY", case
    assert out["route_packet_written"] is True, case
    assert not out["blockers"], case
    assert route["route_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, route, wf, status = run(root, "close", final_receipt("action_completed"), lic())
        assert_ready("close", code, out, route)
        assert out["route_state"] == "close_autopilot_cycle"
        assert wf == {}
        assert status == {}

        code, out, route, wf, status = run(root, "rerun", final_receipt("action_rerun_requested", {"success": True}), lic())
        assert_ready("rerun", code, out, route)
        assert out["route_state"] == "wait_for_new_workflow_runs"
        assert wf == {}
        assert status == {}

        code, out, route, wf, status = run(root, "reobserve", final_receipt("action_reobserve_ready", {"workflow_runs": runs()}), lic())
        assert_ready("reobserve", code, out, route)
        assert out["route_state"] == "feed_reobserved_workflow_runs"
        assert out["feedback_packets_written"] is True
        assert wf["workflow_runs"]
        assert status["all_success"] is True

        code, out, route, wf, status = run(root, "missing_runs", final_receipt("action_reobserve_ready", {"workflow_runs": []}), lic())
        assert code == 1
        assert "workflow_runs_empty_or_invalid" in out["blockers"]
        assert route == {}

        code, out, route, wf, status = run(root, "license_block", final_receipt("action_completed"), lic(route_packet_write_allowed=False))
        assert code == 1
        assert "route_packet_write_not_allowed" in out["blockers"]
        assert route == {}
    print("qi_github_actions_policy_action_final_router_v9_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

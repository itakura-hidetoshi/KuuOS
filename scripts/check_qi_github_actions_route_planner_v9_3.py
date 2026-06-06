#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_route_planner_v9_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_route_planner_enabled": True, "apply_github_actions_route_planner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_ROUTE_PLANNER_LICENSE_READY", "route_packet_read_allowed": True, "context_packet_read_allowed": True, "next_cycle_packet_write_allowed": True, "reobserve_request_write_allowed": True, "reentry_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def route(state: str) -> dict[str, Any]:
    return {"route_allowed": True, "final_state": "state", "route_state": state, "next_expected": "next"}


def query() -> dict[str, Any]:
    return {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "commit_sha": "abc"}


def pr() -> dict[str, Any]:
    return {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc"}


def runs() -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
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
    return (
        done.returncode,
        load_json(op),
        load_json(runtime / "qi_github_actions_route_next_cycle_packet.json"),
        load_json(runtime / "qi_github_actions_route_reobserve_request_packet.json"),
        load_json(runtime / "qi_github_actions_route_policy_reentry_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], next_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_ROUTE_PLANNER_READY", case
    assert out["next_cycle_packet_written"] is True, case
    assert not out["blockers"], case
    assert next_packet["next_cycle_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, next_packet, req, reentry = run(root, "close", {"qi_github_actions_policy_action_final_route_packet.json": route("close_autopilot_cycle")}, lic())
        assert_ready("close", code, out, next_packet)
        assert out["next_cycle_state"] == "closed"
        assert req == {}
        assert reentry == {}

        files = {"qi_github_actions_policy_action_final_route_packet.json": route("wait_for_new_workflow_runs"), "qi_github_actions_pr_live_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": pr()}
        code, out, next_packet, req, reentry = run(root, "wait", files, lic())
        assert_ready("wait", code, out, next_packet)
        assert out["next_cycle_state"] == "await_workflow_reobserve"
        assert out["next_connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert req["connector_payload"]["commit_sha"] == "abc"
        assert reentry == {}

        files = {"qi_github_actions_policy_action_final_route_packet.json": route("feed_reobserved_workflow_runs"), "qi_github_actions_raw_commit_workflow_runs_packet.json": runs()}
        code, out, next_packet, req, reentry = run(root, "reentry", files, lic())
        assert_ready("reentry", code, out, next_packet)
        assert out["next_cycle_state"] == "reenter_policy_loop"
        assert reentry["reentry_allowed"] is True
        assert reentry["status_summary"]["all_success"] is True

        files = {"qi_github_actions_policy_action_final_route_packet.json": route("feed_reobserved_workflow_runs"), "qi_github_actions_raw_commit_workflow_runs_packet.json": {"workflow_runs": []}}
        code, out, next_packet, req, reentry = run(root, "missing_runs", files, lic())
        assert code == 1
        assert "workflow_runs_empty_or_invalid" in out["blockers"]
        assert next_packet == {}

        files = {"qi_github_actions_policy_action_final_route_packet.json": route("wait_for_new_workflow_runs"), "qi_github_actions_pr_live_query_packet.json": {"repo_full_name": "bad"}}
        code, out, next_packet, req, reentry = run(root, "bad_wait", files, lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert next_packet == {}

        code, out, next_packet, req, reentry = run(root, "license_block", {"qi_github_actions_policy_action_final_route_packet.json": route("close_autopilot_cycle")}, lic(next_cycle_packet_write_allowed=False))
        assert code == 1
        assert "next_cycle_packet_write_not_allowed" in out["blockers"]
        assert next_packet == {}
    print("qi_github_actions_route_planner_v9_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

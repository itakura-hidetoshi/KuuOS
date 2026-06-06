#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_unified_closed_loop_v10_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 6) -> dict[str, Any]:
    return {"qi_github_actions_unified_closed_loop_enabled": True, "apply_github_actions_unified_closed_loop": True, "runtime_root": str(root), "max_unified_closed_loop_phases": max_phases, "max_inner_closed_loop_phases": 8, "max_inner_reentry_merge_phases": 10}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_LICENSE_READY", "closed_loop_supercycle_run_allowed": True, "reentry_merge_supercycle_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def closure() -> dict[str, Any]:
    return {"closure_allowed": True, "bridge_state": "cycle_closed_final"}


def workflow_success() -> list[dict[str, Any]]:
    return [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]


def reentry_packet() -> dict[str, Any]:
    runs = workflow_success()
    return {"policy_reentry_allowed": True, "reentry_state": "policy_reentry_ready", "query_context": {"repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}, "status_summary": {"all_success": True, "any_failed": False, "any_pending": False, "all_completed": True, "workflow_run_count": len(runs), "workflow_runs": runs}, "workflow_runs": runs}


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": True, "sha": "merge-sha"}}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 6) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, max_phases))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "closure", {"qi_github_actions_next_cycle_closure_packet.json": closure()}, lic())
        assert_ready("closure", code, out)
        assert out["final_stage"] == "closure_present"
        assert out["unified_state"] == "cycle_closed"
        assert out["phases_run"] == 0

        code, out = run(root, "reentry", {"qi_github_actions_policy_reentry_packet.json": reentry_packet()}, lic())
        assert_ready("reentry", code, out)
        assert out["final_stage"] in {"run_reentry_merge_supercycle", "policy_action_final_receipt_present"}
        assert out["connector_action"] in {"GitHub.get_pr_info", "GitHub.merge_pull_request", "none"}

        code, out = run(root, "final", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("final", code, out)
        assert out["final_stage"] == "policy_action_final_receipt_present"
        assert out["unified_state"] == "action_completed"
        assert out["phases_run"] == 0

        code, out = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["final_stage"] in {"run_closed_loop_supercycle", "run_reentry_merge_supercycle", "policy_action_final_receipt_present"}

        code, out = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_unified_closed_loop_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(reentry_merge_supercycle_run_allowed=False))
        assert code == 1
        assert "reentry_merge_supercycle_run_not_allowed" in out["blockers"]
    print("qi_github_actions_unified_closed_loop_v10_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

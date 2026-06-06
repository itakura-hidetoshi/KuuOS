#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_dispatch_supercycle_v10_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, max_phases: int = 8) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_supercycle_enabled": True, "apply_github_actions_dispatch_supercycle": True, "runtime_root": str(root), "max_dispatch_supercycle_phases": max_phases, "max_inner_unified_closed_loop_phases": 6}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_LICENSE_READY", "unified_closed_loop_run_allowed": True, "dispatch_router_run_allowed": True, "dispatch_result_router_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], max_phases: int = 8) -> tuple[int, dict[str, Any]]:
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
    assert out["status"] == "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_READY", case
    assert not out["blockers"], case


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request", "connector_result": {"merged": True, "sha": "merge-sha"}}


def closure() -> dict[str, Any]:
    return {"closure_allowed": True, "bridge_state": "cycle_closed_final"}


def pr_info_call() -> dict[str, Any]:
    return {"external_call_allowed": True, "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}}


def dispatch(action: str) -> dict[str, Any]:
    return {"dispatch_allowed": True, "dispatch_kind": "policy_reentry_pr_info", "connector_action": action, "raw_result_expected_file": "qi_github_actions_dispatch_pr_info_raw_result_packet.json"}


def pr_info_raw() -> dict[str, Any]:
    return {"connector_action": "GitHub.get_pr_info", "repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "head_sha": "abc"}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "final", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("final", code, out)
        assert out["final_stage"] == "final_receipt_present"
        assert out["supercycle_state"] == "action_completed"
        assert out["phases_run"] == 0

        code, out = run(root, "closure", {"qi_github_actions_next_cycle_closure_packet.json": closure()}, lic())
        assert_ready("closure", code, out)
        assert out["final_stage"] == "closure_present"
        assert out["supercycle_state"] == "cycle_closed"
        assert out["phases_run"] == 0

        code, out = run(root, "call_to_dispatch_wait", {"qi_github_actions_policy_reentry_external_call_packet.json": pr_info_call()}, lic())
        assert_ready("call_to_dispatch_wait", code, out)
        assert out["final_stage"] == "await_dispatch_external_result"
        assert out["connector_action"] == "GitHub.get_pr_info"

        files = {"qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.get_pr_info"), "qi_github_actions_dispatch_pr_info_raw_result_packet.json": pr_info_raw()}
        code, out = run(root, "raw_to_target", files, lic())
        assert_ready("raw_to_target", code, out)
        assert out["final_stage"] in {"run_dispatch_result_router", "await_pr_info_external_result", "run_reentry_merge_supercycle"}
        assert out["connector_action"] in {"GitHub.get_pr_info", "none"}

        code, out = run(root, "initial", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic())
        assert_ready("initial", code, out)
        assert out["final_stage"] in {"run_unified_closed_loop", "run_dispatch_router", "await_dispatch_external_result", "run_dispatch_result_router"}

        code, out = run(root, "bad_cap", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(), 0)
        assert code == 1
        assert "max_dispatch_supercycle_phases_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_pr_live_autopilot_query_packet.json": query()}, lic(dispatch_result_router_run_allowed=False))
        assert code == 1
        assert "dispatch_result_router_run_not_allowed" in out["blockers"]
    print("qi_github_actions_dispatch_supercycle_v10_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

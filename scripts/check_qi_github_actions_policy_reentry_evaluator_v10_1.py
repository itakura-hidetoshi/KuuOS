#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_reentry_evaluator_v10_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_reentry_evaluator_enabled": True, "apply_github_actions_policy_reentry_evaluator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_LICENSE_READY", "policy_reentry_packet_read_allowed": True, "evaluation_packet_write_allowed": True, "handoff_packet_write_allowed": True, "external_call_packet_write_allowed": True, "live_query_packet_write_allowed": True, "status_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run_item(conclusion: str | None, status: str = "completed", run_id: int = 10) -> dict[str, Any]:
    value: dict[str, Any] = {"id": run_id, "name": "Qi Process Tensor Review Checks", "status": status}
    if conclusion is not None:
        value["conclusion"] = conclusion
    return value


def reentry(runs: list[dict[str, Any]], *, merge: bool = True, rerun: bool = True, reobserve: bool = True, repo: str = "itakura-hidetoshi/KuuOS") -> dict[str, Any]:
    all_success = bool(runs) and all(item.get("status") == "completed" and item.get("conclusion") == "success" for item in runs)
    any_failed = any(item.get("conclusion") in {"failure", "cancelled", "timed_out"} for item in runs)
    any_pending = any(item.get("status") != "completed" for item in runs)
    return {
        "policy_reentry_allowed": True,
        "reentry_state": "policy_reentry_ready",
        "query_context": {"repo_full_name": repo, "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": merge, "rerun_when_failed": rerun, "reobserve_when_pending": reobserve},
        "status_summary": {"all_success": all_success, "any_failed": any_failed, "any_pending": any_pending, "all_completed": not any_pending, "workflow_run_count": len(runs), "workflow_runs": runs},
        "workflow_runs": runs,
    }


def run(root: pathlib.Path, name: str, packet: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_policy_reentry_packet.json", packet)
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
        load_json(runtime / "qi_github_actions_policy_reentry_evaluation_packet.json"),
        load_json(runtime / "qi_github_actions_pr_live_autopilot_handoff_packet.json"),
        load_json(runtime / "qi_github_actions_policy_reentry_external_call_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], eval_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_READY", case
    assert out["evaluation_packet_written"] is True, case
    assert not out["blockers"], case
    assert eval_packet["evaluation_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, eval_packet, handoff, external = run(root, "success", reentry([run_item("success")]), lic())
        assert_ready("success", code, out, eval_packet)
        assert out["evaluation_state"] == "pr_info_refresh_required"
        assert out["connector_action"] == "GitHub.get_pr_info"
        assert out["external_call_packet_written"] is True
        assert handoff == {}
        assert external["connector_payload"]["pr_number"] == 1

        code, out, eval_packet, handoff, external = run(root, "failure", reentry([run_item("failure", run_id=22)]), lic())
        assert_ready("failure", code, out, eval_packet)
        assert out["evaluation_state"] == "rerun_ready"
        assert out["action_prepared"] == "rerun_failed_workflow_run_jobs"
        assert out["handoff_packet_written"] is True
        assert handoff["action_prepared"] == "rerun_failed_workflow_run_jobs"
        assert external == {}

        code, out, eval_packet, handoff, external = run(root, "pending", reentry([run_item(None, "in_progress")]), lic())
        assert_ready("pending", code, out, eval_packet)
        assert out["evaluation_state"] == "pending_reobserve_required"
        assert out["action_prepared"] == "commit_workflow_runs_reobserve"
        assert handoff["policy_decision"] == "policy_pending_reobserve"
        assert external["connector_action"] == "GitHub.fetch_commit_workflow_runs"

        code, out, eval_packet, handoff, external = run(root, "green_hold", reentry([run_item("success")], merge=False), lic())
        assert_ready("green_hold", code, out, eval_packet)
        assert out["evaluation_state"] == "green_hold"
        assert out["action_prepared"] == "none"
        assert handoff == {}
        assert external == {}

        code, out, eval_packet, handoff, external = run(root, "bad_repo", reentry([run_item("success")], repo="bad"), lic())
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert eval_packet == {}

        code, out, eval_packet, handoff, external = run(root, "license_block", reentry([run_item("success")]), lic(evaluation_packet_write_allowed=False))
        assert code == 1
        assert "evaluation_packet_write_not_allowed" in out["blockers"]
        assert eval_packet == {}
    print("qi_github_actions_policy_reentry_evaluator_v10_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

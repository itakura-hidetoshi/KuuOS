#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_reentry_adapter_v9_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_reentry_adapter_enabled": True, "apply_github_actions_policy_reentry_adapter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_LICENSE_READY", "reentry_bridge_packet_read_allowed": True, "context_packet_read_allowed": True, "raw_workflow_packet_write_allowed": True, "status_packet_write_allowed": True, "policy_reentry_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run_item(conclusion: str | None, status: str = "completed") -> dict[str, Any]:
    value: dict[str, Any] = {"id": 10, "name": "Qi Process Tensor Review Checks", "status": status}
    if conclusion is not None:
        value["conclusion"] = conclusion
    return value


def reentry(runs: list[dict[str, Any]]) -> dict[str, Any]:
    all_success = bool(runs) and all(item.get("status") == "completed" and item.get("conclusion") == "success" for item in runs)
    any_failed = any(item.get("conclusion") in {"failure", "cancelled", "timed_out"} for item in runs)
    return {"reentry_bridge_allowed": True, "bridge_state": "policy_reentry_bridge_ready", "workflow_runs": runs, "status_summary": {"all_success": all_success, "any_failed": any_failed, "workflow_run_count": len(runs)}}


def query() -> dict[str, Any]:
    return {"query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


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
        load_json(runtime / "qi_github_actions_raw_commit_workflow_runs_packet.json"),
        load_json(runtime / "qi_github_actions_status_packet.json"),
        load_json(runtime / "qi_github_actions_policy_reentry_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], raw: dict[str, Any], status: dict[str, Any], reentry_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_READY", case
    assert out["raw_workflow_runs_written"] is True, case
    assert out["status_packet_written"] is True, case
    assert out["reentry_packet_written"] is True, case
    assert not out["blockers"], case
    assert raw["workflow_runs"], case
    assert reentry_packet["policy_reentry_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": reentry([run_item("success")]), "qi_github_actions_pr_live_query_packet.json": query()}
        code, out, raw, status, reentry_packet = run(root, "success", files, lic())
        assert_ready("success", code, out, raw, status, reentry_packet)
        assert status["all_success"] is True
        assert reentry_packet["status_summary"]["all_success"] is True
        assert reentry_packet["query_context"]["repo_full_name"] == "itakura-hidetoshi/KuuOS"

        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": reentry([run_item("failure")]), "qi_github_actions_pr_live_query_packet.json": query()}
        code, out, raw, status, reentry_packet = run(root, "failure", files, lic())
        assert_ready("failure", code, out, raw, status, reentry_packet)
        assert status["any_failed"] is True
        assert reentry_packet["status_summary"]["any_failed"] is True

        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": reentry([run_item(None, "in_progress")])}
        code, out, raw, status, reentry_packet = run(root, "pending_no_query", files, lic())
        assert_ready("pending_no_query", code, out, raw, status, reentry_packet)
        assert status["any_pending"] is True
        assert "query_context_missing" in out["warnings"]

        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": reentry([]), "qi_github_actions_pr_live_query_packet.json": query()}
        code, out, raw, status, reentry_packet = run(root, "empty_runs", files, lic())
        assert code == 1
        assert "workflow_runs_empty_or_invalid" in out["blockers"]
        assert raw == {}
        assert reentry_packet == {}

        bad = reentry([run_item("success")])
        bad["bridge_state"] = "wrong"
        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": bad, "qi_github_actions_pr_live_query_packet.json": query()}
        code, out, raw, status, reentry_packet = run(root, "bad_state", files, lic())
        assert code == 1
        assert "bridge_state_not_policy_reentry_bridge_ready" in out["blockers"]

        files = {"qi_github_actions_next_cycle_reentry_bridge_packet.json": reentry([run_item("success")]), "qi_github_actions_pr_live_query_packet.json": query()}
        code, out, raw, status, reentry_packet = run(root, "license_block", files, lic(policy_reentry_packet_write_allowed=False))
        assert code == 1
        assert "policy_reentry_packet_write_not_allowed" in out["blockers"]
        assert reentry_packet == {}
    print("qi_github_actions_policy_reentry_adapter_v9_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

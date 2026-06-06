#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_snapshot_collector_v7_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_snapshot_collector_enabled": True, "apply_github_actions_pr_live_snapshot_collector": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_LICENSE_READY", "raw_pr_info_read_allowed": True, "raw_workflow_runs_read_allowed": True, "snapshot_packet_write_allowed": True, "adapter_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def raw_pr(**overrides: Any) -> dict[str, Any]:
    value = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "base": "main"}
    value.update(overrides)
    return value


def raw_runs(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def config(**overrides: Any) -> dict[str, Any]:
    value = {"adapter_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_snapshot_packet.json"), load_json(runtime / "qi_github_actions_commit_workflow_runs_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], pr_packet: dict[str, Any], runs_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_READY", case
    assert out["collector_result"] == "snapshot_packets_written", case
    assert not out["blockers"], case
    assert pr_packet["head_sha"], case
    assert runs_packet["workflow_runs"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_raw_pr_info_packet.json": raw_pr(), "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "green", files, lic())
        assert_ready("green", code, out, pr_packet, runs_packet)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        nested = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "head": {"sha": "nestedabc"}, "base": {"ref": "main"}}
        files = {"qi_github_actions_raw_pr_info_packet.json": nested, "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs("failure"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "nested_failed", files, lic())
        assert_ready("nested_failed", code, out, pr_packet, runs_packet)
        assert pr_packet["head_sha"] == "nestedabc"
        assert out["policy_decision"] == "policy_failed_rerun"

        files = {"qi_github_actions_raw_pr_info_packet.json": raw_pr(), "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs(None, "in_progress"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "pending", files, lic())
        assert_ready("pending", code, out, pr_packet, runs_packet)
        assert out["policy_decision"] == "policy_pending_reobserve"

        files = {"qi_github_actions_raw_pr_info_packet.json": raw_pr(state="closed"), "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "closed", files, lic())
        assert code == 1
        assert "pr_live_snapshot_adapter_not_ready" in out["blockers"]

        files = {"qi_github_actions_raw_pr_info_packet.json": raw_pr(), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "missing_runs", files, lic())
        assert code == 1
        assert "raw_workflow_runs_packet_missing_or_invalid" in out["blockers"]

        files = {"qi_github_actions_raw_pr_info_packet.json": raw_pr(), "qi_github_actions_raw_commit_workflow_runs_packet.json": raw_runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, pr_packet, runs_packet = run(root, "license_block", files, lic(snapshot_packet_write_allowed=False))
        assert code == 1
        assert "snapshot_packet_write_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_snapshot_collector_v7_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

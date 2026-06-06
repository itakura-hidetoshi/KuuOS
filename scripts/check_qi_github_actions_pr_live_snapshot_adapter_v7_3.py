#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_snapshot_adapter_v7_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_snapshot_adapter_enabled": True, "apply_github_actions_pr_live_snapshot_adapter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_LICENSE_READY", "pr_snapshot_read_allowed": True, "workflow_runs_read_allowed": True, "entry_packet_write_allowed": True, "entrypoint_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def pr_snapshot(**overrides: Any) -> dict[str, Any]:
    value = {"repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "base": "main"}
    value.update(overrides)
    return value


def runs(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}]}


def config(**overrides: Any) -> dict[str, Any]:
    value = {"adapter_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}
    value.update(overrides)
    return value


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_policy_entry_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], entry: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_READY", case
    assert out["adapter_result"] == "entry_packet_written", case
    assert not out["blockers"], case
    assert entry["entry_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(), "qi_github_actions_commit_workflow_runs_packet.json": runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "green", files, lic())
        assert_ready("green", code, out, entry)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(), "qi_github_actions_commit_workflow_runs_packet.json": runs("failure"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "failed", files, lic())
        assert_ready("failed", code, out, entry)
        assert out["policy_decision"] == "policy_failed_rerun"

        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(), "qi_github_actions_commit_workflow_runs_packet.json": runs(None, "in_progress"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "pending", files, lic())
        assert_ready("pending", code, out, entry)
        assert out["policy_decision"] == "policy_pending_reobserve"

        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(state="closed"), "qi_github_actions_commit_workflow_runs_packet.json": runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "closed", files, lic())
        assert code == 1
        assert "pr_not_open" in out["blockers"]
        assert entry == {}

        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "missing_runs", files, lic())
        assert code == 1
        assert "workflow_runs_packet_missing_or_invalid" in out["blockers"]
        assert entry == {}

        files = {"qi_github_actions_pr_snapshot_packet.json": pr_snapshot(), "qi_github_actions_commit_workflow_runs_packet.json": runs("success"), "qi_github_actions_pr_live_policy_config.json": config()}
        code, out, entry = run(root, "license_block", files, lic(entry_packet_write_allowed=False))
        assert code == 1
        assert "entry_packet_write_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_snapshot_adapter_v7_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

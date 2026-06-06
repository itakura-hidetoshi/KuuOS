#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_policy_entrypoint_v7_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_policy_entrypoint_enabled": True, "apply_github_actions_pr_policy_entrypoint": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_LICENSE_READY", "entry_packet_read_allowed": True, "intent_packet_write_allowed": True, "status_packet_write_allowed": True, "guarded_runner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def entry(conclusion: str | None = "success", run_status: str = "completed", **overrides: Any) -> dict[str, Any]:
    value = {"entry_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "head_sha": "abc", "commit_sha": "abc", "base_branch": "main", "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True, "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": run_status, "conclusion": conclusion}]}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_github_actions_pr_policy_entry_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_policy_intent_packet.json"), load_json(runtime / "qi_github_actions_status_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], intent_packet: dict[str, Any], status_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_READY", case
    assert out["entry_result"] == "packets_written", case
    assert not out["blockers"], case
    assert intent_packet["policy_intent_allowed"] is True, case
    assert status_packet["github_actions_status_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, intent_packet, status_packet = run(root, "green", entry("success"), lic())
        assert_ready("green", code, out, intent_packet, status_packet)
        assert out["policy_decision"] == "policy_all_green"
        assert out["action_prepared"] == "merge_pull_request"

        code, out, intent_packet, status_packet = run(root, "failed", entry("failure", "completed"), lic())
        assert_ready("failed", code, out, intent_packet, status_packet)
        assert out["policy_decision"] == "policy_failed_rerun"
        assert out["action_prepared"] == "rerun_failed_workflow_run_jobs"

        code, out, intent_packet, status_packet = run(root, "pending", entry(None, "in_progress"), lic())
        assert_ready("pending", code, out, intent_packet, status_packet)
        assert out["policy_decision"] == "policy_pending_reobserve"

        code, out, intent_packet, status_packet = run(root, "missing_sha", entry("success", head_sha="", commit_sha=""), lic())
        assert code == 1
        assert "head_sha_missing" in out["blockers"]
        assert intent_packet == {}
        assert status_packet == {}

        code, out, intent_packet, status_packet = run(root, "missing_entry", None, lic())
        assert code == 1
        assert "entry_packet_missing_or_invalid" in out["blockers"]

        code, out, intent_packet, status_packet = run(root, "license_block", entry("success"), lic(status_packet_write_allowed=False))
        assert code == 1
        assert "status_packet_write_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_policy_entrypoint_v7_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

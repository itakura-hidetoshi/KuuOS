#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_info_result_bridge_v10_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_info_result_bridge_enabled": True, "apply_github_actions_pr_info_result_bridge": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "raw_pr_info_packet_write_allowed": True, "handoff_packet_write_allowed": True, "evaluation_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def call() -> dict[str, Any]:
    return {"external_call_allowed": True, "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}}


def raw(**overrides: Any) -> dict[str, Any]:
    value = {"connector_action": "GitHub.get_pr_info", "repo_full_name": "itakura-hidetoshi/KuuOS", "number": 1, "state": "open", "draft": False, "merged": False, "mergeable": True, "head_sha": "abc", "base": "main"}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, call_packet: dict[str, Any], raw_packet: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_github_actions_policy_reentry_external_call_packet.json", call_packet)
    dump(runtime / "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json", raw_packet)
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
        load_json(runtime / "qi_github_actions_raw_pr_info_packet.json"),
        load_json(runtime / "qi_github_actions_pr_live_autopilot_handoff_packet.json"),
        load_json(runtime / "qi_github_actions_policy_reentry_pr_info_evaluation_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], pr: dict[str, Any], eval_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_READY", case
    assert out["raw_pr_info_written"] is True, case
    assert out["evaluation_packet_written"] is True, case
    assert not out["blockers"], case
    assert pr["head_sha"] == "abc", case
    assert eval_packet["evaluation_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, pr, handoff, eval_packet = run(root, "open", call(), raw(), lic())
        assert_ready("open", code, out, pr, eval_packet)
        assert out["bridge_state"] == "merge_handoff_ready"
        assert out["handoff_packet_written"] is True
        assert handoff["action_prepared"] == "merge_pull_request"

        code, out, pr, handoff, eval_packet = run(root, "draft", call(), raw(draft=True), lic())
        assert_ready("draft", code, out, pr, eval_packet)
        assert out["bridge_state"] == "merge_hold"
        assert "pr_is_draft" in out["warnings"]
        assert handoff == {}

        code, out, pr, handoff, eval_packet = run(root, "closed", call(), raw(state="closed"), lic())
        assert_ready("closed", code, out, pr, eval_packet)
        assert out["bridge_state"] == "merge_hold"
        assert "pr_not_open" in out["warnings"]
        assert handoff == {}

        code, out, pr, handoff, eval_packet = run(root, "merged", call(), raw(merged=True), lic())
        assert_ready("merged", code, out, pr, eval_packet)
        assert out["bridge_state"] == "merge_hold"
        assert "pr_already_merged" in out["warnings"]
        assert handoff == {}

        code, out, pr, handoff, eval_packet = run(root, "bad_action", call(), raw(connector_action="GitHub.fetch_commit_workflow_runs"), lic())
        assert code == 1
        assert "raw_result_connector_action_mismatch" in out["blockers"]
        assert pr == {}
        assert handoff == {}

        code, out, pr, handoff, eval_packet = run(root, "license_block", call(), raw(), lic(handoff_packet_write_allowed=False))
        assert code == 1
        assert "handoff_packet_write_not_allowed" in out["blockers"]
        assert pr == {}
        assert handoff == {}
    print("qi_github_actions_pr_info_result_bridge_v10_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

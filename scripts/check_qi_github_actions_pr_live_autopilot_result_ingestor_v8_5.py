#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_autopilot_result_ingestor_v8_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_autopilot_result_ingestor_enabled": True, "apply_github_actions_pr_live_autopilot_result_ingestor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_LICENSE_READY", "handoff_packet_read_allowed": True, "connector_result_read_allowed": True, "raw_result_packet_write_allowed": True, "autopilot_runner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def query() -> dict[str, Any]:
    return {"autopilot_query_allowed": True, "repo_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "required_workflows": ["Qi Process Tensor Review Checks"], "merge_when_green": True, "rerun_when_failed": True, "reobserve_when_pending": True}


def handoff(action: str) -> dict[str, Any]:
    payload = {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1} if action == "GitHub.get_pr_info" else {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
    return {"handoff_allowed": True, "autopilot_state": "await_external_connector", "connector_action": action, "connector_payload": payload, "external_call_packet": {"connector_action": action, "connector_payload": payload}, "next_expected": "call connector"}


def pr_result(**overrides: Any) -> dict[str, Any]:
    value = {"connector_action": "GitHub.get_pr_info", "number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS"}
    value.update(overrides)
    return value


def runs_result(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"connector_action": "GitHub.fetch_commit_workflow_runs", "workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def raw_pr_packet() -> dict[str, Any]:
    return {"number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS", "base": "main"}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_live_external_call_raw_result_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], raw: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_READY", case
    assert out["raw_result_written"] is True, case
    assert not out["blockers"], case
    assert raw["version"] == "qi_github_actions_pr_live_external_call_raw_result_from_autopilot_ingestor_v8_5", case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("GitHub.get_pr_info"), "qi_github_actions_pr_live_autopilot_connector_result_packet.json": pr_result()}
        code, out, raw = run(root, "pr", files, lic())
        assert_ready("pr", code, out, raw)
        assert raw["connector_action"] == "GitHub.get_pr_info"
        assert raw["connector_result"]["head_sha"] == "abc"

        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_raw_pr_info_packet.json": raw_pr_packet(), "qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("GitHub.fetch_commit_workflow_runs"), "qi_github_actions_pr_live_autopilot_connector_result_packet.json": runs_result("success")}
        code, out, raw = run(root, "runs", files, lic())
        assert_ready("runs", code, out, raw)
        assert raw["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert raw["connector_result"]["workflow_runs"]

        bad = pr_result(connector_action="GitHub.fetch_commit_workflow_runs")
        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("GitHub.get_pr_info"), "qi_github_actions_pr_live_autopilot_connector_result_packet.json": bad}
        code, out, raw = run(root, "mismatch", files, lic())
        assert code == 1
        assert "connector_action_mismatch" in out["blockers"]

        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("GitHub.get_pr_info"), "qi_github_actions_pr_live_autopilot_connector_result_packet.json": {"connector_action": "GitHub.get_pr_info", "number": 1}}
        code, out, raw = run(root, "missing_head", files, lic())
        assert code == 1
        assert "head_sha_missing" in out["blockers"]

        files = {"qi_github_actions_pr_live_autopilot_query_packet.json": query(), "qi_github_actions_pr_live_autopilot_handoff_packet.json": handoff("GitHub.get_pr_info"), "qi_github_actions_pr_live_autopilot_connector_result_packet.json": pr_result()}
        code, out, raw = run(root, "license_block", files, lic(raw_result_packet_write_allowed=False))
        assert code == 1
        assert "raw_result_packet_write_not_allowed" in out["blockers"]
    print("qi_github_actions_pr_live_autopilot_result_ingestor_v8_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_external_call_bridge_v8_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, target: str | None = None) -> dict[str, Any]:
    value = {"qi_github_actions_pr_live_external_call_bridge_enabled": True, "apply_github_actions_pr_live_external_call_bridge": True, "runtime_root": str(root)}
    if target:
        value["dispatch_target"] = target
    return value


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_LICENSE_READY", "dispatch_packet_read_allowed": True, "external_call_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_external_call"] = True
    value.update(overrides)
    return value


def pr_dispatch(**overrides: Any) -> dict[str, Any]:
    value = {"dispatch_target": "pr_info", "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "result_expected_file": "qi_github_actions_raw_pr_info_packet.json"}
    value.update(overrides)
    return value


def runs_dispatch(**overrides: Any) -> dict[str, Any]:
    value = {"dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_raw_commit_workflow_runs_packet.json"}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], target: str | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, target))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_live_external_call_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_READY", case
    assert out["external_call_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["external_call_allowed"] is True, case
    assert packet["boundary"]["result_must_be_collected_by_v7_9"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "pr", {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch()}, lic("pr_info"))
        assert_ready("pr", code, out, packet)
        assert packet["dispatch_target"] == "pr_info"
        assert packet["connector_action"] == "GitHub.get_pr_info"
        assert packet["dispatch_result_expected_file"] == "qi_github_actions_pr_live_dispatch_pr_info_result.json"

        code, out, packet = run(root, "runs", {"qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json": runs_dispatch()}, lic("commit_workflow_runs"))
        assert_ready("runs", code, out, packet)
        assert packet["dispatch_target"] == "commit_workflow_runs"
        assert packet["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert packet["dispatch_result_expected_file"] == "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json"

        bad_repo = pr_dispatch(connector_payload={"repository_full_name": "bad", "pr_number": 1})
        code, out, packet = run(root, "bad_repo", {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": bad_repo}, lic("pr_info"), "pr_info")
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert packet == {}

        mismatch = pr_dispatch(connector_action="GitHub.fetch_commit_workflow_runs")
        code, out, packet = run(root, "mismatch", {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": mismatch}, lic("pr_info"), "pr_info")
        assert code == 1
        assert "connector_action_mismatch" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_pr_live_dispatch_pr_info_packet.json": pr_dispatch()}, lic())
        assert code == 1
        assert "pr_info_not_allowed_by_external_call_bridge_license" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_pr_live_external_call_bridge_v8_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

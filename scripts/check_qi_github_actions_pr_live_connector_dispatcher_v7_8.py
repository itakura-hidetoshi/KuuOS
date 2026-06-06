#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_connector_dispatcher_v7_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_connector_dispatcher_enabled": True, "apply_github_actions_pr_live_connector_dispatcher": True, "runtime_root": str(root)}


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_CONNECTOR_DISPATCHER_LICENSE_READY", "connector_request_read_allowed": True, "dispatch_packet_write_allowed": True, "bridge_request_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_dispatch"] = True
    value.update(overrides)
    return value


def pr_request() -> dict[str, Any]:
    return {"connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "result_expected_file": "qi_github_actions_raw_pr_info_packet.json"}


def runs_request() -> dict[str, Any]:
    return {"connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "result_expected_file": "qi_github_actions_raw_commit_workflow_runs_packet.json"}


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
    return (
        done.returncode,
        load_json(op),
        load_json(runtime / "qi_github_actions_pr_live_connector_request.json"),
        load_json(pathlib.Path(load_json(op).get("dispatch_packet_path", ""))) if load_json(op).get("dispatch_packet_path") else {},
    )


def assert_ready(case: str, code: int, out: dict[str, Any], bridge: dict[str, Any], dispatch: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_CONNECTOR_DISPATCHER_READY", case
    assert out["dispatch_packet_written"] is True, case
    assert out["bridge_request_written"] is True, case
    assert not out["blockers"], case
    assert bridge["connector_action"] == dispatch["connector_action"], case
    assert dispatch["boundary"]["feeds_pr_live_result_adapter_v7_6"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, bridge, dispatch = run(root, "pr", {"qi_github_actions_pr_info_connector_request.json": pr_request()}, lic("pr_info"))
        assert_ready("pr", code, out, bridge, dispatch)
        assert out["dispatch_target"] == "pr_info"
        assert dispatch["connector_payload"]["pr_number"] == 1
        assert dispatch["result_expected_file"] == "qi_github_actions_raw_pr_info_packet.json"

        code, out, bridge, dispatch = run(root, "runs", {"qi_github_actions_commit_workflow_runs_connector_request.json": runs_request()}, lic("commit_workflow_runs"))
        assert_ready("runs", code, out, bridge, dispatch)
        assert out["dispatch_target"] == "commit_workflow_runs"
        assert dispatch["connector_payload"]["commit_sha"] == "abc"
        assert dispatch["result_expected_file"] == "qi_github_actions_raw_commit_workflow_runs_packet.json"

        code, out, bridge, dispatch = run(root, "bridge_priority", {"qi_github_actions_pr_live_connector_request.json": runs_request(), "qi_github_actions_pr_info_connector_request.json": pr_request()}, lic("commit_workflow_runs"))
        assert_ready("bridge_priority", code, out, bridge, dispatch)
        assert out["dispatch_target"] == "commit_workflow_runs"

        bad = {"connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "bad", "pr_number": 1}}
        code, out, bridge, dispatch = run(root, "bad_repo", {"qi_github_actions_pr_info_connector_request.json": bad}, lic("pr_info"))
        assert code == 1
        assert "repo_full_name_invalid" in out["blockers"]
        assert bridge == {}

        code, out, bridge, dispatch = run(root, "unsupported", {"qi_github_actions_pr_info_connector_request.json": {"connector_action": "GitHub.unknown", "connector_payload": {}}}, lic("pr_info"))
        assert code == 1
        assert "connector_action_not_dispatchable" in out["blockers"]
        assert bridge == {}

        code, out, bridge, dispatch = run(root, "license_block", {"qi_github_actions_pr_info_connector_request.json": pr_request()}, lic())
        assert code == 1
        assert "pr_info_not_allowed_by_pr_live_connector_dispatcher_license" in out["blockers"]
        assert bridge == {}
    print("qi_github_actions_pr_live_connector_dispatcher_v7_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

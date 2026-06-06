#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_external_call_dispatcher_v6_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_dispatcher_enabled": True, "apply_github_actions_external_call_dispatcher": True, "runtime_root": str(root)}


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_LICENSE_READY", "external_call_packet_read_allowed": True, "dispatch_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_dispatch"] = True
    value.update(overrides)
    return value


def call(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"connector_action": action, "connector_payload": payload}


def run(root: pathlib.Path, name: str, payload: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if payload is not None:
        dump(runtime / "qi_github_actions_external_call_packet.json", payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    out = load_json(op)
    packet = load_json(pathlib.Path(out.get("dispatch_packet_path", ""))) if out.get("dispatch_packet_path") else {}
    return done.returncode, out, packet


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_READY", case
    assert out["dispatch_packet_emitted"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["target_specific_payload"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "commit", call("GitHub.fetch_commit_workflow_runs", {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}), lic("commit_workflow_runs"))
        assert_ready("commit", code, out, packet)
        assert packet["dispatch_target"] == "commit_workflow_runs"
        assert packet["result_expected_file"] == "qi_github_actions_observation_connector_result_packet.json"

        code, out, packet = run(root, "rerun", call("GitHub.rerun_workflow_job", {"repo_full_name": "itakura-hidetoshi/KuuOS", "job_id": 10}), lic("rerun_workflow_job"))
        assert_ready("rerun", code, out, packet)
        assert packet["dispatch_target"] == "rerun_workflow_job"
        assert packet["result_expected_file"] == "qi_github_actions_connector_result_packet.json"

        code, out, packet = run(root, "bad_payload", call("GitHub.fetch_workflow_run_jobs", {"repo_full_name": "itakura-hidetoshi/KuuOS"}), lic("workflow_run_jobs"))
        assert code == 1
        assert "run_id_missing" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "unsupported", call("GitHub.unsupported", {"repo_full_name": "itakura-hidetoshi/KuuOS"}), lic("commit_workflow_runs"))
        assert code == 1
        assert "connector_action_not_dispatchable" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", call("GitHub.fetch_commit_workflow_runs", {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}), lic())
        assert code == 1
        assert "commit_workflow_runs_not_allowed_by_external_call_dispatcher_license" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing", None, lic("commit_workflow_runs"))
        assert code == 1
        assert "external_call_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_external_call_dispatcher_v6_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

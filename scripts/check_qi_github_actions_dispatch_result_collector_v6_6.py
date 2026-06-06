#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_dispatch_result_collector_v6_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, target: str | None = None) -> dict[str, Any]:
    value = {"qi_github_actions_dispatch_result_collector_enabled": True, "apply_github_actions_dispatch_result_collector": True, "runtime_root": str(root)}
    if target:
        value["dispatch_target"] = target
    return value


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_LICENSE_READY", "dispatch_packet_read_allowed": True, "dispatch_result_read_allowed": True, "raw_result_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_collect"] = True
    value.update(overrides)
    return value


def dispatch(target: str, result_file: str) -> dict[str, Any]:
    return {"dispatch_target": target, "connector_action": "GitHub." + target, "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS"}, "result_expected_file": result_file}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_external_call_raw_result_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], raw: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_READY", case
    assert out["raw_result_packet_written"] is True, case
    assert not out["blockers"], case
    assert raw["version"] == "qi_github_actions_external_call_raw_result_packet_from_dispatch_v6_6", case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        target = "commit_workflow_runs"
        files = {
            "qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch(target, "qi_github_actions_observation_connector_result_packet.json"),
            "qi_github_actions_dispatch_commit_workflow_runs_result.json": {"dispatch_result_allowed": True, "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]},
        }
        code, out, raw = run(root, "commit", files, lic(target))
        assert_ready("commit", code, out, raw)
        assert out["dispatch_target"] == target
        assert raw["dispatch_target"] == target

        target = "rerun_workflow_job"
        files = {
            "qi_github_actions_dispatch_rerun_workflow_job_packet.json": dispatch(target, "qi_github_actions_connector_result_packet.json"),
            "qi_github_actions_dispatch_rerun_workflow_job_result.json": {"dispatch_result_allowed": True, "success": True, "http_status": 201},
        }
        code, out, raw = run(root, "rerun", files, lic(target), target)
        assert_ready("rerun", code, out, raw)
        assert raw["dispatch_target"] == target

        target = "workflow_run_jobs"
        files = {"qi_github_actions_dispatch_workflow_run_jobs_packet.json": dispatch(target, "qi_github_actions_observation_connector_result_packet.json")}
        code, out, raw = run(root, "missing_result", files, lic(target), target)
        assert code == 1
        assert "dispatch_result_missing_or_invalid" in out["blockers"]
        assert raw == {}

        target = "commit_workflow_runs"
        files = {
            "qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch(target, "qi_github_actions_observation_connector_result_packet.json"),
            "qi_github_actions_dispatch_commit_workflow_runs_result.json": {"dispatch_result_allowed": False},
        }
        code, out, raw = run(root, "denied", files, lic(target), target)
        assert code == 1
        assert "dispatch_result_allowed_not_true" in out["blockers"]
        assert raw == {}

        code, out, raw = run(root, "license_block", files, lic(), target)
        assert code == 1
        assert "commit_workflow_runs_not_allowed_by_dispatch_result_collector_license" in out["blockers"]
        assert raw == {}
    print("qi_github_actions_dispatch_result_collector_v6_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

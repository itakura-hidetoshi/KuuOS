#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_observation_result_ingestor_v5_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_observation_result_ingestor_enabled": True, "apply_github_actions_observation_result_ingestor": True, "runtime_root": str(root)}


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_LICENSE_READY", "observation_request_read_allowed": True, "observation_result_read_allowed": True, "status_packet_write_allowed": True, "observation_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_observation"] = True
    value.update(overrides)
    return value


def request(kind: str) -> dict[str, Any]:
    return {"observation_kind": kind, "connector_action": "GitHub.fetch", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS"}}


def result(kind: str, **overrides: Any) -> dict[str, Any]:
    value = {"observation_result_allowed": True, "observation_kind": kind}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, req: dict[str, Any] | None, res: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if req is not None:
        dump(runtime / "qi_github_actions_observation_connector_request.json", req)
    if res is not None:
        dump(runtime / "qi_github_actions_observation_connector_result_packet.json", res)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_status_packet.json"), load_json(runtime / "qi_github_actions_observation_result_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        runs = [{"id": 1, "name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success", "run_number": 7, "workflow_id": 11}]
        code, out, status_packet, obs_packet = run(root, "runs", request("commit_workflow_runs"), result("commit_workflow_runs", workflow_runs=runs), lic("commit_workflow_runs"))
        assert_ready("runs", code, out)
        assert out["status_packet_emitted"] is True
        assert status_packet["github_actions_status_allowed"] is True
        assert status_packet["workflow_runs"][0]["name"] == "Qi Process Tensor Review Checks"
        assert obs_packet == {}

        jobs = [{"id": 22, "name": "runtime", "status": "completed", "conclusion": "success", "run_id": 33}]
        code, out, status_packet, obs_packet = run(root, "jobs", request("workflow_run_jobs"), result("workflow_run_jobs", jobs=jobs), lic("workflow_run_jobs"))
        assert_ready("jobs", code, out)
        assert out["observation_packet_emitted"] is True
        assert obs_packet["jobs"][0]["id"] == 22
        assert status_packet == {}

        code, out, status_packet, obs_packet = run(root, "empty_runs", request("commit_workflow_runs"), result("commit_workflow_runs", workflow_runs=[]), lic("commit_workflow_runs"))
        assert code == 1
        assert "workflow_runs_empty_or_invalid" in out["blockers"]

        code, out, status_packet, obs_packet = run(root, "mismatch", request("commit_workflow_runs"), result("workflow_run_jobs", jobs=[]), lic("commit_workflow_runs"))
        assert code == 1
        assert "observation_result_kind_mismatch" in out["blockers"]

        code, out, status_packet, obs_packet = run(root, "blocked_license", request("commit_workflow_runs"), result("commit_workflow_runs", workflow_runs=runs), lic())
        assert code == 1
        assert "commit_workflow_runs_not_allowed_by_observation_result_ingestor_license" in out["blockers"]

        code, out, status_packet, obs_packet = run(root, "missing", None, result("commit_workflow_runs", workflow_runs=runs), lic("commit_workflow_runs"))
        assert code == 1
        assert "observation_connector_request_missing_or_invalid" in out["blockers"]
    print("qi_github_actions_observation_result_ingestor_v5_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_status_reobserver_v5_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_status_reobserver_enabled": True, "apply_github_actions_status_reobserver": True, "runtime_root": str(root)}


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_LICENSE_READY", "reobserve_request_read_allowed": True, "observation_request_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if kind:
        value[f"allow_{kind}_observation"] = True
    value.update(overrides)
    return value


def packet(kind: str, **overrides: Any) -> dict[str, Any]:
    value = {"reobserve_allowed": True, "observation_kind": kind, "repo_full_name": "itakura-hidetoshi/KuuOS"}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, req: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if req is not None:
        dump(runtime / "qi_github_actions_status_reobserve_request.json", req)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_observation_connector_request.json")


def assert_ready(case: str, code: int, out: dict[str, Any], request: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_READY", case
    assert out["request_emitted"] is True, case
    assert not out["blockers"], case
    assert request["connector_action"].startswith("GitHub.fetch_"), case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, request = run(root, "commit", packet("commit_workflow_runs", commit_sha="abc123"), lic("commit_workflow_runs"))
        assert_ready("commit", code, out, request)
        assert request["connector_action"] == "GitHub.fetch_commit_workflow_runs"
        assert request["connector_payload"]["commit_sha"] == "abc123"

        code, out, request = run(root, "jobs", packet("workflow_run_jobs", run_id=123), lic("workflow_run_jobs"))
        assert_ready("jobs", code, out, request)
        assert request["connector_action"] == "GitHub.fetch_workflow_run_jobs"
        assert request["connector_payload"]["run_id"] == 123

        code, out, request = run(root, "steps", packet("workflow_job_steps", job_id=456), lic("workflow_job_steps"))
        assert_ready("steps", code, out, request)
        assert request["connector_action"] == "GitHub.fetch_workflow_job_steps"
        assert request["connector_payload"]["job_id"] == 456

        code, out, request = run(root, "bad_id", packet("workflow_run_jobs", run_id=0), lic("workflow_run_jobs"))
        assert code == 1
        assert "run_id_invalid" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "denied", packet("commit_workflow_runs", commit_sha="abc123", reobserve_allowed=False), lic("commit_workflow_runs"))
        assert code == 1
        assert "status_reobserve_request_allowed_not_true" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "blocked_license", packet("commit_workflow_runs", commit_sha="abc123"), lic())
        assert code == 1
        assert "commit_workflow_runs_not_allowed_by_status_reobserver_license" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "unknown", packet("unsupported_observation"), lic("unsupported_observation"))
        assert code == 1
        assert "observation_kind_not_allowlisted" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "missing", None, lic("commit_workflow_runs"))
        assert code == 1
        assert "status_reobserve_request_missing_or_invalid" in out["blockers"]
        assert request == {}
    print("qi_github_actions_status_reobserver_v5_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

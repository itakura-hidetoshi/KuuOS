#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_direct_executor_v5_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_direct_executor_enabled": True,
        "apply_github_actions_direct_executor": True,
        "runtime_root": str(root),
        "execution_mode": "connector_request",
    }


def lic(action: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_LICENSE_READY",
        "direct_execution_packet_read_allowed": True,
        "connector_execution_request_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if action:
        value[f"allow_{action}_action"] = True
    value.update(overrides)
    return value


def packet(action: str, **overrides: Any) -> dict[str, Any]:
    value = {
        "action": action,
        "direct_execution_allowed": True,
        "repo_full_name": "itakura-hidetoshi/KuuOS",
        "execution_mode": "connector_request",
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, direct_packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if direct_packet is not None:
        dump(runtime / "qi_github_actions_direct_execution_packet.json", direct_packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run(
        [sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_connector_execution_request.json")


def assert_ready(case: str, code: int, out: dict[str, Any], request: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_READY", case
    assert out["execution_request_emitted"] is True, case
    assert not out["blockers"], case
    assert request["direct_execution_supported"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, request = run(root, "rerun_failed", packet("rerun_failed_workflow_run_jobs", run_id=123), lic("rerun_failed_workflow_run_jobs"))
        assert_ready("rerun_failed", code, out, request)
        assert request["connector_action"] == "GitHub.rerun_failed_workflow_run_jobs"
        assert request["connector_payload"]["run_id"] == 123

        code, out, request = run(root, "rerun_job", packet("rerun_workflow_job", job_id=456), lic("rerun_workflow_job"))
        assert_ready("rerun_job", code, out, request)
        assert request["connector_action"] == "GitHub.rerun_workflow_job"
        assert request["connector_payload"]["job_id"] == 456

        code, out, request = run(root, "merge_pr", packet("merge_pull_request", pr_number=385, merge_method="merge", expected_head_sha="abc"), lic("merge_pull_request"))
        assert_ready("merge_pr", code, out, request)
        assert request["connector_action"] == "GitHub.merge_pull_request"
        assert request["connector_payload"]["pr_number"] == 385

        code, out, request = run(root, "dispatch", packet("workflow_dispatch", workflow_id_or_file="qi-process-tensor-review.yml", ref="main", inputs={}), lic("workflow_dispatch"))
        assert_ready("dispatch", code, out, request)
        assert request["connector_payload"]["workflow_id_or_file"] == "qi-process-tensor-review.yml"

        code, out, request = run(root, "denied", packet("rerun_failed_workflow_run_jobs", run_id=123, direct_execution_allowed=False), lic("rerun_failed_workflow_run_jobs"))
        assert code == 1
        assert "direct_execution_packet_allowed_not_true" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "license_block", packet("rerun_failed_workflow_run_jobs", run_id=123), lic())
        assert code == 1
        assert "rerun_failed_workflow_run_jobs_not_allowed_by_direct_executor_license" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "bad_run", packet("rerun_failed_workflow_run_jobs", run_id=0), lic("rerun_failed_workflow_run_jobs"))
        assert code == 1
        assert "run_id_invalid" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "unsupported", packet("unsupported_direct_action"), lic("unsupported_direct_action"))
        assert code == 1
        assert "direct_action_not_allowlisted" in out["blockers"]
        assert request == {}

        code, out, request = run(root, "missing", None, lic("rerun_failed_workflow_run_jobs"))
        assert code == 1
        assert "direct_execution_packet_missing_or_invalid" in out["blockers"]
        assert request == {}

        rows = read_rows(root / "rerun_failed" / "qi_github_actions_direct_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_READY"
    print("qi_github_actions_direct_executor_v5_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

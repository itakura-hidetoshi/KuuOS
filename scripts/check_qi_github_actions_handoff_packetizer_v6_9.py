#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_handoff_packetizer_v6_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_handoff_packetizer_enabled": True, "apply_github_actions_handoff_packetizer": True, "runtime_root": str(root)}


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_HANDOFF_PACKETIZER_LICENSE_READY", "dispatch_packet_read_allowed": True, "handoff_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_handoff"] = True
    value.update(overrides)
    return value


def dispatch(target: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"dispatch_target": target, "connector_action": "GitHub." + target, "connector_payload": payload, "result_expected_file": "result.json"}


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
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_handoff_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], handoff: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_HANDOFF_PACKETIZER_READY", case
    assert out["handoff_packet_emitted"] is True, case
    assert not out["blockers"], case
    assert handoff["boundary"]["operator_or_chatgpt_connector_executes_tool"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch("commit_workflow_runs", {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"})}
        code, out, handoff = run(root, "commit", files, lic("commit_workflow_runs"))
        assert_ready("commit", code, out, handoff)
        assert handoff["connector_tool"] == "GitHub.fetch_commit_workflow_runs"
        assert handoff["connector_tool_args"]["commit_sha"] == "abc"
        assert handoff["dispatch_result_file"] == "qi_github_actions_dispatch_commit_workflow_runs_result.json"

        files = {"qi_github_actions_dispatch_rerun_workflow_job_packet.json": dispatch("rerun_workflow_job", {"repo_full_name": "itakura-hidetoshi/KuuOS", "job_id": 123})}
        code, out, handoff = run(root, "job", files, lic("rerun_workflow_job"))
        assert_ready("job", code, out, handoff)
        assert handoff["connector_tool"] == "GitHub.rerun_workflow_job"
        assert handoff["connector_tool_args"]["job_id"] == 123

        files = {"qi_github_actions_dispatch_merge_pull_request_packet.json": dispatch("merge_pull_request", {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1, "merge_method": "merge"})}
        code, out, handoff = run(root, "merge", files, lic("merge_pull_request"))
        assert_ready("merge", code, out, handoff)
        assert handoff["connector_tool"] == "GitHub.merge_pull_request"
        assert handoff["connector_tool_args"]["pr_number"] == 1

        files = {"qi_github_actions_dispatch_workflow_run_jobs_packet.json": dispatch("workflow_run_jobs", {"repo_full_name": "itakura-hidetoshi/KuuOS"})}
        code, out, handoff = run(root, "bad_payload", files, lic("workflow_run_jobs"))
        assert code == 1
        assert "run_id_invalid" in out["blockers"]
        assert handoff == {}

        code, out, handoff = run(root, "license_block", {"qi_github_actions_dispatch_commit_workflow_runs_packet.json": dispatch("commit_workflow_runs", {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"})}, lic())
        assert code == 1
        assert "commit_workflow_runs_not_allowed_by_handoff_packetizer_license" in out["blockers"]
        assert handoff == {}

        code, out, handoff = run(root, "missing", {}, lic("commit_workflow_runs"))
        assert code == 1
        assert "dispatch_packet_missing_or_invalid" in out["blockers"]
        assert handoff == {}
    print("qi_github_actions_handoff_packetizer_v6_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

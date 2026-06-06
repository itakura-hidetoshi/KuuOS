#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_pr_live_external_result_bridge_v8_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_external_result_bridge_enabled": True, "apply_github_actions_pr_live_external_result_bridge": True, "runtime_root": str(root)}


def lic(target: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "dispatch_result_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if target:
        value[f"allow_{target}_result_bridge"] = True
    value.update(overrides)
    return value


def pr_call(**overrides: Any) -> dict[str, Any]:
    value = {"external_call_allowed": True, "dispatch_target": "pr_info", "connector_action": "GitHub.get_pr_info", "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "dispatch_result_expected_file": "qi_github_actions_pr_live_dispatch_pr_info_result.json"}
    value.update(overrides)
    return value


def runs_call(**overrides: Any) -> dict[str, Any]:
    value = {"external_call_allowed": True, "dispatch_target": "commit_workflow_runs", "connector_action": "GitHub.fetch_commit_workflow_runs", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}, "dispatch_result_expected_file": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json"}
    value.update(overrides)
    return value


def pr_raw(**overrides: Any) -> dict[str, Any]:
    value = {"number": 1, "state": "open", "draft": False, "merged": False, "head_sha": "abc", "repo_full_name": "itakura-hidetoshi/KuuOS"}
    value.update(overrides)
    return value


def runs_raw(conclusion: str | None = "success", status: str = "completed") -> dict[str, Any]:
    return {"workflow_runs": [{"id": 10, "name": "Qi Process Tensor Review Checks", "status": status, "conclusion": conclusion}], "required_workflows": ["Qi Process Tensor Review Checks"]}


def run(root: pathlib.Path, name: str, call: dict[str, Any] | None, raw: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if call is not None:
        dump(runtime / "qi_github_actions_pr_live_external_call_packet.json", call)
    if raw is not None:
        dump(runtime / "qi_github_actions_pr_live_external_call_raw_result_packet.json", raw)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_pr_live_dispatch_pr_info_result.json"), load_json(runtime / "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_READY", case
    assert out["dispatch_result_written"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, pr_result, runs_result = run(root, "pr", pr_call(), pr_raw(), lic("pr_info"))
        assert_ready("pr", code, out)
        assert out["dispatch_target"] == "pr_info"
        assert pr_result["dispatch_result_allowed"] is True
        assert pr_result["connector_result"]["head_sha"] == "abc"
        assert runs_result == {}

        nested_pr = {"connector_result": {"number": 1, "head": {"sha": "nestedabc"}, "repo_full_name": "itakura-hidetoshi/KuuOS"}}
        code, out, pr_result, runs_result = run(root, "nested_pr", pr_call(), nested_pr, lic("pr_info"))
        assert_ready("nested_pr", code, out)
        assert pr_result["connector_result"]["head"]["sha"] == "nestedabc"

        code, out, pr_result, runs_result = run(root, "runs", runs_call(), runs_raw("success"), lic("commit_workflow_runs"))
        assert_ready("runs", code, out)
        assert out["dispatch_target"] == "commit_workflow_runs"
        assert runs_result["dispatch_result_allowed"] is True
        assert runs_result["connector_result"]["workflow_runs"]

        code, out, pr_result, runs_result = run(root, "missing_head", pr_call(), {"number": 1, "repo_full_name": "itakura-hidetoshi/KuuOS"}, lic("pr_info"))
        assert code == 1
        assert "head_sha_missing" in out["blockers"]

        mismatch = pr_call(dispatch_result_expected_file="wrong.json")
        code, out, pr_result, runs_result = run(root, "expected_mismatch", mismatch, pr_raw(), lic("pr_info"))
        assert code == 1
        assert "dispatch_result_expected_file_mismatch" in out["blockers"]

        code, out, pr_result, runs_result = run(root, "license_block", pr_call(), pr_raw(), lic())
        assert code == 1
        assert "pr_info_not_allowed_by_external_result_bridge_license" in out["blockers"]
    print("qi_github_actions_pr_live_external_result_bridge_v8_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

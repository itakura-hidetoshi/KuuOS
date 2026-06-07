#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_aware_runner_v7_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_aware_runner_enabled": True, "apply_github_actions_policy_aware_runner": True, "runtime_root": str(root)}


def lic(mode: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_LICENSE_READY", "policy_packet_read_allowed": True, "integrated_runner_invoke_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if mode:
        value[f"allow_{mode}_mode"] = True
    value.update(overrides)
    return value


def policy(mode: str, hint: str | None = None, cycles: int = 2, steps: int = 2, hold: bool = False) -> dict[str, Any]:
    return {"version": "qi_github_actions_lifecycle_policy_packet_v7_1", "runner_mode": mode, "policy_hint": hint or mode, "max_bridge_cycles": cycles, "max_loop_steps_per_cycle": steps, "hold_required": hold}


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
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
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("hold", "hold_for_review", hold=True)}
        code, out = run(root, "hold", files, lic("hold"))
        assert_ready("hold", code, out)
        assert out["execution_class"] == "policy_hold"
        assert out["integrated_runner_invoked"] is False

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("continue", "stable_continue"), "qi_github_actions_status_packet.json": status_packet()}
        code, out = run(root, "continue", files, lic("continue"))
        assert_ready("continue", code, out)
        assert out["execution_class"] == "policy_runner_completed"
        assert out["integrated_runner_invoked"] is True
        assert out["integrated_runner_status"] == "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY"

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("observe", "observe_more"), "qi_github_actions_status_reobserve_request.json": {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}
        code, out = run(root, "observe", files, lic("observe"))
        assert_ready("observe", code, out)
        assert out["integrated_runner_invoked"] is True

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("retry", "retry_heavy"), "qi_github_actions_connector_execution_request.json": {"connector_action": "GitHub.connector_operation", "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS", "target_id": 1}}}
        code, out = run(root, "retry", files, lic("retry"))
        assert_ready("retry", code, out)
        assert out["integrated_runner_invoked"] is True

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("continue", "stable_continue", cycles=0)}
        code, out = run(root, "bad_limits", files, lic("continue"))
        assert code == 1
        assert "policy_runner_limits_invalid" in out["blockers"]

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("continue", "stable_continue", hold=True)}
        code, out = run(root, "bad_hold", files, lic("continue"))
        assert code == 1
        assert "hold_required_but_runner_mode_not_hold" in out["blockers"]

        code, out = run(root, "missing", {}, lic("continue"))
        assert code == 1
        assert "lifecycle_policy_packet_missing_or_invalid" in out["blockers"]

        files = {"qi_github_actions_lifecycle_policy_packet.json": policy("continue", "stable_continue")}
        code, out = run(root, "license_block", files, lic())
        assert code == 1
        assert "continue_mode_not_allowed_by_policy_aware_runner_license" in out["blockers"]
    print("qi_github_actions_policy_aware_runner_v7_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

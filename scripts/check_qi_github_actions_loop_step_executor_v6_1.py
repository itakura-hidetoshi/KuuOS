#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_loop_step_executor_v6_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_loop_step_executor_enabled": True, "apply_github_actions_loop_step_executor": True, "runtime_root": str(root)}


def lic(stage: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_LICENSE_READY", "loop_command_read_allowed": True, "local_step_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if stage:
        value[f"allow_{stage}_stage"] = True
    value.update(overrides)
    return value


def command(stage: str, cmd: str) -> dict[str, Any]:
    return {"selected_stage": stage, "next_command": cmd}


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


def assert_ready(case: str, code: int, out: dict[str, Any], stage: str, local: bool) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_READY", case
    assert out["selected_stage"] == stage, case
    assert out["local_step_performed"] is local, case


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "plan", {"qi_github_actions_loop_command_packet.json": command("plan_from_status", "run_qi_github_actions_capability_planner_v5_5"), "qi_github_actions_status_packet.json": status_packet()}, lic("plan_from_status"))
        assert_ready("plan", code, out, "plan_from_status", True)
        assert out["step_result_class"] == "local_stage_completed"
        assert (root / "plan" / "qi_executable_capability_recipe_batch_packet.json").is_file()

        code, out = run(root, "wait_op", {"qi_github_actions_loop_command_packet.json": command("await_connector_operation", "await_github_connector_operation")}, lic("await_connector_operation"))
        assert_ready("wait_op", code, out, "await_connector_operation", False)
        assert out["substage_status"] == "WAITING"

        reobserve = {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
        code, out = run(root, "reobserve", {"qi_github_actions_loop_command_packet.json": command("status_reobserve", "run_qi_github_actions_status_reobserver_v5_8"), "qi_github_actions_status_reobserve_request.json": reobserve}, lic("status_reobserve"))
        assert_ready("reobserve", code, out, "status_reobserve", True)
        assert (root / "reobserve" / "qi_github_actions_observation_connector_request.json").is_file()

        code, out = run(root, "missing", {}, lic("plan_from_status"))
        assert code == 1
        assert "loop_command_packet_missing_or_invalid" in out["blockers"]

        code, out = run(root, "license_block", {"qi_github_actions_loop_command_packet.json": command("plan_from_status", "run_qi_github_actions_capability_planner_v5_5")}, lic())
        assert code == 1
        assert "plan_from_status_not_allowed_by_loop_step_executor_license" in out["blockers"]
    print("qi_github_actions_loop_step_executor_v6_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

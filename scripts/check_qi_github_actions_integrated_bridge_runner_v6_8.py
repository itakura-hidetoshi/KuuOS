#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_integrated_bridge_runner_v6_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {"qi_github_actions_integrated_bridge_runner_enabled": True, "apply_github_actions_integrated_bridge_runner": True, "runtime_root": str(root), "max_bridge_cycles": 5, "max_loop_steps_per_cycle": 5}
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_LICENSE_READY", "internal_loop_run_allowed": True, "external_bridge_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY", case
    assert not out["blockers"], case
    assert out["cycles_run"] >= 1, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "from_status", {"qi_github_actions_status_packet.json": status_packet()}, lic())
        assert_ready("from_status", code, out)
        assert out["stop_reason"] == "max_steps_reached"
        assert out["cycle_records"][0]["internal_final_stage"] == "plan_from_status"
        assert (root / "from_status" / "qi_executable_capability_recipe_batch_packet.json").is_file()

        req = {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}
        code, out = run(root, "from_reobserve", {"qi_github_actions_status_reobserve_request.json": req}, lic())
        assert_ready("from_reobserve", code, out)
        assert out["stop_reason"] == "await_dispatch_result"
        assert out["final_external_stage"] == "await_dispatch_result"
        assert (root / "from_reobserve" / "qi_github_actions_dispatch_commit_workflow_runs_packet.json").is_file()

        code, out = run(root, "empty", {}, lic())
        assert_ready("empty", code, out)
        assert out["stop_reason"] in {"await_external_call", "max_bridge_cycles_reached", "waiting_for_external_observation"}

        code, out = run(root, "max_cycle", {"qi_github_actions_status_reobserve_request.json": req}, lic(), {"max_bridge_cycles": 1})
        assert_ready("max_cycle", code, out)
        assert out["cycles_run"] == 1

        code, out = run(root, "bad_cap", {}, lic(), {"max_bridge_cycles": 0})
        assert code == 1
        assert "max_bridge_cycles_invalid" in out["blockers"]

        code, out = run(root, "license_block", {}, lic(external_bridge_run_allowed=False))
        assert code == 1
        assert "external_bridge_run_not_allowed" in out["blockers"]
    print("qi_github_actions_integrated_bridge_runner_v6_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

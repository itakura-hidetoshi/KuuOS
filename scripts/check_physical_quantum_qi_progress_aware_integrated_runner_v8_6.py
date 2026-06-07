#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_progress_aware_integrated_runner_v8_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"physical_quantum_qi_progress_aware_integrated_runner_enabled": True, "apply_physical_quantum_qi_progress_aware_integrated_runner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_LICENSE_READY", "runner_packet_read_allowed": True, "delegated_runner_invoke_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def packet(mode: str, klass: str, cycles: int = 2, steps: int = 2, review: bool = False) -> dict[str, Any]:
    return {"version": "qi_progress_aware_runner_packet_v8_5_from_physical_quantum_qi", "physical_quantum_qi_motion_bias_used": True, "runner_mode": mode, "progress_class": klass, "progress_action": "advance_light", "max_bridge_cycles": cycles, "max_loop_steps_per_cycle": steps, "progress_required": True, "review_exit_required": review, "boundary": {"path_integral_candidate_weighting_preserved": True, "progress_obligation_preserved": True}}


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def run(root: pathlib.Path, name: str, runner_packet: dict[str, Any] | None, extra_files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if runner_packet is not None:
        dump(runtime / "qi_progress_aware_runner_packet.json", runner_packet)
    for file_name, payload in extra_files.items():
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
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        p = packet("hold", "hold_with_review_exit", review=True)
        code, out = run(root, "hold", p, {}, lic())
        assert_ready("hold", code, out)
        assert out["execution_class"] == "progress_hold_with_exit"
        assert out["delegated_runner_invoked"] is False

        p = packet("continue", "safe_progress_continue")
        code, out = run(root, "continue", p, {"qi_github_actions_status_packet.json": status_packet()}, lic())
        assert_ready("continue", code, out)
        assert out["execution_class"] == "progress_runner_completed"
        assert out["delegated_runner_invoked"] is True

        p = packet("observe", "observe_with_progress_obligation")
        code, out = run(root, "observe", p, {"qi_github_actions_status_reobserve_request.json": {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}, lic())
        assert_ready("observe", code, out)
        assert out["delegated_runner_status"] == "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY"

        code, out = run(root, "missing", None, {}, lic())
        assert code == 1
        assert "qi_progress_aware_runner_packet_missing_or_invalid" in out["blockers"]

        bad = packet("continue", "safe_progress_continue")
        bad["physical_quantum_qi_motion_bias_used"] = False
        code, out = run(root, "bad_origin", bad, {}, lic())
        assert code == 1
        assert "physical_quantum_qi_motion_bias_used_not_true" in out["blockers"]

        bad = packet("continue", "safe_progress_continue")
        bad["boundary"]["path_integral_candidate_weighting_preserved"] = False
        code, out = run(root, "bad_boundary", bad, {}, lic())
        assert code == 1
        assert "path_integral_candidate_weighting_boundary_invalid" in out["blockers"]

        code, out = run(root, "license_block", packet("continue", "safe_progress_continue"), {}, lic(delegated_runner_invoke_allowed=False))
        assert code == 1
        assert "delegated_runner_invoke_not_allowed" in out["blockers"]
    print("physical_quantum_qi_progress_aware_integrated_runner_v8_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

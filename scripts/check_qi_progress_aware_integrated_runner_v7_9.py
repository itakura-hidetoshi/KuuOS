#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_progress_aware_integrated_runner_v7_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_progress_aware_integrated_runner_enabled": True, "apply_qi_progress_aware_integrated_runner": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_LICENSE_READY", "runner_packet_read_allowed": True, "integrated_runner_invoke_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def runner_packet(mode: str, klass: str, cycles: int = 2, steps: int = 2, review: bool = False) -> dict[str, Any]:
    return {"version": "qi_progress_aware_runner_packet_v7_8", "runner_mode": mode, "progress_class": klass, "progress_action": "advance_light", "max_bridge_cycles": cycles, "max_loop_steps_per_cycle": steps, "progress_required": True, "review_exit_required": review, "boundary": {"progress_obligation_preserved": True}}


def status_packet() -> dict[str, Any]:
    return {"github_actions_status_allowed": True, "required_workflows": ["Qi Process Tensor Review Checks"], "workflow_runs": [{"name": "Qi Process Tensor Review Checks", "status": "completed", "conclusion": "success"}]}


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_progress_aware_runner_packet.json", packet)
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
    assert out["status"] == "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY", case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "hold", runner_packet("hold", "hold_with_review_exit", review=True), {}, lic())
        assert_ready("hold", code, out)
        assert out["execution_class"] == "progress_hold_with_exit"
        assert out["integrated_runner_invoked"] is False
        assert out["integrated_runner_status"] == "HELD_WITH_EXIT"

        code, out = run(root, "continue", runner_packet("continue", "safe_progress_continue"), {"qi_github_actions_status_packet.json": status_packet()}, lic())
        assert_ready("continue", code, out)
        assert out["execution_class"] == "progress_runner_completed"
        assert out["integrated_runner_invoked"] is True

        code, out = run(root, "observe", runner_packet("observe", "observe_with_progress_obligation"), {"qi_github_actions_status_reobserve_request.json": {"reobserve_allowed": True, "observation_kind": "commit_workflow_runs", "repo_full_name": "itakura-hidetoshi/KuuOS", "commit_sha": "abc"}}, lic())
        assert_ready("observe", code, out)
        assert out["integrated_runner_invoked"] is True

        code, out = run(root, "missing", None, {}, lic())
        assert code == 1
        assert "qi_progress_aware_runner_packet_missing_or_invalid" in out["blockers"]

        bad = runner_packet("continue", "safe_progress_continue", cycles=0)
        code, out = run(root, "bad_limits", bad, {}, lic())
        assert code == 1
        assert "runner_packet_limits_invalid" in out["blockers"]

        no_progress = runner_packet("continue", "safe_progress_continue")
        no_progress["progress_required"] = False
        code, out = run(root, "no_progress", no_progress, {}, lic())
        assert code == 1
        assert "progress_required_not_true" in out["blockers"]

        code, out = run(root, "license_block", runner_packet("continue", "safe_progress_continue"), {}, lic(integrated_runner_invoke_allowed=False))
        assert code == 1
        assert "integrated_runner_invoke_not_allowed" in out["blockers"]
    print("qi_progress_aware_integrated_runner_v7_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_motion_to_runner_adapter_v8_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"physical_quantum_qi_motion_to_runner_adapter_enabled": True, "apply_physical_quantum_qi_motion_to_runner_adapter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_MOTION_TO_RUNNER_ADAPTER_LICENSE_READY", "motion_bias_packet_read_allowed": True, "runner_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def motion(mode: str, action: str, cycles: int = 4, steps: int = 4, small: bool = False, review: bool = False) -> dict[str, Any]:
    return {
        "version": "physical_quantum_qi_motion_bias_packet_v8_4",
        "physical_quantum_qi_path_integral_used": True,
        "observe_only_bounded_motion_candidate": True,
        "dominant_path": "light_progress",
        "next_motion_bias": "stable_continue",
        "motion_mode": mode,
        "progress_action": action,
        "max_bridge_cycles": cycles,
        "max_loop_steps_per_cycle": steps,
        "small_probe_required": small,
        "review_exit_required": review,
        "path_weight_confidence": 0.55,
        "boundary": {"motion_bias_only": True, "does_not_authorize_execution": True},
    }


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_motion_bias_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_progress_aware_runner_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_MOTION_TO_RUNNER_ADAPTER_READY", case
    assert out["runner_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["physical_quantum_qi_motion_bias_used"] is True, case
    assert packet["boundary"]["progress_obligation_preserved"] is True, case
    assert packet["boundary"]["does_not_run_runner"] is True, case
    assert packet["boundary"]["path_integral_candidate_weighting_preserved"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("continue", motion("continue", "advance_light"), "safe_progress_continue", 4, 4),
            ("observe", motion("observe", "observe_then_replan", 9, 9, True), "observe_with_progress_obligation", 3, 3),
            ("retry", motion("retry", "rebalance_then_retry", 9, 9, True), "retry_with_rebalance_probe", 3, 3),
            ("hold", motion("hold", "hold_but_require_exit_condition", 8, 8, False, True), "hold_with_review_exit", 1, 1),
        ]
        for name, m, expected_class, expected_cycles, expected_steps in cases:
            code, out, packet = run(root, name, m, lic())
            assert_ready(name, code, out, packet)
            assert packet["runner_mode"] == m["motion_mode"], name
            assert packet["progress_class"] == expected_class, name
            assert packet["max_bridge_cycles"] == expected_cycles, name
            assert packet["max_loop_steps_per_cycle"] == expected_steps, name

        code, out, packet = run(root, "missing", None, lic())
        assert code == 1
        assert "physical_quantum_qi_motion_bias_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = motion("bad", "advance_light")
        code, out, packet = run(root, "bad_mode", bad, lic())
        assert code == 1
        assert "motion_mode_not_allowlisted" in out["blockers"]
        assert packet == {}

        bad_boundary = motion("continue", "advance_light")
        bad_boundary["observe_only_bounded_motion_candidate"] = False
        code, out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert code == 1
        assert "observe_only_bounded_motion_candidate_not_true" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", motion("continue", "advance_light"), lic(runner_packet_write_allowed=False))
        assert code == 1
        assert "runner_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("physical_quantum_qi_motion_to_runner_adapter_v8_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

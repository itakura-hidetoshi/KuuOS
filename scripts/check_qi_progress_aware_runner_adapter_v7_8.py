#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_progress_aware_runner_adapter_v7_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_progress_aware_runner_adapter_enabled": True, "apply_qi_progress_aware_runner_adapter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROGRESS_AWARE_RUNNER_ADAPTER_LICENSE_READY", "safety_packet_read_allowed": True, "runner_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def safety(progress_class: str, action: str, cycles: int = 4, steps: int = 4, small: bool = False, review: bool = False) -> dict[str, Any]:
    return {"version": "qi_progress_bearing_safety_packet_v7_7", "progress_required": True, "progress_class": progress_class, "progress_action": action, "suggested_max_bridge_cycles": cycles, "suggested_max_loop_steps_per_cycle": steps, "small_probe_required": small, "review_exit_required": review, "boundary": {"progress_bearing_safety": True}}


def run(root: pathlib.Path, name: str, s: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if s is not None:
        dump(runtime / "qi_progress_bearing_safety_packet.json", s)
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
    assert out["status"] == "QI_PROGRESS_AWARE_RUNNER_ADAPTER_READY", case
    assert out["runner_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["progress_obligation_preserved"] is True, case
    assert packet["progress_required"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "continue", safety("safe_progress_continue", "advance_light"), lic())
        assert_ready("continue", code, out, packet)
        assert packet["runner_mode"] == "continue"
        assert packet["max_bridge_cycles"] == 4

        code, out, packet = run(root, "observe", safety("observe_with_progress_obligation", "observe_then_replan", 8, 8, small=True), lic())
        assert_ready("observe", code, out, packet)
        assert packet["runner_mode"] == "observe"
        assert packet["max_bridge_cycles"] == 3
        assert packet["max_loop_steps_per_cycle"] == 3

        code, out, packet = run(root, "retry", safety("retry_with_rebalance_probe", "rebalance_then_retry", small=True), lic())
        assert_ready("retry", code, out, packet)
        assert packet["runner_mode"] == "retry"

        code, out, packet = run(root, "hold", safety("hold_with_review_exit", "hold_but_require_exit_condition", 5, 5, review=True), lic())
        assert_ready("hold", code, out, packet)
        assert packet["runner_mode"] == "hold"
        assert packet["max_bridge_cycles"] == 1
        assert packet["review_exit_required"] is True

        code, out, packet = run(root, "gap", safety("progress_gap_detected", "open_small_probe_or_review_exit", 9, 9, small=True), lic())
        assert_ready("gap", code, out, packet)
        assert packet["runner_mode"] == "observe"
        assert packet["small_probe_required"] is True

        code, out, packet = run(root, "missing", None, lic())
        assert code == 1
        assert "qi_progress_bearing_safety_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = safety("bad", "advance_light")
        code, out, packet = run(root, "bad_class", bad, lic())
        assert code == 1
        assert "progress_class_not_allowlisted" in out["blockers"]
        assert packet == {}

        no_progress = safety("safe_progress_continue", "advance_light")
        no_progress["progress_required"] = False
        code, out, packet = run(root, "no_progress", no_progress, lic())
        assert code == 1
        assert "progress_required_not_true" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", safety("safe_progress_continue", "advance_light"), lic(runner_packet_write_allowed=False))
        assert code == 1
        assert "runner_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_progress_aware_runner_adapter_v7_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

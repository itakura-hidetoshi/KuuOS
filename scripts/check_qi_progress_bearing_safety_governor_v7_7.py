#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_progress_bearing_safety_governor_v7_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_progress_bearing_safety_governor_enabled": True, "apply_qi_progress_bearing_safety_governor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROGRESS_BEARING_SAFETY_GOVERNOR_LICENSE_READY", "bias_packet_read_allowed": True, "current_policy_read_allowed": True, "policy_outcome_read_allowed": True, "safety_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def bias(mode: str, qi_state: str = "smooth_circulation") -> dict[str, Any]:
    return {"version": "qi_process_tensor_policy_bias_packet_v7_6", "runner_mode_bias": mode, "qi_state": qi_state, "next_policy_bias": {"continue": "stable_continue", "observe": "observe_more", "retry": "retry_heavy", "hold": "hold_for_review"}.get(mode, "observe_more"), "suggested_max_bridge_cycles": 4, "suggested_max_loop_steps_per_cycle": 4, "boundary": {"bias_only": True}}


def policy() -> dict[str, Any]:
    return {"version": "qi_github_actions_lifecycle_policy_packet_v7_1", "runner_mode": "continue", "policy_hint": "stable_continue", "max_bridge_cycles": 4, "max_loop_steps_per_cycle": 4, "hold_required": False}


def run(root: pathlib.Path, name: str, b: dict[str, Any] | None, p: dict[str, Any] | None, outcomes: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if b is not None:
        dump(runtime / "qi_process_tensor_policy_bias_packet.json", b)
    if p is not None:
        dump(runtime / "qi_github_actions_lifecycle_policy_packet.json", p)
    for row in outcomes:
        append_jsonl(runtime / "qi_github_actions_policy_outcome_ledger.jsonl", row)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_progress_bearing_safety_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROGRESS_BEARING_SAFETY_GOVERNOR_READY", case
    assert out["safety_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["safety_without_progress_is_not_sufficient"] is True, case
    assert packet["progress_required"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        completed = [{"outcome_class": "runner_completed"}]
        code, out, packet = run(root, "continue", bias("continue"), policy(), completed, lic())
        assert_ready("continue", code, out, packet)
        assert packet["progress_class"] == "safe_progress_continue"
        assert packet["progress_action"] == "advance_light"

        code, out, packet = run(root, "observe", bias("observe", "observation_deficiency"), policy(), completed, lic())
        assert_ready("observe", code, out, packet)
        assert packet["progress_class"] == "observe_with_progress_obligation"
        assert packet["small_probe_required"] is True

        code, out, packet = run(root, "retry", bias("retry", "retry_stagnation"), policy(), completed, lic())
        assert_ready("retry", code, out, packet)
        assert packet["progress_class"] == "retry_with_rebalance_probe"
        assert packet["progress_action"] == "rebalance_then_retry"

        code, out, packet = run(root, "hold", bias("hold", "review_constraint"), policy(), completed, lic())
        assert_ready("hold", code, out, packet)
        assert packet["progress_class"] == "hold_with_review_exit"
        assert packet["review_exit_required"] is True

        stagnant = [{"outcome_class": "held_by_policy"}, {"outcome_class": "blocked_or_not_run"}, {"outcome_class": "held_by_policy"}]
        code, out, packet = run(root, "gap", bias("hold", "review_constraint"), policy(), stagnant, lic())
        assert_ready("gap", code, out, packet)
        assert packet["progress_class"] == "progress_gap_detected"
        assert "recent_history_has_no_completed_progress" in packet["progress_reason_codes"]

        code, out, packet = run(root, "missing_bias", None, policy(), completed, lic())
        assert code == 1
        assert "qi_process_tensor_policy_bias_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = bias("bad")
        code, out, packet = run(root, "bad_mode", bad, policy(), completed, lic())
        assert code == 1
        assert "runner_mode_bias_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", bias("continue"), policy(), completed, lic(safety_packet_write_allowed=False))
        assert code == 1
        assert "safety_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_progress_bearing_safety_governor_v7_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

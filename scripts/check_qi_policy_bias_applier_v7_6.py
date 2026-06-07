#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_policy_bias_applier_v7_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_policy_bias_applier_enabled": True, "apply_qi_policy_bias_applier": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_POLICY_BIAS_APPLIER_LICENSE_READY", "coupling_packet_read_allowed": True, "current_policy_read_allowed": True, "bias_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def coupling(state: str, bias: str) -> dict[str, Any]:
    return {"version": "qi_process_tensor_policy_coupling_packet_v7_5", "qi_process_tensor_considered": True, "qi_state": state, "next_policy_bias": bias, "process_memory_depth": 5}


def policy(mode: str = "continue", hold: bool = False) -> dict[str, Any]:
    return {"version": "qi_github_actions_lifecycle_policy_packet_v7_1", "runner_mode": mode, "policy_hint": "stable_continue", "max_bridge_cycles": 4, "max_loop_steps_per_cycle": 4, "hold_required": hold}


def run(root: pathlib.Path, name: str, c: dict[str, Any] | None, p: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if c is not None:
        dump(runtime / "qi_process_tensor_policy_coupling_packet.json", c)
    if p is not None:
        dump(runtime / "qi_github_actions_lifecycle_policy_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_process_tensor_policy_bias_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_POLICY_BIAS_APPLIER_READY", case
    assert out["bias_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["does_not_overwrite_lifecycle_policy_packet"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "stable", coupling("smooth_circulation", "stable_continue"), policy(), lic())
        assert_ready("stable", code, out, packet)
        assert packet["runner_mode_bias"] == "continue"
        assert packet["suggested_max_bridge_cycles"] == 5

        code, out, packet = run(root, "observe", coupling("observation_deficiency", "observe_more"), policy(), lic())
        assert_ready("observe", code, out, packet)
        assert packet["runner_mode_bias"] == "observe"
        assert packet["suggested_max_loop_steps_per_cycle"] == 3

        code, out, packet = run(root, "retry", coupling("retry_stagnation", "retry_heavy"), policy(), lic())
        assert_ready("retry", code, out, packet)
        assert packet["runner_mode_bias"] == "retry"
        assert packet["suggested_max_bridge_cycles"] == 3

        code, out, packet = run(root, "hold", coupling("review_constraint", "hold_for_review"), policy("hold", True), lic())
        assert_ready("hold", code, out, packet)
        assert packet["runner_mode_bias"] == "hold"
        assert packet["hold_bias"] is True
        assert packet["suggested_max_bridge_cycles"] == 1

        code, out, packet = run(root, "bad_state", coupling("bad", "stable_continue"), policy(), lic())
        assert code == 1
        assert "qi_state_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing_coupling", None, policy(), lic())
        assert code == 1
        assert "qi_process_tensor_policy_coupling_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", coupling("smooth_circulation", "stable_continue"), policy(), lic(bias_packet_write_allowed=False))
        assert code == 1
        assert "bias_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_policy_bias_applier_v7_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

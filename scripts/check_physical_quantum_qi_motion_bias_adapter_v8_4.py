#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_motion_bias_adapter_v8_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"physical_quantum_qi_motion_bias_adapter_enabled": True, "apply_physical_quantum_qi_motion_bias_adapter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_MOTION_BIAS_ADAPTER_LICENSE_READY", "path_integral_packet_read_allowed": True, "motion_bias_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def path_packet(path: str, bias: str) -> dict[str, Any]:
    weights = {"stay_safely": 0.05, "light_progress": 0.2, "observe_probe": 0.25, "rebalance_retry": 0.25, "review_exit": 0.25}
    weights[path] = 0.55
    return {
        "version": "physical_quantum_qi_path_integral_packet_v8_3",
        "physical_quantum_qi_path_integral_considered": True,
        "qi_is_relational_field_not_substance": True,
        "observe_only_bounded_motion_candidate": True,
        "dominant_path": path,
        "stationary_path": path,
        "next_motion_bias": bias,
        "path_integral_action": 1.23,
        "path_amplitude_weights": weights,
        "boundary": {"path_integral_is_candidate_weighting_not_truth": True, "does_not_authorize_execution": True},
    }


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_path_integral_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "physical_quantum_qi_motion_bias_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_MOTION_BIAS_ADAPTER_READY", case
    assert out["motion_bias_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["observe_only_bounded_motion_candidate"] is True, case
    assert packet["boundary"]["motion_bias_only"] is True, case
    assert packet["boundary"]["does_not_run_runner"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("light", "light_progress", "stable_continue", "continue"),
            ("observe", "observe_probe", "observe_more", "observe"),
            ("retry", "rebalance_retry", "retry_heavy", "retry"),
            ("review", "review_exit", "hold_for_review", "hold"),
            ("stay", "stay_safely", "hold_for_review", "hold"),
        ]
        for name, path, bias, mode in cases:
            code, out, packet = run(root, name, path_packet(path, bias), lic())
            assert_ready(name, code, out, packet)
            assert packet["motion_mode"] == mode, name
            assert packet["dominant_path"] == path, name
            assert packet["next_motion_bias"] == bias, name

        code, out, packet = run(root, "missing", None, lic())
        assert code == 1
        assert "physical_quantum_qi_path_integral_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = path_packet("light_progress", "stable_continue")
        bad["observe_only_bounded_motion_candidate"] = False
        code, out, packet = run(root, "bad_boundary", bad, lic())
        assert code == 1
        assert "observe_only_bounded_motion_candidate_not_true" in out["blockers"]
        assert packet == {}

        bad_path = path_packet("light_progress", "stable_continue")
        bad_path["dominant_path"] = "bad_path"
        code, out, packet = run(root, "bad_path", bad_path, lic())
        assert code == 1
        assert "dominant_path_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", path_packet("light_progress", "stable_continue"), lic(motion_bias_packet_write_allowed=False))
        assert code == 1
        assert "motion_bias_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("physical_quantum_qi_motion_bias_adapter_v8_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

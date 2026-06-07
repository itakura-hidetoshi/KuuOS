#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_path_integral_governor_v8_3.py"


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
    return {"physical_quantum_qi_path_integral_governor_enabled": True, "apply_physical_quantum_qi_path_integral_governor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_GOVERNOR_LICENSE_READY", "suffering_integral_read_allowed": True, "qi_process_tensor_coupling_read_allowed": True, "progress_outcome_read_allowed": True, "path_integral_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def suffering(integral_class: str, stagnant: int = 3, transient: int = 0, net: int = 3) -> dict[str, Any]:
    return {"version": "qi_suffering_integral_packet_v8_2", "suffering_integral_considered": True, "suffering_integral_class": integral_class, "stagnant_safety_burden": stagnant, "transient_progress_pain": transient, "net_suffering_integral_proxy": net}


def coupling(qi_state: str) -> dict[str, Any]:
    return {"version": "qi_process_tensor_policy_coupling_packet_v7_5", "qi_process_tensor_considered": True, "qi_state": qi_state, "next_policy_bias": "observe_more"}


def outcome(value: str) -> dict[str, Any]:
    return {"record_type": "progress_outcome", "progress_outcome_class": value, "record_digest": value}


def run(root: pathlib.Path, name: str, s: dict[str, Any] | None, c: dict[str, Any] | None, outcomes: list[str], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if s is not None:
        dump(runtime / "qi_suffering_integral_packet.json", s)
    if c is not None:
        dump(runtime / "qi_process_tensor_policy_coupling_packet.json", c)
    for item in outcomes:
        append_jsonl(runtime / "qi_progress_outcome_ledger.jsonl", outcome(item))
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "physical_quantum_qi_path_integral_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_GOVERNOR_READY", case
    assert out["path_integral_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["physical_quantum_qi_path_integral_considered"] is True, case
    assert packet["observe_only_bounded_motion_candidate"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["path_integral_is_candidate_weighting_not_truth"] is True, case
    assert abs(sum(packet["path_amplitude_weights"].values()) - 1.0) < 0.00001, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "stay_dominates", suffering("staying_suffering_dominates", 8, 0, 8), coupling("smooth_circulation"), ["exit_preserved_hold"], lic())
        assert_ready("stay_dominates", code, out, packet)
        assert packet["dominant_path"] == "light_progress"
        assert packet["next_motion_bias"] == "stable_continue"

        code, out, packet = run(root, "hold_exit", suffering("hold_requires_exit", 5, 0, 5), coupling("review_constraint"), ["exit_preserved_hold", "exit_preserved_hold"], lic())
        assert_ready("hold_exit", code, out, packet)
        assert packet["dominant_path"] == "review_exit"
        assert packet["next_motion_bias"] == "hold_for_review"

        code, out, packet = run(root, "rebalance", suffering("rebalance_required", 4, 1, 4), coupling("retry_stagnation"), ["progress_blocked", "progress_blocked"], lic())
        assert_ready("rebalance", code, out, packet)
        assert packet["dominant_path"] == "rebalance_retry"
        assert packet["next_motion_bias"] == "retry_heavy"

        code, out, packet = run(root, "observe", suffering("progress_pain_acceptable", 2, 1, 2), coupling("observation_deficiency"), ["gap_probe_completed"], lic())
        assert_ready("observe", code, out, packet)
        assert packet["dominant_path"] == "observe_probe"
        assert packet["next_motion_bias"] == "observe_more"

        code, out, packet = run(root, "missing_suffering", None, coupling("smooth_circulation"), ["progress_completed"], lic())
        assert code == 1
        assert "qi_suffering_integral_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad_s = suffering("integral_relief_observed")
        bad_s["suffering_integral_considered"] = False
        code, out, packet = run(root, "bad_suffering", bad_s, coupling("smooth_circulation"), ["progress_completed"], lic())
        assert code == 1
        assert "suffering_integral_considered_not_true" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", suffering("integral_relief_observed"), coupling("smooth_circulation"), ["progress_completed"], lic(path_integral_packet_write_allowed=False))
        assert code == 1
        assert "path_integral_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("physical_quantum_qi_path_integral_governor_v8_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

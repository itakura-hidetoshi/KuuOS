#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_suffering_integral_governor_v8_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, window: int = 6) -> dict[str, Any]:
    return {"qi_suffering_integral_governor_enabled": True, "apply_qi_suffering_integral_governor": True, "runtime_root": str(root), "integral_window_records": window}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_SUFFERING_INTEGRAL_GOVERNOR_LICENSE_READY", "suffering_packet_read_allowed": True, "progress_outcome_ledger_read_allowed": True, "integral_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def suffering(pressure: str) -> dict[str, Any]:
    return {"version": "qi_stagnant_safety_suffering_packet_v8_1", "suffering_pressure_considered": True, "suffering_pressure_class": pressure, "recommended_relief_action": "open_small_probe"}


def outcome(value: str) -> dict[str, Any]:
    return {"record_type": "progress_outcome", "progress_outcome_class": value, "record_digest": value}


def run(root: pathlib.Path, name: str, pressure: str | None, outcomes: list[str], license_packet: dict[str, Any], window: int = 6) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if pressure is not None:
        dump(runtime / "qi_stagnant_safety_suffering_packet.json", suffering(pressure))
    for item in outcomes:
        append_jsonl(runtime / "qi_progress_outcome_ledger.jsonl", outcome(item))
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, window))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_suffering_integral_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_SUFFERING_INTEGRAL_GOVERNOR_READY", case
    assert out["integral_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["staying_can_increase_total_suffering"] is True, case
    assert packet["boundary"]["does_not_equate_short_term_pain_with_total_harm"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "relief", "suffering_pressure_relieved", ["progress_completed"], lic())
        assert_ready("relief", code, out, packet)
        assert packet["suffering_integral_class"] == "integral_relief_observed"
        assert packet["recommended_integral_action"] == "continue_light_progress"

        code, out, packet = run(root, "staying", "suffering_pressure_high", ["exit_preserved_hold", "progress_not_run"], lic())
        assert_ready("staying", code, out, packet)
        assert packet["suffering_integral_class"] == "staying_suffering_dominates"
        assert packet["recommended_integral_action"] == "accept_small_progress_pain"
        assert "staying_suffering_exceeds_transient_progress_pain" in packet["integral_reason_codes"]

        code, out, packet = run(root, "hold_exit", "suffering_pressure_moderate", ["exit_preserved_hold", "exit_preserved_hold"], lic())
        assert_ready("hold_exit", code, out, packet)
        assert packet["suffering_integral_class"] == "hold_requires_exit"

        code, out, packet = run(root, "rebalance", "suffering_pressure_low", ["progress_blocked", "progress_blocked"], lic())
        assert_ready("rebalance", code, out, packet)
        assert packet["suffering_integral_class"] == "rebalance_required"

        code, out, packet = run(root, "acceptable", "suffering_pressure_low", ["gap_probe_completed", "progress_not_run"], lic())
        assert_ready("acceptable", code, out, packet)
        assert packet["suffering_integral_class"] in {"progress_pain_acceptable", "integral_relief_observed"}

        code, out, packet = run(root, "missing_suffering", None, ["progress_completed"], lic())
        assert code == 1
        assert "qi_stagnant_safety_suffering_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_window", "suffering_pressure_low", ["progress_completed"], lic(), 0)
        assert code == 1
        assert "integral_window_records_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", "suffering_pressure_low", ["progress_completed"], lic(integral_packet_write_allowed=False))
        assert code == 1
        assert "integral_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_suffering_integral_governor_v8_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

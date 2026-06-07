#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_stagnant_safety_suffering_assessor_v8_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, window: int = 5) -> dict[str, Any]:
    return {"qi_stagnant_safety_suffering_assessor_enabled": True, "apply_qi_stagnant_safety_suffering_assessor": True, "runtime_root": str(root), "suffering_window_records": window}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_STAGNANT_SAFETY_SUFFERING_ASSESSOR_LICENSE_READY", "progress_outcome_ledger_read_allowed": True, "safety_packet_read_allowed": True, "suffering_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def safety(progress_required: bool = True) -> dict[str, Any]:
    return {"version": "qi_progress_bearing_safety_packet_v7_7", "progress_required": progress_required, "progress_class": "hold_with_review_exit", "progress_action": "hold_but_require_exit_condition"}


def outcome(value: str) -> dict[str, Any]:
    return {"record_type": "progress_outcome", "progress_outcome_class": value, "record_digest": value}


def run(root: pathlib.Path, name: str, outcomes: list[str], safety_packet: dict[str, Any] | None, license_packet: dict[str, Any], window: int = 5) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if safety_packet is not None:
        dump(runtime / "qi_progress_bearing_safety_packet.json", safety_packet)
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
    return done.returncode, load_json(op), load_json(runtime / "qi_stagnant_safety_suffering_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_STAGNANT_SAFETY_SUFFERING_ASSESSOR_READY", case
    assert out["suffering_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["safety_without_progress_increases_suffering"] is True, case
    assert packet["boundary"]["stagnant_safety_not_equivalent_to_relief"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "relieved", ["progress_completed", "gap_probe_completed"], safety(), lic())
        assert_ready("relieved", code, out, packet)
        assert packet["suffering_pressure_class"] == "suffering_pressure_relieved"
        assert packet["recommended_relief_action"] == "continue_light_progress"

        code, out, packet = run(root, "moderate", ["exit_preserved_hold", "progress_blocked"], safety(), lic())
        assert_ready("moderate", code, out, packet)
        assert packet["suffering_pressure_class"] == "suffering_pressure_moderate"
        assert packet["recommended_relief_action"] == "open_small_probe"

        code, out, packet = run(root, "high", ["exit_preserved_hold", "progress_blocked", "progress_not_run", "exit_preserved_hold"], safety(), lic())
        assert_ready("high", code, out, packet)
        assert packet["suffering_pressure_class"] == "suffering_pressure_high"
        assert packet["recommended_relief_action"] == "force_review_exit_or_small_probe"
        assert "repeated_safety_without_progress" in packet["suffering_reason_codes"]

        code, out, packet = run(root, "empty_ledger", [], safety(), lic())
        assert_ready("empty_ledger", code, out, packet)
        assert packet["suffering_pressure_class"] == "suffering_pressure_moderate"
        assert "progress_outcome_ledger_empty_or_missing" in out["warnings"]

        code, out, packet = run(root, "missing_safety", ["progress_completed"], None, lic())
        assert code == 1
        assert "qi_progress_bearing_safety_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "no_progress_required", ["progress_completed"], safety(False), lic())
        assert code == 1
        assert "progress_required_not_true" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_window", ["progress_completed"], safety(), lic(), 0)
        assert code == 1
        assert "suffering_window_records_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", ["progress_completed"], safety(), lic(suffering_packet_write_allowed=False))
        assert code == 1
        assert "suffering_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_stagnant_safety_suffering_assessor_v8_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

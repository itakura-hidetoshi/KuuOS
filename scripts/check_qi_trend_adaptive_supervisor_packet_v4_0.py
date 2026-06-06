#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_trend_adaptive_supervisor_packet_v4_0.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {
        "qi_trend_adaptive_supervisor_packet_enabled": True,
        "apply_trend_adaptive_supervisor_packet": True,
        "runtime_root": str(root),
        "base_max_supervised_cycles": 3,
        "base_max_trajectory_records": 50,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_LICENSE_READY",
        "trend_summary_read_allowed": True,
        "trend_receipt_read_allowed": True,
        "next_supervisor_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def summary(trend_class: str, recommendation: str, reliability: float, records_used: int = 4, trajectory_length: int = 8) -> dict[str, Any]:
    return {
        "trend_class": trend_class,
        "recommendation": recommendation,
        "reliability_score": reliability,
        "records_used": records_used,
        "trajectory_length": trajectory_length,
    }


def run(root: pathlib.Path, name: str, s: dict[str, Any] | None, r: dict[str, Any] | None, l: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if s is not None:
        dump(runtime / "qi_process_tensor_cycle_trend_summary.json", s)
    if r is not None:
        dump(runtime / "qi_process_tensor_cycle_trend_summary_receipt.json", r)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
    dump(lp, l)
    done = subprocess.run(
        [sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "next_qi_process_tensor_cycle_supervisor_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["suggested_packet_only"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "lighten", summary("stable_converging_trend", "lighten_next_supervision", 0.90), None, lic())
        assert_ready("lighten", code, out, packet)
        assert out["adaptation_class"] == "lighten_supervision_packet"
        assert out["max_supervised_cycles"] == 2
        assert packet["supervisor_context"]["max_supervised_cycles"] == 2

        code, out, packet = run(root, "rebalance", summary("no_progress_trend", "rebalance_next_supervision", 0.45), None, lic())
        assert_ready("rebalance", code, out, packet)
        assert out["adaptation_class"] == "rebalance_supervision_packet"
        assert out["max_supervised_cycles"] == 4
        assert out["max_trajectory_records"] == 55

        code, out, packet = run(root, "hold", summary("hold_dominant_trend", "review_hold_condition", 0.40), None, lic())
        assert_ready("hold", code, out, packet)
        assert out["adaptation_class"] == "hold_review_supervision_packet"
        assert out["max_supervised_cycles"] == 4

        code, out, packet = run(root, "blocked", summary("blocked_dominant_trend", "repair_blocked_path", 0.20), None, lic())
        assert_ready("blocked", code, out, packet)
        assert out["adaptation_class"] == "blocked_repair_supervision_packet"
        assert out["max_supervised_cycles"] == 5

        code, out, packet = run(root, "observe", summary("insufficient_history_trend", "observe_more_history", 0.0, records_used=0, trajectory_length=0), None, lic())
        assert_ready("observe", code, out, packet)
        assert out["adaptation_class"] == "observe_more_supervision_packet"
        assert "records_used_zero_or_missing" in out["warnings"]

        code, out, packet = run(root, "receipt_only", None, summary("bounded_working_trend", "continue_current_supervision", 0.60), lic())
        assert_ready("receipt_only", code, out, packet)
        assert out["adaptation_class"] == "continue_supervision_packet"

        code, out, packet = run(root, "missing", None, None, lic())
        assert code == 1
        assert out["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_BLOCKED"
        assert "trend_summary_missing" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "blocked_license", summary("stable_converging_trend", "lighten_next_supervision", 0.90), None, lic(next_supervisor_packet_write_allowed=False))
        assert code == 1
        assert "next_supervisor_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

        rows = read_rows(root / "lighten" / "qi_trend_adaptive_supervisor_packet_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_READY"
    print("qi_trend_adaptive_supervisor_packet_v4_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

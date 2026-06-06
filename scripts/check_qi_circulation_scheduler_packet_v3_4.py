#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_scheduler_packet_v3_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_circulation_scheduler_packet_enabled": True,
        "apply_circulation_scheduler_packet": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_CIRCULATION_SCHEDULER_PACKET_LICENSE_READY",
        "next_scheduler_packet_read_allowed": True,
        "scheduled_closed_loop_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "next_qi_circulation_scheduler_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
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
    return done.returncode, load_json(op), load_json(runtime / "qi_scheduled_closed_loop_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_CIRCULATION_SCHEDULER_PACKET_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        stable = {
            "initial_qi_packet": {"qi_flow": 0.86, "friction": 0.08},
            "route_base": {"segment": "upper-middle-lower"},
            "objective_hint": "maintain",
            "max_cycles_delta": -1,
            "convergence_threshold_delta": -0.005,
            "trajectory_adapted": True,
            "adapted_epoch": 123,
        }
        code, out, scheduled = run(root, "stable", stable, lic())
        assert_ready("stable", code, out)
        assert out["handoff_class"] == "stable_lighten_handoff"
        assert scheduled["initial_qi_packet"]["qi_flow"] == 0.86
        assert scheduled["scheduler_handoff"]["source"] == "next_qi_circulation_scheduler_packet"
        assert scheduled["scheduler_handoff"]["trajectory_adapted"] is True

        reopen = {
            "initial_qi_packet": {"qi_flow": 0.42, "friction": 0.41},
            "route_base": {"segment": "stagnation"},
            "objective_hint": "reopen",
            "max_cycles_delta": 2,
            "convergence_threshold_delta": 0.02,
            "trajectory_adapted": True,
        }
        code, out, scheduled = run(root, "reopen", reopen, lic())
        assert_ready("reopen", code, out)
        assert out["handoff_class"] == "reopen_handoff"
        assert scheduled["scheduler_handoff"]["objective_hint"] == "reopen"

        rebalance = {
            "initial_qi_packet": {"qi_flow": 0.61},
            "route_base": {},
            "objective_hint": "rebalance",
            "max_cycles_delta": 1,
            "convergence_threshold_delta": 0.01,
            "trajectory_adapted": True,
        }
        code, out, _ = run(root, "rebalance", rebalance, lic())
        assert_ready("rebalance", code, out)
        assert out["handoff_class"] == "rebalance_handoff"

        code, out, scheduled = run(root, "blocked", stable, lic(scheduled_closed_loop_packet_write_allowed=False))
        assert code == 1
        assert out["status"] == "QI_CIRCULATION_SCHEDULER_PACKET_BLOCKED"
        assert "scheduled_closed_loop_packet_write_not_allowed" in out["blockers"]
        assert scheduled == {}

        missing_runtime = root / "missing"
        cp = root / "missing_ctx.json"
        lp = root / "missing_lic.json"
        op = root / "missing_out.json"
        dump(cp, ctx(missing_runtime))
        dump(lp, lic())
        done = subprocess.run(
            [sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        out = load_json(op)
        assert done.returncode == 1
        assert "next_scheduler_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "stable" / "qi_circulation_scheduler_packet_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_CIRCULATION_SCHEDULER_PACKET_READY"
    print("qi_circulation_scheduler_packet_v3_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

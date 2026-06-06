#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_dispatcher_v4_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_executable_action_dispatcher_enabled": True,
        "apply_executable_action_dispatcher": True,
        "runtime_root": str(root),
    }


def lic(action: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_DISPATCHER_LICENSE_READY",
        "action_packet_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if action:
        value[f"allow_{action}_action"] = True
    value.update(overrides)
    return value


def action_packet(action: str, **overrides: Any) -> dict[str, Any]:
    value = {"action": action, "action_allowed": True, "action_context_patch": {}}
    value.update(overrides)
    return value


def supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def trend_summary(root: pathlib.Path) -> None:
    dump(root / "qi_process_tensor_cycle_trend_summary.json", {"trend_class": "stable_converging_trend", "recommendation": "lighten_next_supervision", "reliability_score": 0.9, "records_used": 2, "trajectory_length": 4})


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_action_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
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
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_ACTION_DISPATCHER_READY", case
    assert out["action_performed"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        supervisor_history(root / "trend")
        code, out = run(root, "trend", action_packet("cycle_trend_summary"), lic("cycle_trend_summary"))
        assert_ready("trend", code, out)
        assert out["action"] == "cycle_trend_summary"
        assert out["delegated_status"] == "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_READY"
        assert (root / "trend" / "qi_process_tensor_cycle_trend_summary.json").is_file()

        trend_summary(root / "packet")
        code, out = run(root, "packet", action_packet("trend_adaptive_supervisor_packet"), lic("trend_adaptive_supervisor_packet"))
        assert_ready("packet", code, out)
        assert out["delegated_status"] == "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_READY"
        assert (root / "packet" / "next_qi_process_tensor_cycle_supervisor_packet.json").is_file()

        code, out = run(root, "unknown", action_packet("shell"), lic("shell"))
        assert code == 1
        assert "action_not_allowlisted" in out["blockers"]
        assert out["action_performed"] is False

        code, out = run(root, "packet_blocked_by_license", action_packet("cycle_trend_summary"), lic())
        assert code == 1
        assert "cycle_trend_summary_not_allowed_by_dispatcher_license" in out["blockers"]

        code, out = run(root, "packet_denies", action_packet("cycle_trend_summary", action_allowed=False), lic("cycle_trend_summary"))
        assert code == 1
        assert "action_packet_action_allowed_not_true" in out["blockers"]

        code, out = run(root, "missing", None, lic("cycle_trend_summary"))
        assert code == 1
        assert "action_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "trend" / "qi_executable_action_dispatcher_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_DISPATCHER_READY"
    print("qi_executable_action_dispatcher_v4_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

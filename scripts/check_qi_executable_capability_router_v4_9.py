#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_router_v4_9.py"


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


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {
        "qi_executable_capability_router_enabled": True,
        "apply_executable_capability_router": True,
        "runtime_root": str(root),
    }
    value.update(overrides)
    return value


def lic(kind: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_ROUTER_LICENSE_READY",
        "capability_packet_read_allowed": True,
        "delegated_packet_write_allowed": True,
        "delegated_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if kind:
        value[f"allow_{kind}_capability"] = True
    value.update(overrides)
    return value


def seed_supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def cap_packet(kind: str, delegated: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {"capability_kind": kind, "capability_allowed": True, "delegated_input_packet": delegated, "runtime_context_patch": {}}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_capability_packet.json", packet)
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
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_ROUTER_READY", case
    assert out["delegated_performed"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        seed_supervisor_history(root / "action")
        code, out = run(root, "action", cap_packet("action_dispatch", {"action": "cycle_trend_summary", "action_allowed": True}), lic("action_dispatch"))
        assert_ready("action", code, out)
        assert out["capability_kind"] == "action_dispatch"
        assert out["delegated_status"] == "QI_EXECUTABLE_ACTION_DISPATCHER_READY"
        assert (root / "action" / "qi_executable_action_packet.json").is_file()

        seed_supervisor_history(root / "batch_recipe")
        code, out = run(root, "batch_recipe", cap_packet("batch_recipe_execute", {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}), lic("batch_recipe_execute"))
        assert_ready("batch_recipe", code, out)
        assert out["delegated_status"] == "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_READY"
        assert (root / "batch_recipe" / "qi_executable_action_recipe_batch_packet.json").is_file()

        code, out = run(root, "unknown", cap_packet("shell", {"cmd": "echo no"}), lic("shell"))
        assert code == 1
        assert "capability_kind_not_allowlisted" in out["blockers"]
        assert out["delegated_performed"] is False

        code, out = run(root, "denied", cap_packet("action_dispatch", {"action": "cycle_trend_summary", "action_allowed": True}, capability_allowed=False), lic("action_dispatch"))
        assert code == 1
        assert "capability_packet_allowed_not_true" in out["blockers"]

        code, out = run(root, "license_block", cap_packet("action_dispatch", {"action": "cycle_trend_summary", "action_allowed": True}), lic())
        assert code == 1
        assert "action_dispatch_not_allowed_by_router_license" in out["blockers"]

        code, out = run(root, "missing_input", cap_packet("action_dispatch", {}), lic("action_dispatch"))
        assert code == 1
        assert "delegated_input_packet_missing_or_invalid" in out["blockers"]

        code, out = run(root, "missing", None, lic("action_dispatch"))
        assert code == 1
        assert "capability_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "action" / "qi_executable_capability_router_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_ROUTER_READY"
    print("qi_executable_capability_router_v4_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

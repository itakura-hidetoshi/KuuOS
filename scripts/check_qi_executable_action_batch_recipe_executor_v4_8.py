#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_batch_recipe_executor_v4_8.py"


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
        "qi_executable_action_batch_recipe_executor_enabled": True,
        "apply_executable_action_batch_recipe_executor": True,
        "runtime_root": str(root),
        "max_compiled_batch_recipes": 5,
        "max_batch_recipes": 5,
        "max_compiled_actions": 5,
        "max_sequence_actions": 5,
    }
    value.update(overrides)
    return value


def lic(batch_recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_LICENSE_READY",
        "batch_compiler_packet_read_allowed": True,
        "batch_compiler_run_allowed": True,
        "batch_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if batch_recipe:
        value[f"allow_{batch_recipe}_batch_recipe"] = True
    value.update(overrides)
    return value


def seed_supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def compiler_packet(batch_recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"batch_recipe": batch_recipe, "batch_recipe_allowed": True, "max_compiled_batch_recipes": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_action_recipe_batch_compiler_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
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
    return done.returncode, load_json(op), load_json(runtime / "qi_executable_action_recipe_batch_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], batch: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_READY", case
    assert out["executor_completed"] is True, case
    assert out["compile_status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY", case
    assert out["batch_status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY", case
    assert out["recipes_run"] == out["batch_length"], case
    assert batch["boundary"]["requires_v4_6_batch_executor"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        seed_supervisor_history(root / "observe_twice")
        code, out, batch = run(root, "observe_twice", compiler_packet("observe_adapt_twice"), lic("observe_adapt_twice"))
        assert_ready("observe_twice", code, out, batch)
        assert out["batch_recipe"] == "observe_adapt_twice"
        assert out["batch_length"] == 2
        assert out["recipes_run"] == 2

        seed_supervisor_history(root / "compile_cap")
        code, out, batch = run(root, "compile_cap", compiler_packet("observe_supervise_adapt"), lic("observe_supervise_adapt"), {"max_compiled_batch_recipes": 2})
        assert code == 1
        assert out["status"] == "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_BLOCKED"
        assert "batch_recipe_compiler_not_ready" in out["blockers"]
        assert out["batch_status"] == "NOT_RUN"

        seed_supervisor_history(root / "batch_cap")
        code, out, batch = run(root, "batch_cap", compiler_packet("observe_supervise_adapt"), lic("observe_supervise_adapt"), {"max_batch_recipes": 2})
        assert code == 1
        assert "recipe_batch_executor_not_ready" in out["blockers"]
        assert out["compile_status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY"

        seed_supervisor_history(root / "denied")
        code, out, _ = run(root, "denied", compiler_packet("observe_adapt_twice", batch_recipe_allowed=False), lic("observe_adapt_twice"))
        assert code == 1
        assert "batch_recipe_packet_allowed_not_true" in out["blockers"]

        seed_supervisor_history(root / "unknown")
        code, out, _ = run(root, "unknown", compiler_packet("arbitrary_batch"), lic("arbitrary_batch"))
        assert code == 1
        assert "batch_recipe_not_allowlisted" in out["blockers"]

        seed_supervisor_history(root / "license_block")
        code, out, _ = run(root, "license_block", compiler_packet("observe_adapt_twice"), lic())
        assert code == 1
        assert "observe_adapt_twice_not_allowed_by_batch_recipe_executor_license" in out["blockers"]

        code, out, _ = run(root, "missing", None, lic("observe_adapt_twice"))
        assert code == 1
        assert "batch_compiler_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "observe_twice" / "qi_executable_action_batch_recipe_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_BATCH_RECIPE_EXECUTOR_READY"
    print("qi_executable_action_batch_recipe_executor_v4_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

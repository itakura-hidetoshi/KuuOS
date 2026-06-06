#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_recipe_executor_v4_5.py"


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
        "qi_executable_action_recipe_executor_enabled": True,
        "apply_executable_action_recipe_executor": True,
        "runtime_root": str(root),
        "max_compiled_actions": 5,
        "max_sequence_actions": 5,
    }
    value.update(overrides)
    return value


def lic(recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_LICENSE_READY",
        "recipe_packet_read_allowed": True,
        "compiler_run_allowed": True,
        "sequence_runner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if recipe:
        value[f"allow_{recipe}_recipe"] = True
    value.update(overrides)
    return value


def seed_supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def recipe_packet(recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"recipe": recipe, "recipe_allowed": True, "max_compiled_actions": 5, "max_sequence_actions": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_action_recipe_packet.json", packet)
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
    return done.returncode, load_json(op), load_json(runtime / "qi_executable_action_sequence_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], sequence: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_READY", case
    assert out["executor_completed"] is True, case
    assert out["compile_status"] == "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY", case
    assert out["sequence_status"] == "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_READY", case
    assert out["actions_run"] == out["sequence_length"], case
    assert sequence["boundary"]["requires_v4_3_sequence_runner"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        seed_supervisor_history(root / "observe")
        code, out, sequence = run(root, "observe", recipe_packet("observe_and_adapt"), lic("observe_and_adapt"))
        assert_ready("observe", code, out, sequence)
        assert out["recipe"] == "observe_and_adapt"
        assert out["sequence_length"] == 2
        assert out["actions_run"] == 2
        assert (root / "observe" / "qi_process_tensor_cycle_trend_summary.json").is_file()
        assert (root / "observe" / "next_qi_process_tensor_cycle_supervisor_packet.json").is_file()

        seed_supervisor_history(root / "compile_cap")
        code, out, sequence = run(root, "compile_cap", recipe_packet("observe_adapt_and_run"), lic("observe_adapt_and_run"), {"max_compiled_actions": 2})
        assert code == 1
        assert out["status"] == "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_BLOCKED"
        assert "recipe_compiler_not_ready" in out["blockers"]
        assert out["sequence_status"] == "NOT_RUN"

        seed_supervisor_history(root / "sequence_cap")
        code, out, sequence = run(root, "sequence_cap", recipe_packet("observe_adapt_and_run"), lic("observe_adapt_and_run"), {"max_sequence_actions": 2})
        assert code == 1
        assert "action_sequence_runner_not_ready" in out["blockers"]
        assert out["compile_status"] == "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY"

        seed_supervisor_history(root / "denied")
        code, out, _ = run(root, "denied", recipe_packet("observe_and_adapt", recipe_allowed=False), lic("observe_and_adapt"))
        assert code == 1
        assert "recipe_packet_recipe_allowed_not_true" in out["blockers"]

        seed_supervisor_history(root / "unknown")
        code, out, _ = run(root, "unknown", recipe_packet("arbitrary_shell"), lic("arbitrary_shell"))
        assert code == 1
        assert "recipe_not_allowlisted" in out["blockers"]

        seed_supervisor_history(root / "license_block")
        code, out, _ = run(root, "license_block", recipe_packet("observe_and_adapt"), lic())
        assert code == 1
        assert "observe_and_adapt_not_allowed_by_executor_license" in out["blockers"]

        code, out, _ = run(root, "missing", None, lic("observe_and_adapt"))
        assert code == 1
        assert "recipe_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "observe" / "qi_executable_action_recipe_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_RECIPE_EXECUTOR_READY"
    print("qi_executable_action_recipe_executor_v4_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

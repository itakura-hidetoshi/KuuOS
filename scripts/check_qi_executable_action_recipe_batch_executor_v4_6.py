#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_recipe_batch_executor_v4_6.py"


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
        "qi_executable_action_recipe_batch_executor_enabled": True,
        "apply_executable_action_recipe_batch_executor": True,
        "runtime_root": str(root),
        "max_batch_recipes": 5,
        "max_compiled_actions": 5,
        "max_sequence_actions": 5,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_LICENSE_READY",
        "batch_packet_read_allowed": True,
        "recipe_packet_write_allowed": True,
        "recipe_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def seed_supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def batch_packet(batch: list[Any], **overrides: Any) -> dict[str, Any]:
    value = {"batch_allowed": True, "batch": batch, "max_batch_recipes": 5}
    value.update(overrides)
    return value


def recipe(recipe_name: str, **overrides: Any) -> dict[str, Any]:
    value = {"recipe": recipe_name, "recipe_allowed": True, "max_compiled_actions": 5, "max_sequence_actions": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_action_recipe_batch_packet.json", packet)
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
    return done.returncode, load_json(op)


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY", case
    assert out["batch_completed"] is True, case
    assert out["recipes_run"] == out["batch_length"], case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        seed_supervisor_history(root / "batch")
        packet = batch_packet([recipe("observe_and_adapt"), recipe("observe_and_adapt")])
        code, out = run(root, "batch", packet, lic())
        assert_ready("batch", code, out)
        assert out["batch_length"] == 2
        assert out["recipes_run"] == 2
        assert out["recipe_records"][0]["recipe"] == "observe_and_adapt"
        assert out["recipe_records"][1]["recipe"] == "observe_and_adapt"
        assert (root / "batch" / "qi_executable_action_recipe_packet.json").is_file()

        seed_supervisor_history(root / "bad_recipe")
        code, out = run(root, "bad_recipe", batch_packet([recipe("arbitrary_shell")]), lic())
        assert code == 1
        assert "recipe_not_allowlisted" in out["blockers"]
        assert out["recipes_run"] == 0

        seed_supervisor_history(root / "denied")
        code, out = run(root, "denied", batch_packet([recipe("observe_and_adapt", recipe_allowed=False)]), lic())
        assert code == 1
        assert "recipe_packet_recipe_allowed_not_true" in out["blockers"]
        assert out["recipes_run"] == 0

        seed_supervisor_history(root / "cap")
        code, out = run(root, "cap", batch_packet(["observe_and_adapt", "observe_and_adapt"], max_batch_recipes=2), lic(), {"max_batch_recipes": 1})
        assert code == 1
        assert "batch_exceeds_cap" in out["blockers"]
        assert out["recipes_run"] == 0

        seed_supervisor_history(root / "delegated_block")
        code, out = run(root, "delegated_block", batch_packet([recipe("observe_adapt_and_run", max_sequence_actions=2)]), lic())
        assert code == 1
        assert "delegated_recipe_executor_blocked" in out["blockers"]
        assert out["recipes_run"] == 1

        code, out = run(root, "missing", None, lic())
        assert code == 1
        assert "batch_packet_missing_or_invalid" in out["blockers"]

        seed_supervisor_history(root / "blocked_license")
        code, out = run(root, "blocked_license", batch_packet(["observe_and_adapt"]), lic(recipe_executor_run_allowed=False))
        assert code == 1
        assert "recipe_executor_run_not_allowed" in out["blockers"]

        rows = read_rows(root / "batch" / "qi_executable_action_recipe_batch_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_EXECUTOR_READY"
    print("qi_executable_action_recipe_batch_executor_v4_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

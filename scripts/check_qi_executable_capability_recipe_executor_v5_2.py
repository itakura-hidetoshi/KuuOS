#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_recipe_executor_v5_2.py"


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
        "qi_executable_capability_recipe_executor_enabled": True,
        "apply_executable_capability_recipe_executor": True,
        "runtime_root": str(root),
        "max_compiled_capability_sequence": 5,
        "max_capability_sequence": 5,
    }
    value.update(overrides)
    return value


def lic(recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_LICENSE_READY",
        "capability_recipe_packet_read_allowed": True,
        "capability_recipe_compiler_run_allowed": True,
        "capability_sequence_runner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if recipe:
        value[f"allow_{recipe}_capability_recipe"] = True
    value.update(overrides)
    return value


def seed_supervisor_history(root: pathlib.Path) -> None:
    dump(root / "qi_circulation_trajectory_packet.json", {"trajectory": [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}, {"status": "QI_SCHEDULED_CLOSED_LOOP_READY"}]})
    dump(root / "qi_process_tensor_cycle_supervisor_receipt.json", {"cycle_records": [{"stop_reason_after_cycle": "converged", "scheduled_closed_loop_status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "trajectory_length": 2}]})
    append_jsonl(root / "qi_process_tensor_cycle_supervisor_audit.jsonl", [])


def recipe_packet(recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"capability_recipe": recipe, "capability_recipe_allowed": True, "max_compiled_capability_sequence": 5, "max_capability_sequence": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_capability_recipe_packet.json", packet)
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
    return done.returncode, load_json(op), load_json(runtime / "qi_executable_capability_sequence_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], sequence: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_READY", case
    assert out["executor_completed"] is True, case
    assert out["compile_status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY", case
    assert out["sequence_status"] == "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY", case
    assert out["capabilities_run"] == out["sequence_length"], case
    assert sequence["boundary"]["requires_v5_0_capability_sequence_runner"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, sequence = run(root, "compile_pair", recipe_packet("compile_recipe_and_batch"), lic("compile_recipe_and_batch"))
        assert_ready("compile_pair", code, out, sequence)
        assert out["capability_recipe"] == "compile_recipe_and_batch"
        assert out["sequence_length"] == 2
        assert out["capabilities_run"] == 2
        assert (root / "compile_pair" / "qi_executable_action_sequence_packet.json").is_file()
        assert (root / "compile_pair" / "qi_executable_action_recipe_batch_packet.json").is_file()

        seed_supervisor_history(root / "execute_batch")
        code, out, sequence = run(root, "execute_batch", recipe_packet("compile_batch_then_execute_batch"), lic("compile_batch_then_execute_batch"))
        assert_ready("execute_batch", code, out, sequence)
        assert out["sequence_length"] == 2
        assert out["capabilities_run"] == 2

        code, out, sequence = run(root, "compile_cap", recipe_packet("safe_compile_full_surface"), lic("safe_compile_full_surface"), {"max_compiled_capability_sequence": 2})
        assert code == 1
        assert out["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_BLOCKED"
        assert "capability_recipe_compiler_not_ready" in out["blockers"]
        assert out["sequence_status"] == "NOT_RUN"

        code, out, sequence = run(root, "sequence_cap", recipe_packet("safe_compile_full_surface"), lic("safe_compile_full_surface"), {"max_capability_sequence": 2})
        assert code == 1
        assert "capability_sequence_runner_not_ready" in out["blockers"]
        assert out["compile_status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY"

        code, out, _ = run(root, "denied", recipe_packet("compile_recipe_and_batch", capability_recipe_allowed=False), lic("compile_recipe_and_batch"))
        assert code == 1
        assert "capability_recipe_packet_allowed_not_true" in out["blockers"]

        code, out, _ = run(root, "unknown", recipe_packet("arbitrary_capability_recipe"), lic("arbitrary_capability_recipe"))
        assert code == 1
        assert "capability_recipe_not_allowlisted" in out["blockers"]

        code, out, _ = run(root, "license_block", recipe_packet("compile_recipe_and_batch"), lic())
        assert code == 1
        assert "compile_recipe_and_batch_not_allowed_by_capability_recipe_executor_license" in out["blockers"]

        code, out, _ = run(root, "missing", None, lic("compile_recipe_and_batch"))
        assert code == 1
        assert "capability_recipe_packet_missing_or_invalid" in out["blockers"]

        rows = read_rows(root / "compile_pair" / "qi_executable_capability_recipe_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_EXECUTOR_READY"
    print("qi_executable_capability_recipe_executor_v5_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

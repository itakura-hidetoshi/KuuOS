#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_recipe_batch_executor_v5_3.py"


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
        "qi_executable_capability_recipe_batch_executor_enabled": True,
        "apply_executable_capability_recipe_batch_executor": True,
        "runtime_root": str(root),
        "max_capability_recipe_batch": 5,
        "max_compiled_capability_sequence": 5,
        "max_capability_sequence": 5,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_EXECUTOR_LICENSE_READY",
        "batch_packet_read_allowed": True,
        "capability_recipe_packet_write_allowed": True,
        "capability_recipe_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def batch_packet(batch: list[Any], **overrides: Any) -> dict[str, Any]:
    value = {"batch_allowed": True, "batch": batch, "max_capability_recipe_batch": 5}
    value.update(overrides)
    return value


def recipe(recipe_name: str, **overrides: Any) -> dict[str, Any]:
    value = {"capability_recipe": recipe_name, "capability_recipe_allowed": True, "max_compiled_capability_sequence": 5, "max_capability_sequence": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_capability_recipe_batch_packet.json", packet)
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
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_EXECUTOR_READY", case
    assert out["batch_completed"] is True, case
    assert out["recipes_run"] == out["batch_length"], case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out = run(root, "batch", batch_packet([recipe("compile_recipe_and_batch"), recipe("safe_compile_full_surface")]), lic())
        assert_ready("batch", code, out)
        assert out["batch_length"] == 2
        assert out["recipes_run"] == 2
        assert out["recipe_records"][0]["capability_recipe"] == "compile_recipe_and_batch"
        assert out["recipe_records"][1]["capability_recipe"] == "safe_compile_full_surface"
        assert (root / "batch" / "qi_executable_capability_recipe_packet.json").is_file()

        code, out = run(root, "bad_recipe", batch_packet([recipe("arbitrary_capability_recipe")]), lic())
        assert code == 1
        assert "capability_recipe_not_allowlisted" in out["blockers"]
        assert out["recipes_run"] == 0

        code, out = run(root, "denied", batch_packet([recipe("compile_recipe_and_batch", capability_recipe_allowed=False)]), lic())
        assert code == 1
        assert "capability_recipe_packet_allowed_not_true" in out["blockers"]
        assert out["recipes_run"] == 0

        code, out = run(root, "cap", batch_packet(["compile_recipe_and_batch", "safe_compile_full_surface"], max_capability_recipe_batch=2), lic(), {"max_capability_recipe_batch": 1})
        assert code == 1
        assert "capability_recipe_batch_exceeds_cap" in out["blockers"]
        assert out["recipes_run"] == 0

        code, out = run(root, "delegated_block", batch_packet([recipe("safe_compile_full_surface", max_capability_sequence=2)]), lic())
        assert code == 1
        assert "delegated_capability_recipe_executor_blocked" in out["blockers"]
        assert out["recipes_run"] == 1

        code, out = run(root, "missing", None, lic())
        assert code == 1
        assert "capability_recipe_batch_packet_missing_or_invalid" in out["blockers"]

        code, out = run(root, "blocked_license", batch_packet(["compile_recipe_and_batch"]), lic(capability_recipe_executor_run_allowed=False))
        assert code == 1
        assert "capability_recipe_executor_run_not_allowed" in out["blockers"]

        rows = read_rows(root / "batch" / "qi_executable_capability_recipe_batch_executor_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_EXECUTOR_READY"
    print("qi_executable_capability_recipe_batch_executor_v5_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

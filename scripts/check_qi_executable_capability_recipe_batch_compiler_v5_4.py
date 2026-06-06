#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_recipe_batch_compiler_v5_4.py"


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
        "qi_executable_capability_recipe_batch_compiler_enabled": True,
        "apply_executable_capability_recipe_batch_compiler": True,
        "runtime_root": str(root),
        "max_compiled_capability_recipe_batch": 5,
    }
    value.update(overrides)
    return value


def lic(batch_recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_LICENSE_READY",
        "batch_compiler_packet_read_allowed": True,
        "batch_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if batch_recipe:
        value[f"allow_{batch_recipe}_batch_recipe"] = True
    value.update(overrides)
    return value


def compiler_packet(batch_recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"batch_recipe": batch_recipe, "batch_recipe_allowed": True, "max_compiled_capability_recipe_batch": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_capability_recipe_batch_compiler_packet.json", packet)
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
    return done.returncode, load_json(op), load_json(runtime / "qi_executable_capability_recipe_batch_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], batch: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert batch["boundary"]["requires_v5_3_capability_recipe_batch_executor"] is True, case


def recipes(batch: dict[str, Any]) -> list[str]:
    return [item["capability_recipe"] for item in batch.get("batch", [])]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, batch = run(root, "twice", compiler_packet("compile_surface_twice"), lic("compile_surface_twice"))
        assert_ready("twice", code, out, batch)
        assert recipes(batch) == ["compile_recipe_and_batch", "compile_recipe_and_batch"]
        assert out["batch_length"] == 2

        packet = compiler_packet(
            "safe_full_capability_batch_surface",
            default_recipe_context={"max_compiled_capability_sequence": 5, "max_capability_sequence": 5},
            recipe_context_by_recipe={"compile_batch_then_execute_batch": {"max_capability_sequence": 2}},
        )
        code, out, batch = run(root, "full", packet, lic("safe_full_capability_batch_surface"))
        assert_ready("full", code, out, batch)
        assert recipes(batch) == ["compile_recipe_and_batch", "safe_compile_full_surface", "compile_batch_then_execute_batch"]
        assert batch["batch"][2]["max_capability_sequence"] == 2

        code, out, batch = run(root, "observe", compiler_packet("observe_compile_batch_surface"), lic("observe_compile_batch_surface"))
        assert_ready("observe", code, out, batch)
        assert recipes(batch) == ["route_observe_then_compile", "compile_recipe_and_batch"]

        code, out, batch = run(root, "unknown", compiler_packet("arbitrary_capability_batch"), lic("arbitrary_capability_batch"))
        assert code == 1
        assert "capability_recipe_batch_not_allowlisted" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "denied", compiler_packet("compile_surface_twice", batch_recipe_allowed=False), lic("compile_surface_twice"))
        assert code == 1
        assert "capability_recipe_batch_packet_allowed_not_true" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "license_block", compiler_packet("compile_surface_twice"), lic())
        assert code == 1
        assert "compile_surface_twice_not_allowed_by_capability_recipe_batch_compiler_license" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "cap", compiler_packet("safe_full_capability_batch_surface"), lic("safe_full_capability_batch_surface"), {"max_compiled_capability_recipe_batch": 2})
        assert code == 1
        assert "compiled_capability_recipe_batch_exceeds_cap" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "missing", None, lic("compile_surface_twice"))
        assert code == 1
        assert "capability_recipe_batch_compiler_packet_missing_or_invalid" in out["blockers"]
        assert batch == {}

        rows = read_rows(root / "twice" / "qi_executable_capability_recipe_batch_compiler_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_BATCH_COMPILER_READY"
    print("qi_executable_capability_recipe_batch_compiler_v5_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

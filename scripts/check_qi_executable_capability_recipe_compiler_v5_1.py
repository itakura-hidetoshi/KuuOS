#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_recipe_compiler_v5_1.py"


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
        "qi_executable_capability_recipe_compiler_enabled": True,
        "apply_executable_capability_recipe_compiler": True,
        "runtime_root": str(root),
        "max_compiled_capability_sequence": 5,
    }
    value.update(overrides)
    return value


def lic(recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_LICENSE_READY",
        "capability_recipe_packet_read_allowed": True,
        "capability_sequence_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if recipe:
        value[f"allow_{recipe}_capability_recipe"] = True
    value.update(overrides)
    return value


def recipe_packet(recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"capability_recipe": recipe, "capability_recipe_allowed": True, "max_compiled_capability_sequence": 5}
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
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert sequence["boundary"]["requires_v5_0_capability_sequence_runner"] is True, case


def kinds(sequence: dict[str, Any]) -> list[str]:
    return [item["capability_kind"] for item in sequence.get("sequence", [])]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, sequence = run(root, "compile_pair", recipe_packet("compile_recipe_and_batch"), lic("compile_recipe_and_batch"))
        assert_ready("compile_pair", code, out, sequence)
        assert kinds(sequence) == ["recipe_compile", "batch_recipe_compile"]
        assert out["sequence_length"] == 2

        packet = recipe_packet(
            "compile_batch_then_execute_batch",
            default_runtime_context_patch={"max_batch_recipes": 4},
            runtime_context_patch_by_capability={"batch_recipe_execute": {"max_sequence_actions": 4}},
            delegated_input_patch_by_capability={"batch_recipe_execute": {"max_batch_recipes": 4}},
        )
        code, out, sequence = run(root, "execute_batch", packet, lic("compile_batch_then_execute_batch"))
        assert_ready("execute_batch", code, out, sequence)
        assert kinds(sequence) == ["batch_recipe_compile", "batch_recipe_execute"]
        assert sequence["sequence"][1]["runtime_context_patch"]["max_sequence_actions"] == 4
        assert sequence["sequence"][1]["delegated_input_packet"]["max_batch_recipes"] == 4

        code, out, sequence = run(root, "full", recipe_packet("safe_compile_full_surface"), lic("safe_compile_full_surface"))
        assert_ready("full", code, out, sequence)
        assert kinds(sequence) == ["recipe_compile", "batch_recipe_compile", "batch_recipe_compile"]

        code, out, sequence = run(root, "unknown", recipe_packet("arbitrary_capability_recipe"), lic("arbitrary_capability_recipe"))
        assert code == 1
        assert "capability_recipe_not_allowlisted" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "denied", recipe_packet("compile_recipe_and_batch", capability_recipe_allowed=False), lic("compile_recipe_and_batch"))
        assert code == 1
        assert "capability_recipe_packet_allowed_not_true" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "license_block", recipe_packet("compile_recipe_and_batch"), lic())
        assert code == 1
        assert "compile_recipe_and_batch_not_allowed_by_capability_recipe_compiler_license" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "cap", recipe_packet("safe_compile_full_surface"), lic("safe_compile_full_surface"), {"max_compiled_capability_sequence": 2})
        assert code == 1
        assert "compiled_capability_sequence_exceeds_cap" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "missing", None, lic("compile_recipe_and_batch"))
        assert code == 1
        assert "capability_recipe_packet_missing_or_invalid" in out["blockers"]
        assert sequence == {}

        rows = read_rows(root / "compile_pair" / "qi_executable_capability_recipe_compiler_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_RECIPE_COMPILER_READY"
    print("qi_executable_capability_recipe_compiler_v5_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

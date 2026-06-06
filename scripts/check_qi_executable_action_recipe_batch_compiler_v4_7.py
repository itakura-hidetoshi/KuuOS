#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_recipe_batch_compiler_v4_7.py"


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
        "qi_executable_action_recipe_batch_compiler_enabled": True,
        "apply_executable_action_recipe_batch_compiler": True,
        "runtime_root": str(root),
        "max_compiled_batch_recipes": 5,
    }
    value.update(overrides)
    return value


def lic(batch_recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_LICENSE_READY",
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
    assert out["status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert batch["boundary"]["requires_v4_6_batch_executor"] is True, case


def recipes(batch: dict[str, Any]) -> list[str]:
    return [item["recipe"] for item in batch.get("batch", [])]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, batch = run(root, "observe_twice", compiler_packet("observe_adapt_twice"), lic("observe_adapt_twice"))
        assert_ready("observe_twice", code, out, batch)
        assert recipes(batch) == ["observe_and_adapt", "observe_and_adapt"]
        assert out["batch_length"] == 2

        packet = compiler_packet(
            "safe_full_observe_adapt_run",
            default_recipe_context={"max_compiled_actions": 5, "max_sequence_actions": 5},
            recipe_context_by_recipe={"observe_adapt_and_run": {"max_sequence_actions": 3}},
        )
        code, out, batch = run(root, "full", packet, lic("safe_full_observe_adapt_run"))
        assert_ready("full", code, out, batch)
        assert recipes(batch) == ["observe_and_adapt", "observe_adapt_and_run"]
        assert batch["batch"][1]["max_sequence_actions"] == 3

        code, out, batch = run(root, "return_cycle", compiler_packet("return_cycle_observe"), lic("return_cycle_observe"))
        assert_ready("return_cycle", code, out, batch)
        assert recipes(batch) == ["return_loop_then_cycle", "single_cycle_then_summarize"]

        code, out, batch = run(root, "unknown", compiler_packet("arbitrary_batch"), lic("arbitrary_batch"))
        assert code == 1
        assert "batch_recipe_not_allowlisted" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "denied", compiler_packet("observe_adapt_twice", batch_recipe_allowed=False), lic("observe_adapt_twice"))
        assert code == 1
        assert "batch_recipe_packet_allowed_not_true" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "license_block", compiler_packet("observe_adapt_twice"), lic())
        assert code == 1
        assert "observe_adapt_twice_not_allowed_by_batch_compiler_license" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "cap", compiler_packet("observe_supervise_adapt"), lic("observe_supervise_adapt"), {"max_compiled_batch_recipes": 2})
        assert code == 1
        assert "compiled_batch_exceeds_cap" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "missing", None, lic("observe_adapt_twice"))
        assert code == 1
        assert "batch_compiler_packet_missing_or_invalid" in out["blockers"]
        assert batch == {}

        rows = read_rows(root / "observe_twice" / "qi_executable_action_recipe_batch_compiler_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_RECIPE_BATCH_COMPILER_READY"
    print("qi_executable_action_recipe_batch_compiler_v4_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_action_recipe_compiler_v4_4.py"


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
        "qi_executable_action_recipe_compiler_enabled": True,
        "apply_executable_action_recipe_compiler": True,
        "runtime_root": str(root),
        "max_compiled_actions": 5,
    }
    value.update(overrides)
    return value


def lic(recipe: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_LICENSE_READY",
        "recipe_packet_read_allowed": True,
        "sequence_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    if recipe:
        value[f"allow_{recipe}_recipe"] = True
    value.update(overrides)
    return value


def recipe_packet(recipe: str, **overrides: Any) -> dict[str, Any]:
    value = {"recipe": recipe, "recipe_allowed": True, "max_compiled_actions": 5}
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
    assert out["status"] == "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert sequence["boundary"]["does_not_execute_actions"] is True, case


def actions(sequence: dict[str, Any]) -> list[str]:
    return [item["action"] for item in sequence.get("sequence", [])]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, sequence = run(root, "observe_adapt", recipe_packet("observe_and_adapt"), lic("observe_and_adapt"))
        assert_ready("observe_adapt", code, out, sequence)
        assert actions(sequence) == ["cycle_trend_summary", "trend_adaptive_supervisor_packet"]
        assert out["sequence_length"] == 2

        packet = recipe_packet(
            "observe_adapt_and_run",
            default_action_context_patch={"max_summary_records": 7},
            action_context_patch_by_action={"trend_adaptive_supervisor_run": {"max_supervised_cycles": 1}},
        )
        code, out, sequence = run(root, "adapt_run", packet, lic("observe_adapt_and_run"))
        assert_ready("adapt_run", code, out, sequence)
        assert actions(sequence) == ["cycle_trend_summary", "trend_adaptive_supervisor_packet", "trend_adaptive_supervisor_run"]
        assert sequence["sequence"][0]["action_context_patch"]["max_summary_records"] == 7
        assert sequence["sequence"][2]["action_context_patch"]["max_supervised_cycles"] == 1

        code, out, sequence = run(root, "supervise", recipe_packet("supervise_then_summarize"), lic("supervise_then_summarize"))
        assert_ready("supervise", code, out, sequence)
        assert actions(sequence) == ["cycle_supervisor", "cycle_trend_summary"]

        code, out, sequence = run(root, "unknown", recipe_packet("arbitrary_shell"), lic("arbitrary_shell"))
        assert code == 1
        assert "recipe_not_allowlisted" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "denied", recipe_packet("observe_and_adapt", recipe_allowed=False), lic("observe_and_adapt"))
        assert code == 1
        assert "recipe_packet_recipe_allowed_not_true" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "license_block", recipe_packet("observe_and_adapt"), lic())
        assert code == 1
        assert "observe_and_adapt_not_allowed_by_compiler_license" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "cap", recipe_packet("observe_adapt_and_run"), lic("observe_adapt_and_run"), {"max_compiled_actions": 2})
        assert code == 1
        assert "compiled_sequence_exceeds_cap" in out["blockers"]
        assert sequence == {}

        code, out, sequence = run(root, "missing", None, lic("observe_and_adapt"))
        assert code == 1
        assert "recipe_packet_missing_or_invalid" in out["blockers"]
        assert sequence == {}

        rows = read_rows(root / "observe_adapt" / "qi_executable_action_recipe_compiler_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_ACTION_RECIPE_COMPILER_READY"
    print("qi_executable_action_recipe_compiler_v4_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

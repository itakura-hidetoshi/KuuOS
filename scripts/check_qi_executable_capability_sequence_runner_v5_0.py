#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_executable_capability_sequence_runner_v5_0.py"


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
        "qi_executable_capability_sequence_runner_enabled": True,
        "apply_executable_capability_sequence_runner": True,
        "runtime_root": str(root),
        "max_capability_sequence": 5,
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_LICENSE_READY",
        "sequence_packet_read_allowed": True,
        "capability_packet_write_allowed": True,
        "capability_router_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def cap(kind: str, delegated: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "capability_kind": kind,
        "capability_allowed": True,
        "delegated_input_packet": delegated,
        "runtime_context_patch": {},
    }
    value.update(overrides)
    return value


def sequence_packet(sequence: list[dict[str, Any]], **overrides: Any) -> dict[str, Any]:
    value = {"sequence_allowed": True, "sequence": sequence, "max_capability_sequence": 5}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "qi_executable_capability_sequence_packet.json", packet)
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
    assert out["status"] == "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY", case
    assert out["sequence_completed"] is True, case
    assert out["capabilities_run"] == out["sequence_length"], case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        packet = sequence_packet([
            cap("recipe_compile", {"recipe": "observe_and_adapt", "recipe_allowed": True}),
            cap("batch_recipe_compile", {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}),
        ])
        code, out = run(root, "sequence", packet, lic())
        assert_ready("sequence", code, out)
        assert out["capabilities_run"] == 2
        assert out["capability_records"][0]["capability_kind"] == "recipe_compile"
        assert out["capability_records"][1]["capability_kind"] == "batch_recipe_compile"
        assert (root / "sequence" / "qi_executable_action_sequence_packet.json").is_file()
        assert (root / "sequence" / "qi_executable_action_recipe_batch_packet.json").is_file()

        code, out = run(root, "bad_kind", sequence_packet([cap("shell", {"cmd": "echo no"})]), lic())
        assert code == 1
        assert "capability_kind_not_allowlisted" in out["blockers"]
        assert out["capabilities_run"] == 0

        code, out = run(root, "denied", sequence_packet([cap("recipe_compile", {"recipe": "observe_and_adapt", "recipe_allowed": True}, capability_allowed=False)]), lic())
        assert code == 1
        assert "capability_packet_allowed_not_true" in out["blockers"]
        assert out["capabilities_run"] == 0

        code, out = run(root, "missing_delegated", sequence_packet([cap("recipe_compile", {})]), lic())
        assert code == 1
        assert "delegated_input_packet_missing_or_invalid" in out["blockers"]
        assert out["capabilities_run"] == 0

        code, out = run(root, "cap", sequence_packet([
            cap("recipe_compile", {"recipe": "observe_and_adapt", "recipe_allowed": True}),
            cap("batch_recipe_compile", {"batch_recipe": "observe_adapt_twice", "batch_recipe_allowed": True}),
        ]), lic(), {"max_capability_sequence": 1})
        assert code == 1
        assert "capability_sequence_exceeds_cap" in out["blockers"]
        assert out["capabilities_run"] == 0

        code, out = run(root, "missing", None, lic())
        assert code == 1
        assert "capability_sequence_packet_missing_or_invalid" in out["blockers"]

        code, out = run(root, "blocked_license", sequence_packet([cap("recipe_compile", {"recipe": "observe_and_adapt", "recipe_allowed": True})]), lic(capability_router_run_allowed=False))
        assert code == 1
        assert "capability_router_run_not_allowed" in out["blockers"]

        rows = read_rows(root / "sequence" / "qi_executable_capability_sequence_runner_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY"
    print("qi_executable_capability_sequence_runner_v5_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

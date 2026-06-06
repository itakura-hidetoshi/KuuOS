#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_capability_planner_v5_5.py"
REQUIRED = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]


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
        "qi_github_actions_capability_planner_enabled": True,
        "apply_github_actions_capability_planner": True,
        "runtime_root": str(root),
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_LICENSE_READY",
        "github_actions_status_packet_read_allowed": True,
        "capability_recipe_batch_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def run_row(name: str, status: str = "completed", conclusion: str = "success") -> dict[str, Any]:
    return {"name": name, "status": status, "conclusion": conclusion, "run_number": 1}


def packet(rows: list[dict[str, Any]], **overrides: Any) -> dict[str, Any]:
    value = {"github_actions_status_allowed": True, "required_workflows": REQUIRED, "workflow_runs": rows}
    value.update(overrides)
    return value


def success_rows() -> list[dict[str, Any]]:
    return [run_row(name) for name in REQUIRED]


def run(root: pathlib.Path, name: str, status_packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if status_packet is not None:
        dump(runtime / "qi_github_actions_status_packet.json", status_packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
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
    assert out["status"] == "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case
    assert batch["boundary"]["does_not_dispatch_workflows"] is True, case
    assert batch["boundary"]["requires_v5_3_capability_recipe_batch_executor"] is True, case


def recipes(batch: dict[str, Any]) -> list[str]:
    return [item["capability_recipe"] for item in batch.get("batch", [])]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, batch = run(root, "all_green", packet(success_rows()), lic())
        assert_ready("all_green", code, out, batch)
        assert out["plan_class"] == "github_actions_all_green_batch"
        assert recipes(batch) == ["compile_recipe_and_batch", "safe_compile_full_surface"]

        rows = success_rows()
        rows[-1] = run_row("Qi Process Tensor Review Checks", "completed", "failure")
        code, out, batch = run(root, "qi_fail", packet(rows), lic())
        assert_ready("qi_fail", code, out, batch)
        assert out["plan_class"] == "github_actions_qi_repair_batch"
        assert recipes(batch) == ["route_observe_then_compile", "compile_recipe_and_batch"]

        rows = success_rows()
        rows[-2] = run_row("KuuOS Runtime Full Check", "completed", "failure")
        code, out, batch = run(root, "runtime_fail", packet(rows), lic())
        assert_ready("runtime_fail", code, out, batch)
        assert out["plan_class"] == "github_actions_runtime_repair_batch"
        assert recipes(batch) == ["compile_then_execute_recipe", "compile_recipe_and_batch"]

        rows = success_rows()
        rows[0] = run_row("All Governance Validation", "completed", "failure")
        code, out, batch = run(root, "gov_fail", packet(rows), lic())
        assert_ready("gov_fail", code, out, batch)
        assert out["plan_class"] == "github_actions_governance_repair_batch"
        assert recipes(batch) == ["safe_compile_full_surface"]

        rows = success_rows()
        rows[0] = run_row("All Governance Validation", "in_progress", "")
        code, out, batch = run(root, "pending", packet(rows), lic())
        assert_ready("pending", code, out, batch)
        assert out["plan_class"] == "github_actions_pending_observe_batch"
        assert recipes(batch) == ["compile_recipe_and_batch"]

        code, out, batch = run(root, "missing_required", packet(success_rows()[:-1]), lic())
        assert code == 1
        assert out["status"] == "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_BLOCKED"
        assert "required_workflows_missing" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "denied", packet(success_rows(), github_actions_status_allowed=False), lic())
        assert code == 1
        assert "github_actions_status_packet_allowed_not_true" in out["blockers"]
        assert batch == {}

        code, out, batch = run(root, "license_block", packet(success_rows()), lic(capability_recipe_batch_packet_write_allowed=False))
        assert code == 1
        assert "capability_recipe_batch_packet_write_not_allowed" in out["blockers"]
        assert batch == {}

        rows_log = read_rows(root / "all_green" / "qi_github_actions_capability_planner_audit.jsonl")
        assert len(rows_log) == 1
        assert rows_log[0]["status"] == "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_READY"
    print("qi_github_actions_capability_planner_v5_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

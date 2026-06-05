#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_scheduled_closed_loop_runner_v3_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_scheduled_closed_loop_enabled": True, "apply_scheduled_closed_loop": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_SCHEDULED_CLOSED_LOOP_LICENSE_READY", "packet_read_allowed": True, "scheduler_run_allowed": True, "closed_loop_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def route_base() -> dict[str, Any]:
    return {"repository_full_name": "itakura-hidetoshi/KuuOS", "branch": "qi-scheduled-loop-test", "base_branch": "main", "base_sha": "abc123", "pr_number": 1, "expected_head_sha": "abc123", "actual_head_sha": "abc123", "mode": "mock", "required_checks": [{"name": "KuuOS Runtime Full Check", "status": "success"}], "files": [{"kind": "create_file", "path": "tmp/qi-scheduled-loop-test.txt", "content": "ok", "message": "Qi scheduled loop test"}]}


def packet(qi: dict[str, Any]) -> dict[str, Any]:
    return {"initial_qi_packet": qi, "route_base": route_base()}


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_scheduled_closed_loop_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def expect_ok(errors: list[str], name: str, rc: int, out: dict[str, Any], objective: str) -> None:
    if rc != 0 or out.get("status") not in {"QI_SCHEDULED_CLOSED_LOOP_READY", "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}:
        errors.append(f"{name}_status")
    if out.get("scheduler_status") != "QI_CIRCULATION_SCHEDULER_READY":
        errors.append(f"{name}_scheduler")
    if out.get("closed_loop_status") not in {"QI_CIRCULATION_CLOSED_LOOP_READY", "QI_CIRCULATION_CLOSED_LOOP_CONVERGED"}:
        errors.append(f"{name}_closed_loop")
    if out.get("objective_class") != objective:
        errors.append(f"{name}_objective")
    if out.get("cycle_count", 0) < 1:
        errors.append(f"{name}_cycles")
    if not out.get("final_qi_packet"):
        errors.append(f"{name}_final_packet")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "maintain", packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05}), lic())
        expect_ok(errors, "maintain", rc, out, "maintain")

        rc, out = run(root, "rebalance", packet({"qi_flow": 0.60, "coherence_score": 0.55, "circulation_pressure": 0.55, "friction": 0.25}), lic())
        expect_ok(errors, "rebalance", rc, out, "rebalance")

        rc, out = run(root, "reopen", packet({"qi_flow": 0.20, "coherence_score": 0.25, "circulation_pressure": 0.20, "friction": 0.80}), lic())
        expect_ok(errors, "reopen", rc, out, "reopen")

        rc, out = run(root, "stop", packet({"qi_flow": 0.90, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05, "critical_blocker_present": True}), lic())
        if rc != 1 or out.get("status") != "QI_SCHEDULED_CLOSED_LOOP_BLOCKED":
            errors.append("stop_status")
        if "scheduler_not_ready" not in out.get("blockers", []):
            errors.append("stop_reason")
        if out.get("closed_loop_status") != "NOT_RUN":
            errors.append("stop_closed_loop_should_not_run")

        rc, out = run(root, "license", packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05}), lic(closed_loop_run_allowed=False))
        if rc != 1 or "closed_loop_run_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

        if len(read_rows(root / "maintain" / "qi_scheduled_closed_loop_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "maintain" / "qi_scheduled_closed_loop_receipt.json").get("status") != out.get("status") and not load_json(root / "maintain" / "qi_scheduled_closed_loop_receipt.json"):
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi scheduled closed-loop runner v3.2 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

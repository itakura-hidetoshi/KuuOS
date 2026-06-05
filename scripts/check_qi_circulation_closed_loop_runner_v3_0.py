#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_closed_loop_runner_v3_0.py"


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
    return {
        "qi_circulation_closed_loop_enabled": True,
        "apply_circulation_closed_loop": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_CIRCULATION_CLOSED_LOOP_LICENSE_READY",
        "packet_read_allowed": True,
        "router_run_allowed": True,
        "feedback_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "max_cycles": 3,
        "convergence_threshold": 0.000001,
        "initial_qi_packet": {
            "qi_flow": 0.20,
            "coherence_score": 0.30,
            "circulation_pressure": 0.25,
            "friction": 0.70,
            "recovery_witness_present": True,
        },
        "route_base": {
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "branch": "qi-closed-loop-test",
            "base_branch": "main",
            "base_sha": "abc123",
            "pr_number": 1,
            "expected_head_sha": "abc123",
            "actual_head_sha": "abc123",
            "mode": "mock",
            "required_checks": [{"name": "KuuOS Runtime Full Check", "status": "success"}],
            "files": [{"kind": "create_file", "path": "tmp/qi-closed-loop-test.txt", "content": "ok", "message": "Qi closed-loop test"}],
        },
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_circulation_closed_loop_packet.json", p)
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


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "ready", packet(), lic())
        if rc != 0 or out.get("status") not in {"QI_CIRCULATION_CLOSED_LOOP_READY", "QI_CIRCULATION_CLOSED_LOOP_CONVERGED"}:
            errors.append("ready_status")
        if out.get("cycle_count", 0) < 1:
            errors.append("ready_cycle_count")
        if not out.get("records") or len(out.get("records", [])) < 2:
            errors.append("ready_records")
        final_qi = out.get("final_qi_packet", {})
        if final_qi.get("qi_flow", 0) <= 0.20:
            errors.append("ready_flow_not_improved")
        if final_qi.get("friction", 1) >= 0.70:
            errors.append("ready_friction_not_reduced")
        if load_json(root / "ready" / "qi_circulation_closed_loop_receipt.json").get("status") != out.get("status"):
            errors.append("ready_receipt")
        if len(read_rows(root / "ready" / "qi_circulation_closed_loop_audit.jsonl")) != 1:
            errors.append("ready_audit")

        convergent_packet = packet(
            max_cycles=3,
            convergence_threshold=10.0,
            initial_qi_packet={
                "qi_flow": 0.90,
                "coherence_score": 0.85,
                "circulation_pressure": 0.85,
                "friction": 0.05,
                "recovery_witness_present": True,
            },
        )
        rc, out = run(root, "converged", convergent_packet, lic())
        if rc != 0 or out.get("status") != "QI_CIRCULATION_CLOSED_LOOP_CONVERGED":
            errors.append("converged_status")
        if out.get("converged") is not True:
            errors.append("converged_flag")
        if out.get("cycle_count") < 2:
            errors.append("converged_cycle_count")

        blocked_packet = packet(initial_qi_packet={
            "qi_flow": 0.90,
            "coherence_score": 0.90,
            "circulation_pressure": 0.90,
            "friction": 0.05,
            "critical_blocker_present": True,
        })
        rc, out = run(root, "blocked", blocked_packet, lic())
        if rc != 1 or out.get("status") != "QI_CIRCULATION_CLOSED_LOOP_BLOCKED":
            errors.append("blocked_status")
        if "router_blocked" not in out.get("blockers", []):
            errors.append("blocked_reason")

        missing_route = packet(route_base={})
        rc, out = run(root, "missing", missing_route, lic())
        if rc != 1 or out.get("status") != "QI_CIRCULATION_CLOSED_LOOP_BLOCKED":
            errors.append("missing_status")
        if "route_base_repository_full_name_missing" not in out.get("blockers", []):
            errors.append("missing_route_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi circulation closed-loop runner v3.0 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

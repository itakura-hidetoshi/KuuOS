#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_change_router_v2_8.py"


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
    return {"qi_circulation_change_router_enabled": True, "apply_circulation_change_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_CIRCULATION_CHANGE_ROUTER_LICENSE_READY",
        "route_packet_read_allowed": True,
        "circulation_packet_write_allowed": True,
        "circulation_run_allowed": True,
        "forward_packet_write_allowed": True,
        "forward_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def base_route(qi_packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "branch": "qi-router-test",
        "base_branch": "main",
        "base_sha": "abc123",
        "pr_number": 1,
        "expected_head_sha": "abc123",
        "actual_head_sha": "abc123",
        "mode": "mock",
        "required_checks": [{"name": "KuuOS Runtime Full Check", "status": "success"}],
        "files": [{"kind": "create_file", "path": "tmp/qi-router-test.txt", "content": "ok", "message": "Qi router test"}],
        "qi_process_tensor_packet": qi_packet,
    }


def run(root: pathlib.Path, name: str, route: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    dump(runtime / "circulation_change_route_packet.json", route)
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


def assert_routed(errors: list[str], name: str, out: dict[str, Any], action: str) -> None:
    if out.get("status") != "QI_CIRCULATION_CHANGE_ROUTER_ROUTED":
        errors.append(f"{name}_status")
    if out.get("recommended_action") != action:
        errors.append(f"{name}_action")
    if out.get("routed") is not True:
        errors.append(f"{name}_routed")
    if out.get("downstream_status") != "QI_FORWARD_CHANGE_RUNNER_MERGED":
        errors.append(f"{name}_downstream")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "stable", base_route({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.80, "recovery_witness_present": True, "friction": 0.05}), lic())
        if rc != 0:
            errors.append("stable_rc")
        assert_routed(errors, "stable", out, "continue_cycle")

        rc, out = run(root, "meta", base_route({"qi_flow": 0.60, "coherence_score": 0.55, "circulation_pressure": 0.55, "recovery_witness_present": True, "friction": 0.15}), lic())
        if rc != 0:
            errors.append("meta_rc")
        assert_routed(errors, "meta", out, "rebalance_and_continue")

        rc, out = run(root, "stagnation", base_route({"qi_flow": 0.10, "coherence_score": 0.20, "circulation_pressure": 0.10, "recovery_witness_present": False, "friction": 0.80}), lic())
        if rc != 0:
            errors.append("stagnation_rc")
        assert_routed(errors, "stagnation", out, "reopen_flow")

        rc, out = run(root, "concrete", base_route({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.80, "critical_blocker_present": True}), lic())
        if rc != 1 or out.get("status") != "QI_CIRCULATION_CHANGE_ROUTER_BLOCKED":
            errors.append("concrete_status")
        if out.get("recommended_action") != "concrete_stop" or out.get("routed") is not False:
            errors.append("concrete_action")

        if len(read_rows(root / "stable" / "circulation_change_router_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "stable" / "circulation_change_router_receipt.json").get("status") != "QI_CIRCULATION_CHANGE_ROUTER_ROUTED":
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi circulation change router v2.8 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

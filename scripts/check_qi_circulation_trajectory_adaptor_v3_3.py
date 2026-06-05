#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_trajectory_adaptor_v3_3.py"


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
    return {"qi_circulation_trajectory_adaptor_enabled": True, "apply_circulation_trajectory_adaptor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_CIRCULATION_TRAJECTORY_ADAPTOR_LICENSE_READY", "packet_read_allowed": True, "next_scheduler_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_circulation_trajectory_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "next_qi_circulation_scheduler_packet.json")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        base = {"initial_qi_packet": {"qi_flow": 0.5}, "route_base": {"repository_full_name": "itakura-hidetoshi/KuuOS"}}

        stable = dict(base)
        stable["trajectory"] = [{"status": "QI_SCHEDULED_CLOSED_LOOP_CONVERGED", "objective_class": "maintain", "converged": True, "cycle_count": 2, "final_qi_packet": {"qi_flow": 0.90, "friction": 0.05}}]
        rc, out, nxt = run(root, "stable", stable, lic())
        if rc != 0 or out.get("adaptation_class") != "stable_lighten":
            errors.append("stable_class")
        if out.get("next_objective_hint") != "maintain" or out.get("max_cycles_delta") != -1:
            errors.append("stable_params")
        if nxt.get("objective_hint") != "maintain":
            errors.append("stable_next")

        blocked = dict(base)
        blocked["trajectory"] = [{"status": "QI_SCHEDULED_CLOSED_LOOP_BLOCKED", "objective_class": "rebalance", "converged": False, "cycle_count": 1, "final_qi_packet": {"qi_flow": 0.30, "friction": 0.70}}]
        rc, out, nxt = run(root, "blocked", blocked, lic())
        if rc != 0 or out.get("adaptation_class") != "blocked_recovery":
            errors.append("blocked_class")
        if out.get("next_objective_hint") != "reopen" or out.get("max_cycles_delta") != 2:
            errors.append("blocked_params")

        long_cycle = dict(base)
        long_cycle["trajectory"] = [{"status": "QI_SCHEDULED_CLOSED_LOOP_READY", "objective_class": "rebalance", "converged": False, "cycle_count": 6, "final_qi_packet": {"qi_flow": 0.60, "friction": 0.30}}]
        rc, out, nxt = run(root, "long", long_cycle, lic())
        if rc != 0 or out.get("adaptation_class") != "long_cycle_rebalance":
            errors.append("long_class")
        if out.get("next_objective_hint") != "rebalance" or out.get("max_cycles_delta") != 1:
            errors.append("long_params")

        rc, out, nxt = run(root, "empty", base, lic())
        if rc != 0 or out.get("adaptation_class") != "no_trajectory":
            errors.append("empty_class")
        if out.get("next_objective_hint") != "reopen":
            errors.append("empty_hint")

        rc, out, nxt = run(root, "license", stable, lic(next_scheduler_packet_write_allowed=False))
        if rc != 1 or out.get("status") != "QI_CIRCULATION_TRAJECTORY_ADAPTOR_BLOCKED":
            errors.append("license_status")
        if "next_scheduler_packet_write_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

        if len(read_rows(root / "stable" / "qi_circulation_trajectory_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "stable" / "qi_circulation_trajectory_receipt.json").get("status") != "QI_CIRCULATION_TRAJECTORY_ADAPTOR_READY":
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi circulation trajectory adaptor v3.3 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

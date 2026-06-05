#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_adaptive_objective_scheduler_v3_4.py"


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
    return {"qi_adaptive_scheduler_enabled": True, "apply_adaptive_scheduler": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_ADAPTIVE_SCHEDULER_LICENSE_READY", "packet_read_allowed": True, "base_scheduler_run_allowed": True, "closed_loop_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def route_base() -> dict[str, Any]:
    return {"repository_full_name": "itakura-hidetoshi/KuuOS", "branch": "qi-adaptive-test", "base_branch": "main", "base_sha": "abc123", "pr_number": 1, "expected_head_sha": "abc123", "actual_head_sha": "abc123"}


def packet(qi: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    src = {"initial_qi_packet": qi, "route_base": route_base()}
    src.update(overrides)
    return {"next_qi_circulation_scheduler_packet": src}


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_adaptive_scheduler_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_circulation_closed_loop_packet.json")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out, closed = run(root, "hint_reopen", packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05}, objective_hint="reopen", max_cycles_delta=2, convergence_threshold_delta=0.01), lic())
        if rc != 0 or out.get("status") != "QI_ADAPTIVE_SCHEDULER_READY":
            errors.append("hint_reopen_status")
        if out.get("base_objective_class") != "maintain" or out.get("applied_objective_class") != "reopen":
            errors.append("hint_reopen_objective")
        if out.get("adapted_max_cycles") != 8 or closed.get("max_cycles") != 8:
            errors.append("hint_reopen_cycles")
        if abs(float(out.get("adapted_threshold", 0.0)) - 0.05) > 1e-9:
            errors.append("hint_reopen_threshold")
        if closed.get("adaptive_scheduler_applied") is not True:
            errors.append("hint_reopen_marker")

        rc, out, closed = run(root, "lighten", packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05}, objective_hint="maintain", max_cycles_delta=-1, convergence_threshold_delta=-0.005), lic())
        if rc != 0 or out.get("adapted_max_cycles") != 1:
            errors.append("lighten_cycles")
        if abs(float(out.get("adapted_threshold", 0.0)) - 0.01) > 1e-9:
            errors.append("lighten_threshold")

        rc, out, closed = run(root, "invalid_hint", packet({"qi_flow": 0.70, "coherence_score": 0.65, "circulation_pressure": 0.65, "friction": 0.20}, objective_hint="unknown", max_cycles_delta=1), lic())
        if rc != 0 or out.get("applied_objective_class") != "rebalance":
            errors.append("invalid_hint_objective")
        if out.get("adapted_max_cycles") != 5:
            errors.append("invalid_hint_cycles")

        stop_packet = packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05, "critical_blocker_present": True}, objective_hint="reopen")
        rc, out, closed = run(root, "stop", stop_packet, lic())
        if rc != 1 or out.get("status") != "QI_ADAPTIVE_SCHEDULER_BLOCKED":
            errors.append("stop_status")
        if "base_scheduler_not_ready" not in out.get("blockers", []):
            errors.append("stop_reason")

        rc, out, closed = run(root, "license", packet({"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.90, "friction": 0.05}), lic(closed_loop_packet_write_allowed=False))
        if rc != 1 or "closed_loop_packet_write_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

        if len(read_rows(root / "hint_reopen" / "qi_adaptive_scheduler_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "hint_reopen" / "qi_adaptive_scheduler_receipt.json").get("status") != "QI_ADAPTIVE_SCHEDULER_READY":
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi adaptive objective scheduler v3.4 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

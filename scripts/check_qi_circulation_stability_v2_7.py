#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_stability_v2_7.py"


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
    return {"qi_circulation_stability_enabled": True, "apply_circulation_stability": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_CIRCULATION_STABILITY_LICENSE_READY", "packet_read_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, packet: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_circulation_packet.json", packet)
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

        rc, out = run(root, "stable", {"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.80, "recovery_witness_present": True, "friction": 0.05}, lic())
        if rc != 0 or out.get("status") != "QI_CIRCULATION_STABILITY_READY":
            errors.append("stable_status")
        if out.get("stability_class") != "stable_by_circulation" or out.get("recommended_action") != "continue_cycle":
            errors.append("stable_class")
        if out.get("cycle_open") is not True:
            errors.append("stable_cycle")

        rc, out = run(root, "meta", {"qi_flow": 0.60, "coherence_score": 0.55, "circulation_pressure": 0.55, "recovery_witness_present": True, "friction": 0.15}, lic())
        if rc != 0 or out.get("recommended_action") != "rebalance_and_continue":
            errors.append("meta_action")

        rc, out = run(root, "stagnation", {"qi_flow": 0.10, "coherence_score": 0.20, "circulation_pressure": 0.10, "recovery_witness_present": False, "friction": 0.80}, lic())
        if rc != 0 or out.get("recommended_action") != "reopen_flow":
            errors.append("stagnation_action")
        if out.get("cycle_open") is not True:
            errors.append("stagnation_cycle_open")

        rc, out = run(root, "concrete", {"qi_flow": 0.95, "coherence_score": 0.90, "circulation_pressure": 0.80, "critical_blocker_present": True}, lic())
        if rc != 1 or out.get("status") != "QI_CIRCULATION_STABILITY_BLOCKED":
            errors.append("concrete_status")
        if out.get("recommended_action") != "concrete_stop" or out.get("cycle_open") is not False:
            errors.append("concrete_action")

        if len(read_rows(root / "stable" / "qi_circulation_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "stable" / "qi_circulation_receipt.json").get("status") != "QI_CIRCULATION_STABILITY_READY":
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi circulation stability v2.7 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

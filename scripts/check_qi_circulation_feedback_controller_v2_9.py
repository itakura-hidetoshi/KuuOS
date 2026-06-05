#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_circulation_feedback_controller_v2_9.py"


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
    return {"qi_circulation_feedback_enabled": True, "apply_circulation_feedback": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_CIRCULATION_FEEDBACK_LICENSE_READY", "packet_read_allowed": True, "next_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def packet(action: str, qi_flow: float = 0.5, friction: float = 0.2, circulation: float = 0.5, stagnation: float = 0.5) -> dict[str, Any]:
    return {
        "recommended_action": action,
        "circulation_index": circulation,
        "stagnation_index": stagnation,
        "current_qi_packet": {
            "qi_flow": qi_flow,
            "coherence_score": 0.5,
            "circulation_pressure": 0.5,
            "friction": friction,
            "recovery_witness_present": True,
        }
    }


def run(root: pathlib.Path, name: str, p: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_circulation_feedback_packet.json", p)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "next_qi_process_tensor_packet.json")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out, nxt = run(root, "continue", packet("continue_cycle", qi_flow=0.80, friction=0.20, circulation=0.80, stagnation=0.20), lic())
        if rc != 0 or out.get("feedback_action") != "maintain_circulation":
            errors.append("continue_status")
        if nxt.get("qi_flow", 0) <= 0.80:
            errors.append("continue_flow")

        rc, out, nxt = run(root, "rebalance", packet("rebalance_and_continue", qi_flow=0.50, friction=0.40, circulation=0.55, stagnation=0.45), lic())
        if rc != 0 or out.get("feedback_action") != "rebalance_circulation":
            errors.append("rebalance_status")
        if nxt.get("friction", 1) >= 0.40:
            errors.append("rebalance_friction")

        rc, out, nxt = run(root, "reopen", packet("reopen_flow", qi_flow=0.20, friction=0.80, circulation=0.20, stagnation=0.90), lic())
        if rc != 0 or out.get("feedback_action") != "reopen_circulation":
            errors.append("reopen_status")
        if nxt.get("qi_flow", 0) <= 0.20 or nxt.get("friction", 1) >= 0.80:
            errors.append("reopen_packet")

        rc, out, nxt = run(root, "stop", packet("concrete_stop", qi_flow=0.90, friction=0.10, circulation=0.90, stagnation=0.10), lic())
        if rc != 1 or out.get("status") != "QI_CIRCULATION_FEEDBACK_BLOCKED":
            errors.append("stop_status")
        if "concrete_reason_feedback_hold" not in out.get("blockers", []):
            errors.append("stop_blocker")
        if nxt:
            errors.append("stop_next_written")

        if len(read_rows(root / "continue" / "qi_circulation_feedback_audit.jsonl")) != 1:
            errors.append("audit")
        if load_json(root / "continue" / "qi_circulation_feedback_receipt.json").get("status") != "QI_CIRCULATION_FEEDBACK_READY":
            errors.append("receipt")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi circulation feedback controller v2.9 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

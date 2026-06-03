#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cadence_loop_confirmed_baseline_packet_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def cycle() -> dict:
    return {
        "cycle_packet_status": "QI_END_TO_END_CADENCE_CYCLE_PACKET_READY",
        "cycle_packet_id": "qi-cadence-cycle-demo",
        "cycle_root_digest": "cycle-root-demo",
        "cycle_lineage_digest": "cycle-lineage-demo",
        "source_advisory_packet_id": "qi-forecast-advisory-demo",
        "source_forecast_packet_id": "qi-rhythm-forecast-demo",
        "source_ledger_root_digest": "ledger-root-demo",
        "source_last_entry_digest": "last-entry-demo",
        "cadence_cycle_closed": True,
        "receipt_only_cycle_packet": True,
        "lineage_complete": True,
        "no_authority_boundary_preserved": True,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
        "cycle_packet": {
            "lineage": {
                "advisory_packet_id": "qi-forecast-advisory-demo",
                "forecast_packet_id": "qi-rhythm-forecast-demo",
                "ledger_root_digest": "ledger-root-demo",
                "last_entry_digest": "last-entry-demo",
            }
        },
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "baseline_context_id": "qi-cadence-baseline-test-0001",
        "cadence_loop_confirmed_baseline_enabled": True,
        "receipt_only_required": True,
        "confirmed_baseline_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, packet: dict, context: dict) -> tuple[int, dict]:
    cp = root / f"{name}_cycle.json"
    xp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(cp, packet)
    dump(xp, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--cycle", str(cp),
        "--context", str(xp),
        "--write", str(op),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(op)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "ready", cycle(), ctx())
        if rc != 0 or out.get("baseline_packet_status") != "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_READY":
            errors.append("ready_failed")
        if out.get("confirmed_baseline") is not True or out.get("autonomous_qi_cadence_loop_confirmed") is not True:
            errors.append("confirm_flags_failed")
        if out.get("receipt_only_baseline_packet") is not True or out.get("memory_write_performed") is not False:
            errors.append("boundary_failed")
        if not out.get("baseline_root_digest") or not out.get("baseline_packet_id"):
            errors.append("baseline_digest_missing")

        c = cycle()
        c["cadence_cycle_closed"] = False
        rc, out = run(root, "open_cycle", c, ctx())
        if rc != 1 or out.get("baseline_packet_status") != "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_BLOCKED":
            errors.append("open_cycle_not_blocked")

        c = cycle()
        c["memory_write_performed"] = True
        rc, out = run(root, "bad_boundary", c, ctx())
        if rc != 1 or out.get("baseline_packet_status") != "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_BLOCKED":
            errors.append("bad_boundary_not_blocked")

        rc, out = run(root, "ctx_exec", cycle(), ctx({"request_runtime_execution": True}))
        if rc != 1 or out.get("baseline_packet_status") != "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_BLOCKED":
            errors.append("ctx_exec_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi cadence loop confirmed baseline packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

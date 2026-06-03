#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_end_to_end_cadence_cycle_packet_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def packet() -> dict:
    return {
        "integration_status": "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_COMPLETED",
        "advisory_packet_id": "qi-forecast-advisory-demo",
        "source_forecast_packet_id": "qi-rhythm-forecast-demo",
        "source_ledger_root_digest": "ledger-root-demo",
        "source_last_entry_digest": "last-entry-demo",
        "advisory_applied_as_hint": True,
        "advisory_direct_authority": False,
        "live_scheduler_still_decides": True,
        "delegated_adaptive_status": "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED",
        "delegated_cadence_mode": "wide_compressed_window",
        "delegated_recommended_window_ticks": 4,
        "delegated_completed_tick_count": 4,
        "delegated_stop_reason": "window_completed",
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
        "delegated_adaptive_packet": {
            "adaptive_scheduler_status": "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED",
            "delegates_only_to_multi_tick_window_governor": True,
            "memory_write_performed": False,
            "memory_append_performed": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
            "control_packet_mutation_performed": False,
            "probe_execution_performed": False,
            "grants_probe_execution_authority": False,
            "grants_world_update_authority": False,
            "grants_memory_overwrite_authority": False,
        },
    }


def context(extra: dict | None = None) -> dict:
    value = {
        "cycle_context_id": "qi-cycle-test-0001",
        "end_to_end_cadence_cycle_packet_enabled": True,
        "receipt_only_required": True,
        "scheduler_bypass_forbidden": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, p: dict, c: dict) -> tuple[int, dict]:
    ip = root / f"{name}_in.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(ip, p)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--integration", str(ip),
        "--context", str(cp),
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
        rc, out = run(root, "ready", packet(), context())
        if rc != 0 or out.get("cycle_packet_status") != "QI_END_TO_END_CADENCE_CYCLE_PACKET_READY":
            errors.append("ready_failed")
        if out.get("cadence_cycle_closed") is not True or out.get("receipt_only_cycle_packet") is not True:
            errors.append("ready_flags_failed")
        if out.get("scheduler_bypass_performed") is not False or out.get("memory_append_performed") is not False:
            errors.append("ready_boundary_failed")
        if not out.get("cycle_root_digest") or not out.get("cycle_lineage_digest"):
            errors.append("digest_missing")

        rc, out = run(root, "ctx_block", packet(), context({"request_scheduler_execution": True}))
        if rc != 1 or out.get("cycle_packet_status") != "QI_END_TO_END_CADENCE_CYCLE_PACKET_BLOCKED":
            errors.append("ctx_block_failed")

        p = packet()
        p["advisory_direct_authority"] = True
        rc, out = run(root, "source_block", p, context())
        if rc != 1 or out.get("cycle_packet_status") != "QI_END_TO_END_CADENCE_CYCLE_PACKET_BLOCKED":
            errors.append("source_block_failed")

        p = packet()
        p.pop("delegated_adaptive_packet")
        rc, out = run(root, "missing", p, context())
        if rc != 1 or out.get("cycle_packet_status") != "QI_END_TO_END_CADENCE_CYCLE_PACKET_BLOCKED":
            errors.append("missing_delegate_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi end-to-end cadence cycle packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

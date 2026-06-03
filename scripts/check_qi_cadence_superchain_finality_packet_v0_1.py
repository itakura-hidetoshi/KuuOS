#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cadence_superchain_finality_packet_v0_1.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def baseline() -> dict:
    return {
        "baseline_packet_status": "QI_CADENCE_LOOP_CONFIRMED_BASELINE_PACKET_READY",
        "baseline_packet_id": "qi-cadence-baseline-demo",
        "baseline_root_digest": "baseline-root-demo",
        "source_cycle_packet_id": "qi-cadence-cycle-demo",
        "source_cycle_root_digest": "cycle-root-demo",
        "source_cycle_lineage_digest": "cycle-lineage-demo",
        "confirmed_baseline": True,
        "autonomous_qi_cadence_loop_confirmed": True,
        "receipt_only_baseline_packet": True,
        "cycle_lineage_preserved": True,
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
    }


def context(extra: dict | None = None) -> dict:
    value = {
        "finality_context_id": "qi-finality-test-0001",
        "cadence_superchain_finality_enabled": True,
        "receipt_only_required": True,
        "finality_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, b: dict, c: dict) -> tuple[int, dict]:
    bp = root / f"{name}_baseline.json"
    cp = root / f"{name}_context.json"
    op = root / f"{name}_out.json"
    dump(bp, b)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--baseline", str(bp),
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
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, out = run(root, "ready", baseline(), context())
        if rc != 0 or out.get("finality_packet_status") != "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY":
            errors.append("ready_failed")
        if out.get("finality_confirmed") is not True or out.get("receipt_only_finality_packet") is not True:
            errors.append("ready_flags_failed")
        if out.get("scheduler_bypass_performed") is not False or out.get("memory_write_performed") is not False:
            errors.append("ready_boundary_failed")

        b = baseline()
        b["memory_write_performed"] = True
        rc, out = run(root, "bad_source", b, context())
        if rc != 1 or out.get("finality_packet_status") != "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_BLOCKED":
            errors.append("bad_source_failed")

        rc, out = run(root, "bad_context", baseline(), context({"request_runtime_execution": True}))
        if rc != 1 or out.get("finality_packet_status") != "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_BLOCKED":
            errors.append("bad_context_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi cadence superchain finality packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

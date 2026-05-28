#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_memoryos_process_tensor_retrieval_replay_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


ENTRY = {
    "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
    "source_probe_type": "observation_debt_probe",
    "append_only": True,
    "memory_append_performed": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "lineage_preserved": True,
}

CTX = {
    "request_memory_write": False,
    "request_memory_overwrite": False,
    "request_world_update": False,
    "request_scheduler_mutation": False,
    "request_probe_execution": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        memory = root / "memory.json"
        ctx = root / "ctx.json"
        out = root / "replay.json"
        dump(memory, {"entries": [ENTRY]})
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--context", str(ctx), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("replay_output_missing")
        else:
            value = load(out)
            if value.get("replay_status") != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY":
                errors.append("replay_status_mismatch")
            if value.get("memory_read_performed") is not True:
                errors.append("memory_read_performed_not_true")
            if value.get("retrieval_only") is not True:
                errors.append("retrieval_only_not_true")
            if value.get("replay_surface_only") is not True:
                errors.append("replay_surface_only_not_true")
            if value.get("dominant_probe_type") != "observation_debt_probe":
                errors.append("dominant_probe_type_mismatch")
            for key in [
                "process_tensor_trace_available",
                "nonmarkov_trace_available",
                "observation_debt_trace_available",
                "recoverability_trace_available",
                "safe_reentry_trace_available",
                "lineage_available",
            ]:
                if value.get(key) is not True:
                    errors.append(f"{key}_not_true")
            for key in [
                "memory_write_performed",
                "memory_append_performed",
                "memory_overwrite_performed",
                "memory_delete_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "scheduler_state_mutation_performed",
                "grants_memory_write_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
                "grants_scheduler_authority",
                "grants_probe_execution_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_world_update"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--memory", str(memory), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("replay_status") != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_BLOCKED":
                errors.append("blocked_replay_status_mismatch")
            if "request_world_update" not in value.get("replay_blockers", []):
                errors.append("world_update_blocker_missing")
            if value.get("world_update_performed") is not False:
                errors.append("blocked_world_update_performed_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi MemoryOS process tensor retrieval replay check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

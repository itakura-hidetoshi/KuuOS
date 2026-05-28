#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_memoryos_process_tensor_append_writeback_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


PROBE_RESULT = {
    "execution_status": "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED",
    "probe_type": "observation_debt_probe",
    "probe_result_summary": "observation debt probe result artifact only",
    "probe_execution_performed": True,
    "probe_result_artifact_only": True,
    "one_shot_token_consumed": True,
    "token_reuse_allowed": False,
    "grants_probe_execution_authority": False,
    "grants_execution_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "grants_control_packet_authority": False,
    "grants_scheduler_authority": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "scheduler_state_mutation_performed": False,
}

CTX = {
    "memory_entry_kind": "qi_process_tensor_probe_result_memory_entry",
    "memory_entry_summary": "append process tensor probe result to MemoryOS",
    "memoryos_target_stream": "memoryos/qi_process_tensor/append_only",
    "append_only_required": True,
    "lineage_preserved": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "no_memory_overwrite": True,
    "no_world_update": True,
    "no_control_packet_mutation": True,
    "request_memory_overwrite": False,
    "request_memory_delete": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        probe = root / "probe.json"
        ctx = root / "ctx.json"
        out = root / "writeback.json"
        dump(probe, PROBE_RESULT)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--probe-result", str(probe), "--context", str(ctx), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("writeback_output_missing")
        else:
            value = load(out)
            if value.get("writeback_status") != "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED":
                errors.append("writeback_status_mismatch")
            if value.get("memory_append_performed") is not True:
                errors.append("memory_append_performed_not_true")
            if value.get("memory_write_performed") is not True:
                errors.append("memory_write_performed_not_true")
            for key in [
                "process_tensor_trace_preserved",
                "nonmarkov_trace_preserved",
                "observation_debt_trace_preserved",
                "recoverability_trace_preserved",
                "safe_reentry_trace_preserved",
                "lineage_preserved",
                "append_only",
            ]:
                if value.get(key) is not True:
                    errors.append(f"{key}_not_true")
            for key in [
                "memory_overwrite_performed",
                "memory_delete_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "scheduler_state_mutation_performed",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
                "grants_probe_execution_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_memory_overwrite"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--probe-result", str(probe), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("writeback_status") != "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_BLOCKED":
                errors.append("blocked_writeback_status_mismatch")
            if "request_memory_overwrite" not in value.get("writeback_blockers", []):
                errors.append("memory_overwrite_blocker_missing")
            if value.get("memory_append_performed") is not False:
                errors.append("blocked_memory_append_performed_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi MemoryOS process tensor append writeback check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

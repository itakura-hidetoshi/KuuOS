#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_append_only_rhythm_receipt_ledger_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_jsonl(path: pathlib.Path):
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rhythm_packet(kind: str = "stable") -> dict:
    stop = "window_completed"
    if kind == "observe":
        stop = "process_tensor_observe_required"
    return {
        "rhythm_layer_status": "QI_RHYTHM_MEMORY_CADENCE_HISTORY_LAYER_COMPLETED",
        "rhythm_layer_version": "kuuos_runtime_daemon_qi_rhythm_memory_cadence_history_layer_v0_1",
        "rhythm_history_projection_only": True,
        "rhythm_layer_grants_no_new_authority": True,
        "rhythm_bias": "expand_if_low_pressure" if kind == "stable" else "observe_sensitive",
        "rhythm_mode": "stable_expansion" if kind == "stable" else "observation_guarded",
        "rhythm_stability_score": 0.88 if kind == "stable" else 0.42,
        "recent_pressure_mean": 0.15 if kind == "stable" else 0.55,
        "delegated_cadence_mode": "wide_compressed_window" if kind == "stable" else "observe_first_single_tick",
        "delegated_recommended_window_ticks": 4 if kind == "stable" else 1,
        "delegated_completed_tick_count": 4 if kind == "stable" else 0,
        "delegated_stop_reason": stop,
        "rhythm_entry_candidate": {
            "entry_kind": "rhythm_cadence_history_candidate",
            "projection_only": True,
            "rhythm_mode": "stable_expansion" if kind == "stable" else "observation_guarded",
            "rhythm_bias": "expand_if_low_pressure" if kind == "stable" else "observe_sensitive",
            "process_tensor_pressure_score": 0.15 if kind == "stable" else 0.55,
            "recommended_window_ticks": 4 if kind == "stable" else 1,
            "delegated_completed_tick_count": 4 if kind == "stable" else 0,
            "delegated_stop_reason": stop,
            "cadence_mode": "wide_compressed_window" if kind == "stable" else "observe_first_single_tick",
            "memory_write_performed": False,
            "memory_append_performed": False,
            "world_update_performed": False,
            "probe_execution_performed": False,
        },
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "append_only_rhythm_ledger_enabled": True,
        "jsonl_backend_required": True,
        "append_only_required": True,
        "append_receipt": True,
    }
    if extra:
        value.update(extra)
    return value


def run_case(root: pathlib.Path, name: str, packet: dict, context: dict, ledger: pathlib.Path) -> tuple[int, dict]:
    packet_path = root / f"{name}_rhythm.json"
    ctx_path = root / f"{name}_ctx.json"
    out_path = root / f"{name}_out.json"
    dump(packet_path, packet)
    dump(ctx_path, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--rhythm-layer", str(packet_path),
        "--ledger", str(ledger),
        "--context", str(ctx_path),
        "--write", str(out_path),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(out_path)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        ledger = root / "rhythm_receipts.jsonl"

        rc, out1 = run_case(root, "first", rhythm_packet("stable"), ctx(), ledger)
        if rc != 0 or out1.get("ledger_status") != "QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_APPENDED":
            errors.append("first_append_failed")
        if out1.get("ledger_append_performed") is not True or out1.get("memory_append_performed") is not False:
            errors.append("first_append_boundary_failed")
        if len(read_jsonl(ledger)) != 1:
            errors.append("first_ledger_count_failed")

        rc, out2 = run_case(root, "second", rhythm_packet("observe"), ctx(), ledger)
        if rc != 0 or out2.get("prior_entry_count") != 1 or out2.get("final_entry_count") != 2:
            errors.append("second_append_count_failed")
        if out2.get("prev_entry_digest") != out1.get("entry_digest"):
            errors.append("prev_digest_chain_failed")
        lines = read_jsonl(ledger)
        if len(lines) != 2 or lines[1].get("prev_entry_digest") != lines[0].get("entry_digest"):
            errors.append("jsonl_digest_chain_failed")

        bad_context = ctx({"destructive_rewrite_requested": True})
        rc, out3 = run_case(root, "rewrite", rhythm_packet("stable"), bad_context, ledger)
        if rc != 1 or out3.get("ledger_status") != "QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_BLOCKED":
            errors.append("destructive_rewrite_not_blocked")
        if len(read_jsonl(ledger)) != 2:
            errors.append("blocked_rewrite_mutated_ledger")

        bad_context = ctx({"request_memory_append": True})
        rc, out4 = run_case(root, "memory_append", rhythm_packet("stable"), bad_context, ledger)
        if rc != 1 or out4.get("ledger_status") != "QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_BLOCKED":
            errors.append("memory_append_request_not_blocked")
        if len(read_jsonl(ledger)) != 2:
            errors.append("blocked_memory_append_mutated_ledger")

        bad_packet = rhythm_packet("stable")
        bad_packet["rhythm_history_projection_only"] = False
        rc, out5 = run_case(root, "bad_source", bad_packet, ctx(), ledger)
        if rc != 1 or out5.get("ledger_status") != "QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_BLOCKED":
            errors.append("bad_source_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi append-only rhythm receipt ledger check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_execution_intent_audit_ledger_v0_1.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_jsonl(path: pathlib.Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def engine(action: str, reason: str, staged: bool) -> dict:
    mode = "staged_intent_only" if staged else "nonexecuting_receipt"
    return {
        "engine_status": "QI_AUTONOMOUS_EXECUTION_ENGINE_READY",
        "engine_packet_id": f"qi-exec-engine-{action}-{reason}",
        "selected_action": action,
        "execution_mode": mode,
        "execution_intent_staged": staged,
        "execution_committed": False,
        "selected_reason": reason,
        "process_tensor_guard_passed": True,
        "decisionos_guard_passed": True,
        "cbf_guard_passed": True,
        "token_guard_passed": True,
        "authority_guard_passed": staged,
        "recovery_guard_passed": True,
        "nonmarkov_guard_passed": True,
        "receipt_only": True,
        "read_only": True,
        "projection_only": True,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "handover_performed": False,
        "ledger_append_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
        "execution_intent_packet": {
            "engine_packet_id": f"qi-exec-engine-{action}-{reason}",
            "selected_action": action,
            "execution_mode": mode,
            "execution_intent_staged": staged,
            "execution_committed": False,
            "receipt_only": True,
            "read_only": True,
            "projection_only": True,
            "runtime_control_performed": False,
            "scheduler_bypass_performed": False,
            "notification_sent": False,
            "ticket_created": False,
            "handover_performed": False,
            "ledger_append_performed": False,
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


def ctx(extra: dict | None = None) -> dict:
    value = {
        "execution_intent_audit_ledger_enabled": True,
        "append_only_required": True,
        "intent_receipt_only_required": True,
        "jsonl_backend_required": True,
        "append_receipt": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, packet: dict, context: dict, ledger: pathlib.Path) -> tuple[int, dict]:
    ep = root / f"{name}_engine.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(ep, packet)
    dump(cp, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--engine", str(ep),
        "--ledger", str(ledger),
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
        ledger = root / "execution_audit.jsonl"

        rc, out1 = run(root, "staged", engine("advance_tick", "staged_execution_intent_ready", True), ctx(), ledger)
        if rc != 0 or out1.get("ledger_status") != "QI_EXECUTION_INTENT_AUDIT_LEDGER_APPENDED":
            errors.append("staged_append_failed")
        if out1.get("execution_intent_staged") is not True or out1.get("execution_committed") is not False:
            errors.append("staged_boundary_failed")
        if len(read_jsonl(ledger)) != 1:
            errors.append("first_count_failed")

        rc, out2 = run(root, "hold", engine("hold", "authority_guard_failed", False), ctx(), ledger)
        if rc != 0 or out2.get("prior_entry_count") != 1 or out2.get("final_entry_count") != 2:
            errors.append("hold_append_failed")
        if out2.get("prev_entry_digest") != out1.get("entry_digest"):
            errors.append("digest_chain_failed")
        if out2.get("selected_action") != "hold" or out2.get("execution_committed") is not False:
            errors.append("hold_boundary_failed")

        bad = engine("advance_tick", "bad", True)
        bad["execution_committed"] = True
        rc, out3 = run(root, "bad", bad, ctx(), ledger)
        if rc != 1 or out3.get("ledger_status") != "QI_EXECUTION_INTENT_AUDIT_LEDGER_BLOCKED":
            errors.append("bad_engine_not_blocked")
        if len(read_jsonl(ledger)) != 2:
            errors.append("blocked_mutated_ledger")

        rc, out4 = run(root, "runtime", engine("hold", "safe_default_hold", False), ctx({"request_runtime_control": True}), ledger)
        if rc != 1 or out4.get("ledger_status") != "QI_EXECUTION_INTENT_AUDIT_LEDGER_BLOCKED":
            errors.append("runtime_request_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi execution intent audit ledger check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

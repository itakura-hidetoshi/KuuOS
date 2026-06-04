#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_execution_audit_trend_summary_v0_1.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: pathlib.Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def row(idx: int, action: str, staged: bool, authority: bool = True, cbf: bool = True, pt: bool = True) -> dict:
    value = {
        "execution_audit_receipt_id": f"qi-exec-audit-{idx}",
        "entry_digest": f"digest-{idx}",
        "selected_action": action,
        "execution_mode": "staged_intent_only" if staged else "nonexecuting_receipt",
        "execution_intent_staged": staged,
        "execution_committed": False,
        "selected_reason": "staged_execution_intent_ready" if staged else "safe_default_hold",
        "process_tensor_guard_passed": pt,
        "decisionos_guard_passed": True,
        "cbf_guard_passed": cbf,
        "token_guard_passed": True,
        "authority_guard_passed": authority,
        "recovery_guard_passed": True,
        "nonmarkov_guard_passed": True,
        "append_only": True,
        "intent_receipt_only": True,
        "read_only_receipt": True,
        "projection_only_receipt": True,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "handover_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    }
    if idx > 1:
        value["prev_entry_digest"] = f"digest-{idx-1}"
    return value


def ctx(extra: dict | None = None) -> dict:
    value = {
        "execution_audit_trend_summary_enabled": True,
        "read_only_summary_required": True,
        "projection_only_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, rows: list[dict], c: dict) -> tuple[int, dict]:
    ledger = root / f"{name}.jsonl"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    write_jsonl(ledger, rows)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
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
        rc, out = run(root, "stable", [row(1, "advance_tick", True, True), row(2, "hold", False, False)], ctx())
        if rc != 0 or out.get("trend_status") != "QI_EXECUTION_AUDIT_TREND_SUMMARY_READY":
            errors.append("stable_ready_failed")
        if out.get("committed_execution_count") != 0 or out.get("review_recommended") is not False:
            errors.append("stable_review_failed")
        if out.get("ledger_append_performed") is not False or out.get("runtime_control_performed") is not False:
            errors.append("stable_boundary_failed")

        rc, out = run(root, "falling", [row(1, "advance_tick", True, True), row(2, "advance_tick", True, False, cbf=False), row(3, "advance_tick", True, False, cbf=False, pt=False)], ctx())
        if rc != 0 or out.get("review_recommended") is not True:
            errors.append("falling_review_failed")
        if "cbf_guard_pass_rate_low" not in out.get("review_reasons", []):
            errors.append("cbf_reason_missing")

        bad = row(1, "advance_tick", True, True)
        bad["execution_committed"] = True
        rc, out = run(root, "bad_entry", [bad], ctx())
        if rc != 1 or out.get("trend_status") != "QI_EXECUTION_AUDIT_TREND_SUMMARY_BLOCKED":
            errors.append("committed_entry_not_blocked")

        rc, out = run(root, "request", [row(1, "hold", False, False)], ctx({"request_runtime_control": True}))
        if rc != 1 or out.get("trend_status") != "QI_EXECUTION_AUDIT_TREND_SUMMARY_BLOCKED":
            errors.append("runtime_request_not_blocked")

        rc, out = run(root, "empty", [], ctx())
        if rc != 1 or out.get("trend_status") != "QI_EXECUTION_AUDIT_TREND_SUMMARY_BLOCKED":
            errors.append("empty_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi execution audit trend summary check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

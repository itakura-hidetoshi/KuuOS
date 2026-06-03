#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_observability_audit_trend_summary_v0_2.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: pathlib.Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def row(idx: int, severity: str, count: int) -> dict:
    value = {
        "audit_receipt_id": f"qi-audit-{idx}",
        "entry_digest": f"digest-{idx}",
        "alert_severity": severity,
        "alert_count": count,
        "alert_reasons": [] if count == 0 else ["review_required"],
        "append_only": True,
        "read_only_review_receipt": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
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
        "audit_trend_summary_enabled": True,
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
        rc, out = run(root, "excellent", [row(1, "none", 0), row(2, "none", 0)], ctx())
        if rc != 0 or out.get("trend_status") != "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_READY":
            errors.append("excellent_ready_failed")
        if out.get("reliability_class") != "excellent" or out.get("review_recommended") is not False:
            errors.append("excellent_score_failed")
        if out.get("ledger_append_performed") is not False or out.get("projection_only") is not True:
            errors.append("excellent_boundary_failed")

        rc, out = run(root, "falling", [row(1, "none", 0), row(2, "medium", 1), row(3, "critical", 2)], ctx())
        if rc != 0 or out.get("review_recommended") is not True:
            errors.append("falling_review_failed")
        if "critical_alert_seen" not in out.get("review_reasons", []):
            errors.append("critical_reason_missing")

        rc, out = run(root, "blocked_request", [row(1, "none", 0)], ctx({"request_ledger_append": True}))
        if rc != 1 or out.get("trend_status") != "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_BLOCKED":
            errors.append("append_request_not_blocked")

        rc, out = run(root, "empty", [], ctx())
        if rc != 1 or out.get("trend_status") != "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_BLOCKED":
            errors.append("empty_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi observability audit trend summary check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

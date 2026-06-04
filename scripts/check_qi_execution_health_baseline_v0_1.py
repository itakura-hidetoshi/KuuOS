#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_execution_health_baseline_v0_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def trend(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "trend_version": "kuuos_runtime_daemon_qi_execution_audit_trend_summary_v0_1",
        "trend_status": "QI_EXECUTION_AUDIT_TREND_SUMMARY_READY",
        "trend_packet_id": "qi-exec-trend-demo",
        "audit_entry_count": 2,
        "audit_root_digest": "audit-root-demo",
        "last_entry_digest": "entry-2",
        "staged_intent_count": 1,
        "safe_fallback_count": 1,
        "committed_execution_count": 0,
        "mean_autonomy_reliability_score": 0.91,
        "autonomy_reliability_class": "stable",
        "autonomy_trend": "autonomy_reliability_flat",
        "review_recommended": False,
        "review_reasons": [],
        "read_only_summary": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "execution_committed": False,
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
    if extra:
        value.update(extra)
    return value


def ctx(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "execution_health_baseline_enabled": True,
        "read_only_baseline_required": True,
        "projection_only_required": True,
        "reliability_threshold": 0.80,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, trend_packet: dict[str, Any], c: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    tp = root / f"{name}_trend.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(tp, trend_packet)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--trend", str(tp),
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

        rc, out = run(root, "ready", trend(), ctx())
        if rc != 0 or out.get("health_status") != "QI_EXECUTION_HEALTH_BASELINE_READY":
            errors.append("ready_baseline_failed")
        if out.get("confirmed_autonomy") is not True or not out.get("confirmed_autonomy_packet"):
            errors.append("confirmed_autonomy_packet_missing")
        if out.get("execution_committed") is not False or out.get("runtime_control_performed") is not False:
            errors.append("ready_boundary_failed")
        cap = out.get("confirmed_autonomy_packet", {})
        if cap.get("execution_authority_granted") is not False or cap.get("execution_commit_allowed") is not False:
            errors.append("confirmed_packet_authority_boundary_failed")

        rc, out = run(root, "low_score", trend({"mean_autonomy_reliability_score": 0.70}), ctx())
        if rc != 1 or out.get("health_status") != "QI_EXECUTION_HEALTH_BASELINE_BLOCKED":
            errors.append("low_score_not_blocked")
        if "mean_autonomy_reliability_score_below_threshold" not in out.get("health_blockers", []):
            errors.append("low_score_blocker_missing")

        rc, out = run(root, "committed", trend({"committed_execution_count": 1}), ctx())
        if rc != 1 or out.get("health_status") != "QI_EXECUTION_HEALTH_BASELINE_BLOCKED":
            errors.append("committed_count_not_blocked")

        rc, out = run(root, "review", trend({"review_recommended": True, "review_reasons": ["cbf_guard_pass_rate_low"]}), ctx())
        if rc != 1 or "review_recommended_without_explicit_allowance" not in out.get("health_blockers", []):
            errors.append("review_recommended_not_blocked")

        rc, out = run(root, "allowed_review", trend({"review_recommended": True, "review_reasons": ["cbf_guard_pass_rate_low"]}), ctx({"allow_review_recommended": True}))
        if rc != 0 or out.get("health_status") != "QI_EXECUTION_HEALTH_BASELINE_READY":
            errors.append("allowed_review_record_failed")
        if out.get("confirmed_autonomy_packet", {}).get("execution_authority_granted") is not False:
            errors.append("allowed_review_authority_boundary_failed")

        rc, out = run(root, "runtime_request", trend(), ctx({"request_runtime_control": True}))
        if rc != 1 or "request_runtime_control_not_allowed" not in out.get("health_blockers", []):
            errors.append("runtime_request_not_blocked")

        rc, out = run(root, "bad_trend_boundary", trend({"runtime_control_performed": True}), ctx())
        if rc != 1 or "trend_runtime_control_performed_not_false" not in out.get("health_blockers", []):
            errors.append("bad_trend_boundary_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi execution health baseline check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_observability_health_baseline_packet_v0_2.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def trend(score: float = 0.98, cls: str = "excellent", review: bool = False) -> dict:
    return {
        "trend_status": "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_READY",
        "trend_packet_id": "qi-audit-trend-demo",
        "audit_root_digest": "audit-root-demo",
        "last_entry_digest": "audit-last-demo",
        "mean_reliability_score": score,
        "reliability_class": cls,
        "reliability_trend": "reliability_flat",
        "review_recommended": review,
        "review_reasons": ["review_required"] if review else [],
        "read_only_summary": True,
        "projection_only": True,
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
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "health_context_id": "qi-observe-health-test-0001",
        "observability_health_baseline_enabled": True,
        "confirmed_observability_required": True,
        "receipt_only_required": True,
        "read_only_required": True,
        "min_confirmed_reliability_score": 0.75,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, t: dict, c: dict) -> tuple[int, dict]:
    tp = root / f"{name}_trend.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(tp, t)
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
        if rc != 0 or out.get("health_baseline_status") != "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_READY":
            errors.append("ready_failed")
        if out.get("observability_health_confirmed") is not True or out.get("confirmed_observability_packet") is not True:
            errors.append("confirm_flags_failed")
        if out.get("ledger_append_performed") is not False or out.get("runtime_control_authority") is not False:
            errors.append("boundary_failed")
        if not out.get("health_baseline_root_digest") or not out.get("health_baseline_packet_id"):
            errors.append("digest_missing")

        rc, out = run(root, "low", trend(0.40, "review_required", True), ctx())
        if rc != 1 or out.get("health_baseline_status") != "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_BLOCKED":
            errors.append("low_not_blocked")

        rc, out = run(root, "review", trend(0.90, "stable", True), ctx())
        if rc != 1 or out.get("health_baseline_status") != "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_BLOCKED":
            errors.append("review_not_blocked")

        rc, out = run(root, "exec", trend(), ctx({"request_runtime_control": True}))
        if rc != 1 or out.get("health_baseline_status") != "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_BLOCKED":
            errors.append("runtime_control_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi observability health baseline packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

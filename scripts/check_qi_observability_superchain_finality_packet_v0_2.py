#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_observability_superchain_finality_packet_v0_2.py"
CHAIN = [
    "qi_cadence_observability_projection",
    "qi_cadence_alert_policy",
    "qi_incident_review_audit_ledger",
    "qi_observability_audit_trend_summary",
    "qi_observability_health_baseline_packet",
]


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def health() -> dict:
    return {
        "health_baseline_status": "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_READY",
        "health_baseline_packet_id": "qi-observe-health-demo",
        "health_baseline_root_digest": "health-root-demo",
        "source_trend_packet_id": "qi-audit-trend-demo",
        "source_audit_root_digest": "audit-root-demo",
        "source_last_entry_digest": "audit-last-demo",
        "mean_reliability_score": 0.98,
        "reliability_class": "excellent",
        "observability_health_confirmed": True,
        "confirmed_observability_packet": True,
        "receipt_only_health_baseline": True,
        "read_only_health_baseline": True,
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
        "finality_context_id": "qi-observe-finality-test-0001",
        "observability_superchain_finality_enabled": True,
        "receipt_only_required": True,
        "read_only_required": True,
        "projection_only_required": True,
        "observability_chain": CHAIN,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, h: dict, c: dict) -> tuple[int, dict]:
    hp = root / f"{name}_health.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(hp, h)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--health", str(hp),
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
        rc, out = run(root, "ready", health(), ctx())
        if rc != 0 or out.get("finality_status") != "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_READY":
            errors.append("ready_failed")
        if out.get("observability_finality_confirmed") is not True or out.get("observability_chain_complete") is not True:
            errors.append("ready_flags_failed")
        if out.get("ledger_append_performed") is not False or out.get("runtime_control_authority") is not False:
            errors.append("ready_boundary_failed")
        if not out.get("finality_root_digest") or not out.get("finality_packet_id"):
            errors.append("digest_missing")

        rc, out = run(root, "short_chain", health(), ctx({"observability_chain": CHAIN[:-1]}))
        if rc != 1 or out.get("finality_status") != "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_BLOCKED":
            errors.append("short_chain_not_blocked")

        h = health()
        h["health_baseline_status"] = "NOT_READY"
        rc, out = run(root, "bad_health", h, ctx())
        if rc != 1 or out.get("finality_status") != "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_BLOCKED":
            errors.append("bad_health_not_blocked")

        rc, out = run(root, "runtime", health(), ctx({"request_runtime_control": True}))
        if rc != 1 or out.get("finality_status") != "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_BLOCKED":
            errors.append("runtime_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi observability superchain finality packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

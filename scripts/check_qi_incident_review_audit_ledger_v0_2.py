#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_incident_review_audit_ledger_v0_2.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_jsonl(path: pathlib.Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def alert(name: str = "clean") -> dict:
    sev = "none" if name == "clean" else "medium"
    reasons = [] if name == "clean" else ["review_required"]
    return {
        "alert_policy_status": "QI_CADENCE_ALERT_POLICY_READY",
        "alert_packet_id": f"qi-cadence-alert-{name}",
        "source_metrics_packet_id": "qi-cadence-metrics-demo",
        "source_finality_packet_id": "qi-cadence-finality-demo",
        "alert_severity": sev,
        "alert_count": len(reasons),
        "alert_reasons": reasons,
        "read_only_incident_surface": True,
        "alert_policy_projection_only": True,
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
        "incident_surface": {
            "surface_kind": "qi_cadence_read_only_incident_surface_v0_2",
            "alert_packet_id": f"qi-cadence-alert-{name}",
            "severity": sev,
            "reasons": reasons,
            "projection_only": True,
            "notification_sent": False,
            "ticket_created": False,
            "runtime_control_authority": False,
            "memory_write_performed": False,
            "memory_append_performed": False,
            "world_update_performed": False,
            "probe_execution_performed": False,
        },
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "incident_review_audit_ledger_enabled": True,
        "append_only_required": True,
        "read_only_review_required": True,
        "jsonl_backend_required": True,
        "append_receipt": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, packet: dict, context: dict, ledger: pathlib.Path) -> tuple[int, dict]:
    ap = root / f"{name}_alert.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(ap, packet)
    dump(cp, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--alert-policy", str(ap),
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
        ledger = root / "incident_audit.jsonl"

        rc, out1 = run(root, "first", alert("clean"), ctx(), ledger)
        if rc != 0 or out1.get("ledger_status") != "QI_INCIDENT_REVIEW_AUDIT_LEDGER_APPENDED":
            errors.append("first_append_failed")
        if out1.get("ledger_append_performed") is not True or out1.get("notification_sent") is not False:
            errors.append("first_boundary_failed")
        if len(read_jsonl(ledger)) != 1:
            errors.append("first_count_failed")

        rc, out2 = run(root, "second", alert("review"), ctx(), ledger)
        if rc != 0 or out2.get("prior_entry_count") != 1 or out2.get("final_entry_count") != 2:
            errors.append("second_count_failed")
        if out2.get("prev_entry_digest") != out1.get("entry_digest"):
            errors.append("digest_chain_failed")

        rc, out3 = run(root, "notify", alert("clean"), ctx({"request_notification_send": True}), ledger)
        if rc != 1 or out3.get("ledger_status") != "QI_INCIDENT_REVIEW_AUDIT_LEDGER_BLOCKED":
            errors.append("notify_not_blocked")
        if len(read_jsonl(ledger)) != 2:
            errors.append("blocked_mutated_ledger")

        bad = alert("clean")
        bad["alert_policy_status"] = "NOT_READY"
        rc, out4 = run(root, "bad", bad, ctx(), ledger)
        if rc != 1 or out4.get("ledger_status") != "QI_INCIDENT_REVIEW_AUDIT_LEDGER_BLOCKED":
            errors.append("bad_alert_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi incident review audit ledger check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

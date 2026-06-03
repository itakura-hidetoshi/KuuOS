#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cadence_alert_policy_v0_2.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def obs() -> dict:
    return {
        "observability_status": "QI_CADENCE_OBSERVABILITY_PROJECTION_READY",
        "metrics_packet_id": "qi-cadence-metrics-demo",
        "source_finality_packet_id": "qi-cadence-finality-demo",
        "projection_only": True,
        "dashboard_projection_only": True,
        "runtime_control_authority": False,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "finality_confirmed_gauge": 1,
        "canonical_chain_complete_gauge": 1,
        "no_authority_boundary_gauge": 1,
        "scheduler_bypass_gauge": 0,
        "memory_write_gauge": 0,
        "memory_append_gauge": 0,
        "world_update_gauge": 0,
        "probe_execution_gauge": 0,
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "cadence_alert_policy_enabled": True,
        "read_only_incident_surface_required": True,
        "projection_only_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, o: dict, c: dict) -> tuple[int, dict, dict]:
    op = root / f"{name}_obs.json"
    cp = root / f"{name}_ctx.json"
    rp = root / f"{name}_result.json"
    ip = root / f"{name}_incident.json"
    dump(op, o)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--observability", str(op),
        "--context", str(cp),
        "--write", str(rp),
        "--write-incident", str(ip),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(rp), load(ip)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, out, incident = run(root, "clean", obs(), ctx())
        if rc != 0 or out.get("alert_policy_status") != "QI_CADENCE_ALERT_POLICY_READY":
            errors.append("clean_failed")
        if out.get("alert_severity") != "none" or out.get("alert_count") != 0:
            errors.append("clean_alert_failed")
        if out.get("notification_sent") is not False or out.get("ticket_created") is not False:
            errors.append("clean_boundary_failed")
        if incident.get("projection_only") is not True or incident.get("runtime_control_authority") is not False:
            errors.append("incident_boundary_failed")

        o = obs()
        o["scheduler_bypass_gauge"] = 1
        rc, out, incident = run(root, "critical", o, ctx())
        if rc != 0 or out.get("alert_severity") != "critical":
            errors.append("critical_failed")
        if "scheduler_bypass_detected" not in out.get("alert_reasons", []):
            errors.append("critical_reason_missing")

        rc, out, incident = run(root, "notify", obs(), ctx({"request_notification_send": True}))
        if rc != 1 or out.get("alert_policy_status") != "QI_CADENCE_ALERT_POLICY_BLOCKED":
            errors.append("notify_not_blocked")

        o = obs()
        o["observability_status"] = "NOT_READY"
        rc, out, incident = run(root, "bad_obs", o, ctx())
        if rc != 1 or out.get("alert_policy_status") != "QI_CADENCE_ALERT_POLICY_BLOCKED":
            errors.append("bad_obs_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi cadence alert policy check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_execution_health_packet_chain_v0_1.py"

FORBIDDEN_FALSE = [
    "execution_authority_granted",
    "execution_commit_allowed",
    "runtime_control_allowed",
    "scheduler_bypass_allowed",
    "ledger_append_allowed",
    "memory_write_allowed",
    "world_update_allowed",
    "probe_execution_allowed",
    "execution_committed",
    "runtime_control_performed",
    "scheduler_bypass_performed",
    "ledger_append_performed",
    "memory_write_performed",
    "world_update_performed",
    "probe_execution_performed",
]


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def health(extra: dict[str, Any] | None = None, confirmed_extra: dict[str, Any] | None = None) -> dict[str, Any]:
    confirmed: dict[str, Any] = {
        "confirmed_autonomy_packet_id": "qi-confirmed-autonomy-demo",
        "source_health_baseline_packet_id": "qi-exec-health-demo",
        "autonomy_health_root_digest": "health-root-demo",
        "confirmed_autonomy_status": "CONFIRMED_AUTONOMY_HEALTH_BASELINE_READY",
        "confirmed_autonomy_scope": "read_only_health_baseline_not_execution_authority",
        "execution_authority_granted": False,
        "execution_commit_allowed": False,
        "runtime_control_allowed": False,
        "scheduler_bypass_allowed": False,
        "ledger_append_allowed": False,
        "memory_write_allowed": False,
        "world_update_allowed": False,
        "probe_execution_allowed": False,
        "read_only_baseline": True,
        "projection_only": True,
    }
    if confirmed_extra:
        confirmed.update(confirmed_extra)
    value: dict[str, Any] = {
        "health_version": "kuuos_runtime_daemon_qi_execution_health_baseline_v0_1",
        "health_status": "QI_EXECUTION_HEALTH_BASELINE_READY",
        "health_baseline_packet_id": "qi-exec-health-demo",
        "confirmed_autonomy_packet_id": "qi-confirmed-autonomy-demo",
        "autonomy_health_root_digest": "health-root-demo",
        "confirmed_autonomy": True,
        "confirmed_autonomy_scope": "read_only_health_baseline_not_execution_authority",
        "confirmed_autonomy_packet": confirmed,
        "read_only_baseline": True,
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
        "execution_health_packet_chain_enabled": True,
        "read_only_chain_required": True,
        "projection_only_required": True,
        "additive_only_required": True,
        "tighten_only_required": True,
        "same_root_required": True,
        "expected_autonomy_health_root_digest": "health-root-demo",
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, health_packet: dict[str, Any], c: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    hp = root / f"{name}_health.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(hp, health_packet)
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


def packets_safe(out: dict[str, Any]) -> bool:
    for key in ["release_packet", "established_packet", "confirmed_baseline_packet", "finality_packet"]:
        packet = out.get(key, {})
        if not packet:
            return False
        for field in FORBIDDEN_FALSE:
            if packet.get(field) is not False:
                return False
    return True


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "ready", health(), ctx())
        if rc != 0 or out.get("chain_status") != "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY":
            errors.append("ready_chain_failed")
        if not packets_safe(out):
            errors.append("ready_packets_boundary_failed")
        if out.get("read_only_chain") is not True or out.get("additive_only") is not True:
            errors.append("chain_flags_failed")

        rc, out = run(root, "bad_health", health({"health_status": "QI_EXECUTION_HEALTH_BASELINE_BLOCKED"}), ctx())
        if rc != 1 or "health_status_not_ready" not in out.get("chain_blockers", []):
            errors.append("bad_health_not_blocked")

        rc, out = run(root, "bad_authority", health(confirmed_extra={"execution_authority_granted": True}), ctx())
        if rc != 1 or "confirmed_autonomy_execution_authority_granted_not_false" not in out.get("chain_blockers", []):
            errors.append("authority_grant_not_blocked")

        rc, out = run(root, "runtime_request", health(), ctx({"request_runtime_control": True}))
        if rc != 1 or "request_runtime_control_not_allowed" not in out.get("chain_blockers", []):
            errors.append("runtime_request_not_blocked")

        rc, out = run(root, "root_mismatch", health(), ctx({"expected_autonomy_health_root_digest": "other-root"}))
        if rc != 1 or "autonomy_health_root_digest_mismatch" not in out.get("chain_blockers", []):
            errors.append("root_mismatch_not_blocked")

        rc, out = run(root, "same_root_missing", health(), ctx({"same_root_required": False}))
        if rc != 1 or "same_root_required_not_true" not in out.get("chain_blockers", []):
            errors.append("same_root_missing_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi execution health packet chain check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

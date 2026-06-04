#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_local_execution_adapter_v0_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def engine(action: str, staged: bool = True, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "engine_version": "kuuos_runtime_daemon_qi_autonomous_execution_engine_v0_1",
        "engine_status": "QI_AUTONOMOUS_EXECUTION_ENGINE_READY",
        "engine_packet_id": f"qi-exec-engine-{action}",
        "selected_action": action,
        "execution_mode": "staged_intent_only" if staged else "nonexecuting_receipt",
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
        "external_notification_sent": False,
        "external_ticket_created": False,
        "external_handover_performed": False,
        "os_process_spawned": False,
        "network_call_performed": False
    }
    if extra:
        value.update(extra)
    return value


def chain(extra: dict[str, Any] | None = None, finality_extra: dict[str, Any] | None = None) -> dict[str, Any]:
    finality: dict[str, Any] = {
        "packet_id": "qi-exec-health-finality-demo",
        "packet_status": "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY",
        "finality_scope": "packet_chain_finality_not_authority_surface",
        "external_notification_sent": False,
        "external_ticket_created": False,
        "external_handover_performed": False,
        "scheduler_bypass_performed": False,
        "os_process_spawned": False,
        "network_call_performed": False,
        "probe_execution_performed": False,
        "world_update_performed": False,
        "memory_overwrite_performed": False
    }
    if finality_extra:
        finality.update(finality_extra)
    value: dict[str, Any] = {
        "chain_status": "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY",
        "packet_chain_id": "qi-exec-health-chain-demo",
        "finality_packet_id": "qi-exec-health-finality-demo",
        "finality_packet": finality
    }
    if extra:
        value.update(extra)
    return value


def license_packet(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "license_status": "QI_LOCAL_EXECUTION_LICENSE_READY",
        "local_runtime_state_write_allowed": True,
        "local_execution_ledger_append_allowed": True,
        "local_outbox_append_allowed": True,
        "external_side_effects_allowed": False
    }
    if extra:
        value.update(extra)
    return value


def ctx(runtime_root: pathlib.Path, nonce: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "qi_local_execution_adapter_enabled": True,
        "commit_local_effects": True,
        "runtime_root": str(runtime_root),
        "execution_nonce": nonce,
        "allowed_actions": ["advance_tick", "notify", "ticket", "handover", "hold", "observe", "freeze"]
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, engine_packet: dict[str, Any], chain_packet: dict[str, Any], lic: dict[str, Any], c: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    ep = root / f"{name}_engine.json"
    hp = root / f"{name}_chain.json"
    lp = root / f"{name}_license.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(ep, engine_packet)
    dump(hp, chain_packet)
    dump(lp, lic)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--engine", str(ep),
        "--health-chain", str(hp),
        "--license", str(lp),
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
        runtime_root = root / "runtime"

        rc, out = run(root, "advance", engine("advance_tick"), chain(), license_packet(), ctx(runtime_root, "n1"))
        if rc != 0 or out.get("adapter_status") != "QI_LOCAL_EXECUTION_ADAPTER_COMMITTED":
            errors.append("advance_not_committed")
        state = load(runtime_root / "runtime_state.json")
        ledger = read_jsonl(runtime_root / "execution_ledger.jsonl")
        if state.get("tick") != 1 or not ledger or out.get("local_runtime_state_updated") is not True:
            errors.append("advance_state_or_ledger_missing")
        if out.get("execution_committed") is not True or out.get("local_execution_ledger_appended") is not True:
            errors.append("advance_effect_flags_wrong")
        if out.get("network_call_performed") is not False or out.get("os_process_spawned") is not False:
            errors.append("advance_external_boundary_failed")

        rc, out = run(root, "advance_replay", engine("advance_tick"), chain(), license_packet(), ctx(runtime_root, "n1"))
        state2 = load(runtime_root / "runtime_state.json")
        ledger2 = read_jsonl(runtime_root / "execution_ledger.jsonl")
        if rc != 0 or out.get("adapter_status") != "QI_LOCAL_EXECUTION_ADAPTER_REPLAYED":
            errors.append("replay_not_detected")
        if state2.get("tick") != 1 or len(ledger2) != len(ledger):
            errors.append("replay_wrote_again")

        rc, out = run(root, "notify", engine("notify"), chain(), license_packet(), ctx(runtime_root, "n2"))
        notify_outbox = read_jsonl(runtime_root / "outbox" / "notifications.jsonl")
        ledger3 = read_jsonl(runtime_root / "execution_ledger.jsonl")
        if rc != 0 or out.get("adapter_status") != "QI_LOCAL_EXECUTION_ADAPTER_COMMITTED":
            errors.append("notify_not_committed")
        if not notify_outbox or len(ledger3) != len(ledger2) + 1:
            errors.append("notify_outbox_or_ledger_missing")
        if out.get("local_outbox_appended") is not True or out.get("external_notification_sent") is not False:
            errors.append("notify_boundary_failed")

        rc, out = run(root, "ticket_no_license", engine("ticket"), chain(), license_packet({"local_outbox_append_allowed": False}), ctx(runtime_root, "n3"))
        if rc != 1 or "outbox_append_not_licensed" not in out.get("blockers", []):
            errors.append("ticket_without_outbox_license_not_blocked")

        rc, out = run(root, "blocked_action", engine("advance_tick"), chain(), license_packet(), ctx(runtime_root, "n4", {"allowed_actions": ["hold"]}))
        if rc != 1 or "action_not_allowed" not in out.get("blockers", []):
            errors.append("action_allowlist_not_enforced")

        rc, out = run(root, "bad_engine", engine("advance_tick", extra={"network_call_performed": True}), chain(), license_packet(), ctx(runtime_root, "n5"))
        if rc != 1 or "engine_network_call_performed_not_false" not in out.get("blockers", []):
            errors.append("engine_network_effect_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi local execution adapter v0.2 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

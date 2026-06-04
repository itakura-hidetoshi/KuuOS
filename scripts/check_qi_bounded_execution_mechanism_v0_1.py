#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_bounded_execution_mechanism_v0_1.py"

FORBIDDEN_FALSE = [
    "execution_committed",
    "runtime_control_performed",
    "scheduler_bypass_performed",
    "notification_sent",
    "ticket_created",
    "handover_performed",
    "ledger_append_performed",
    "memory_write_performed",
    "memory_append_performed",
    "memory_overwrite_performed",
    "world_update_performed",
    "control_packet_mutation_performed",
    "probe_execution_performed",
    "execution_authority_granted",
    "execution_commit_allowed",
    "runtime_control_allowed",
    "scheduler_bypass_allowed",
    "ledger_append_allowed",
    "memory_write_allowed",
    "world_update_allowed",
    "probe_execution_allowed",
]


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def engine(action: str = "advance_tick", staged: bool = True, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "engine_version": "kuuos_runtime_daemon_qi_autonomous_execution_engine_v0_1",
        "engine_status": "QI_AUTONOMOUS_EXECUTION_ENGINE_READY",
        "engine_packet_id": "qi-exec-engine-demo",
        "selected_action": action,
        "execution_mode": "staged_intent_only" if staged else "nonexecuting_receipt",
        "execution_intent_staged": staged,
        "execution_committed": False,
        "process_tensor_guard_passed": True,
        "decisionos_guard_passed": True,
        "cbf_guard_passed": True,
        "token_guard_passed": True,
        "authority_guard_passed": True,
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
    }
    if extra:
        value.update(extra)
    return value


def finality_packet(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "packet_id": "qi-exec-health-finality-demo",
        "packet_kind": "qi_execution_health_finality_packet_v0_1",
        "packet_status": "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY",
        "finality_scope": "packet_chain_finality_not_authority_surface",
        "packet_chain_id": "qi-exec-health-chain-demo",
        "packet_chain_root_digest": "packet-chain-root-demo",
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
        "execution_authority_granted": False,
        "execution_commit_allowed": False,
        "runtime_control_allowed": False,
        "scheduler_bypass_allowed": False,
        "ledger_append_allowed": False,
        "memory_write_allowed": False,
        "world_update_allowed": False,
        "probe_execution_allowed": False,
    }
    if extra:
        value.update(extra)
    return value


def chain(extra: dict[str, Any] | None = None, finality_extra: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "chain_version": "kuuos_runtime_daemon_qi_execution_health_packet_chain_v0_1",
        "chain_status": "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY",
        "packet_chain_id": "qi-exec-health-chain-demo",
        "packet_chain_root_digest": "packet-chain-root-demo",
        "finality_packet_id": "qi-exec-health-finality-demo",
        "finality_packet": finality_packet(finality_extra),
        "read_only_chain": True,
        "projection_only": True,
        "additive_only": True,
        "tighten_only": True,
        "same_root_required": True,
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
        "qi_bounded_execution_mechanism_enabled": True,
        "bounded_adapter_scope_granted": True,
        "dry_run_only_required": True,
        "staged_intent_only_required": True,
        "receipt_only_required": True,
        "read_only_required": True,
        "projection_only_required": True,
        "allowed_adapters": [
            "tick_step_adapter_dry_run",
            "notification_adapter_dry_run",
            "ticket_adapter_dry_run",
            "handover_adapter_dry_run",
            "hold_noop_adapter",
            "observe_plan_adapter_dry_run",
            "freeze_noop_adapter"
        ]
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, engine_packet: dict[str, Any], chain_packet: dict[str, Any], c: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    ep = root / f"{name}_engine.json"
    hp = root / f"{name}_chain.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    dump(ep, engine_packet)
    dump(hp, chain_packet)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--engine", str(ep),
        "--health-chain", str(hp),
        "--context", str(cp),
        "--write", str(op),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(op)


def safe_receipt(out: dict[str, Any]) -> bool:
    receipt = out.get("dry_run_actuator_receipt", {})
    if not receipt:
        return False
    for key in FORBIDDEN_FALSE:
        if receipt.get(key) is not False:
            return False
    return receipt.get("dry_run_actuator_performed") is True and receipt.get("external_side_effects_performed") is False


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run(root, "advance", engine("advance_tick", True), chain(), ctx())
        if rc != 0 or out.get("mechanism_status") != "QI_BOUNDED_EXECUTION_MECHANISM_READY":
            errors.append("advance_ready_failed")
        if out.get("adapter_name") != "tick_step_adapter_dry_run" or not safe_receipt(out):
            errors.append("advance_adapter_boundary_failed")
        if out.get("execution_committed") is not False or out.get("dry_run_only") is not True:
            errors.append("advance_mechanism_boundary_failed")

        rc, out = run(root, "ticket", engine("ticket", True), chain(), ctx())
        if rc != 0 or out.get("adapter_name") != "ticket_adapter_dry_run" or out.get("ticket_created") is not False:
            errors.append("ticket_dry_run_failed")

        rc, out = run(root, "hold", engine("hold", False), chain(), ctx())
        if rc != 0 or out.get("adapter_name") != "hold_noop_adapter":
            errors.append("hold_noop_failed")
        if "nonexecuting_action_uses_noop_or_plan_adapter" not in out.get("mechanism_warnings", []):
            errors.append("hold_warning_missing")

        rc, out = run(root, "commit_request", engine("advance_tick", True), chain(), ctx({"request_execution_commit": True}))
        if rc != 1 or "request_execution_commit_not_allowed" not in out.get("mechanism_blockers", []):
            errors.append("commit_request_not_blocked")

        rc, out = run(root, "unstaged_ticket", engine("ticket", False), chain(), ctx())
        if rc != 1 or "executable_action_without_staged_intent" not in out.get("mechanism_blockers", []):
            errors.append("unstaged_executable_not_blocked")

        rc, out = run(root, "bad_finality", engine("advance_tick", True), chain(finality_extra={"execution_authority_granted": True}), ctx())
        if rc != 1 or "finality_execution_authority_granted_not_false" not in out.get("mechanism_blockers", []):
            errors.append("finality_authority_not_blocked")

        rc, out = run(root, "adapter_not_allowed", engine("notify", True), chain(), ctx({"allowed_adapters": ["tick_step_adapter_dry_run"]}))
        if rc != 1 or "adapter_not_allowlisted" not in out.get("mechanism_blockers", []):
            errors.append("adapter_allowlist_not_enforced")

        rc, out = run(root, "bad_engine_effect", engine("advance_tick", True, {"notification_sent": True}), chain(), ctx())
        if rc != 1 or "engine_notification_sent_not_false" not in out.get("mechanism_blockers", []):
            errors.append("engine_effect_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi bounded execution mechanism check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

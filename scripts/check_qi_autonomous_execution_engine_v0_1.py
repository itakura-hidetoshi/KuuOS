#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_autonomous_execution_engine_v0_1.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def decision(action: str = "advance_tick") -> dict:
    return {"decision_action": action}


def cbf(ok: bool = True, closed: bool = False, action: str = "advance_tick") -> dict:
    return {"cbf_ok": ok, "barrier_closed": closed, "cbf_action": action}


def token(remaining: int = 8) -> dict:
    return {"token_ledger_ok": True, "token_ledger_action": "advance_tick", "remaining_tokens": remaining, "minimum_required_tokens": 1}


def pt(ok: bool = True, nonmarkov: bool = False, recovery_missing: bool = False, freeze: bool = False) -> dict:
    return {
        "process_tensor_ok": ok,
        "process_tensor_action": "freeze" if freeze else "advance_tick",
        "non_markov_unresolved": nonmarkov,
        "recovery_witness_missing": recovery_missing,
        "recovery_witness_present": not recovery_missing,
        "freeze_required": freeze,
    }


def release() -> dict:
    return {
        "packet_status": "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_READY",
        "release_packet_id": "qi-cadence-v0-2-release-demo",
        "established_packet_id": "qi-cadence-v0-2-established-demo",
        "v0_2_release_ready": True,
        "v0_2_established": True,
        "release_receipt_only": True,
        "established_receipt_only": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "scheduler_bypass_performed": False,
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


def ctx(authority: bool = False, extra: dict | None = None) -> dict:
    value = {
        "qi_autonomous_execution_engine_enabled": True,
        "governance_bounded_execution_required": True,
        "staged_execution_only": True,
        "receipt_only_required": True,
        "read_only_required": True,
        "projection_only_required": True,
        "execution_authority_granted": authority,
        "allowed_actions": ["advance_tick"] if authority else [],
        "proposed_action": "advance_tick",
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, d: dict, c: dict, t: dict, p: dict, r: dict, x: dict) -> tuple[int, dict]:
    paths = {
        "decisionos": root / f"{name}_decision.json",
        "cbf": root / f"{name}_cbf.json",
        "token": root / f"{name}_token.json",
        "pt": root / f"{name}_pt.json",
        "release": root / f"{name}_release.json",
        "ctx": root / f"{name}_ctx.json",
        "out": root / f"{name}_out.json",
    }
    dump(paths["decisionos"], d)
    dump(paths["cbf"], c)
    dump(paths["token"], t)
    dump(paths["pt"], p)
    dump(paths["release"], r)
    dump(paths["ctx"], x)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--decisionos", str(paths["decisionos"]),
        "--cbf", str(paths["cbf"]),
        "--token-ledger", str(paths["token"]),
        "--process-tensor", str(paths["pt"]),
        "--cadence-release", str(paths["release"]),
        "--context", str(paths["ctx"]),
        "--write", str(paths["out"]),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(paths["out"])


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, out = run(root, "noauth", decision(), cbf(), token(), pt(), release(), ctx(False))
        if rc != 0 or out.get("engine_status") != "QI_AUTONOMOUS_EXECUTION_ENGINE_READY":
            errors.append("noauth_not_ready")
        if out.get("selected_action") != "hold" or out.get("selected_reason") != "authority_guard_failed":
            errors.append("noauth_hold_failed")
        if out.get("execution_committed") is not False or out.get("runtime_control_performed") is not False:
            errors.append("noauth_boundary_failed")

        rc, out = run(root, "auth", decision(), cbf(), token(), pt(), release(), ctx(True))
        if rc != 0 or out.get("selected_action") != "advance_tick":
            errors.append("auth_action_failed")
        if out.get("execution_intent_staged") is not True or out.get("execution_committed") is not False:
            errors.append("auth_staged_boundary_failed")

        rc, out = run(root, "nonmarkov", decision(), cbf(), token(), pt(nonmarkov=True), release(), ctx(True))
        if rc != 0 or out.get("selected_action") != "observe":
            errors.append("nonmarkov_observe_failed")

        rc, out = run(root, "cbf", decision(), cbf(ok=True, closed=True), token(), pt(), release(), ctx(True))
        if rc != 0 or out.get("selected_action") != "hold" or out.get("selected_reason") != "cbf_guard_failed":
            errors.append("cbf_hold_failed")

        rc, out = run(root, "runtime_request", decision(), cbf(), token(), pt(), release(), ctx(True, {"request_runtime_control": True}))
        if rc != 1 or out.get("engine_status") != "QI_AUTONOMOUS_EXECUTION_ENGINE_BLOCKED":
            errors.append("runtime_request_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi autonomous execution engine check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

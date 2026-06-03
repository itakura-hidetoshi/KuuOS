#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cadence_v0_2_release_established_packet.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def cadence() -> dict:
    return {
        "finality_packet_status": "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY",
        "finality_packet_id": "qi-cadence-finality-demo",
        "superchain_root_digest": "cadence-root-demo",
        "finality_confirmed": True,
        "receipt_only_finality_packet": True,
        "canonical_chain_complete": True,
        "no_authority_boundary_preserved": True,
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


def observe() -> dict:
    return {
        "finality_status": "QI_OBSERVABILITY_SUPERCHAIN_FINALITY_PACKET_READY",
        "finality_packet_id": "qi-observe-finality-demo",
        "finality_root_digest": "observe-root-demo",
        "observability_finality_confirmed": True,
        "receipt_only_finality_packet": True,
        "read_only_finality_packet": True,
        "projection_only": True,
        "observability_chain_complete": True,
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


def ctx(extra: dict | None = None) -> dict:
    value = {
        "release_context_id": "qi-cadence-v0-2-release-test",
        "qi_cadence_v0_2_release_enabled": True,
        "established_packet_required": True,
        "receipt_only_required": True,
        "read_only_required": True,
        "projection_only_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, c: dict, o: dict, x: dict) -> tuple[int, dict]:
    cp = root / f"{name}_cadence.json"
    op = root / f"{name}_observe.json"
    xp = root / f"{name}_ctx.json"
    rp = root / f"{name}_out.json"
    dump(cp, c)
    dump(op, o)
    dump(xp, x)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--cadence-finality", str(cp),
        "--observability-finality", str(op),
        "--context", str(xp),
        "--write", str(rp),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(rp)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, out = run(root, "ready", cadence(), observe(), ctx())
        if rc != 0 or out.get("packet_status") != "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_READY":
            errors.append("ready_failed")
        if out.get("v0_2_release_ready") is not True or out.get("v0_2_established") is not True:
            errors.append("release_flags_failed")
        if out.get("runtime_control_authority") is not False or out.get("ledger_append_performed") is not False:
            errors.append("boundary_failed")
        if not out.get("release_root_digest") or not out.get("established_root_digest"):
            errors.append("digest_missing")

        c = cadence()
        c["finality_packet_status"] = "NOT_READY"
        rc, out = run(root, "bad_cadence", c, observe(), ctx())
        if rc != 1 or out.get("packet_status") != "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_BLOCKED":
            errors.append("bad_cadence_not_blocked")

        o = observe()
        o["finality_status"] = "NOT_READY"
        rc, out = run(root, "bad_observe", cadence(), o, ctx())
        if rc != 1 or out.get("packet_status") != "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_BLOCKED":
            errors.append("bad_observe_not_blocked")

        rc, out = run(root, "runtime", cadence(), observe(), ctx({"request_runtime_control": True}))
        if rc != 1 or out.get("packet_status") != "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_BLOCKED":
            errors.append("runtime_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi cadence v0.2 release established packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

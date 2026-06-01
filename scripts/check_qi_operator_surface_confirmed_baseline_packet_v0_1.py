#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_operator_surface_confirmed_baseline_packet_v0_1.py"

ESTABLISHED = {
    "established_status": "QI_OPERATOR_SURFACE_BASELINE_ESTABLISHED_PACKET_READY",
    "established_packet_id": "qi-operator-surface-established-test-0001",
    "source_declaration_id": "qi-nav-chain-final-test-0001",
    "source_finality_packet_id": "qi-nav-finality-test-0001",
    "source_catalog_id": "qi-dashboard-catalog-test-0001",
    "release_marker": "QI_OPERATOR_NAVIGATION_ENTRYPOINT_RELEASED_V0_1",
    "release_marker_hash": "release-marker-hash-test",
    "navigation_landing_uri": "file://static/qi-dashboard/qi-dashboard-catalog-test.html",
    "navigation_landing_hash": "landing-hash-test",
    "html_artifact_name": "qi-dashboard-catalog-test.html",
    "html_sha256": "html-sha256-test",
    "catalog_entry_count": 1,
    "operator_surface_baseline_established": True,
    "navigation_chain_finalized": True,
    "release_ready_confirmed": True,
    "additive_only_future_required": True,
    "read_only_surface": True,
    "js_enabled": False,
    "external_network_required": False,
    "daemon_control_performed": False,
    "daemon_restart_performed": False,
    "daemon_stop_performed": False,
    "daemon_resume_performed": False,
    "memory_write_performed": False,
    "memory_append_performed": False,
    "memory_overwrite_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "auto_remediation_performed": False,
    "grants_daemon_control_authority": False,
    "grants_probe_execution_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_overwrite_authority": False
}

CTX = {
    "additive_only_future_required": True,
    "operator_surface_confirmed_baseline_enabled": True,
    "read_only_surface_required": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, established: dict, ctx: dict, name: str) -> tuple[int, dict]:
    established_path = root / f"{name}_established.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_confirmed.json"
    dump(established_path, established)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--established-packet", str(established_path),
        "--context", str(ctx_path),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return completed.returncode, load(out) if out.is_file() else {}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, good = run_case(root, ESTABLISHED, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("confirmed_status") != "QI_OPERATOR_SURFACE_CONFIRMED_BASELINE_PACKET_READY":
            errors.append("good_status_mismatch")
        if good.get("operator_surface_confirmed_baseline") is not True:
            errors.append("confirmed_baseline_not_true")
        if good.get("established_packet_confirmed") is not True:
            errors.append("established_packet_not_confirmed")
        if good.get("navigation_chain_finalized") is not True:
            errors.append("navigation_chain_finalized_not_true")
        if good.get("release_ready_confirmed") is not True:
            errors.append("release_ready_not_true")
        if good.get("additive_only_future_required") is not True:
            errors.append("additive_only_not_true")
        if not good.get("confirmed_packet_id"):
            errors.append("confirmed_packet_id_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**ESTABLISHED, "release_marker_hash": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "release_marker_hash_missing" not in bad.get("confirmed_blockers", []):
            errors.append("release_marker_hash_blocker_missing")
        if bad.get("operator_surface_confirmed_baseline") is not False:
            errors.append("bad_confirmed_not_false")

        not_additive = {**CTX, "additive_only_future_required": False}
        rc, blocked = run_case(root, ESTABLISHED, not_additive, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "additive_only_future_required_not_true" not in blocked.get("confirmed_blockers", []):
            errors.append("additive_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi operator surface confirmed baseline packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

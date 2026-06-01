#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_operator_navigation_finality_packet_v0_1.py"

SMOKE = {
    "smoke_status": "QI_OPERATOR_ENTRYPOINT_SMOKE_RECEIPT_READY",
    "smoke_receipt_id": "qi-entrypoint-smoke-test-0001",
    "source_landing_receipt_id": "qi-landing-test-0001",
    "source_catalog_id": "qi-dashboard-catalog-test-0001",
    "navigation_landing_key": "qi/navigation/landing/test",
    "navigation_landing_uri": "file://static/qi-dashboard/qi-dashboard-catalog-test.html",
    "navigation_landing_hash": "landing-hash-test",
    "html_artifact_name": "qi-dashboard-catalog-test.html",
    "html_sha256": "html-sha256-test",
    "catalog_entry_count": 1,
    "operator_entrypoint_ready": True,
    "published_landing_receipt_ready": True,
    "entrypoint_uri_resolved": True,
    "entrypoint_hash_confirmed": True,
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
    "operator_navigation_finality_enabled": True,
    "read_only_surface_required": True,
    "release_marker": "QI_OPERATOR_NAVIGATION_ENTRYPOINT_RELEASED_V0_1"
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, smoke: dict, ctx: dict, name: str) -> tuple[int, dict]:
    smoke_path = root / f"{name}_smoke.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_finality.json"
    dump(smoke_path, smoke)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--smoke-receipt", str(smoke_path),
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
        rc, good = run_case(root, SMOKE, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("finality_status") != "QI_OPERATOR_NAVIGATION_FINALITY_PACKET_READY":
            errors.append("good_status_mismatch")
        if good.get("operator_navigation_final") is not True:
            errors.append("operator_navigation_final_not_true")
        if good.get("release_marker_rendered") is not True:
            errors.append("release_marker_not_rendered")
        if good.get("entrypoint_ready_confirmed") is not True:
            errors.append("entrypoint_not_confirmed")
        if good.get("published_landing_confirmed") is not True:
            errors.append("landing_not_confirmed")
        if not good.get("release_marker_hash"):
            errors.append("release_marker_hash_missing")
        if not good.get("finality_packet_id"):
            errors.append("finality_packet_id_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**SMOKE, "html_sha256": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "html_sha256_missing" not in bad.get("finality_blockers", []):
            errors.append("html_sha_blocker_missing")
        if bad.get("operator_navigation_final") is not False:
            errors.append("bad_final_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, SMOKE, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("finality_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi operator navigation finality packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_operator_entrypoint_smoke_receipt_v0_1.py"

LANDING = {
    "landing_status": "QI_NAVIGATION_LANDING_SURFACE_READY",
    "landing_receipt_id": "qi-landing-test-0001",
    "source_catalog_id": "qi-dashboard-catalog-test-0001",
    "navigation_landing_key": "qi/navigation/landing/test",
    "navigation_landing_uri": "file://static/qi-dashboard/qi-dashboard-catalog-test.html",
    "navigation_landing_hash": "landing-hash-test",
    "html_artifact_name": "qi-dashboard-catalog-test.html",
    "html_sha256": "html-sha256-test",
    "catalog_entry_count": 1,
    "landing_surface_registered": True,
    "navigation_entrypoint_ready": True,
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
    "operator_entrypoint_smoke_enabled": True,
    "read_only_surface_required": True,
    "smoke_mode": "read_only_entrypoint_receipt"
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, landing: dict, ctx: dict, name: str) -> tuple[int, dict]:
    landing_path = root / f"{name}_landing.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_smoke.json"
    dump(landing_path, landing)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--landing-surface", str(landing_path),
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
        rc, good = run_case(root, LANDING, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("smoke_status") != "QI_OPERATOR_ENTRYPOINT_SMOKE_RECEIPT_READY":
            errors.append("good_status_mismatch")
        if good.get("operator_entrypoint_ready") is not True:
            errors.append("operator_entrypoint_not_true")
        if good.get("published_landing_receipt_ready") is not True:
            errors.append("published_landing_not_true")
        if good.get("entrypoint_uri_resolved") is not True:
            errors.append("uri_not_resolved")
        if good.get("entrypoint_hash_confirmed") is not True:
            errors.append("hash_not_confirmed")
        if not good.get("smoke_receipt_id"):
            errors.append("smoke_receipt_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        mismatch_ctx = {**CTX, "observed_navigation_landing_hash": "different"}
        rc, mismatch = run_case(root, LANDING, mismatch_ctx, "mismatch")
        if rc != 1:
            errors.append("mismatch_returncode_mismatch")
        if "navigation_landing_hash_mismatch" not in mismatch.get("smoke_blockers", []):
            errors.append("hash_mismatch_blocker_missing")
        if mismatch.get("operator_entrypoint_ready") is not False:
            errors.append("mismatch_entrypoint_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, LANDING, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("smoke_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi operator entrypoint smoke receipt check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

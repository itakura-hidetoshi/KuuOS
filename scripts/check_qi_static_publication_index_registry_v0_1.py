#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_static_publication_index_registry_v0_1.py"

SURFACE = {
    "surface_status": "QI_STATIC_DASHBOARD_SURFACE_READY",
    "surface_id": "qi-static-dashboard-test-0001",
    "dashboard_artifact_ready": True,
    "static_html_rendered": True,
    "html_artifact_name": "qi-dashboard-test.html",
    "html_sha256": "html-sha256-test",
    "html_bytes": 4096,
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
    "index_registry_key": "qi/static-dashboard/test",
    "publication_base": "static/qi-dashboard",
    "publication_uri": "file://static/qi-dashboard/qi-dashboard-test.html",
    "read_only_surface_required": True,
    "registry_mode": "static_artifact_index",
    "static_publication_index_enabled": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, surface: dict, ctx: dict, name: str) -> tuple[int, dict]:
    surface_path = root / f"{name}_surface.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_registry.json"
    dump(surface_path, surface)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--surface", str(surface_path),
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

        rc, good = run_case(root, SURFACE, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("registry_status") != "QI_STATIC_PUBLICATION_INDEX_REGISTRY_READY":
            errors.append("good_status_mismatch")
        if good.get("static_dashboard_published") is not True:
            errors.append("published_not_true")
        if good.get("index_entry_registered") is not True:
            errors.append("registered_not_true")
        if not good.get("index_entry_hash"):
            errors.append("index_entry_hash_missing")
        if not good.get("publication_receipt_id"):
            errors.append("publication_receipt_id_missing")
        if good.get("js_enabled") is not False:
            errors.append("js_enabled_not_false")
        if good.get("external_network_required") is not False:
            errors.append("external_network_not_false")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**SURFACE, "html_sha256": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "html_sha256_missing" not in bad.get("registry_blockers", []):
            errors.append("html_sha_blocker_missing")
        if bad.get("index_entry_registered") is not False:
            errors.append("bad_registered_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, SURFACE, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("registry_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi static publication index registry check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

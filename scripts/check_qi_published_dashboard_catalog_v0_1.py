#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_published_dashboard_catalog_v0_1.py"

ENTRY = {
    "registry_status": "QI_STATIC_PUBLICATION_INDEX_REGISTRY_READY",
    "publication_receipt_id": "qi-static-pub-test-0001",
    "source_surface_id": "qi-static-dashboard-test-0001",
    "html_artifact_name": "qi-dashboard-test.html",
    "html_sha256": "html-sha256-test",
    "html_bytes": 4096,
    "publication_path": "static/qi-dashboard/qi-dashboard-test.html",
    "publication_uri": "file://static/qi-dashboard/qi-dashboard-test.html",
    "index_registry_key": "qi/static-dashboard/test",
    "index_entry_hash": "index-entry-hash-test",
    "registry_mode": "static_artifact_index",
    "static_dashboard_published": True,
    "index_entry_registered": True,
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
    "catalog_key": "qi/published-dashboard/catalog",
    "navigation_index_key": "qi/published-dashboard/navigation",
    "published_dashboard_catalog_enabled": True,
    "read_only_surface_required": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, entries, ctx: dict, name: str) -> tuple[int, dict]:
    entries_path = root / f"{name}_entries.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_catalog.json"
    dump(entries_path, entries)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--registry-entries", str(entries_path),
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

        rc, good = run_case(root, [ENTRY], CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("catalog_status") != "QI_PUBLISHED_DASHBOARD_CATALOG_READY":
            errors.append("good_status_mismatch")
        if good.get("catalog_entry_count") != 1:
            errors.append("entry_count_mismatch")
        if good.get("published_dashboard_catalog_rendered") is not True:
            errors.append("catalog_not_rendered")
        if good.get("operator_navigation_index_rendered") is not True:
            errors.append("navigation_not_rendered")
        if not good.get("navigation_index_hash"):
            errors.append("navigation_hash_missing")
        if good.get("latest_publication_uri") != "file://static/qi-dashboard/qi-dashboard-test.html":
            errors.append("latest_uri_mismatch")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        rc, empty = run_case(root, [], CTX, "empty")
        if rc != 1:
            errors.append("empty_returncode_mismatch")
        if "registry_entries_missing" not in empty.get("catalog_blockers", []):
            errors.append("missing_entries_blocker_missing")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, [ENTRY], not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("catalog_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi published dashboard catalog check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

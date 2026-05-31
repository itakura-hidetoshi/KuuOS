#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_catalog_static_index_v0_1.py"

CATALOG = {
    "catalog_status": "QI_PUBLISHED_DASHBOARD_CATALOG_READY",
    "catalog_id": "qi-dashboard-catalog-test-0001",
    "catalog_key": "qi/published-dashboard/catalog",
    "catalog_entry_count": 1,
    "navigation_index_key": "qi/published-dashboard/navigation",
    "navigation_index_hash": "navigation-index-hash-test",
    "latest_publication_uri": "file://static/qi-dashboard/qi-dashboard-test.html",
    "published_dashboard_catalog_rendered": True,
    "operator_navigation_index_rendered": True,
    "entries": [
        {
            "publication_receipt_id": "qi-static-pub-test-0001",
            "source_surface_id": "qi-static-dashboard-test-0001",
            "html_artifact_name": "qi-dashboard-test.html",
            "html_sha256": "html-sha256-test",
            "html_bytes": 4096,
            "publication_path": "static/qi-dashboard/qi-dashboard-test.html",
            "publication_uri": "file://static/qi-dashboard/qi-dashboard-test.html",
            "index_registry_key": "qi/static-dashboard/test",
            "index_entry_hash": "index-entry-hash-test",
            "registry_mode": "static_artifact_index"
        }
    ],
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
    "catalog_static_index_enabled": True,
    "generated_by": "kuuos_catalog_static_index_v0_1",
    "html_artifact_name": "qi-catalog-index-test.html",
    "read_only_surface_required": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, catalog: dict, ctx: dict, name: str) -> tuple[int, dict, str]:
    catalog_path = root / f"{name}_catalog.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_index.json"
    html = root / f"{name}.html"
    dump(catalog_path, catalog)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--catalog", str(catalog_path),
        "--context", str(ctx_path),
        "--write", str(out),
        "--write-html", str(html),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return completed.returncode, load(out) if out.is_file() else {}, html.read_text(encoding="utf-8") if html.is_file() else ""


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, good, html = run_case(root, CATALOG, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("index_status") != "QI_CATALOG_STATIC_INDEX_READY":
            errors.append("good_status_mismatch")
        if good.get("multi_dashboard_index_ready") is not True:
            errors.append("index_ready_not_true")
        if good.get("static_catalog_index_rendered") is not True:
            errors.append("static_index_not_rendered")
        if good.get("js_enabled") is not False:
            errors.append("js_enabled_not_false")
        if good.get("external_network_required") is not False:
            errors.append("external_network_not_false")
        if good.get("entry_count") != 1:
            errors.append("entry_count_mismatch")
        if not good.get("html_sha256"):
            errors.append("html_sha_missing")
        if "<script" in html.lower():
            errors.append("script_tag_present")
        if "Qi Published Dashboard Catalog" not in html:
            errors.append("catalog_title_missing")
        if "qi-dashboard-test.html" not in html:
            errors.append("entry_missing_in_html")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing_entries = {**CATALOG, "entries": []}
        rc, bad, _ = run_case(root, missing_entries, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "catalog_entries_missing" not in bad.get("index_blockers", []):
            errors.append("entries_blocker_missing")
        if bad.get("multi_dashboard_index_ready") is not False:
            errors.append("bad_ready_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked, _ = run_case(root, CATALOG, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("index_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi catalog static index check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

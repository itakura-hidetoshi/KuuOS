#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_operator_navigation_chain_final_declaration_v0_1.py"

FINALITY = {
    "finality_status": "QI_OPERATOR_NAVIGATION_FINALITY_PACKET_READY",
    "finality_packet_id": "qi-nav-finality-test-0001",
    "source_smoke_receipt_id": "qi-entrypoint-smoke-test-0001",
    "source_landing_receipt_id": "qi-landing-test-0001",
    "source_catalog_id": "qi-dashboard-catalog-test-0001",
    "release_marker": "QI_OPERATOR_NAVIGATION_ENTRYPOINT_RELEASED_V0_1",
    "release_marker_hash": "release-marker-hash-test",
    "navigation_landing_uri": "file://static/qi-dashboard/qi-dashboard-catalog-test.html",
    "navigation_landing_hash": "landing-hash-test",
    "html_artifact_name": "qi-dashboard-catalog-test.html",
    "html_sha256": "html-sha256-test",
    "catalog_entry_count": 1,
    "operator_navigation_final": True,
    "release_marker_rendered": True,
    "entrypoint_ready_confirmed": True,
    "published_landing_confirmed": True,
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
    "chain_final_declaration_enabled": True,
    "read_only_surface_required": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, finality: dict, ctx: dict, name: str) -> tuple[int, dict]:
    finality_path = root / f"{name}_finality.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_declaration.json"
    dump(finality_path, finality)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--finality-packet", str(finality_path),
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
        rc, good = run_case(root, FINALITY, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("declaration_status") != "QI_OPERATOR_NAVIGATION_CHAIN_FINAL_DECLARATION_READY":
            errors.append("good_status_mismatch")
        if good.get("chain_finalized") is not True:
            errors.append("chain_finalized_not_true")
        if good.get("release_ready_confirmed") is not True:
            errors.append("release_ready_not_true")
        if good.get("final_declaration_rendered") is not True:
            errors.append("declaration_not_rendered")
        if good.get("additive_only_future_required") is not True:
            errors.append("additive_only_not_true")
        if not good.get("declaration_id"):
            errors.append("declaration_id_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**FINALITY, "release_marker_hash": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "release_marker_hash_missing" not in bad.get("declaration_blockers", []):
            errors.append("release_marker_hash_blocker_missing")
        if bad.get("chain_finalized") is not False:
            errors.append("bad_chain_finalized_not_false")

        not_additive = {**CTX, "additive_only_future_required": False}
        rc, blocked = run_case(root, FINALITY, not_additive, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "additive_only_future_required_not_true" not in blocked.get("declaration_blockers", []):
            errors.append("additive_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi operator navigation chain final declaration check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

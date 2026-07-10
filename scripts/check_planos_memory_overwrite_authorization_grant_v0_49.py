#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_memory_overwrite_authorization_request_v0_48 import _ready_external_commit_closeout
from runtime.kuuos_planos_memory_overwrite_authorization_request_v0_48 import build_memory_overwrite_authorization_request
from runtime.kuuos_planos_memory_overwrite_authorization_grant_v0_49 import (
    SOURCE_VERSION,
    VERSION,
    build_memory_overwrite_authorization_grant,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_memory_overwrite_request() -> dict:
    source = _ready_external_commit_closeout()
    return build_memory_overwrite_authorization_request(external_commit_closeout=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_memory_overwrite_request()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_memory_overwrite_authorization_grant(memory_overwrite_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_READY", f"grant blocked: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_authorization_grant_only"] is True, "grant-only boundary missing")
    require(receipt["boundary"]["memory_overwrite_authorization_requested"] is True, "request not preserved")
    require(receipt["boundary"]["memory_overwrite_authorization_granted"] is True, "authorization not granted")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite applied")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["memory_overwrite_authorization_grant"]
    require(record["memory_overwrite_authorization_granted"] is True, "grant record missing authorization")
    require(record["memory_overwrite_ready"] is False, "grant record applied memory overwrite")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["memory_overwrite_authorization_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_memory_overwrite_authorization_grant(memory_overwrite_request=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_BLOCKED", "pre-granted source not blocked")
    require("source_boundary_memory_overwrite_authorization_granted_promoted" in blocked["blockers"], "pre-grant blocker missing")

    mismatch = dict(source)
    request_record = dict(mismatch["memory_overwrite_authorization_request"])
    request_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["memory_overwrite_authorization_request"] = request_record
    blocked_mismatch = build_memory_overwrite_authorization_grant(memory_overwrite_request=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_BLOCKED", "mismatch not blocked")
    require("selected_candidate_digest_memory_overwrite_request_mismatch" in blocked_mismatch["blockers"], "digest mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_memory_overwrite_authorization_grant_v0_49.py"
    formal = ROOT / "formal/KUOS/PlanOS/MemoryOverwriteAuthorizationGrantV0_49.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_49.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_v0_49.md"
    manifest_path = ROOT / "manifests/kuuos_planos_memory_overwrite_authorization_grant_v0_49.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_memory_overwrite_authorization_grant",
        "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_READY",
        "memory_overwrite_authorization_grant_only",
        "memory_overwrite_authorization_granted",
        "memory_overwrite_granted",
    ))
    require_tokens(formal, (
        "MemoryOverwriteAuthorizationGrantSurface",
        "MemoryOverwriteAuthorizationGrantBoundary",
        "PlanOSMemoryOverwriteAuthorizationGrantBridge",
        "source_request_asks_but_does_not_grant_memory_overwrite",
        "grant_authorizes_but_does_not_apply_memory_or_grant_truth_or_blocker_release",
        "history_appends_one_memory_overwrite_authorization_grant_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationGrantV0_49",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationGrantV0_49",))
    require_tokens(docs, (
        "PlanOS Memory Overwrite Authorization Grant v0.49",
        "memory overwrite authorization granted = true",
        "memory overwrite granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_memory_overwrite_authorization_grant_v0_49.py",
        "v0.1-v0.49",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v049",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS memory overwrite authorization grant v0.49 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

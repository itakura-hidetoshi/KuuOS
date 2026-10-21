#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_truth_authority_authorization_request_v0_52 import _ready_memory_overwrite_closeout
from runtime.kuuos_planos_truth_authority_authorization_request_v0_52 import build_truth_authority_authorization_request
from runtime.kuuos_planos_truth_authority_authorization_grant_v0_53 import (
    SOURCE_VERSION,
    VERSION,
    build_truth_authority_authorization_grant,
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


def _ready_truth_authority_request() -> dict:
    source = _ready_memory_overwrite_closeout()
    return build_truth_authority_authorization_request(memory_overwrite_closeout=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_truth_authority_request()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_truth_authority_authorization_grant(truth_authority_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_READY",
        f"grant blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "cycle closeout not preserved")
    require(
        receipt["boundary"]["truth_authority_authorization_grant_only"] is True,
        "grant-only boundary missing",
    )
    require(receipt["boundary"]["truth_authority_authorization_requested"] is True, "request not preserved")
    require(receipt["boundary"]["truth_authority_authorization_granted"] is True, "authorization not granted")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority applied")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["truth_authority_authorization_grant"]
    require(record["memory_overwrite_preserved"] is True, "grant lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "grant lost memory closeout")
    require(record["cycle_closed_preserved"] is True, "grant lost cycle closeout")
    require(record["truth_authority_authorization_granted"] is True, "grant record missing authorization")
    require(record["truth_authority_ready"] is False, "grant record applied truth authority")
    require(record["blocker_release_ready"] is False, "grant record released blockers")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["truth_authority_authorization_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_truth_authority_authorization_grant(truth_authority_request=promoted).to_dict()
    require(
        blocked["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_BLOCKED",
        "pre-granted source not blocked",
    )
    require(
        "source_boundary_truth_authority_authorization_granted_promoted" in blocked["blockers"],
        "pre-grant blocker missing",
    )

    missing_cycle = dict(source)
    boundary2 = dict(missing_cycle["boundary"])
    boundary2["cycle_closed_preserved"] = False
    missing_cycle["boundary"] = boundary2
    blocked_cycle = build_truth_authority_authorization_grant(truth_authority_request=missing_cycle).to_dict()
    require(
        blocked_cycle["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_BLOCKED",
        "missing cycle closeout not blocked",
    )
    require("source_boundary_cycle_closed_preserved_missing" in blocked_cycle["blockers"], "cycle blocker missing")

    mismatch = dict(source)
    request_record = dict(mismatch["truth_authority_authorization_request"])
    request_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["truth_authority_authorization_request"] = request_record
    blocked_mismatch = build_truth_authority_authorization_grant(truth_authority_request=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_truth_authority_request_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_truth_authority_authorization_grant_v0_53.py"
    formal = ROOT / "formal/KUOS/PlanOS/TruthAuthorityAuthorizationGrantV0_53.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_53.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_v0_53.md"
    manifest_path = ROOT / "manifests/kuuos_planos_truth_authority_authorization_grant_v0_53.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_truth_authority_authorization_grant",
        "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_READY",
        "truth_authority_authorization_grant_only",
        "truth_authority_authorization_granted",
        "truth_authority_granted",
    ))
    require_tokens(formal, (
        "TruthAuthorityAuthorizationGrantSurface",
        "TruthAuthorityAuthorizationGrantBoundary",
        "PlanOSTruthAuthorityAuthorizationGrantBridge",
        "source_request_asks_but_does_not_grant_truth_authority",
        "grant_binds_candidate_and_preserves_memory_closeout_state",
        "grant_authorizes_but_does_not_apply_truth_or_release_blockers",
        "boundary_preserves_truth_authority_authorization_grant_only",
        "history_appends_one_truth_authority_authorization_grant_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.TruthAuthorityAuthorizationGrantV0_53",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.TruthAuthorityAuthorizationGrantV0_53",))
    require_tokens(docs, (
        "PlanOS Truth Authority Authorization Grant v0.53",
        "truth authority authorization grant only = true",
        "truth authority authorization granted = true",
        "truth authority granted = false",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_truth_authority_authorization_grant_v0_53.py",
        "v0.1-v0.53",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v053",))

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
    print("PlanOS truth authority authorization grant v0.53 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

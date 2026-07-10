#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_truth_authority_closeout_receipt_v0_55 import _ready_truth_authority_receipt
from runtime.kuuos_planos_truth_authority_closeout_receipt_v0_55 import build_truth_authority_closeout_receipt
from runtime.kuuos_planos_blocker_release_authorization_request_v0_56 import (
    SOURCE_VERSION,
    VERSION,
    build_blocker_release_authorization_request,
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


def _ready_truth_authority_closeout() -> dict:
    source = _ready_truth_authority_receipt()
    return build_truth_authority_closeout_receipt(truth_authority_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_truth_authority_closeout()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_blocker_release_authorization_request(truth_authority_closeout=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_READY",
        f"request blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(receipt["boundary"]["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        receipt["boundary"]["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_request_only"] is True,
        "request-only boundary missing",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_requested"] is True,
        "authorization request missing",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_granted"] is False,
        "authorization grant promoted",
    )
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["blocker_release_authorization_request"]
    require(record["memory_overwrite_preserved"] is True, "request lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "request lost memory closeout")
    require(record["truth_authority_preserved"] is True, "request lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "request lost truth cycle closeout")
    require(record["blocker_release_authorization_requested"] is True, "request record missing request")
    require(record["blocker_release_authorization_granted"] is False, "request record granted authorization")
    require(record["blocker_release_ready"] is False, "request record released blockers")

    missing_closeout = dict(source)
    boundary = dict(missing_closeout["boundary"])
    boundary["truth_authority_cycle_closed"] = False
    missing_closeout["boundary"] = boundary
    blocked_closeout = build_blocker_release_authorization_request(truth_authority_closeout=missing_closeout).to_dict()
    require(
        blocked_closeout["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_BLOCKED",
        "missing truth closeout not blocked",
    )
    require(
        "source_boundary_truth_authority_cycle_closed_missing" in blocked_closeout["blockers"],
        "truth closeout blocker missing",
    )

    release_promoted = dict(source)
    boundary2 = dict(release_promoted["boundary"])
    boundary2["blocker_release_granted"] = True
    release_promoted["boundary"] = boundary2
    blocked_release = build_blocker_release_authorization_request(truth_authority_closeout=release_promoted).to_dict()
    require(
        blocked_release["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_BLOCKED",
        "pre-released source not blocked",
    )
    require(
        "source_boundary_blocker_release_granted_promoted" in blocked_release["blockers"],
        "pre-release blocker missing",
    )

    mismatch = dict(source)
    source_record = dict(mismatch["truth_authority_closeout_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["truth_authority_closeout_receipt"] = source_record
    blocked_mismatch = build_blocker_release_authorization_request(truth_authority_closeout=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_truth_authority_closeout_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_blocker_release_authorization_request_v0_56.py"
    formal = ROOT / "formal/KUOS/PlanOS/BlockerReleaseAuthorizationRequestV0_56.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_56.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_v0_56.md"
    manifest_path = ROOT / "manifests/kuuos_planos_blocker_release_authorization_request_v0_56.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_blocker_release_authorization_request",
        "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_READY",
        "blocker_release_authorization_request_only",
        "blocker_release_authorization_requested",
        "blocker_release_authorization_granted",
        "blocker_release_granted",
    ))
    require_tokens(formal, (
        "BlockerReleaseAuthorizationRequestSurface",
        "BlockerReleaseAuthorizationRequestBoundary",
        "PlanOSBlockerReleaseAuthorizationRequestBridge",
        "source_closeout_preserves_truth_and_keeps_release_closed",
        "request_binds_candidate_and_preserves_closed_truth_state",
        "request_asks_blocker_release_but_does_not_grant_or_apply_it",
        "boundary_is_blocker_release_authorization_request_only",
        "history_appends_one_blocker_release_authorization_request",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.BlockerReleaseAuthorizationRequestV0_56",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.BlockerReleaseAuthorizationRequestV0_56",))
    require_tokens(docs, (
        "PlanOS Blocker Release Authorization Request v0.56",
        "blocker release authorization request only = true",
        "blocker release authorization requested = true",
        "blocker release authorization granted = false",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_blocker_release_authorization_request_v0_56.py",
        "v0.1-v0.56",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v056",))

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
    print("PlanOS blocker release authorization request v0.56 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

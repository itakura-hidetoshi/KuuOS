#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_memory_overwrite_closeout_receipt_v0_51 import _ready_memory_overwrite_receipt
from runtime.kuuos_planos_memory_overwrite_closeout_receipt_v0_51 import build_memory_overwrite_closeout_receipt
from runtime.kuuos_planos_truth_authority_authorization_request_v0_52 import (
    SOURCE_VERSION,
    VERSION,
    build_truth_authority_authorization_request,
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


def _ready_memory_overwrite_closeout() -> dict:
    source = _ready_memory_overwrite_receipt()
    return build_memory_overwrite_closeout_receipt(memory_overwrite_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_memory_overwrite_closeout()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_truth_authority_authorization_request(memory_overwrite_closeout=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_READY",
        f"request blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "cycle closeout not preserved")
    require(
        receipt["boundary"]["truth_authority_authorization_request_only"] is True,
        "request-only boundary missing",
    )
    require(
        receipt["boundary"]["truth_authority_authorization_requested"] is True,
        "truth authority request missing",
    )
    require(
        receipt["boundary"]["truth_authority_authorization_granted"] is False,
        "truth authorization granted too early",
    )
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["truth_authority_authorization_request"]
    require(record["memory_overwrite_preserved"] is True, "record lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "record lost memory closeout")
    require(record["cycle_closed_preserved"] is True, "record lost cycle closeout")
    require(record["truth_authority_authorization_requested"] is True, "record missing request")
    require(record["truth_authority_authorization_granted"] is False, "record granted authorization")
    require(record["truth_authority_ready"] is False, "record leaked truth readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["truth_authority_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_truth_authority_authorization_request(memory_overwrite_closeout=promoted).to_dict()
    require(
        blocked["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BLOCKED",
        "truth-promoted source not blocked",
    )
    require(
        "source_boundary_truth_authority_granted_promoted" in blocked["blockers"],
        "truth blocker missing",
    )

    missing_closeout = dict(source)
    boundary2 = dict(missing_closeout["boundary"])
    boundary2["cycle_closed"] = False
    missing_closeout["boundary"] = boundary2
    blocked_cycle = build_truth_authority_authorization_request(
        memory_overwrite_closeout=missing_closeout
    ).to_dict()
    require(
        blocked_cycle["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BLOCKED",
        "missing closeout not blocked",
    )
    require("source_boundary_cycle_closed_missing" in blocked_cycle["blockers"], "cycle blocker missing")

    mismatch = dict(source)
    source_record = dict(mismatch["memory_overwrite_closeout_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["memory_overwrite_closeout_receipt"] = source_record
    blocked_mismatch = build_truth_authority_authorization_request(
        memory_overwrite_closeout=mismatch
    ).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_memory_overwrite_closeout_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_truth_authority_authorization_request_v0_52.py"
    formal = ROOT / "formal/KUOS/PlanOS/TruthAuthorityAuthorizationRequestV0_52.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_52.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_v0_52.md"
    manifest_path = ROOT / "manifests/kuuos_planos_truth_authority_authorization_request_v0_52.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_truth_authority_authorization_request",
        "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_READY",
        "truth_authority_authorization_request_only",
        "truth_authority_authorization_requested",
        "truth_authority_authorization_granted",
    ))
    require_tokens(formal, (
        "TruthAuthorityAuthorizationRequestSurface",
        "TruthAuthorityAuthorizationRequestBoundary",
        "PlanOSTruthAuthorityAuthorizationRequestBridge",
        "source_closeout_preserves_memory_overwrite_and_keeps_truth_and_release_closed",
        "request_binds_candidate_and_preserves_memory_closeout_state",
        "request_asks_truth_authority_but_does_not_grant_truth_or_blocker_release",
        "boundary_preserves_truth_authority_authorization_request_only",
        "history_appends_one_truth_authority_authorization_request_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.TruthAuthorityAuthorizationRequestV0_52",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.TruthAuthorityAuthorizationRequestV0_52",))
    require_tokens(docs, (
        "PlanOS Truth Authority Authorization Request v0.52",
        "truth authority authorization request only = true",
        "truth authority authorization requested = true",
        "truth authority authorization granted = false",
        "truth authority granted = false",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_truth_authority_authorization_request_v0_52.py",
        "v0.1-v0.52",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v052",))

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
    print("PlanOS truth authority authorization request v0.52 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

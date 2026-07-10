#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_truth_authority_authorization_grant_v0_53 import _ready_truth_authority_request
from runtime.kuuos_planos_truth_authority_authorization_grant_v0_53 import build_truth_authority_authorization_grant
from runtime.kuuos_planos_truth_authority_receipt_v0_54 import (
    SOURCE_VERSION,
    VERSION,
    build_truth_authority_receipt,
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


def _ready_truth_authority_grant() -> dict:
    source = _ready_truth_authority_request()
    return build_truth_authority_authorization_grant(truth_authority_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_truth_authority_grant()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_truth_authority_receipt(truth_authority_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_TRUTH_AUTHORITY_RECEIPT_READY",
        f"receipt blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "cycle closeout not preserved")
    require(
        receipt["boundary"]["truth_authority_authorization_grant_preserved"] is True,
        "authorization grant not preserved",
    )
    require(receipt["boundary"]["truth_authority_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["truth_authority_authorization_granted"] is True, "authorization not preserved")
    require(receipt["boundary"]["truth_authority_granted"] is True, "truth authority not recorded")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["truth_authority_receipt"]
    require(record["memory_overwrite_preserved"] is True, "receipt lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "receipt lost memory closeout")
    require(record["cycle_closed_preserved"] is True, "receipt lost cycle closeout")
    require(record["truth_authority_authorization_granted"] is True, "receipt lost authorization")
    require(record["truth_authority_granted"] is True, "receipt record missing truth authority")
    require(record["blocker_release_ready"] is False, "receipt released blockers")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["truth_authority_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_truth_authority_receipt(truth_authority_grant=promoted).to_dict()
    require(
        blocked["status"] == "PLANOS_TRUTH_AUTHORITY_RECEIPT_BLOCKED",
        "pre-applied truth source not blocked",
    )
    require(
        "source_boundary_truth_authority_granted_promoted" in blocked["blockers"],
        "pre-truth blocker missing",
    )

    release_promoted = dict(source)
    boundary2 = dict(release_promoted["boundary"])
    boundary2["blocker_release_granted"] = True
    release_promoted["boundary"] = boundary2
    blocked_release = build_truth_authority_receipt(truth_authority_grant=release_promoted).to_dict()
    require(
        blocked_release["status"] == "PLANOS_TRUTH_AUTHORITY_RECEIPT_BLOCKED",
        "blocker-release source not blocked",
    )
    require(
        "source_boundary_blocker_release_granted_promoted" in blocked_release["blockers"],
        "blocker release blocker missing",
    )

    mismatch = dict(source)
    grant_record = dict(mismatch["truth_authority_authorization_grant"])
    grant_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["truth_authority_authorization_grant"] = grant_record
    blocked_mismatch = build_truth_authority_receipt(truth_authority_grant=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_TRUTH_AUTHORITY_RECEIPT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_truth_authority_grant_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_truth_authority_receipt_v0_54.py"
    formal = ROOT / "formal/KUOS/PlanOS/TruthAuthorityReceiptV0_54.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_54.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_TRUTH_AUTHORITY_RECEIPT_v0_54.md"
    manifest_path = ROOT / "manifests/kuuos_planos_truth_authority_receipt_v0_54.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_truth_authority_receipt",
        "PLANOS_TRUTH_AUTHORITY_RECEIPT_READY",
        "truth_authority_receipt_only",
        "truth_authority_authorization_granted",
        "truth_authority_granted",
    ))
    require_tokens(formal, (
        "TruthAuthorityReceiptSurface",
        "TruthAuthorityReceiptBoundary",
        "PlanOSTruthAuthorityReceiptBridge",
        "source_grant_authorizes_but_does_not_apply_truth_authority",
        "receipt_binds_candidate_and_preserves_authorized_state",
        "receipt_records_truth_authority_but_not_blocker_release",
        "boundary_preserves_truth_authority_receipt_only",
        "history_appends_one_truth_authority_receipt_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.TruthAuthorityReceiptV0_54",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.TruthAuthorityReceiptV0_54",))
    require_tokens(docs, (
        "PlanOS Truth Authority Receipt v0.54",
        "truth authority receipt only = true",
        "truth authority authorization granted = true",
        "truth authority granted = true",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_truth_authority_receipt_v0_54.py",
        "v0.1-v0.54",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v054",))

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
    print("PlanOS truth authority receipt v0.54 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

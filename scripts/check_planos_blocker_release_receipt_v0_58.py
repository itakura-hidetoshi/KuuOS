#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_blocker_release_authorization_grant_v0_57 import _ready_blocker_release_request
from runtime.kuuos_planos_blocker_release_authorization_grant_v0_57 import (
    build_blocker_release_authorization_grant,
)
from runtime.kuuos_planos_blocker_release_receipt_v0_58 import (
    SOURCE_VERSION,
    VERSION,
    build_blocker_release_receipt,
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


def _ready_blocker_release_grant() -> dict:
    source = _ready_blocker_release_request()
    return build_blocker_release_authorization_grant(blocker_release_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_blocker_release_grant()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_blocker_release_receipt(blocker_release_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_BLOCKER_RELEASE_RECEIPT_READY",
        f"receipt blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["receipt_owned_by_plan_os"] is True, "receipt owner missing")
    require(
        boundary["source_blocker_release_authorization_grant_preserved"] is True,
        "source grant not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_blocker_release_grant"] is True,
        "selected candidate not bound to grant",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        boundary["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(
        boundary["blocker_release_authorization_request_preserved"] is True,
        "blocker release request not preserved",
    )
    require(
        boundary["blocker_release_authorization_grant_preserved"] is True,
        "blocker release grant not preserved",
    )
    require(boundary["blocker_release_receipt_only"] is True, "receipt-only boundary missing")
    require(
        boundary["blocker_release_authorization_requested"] is True,
        "authorization request not preserved",
    )
    require(
        boundary["blocker_release_authorization_granted"] is True,
        "authorization grant not preserved",
    )
    require(boundary["blocker_release_granted"] is True, "blocker release not recorded")
    require(boundary["blocker_release_cycle_closed"] is False, "blocker release cycle closed early")

    record = receipt["blocker_release_receipt"]
    require(record["memory_overwrite_preserved"] is True, "receipt lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "receipt lost memory closeout")
    require(record["truth_authority_preserved"] is True, "receipt lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "receipt lost truth closeout")
    require(record["blocker_release_authorization_requested"] is True, "receipt lost request")
    require(record["blocker_release_authorization_granted"] is True, "receipt lost authorization")
    require(record["blocker_release_granted"] is True, "receipt did not release blockers")
    require(record["blocker_release_cycle_closed"] is False, "receipt closed release cycle")

    promoted = dict(source)
    promoted_boundary = dict(promoted["boundary"])
    promoted_boundary["blocker_release_granted"] = True
    promoted["boundary"] = promoted_boundary
    blocked = build_blocker_release_receipt(blocker_release_grant=promoted).to_dict()
    require(
        blocked["status"] == "PLANOS_BLOCKER_RELEASE_RECEIPT_BLOCKED",
        "pre-released source not blocked",
    )
    require(
        "source_boundary_blocker_release_granted_promoted" in blocked["blockers"],
        "pre-release blocker missing",
    )

    ready_promoted = dict(source)
    grant_record = dict(ready_promoted["blocker_release_authorization_grant"])
    grant_record["blocker_release_ready"] = True
    ready_promoted["blocker_release_authorization_grant"] = grant_record
    blocked_ready = build_blocker_release_receipt(blocker_release_grant=ready_promoted).to_dict()
    require(
        blocked_ready["status"] == "PLANOS_BLOCKER_RELEASE_RECEIPT_BLOCKED",
        "source ready promotion not blocked",
    )
    require(
        "source_record_blocker_release_ready_promoted" in blocked_ready["blockers"],
        "source ready blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["blocker_release_authorization_grant"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["blocker_release_authorization_grant"] = mismatch_record
    blocked_mismatch = build_blocker_release_receipt(blocker_release_grant=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_BLOCKER_RELEASE_RECEIPT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_blocker_release_grant_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_blocker_release_receipt_v0_58.py"
    formal = ROOT / "formal/KUOS/PlanOS/BlockerReleaseReceiptV0_58.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_58.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_BLOCKER_RELEASE_RECEIPT_v0_58.md"
    manifest_path = ROOT / "manifests/kuuos_planos_blocker_release_receipt_v0_58.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_blocker_release_receipt",
        "PLANOS_BLOCKER_RELEASE_RECEIPT_READY",
        "blocker_release_receipt_only",
        "blocker_release_granted",
        "blocker_release_cycle_closed",
    ))
    require_tokens(formal, (
        "BlockerReleaseReceiptSurface",
        "BlockerReleaseReceiptBoundary",
        "PlanOSBlockerReleaseReceiptBridge",
        "source_grant_authorizes_but_does_not_release_blockers",
        "receipt_binds_candidate_and_preserves_authorized_state",
        "receipt_records_blocker_release_but_keeps_cycle_open",
        "boundary_preserves_blocker_release_receipt_only",
        "history_appends_one_blocker_release_receipt_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.BlockerReleaseReceiptV0_58",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.BlockerReleaseReceiptV0_58",))
    require_tokens(docs, (
        "PlanOS Blocker Release Receipt v0.58",
        "blocker release receipt only = true",
        "blocker release granted = true",
        "blocker release cycle closed = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_blocker_release_receipt_v0_58.py",
        "v0.1-v0.58",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v058",))

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
    print("PlanOS blocker release receipt v0.58 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

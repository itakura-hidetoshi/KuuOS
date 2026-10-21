#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_blocker_release_authorization_request_v0_56 import _ready_truth_authority_closeout
from runtime.kuuos_planos_blocker_release_authorization_request_v0_56 import (
    build_blocker_release_authorization_request,
)
from runtime.kuuos_planos_blocker_release_authorization_grant_v0_57 import (
    SOURCE_VERSION,
    VERSION,
    build_blocker_release_authorization_grant,
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


def _ready_blocker_release_request() -> dict:
    source = _ready_truth_authority_closeout()
    return build_blocker_release_authorization_request(truth_authority_closeout=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_blocker_release_request()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_blocker_release_authorization_grant(blocker_release_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_READY",
        f"grant blocked: {receipt.get('blockers')}",
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
        receipt["boundary"]["blocker_release_authorization_request_preserved"] is True,
        "blocker release request not preserved",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_grant_only"] is True,
        "grant-only boundary missing",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_requested"] is True,
        "authorization request not preserved",
    )
    require(
        receipt["boundary"]["blocker_release_authorization_granted"] is True,
        "authorization not granted",
    )
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["blocker_release_authorization_grant"]
    require(record["memory_overwrite_preserved"] is True, "grant lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "grant lost memory closeout")
    require(record["truth_authority_preserved"] is True, "grant lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "grant lost truth closeout")
    require(record["blocker_release_authorization_requested"] is True, "grant lost request")
    require(record["blocker_release_authorization_granted"] is True, "grant record missing authorization")
    require(record["blocker_release_ready"] is False, "grant released blockers")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["blocker_release_authorization_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_blocker_release_authorization_grant(blocker_release_request=promoted).to_dict()
    require(
        blocked["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_BLOCKED",
        "pre-granted source not blocked",
    )
    require(
        "source_boundary_blocker_release_authorization_granted_promoted" in blocked["blockers"],
        "pre-grant blocker missing",
    )

    released = dict(source)
    boundary2 = dict(released["boundary"])
    boundary2["blocker_release_granted"] = True
    released["boundary"] = boundary2
    blocked_release = build_blocker_release_authorization_grant(blocker_release_request=released).to_dict()
    require(
        blocked_release["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_BLOCKED",
        "pre-released source not blocked",
    )
    require(
        "source_boundary_blocker_release_granted_promoted" in blocked_release["blockers"],
        "pre-release blocker missing",
    )

    mismatch = dict(source)
    request_record = dict(mismatch["blocker_release_authorization_request"])
    request_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["blocker_release_authorization_request"] = request_record
    blocked_mismatch = build_blocker_release_authorization_grant(blocker_release_request=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_blocker_release_request_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_blocker_release_authorization_grant_v0_57.py"
    formal = ROOT / "formal/KUOS/PlanOS/BlockerReleaseAuthorizationGrantV0_57.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_57.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_v0_57.md"
    manifest_path = ROOT / "manifests/kuuos_planos_blocker_release_authorization_grant_v0_57.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_blocker_release_authorization_grant",
        "PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_READY",
        "blocker_release_authorization_grant_only",
        "blocker_release_authorization_granted",
        "blocker_release_granted",
    ))
    require_tokens(formal, (
        "BlockerReleaseAuthorizationGrantSurface",
        "BlockerReleaseAuthorizationGrantBoundary",
        "PlanOSBlockerReleaseAuthorizationGrantBridge",
        "source_request_asks_but_does_not_grant_or_apply_release",
        "grant_binds_candidate_and_preserves_closed_truth_state",
        "grant_authorizes_but_does_not_release_blockers",
        "boundary_is_blocker_release_authorization_grant_only",
        "history_appends_one_blocker_release_authorization_grant",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.BlockerReleaseAuthorizationGrantV0_57",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.BlockerReleaseAuthorizationGrantV0_57",))
    require_tokens(docs, (
        "PlanOS Blocker Release Authorization Grant v0.57",
        "blocker release authorization grant only = true",
        "blocker release authorization granted = true",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_blocker_release_authorization_grant_v0_57.py",
        "v0.1-v0.57",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v057",))

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
    print("PlanOS blocker release authorization grant v0.57 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

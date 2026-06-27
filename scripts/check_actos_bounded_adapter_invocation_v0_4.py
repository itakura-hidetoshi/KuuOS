#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_actos_bounded_adapter_invocation_v0_4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSActOSV0_4.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/ActOS/VacuumExpectationBoundedAdapterInvocationV0_4.lean"
    source = ROOT / "formal/KUOS/ActOS/VacuumExpectationActivationAuthorizationIntakeV0_3.lean"
    authority = ROOT / "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean"
    docs = ROOT / "docs/KUUOS_ACTOS_BOUNDED_ADAPTER_INVOCATION_v0_4.md"
    manifest_path = ROOT / "manifests/kuuos_actos_bounded_adapter_invocation_v0_4.json"
    workflow = ROOT / ".github/workflows/evidence-cycle-os-validation.yml"

    for path in (
        formal_root,
        aggregate_root,
        formal,
        source,
        authority,
        docs,
        manifest_path,
        workflow,
    ):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.ActOS.VacuumExpectationBoundedAdapterInvocationV0_4"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(
        formal,
        (
            "ActOSPlanActivationBoundary",
            "ExactAdapterInvocationBinding",
            "AdapterInvocationProjectionBoundary",
            "AdapterInvocationRouteBoundary",
            "CanonicalHostInvocationReceiptBinding",
            "VacuumExpectationBoundedAdapterInvocationBridge",
            "VacuumExpectationBoundedAdapterInvocationReceipt",
            "effect_recorded_route_invokes_once_and_records_once",
            "blocked_route_has_no_call_effect_or_record",
            "replayed_route_is_idempotent_and_starts_no_new_invocation",
            "effect_recorded_preserves_observation_and_verification_debt",
            "invocation_and_host_receipt_do_not_commit_world_or_promote_truth",
            "invocation_digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "VacuumExpectationActivationAuthorizationIntakeReceipt",
            "activation_authorization_is_committed_without_activation_or_effect",
        ),
    )
    require_tokens(
        authority,
        ("BoundedInvocation", "HostReceiptSemantics", "PostEffectDebt"),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_actos_v04",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {field}")

    print("ActOS bounded adapter invocation v0.4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

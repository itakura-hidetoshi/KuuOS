#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_actos_activation_authorization_intake_v0_3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def require_tokens_across(paths: tuple[Path, ...], tokens: tuple[str, ...]) -> None:
    require(bool(paths), "empty module family")
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for token in tokens:
        require(token in text, f"module family missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSActOSV0_3.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/ActOS/VacuumExpectationActivationAuthorizationIntakeV0_3.lean"
    formal_family = tuple(sorted(formal.parent.glob("VacuumExpectationActivationAuthorization*.lean")))
    source = ROOT / "formal/KUOS/PlanOS/VacuumExpectationActivationAdmissionActOSHandoffV0_23.lean"
    source_family = tuple(sorted(source.parent.glob("VacuumExpectationActivationAdmissionActOSHandoff*.lean")))
    authority_v01 = ROOT / "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean"
    authority_v02 = ROOT / "formal/KUOS/ActOS/ReplanLineageAuthorityEnvelopeV0_2.lean"
    docs = ROOT / "docs/KUUOS_ACTOS_ACTIVATION_AUTHORIZATION_INTAKE_v0_3.md"
    manifest_path = ROOT / "manifests/kuuos_actos_activation_authorization_intake_v0_3.json"
    workflow = ROOT / ".github/workflows/actos-authorization-intake-v0-3.yml"

    for path in (
        formal_root,
        aggregate_root,
        formal,
        source,
        authority_v01,
        authority_v02,
        docs,
        manifest_path,
        workflow,
        *formal_family,
        *source_family,
    ):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.ActOS.«VacuumExpectationActivationAuthorizationIntakeV0_3»"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens_across(
        formal_family,
        (
            "IndependentActFreshnessRevalidation",
            "CapabilityRegistryConfirmation",
            "LeaseUseReservationBoundary",
            "SessionIntentReplayBoundary",
            "StagedEffectAuthorizationBoundary",
            "ActivationAuthorizationReceiptBoundary",
            "VacuumExpectationActivationAuthorizationIntakeBridge",
            "VacuumExpectationActivationAuthorizationIntakeReceipt",
            "intake_requires_committed_nonexecuting_planos_handoff",
            "exact_act_cycle_revalidates_planos_target",
            "fivefold_binding_is_complete",
            "selected_step_is_effectful_and_safety_bound",
            "freshness_is_independently_revalidated",
            "registry_entry_is_present_unrevoked_and_exact",
            "lease_reservation_consumes_exactly_one_remaining_use",
            "lease_reservation_is_replay_safe",
            "session_and_intent_are_fresh_distinct_and_nonreplayed",
            "authorization_is_single_use_and_cannot_widen_license",
            "staged_effect_remains_projected_and_noninvoked",
            "activation_authorization_is_committed_without_activation_or_effect",
            "act_events_append_strictly_from_planos_handoff",
            "act_history_appends_three_records",
            "bridge_preserves_actos_ownership",
            "bridge_grants_no_activation_invocation_or_effect",
            "authorization_digest_is_exact",
        ),
    )
    require_tokens_across(
        source_family,
        (
            "VacuumExpectationActivationAdmissionActOSHandoffReceipt",
            "handoff_is_not_activation_authorization_or_execution",
        ),
    )
    require_tokens(
        authority_v01,
        (
            "FivefoldBinding",
            "SelectedActStep",
            "AuthorizationBoundary",
            "LowerAuthorityBoundary",
            "ActEventIndex",
            "ActHistory",
        ),
    )
    require_tokens(
        authority_v02,
        (
            "ExactActCycleGate",
            "AuthorizationEnvelopeBoundary",
        ),
    )
    require_tokens(
        docs,
        (
            "remaining uses after + 1 = remaining uses before",
            "activation authorized",
            "plan activated = false",
            "adapter invoked = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_actos_v03",),
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

    print("ActOS activation authorization intake v0.3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

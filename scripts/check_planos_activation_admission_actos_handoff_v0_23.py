#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_activation_admission_actos_handoff_v0_23"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_23.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationActivationAdmissionActOSHandoffV0_23.lean"
    source = ROOT / "formal/KUOS/PlanOS/VacuumExpectationCompilerMaterializationV0_22.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_ACTIVATION_ADMISSION_ACTOS_HANDOFF_v0_23.md"
    manifest_path = ROOT / "manifests/kuuos_planos_activation_admission_actos_handoff_v0_23.json"
    workflow = ROOT / ".github/workflows/plan-os-validation.yml"

    for path in (formal_root, aggregate_root, formal, source, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.«VacuumExpectationActivationAdmissionActOSHandoffV0_23»"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(
        formal,
        (
            "ActivationMaterialFreshness",
            "ActivationAdmissionBinding",
            "ActivationAdmissionReceiptBoundary",
            "ActOSHandoffBoundary",
            "VacuumExpectationActivationAdmissionActOSHandoffBridge",
            "VacuumExpectationActivationAdmissionActOSHandoffReceipt",
            "requires_materialized_non_hold_candidate",
            "requires_exact_next_cycle_and_fresh_epoch",
            "requires_fresh_generation_material",
            "requires_complete_authority_binding",
            "requires_exact_scope_and_effect_concordance",
            "intent_is_distinct_and_staged_only",
            "admission_does_not_activate_invoke_or_execute",
            "handoff_preserves_material_identity_cycle_and_authority",
            "handoff_is_not_activation_authorization_or_execution",
            "events_append_strictly",
            "history_appends_two_records",
            "bridge_preserves_ownership",
            "bridge_grants_no_activation_execution_or_commit",
            "digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "VacuumExpectationCompilerMaterializationReceipt",
            "hold_materializes_zero_executable_steps",
            "materialization_is_single_use_and_replay_safe",
        ),
    )
    require_tokens(
        docs,
        (
            "selected candidate != hold",
            "action intent distinct from decision = true",
            "admittedはactivatedを意味しない",
            "activation authorization owner = ActOS",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v023",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    print("PlanOS activation admission ActOS handoff v0.23 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

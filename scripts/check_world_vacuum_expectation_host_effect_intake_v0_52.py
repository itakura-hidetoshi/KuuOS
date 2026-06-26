#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "world_vacuum_expectation_host_effect_intake_v0_52"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/VacuumExpectationHostEffectAtomicCommitIntakeV0_52.lean"
    formal_root = ROOT / "formal/KuuOSFormalV0_52.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KU_WORLD_HOST_EFFECT_INTAKE_v0_52.md"
    manifest_path = ROOT / "manifests/world_vacuum_expectation_host_effect_intake_v0_52.json"
    workflow = ROOT / ".github/workflows/world-host-effect-intake-v0-52.yml"

    for path in (formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.WORLD.VacuumExpectationHostEffectAtomicCommitIntakeV0_52"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(ROOT / "formal/KUOS.lean", (import_token,))
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_52",))
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge",
            "WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope",
            "intake_requires_canonical_effect_record",
            "candidate_preserves_effect_identity",
            "observeos_source_binding_is_complete",
            "evidence_requirements_are_complete",
            "provenance_is_complete_and_immutable",
            "observation_and_verification_debts_remain_unpaid",
            "atomic_commit_prerequisites_are_explicit_but_unsupplied",
            "intake_is_not_atomic_commit",
            "pending_debt_forbids_automatic_promotion_completion_or_rollback",
            "intake_history_appends_one_record",
            "intake_index_follows_host_receipt",
            "ownership_boundaries_are_preserved",
            "intake_grants_no_truth_causality_observation_verification_or_execution",
            "intake_digest_is_exact",
        ),
    )
    require_tokens(
        docs,
        (
            "host route = effectRecorded",
            "observation committed = false",
            "verification committed = false",
            "WORLD update ready = false",
            "WORLD update performed = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_world_v052",),
    )
    require_tokens(
        ROOT / ".github/workflows/kuuos_runtime_full_check.yml",
        ("Run cumulative runtime full check", "run_kuuos_runtime_full_check_v0_55.py"),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["manifest_version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_root"] == str(formal_root.relative_to(ROOT)), "formal root mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for boundary in (
        "observation_debt_unpaid",
        "verification_debt_unpaid",
        "verified_disposition_not_yet_supplied",
        "world_update_not_ready",
        "world_update_not_performed",
    ):
        require(boundary in manifest["boundaries"], f"missing boundary: {boundary}")

    print("WORLD host-effect intake v0.52 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

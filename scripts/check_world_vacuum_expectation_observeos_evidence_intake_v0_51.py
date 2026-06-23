#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main() -> int:
    formal = (
        ROOT
        / "formal/KUOS/WORLD/VacuumExpectationObserveOSEvidenceIntakeBridgeV0_51.lean"
    )
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationObserveOSEvidenceIntakeBridge",
            "VacuumExpectationObserveOSEvidenceEnvelope",
            "envelopeOfCandidate",
            "envelope_candidate_value_exact",
            "envelope_candidate_source_exact",
            "envelope_digest_binding_exact",
            "envelope_evidence_requirements_complete",
            "envelope_provenance_complete",
            "envelope_preserves_verification_debt",
            "intake_ownership_boundary_preserved",
            "intake_grants_no_truth_verification_or_execution_authority",
            "runtime_remains_read_only",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_51.lean",
        ("VacuumExpectationObserveOSEvidenceIntakeBridgeV0_51",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.VacuumExpectationObserveOSEvidenceIntakeBridgeV0_51",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_51",))
    require_tokens(
        ROOT / "docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVEOS_EVIDENCE_INTAKE_v0_51.md",
        (
            "intake-ready envelope != committed observation",
            "observation != verification",
            "WORLD sidecar != observation owner",
            "runtime remains read-only",
        ),
    )
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar             v0.51",
            "intake-ready envelope != committed observation",
            "run_kuuos_runtime_full_check_v0_51.py",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "implemented through v0.51",
            "ObserveOS evidence-intake envelope",
            "Strengthen WORLD v0.51 proof status",
        ),
    )

    manifest_path = (
        ROOT / "manifests/world_vacuum_expectation_observeos_evidence_intake_v0_51.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert (
        manifest["manifest_version"]
        == "world_vacuum_expectation_observeos_evidence_intake_v0_51"
    )
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_51.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert "verification_debt_preserved" in manifest["boundaries"]
    assert "world_sidecar_not_observation_owner" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "envelope_evidence_requirements_complete" in manifest["derived_results"]

    print("world_vacuum_expectation_observeos_evidence_intake_v0_51 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

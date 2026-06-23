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
        / "formal/KUOS/WORLD/VacuumExpectationObserveOSCommitVerifyOSHandoffBridgeV0_52.lean"
    )
    require_tokens(
        formal,
        (
            "WorldAnalyticSourceObservationBinding",
            "sourceClassAnalytic",
            "sourceEffectBound",
            "effectReclassificationForbidden",
            "WorldVacuumExpectationObserveOSCommitVerifyHandoffBridge",
            "VacuumExpectationObserveOSCommitReceipt",
            "VacuumExpectationVerifyOSHandoff",
            "commitReceiptOfEnvelope",
            "verifyHandoffOfCommit",
            "commit_receipt_exact",
            "commit_requires_explicit_evidence",
            "observe_commit_owner_and_recorded",
            "verify_handoff_requires_explicit_evidence",
            "verify_handoff_source_ready",
            "verify_handoff_preserves_analytic_source_identity",
            "verify_handoff_uses_exact_observe_cycle",
            "handoff_preserves_open_verification_debt",
            "verify_handoff_grants_no_authority",
            "runtime_remains_read_only",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_52.lean",
        ("VacuumExpectationObserveOSCommitVerifyOSHandoffBridgeV0_52",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.VacuumExpectationObserveOSCommitVerifyOSHandoffBridgeV0_52",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_52",))
    require_tokens(
        ROOT / "docs/KU_WORLD_OBSERVEOS_COMMIT_VERIFYOS_HANDOFF_v0_52.md",
        (
            "commit evidence is required",
            "analytic source != ActOS effect observation",
            "VerifyOS handoff != verification execution",
            "verification debt remains open",
            "runtime remains read-only",
        ),
    )
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar             v0.52",
            "commit receipt != verification result",
            "run_kuuos_runtime_full_check_v0_52.py",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "implemented through v0.52",
            "ObserveOS commit and VerifyOS handoff",
            "Strengthen WORLD v0.52 proof status",
        ),
    )

    manifest_path = ROOT / "manifests/world_observeos_commit_verifyos_handoff_v0_52.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_observeos_commit_verifyos_handoff_v0_52"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_52.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert "analytic_source_not_actos_effect_observation" in manifest["boundaries"]
    assert "explicit_observeos_commit_evidence_required" in manifest["boundaries"]
    assert "explicit_verifyos_handoff_evidence_required" in manifest["boundaries"]
    assert "verification_debt_preserved" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "verify_handoff_preserves_analytic_source_identity" in manifest["derived_results"]

    print("world_observeos_commit_verifyos_handoff_v0_52 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

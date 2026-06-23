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
        / "formal/KUOS/WORLD/VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52.lean"
    )
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationObserveOSCommitVerifyHandoffBridge",
            "VacuumExpectationObserveOSCommitReceipt",
            "VacuumExpectationVerifyOSHandoffReceipt",
            "observe_commit_source_exact",
            "observe_commit_is_recorded_but_not_verification",
            "observe_commit_ownership_preserved",
            "verify_handoff_source_exact",
            "verify_handoff_is_ready_but_not_started",
            "verify_handoff_preserves_challenge_surface",
            "bridge_ownership_boundary_preserved",
            "bridge_grants_no_observe_or_verify_authority",
            "runtime_remains_read_only",
            "committedByWorld",
            "verificationStarted",
            "verificationResultCreated",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_52.lean",
        ("VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_52",))
    require_tokens(
        ROOT / "docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVEOS_COMMIT_VERIFY_HANDOFF_v0_52.md",
        (
            "validated commit receipt != WORLD performed commit",
            "verification handoff != verification start",
            "verification start != verification result",
            "WORLD sidecar != VerifyOS owner",
            "runtime remains read-only",
        ),
    )
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar             v0.52",
            "verification handoff != verification start",
            "run_kuuos_runtime_full_check_v0_52.py",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "implemented through v0.52",
            "ObserveOS commit receipt",
            "Strengthen WORLD v0.52 proof status",
        ),
    )

    manifest_path = (
        ROOT
        / "manifests/world_vacuum_expectation_observeos_commit_verify_handoff_v0_52.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert (
        manifest["manifest_version"]
        == "world_vacuum_expectation_observeos_commit_verify_handoff_v0_52"
    )
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_52.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert "validated_receipt_not_world_performed_commit" in manifest["boundaries"]
    assert "verification_handoff_not_verification_start" in manifest["boundaries"]
    assert "verification_start_not_verification_result" in manifest["boundaries"]
    assert "world_not_verifyos_owner" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "verify_handoff_source_exact" in manifest["derived_results"]

    print("world_vacuum_expectation_observeos_commit_verify_handoff_v0_52 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

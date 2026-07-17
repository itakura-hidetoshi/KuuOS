#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def require_tokens_across(
    paths: tuple[pathlib.Path, ...], tokens: tuple[str, ...]
) -> None:
    texts = {
        path: path.read_text(encoding="utf-8")
        for path in paths
    }
    for token in tokens:
        assert any(token in text for text in texts.values()), (
            f"{', '.join(str(path) for path in paths)}: {token}"
        )


def require_composition_boundary(paths: tuple[pathlib.Path, ...]) -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    exact_boundary = "receipt composition != receipt construction"
    rolling_summary_boundary = (
        "OS receipt composition" in text
        and "receipt != successor authority" in text
    )
    assert exact_boundary in text or rolling_summary_boundary, (
        f"{', '.join(str(path) for path in paths)}: missing exact "
        "receipt-composition boundary or rolling entry-document "
        "composition/non-authority coverage"
    )


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_53.lean"
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationOSReceiptCompositionBridge",
            "VacuumExpectationOSReceiptComposition",
            "composition_lineage_digest_exact",
            "observe_stage_composes_exactly",
            "verification_stage_composes_exactly",
            "learning_stage_is_future_only",
            "os_ownership_boundary_preserved",
            "composed_candidate_value_remains_exact",
            "composition_preserves_non_authority",
            "runtime_remains_read_only",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_53.lean",
        ("VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_53",),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormal.lean",
        ("KUOS.WORLD.VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_53",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_53",))
    require_tokens(
        ROOT / "docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVEOS_COMMIT_VERIFY_HANDOFF_v0_53.md",
        (
            "receipt composition != receipt construction",
            "verification result != truth",
            "learning receipt != current-cycle mutation",
            "OS receipt composition != host-effect atomic-commit intake",
            "runtime remains read-only",
        ),
    )

    # Repository entry documents are intentionally layered. The root README
    # carries repository-wide fixed points, while docs/ObserveOS/README.md is
    # the structured subsystem index. Durable ObserveOS composition boundaries
    # may live in either document without duplicating all historical detail.
    entry_docs = (
        ROOT / "README.md",
        ROOT / "docs/ObserveOS/README.md",
    )
    require_composition_boundary(entry_docs)
    require_tokens_across(
        entry_docs,
        (
            "WORLD sidecar != exact WORLD",
            "observation != verification",
            "learning != present-cycle mutation",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "OS receipt composition",
            "WORLD sidecar != exact WORLD",
            "WORLD commit != truth",
        ),
    )

    manifest_path = ROOT / "manifests/world_vacuum_expectation_observeos_commit_verify_handoff_v0_53.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_vacuum_expectation_observeos_commit_verify_handoff_v0_53"
    assert manifest["status"] == "formal_read_only_os_receipt_composition_bridge"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_53.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert manifest["predecessor_full_check"] == "scripts/run_kuuos_runtime_full_check_v0_52.py"
    assert len(manifest["composes_existing_modules"]) == 3
    assert "receipt_composition_not_receipt_construction" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "composition_lineage_digest_exact" in manifest["derived_results"]

    print("world_vacuum_expectation_os_receipt_composition_v0_53 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

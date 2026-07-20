#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    STATUS_READY,
)
from runtime.kuuos_codeai_version_bound_repair_memory_v0_1 import (
    build_codeai_version_bound_repair_memory,
)
from scripts.build_codeai_version_bound_repair_memory_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    spec = load("examples/codeai_version_bound_repair_memory_v0_1.json")
    fixture = build_fixture(
        spec,
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )
    result = build_codeai_version_bound_repair_memory(
        source_classification=fixture["source_classification"],
        source_classification_receipt=fixture["source_classification_receipt"],
        repair_evidence_packet=fixture["repair_evidence_packet"],
        memory_request=fixture["memory_request"],
        memory_policy=fixture["memory_policy"],
    )
    if result.status != STATUS_READY or result.snapshot is None or result.receipt is None:
        raise SystemExit("version-bound repair memory blocked: " + ",".join(result.issues))
    snapshot = result.snapshot
    expected = {
        "memory_entry_count": spec["expected_memory_entry_count"],
        "matched_entry_count": spec["expected_matched_entry_count"],
        "excluded_entry_count": spec["expected_excluded_entry_count"],
        "recommendation": spec["expected_recommendation"],
    }
    actual = {key: snapshot[key] for key in expected}
    if actual != expected:
        raise SystemExit(
            f"version-bound repair memory mismatch: expected={expected!r} actual={actual!r}"
        )
    if not snapshot["matched_entries"]:
        raise SystemExit("reference fixture must expose one exact version-bound hint")
    matched = snapshot["matched_entries"][0]
    if matched["toolchain_digest"] != snapshot["query_version_binding"]["toolchain_digest"]:
        raise SystemExit("matched repair hint is not toolchain-bound")
    if any(
        snapshot[field]
        for field in (
            "repair_executed_by_memory",
            "repository_mutation_performed_by_memory",
            "git_effect_performed_by_memory",
            "repair_authority_granted",
            "verification_authority_granted",
            "execution_authority_granted",
            "git_authority_granted",
            "historical_outcome_treated_as_probability",
            "historical_success_treated_as_future_success_proof",
            "memory_hint_treated_as_correctness_proof",
            "version_mismatch_treated_as_transferable",
        )
    ):
        raise SystemExit("repair memory crossed an authority, effect, or truth boundary")
    print(
        "CodeAI Version-Bound Repair Memory v0.1: "
        f"{snapshot['memory_entry_count']} entries, "
        f"{snapshot['matched_entry_count']} exact match, "
        f"{snapshot['excluded_entry_count']} excluded, "
        f"recommendation={snapshot['recommendation']}"
    )


if __name__ == "__main__":
    main()

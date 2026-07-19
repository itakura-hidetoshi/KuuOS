#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_autonomous_git_effect_reobservation,
    canonical_digest,
)
from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    _validate_state as validate_lifecycle_state,
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    fixture = json.loads(
        (root / "examples/codeai_autonomous_git_effect_reobservation_v0_1.json").read_text()
    )
    result = build_codeai_autonomous_git_effect_reobservation(
        source_lifecycle_receipt=fixture["source_lifecycle_receipt"],
        source_execution_receipt=fixture["source_execution_receipt"],
        source_execution_evidence=fixture["source_execution_evidence"],
        reobservation_request=fixture["reobservation_request"],
        reobservation_policy=fixture["reobservation_policy"],
        reobservation_registry=fixture["reobservation_registry"],
        adapter=lambda _invocation: fixture["adapter_result"],
    )
    assert result.status == STATUS_READY, result.issues
    assert result.receipt is not None
    assert result.lifecycle_state is not None
    expected = fixture["expected"]
    assert result.receipt["codeai_disposition"] == expected["codeai_disposition"]
    assert result.receipt["fresh_lifecycle_state_issued"] is expected["fresh_lifecycle_state_issued"]
    assert result.lifecycle_state["merge_performed"] is expected["merge_performed"]
    assert validate_lifecycle_state(result.lifecycle_state) == []
    for field in (
        "automatic_successor_effect_authority_granted",
        "general_git_authority_granted",
        "general_successor_stage_authority_granted",
    ):
        assert result.receipt[field] is expected[field]
    receipt_without_digest = {
        key: value for key, value in result.receipt.items() if key != RECEIPT_DIGEST_FIELD
    }
    assert result.receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(receipt_without_digest)
    assert result.next_registry is not None
    assert result.next_registry["registry_revision"] == fixture["reobservation_registry"]["registry_revision"] + 1
    assert result.next_registry["consumed_count"] == fixture["reobservation_registry"]["consumed_count"] + 1
    print("CodeAI Autonomous Git Effect Re-observation v0.1: PASS")
    print("fresh lifecycle state: existing lifecycle validator accepted")
    print("source execution receipt and nonce: consumed exactly once")
    print("Git/network/secret/deployment effects: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

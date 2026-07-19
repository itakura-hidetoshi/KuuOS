#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    DISPOSITION_CONSUMED,
    EVIDENCE_DIGEST_FIELD,
    EXECUTION_INPUT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_durable_git_lifecycle_loop_resumption_consumption,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import (
    canonical_digest,
)
from tests.test_kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    valid_inputs,
)


def digest_ok(value: dict, field: str) -> bool:
    return value[field] == canonical_digest({k: v for k, v in value.items() if k != field})


def main() -> int:
    values = valid_inputs()
    result = build_codeai_durable_git_lifecycle_loop_resumption_consumption(**values)
    assert result.status == STATUS_READY, result.issues
    assert result.issues == ()
    assert result.execution_input is not None
    assert result.evidence is not None
    assert result.next_registry is not None
    assert result.receipt is not None

    execution_input = result.execution_input
    evidence = result.evidence
    registry = result.next_registry
    receipt = result.receipt

    assert digest_ok(execution_input, EXECUTION_INPUT_DIGEST_FIELD)
    assert digest_ok(evidence, EVIDENCE_DIGEST_FIELD)
    assert digest_ok(registry, REGISTRY_DIGEST_FIELD)
    assert digest_ok(receipt, RECEIPT_DIGEST_FIELD)

    assert execution_input["one_shot"] is True
    assert execution_input["reusable"] is False
    assert execution_input["active_now"] is True
    assert execution_input["loop_execution_authorized"] is True
    assert execution_input["direct_git_effect_authorized"] is False
    assert execution_input["automatic_execution_authorized"] is False
    assert execution_input["network_access_authorized"] is False
    assert execution_input["secret_material_read_authorized"] is False
    assert execution_input["general_git_authority_granted"] is False
    assert execution_input["general_successor_stage_authority_granted"] is False

    assert registry["registry_revision"] == 1
    assert registry["successful_consumption_count"] == 1
    assert len(registry["consumed_consumption_nonce_digests"]) == 1
    assert len(registry["consumed_resumption_receipt_digests"]) == 1
    assert len(registry["consumed_resume_input_digests"]) == 1
    assert registry["issued_execution_input_digests"] == [
        execution_input[EXECUTION_INPUT_DIGEST_FIELD]
    ]

    assert receipt["codeai_disposition"] == DISPOSITION_CONSUMED
    assert receipt["source_resumption_bundle_verified"] is True
    assert receipt["source_resume_input_verified"] is True
    assert receipt["consumption_nonce_consumed"] is True
    assert receipt["consumption_registry_advanced_once"] is True
    assert receipt["resume_input_consumed"] is True
    assert receipt["execution_input_issued"] is True
    assert receipt["execution_input_one_shot"] is True
    assert receipt["execution_input_reusable"] is False
    assert receipt["execution_input_active"] is True
    assert receipt["loop_execution_authorized_for_successor"] is True

    for field in (
        "direct_git_effect_authorized",
        "automatic_execution_authorized",
        "loop_execution_performed",
        "git_effect_performed",
        "automatic_resumption_performed",
        "network_accessed",
        "secret_material_read",
        "general_git_authority_granted",
        "general_successor_stage_authority_granted",
    ):
        assert receipt[field] is False, field

    blocked = valid_inputs()
    blocked["consumption_registry"]["consumed_resume_input_digests"] = [
        blocked["consumption_request"]["source_resume_input_digest"]
    ]
    blocked["consumption_registry"]["consumed_consumption_nonce_digests"] = ["3" * 64]
    blocked["consumption_registry"]["consumed_resumption_receipt_digests"] = ["4" * 64]
    blocked["consumption_registry"]["issued_execution_input_digests"] = ["5" * 64]
    blocked["consumption_registry"]["registry_revision"] = 1
    blocked["consumption_registry"]["successful_consumption_count"] = 1
    blocked["consumption_registry"].pop(REGISTRY_DIGEST_FIELD)
    blocked["consumption_registry"][REGISTRY_DIGEST_FIELD] = canonical_digest(
        blocked["consumption_registry"]
    )
    replay = build_codeai_durable_git_lifecycle_loop_resumption_consumption(**blocked)
    assert replay.status != STATUS_READY
    assert replay.execution_input is None
    assert replay.next_registry is None

    print("CodeAI durable Git lifecycle loop resumption consumption v0.1: passed")
    print("fresh admitted resume input -> one active one-shot bounded loop execution input")
    print("replay, direct Git effect, automatic execution, network, secret, and general authority: denied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

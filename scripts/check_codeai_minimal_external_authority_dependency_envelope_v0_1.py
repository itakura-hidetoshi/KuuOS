#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1 as m

EXAMPLE_PATH = (
    "examples/codeai_minimal_external_authority_dependency_envelope_v0_1.json"
)


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def reseal_source(value: dict) -> dict:
    return m.seal(value, m.SOURCE_RECEIPT_DIGEST_FIELD)


def reseal_request(value: dict) -> dict:
    return m.seal(value, m.REQUEST_DIGEST_FIELD)


def reseal_state(value: dict) -> dict:
    return m.seal(value, m.STATE_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def bind_effect(
    request: dict,
    state: dict,
    *,
    kind: str,
    target: str,
    action: str,
    artifact_digest: str = "",
) -> tuple[dict, dict]:
    request = deepcopy(request)
    state = deepcopy(state)
    request["requested_effect_kind"] = kind
    request["requested_effect_count"] = 0 if kind == m.KIND_NONE else 1
    request["effect_target"] = target
    request["effect_action"] = action
    request["artifact_digest"] = artifact_digest
    if kind == m.KIND_NONE:
        request["effect_scope_digest"] = ""
        request["effect_payload_digest"] = ""
    state["requested_effect_kind"] = kind
    state["effect_target"] = target
    state["effect_action"] = action
    state["effect_scope_digest"] = request["effect_scope_digest"]
    return reseal_request(request), reseal_state(state)


def without_internal_substitute(request: dict, *, critical: bool = True) -> dict:
    request = deepcopy(request)
    request["internal_substitute_available"] = False
    request["critical_path_required"] = critical
    return reseal_request(request)


def with_capability(
    state: dict,
    request: dict,
    *,
    kind: str,
    expires_epoch: int = 7050,
) -> dict:
    state = deepcopy(state)
    state["preauthorized_capability_present"] = True
    state["capability_kind"] = kind
    state["capability_handle_digest"] = "3" * 64
    state["capability_scope_digest"] = request["effect_scope_digest"]
    state["capability_expires_epoch"] = expires_epoch
    state["capability_one_shot"] = True
    return reseal_state(state)


def with_packet(state: dict) -> dict:
    state = deepcopy(state)
    state["external_request_packet_prepared"] = True
    state["external_request_packet_digest"] = "4" * 64
    state["external_request_packet_count"] = 1
    return reseal_state(state)


def with_failure(state: dict) -> dict:
    state = deepcopy(state)
    state["external_effect_failed"] = True
    state["failure_evidence_digest"] = "5" * 64
    return reseal_state(state)


def with_external_success(state: dict, *, deploy: bool = False) -> dict:
    state = deepcopy(state)
    state["external_effect_observed"] = True
    state["external_effect_receipt_digest"] = "6" * 64
    state["deployment_performed"] = deploy
    return reseal_state(state)


def route(source: dict, request: dict, state: dict, policy: dict) -> dict:
    result = m.build_codeai_minimal_external_authority_dependency_envelope(
        source_git_lifecycle_receipt=source,
        dependency_request=request,
        dependency_state=state,
        dependency_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    grants = (
        receipt["internal_substitute_authority_granted"],
        receipt["internal_continuation_authority_granted"],
        receipt["deployment_authority_granted"],
        receipt["secret_mutation_authority_granted"],
        receipt["external_request_packet_authority_granted"],
    )
    assert sum(grants) <= 1
    assert receipt["execution_lease_issued"] is (sum(grants) == 1)
    assert receipt["external_effect_lease_issued"] is (
        receipt["deployment_authority_granted"]
        or receipt["secret_mutation_authority_granted"]
    )
    assert receipt["human_handover_authority_granted"] is False
    assert receipt["secret_access_authority_granted"] is False
    assert receipt["capability_handle_exposed"] is False
    assert receipt["blocking_handover_allowed"] is False
    assert receipt["effect_execution_performed_by_kernel"] is False
    assert receipt["source_receipt_treated_as_external_authority"] is False
    assert receipt["external_result_treated_as_truth"] is False
    return receipt


def build_route_cases(example: dict) -> list[tuple[str, dict, dict, dict, dict]]:
    source = example["source_git_lifecycle_receipt"]
    request = example["dependency_request"]
    state = example["dependency_state"]
    policy = example["dependency_policy"]
    cases: list[tuple[str, dict, dict, dict, dict]] = []

    bad_source = deepcopy(source)
    bad_source["profile_version"] = "unsupported"
    cases.append(
        (m.DISPOSITION_SOURCE_REPAIR, reseal_source(bad_source), request, state, policy)
    )

    bad_request = deepcopy(request)
    bad_request["provenance_integrity_confirmed"] = False
    cases.append(
        (
            m.DISPOSITION_PROVENANCE_REPAIR,
            source,
            reseal_request(bad_request),
            state,
            policy,
        )
    )

    bad_state = deepcopy(state)
    bad_state["preauthorized_capability_present"] = True
    bad_state["capability_kind"] = m.KIND_DEPLOY
    bad_state["capability_handle_digest"] = "bad"
    bad_state["capability_scope_digest"] = request["effect_scope_digest"]
    bad_state["capability_expires_epoch"] = 7050
    bad_state["capability_one_shot"] = True
    cases.append(
        (
            m.DISPOSITION_STATE_EVIDENCE_REPAIR,
            source,
            request,
            reseal_state(bad_state),
            policy,
        )
    )

    mismatch = deepcopy(state)
    mismatch["effect_target"] = "human-authority"
    cases.append(
        (
            m.DISPOSITION_CORRESPONDENCE_REPAIR,
            source,
            request,
            reseal_state(mismatch),
            policy,
        )
    )

    stale_policy = deepcopy(policy)
    stale_policy["evaluation_epoch"] = 7200
    cases.append(
        (
            m.DISPOSITION_WINDOW_REPAIR,
            source,
            request,
            state,
            reseal_policy(stale_policy),
        )
    )

    replay = deepcopy(request)
    replay["prior_execution_session_ids"].append(request["execution_session_id"])
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            source,
            reseal_request(replay),
            state,
            policy,
        )
    )

    unsupported_request = deepcopy(request)
    unsupported_state = deepcopy(state)
    unsupported_request["effect_target"] = "production"
    unsupported_state["effect_target"] = "production"
    cases.append(
        (
            m.DISPOSITION_SCOPE_ABSTAINED,
            source,
            reseal_request(unsupported_request),
            reseal_state(unsupported_state),
            policy,
        )
    )

    plaintext = deepcopy(request)
    plaintext["plaintext_secret_requested"] = True
    cases.append(
        (
            m.DISPOSITION_PLAINTEXT_SECRET_REJECTED,
            source,
            reseal_request(plaintext),
            state,
            policy,
        )
    )

    unowned = deepcopy(state)
    unowned["human_handover_performed"] = True
    cases.append(
        (
            m.DISPOSITION_UNOWNED_EFFECT_REJECTED,
            source,
            request,
            reseal_state(unowned),
            policy,
        )
    )

    inconsistent = deepcopy(state)
    inconsistent["external_effect_observed"] = True
    cases.append(
        (
            m.DISPOSITION_STATE_REPAIR,
            source,
            request,
            reseal_state(inconsistent),
            policy,
        )
    )

    cases.append((m.DISPOSITION_INTERNAL_SUBSTITUTE, source, request, state, policy))

    continuation_request = without_internal_substitute(request, critical=False)
    cases.append(
        (
            m.DISPOSITION_INTERNAL_CONTINUATION,
            source,
            continuation_request,
            state,
            policy,
        )
    )

    deploy_request = without_internal_substitute(request)
    deploy_state = with_capability(
        state, deploy_request, kind=m.KIND_DEPLOY
    )
    cases.append(
        (
            m.DISPOSITION_DEPLOY_AUTHORIZED,
            source,
            deploy_request,
            deploy_state,
            policy,
        )
    )

    secret_request, secret_state = bind_effect(
        request,
        state,
        kind=m.KIND_SECRET_MUTATION,
        target="ci-signing-key",
        action="rotate_version",
    )
    secret_request = without_internal_substitute(secret_request)
    secret_state = with_capability(
        secret_state, secret_request, kind=m.KIND_SECRET_MUTATION
    )
    cases.append(
        (
            m.DISPOSITION_SECRET_MUTATION_AUTHORIZED,
            source,
            secret_request,
            secret_state,
            policy,
        )
    )

    packet_request = without_internal_substitute(request)
    cases.append(
        (
            m.DISPOSITION_PACKET_AUTHORIZED,
            source,
            packet_request,
            state,
            policy,
        )
    )

    cases.append(
        (
            m.DISPOSITION_PENDING_HOLD,
            source,
            packet_request,
            with_packet(state),
            policy,
        )
    )

    cases.append(
        (
            m.DISPOSITION_FAILED_DEGRADED,
            source,
            packet_request,
            with_failure(state),
            policy,
        )
    )

    cases.append(
        (
            m.DISPOSITION_COMPLETED,
            source,
            packet_request,
            with_external_success(state, deploy=True),
            policy,
        )
    )
    return cases


def main() -> None:
    example = load_example()
    observed: set[str] = set()
    for expected, source, request, state, policy in build_route_cases(example):
        receipt = route(source, request, state, policy)
        actual = receipt["codeai_disposition"]
        assert actual == expected, (expected, actual)
        observed.add(actual)
    expected = {
        value
        for name, value in vars(m).items()
        if name.startswith("DISPOSITION_") and isinstance(value, str)
    }
    assert observed == expected, (sorted(observed), sorted(expected))
    print(
        "CodeAI Minimal External Authority Dependency Envelope v0.1: "
        f"{len(observed)} routes validated"
    )


if __name__ == "__main__":
    main()

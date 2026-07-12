#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DIGEST_FIELD = "actos_dukkha_preserving_bounded_adapter_invocation_receipt_digest"
RECEIPT_DIGEST_FIELD = "actos_dukkha_preserving_effect_commit_authorization_intake_receipt_digest"

DISPOSITION_READY = "effect_commit_authorization_ready"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_REVERIFY = "effect_reverification_required"
DISPOSITION_CHECKPOINT = "checkpoint_review_required"
DISPOSITION_OBSERVATION_REPAIR = "observation_route_repair_required"
DISPOSITION_VERIFICATION_REPAIR = "verification_route_repair_required"
DISPOSITION_COMPENSATION_REPAIR = "compensation_route_repair_required"
DISPOSITION_SCOPE_REPAIR = "effect_scope_repair_required"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

SOURCE_STATE = "invoked_effect_not_committed"
REVIEW_SUPPORTED = "dukkha_preserving_effect_commit_supported"

REVIEW_FIELDS = {
    "source_invocation_receipt_digest",
    "adapter_result_envelope_digest",
    "invocation_record_digest",
    "review_disposition",
    "dukkha_reduction_support_status",
    "protected_group_nonexternalization_status",
    "future_nonexternalization_status",
    "revision_capacity_status",
    "persistent_loop_reduction_status",
    "effect_scope_status",
    "effect_ceiling_status",
    "checkpoint_status",
    "stop_condition_status",
    "compensation_route_status",
    "observation_route_status",
    "verification_route_status",
    "review_epoch",
    "reviewer_responsibility_digest",
    "effect_commit_review_certificate_digest",
}

CONTEXT_FIELDS = {
    "source_invocation_receipt_digest",
    "adapter_result_envelope_digest",
    "effect_commit_review_certificate_digest",
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "invocation_receipt_observed_epoch",
    "authorization_epoch",
    "maximum_authorization_delay",
    "commit_session_id",
    "commit_intent_digest",
    "commit_authorization_nonce_digest",
    "prior_commit_session_ids",
    "prior_commit_authorization_nonce_digests",
    "prior_authorized_invocation_receipt_digests",
    "requested_effect_commit_operation_digest",
    "exact_effect_commit_authorization_cycle_digest",
    "effect_commit_authorization_context_digest",
}

SOURCE_TRUE = (
    "adapter_invocation_performed",
    "adapter_host_invocation_performed",
    "exactly_one_adapter_invoked",
    "bounded_scope_preserved",
    "effect_ceiling_preserved",
    "activation_frontier_sequence_preserved",
    "completed_prefix_preserved",
    "later_candidates_remain_uninvoked",
    "adapter_lease_reservation_consumed",
    "adapter_lease_use_consumed",
    "lease_consumption_record_issued",
    "invocation_nonce_consumed",
    "invocation_nonce_replay_closed",
    "frontier_invocation_replay_closed",
    "invocation_result_envelope_issued",
    "effect_proposal_recorded",
    "effect_commit_required",
    "observation_intake_required",
    "verification_debt_open",
    "adapter_registry_snapshot_unchanged",
    "world_conditions_current",
    "invocation_delay_current",
    "lease_reservation_replay_fresh_before_consumption",
    "invocation_nonce_replay_fresh_before_consumption",
    "frontier_replay_fresh_before_invocation",
    "checkpoint_guards_preserved",
    "stop_conditions_preserved",
    "evidence_lineage_preserved",
    "alternative_candidates_preserved",
    "dissent_preserved",
    "minority_preserved",
    "dukkha_reduction_support_preserved",
    "protected_group_nonexternalization_preserved",
    "future_nonexternalization_preserved",
    "revision_capacity_preserved",
    "persistent_loop_reduction_preserved",
    "single_scalar_utility_not_introduced",
    "selection_remains_decisionos_owned",
    "persistent_world_state_unchanged",
    "world_model_prediction_not_truth",
    "world_mutation_not_granted",
    "history_read_only",
    "qi_grants_no_authority",
    "future_only",
)

SOURCE_FALSE = (
    "adapter_lease_double_decremented",
    "effect_commit_performed",
    "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "execution_authority_granted",
    "execution_permission",
    "active_now",
)


@dataclass
class ActOSDukkhaPreservingEffectCommitAuthorizationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def compute_effect_commit_review_certificate_digest(
    certificate: Mapping[str, Any],
) -> str:
    value = dict(certificate)
    value.pop("effect_commit_review_certificate_digest", None)
    return canonical_digest(value)


def compute_effect_commit_authorization_context_digest(
    context: Mapping[str, Any],
) -> str:
    value = dict(context)
    value.pop("effect_commit_authorization_context_digest", None)
    return canonical_digest(value)


def compute_effect_commit_intent_digest(
    source: Mapping[str, Any], review: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source_invocation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "adapter_result_envelope_digest": source.get(
                "adapter_result_envelope_digest"
            ),
            "invoked_frontier_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "invoked_frontier_adapter_id": source.get(
                "invoked_frontier_adapter_id"
            ),
            "invoked_frontier_binding_digest": source.get(
                "invoked_frontier_binding_digest"
            ),
            "review_certificate_digest": review.get(
                "effect_commit_review_certificate_digest"
            ),
            "requested_state": SOURCE_STATE,
        }
    )


def compute_requested_effect_commit_operation_digest(
    source: Mapping[str, Any], review: Mapping[str, Any]
) -> str:
    envelope = source.get("adapter_result_envelope")
    envelope = dict(envelope) if isinstance(envelope, Mapping) else {}
    return canonical_digest(
        {
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get(
                "invoked_frontier_binding_digest"
            ),
            "adapter_result_envelope_digest": source.get(
                "adapter_result_envelope_digest"
            ),
            "requested_effect_tags": envelope.get("requested_effect_tags"),
            "effect_commit_state_before": envelope.get("effect_commit_state"),
            "effect_commit_authorization_state_after": "authorized_not_committed",
            "effect_scope_status": review.get("effect_scope_status"),
            "effect_ceiling_status": review.get("effect_ceiling_status"),
        }
    )


def compute_exact_effect_commit_authorization_cycle_digest(
    source: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_invocation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "invocation_record_digest": source.get("invocation_record_digest"),
            "adapter_result_envelope_digest": source.get(
                "adapter_result_envelope_digest"
            ),
            "lease_consumption_record_digest": source.get(
                "lease_consumption_record_digest"
            ),
            "effect_commit_review_certificate_digest": review.get(
                "effect_commit_review_certificate_digest"
            ),
            "commit_session_id": context.get("commit_session_id"),
            "commit_intent_digest": context.get("commit_intent_digest"),
            "commit_authorization_nonce_digest": context.get(
                "commit_authorization_nonce_digest"
            ),
            "authorization_epoch": context.get("authorization_epoch"),
            "current_world_model_revision": context.get(
                "current_world_model_revision"
            ),
            "requested_effect_commit_operation_digest": context.get(
                "requested_effect_commit_operation_digest"
            ),
        }
    )


def compute_effect_commit_authorization_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_invocation_receipt_missing")
        return "", {}, {}, [], []

    headers = {
        "kernel": "ActOS Dukkha-Preserving Bounded Adapter Invocation Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.8",
        "status": "ACTOS_DUKKHA_PRESERVING_BOUNDED_ADAPTER_INVOCATION_RECORDED",
        "invocation_state_after": SOURCE_STATE,
    }
    for field, value in headers.items():
        if source.get(field) != value:
            blockers.append(f"source_{field}_invalid")

    digest = source.get(SOURCE_DIGEST_FIELD)
    if not isinstance(digest, str) or not digest:
        blockers.append("source_invocation_receipt_digest_missing")
        digest = ""
    else:
        unsigned = dict(source)
        unsigned.pop(SOURCE_DIGEST_FIELD, None)
        if digest != canonical_digest(unsigned):
            blockers.append("source_invocation_receipt_digest_mismatch")
        if digest != expected:
            blockers.append("source_invocation_receipt_expected_binding_mismatch")

    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    if source.get("remaining_uses_at_invocation") != source.get(
        "remaining_uses_after_reservation"
    ):
        blockers.append("source_lease_reservation_consumption_mismatch")

    raw_record = source.get("invocation_record")
    record = dict(raw_record) if isinstance(raw_record, Mapping) else {}
    if not record:
        blockers.append("source_invocation_record_invalid")
    if source.get("invocation_record_digest") != canonical_digest(record):
        blockers.append("source_invocation_record_digest_mismatch")

    raw_envelope = source.get("adapter_result_envelope")
    envelope = dict(raw_envelope) if isinstance(raw_envelope, Mapping) else {}
    if not envelope:
        blockers.append("source_adapter_result_envelope_invalid")
    if source.get("adapter_result_envelope_digest") != canonical_digest(envelope):
        blockers.append("source_adapter_result_envelope_digest_mismatch")
    envelope_expected = {
        "frontier_materialization_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "invocation_outcome": "bounded_effect_proposal_recorded",
        "effect_commit_state": "not_committed",
        "external_effect_requested": False,
        "tool_invocation_requested": False,
        "observation_intake_required": True,
        "verification_debt_open": True,
    }
    for field, value in envelope_expected.items():
        if envelope.get(field) != value:
            blockers.append(f"source_adapter_result_envelope_{field}_mismatch")
    effects_ok, effects = _strings(envelope.get("requested_effect_tags"), True)
    if not effects_ok:
        blockers.append("source_requested_effect_tags_invalid")

    raw_lease = source.get("lease_consumption_record")
    lease = dict(raw_lease) if isinstance(raw_lease, Mapping) else {}
    if not lease:
        blockers.append("source_lease_consumption_record_invalid")
    if source.get("lease_consumption_record_digest") != canonical_digest(lease):
        blockers.append("source_lease_consumption_record_digest_mismatch")
    if lease.get("reservation_consumed") is not True:
        blockers.append("source_lease_reservation_not_consumed")
    if lease.get("double_decrement_performed") is not False:
        blockers.append("source_lease_double_decrement_promoted")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, record, envelope, lineage, responsibility


def _verify_review(
    review: dict, expected: str, source: dict, blockers: list[str]
) -> tuple[str, bool]:
    if not review:
        blockers.append("effect_commit_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("effect_commit_review_certificate_schema_invalid")

    digest = review.get("effect_commit_review_certificate_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("effect_commit_review_certificate_digest_missing")
        digest = ""
    else:
        if digest != compute_effect_commit_review_certificate_digest(review):
            blockers.append("effect_commit_review_certificate_digest_mismatch")
        if digest != expected:
            blockers.append("effect_commit_review_certificate_expected_binding_mismatch")

    exact = {
        "source_invocation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "adapter_result_envelope_digest": source.get(
            "adapter_result_envelope_digest"
        ),
        "invocation_record_digest": source.get("invocation_record_digest"),
    }
    for field, value in exact.items():
        if review.get(field) != value:
            blockers.append(f"effect_commit_review_{field}_mismatch")

    string_fields = REVIEW_FIELDS - {
        "review_epoch",
        "effect_commit_review_certificate_digest",
    }
    for field in string_fields:
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"effect_commit_review_{field}_invalid")
    epoch = review.get("review_epoch")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        blockers.append("effect_commit_review_epoch_invalid")

    supported = all(
        (
            review.get("review_disposition") == REVIEW_SUPPORTED,
            review.get("dukkha_reduction_support_status") == "supported",
            review.get("protected_group_nonexternalization_status") == "preserved",
            review.get("future_nonexternalization_status") == "preserved",
            review.get("revision_capacity_status") == "preserved",
            review.get("persistent_loop_reduction_status") == "preserved",
        )
    )
    return digest, supported


def _verify_context(
    context: dict,
    expected: str,
    source: dict,
    review: dict,
    blockers: list[str],
):
    if not context:
        blockers.append("effect_commit_authorization_context_missing")
        return "", False, False, False, False, False
    if set(context) != CONTEXT_FIELDS:
        blockers.append("effect_commit_authorization_context_schema_invalid")

    digest = context.get("effect_commit_authorization_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("effect_commit_authorization_context_digest_missing")
        digest = ""
    else:
        if digest != compute_effect_commit_authorization_context_digest(context):
            blockers.append("effect_commit_authorization_context_digest_mismatch")
        if digest != expected:
            blockers.append("effect_commit_authorization_context_expected_binding_mismatch")

    string_fields = CONTEXT_FIELDS - {
        "current_world_model_revision",
        "invocation_receipt_observed_epoch",
        "authorization_epoch",
        "maximum_authorization_delay",
        "prior_commit_session_ids",
        "prior_commit_authorization_nonce_digests",
        "prior_authorized_invocation_receipt_digests",
        "effect_commit_authorization_context_digest",
    }
    for field in string_fields:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"effect_commit_authorization_context_{field}_invalid")
    for field in (
        "current_world_model_revision",
        "invocation_receipt_observed_epoch",
        "authorization_epoch",
        "maximum_authorization_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"effect_commit_authorization_context_{field}_invalid")
    delay = context.get("maximum_authorization_delay")
    if not isinstance(delay, int) or isinstance(delay, bool) or not 1 <= delay <= 64:
        blockers.append("effect_commit_authorization_context_delay_bound_invalid")

    sessions_ok, sessions = _strings(context.get("prior_commit_session_ids"), True)
    nonces_ok, nonces = _strings(
        context.get("prior_commit_authorization_nonce_digests"), True
    )
    sources_ok, sources = _strings(
        context.get("prior_authorized_invocation_receipt_digests"), True
    )
    if not sessions_ok:
        blockers.append("effect_commit_authorization_context_sessions_invalid")
    if not nonces_ok:
        blockers.append("effect_commit_authorization_context_nonces_invalid")
    if not sources_ok:
        blockers.append("effect_commit_authorization_context_sources_invalid")

    exact = {
        "source_invocation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "adapter_result_envelope_digest": source.get(
            "adapter_result_envelope_digest"
        ),
        "effect_commit_review_certificate_digest": review.get(
            "effect_commit_review_certificate_digest"
        ),
    }
    for field, value in exact.items():
        if context.get(field) != value:
            blockers.append(f"effect_commit_authorization_context_{field}_mismatch")

    world_expected = {
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get(
            "source_world_model_state_digest"
        ),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_world_lineage_digest": source.get("source_world_lineage_digest"),
    }

    if context.get("commit_intent_digest") != compute_effect_commit_intent_digest(
        source, review
    ):
        blockers.append("effect_commit_authorization_context_intent_digest_mismatch")
    if context.get(
        "requested_effect_commit_operation_digest"
    ) != compute_requested_effect_commit_operation_digest(source, review):
        blockers.append("effect_commit_authorization_context_operation_digest_mismatch")
    if context.get(
        "exact_effect_commit_authorization_cycle_digest"
    ) != compute_exact_effect_commit_authorization_cycle_digest(
        source, review, context
    ):
        blockers.append("effect_commit_authorization_context_cycle_digest_mismatch")

    observed = context.get("invocation_receipt_observed_epoch")
    epoch = context.get("authorization_epoch")
    max_delay = context.get("maximum_authorization_delay")
    delay_current = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (observed, epoch, max_delay)
    ) and 0 <= epoch - observed <= max_delay

    world_current = all(
        context.get(field) == value for field, value in world_expected.items()
    )
    session_fresh = context.get("commit_session_id") not in sessions
    nonce_fresh = context.get("commit_authorization_nonce_digest") not in nonces
    source_fresh = source.get(SOURCE_DIGEST_FIELD) not in sources
    return digest, world_current, delay_current, session_fresh, nonce_fresh, source_fresh


def _route_disposition(
    *,
    review: dict,
    review_supported: bool,
    world_current: bool,
    delay_current: bool,
    session_fresh: bool,
    nonce_fresh: bool,
    source_fresh: bool,
) -> str:
    if not (session_fresh and nonce_fresh and source_fresh):
        return DISPOSITION_REPLAY_REJECTED
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current or not review_supported:
        return DISPOSITION_REVERIFY
    if review.get("effect_scope_status") != "exact" or review.get(
        "effect_ceiling_status"
    ) != "exact":
        return DISPOSITION_SCOPE_REPAIR
    if review.get("checkpoint_status") != "satisfied" or review.get(
        "stop_condition_status"
    ) != "current":
        return DISPOSITION_CHECKPOINT
    if review.get("observation_route_status") != "ready":
        return DISPOSITION_OBSERVATION_REPAIR
    if review.get("verification_route_status") != "ready":
        return DISPOSITION_VERIFICATION_REPAIR
    if review.get("compensation_route_status") != "ready":
        return DISPOSITION_COMPENSATION_REPAIR
    return DISPOSITION_READY


def build_actos_dukkha_preserving_effect_commit_authorization_intake(
    *,
    source_invocation_receipt: Mapping[str, Any],
    expected_source_invocation_receipt_digest: str,
    effect_commit_review_certificate: Mapping[str, Any],
    expected_effect_commit_review_certificate_digest: str,
    effect_commit_authorization_context: Mapping[str, Any],
    expected_effect_commit_authorization_context_digest: str,
    effect_commit_authorization_policy_digest: str,
    actos_effect_commit_authorization_responsibility_digest: str,
    effect_commit_authorization_request_id: str,
    effect_commit_authorization_bundle_digest: str,
) -> ActOSDukkhaPreservingEffectCommitAuthorizationResult:
    blockers: list[str] = []
    source = (
        dict(source_invocation_receipt)
        if isinstance(source_invocation_receipt, Mapping)
        else {}
    )
    review = (
        dict(effect_commit_review_certificate)
        if isinstance(effect_commit_review_certificate, Mapping)
        else {}
    )
    context = (
        dict(effect_commit_authorization_context)
        if isinstance(effect_commit_authorization_context, Mapping)
        else {}
    )
    for name, value in {
        "expected_source_invocation_receipt_digest": (
            expected_source_invocation_receipt_digest
        ),
        "expected_effect_commit_review_certificate_digest": (
            expected_effect_commit_review_certificate_digest
        ),
        "expected_effect_commit_authorization_context_digest": (
            expected_effect_commit_authorization_context_digest
        ),
        "effect_commit_authorization_policy_digest": (
            effect_commit_authorization_policy_digest
        ),
        "actos_effect_commit_authorization_responsibility_digest": (
            actos_effect_commit_authorization_responsibility_digest
        ),
        "effect_commit_authorization_request_id": (
            effect_commit_authorization_request_id
        ),
        "effect_commit_authorization_bundle_digest": (
            effect_commit_authorization_bundle_digest
        ),
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_digest, invocation_record, envelope, lineage, responsibility = (
        _verify_source(
            source, expected_source_invocation_receipt_digest, blockers
        )
    )
    review_digest, review_supported = _verify_review(
        review,
        expected_effect_commit_review_certificate_digest,
        source,
        blockers,
    )
    (
        context_digest,
        world_current,
        delay_current,
        session_fresh,
        nonce_fresh,
        source_fresh,
    ) = _verify_context(
        context,
        expected_effect_commit_authorization_context_digest,
        source,
        review,
        blockers,
    )

    if not blockers:
        expected_bundle = compute_effect_commit_authorization_bundle_digest(
            source_invocation_receipt_digest=source_digest,
            expected_source_invocation_receipt_digest=(
                expected_source_invocation_receipt_digest
            ),
            invocation_record_digest=source.get("invocation_record_digest"),
            adapter_result_envelope_digest=source.get(
                "adapter_result_envelope_digest"
            ),
            lease_consumption_record_digest=source.get(
                "lease_consumption_record_digest"
            ),
            effect_commit_review_certificate_digest=review_digest,
            expected_effect_commit_review_certificate_digest=(
                expected_effect_commit_review_certificate_digest
            ),
            effect_commit_authorization_context_digest=context_digest,
            expected_effect_commit_authorization_context_digest=(
                expected_effect_commit_authorization_context_digest
            ),
            requested_effect_commit_operation_digest=context.get(
                "requested_effect_commit_operation_digest"
            ),
            exact_effect_commit_authorization_cycle_digest=context.get(
                "exact_effect_commit_authorization_cycle_digest"
            ),
            effect_commit_authorization_policy_digest=(
                effect_commit_authorization_policy_digest
            ),
            actos_effect_commit_authorization_responsibility_digest=(
                actos_effect_commit_authorization_responsibility_digest
            ),
            effect_commit_authorization_request_id=(
                effect_commit_authorization_request_id
            ),
        )
        if effect_commit_authorization_bundle_digest != expected_bundle:
            blockers.append("effect_commit_authorization_bundle_digest_mismatch")

    if blockers:
        return ActOSDukkhaPreservingEffectCommitAuthorizationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route_disposition(
        review=review,
        review_supported=review_supported,
        world_current=world_current,
        delay_current=delay_current,
        session_fresh=session_fresh,
        nonce_fresh=nonce_fresh,
        source_fresh=source_fresh,
    )
    admitted = disposition == DISPOSITION_READY

    authorization_record: dict[str, Any] = {}
    authorization_record_digest = ""
    authorization_token_digest = ""
    if admitted:
        authorization_record = {
            "source_invocation_receipt_digest": source_digest,
            "invocation_record_digest": source["invocation_record_digest"],
            "adapter_result_envelope_digest": source[
                "adapter_result_envelope_digest"
            ],
            "lease_consumption_record_digest": source[
                "lease_consumption_record_digest"
            ],
            "effect_commit_review_certificate_digest": review_digest,
            "effect_commit_authorization_context_digest": context_digest,
            "invoked_frontier_candidate_id": source[
                "invoked_frontier_candidate_id"
            ],
            "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
            "invoked_frontier_binding_digest": source[
                "invoked_frontier_binding_digest"
            ],
            "commit_session_id": context["commit_session_id"],
            "commit_intent_digest": context["commit_intent_digest"],
            "commit_authorization_nonce_digest": context[
                "commit_authorization_nonce_digest"
            ],
            "requested_effect_commit_operation_digest": context[
                "requested_effect_commit_operation_digest"
            ],
            "exact_effect_commit_authorization_cycle_digest": context[
                "exact_effect_commit_authorization_cycle_digest"
            ],
            "authorization_disposition": disposition,
            "effect_commit_authorization_admitted": True,
            "authorization_epoch": context["authorization_epoch"],
            "effect_commit_state": "authorized_not_committed",
        }
        authorization_record_digest = canonical_digest(authorization_record)
        authorization_token_digest = canonical_digest(
            {
                **authorization_record,
                "authorization_record_digest": authorization_record_digest,
                "effect_commit_authorization_policy_digest": (
                    effect_commit_authorization_policy_digest
                ),
                "effect_commit_authorization_request_id": (
                    effect_commit_authorization_request_id
                ),
            }
        )

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["invocation_record_digest"],
            source["adapter_result_envelope_digest"],
            source["lease_consumption_record_digest"],
            review_digest,
            context_digest,
            context["requested_effect_commit_operation_digest"],
            context["exact_effect_commit_authorization_cycle_digest"],
            effect_commit_authorization_bundle_digest,
        }
        | ({authorization_record_digest, authorization_token_digest} if admitted else set())
    )
    resulting_responsibility = sorted(
        set(responsibility)
        | {
            review["reviewer_responsibility_digest"],
            actos_effect_commit_authorization_responsibility_digest,
        }
    )

    receipt = {
        "kernel": "ActOS Dukkha-Preserving Effect Commit Authorization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.9",
        "status": "ACTOS_DUKKHA_PRESERVING_EFFECT_COMMIT_AUTHORIZATION_ROUTED",
        "authorization_disposition": disposition,
        "source_invocation_receipt_digest": source_digest,
        "source_activation_receipt_digest": source[
            "source_activation_receipt_digest"
        ],
        "source_authorization_receipt_digest": source[
            "source_authorization_receipt_digest"
        ],
        "source_materialization_receipt_digest": source[
            "source_materialization_receipt_digest"
        ],
        "source_verifyos_dukkha_certificate_digest": source[
            "source_verifyos_dukkha_certificate_digest"
        ],
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source[
            "selected_candidate_plan_intent_digest"
        ],
        "dukkha_assessment_digest": source["dukkha_assessment_digest"],
        "reference_plan_digest": source["reference_plan_digest"],
        "adapter_registry_snapshot_digest": source[
            "adapter_registry_snapshot_digest"
        ],
        "source_invocation_record_digest": source["invocation_record_digest"],
        "adapter_result_envelope": envelope,
        "adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "source_lease_consumption_record_digest": source[
            "lease_consumption_record_digest"
        ],
        "effect_commit_review_certificate": review,
        "effect_commit_review_certificate_digest": review_digest,
        "effect_commit_authorization_context_digest": context_digest,
        "effect_commit_authorization_policy_digest": (
            effect_commit_authorization_policy_digest
        ),
        "actos_effect_commit_authorization_responsibility_digest": (
            actos_effect_commit_authorization_responsibility_digest
        ),
        "effect_commit_authorization_request_id": (
            effect_commit_authorization_request_id
        ),
        "effect_commit_authorization_bundle_digest": (
            effect_commit_authorization_bundle_digest
        ),
        "invoked_frontier_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "invoked_frontier_lease_id": source["invoked_frontier_lease_id"],
        "effect_commit_state_before": SOURCE_STATE,
        "effect_commit_state_after": (
            "authorized_not_committed" if admitted else SOURCE_STATE
        ),
        "effect_commit_authorization_record": authorization_record,
        "effect_commit_authorization_record_digest": (
            authorization_record_digest
        ),
        "effect_commit_authorization_token_digest": authorization_token_digest,
        "effect_commit_authorization_admitted": admitted,
        "effect_commit_authorization_receipt_issued": admitted,
        "single_use_effect_commit_authorization_reserved": admitted,
        "effect_commit_authorization_token_replay_fresh": source_fresh,
        "effect_commit_intake_admitted": admitted,
        "effect_commit_review_supported": review_supported,
        "world_conditions_current": world_current,
        "authorization_delay_current": delay_current,
        "commit_session_replay_fresh": session_fresh,
        "commit_nonce_replay_fresh": nonce_fresh,
        "source_invocation_replay_fresh": source_fresh,
        "effect_scope_exact": review.get("effect_scope_status") == "exact",
        "effect_ceiling_exact": review.get("effect_ceiling_status") == "exact",
        "checkpoint_satisfied": review.get("checkpoint_status") == "satisfied",
        "stop_conditions_current": review.get("stop_condition_status") == "current",
        "compensation_route_ready": review.get("compensation_route_status") == "ready",
        "observation_route_ready": review.get("observation_route_status") == "ready",
        "verification_route_ready": review.get("verification_route_status") == "ready",
        "adapter_invocation_performed": True,
        "adapter_lease_use_consumed": True,
        "effect_proposal_recorded": True,
        "effect_commit_required": True,
        "effect_commit_performed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "persistent_world_state_unchanged": True,
        "observation_intake_required": True,
        "verification_debt_open": True,
        "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True,
        "alternative_candidates_preserved": True,
        "dissent_preserved": True,
        "minority_preserved": True,
        "dukkha_reduction_support_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True,
        "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_actos": False,
        "plan_revision_authority_granted_to_actos": False,
        "dukkha_minimization_authority_granted_to_actos": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ActOSDukkhaPreservingEffectCommitAuthorizationResult(
        STATUS_READY, [], receipt
    )

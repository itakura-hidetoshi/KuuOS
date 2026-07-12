#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
from runtime.kuuos_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake_v0_1 import *
from scripts.check_learnos_dukkha_preserving_future_only_learning_maintenance_fixture_v0_1 import build, source, evidence, review, context, redigest_evidence, redigest_review, redigest_context

def assert_disposition(result, disposition):
    assert result.status==STATUS_READY,result.blockers; assert result.receipt is not None; assert result.receipt["future_only_learning_disposition"]==disposition; assert result.receipt["learnos_version"]=="v0.4"; return result.receipt

def review_route(field, value, disposition):
    src=source(); ev=evidence(src); rv=review(src,ev); rv[field]=value; rv=redigest_review(rv,ev); cx=redigest_context(src,ev,rv,context(src,ev,rv)); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=ev,future_only_learning_review_certificate=rv,future_only_learning_intake_context=cx),disposition)

def main():
    supported=assert_disposition(build(),DISPOSITION_SUPPORTED)
    assert supported["future_only_learning_state_before"]==STATE_BEFORE
    assert supported["future_only_learning_state_after"]==STATE_AFTER_SUPPORTED
    for field in ("world_fact_confirmed","causal_attribution_confirmed","dukkha_reduction_realized_confirmed","future_only_learning_delta_recorded","maintenance_monitoring_handoff_prepared"): assert supported[field] is True
    for field in ("future_only_learning_delta_activated","maintenance_monitoring_activated","persistent_world_state_changed_by_learning","world_model_revision_incremented_by_learning","current_plan_revised_by_learning","current_policy_activated_by_learning","tool_invocation_performed","external_side_effect_performed","selection_authority_granted_to_learnos","plan_revision_authority_granted_to_learnos","dukkha_minimization_authority_granted_to_learnos","general_execution_authority_granted","world_mutation_authority_granted","current_policy_activation_authority_granted","active_now"): assert supported[field] is False
    assert supported[RECEIPT_DIGEST_FIELD]==canonical_digest({k:v for k,v in supported.items() if k!=RECEIPT_DIGEST_FIELD})
    blocked=build(expected_source_realized_dukkha_verification_receipt_digest="wrong"); assert blocked.status==STATUS_BLOCKED and blocked.receipt is None; assert "source_realized_dukkha_verification_expected_binding_mismatch" in blocked.blockers

    src=source(); ev=evidence(src); rv=review(src,ev); cx=context(src,ev,rv)
    stale=deepcopy(cx); stale["current_world_model_state_digest"]="stale"; stale=redigest_context(src,ev,rv,stale); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=ev,future_only_learning_review_certificate=rv,future_only_learning_intake_context=stale),DISPOSITION_WORLD_REFRESH)
    late=deepcopy(cx); late["future_only_learning_intake_epoch"]=late["source_realized_dukkha_verification_epoch"]+late["maximum_future_only_learning_intake_delay"]+1; late=redigest_context(src,ev,rv,late); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=ev,future_only_learning_review_certificate=rv,future_only_learning_intake_context=late),DISPOSITION_CONTEXT_REFRESH)
    replay=deepcopy(cx); replay["prior_future_only_learning_intake_session_ids"]=[replay["future_only_learning_intake_session_id"]]; replay=redigest_context(src,ev,rv,replay); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=ev,future_only_learning_review_certificate=rv,future_only_learning_intake_context=replay),DISPOSITION_REPLAY_REJECTED)
    old_review=deepcopy(rv); old_review["review_completed_epoch"]=old_review["review_started_epoch"]+old_review["maximum_review_duration"]+1; old_review=redigest_review(old_review,ev); old_context=redigest_context(src,ev,old_review,context(src,ev,old_review)); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=ev,future_only_learning_review_certificate=old_review,future_only_learning_intake_context=old_context),DISPOSITION_REVIEW_REFRESH)
    insufficient=deepcopy(ev); insufficient["independent_future_only_learning_evidence"]=False; insufficient=redigest_evidence(insufficient); insufficient_review=redigest_review(rv,insufficient); insufficient_context=redigest_context(src,insufficient,insufficient_review,context(src,insufficient,insufficient_review)); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=insufficient,future_only_learning_review_certificate=insufficient_review,future_only_learning_intake_context=insufficient_context),DISPOSITION_ADDITIONAL_EVIDENCE)

    routes=(("source_receipt_correspondence_confirmed",DISPOSITION_SOURCE_REPAIR),("source_bounded_world_fact_correspondence_confirmed",DISPOSITION_FACT_REPAIR),("source_causal_attribution_correspondence_confirmed",DISPOSITION_CAUSAL_REPAIR),("source_realized_dukkha_correspondence_confirmed",DISPOSITION_DUKKHA_REPAIR),("maintenance_window_adequate",DISPOSITION_MAINTENANCE_WINDOW_REPAIR),("durability_monitoring_adequate",DISPOSITION_DURABILITY_REVIEW),("adverse_effect_monitoring_adequate",DISPOSITION_ADVERSE_REVIEW),("distributional_monitoring_adequate",DISPOSITION_DISTRIBUTIONAL_REVIEW),("uncertainty_adequate",DISPOSITION_UNCERTAINTY_REPAIR),("calibration_adequate",DISPOSITION_CALIBRATION_REPAIR),("provenance_continuity_preserved",DISPOSITION_PROVENANCE_REPAIR),("protected_group_nonexternalization_supported",DISPOSITION_NONEXTERNALIZATION_REVIEW))
    for field, disposition in routes: review_route(field,False,disposition)

    mutating=deepcopy(ev); mutating["current_policy_activated"]=True; mutating=redigest_evidence(mutating); mutating_review=redigest_review(rv,mutating); mutating_context=redigest_context(src,mutating,mutating_review,context(src,mutating,mutating_review)); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=mutating,future_only_learning_review_certificate=mutating_review,future_only_learning_intake_context=mutating_context),DISPOSITION_CURRENT_STATE_MUTATION_REJECTED)
    escalating=deepcopy(ev); escalating["authority_escalation_claimed"]=True; escalating=redigest_evidence(escalating); escalating_review=redigest_review(rv,escalating); escalating_context=redigest_context(src,escalating,escalating_review,context(src,escalating,escalating_review)); assert_disposition(build(source_realized_dukkha_verification_receipt=src,future_only_learning_evidence_packet=escalating,future_only_learning_review_certificate=escalating_review,future_only_learning_intake_context=escalating_context),DISPOSITION_AUTHORITY_ESCALATION_REJECTED)
    print("PASS: LearnOS v0.4 future-only learning maintenance disposition actual-chain validation")
    return 0

if __name__=="__main__": raise SystemExit(main())

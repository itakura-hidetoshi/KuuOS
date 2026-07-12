from __future__ import annotations
from runtime.kuuos_learnos_future_only_learning_common_v0_1 import *

def route_learning(evidence: dict, review: dict, context: dict, source_epoch: int) -> str:
    world_current = all((context.get("current_world_binding_digest") == context.get("source_world_binding_digest"), context.get("current_world_model_state_digest") == context.get("source_world_model_state_digest"), context.get("current_world_model_revision") == context.get("source_world_model_revision"), context.get("current_persistent_world_storage_target_digest") == context.get("source_persistent_world_storage_target_digest")))
    if not world_current: return DISPOSITION_WORLD_REFRESH
    if context.get("future_only_learning_intake_epoch", 0) - source_epoch > context.get("maximum_future_only_learning_intake_delay", 0): return DISPOSITION_CONTEXT_REFRESH
    replay = any((context.get("future_only_learning_intake_session_id") in context.get("prior_future_only_learning_intake_session_ids", []), evidence.get(EVIDENCE_DIGEST_FIELD) in context.get("prior_future_only_learning_evidence_packet_digests", []), review.get(REVIEW_DIGEST_FIELD) in context.get("prior_future_only_learning_review_certificate_digests", []), context.get("future_only_learning_intake_nonce_digest") in context.get("prior_future_only_learning_intake_nonce_digests", []), context.get("source_realized_dukkha_verification_receipt_digest") in context.get("prior_future_only_learning_source_receipt_digests", [])))
    if replay: return DISPOSITION_REPLAY_REJECTED
    if review.get("review_completed_epoch", 0) - review.get("review_started_epoch", 0) > review.get("maximum_review_duration", 0): return DISPOSITION_REVIEW_REFRESH
    if evidence.get("collection_completed_epoch", 0) - evidence.get("collection_started_epoch", 0) > evidence.get("maximum_collection_duration", 0) or evidence.get("independent_future_only_learning_evidence") is not True or evidence.get("exactly_one_future_only_learning_evidence_collection") is not True: return DISPOSITION_ADDITIONAL_EVIDENCE
    checks = (("source_receipt_correspondence_confirmed",DISPOSITION_SOURCE_REPAIR),("source_bounded_world_fact_correspondence_confirmed",DISPOSITION_FACT_REPAIR),("source_causal_attribution_correspondence_confirmed",DISPOSITION_CAUSAL_REPAIR),("source_realized_dukkha_correspondence_confirmed",DISPOSITION_DUKKHA_REPAIR),("maintenance_window_adequate",DISPOSITION_MAINTENANCE_WINDOW_REPAIR),("durability_monitoring_adequate",DISPOSITION_DURABILITY_REVIEW),("adverse_effect_monitoring_adequate",DISPOSITION_ADVERSE_REVIEW),("distributional_monitoring_adequate",DISPOSITION_DISTRIBUTIONAL_REVIEW),("uncertainty_adequate",DISPOSITION_UNCERTAINTY_REPAIR),("calibration_adequate",DISPOSITION_CALIBRATION_REPAIR),("provenance_continuity_preserved",DISPOSITION_PROVENANCE_REPAIR))
    for key, disposition in checks:
        if review.get(key) is not True: return disposition
    if review.get("protected_group_nonexternalization_supported") is not True or review.get("future_nonexternalization_supported") is not True: return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if evidence.get("current_world_mutation_performed") or evidence.get("current_plan_revised") or evidence.get("current_policy_activated") or review.get("no_current_state_mutation") is not True: return DISPOSITION_CURRENT_STATE_MUTATION_REJECTED
    if evidence.get("authority_escalation_claimed") or review.get("no_authority_escalation") is not True: return DISPOSITION_AUTHORITY_ESCALATION_REJECTED
    return DISPOSITION_SUPPORTED

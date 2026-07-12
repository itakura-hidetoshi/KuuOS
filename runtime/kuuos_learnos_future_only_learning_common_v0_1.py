from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from runtime.kuuos_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1 import (
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    canonical_digest,
    compute_realized_dukkha_verification_evidence_packet_digest,
    compute_realized_dukkha_verification_review_certificate_digest,
)
STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake_receipt_digest"
EVIDENCE_DIGEST_FIELD = "future_only_learning_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "future_only_learning_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "future_only_learning_intake_context_digest"
STATE_BEFORE = "world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed"
STATE_AFTER_SUPPORTED = STATE_BEFORE + "_future_only_learning_delta_recorded"
DISPOSITION_SUPPORTED = "future_only_learning_maintenance_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "learning_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "learning_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_future_only_learning_evidence_required"
DISPOSITION_SOURCE_REPAIR = "source_receipt_correspondence_repair_required"
DISPOSITION_FACT_REPAIR = "bounded_fact_correspondence_repair_required"
DISPOSITION_CAUSAL_REPAIR = "causal_attribution_correspondence_repair_required"
DISPOSITION_DUKKHA_REPAIR = "realized_dukkha_correspondence_repair_required"
DISPOSITION_MAINTENANCE_WINDOW_REPAIR = "maintenance_window_repair_required"
DISPOSITION_DURABILITY_REVIEW = "durability_monitoring_review_required"
DISPOSITION_ADVERSE_REVIEW = "adverse_effect_monitoring_review_required"
DISPOSITION_DISTRIBUTIONAL_REVIEW = "distributional_monitoring_review_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = "current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

def as_map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}

def digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value); item.pop(field, None); return canonical_digest(item)

def compute_future_only_learning_evidence_packet_digest(value): return digest_without(value, EVIDENCE_DIGEST_FIELD)
def compute_future_only_learning_review_certificate_digest(value): return digest_without(value, REVIEW_DIGEST_FIELD)
def compute_future_only_learning_intake_context_digest(value): return digest_without(value, CONTEXT_DIGEST_FIELD)
def compute_future_only_learning_bundle_digest(**fields): return canonical_digest(fields)

def compute_requested_future_only_learning_operation_digest(source, evidence, review):
    return canonical_digest({"source": source.get(SOURCE_RECEIPT_DIGEST_FIELD), "evidence": evidence.get(EVIDENCE_DIGEST_FIELD), "review": review.get(REVIEW_DIGEST_FIELD), "fact": source.get("world_candidate_fact_digest"), "relation": source.get("world_candidate_relation_digest"), "target": evidence.get("learning_target_digest"), "delta": evidence.get("future_only_learning_delta_digest"), "before": STATE_BEFORE, "after": STATE_AFTER_SUPPORTED})

def compute_exact_future_only_learning_cycle_digest(source, evidence, review, context):
    return canonical_digest({"source": source.get(SOURCE_RECEIPT_DIGEST_FIELD), "evidence": evidence.get(EVIDENCE_DIGEST_FIELD), "review": review.get(REVIEW_DIGEST_FIELD), "session": context.get("future_only_learning_intake_session_id"), "nonce": context.get("future_only_learning_intake_nonce_digest"), "epoch": context.get("future_only_learning_intake_epoch"), "revision": context.get("current_world_model_revision"), "operation": context.get("requested_future_only_learning_operation_digest")})

@dataclass
class LearnOSFutureOnlyLearningMaintenanceDispositionResult:
    status: str
    blockers: list[str]
    receipt: dict | None

def verify_source(source: dict, expected: str, blockers: list[str]):
    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD, "")
    if not digest or digest != digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD): blockers.append("source_realized_dukkha_verification_receipt_digest_mismatch")
    if digest != expected: blockers.append("source_realized_dukkha_verification_expected_binding_mismatch")
    required = {"verifyos_version":"v0.10", "realized_dukkha_verification_disposition":"realized_dukkha_verification_supported", "realized_dukkha_verification_state_after":STATE_BEFORE, "world_fact_confirmed":True, "causal_attribution_confirmed":True, "dukkha_reduction_realized_confirmed":True, "dukkha_reduction_realized_scope_exactly_bounded":True, "future_learning_intake_admitted":True, "future_learning_receipt_required":True, "history_read_only":True, "future_only":True, "active_now":False}
    for key, value in required.items():
        if source.get(key) != value: blockers.append(f"source_{key}_mismatch")
    evidence = as_map(source.get("realized_dukkha_verification_evidence_packet")); review = as_map(source.get("realized_dukkha_verification_review_certificate"))
    if source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != compute_realized_dukkha_verification_evidence_packet_digest(evidence): blockers.append("source_realized_dukkha_evidence_digest_mismatch")
    if source.get(SOURCE_REVIEW_DIGEST_FIELD) != compute_realized_dukkha_verification_review_certificate_digest(review): blockers.append("source_realized_dukkha_review_digest_mismatch")
    nested = (("realized_dukkha_verification_record","realized_dukkha_verification_record_digest"),("realized_dukkha_verification_debt_consumption_record","realized_dukkha_verification_debt_consumption_record_digest"),("bounded_realized_dukkha_confirmation_binding","bounded_realized_dukkha_confirmation_binding_digest"),("future_learning_handoff_envelope","future_learning_handoff_envelope_digest"))
    for obj_field, digest_field in nested:
        if canonical_digest(as_map(source.get(obj_field))) != source.get(digest_field): blockers.append(f"source_{digest_field}_mismatch")
    handoff = as_map(source.get("future_learning_handoff_envelope"))
    if handoff.get("bounded_realized_dukkha_confirmation_binding_digest") != source.get("bounded_realized_dukkha_confirmation_binding_digest") or handoff.get("future_learning_intake_admitted") is not True or handoff.get("historical_evidence_read_only") is not True: blockers.append("source_future_learning_handoff_mismatch")
    record = as_map(source.get("realized_dukkha_verification_record"))
    return digest, int(record.get("realized_dukkha_verification_intake_epoch", 0)), list(source.get("resulting_lineage_digests", [])), list(source.get("resulting_responsibility_lineage_digests", []))

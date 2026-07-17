from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_RECEIPT_DIGEST_FIELD = (
    "observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_"
    "intake_receipt_digest"
)
RECEIPT_DIGEST_FIELD = "observeos_sequential_epistemic_observability_envelope_receipt_digest"
PACKET_DIGEST_FIELD = "sequential_epistemic_observability_packet_digest"
POLICY_DIGEST_FIELD = "sequential_epistemic_observability_policy_digest"
PROVENANCE_DIGEST_FIELD = "provenance_bundle_digest"
SEQUENTIAL_DIGEST_FIELD = "sequential_uncertainty_digest"
CONFORMAL_DIGEST_FIELD = "conformal_calibration_digest"
DRIFT_DIGEST_FIELD = "distribution_shift_evidence_digest"
SOURCE_STATE = (
    "world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_"
    "realized_confirmed_future_only_learning_delta_recorded_maintenance_"
    "monitoring_observation_recorded"
)
SUPPORTED_STATE = SOURCE_STATE + "_sequential_epistemic_observability_envelope_recorded"

DISPOSITION_SUPPORTED = "sequential_epistemic_observability_supported"
DISPOSITION_SOURCE_REPAIR = "source_observation_receipt_repair_required"
DISPOSITION_TRACE_REPAIR = "trace_context_repair_required"
DISPOSITION_SIGNAL_REPAIR = "signal_coverage_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_SAMPLE_ACCOUNTING_REPAIR = "sample_accounting_repair_required"
DISPOSITION_MISSINGNESS_REVIEW = "missingness_review_required"
DISPOSITION_DISTRIBUTION_SHIFT_REVIEW = "distribution_shift_review_required"
DISPOSITION_SEQUENTIAL_UNCERTAINTY_REPAIR = "sequential_uncertainty_repair_required"
DISPOSITION_CONFORMAL_REPAIR = "conformal_calibration_repair_required"
DISPOSITION_WINDOW_REPAIR = "observation_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = "current_state_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"

TRACEPARENT_V00 = re.compile(
    r"^00-(?P<trace_id>[0-9a-f]{32})-(?P<span_id>[0-9a-f]{16})-(?P<trace_flags>[0-9a-f]{2})$"
)
PACKET_FIELDS = {
    "source_observation_receipt_digest", "traceparent", "tracestate", "trace_id",
    "span_id", "trace_flags", "signals", "resource_attributes_digest",
    "semantic_conventions_schema_url", "provenance_bundle", "sequential_uncertainty",
    "conformal_calibration", "distribution_shift_evidence", "sampling_policy_digest",
    "missingness_policy_digest", "raw_artifact_digests", "total_samples",
    "observed_samples", "missing_samples", "observation_started_epoch",
    "observation_completed_epoch", "collector_id", "evidence_source_id", "session_id",
    "nonce_digest", "prior_session_ids", "prior_nonce_digests", "prior_packet_digests",
    "telemetry_collection_performed_by_kernel", "persistent_world_state_changed",
    "world_model_revision_incremented", "current_plan_revised", "current_policy_activated",
    "learning_delta_activated", "tool_invocation_performed", "external_side_effect_performed",
    "generalized_truth_claimed", "causal_verification_claimed", "authority_escalation_claimed",
    PACKET_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "required_signals", "minimum_observed_samples", "maximum_missing_fraction_ppm",
    "maximum_observation_duration", "maximum_conformal_coverage_gap_ppm",
    "require_w3c_trace_context", "require_prov_o_bundle",
    "require_anytime_valid_uncertainty", "require_conformal_calibration",
    POLICY_DIGEST_FIELD,
}

@dataclass(frozen=True)
class ObserveOSSequentialEpistemicObservabilityResult:
    status: str
    blockers: list[str]
    receipt: dict[str, Any] | None

def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

def digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value); item.pop(field, None)
    return canonical_digest(item)

def mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}

def strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value): return False, []
    if any(not isinstance(x, str) or not x for x in value): return False, []
    xs = list(value)
    return xs == sorted(xs) and len(xs) == len(set(xs)), xs

def nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0

def pos(value: Any) -> bool:
    return nat(value) and value > 0

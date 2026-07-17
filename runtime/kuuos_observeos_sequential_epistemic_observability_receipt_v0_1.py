from __future__ import annotations
from typing import Any
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *

def build_receipt(expected_source_digest: str, ctx: dict[str, Any]) -> dict[str, Any]:
    c, packet = ctx["checks"], ctx["packet"]
    supported = ctx["disposition"] == DISPOSITION_SUPPORTED
    receipt: dict[str, Any] = {
        "kernel": "ObserveOS Sequential Epistemic Observability Envelope Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.7",
        "status": "OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ROUTED",
        "source_observation_receipt_digest": expected_source_digest,
        PACKET_DIGEST_FIELD: ctx["packet_digest"], POLICY_DIGEST_FIELD: ctx["policy_digest"],
        "observability_disposition": ctx["disposition"], "observability_state_before": SOURCE_STATE,
        "observability_state_after": SUPPORTED_STATE if supported else SOURCE_STATE,
        "trace_context_valid": c["trace"], "signal_coverage_complete": c["signals"],
        "provenance_bound": c["provenance"], "sample_accounting_confirmed": c["accounting"],
        "missing_fraction_ppm": ctx["missing_fraction"], "missingness_within_policy": c["missingness"],
        "distribution_shift_detected": ctx["shift_detected"], "sequential_uncertainty_bound": c["sequential"],
        "conformal_calibration_bound": ctx["conformal_ok"], "conformal_coverage_gap_ppm": ctx["conformal_gap"],
        "observation_window_valid": ctx["window"], "replay_closed": ctx["replay"],
        "sequential_epistemic_observability_envelope_recorded": supported,
        "verification_completed": False, "verification_debt_open": True,
        "persistent_world_state_changed_by_observability": False,
        "world_model_revision_incremented_by_observability": False,
        "current_plan_revised_by_observability": False, "current_policy_activated_by_observability": False,
        "learning_delta_activated_by_observability": False, "tool_invocation_performed": False,
        "external_side_effect_performed": False, "generalized_truth_claimed": False,
        "causal_verification_claimed": False, "selection_authority_granted_to_observeos": False,
        "verification_authority_granted_to_observeos": False, "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False, "execution_authority_granted": False,
        "history_read_only": True, "future_only": True, "active_now": False,
        "source_world_revision": ctx["revision"], "resulting_world_revision": ctx["revision"],
        "source_lineage_digests": ctx["source_lineage"], "resulting_lineage_digests": ctx["resulting_lineage"],
        "source_responsibility_lineage_digests": ctx["source_responsibility"],
        "resulting_responsibility_lineage_digests": ctx["resulting_responsibility"],
        "total_samples": ctx["total"], "observed_samples": ctx["observed"],
        "missing_samples": ctx["missing"], "collector_id": packet.get("collector_id"),
        "evidence_source_id": packet.get("evidence_source_id"), "session_id": packet.get("session_id"),
        "nonce_digest": packet.get("nonce_digest"),
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt

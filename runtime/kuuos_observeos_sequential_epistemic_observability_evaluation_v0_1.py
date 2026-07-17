from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *
from runtime.kuuos_observeos_sequential_epistemic_observability_preflight_v0_1 import preflight
from runtime.kuuos_observeos_sequential_epistemic_observability_sampling_v0_1 import sample_checks
from runtime.kuuos_observeos_sequential_epistemic_observability_validators_v0_1 import (
    source_supported, validate_conformal, validate_provenance, validate_sequential,
    validate_shift, validate_trace,
)
ROUTES = (
    ("source", DISPOSITION_SOURCE_REPAIR), ("trace", DISPOSITION_TRACE_REPAIR),
    ("signals", DISPOSITION_SIGNAL_REPAIR), ("provenance", DISPOSITION_PROVENANCE_REPAIR),
    ("accounting", DISPOSITION_SAMPLE_ACCOUNTING_REPAIR), ("missingness", DISPOSITION_MISSINGNESS_REVIEW),
    ("shift", DISPOSITION_DISTRIBUTION_SHIFT_REVIEW), ("sequential", DISPOSITION_SEQUENTIAL_UNCERTAINTY_REPAIR),
    ("conformal", DISPOSITION_CONFORMAL_REPAIR), ("window", DISPOSITION_WINDOW_REPAIR),
    ("replay", DISPOSITION_REPLAY_REJECTED), ("no_mutation", DISPOSITION_CURRENT_STATE_MUTATION_REJECTED),
    ("no_escalation", DISPOSITION_AUTHORITY_ESCALATION_REJECTED),
)

def evaluate(source_value: Mapping[str, Any], expected: str, packet_value: Mapping[str, Any], policy_value: Mapping[str, Any]) -> tuple[list[str], dict[str, Any]]:
    blockers, c = preflight(source_value, expected, packet_value, policy_value)
    if blockers: return blockers, {}
    source, packet, policy = c["source"], c["packet"], c["policy"]
    provenance = mapping(packet.get("provenance_bundle")); sequential = mapping(packet.get("sequential_uncertainty"))
    conformal = mapping(packet.get("conformal_calibration")); drift = mapping(packet.get("distribution_shift_evidence"))
    conformal_ok, conformal_gap = validate_conformal(conformal); shift_ok, shift_detected = validate_shift(drift)
    s = sample_checks(packet, policy, c["packet_digest"])
    checks = {"source": source_supported(source, expected), "trace": validate_trace(packet),
        "signals": c["sig_ok"] and set(c["required"]).issubset(c["signals"]),
        "provenance": validate_provenance(provenance), "accounting": s["accounting"],
        "missingness": s["accounting"] and s["missing_fraction"] <= policy["maximum_missing_fraction_ppm"],
        "shift": shift_ok and not shift_detected, "sequential": validate_sequential(sequential),
        "conformal": conformal_ok and conformal_gap <= policy["maximum_conformal_coverage_gap_ppm"],
        "window": s["window"], "replay": s["replay"], "no_mutation": s["no_mutation"], "no_escalation": s["no_escalation"]}
    disposition = next((route for key, route in ROUTES if not checks[key]), DISPOSITION_SUPPORTED)
    lin_ok, source_lineage = strings(source.get("resulting_lineage_digests"), True)
    rsp_ok, source_responsibility = strings(source.get("resulting_responsibility_lineage_digests"), True)
    if not lin_ok: source_lineage = []
    if not rsp_ok: source_responsibility = []
    lineage = sorted((set(source_lineage) | {str(c["packet_digest"]), str(provenance.get(PROVENANCE_DIGEST_FIELD, "")),
        str(sequential.get(SEQUENTIAL_DIGEST_FIELD, "")), str(conformal.get(CONFORMAL_DIGEST_FIELD, "")),
        str(drift.get(DRIFT_DIGEST_FIELD, ""))}) - {""})
    responsibility = canonical_digest({"collector_id": packet.get("collector_id"),
        "evidence_source_id": packet.get("evidence_source_id"), "session_id": packet.get("session_id")})
    revision = source.get("resulting_world_revision", 0)
    if not nat(revision): revision = 0
    return [], {**c, **s, "checks": checks, "disposition": disposition,
        "conformal_ok": conformal_ok, "conformal_gap": conformal_gap, "shift_detected": shift_detected,
        "source_lineage": source_lineage, "resulting_lineage": lineage,
        "source_responsibility": source_responsibility,
        "resulting_responsibility": sorted(set(source_responsibility) | {responsibility}), "revision": revision}

from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *

def preflight(
    source_value: Mapping[str, Any], expected_source_digest: str,
    packet_value: Mapping[str, Any], policy_value: Mapping[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    source, packet, policy = map(mapping, (source_value, packet_value, policy_value))
    blockers: list[str] = []
    if set(packet) != PACKET_FIELDS: blockers.append("observability_packet_schema_invalid")
    if set(policy) != POLICY_FIELDS: blockers.append("observability_policy_schema_invalid")
    if blockers: return sorted(set(blockers)), {}
    packet_digest, policy_digest = packet.get(PACKET_DIGEST_FIELD), policy.get(POLICY_DIGEST_FIELD)
    if packet_digest != digest_without(packet, PACKET_DIGEST_FIELD): blockers.append("observability_packet_digest_mismatch")
    if policy_digest != digest_without(policy, POLICY_DIGEST_FIELD): blockers.append("observability_policy_digest_mismatch")
    if packet.get("source_observation_receipt_digest") != expected_source_digest:
        blockers.append("source_observation_receipt_binding_mismatch")
    req_ok, required = strings(policy.get("required_signals"))
    sig_ok, signals = strings(packet.get("signals"))
    if not req_ok: blockers.append("required_signals_invalid")
    for field in ("minimum_observed_samples", "maximum_missing_fraction_ppm", "maximum_observation_duration", "maximum_conformal_coverage_gap_ppm"):
        if not nat(policy.get(field)): blockers.append(f"{field}_invalid")
    if not pos(policy.get("minimum_observed_samples")): blockers.append("minimum_observed_samples_invalid")
    if not pos(policy.get("maximum_observation_duration")): blockers.append("maximum_observation_duration_invalid")
    for field in ("maximum_missing_fraction_ppm", "maximum_conformal_coverage_gap_ppm"):
        if not (nat(policy.get(field)) and policy[field] <= 1_000_000): blockers.append(f"{field}_invalid")
    for field in ("require_w3c_trace_context", "require_prov_o_bundle", "require_anytime_valid_uncertainty", "require_conformal_calibration"):
        if policy.get(field) is not True: blockers.append(f"{field}_must_be_true")
    return sorted(set(blockers)), {
        "source": source, "packet": packet, "policy": policy,
        "packet_digest": packet_digest, "policy_digest": policy_digest,
        "required": required, "sig_ok": sig_ok, "signals": signals,
    }

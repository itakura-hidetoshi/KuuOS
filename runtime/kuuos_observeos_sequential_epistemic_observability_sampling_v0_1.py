from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *

def sample_checks(packet: Mapping[str, Any], policy: Mapping[str, Any], packet_digest: str) -> dict[str, Any]:
    total, observed, missing = packet.get("total_samples"), packet.get("observed_samples"), packet.get("missing_samples")
    accounting = (all(nat(x) for x in (total, observed, missing)) and total > 0
        and observed + missing == total and observed >= policy["minimum_observed_samples"])
    missing_fraction = (missing * 1_000_000) // total if accounting else 1_000_000
    start, end = packet.get("observation_started_epoch"), packet.get("observation_completed_epoch")
    window = nat(start) and nat(end) and start <= end and end - start <= policy["maximum_observation_duration"]
    ps_ok, sessions = strings(packet.get("prior_session_ids"), True)
    pn_ok, nonces = strings(packet.get("prior_nonce_digests"), True)
    pp_ok, packets = strings(packet.get("prior_packet_digests"), True)
    replay = (ps_ok and pn_ok and pp_ok and isinstance(packet.get("session_id"), str)
        and bool(packet.get("session_id")) and isinstance(packet.get("nonce_digest"), str)
        and bool(packet.get("nonce_digest")) and packet["session_id"] not in sessions
        and packet["nonce_digest"] not in nonces and packet_digest not in packets)
    no_mutation = all(packet.get(f) is False for f in (
        "telemetry_collection_performed_by_kernel", "persistent_world_state_changed",
        "world_model_revision_incremented", "current_plan_revised", "current_policy_activated",
        "learning_delta_activated", "tool_invocation_performed", "external_side_effect_performed"))
    no_escalation = all(packet.get(f) is False for f in (
        "generalized_truth_claimed", "causal_verification_claimed", "authority_escalation_claimed"))
    return {"total": total, "observed": observed, "missing": missing,
        "accounting": accounting, "missing_fraction": missing_fraction,
        "window": window, "replay": replay, "no_mutation": no_mutation,
        "no_escalation": no_escalation}

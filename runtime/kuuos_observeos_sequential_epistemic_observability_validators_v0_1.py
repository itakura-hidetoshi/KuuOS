from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *

def validate_trace(packet: Mapping[str, Any]) -> bool:
    tp = packet.get("traceparent")
    m = TRACEPARENT_V00.fullmatch(tp) if isinstance(tp, str) else None
    if m is None: return False
    tid, sid, flags = m.group("trace_id"), m.group("span_id"), m.group("trace_flags")
    if tid == "0" * 32 or sid == "0" * 16: return False
    if (packet.get("trace_id"), packet.get("span_id"), packet.get("trace_flags")) != (tid, sid, flags): return False
    state = packet.get("tracestate")
    if not isinstance(state, str) or len(state) > 512: return False
    if not state: return True
    members = [x.strip() for x in state.split(",")]
    keys = [x.split("=", 1)[0] for x in members if "=" in x]
    return len(members) <= 32 and len(keys) == len(members) == len(set(keys))

def validate_provenance(value: Mapping[str, Any]) -> bool:
    fields = {"profile", "entity_digests", "activity_digests", "agent_digests", "relation_digests", PROVENANCE_DIGEST_FIELD}
    if set(value) != fields or value.get("profile") != "W3C-PROV-O": return False
    if not all(strings(value.get(f))[0] for f in ("entity_digests", "activity_digests", "agent_digests", "relation_digests")): return False
    return value.get(PROVENANCE_DIGEST_FIELD) == digest_without(value, PROVENANCE_DIGEST_FIELD)

def validate_sequential(value: Mapping[str, Any]) -> bool:
    fields = {"method", "alpha_ppm", "lower_bound_ppm", "upper_bound_ppm", "e_process_log_digest", "stopping_rule_predeclared", SEQUENTIAL_DIGEST_FIELD}
    if set(value) != fields or value.get("method") != "confidence_sequence": return False
    a, lo, hi = value.get("alpha_ppm"), value.get("lower_bound_ppm"), value.get("upper_bound_ppm")
    return (all(nat(x) for x in (a, lo, hi)) and 0 < a < 1_000_000 and lo <= hi <= 1_000_000
        and isinstance(value.get("e_process_log_digest"), str) and bool(value.get("e_process_log_digest"))
        and value.get("stopping_rule_predeclared") is True
        and value.get(SEQUENTIAL_DIGEST_FIELD) == digest_without(value, SEQUENTIAL_DIGEST_FIELD))

def validate_conformal(value: Mapping[str, Any]) -> tuple[bool, int]:
    fields = {"method", "target_coverage_ppm", "empirical_coverage_ppm", "calibration_sample_count", "exchangeability_scope_digest", CONFORMAL_DIGEST_FIELD}
    target, empirical, count = value.get("target_coverage_ppm"), value.get("empirical_coverage_ppm"), value.get("calibration_sample_count")
    ok = (set(value) == fields and value.get("method") in {"split_conformal", "online_conformal"}
        and nat(target) and nat(empirical) and pos(count) and 0 < target <= 1_000_000 and empirical <= 1_000_000
        and isinstance(value.get("exchangeability_scope_digest"), str) and bool(value.get("exchangeability_scope_digest"))
        and value.get(CONFORMAL_DIGEST_FIELD) == digest_without(value, CONFORMAL_DIGEST_FIELD))
    return (ok, max(target - empirical, 0)) if ok else (False, 1_000_000)

def validate_shift(value: Mapping[str, Any]) -> tuple[bool, bool]:
    fields = {"detector", "window_size", "delta_ppm", "change_detected", "detector_state_digest", DRIFT_DIGEST_FIELD}
    delta = value.get("delta_ppm")
    ok = (set(value) == fields and value.get("detector") == "ADWIN" and pos(value.get("window_size"))
        and nat(delta) and 0 < delta < 1_000_000 and isinstance(value.get("change_detected"), bool)
        and isinstance(value.get("detector_state_digest"), str) and bool(value.get("detector_state_digest"))
        and value.get(DRIFT_DIGEST_FIELD) == digest_without(value, DRIFT_DIGEST_FIELD))
    return ok, bool(value.get("change_detected")) if ok else False

def source_supported(source: Mapping[str, Any], expected: str) -> bool:
    digest = source.get(SOURCE_RECEIPT_DIGEST_FIELD)
    required = {
        "maintenance_monitoring_observation_recorded": True,
        "maintenance_monitoring_observation_scope_exactly_bounded": True,
        "verification_completed": False, "verification_debt_open": True,
        "persistent_world_state_changed_by_observation": False,
        "world_model_revision_incremented_by_observation": False,
        "current_plan_revised_by_observation": False,
        "current_policy_activated_by_observation": False,
        "learning_delta_activated_by_observation": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }
    return (isinstance(digest, str) and bool(digest) and digest == expected
        and digest == digest_without(source, SOURCE_RECEIPT_DIGEST_FIELD)
        and all(source.get(k) is v for k, v in required.items()))

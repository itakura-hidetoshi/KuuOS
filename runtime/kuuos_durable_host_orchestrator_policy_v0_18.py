from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    POLICY_VERSION,
    policy_digest,
)


def build_orchestrator_policy(
    *,
    policy_id: str,
    max_assignments_per_cycle: int = 4,
    worker_heartbeat_ttl_ms: int = 60_000,
    max_worker_failure_streak: int = 3,
    allow_degraded_workers: bool = False,
    queue_high_watermark: int = 8,
    dead_letter_observation_threshold: int = 3,
    max_history: int = 512,
    job_weights: Mapping[str, Any] | None = None,
    in_place_supervisor_write_allowed: bool = False,
    in_place_orchestrator_write_allowed: bool = False,
) -> dict[str, Any]:
    weights: dict[str, float] = {}
    for key, value in dict(job_weights or {}).items():
        try:
            weight = float(value)
        except (TypeError, ValueError):
            continue
        if weight > 0.0:
            weights[str(key)] = weight
    packet = {
        "version": POLICY_VERSION,
        "policy_id": str(policy_id),
        "max_assignments_per_cycle": min(64, max(1, int(max_assignments_per_cycle))),
        "worker_heartbeat_ttl_ms": min(86_400_000, max(1, int(worker_heartbeat_ttl_ms))),
        "max_worker_failure_streak": min(1000, max(1, int(max_worker_failure_streak))),
        "allow_degraded_workers": bool(allow_degraded_workers),
        "queue_high_watermark": min(100000, max(1, int(queue_high_watermark))),
        "dead_letter_observation_threshold": min(1000, max(1, int(dead_letter_observation_threshold))),
        "max_history": min(100000, max(1, int(max_history))),
        "job_weights": weights,
        "in_place_supervisor_write_allowed": bool(in_place_supervisor_write_allowed),
        "in_place_orchestrator_write_allowed": bool(in_place_orchestrator_write_allowed),
        "orchestrator_policy_digest": "",
    }
    packet["orchestrator_policy_digest"] = policy_digest(packet)
    return packet


def validate_orchestrator_policy(policy: Mapping[str, Any]) -> None:
    if str(policy.get("version", "")) != POLICY_VERSION:
        raise ValueError("orchestrator_policy_version_invalid")
    digest = str(policy.get("orchestrator_policy_digest", ""))
    if not digest or digest != policy_digest(policy):
        raise ValueError("orchestrator_policy_digest_invalid")
    if not str(policy.get("policy_id", "")).strip():
        raise ValueError("orchestrator_policy_id_missing")
    if int(policy.get("max_assignments_per_cycle", 0) or 0) < 1:
        raise ValueError("orchestrator_assignment_bound_invalid")
    if int(policy.get("worker_heartbeat_ttl_ms", 0) or 0) < 1:
        raise ValueError("worker_heartbeat_ttl_invalid")
    if int(policy.get("dead_letter_observation_threshold", 0) or 0) < 1:
        raise ValueError("dead_letter_threshold_invalid")

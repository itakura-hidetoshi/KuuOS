from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    WORKER_REPORT_VERSION,
    worker_report_digest,
)

WORKER_STATUSES = frozenset({"healthy", "degraded", "draining", "offline"})


def build_worker_report(
    *,
    worker_id: str,
    observed_at_ms: int,
    sequence: int,
    status: str,
    operation_allowlist: Sequence[str],
    capacity_slots: int = 1,
    failure_streak: int = 0,
) -> dict[str, Any]:
    worker_status = str(status)
    if worker_status not in WORKER_STATUSES:
        raise ValueError("worker_status_invalid")
    operations = sorted({str(item).strip() for item in operation_allowlist if str(item).strip()})
    packet = {
        "version": WORKER_REPORT_VERSION,
        "worker_id": str(worker_id),
        "observed_at_ms": max(0, int(observed_at_ms)),
        "sequence": max(0, int(sequence)),
        "status": worker_status,
        "operation_allowlist": operations,
        "capacity_slots": min(64, max(0, int(capacity_slots))),
        "failure_streak": min(1000000, max(0, int(failure_streak))),
        "worker_report_digest": "",
    }
    packet["worker_report_digest"] = worker_report_digest(packet)
    return packet


def validate_worker_report(report: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if str(report.get("version", "")) != WORKER_REPORT_VERSION:
        blockers.append("worker_report_version_invalid")
    digest = str(report.get("worker_report_digest", ""))
    if not digest or digest != worker_report_digest(report):
        blockers.append("worker_report_digest_invalid")
    if not str(report.get("worker_id", "")).strip():
        blockers.append("worker_id_missing")
    if str(report.get("status", "")) not in WORKER_STATUSES:
        blockers.append("worker_status_invalid")
    operations = report.get("operation_allowlist", [])
    if not isinstance(operations, list):
        blockers.append("worker_operation_allowlist_invalid")
    if int(report.get("capacity_slots", 0) or 0) < 0:
        blockers.append("worker_capacity_invalid")
    if int(report.get("failure_streak", 0) or 0) < 0:
        blockers.append("worker_failure_streak_invalid")
    return blockers


def classify_worker_health(
    report: Mapping[str, Any],
    *,
    now_ms: int,
    policy: Mapping[str, Any],
    licensed_operations: set[str],
    registered_operations: set[str],
) -> dict[str, Any]:
    blockers = validate_worker_report(report)
    now = max(0, int(now_ms))
    observed = max(0, int(report.get("observed_at_ms", 0) or 0))
    age = max(0, now - observed)
    ttl = max(1, int(policy.get("worker_heartbeat_ttl_ms", 1) or 1))
    status = str(report.get("status", ""))
    if age > ttl:
        blockers.append("worker_report_stale")
    if status in {"draining", "offline"}:
        blockers.append(f"worker_status_{status}")
    if status == "degraded" and policy.get("allow_degraded_workers") is not True:
        blockers.append("degraded_worker_not_allowed")
    if int(report.get("capacity_slots", 0) or 0) < 1:
        blockers.append("worker_capacity_zero")
    failure_limit = max(1, int(policy.get("max_worker_failure_streak", 1) or 1))
    if int(report.get("failure_streak", 0) or 0) >= failure_limit:
        blockers.append("worker_failure_streak_exceeded")
    operations = {str(item) for item in report.get("operation_allowlist", []) if str(item)}
    shared = sorted(operations & licensed_operations & registered_operations)
    if not shared:
        blockers.append("worker_operation_capability_gap")
    return {
        "worker_id": str(report.get("worker_id", "")),
        "worker_report_digest": str(report.get("worker_report_digest", "")),
        "status": status,
        "age_ms": age,
        "capacity_slots": max(0, int(report.get("capacity_slots", 0) or 0)),
        "failure_streak": max(0, int(report.get("failure_streak", 0) or 0)),
        "shared_operation_allowlist": shared,
        "dispatchable": not blockers,
        "blockers": blockers,
    }

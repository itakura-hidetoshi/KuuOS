from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_qi_window_trajectory_types_v0_29 import (
    BOUNDARY,
    NON_AUTHORITY,
    PACKET_VERSION,
    REPORT_VERSION,
    TRAJECTORY_CLASSES,
    TRAJECTORY_ROUTES,
    average,
    clamp01,
    copy_boundary,
    copy_non_authority,
    packet_digest,
    report_digest,
    require_bool,
    require_bounded,
    require_nonnegative_int,
    require_sequence,
    require_string,
)

REQUIRED_REPORT_FIELDS = (
    "report_id",
    "observed_at_ms",
    "source_v028_report_digest",
    "classification",
    "interval_lower",
    "interval_center",
    "interval_upper",
    "support_score",
    "burden_score",
    "evidence_quality",
    "red_flags_visible",
    "candidate_only",
    "source_trace",
)


def build_trajectory_packet(
    *,
    packet_id: str,
    context_digest: str,
    source_v028_kernel_digest: str,
    process_tensor_lineage_digest: str,
    reports: list[Mapping[str, Any]],
    created_at_ms: int,
) -> dict[str, Any]:
    packet = {
        "version": PACKET_VERSION,
        "packet_id": require_string(packet_id, "packet_id"),
        "context_digest": require_string(context_digest, "context_digest"),
        "source_v028_kernel_digest": require_string(
            source_v028_kernel_digest, "source_v028_kernel_digest"
        ),
        "process_tensor_lineage_digest": require_string(
            process_tensor_lineage_digest, "process_tensor_lineage_digest"
        ),
        "reports": [deepcopy(dict(item)) for item in reports],
        "candidate_only": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "trajectory_packet_digest": "",
    }
    packet["trajectory_packet_digest"] = packet_digest(packet)
    errors = validate_trajectory_packet(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def _validate_report(
    report: Mapping[str, Any], index: int, previous_time: int | None
) -> tuple[list[str], int | None]:
    errors: list[str] = []
    for field in REQUIRED_REPORT_FIELDS:
        if field not in report:
            errors.append(f"reports[{index}].{field}_required")
    try:
        require_string(report.get("report_id"), f"report_{index}_report_id")
        observed_at = require_nonnegative_int(
            report.get("observed_at_ms"), f"report_{index}_observed_at_ms"
        )
        if previous_time is not None and observed_at <= previous_time:
            errors.append(f"reports[{index}].observed_at_ms_not_increasing")
        require_string(
            report.get("source_v028_report_digest"),
            f"report_{index}_source_v028_report_digest",
        )
        require_string(report.get("classification"), f"report_{index}_classification")
        lower = require_bounded(report.get("interval_lower"), f"report_{index}_lower")
        center = require_bounded(report.get("interval_center"), f"report_{index}_center")
        upper = require_bounded(report.get("interval_upper"), f"report_{index}_upper")
        if not lower <= center <= upper:
            errors.append(f"reports[{index}].interval_order_invalid")
        require_bounded(report.get("support_score"), f"report_{index}_support")
        require_bounded(report.get("burden_score"), f"report_{index}_burden")
        require_bounded(report.get("evidence_quality"), f"report_{index}_quality")
        require_bool(report.get("red_flags_visible"), f"report_{index}_red_flags")
        if report.get("candidate_only") is not True:
            errors.append(f"reports[{index}].candidate_only_required")
        require_string(report.get("source_trace"), f"report_{index}_source_trace")
        return errors, observed_at
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
        return errors, previous_time


def validate_trajectory_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if packet.get("version") != PACKET_VERSION:
            errors.append("trajectory_packet_version_invalid")
        for field in (
            "packet_id",
            "context_digest",
            "source_v028_kernel_digest",
            "process_tensor_lineage_digest",
        ):
            require_string(packet.get(field), field)
        reports = require_sequence(packet.get("reports"), "reports")
        previous_time: int | None = None
        seen_ids: set[str] = set()
        seen_digests: set[str] = set()
        for index, raw in enumerate(reports):
            if not isinstance(raw, Mapping):
                errors.append(f"reports[{index}]_mapping_required")
                continue
            report_errors, previous_time = _validate_report(raw, index, previous_time)
            errors.extend(report_errors)
            report_id = str(raw.get("report_id", ""))
            digest = str(raw.get("source_v028_report_digest", ""))
            if report_id in seen_ids:
                errors.append(f"reports[{index}].report_id_duplicate")
            if digest in seen_digests:
                errors.append(f"reports[{index}].source_digest_duplicate")
            seen_ids.add(report_id)
            seen_digests.add(digest)
        if packet.get("candidate_only") is not True:
            errors.append("trajectory_candidate_only_required")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("trajectory_authority_expansion")
        if dict(packet.get("boundary", {})) != BOUNDARY:
            errors.append("trajectory_boundary_invalid")
        require_nonnegative_int(packet.get("created_at_ms"), "created_at_ms")
        if packet.get("trajectory_packet_digest") != packet_digest(packet):
            errors.append("trajectory_packet_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _sign(value: float, epsilon: float = 0.015) -> int:
    if value > epsilon:
        return 1
    if value < -epsilon:
        return -1
    return 0


def _trajectory_metrics(reports: list[Mapping[str, Any]]) -> dict[str, Any]:
    centers = [float(item["interval_center"]) for item in reports]
    lowers = [float(item["interval_lower"]) for item in reports]
    uppers = [float(item["interval_upper"]) for item in reports]
    support = [float(item["support_score"]) for item in reports]
    burden = [float(item["burden_score"]) for item in reports]
    quality = [float(item["evidence_quality"]) for item in reports]
    deltas = [centers[index] - centers[index - 1] for index in range(1, len(centers))]
    nonzero_signs = [value for value in (_sign(delta) for delta in deltas) if value != 0]
    reversals = sum(
        1
        for index in range(1, len(nonzero_signs))
        if nonzero_signs[index] != nonzero_signs[index - 1]
    )
    global_slope = (centers[-1] - centers[0]) / max(1, len(centers) - 1)
    recent_slope = centers[-1] - centers[-2] if len(centers) >= 2 else 0.0
    prior_visible = any(
        str(item.get("classification")) == "HEALING_POTENTIAL_VISIBLE"
        or float(item["interval_lower"]) >= 0.40
        for item in reports[:-1]
    )
    current_constrained = (
        str(reports[-1].get("classification")) == "HEALING_POTENTIAL_CONSTRAINED"
        or uppers[-1] < 0.35
    )
    consecutive_constrained = len(reports) >= 2 and all(
        str(item.get("classification")) == "HEALING_POTENTIAL_CONSTRAINED"
        or float(item["interval_upper"]) < 0.35
        for item in reports[-2:]
    )
    previous_peak = max(centers[:-1]) if len(centers) > 1 else centers[-1]
    scar_depth = clamp01(max(0.0, previous_peak - centers[-1]))
    reopening_memory = clamp01(previous_peak * 0.40) if prior_visible else 0.0
    return {
        "global_slope": global_slope,
        "recent_slope": recent_slope,
        "reversal_count": reversals,
        "average_support": average(support),
        "average_burden": average(burden),
        "average_evidence_quality": average(quality),
        "current_lower": lowers[-1],
        "current_center": centers[-1],
        "current_upper": uppers[-1],
        "previous_peak_center": previous_peak,
        "prior_visible_window": prior_visible,
        "current_constrained": current_constrained,
        "consecutive_constrained": consecutive_constrained,
        "scar_depth": scar_depth,
        "reopening_memory": reopening_memory,
        "red_flags_visible": any(bool(item.get("red_flags_visible")) for item in reports),
    }


def evaluate_trajectory_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_trajectory_packet(packet)
    raw_reports = packet.get("reports", [])
    reports = [item for item in raw_reports if isinstance(item, Mapping)]
    if reports:
        metrics = _trajectory_metrics(reports)
    else:
        metrics = {
            "global_slope": 0.0,
            "recent_slope": 0.0,
            "reversal_count": 0,
            "average_support": 0.0,
            "average_burden": 1.0,
            "average_evidence_quality": 0.0,
            "current_lower": 0.0,
            "current_center": 0.0,
            "current_upper": 0.0,
            "previous_peak_center": 0.0,
            "prior_visible_window": False,
            "current_constrained": False,
            "consecutive_constrained": False,
            "scar_depth": 0.0,
            "reopening_memory": 0.0,
            "red_flags_visible": False,
        }

    if bool(metrics["red_flags_visible"]):
        classification = "REVIEW_HANDOFF"
        route = "REVIEW_HANDOFF"
    elif errors or len(reports) < 3 or float(metrics["average_evidence_quality"]) < 0.35:
        classification = "INSUFFICIENT_HISTORY"
        route = "REOBSERVE"
    elif int(metrics["reversal_count"]) >= 2:
        classification = "WINDOW_OSCILLATING"
        route = "PRESERVE_OSCILLATION"
    elif bool(metrics["prior_visible_window"]) and bool(metrics["current_constrained"]):
        classification = "WINDOW_DORMANT_REOPENABLE"
        route = "PRESERVE_REOPENING_MEMORY"
    elif bool(metrics["consecutive_constrained"]):
        classification = "WINDOW_CONSTRICTING"
        route = "HOLD"
    elif float(metrics["global_slope"]) > 0.04 and float(metrics["current_lower"]) >= 0.30:
        classification = "WINDOW_OPENING"
        route = "CONTINUE_TRAJECTORY_OBSERVATION"
    elif float(metrics["current_lower"]) >= 0.40 and abs(float(metrics["global_slope"])) <= 0.04:
        classification = "WINDOW_STABLE_VISIBLE"
        route = "CONTINUE_TRAJECTORY_OBSERVATION"
    else:
        classification = "INSUFFICIENT_HISTORY"
        route = "REOBSERVE"

    if classification not in TRAJECTORY_CLASSES:
        raise ValueError("trajectory_class_invalid")
    if route not in TRAJECTORY_ROUTES:
        raise ValueError("trajectory_route_invalid")

    report = {
        "version": REPORT_VERSION,
        "packet_id": packet.get("packet_id", ""),
        "source_packet_digest": packet.get("trajectory_packet_digest", ""),
        "valid": not errors,
        "errors": errors,
        "trajectory_classification": classification,
        "route": route,
        "metrics": {
            key: round(value, 6) if isinstance(value, float) else value
            for key, value in metrics.items()
        },
        "history_count": len(reports),
        "single_decline_closed_future_window": False,
        "prior_visible_window_erased": False,
        "relapse_claimed_irreversible": False,
        "prognosis_claimed": False,
        "treatment_route_generated": False,
        "candidate_only": True,
        "source_history_preserved": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "trajectory_report_digest": "",
    }
    report["trajectory_report_digest"] = report_digest(report)
    return report


__all__ = [
    "build_trajectory_packet",
    "evaluate_trajectory_packet",
    "validate_trajectory_packet",
]

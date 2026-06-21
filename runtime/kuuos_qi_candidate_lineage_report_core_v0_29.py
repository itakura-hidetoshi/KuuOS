from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_source_packet_v0_29 import (
    source_digest,
    unique_key_ending,
)
from runtime.kuuos_qi_candidate_lineage_types_v0_29 import require_string


def validate_report_core(report: Mapping[str, Any]) -> tuple[list[str], str]:
    errors: list[str] = []
    digest_field = ""
    try:
        version = require_string(report.get("version"), "source_v028_report_version")
        if not version.startswith("kuuos_qi_") or not version.endswith("_v0_28"):
            errors.append("source_v028_report_version_invalid")
        for field in ("packet_id", "source_packet_digest", "route"):
            require_string(report.get(field), f"source_v028_{field}")
        digest_field = unique_key_ending(report, "_report_digest", "source_v028_report")
        require_string(report.get(digest_field), "source_v028_report_digest")
        if report.get(digest_field) != source_digest(report, digest_field):
            errors.append("source_v028_report_digest_invalid")
        if report.get("candidate_only") is not True:
            errors.append("source_v028_report_candidate_only_required")
        for key, value in report.items():
            if key.endswith("_instruction") and value is not False:
                errors.append("source_v028_instruction_boundary_invalid")
            if key.endswith("_route_generated") and value is not False:
                errors.append("source_v028_action_route_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors, digest_field


__all__ = ["validate_report_core"]

from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_report_core_v0_29 import validate_report_core
from runtime.kuuos_qi_candidate_lineage_report_shape_v0_29 import validate_report_shape
from runtime.kuuos_qi_candidate_lineage_source_packet_v0_29 import validate_source_packet
from runtime.kuuos_qi_candidate_lineage_source_state_v0_29 import validate_source_state


def validate_sources(
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    report: Mapping[str, Any],
) -> tuple[list[str], dict[str, str]]:
    packet_errors, packet_digest_field = validate_source_packet(packet)
    report_errors, report_digest_field = validate_report_core(report)
    shape_errors, summary_field, potential_field = validate_report_shape(report)
    errors = validate_source_state(state) + packet_errors + report_errors + shape_errors
    fields = {
        "packet_digest": packet_digest_field,
        "report_digest": report_digest_field,
        "summary": summary_field,
        "potential": potential_field,
    }
    return errors, fields


__all__ = ["validate_sources"]

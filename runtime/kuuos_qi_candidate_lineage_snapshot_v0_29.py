from __future__ import annotations

from typing import Any, Mapping


def make_source_snapshot(
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    report: Mapping[str, Any],
    packet_digest_field: str,
    report_digest_field: str,
    summary_field: str,
    potential_field: str,
) -> dict[str, Any]:
    return {
        "state_digest": state.get("integrated_operation_state_digest"),
        "packet_digest": packet.get(packet_digest_field),
        "report_digest": report.get(report_digest_field),
        "summary": report.get(summary_field),
        "potential": report.get(potential_field),
    }


__all__ = ["make_source_snapshot"]

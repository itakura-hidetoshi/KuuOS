from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_match_v0_29 import (
    packet_report_match,
    state_packet_match,
)


def all_sources_match(
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    report: Mapping[str, Any],
    packet_digest: Any,
) -> bool:
    return state_packet_match(state, packet) and packet_report_match(
        packet_digest, packet, report
    )


__all__ = ["all_sources_match"]

from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_match_all_v0_29 import all_sources_match


def sources_match_ordered(
    packet_digest: Any,
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    report: Mapping[str, Any],
) -> bool:
    return all_sources_match(state, packet, report, packet_digest)


__all__ = ["sources_match_ordered"]

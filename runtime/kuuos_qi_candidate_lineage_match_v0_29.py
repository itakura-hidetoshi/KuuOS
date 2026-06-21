from __future__ import annotations

from typing import Any, Mapping


def state_packet_match(state: Mapping[str, Any], packet: Mapping[str, Any]) -> bool:
    return packet.get("source_v027_state_digest") == state.get(
        "integrated_operation_state_digest"
    )


def packet_report_match(
    packet_digest: Any, packet: Mapping[str, Any], report: Mapping[str, Any]
) -> bool:
    return report.get("source_packet_digest") == packet_digest and report.get(
        "packet_id"
    ) == packet.get("packet_id")


__all__ = ["packet_report_match", "state_packet_match"]

from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_candidate_lineage_types_v0_29 import require_string, without


def unique_key_ending(value: Mapping[str, Any], suffix: str, name: str) -> str:
    matches = [key for key in value if isinstance(key, str) and key.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"{name}_unique_key_required")
    return matches[0]


def source_digest(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def validate_source_packet(packet: Mapping[str, Any]) -> tuple[list[str], str]:
    errors: list[str] = []
    digest_field = ""
    try:
        version = require_string(packet.get("version"), "source_v028_packet_version")
        if not version.startswith("kuuos_qi_") or not version.endswith("_v0_28"):
            errors.append("source_v028_packet_version_invalid")
        require_string(packet.get("packet_id"), "source_v028_packet_id")
        require_string(
            packet.get("source_v027_state_digest"),
            "source_v028_source_v027_state_digest",
        )
        digest_field = unique_key_ending(
            packet, "_packet_digest", "source_v028_packet"
        )
        require_string(packet.get(digest_field), "source_v028_packet_digest")
        if packet.get(digest_field) != source_digest(packet, digest_field):
            errors.append("source_v028_packet_digest_invalid")
        if packet.get("candidate_only") is not True:
            errors.append("source_v028_packet_candidate_only_required")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors, digest_field


__all__ = ["source_digest", "unique_key_ending", "validate_source_packet"]

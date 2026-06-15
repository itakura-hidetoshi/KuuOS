#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import ROOT_VERSION
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    BUNDLE_VERSION,
    SECTION_VERSION,
    as_list,
    clamp,
    integer,
    valid_digest,
)


def validate_root(root_packet: Mapping[str, Any], blockers: list[str]) -> None:
    if root_packet.get("version") != ROOT_VERSION:
        blockers.append("root_principles_version_invalid")
    if not valid_digest(root_packet, "root_principles_digest"):
        blockers.append("root_principles_digest_invalid")
    if root_packet.get("protected") is not True:
        blockers.append("root_principles_not_protected")
    if root_packet.get("self_rewrite_allowed") is not False:
        blockers.append("root_principles_self_rewrite_not_denied")


def validate_bundle(
    bundle: Mapping[str, Any], agent_id: str, blockers: list[str]
) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("capability_bundle_version_invalid")
        return
    if not valid_digest(bundle, "capability_bundle_digest"):
        blockers.append("capability_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("capability_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("capability_bundle_generation_invalid")
    keys: set[tuple[str, str]] = set()
    for raw in as_list(bundle.get("sections")):
        section = raw if isinstance(raw, Mapping) else {}
        if section.get("version") != SECTION_VERSION:
            blockers.append("capability_section_version_invalid")
        if not valid_digest(section, "capability_section_digest"):
            blockers.append("capability_section_digest_invalid")
        key = (
            str(section.get("federation_adapter_id", "")),
            str(section.get("context_key", "")),
        )
        if not all(key) or key in keys:
            blockers.append("capability_section_key_missing_or_repeated")
        keys.add(key)
        if integer(section.get("observation_count"), -1) < 0:
            blockers.append("capability_section_observation_count_invalid")
        for field in (
            "mean_progress",
            "mean_benefit",
            "mean_harm",
            "mean_recoverability",
            "mean_confidence",
            "mean_utility",
            "connection_coefficient",
        ):
            if clamp(section.get(field), -1.0) < 0.0:
                blockers.append(f"capability_section_{field}_invalid")
    processed = [str(item) for item in as_list(bundle.get("processed_evidence_digests"))]
    if len(processed) != len(set(processed)):
        blockers.append("processed_evidence_digest_repeated")

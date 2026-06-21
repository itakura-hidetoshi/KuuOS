from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import json
import os

from runtime import kuuos_open_ended_background_agency_v0_30 as v030

VERSION = "v0.31"
PACKET_VERSION = "world_evidence_packet_v0_31"
REPORT_VERSION = "endogenous_mission_observation_report_v0_31"

ROUTES = {
    "NO_NEW_MISSION",
    "MISSION_PORTFOLIO_READY",
    "CAPABILITY_DISCOVERY",
    "HOLD",
    "HANDOVER",
}
MISSION_TYPES = {"INVESTIGATE", "DISAMBIGUATE", "CAPABILITY_DISCOVERY"}


def canonical_json(value: Any) -> str:
    return v030.canonical_json(value)


def digest(value: Any) -> str:
    return v030.digest(value)


def make_envelope(body: Mapping[str, Any]) -> dict[str, Any]:
    return v030.make_envelope(body)


def validate_envelope(envelope: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    return v030.validate_envelope(envelope, label=label)


def _hex_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _clean_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _clean_string_list(value: Any, *, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field}_invalid")
    return sorted(set(item.strip() for item in value))


def make_world_evidence_packet(
    *,
    packet_id: str,
    source_state_digest: str,
    world_fragment_digest: str,
    observed_at_ms: int,
    unresolved_items: list[Mapping[str, Any]],
    observation_channels: list[Mapping[str, Any]],
) -> dict[str, Any]:
    packet_id = _clean_text(packet_id, field="packet_id")
    if not _hex_digest(source_state_digest):
        raise ValueError("source_state_digest_invalid")
    if not _hex_digest(world_fragment_digest):
        raise ValueError("world_fragment_digest_invalid")
    if not isinstance(observed_at_ms, int) or observed_at_ms < 0:
        raise ValueError("observed_at_ms_invalid")
    if not isinstance(unresolved_items, list):
        raise ValueError("unresolved_items_invalid")
    if not isinstance(observation_channels, list):
        raise ValueError("observation_channels_invalid")

    normalized_items: list[dict[str, Any]] = []
    seen_item_ids: set[str] = set()
    for raw in unresolved_items:
        if not isinstance(raw, Mapping):
            raise ValueError("unresolved_item_invalid")
        item_id = _clean_text(raw.get("item_id"), field="item_id")
        if item_id in seen_item_ids:
            raise ValueError("unresolved_item_id_duplicate")
        seen_item_ids.add(item_id)
        severity = raw.get("severity")
        uncertainty = raw.get("uncertainty")
        if not isinstance(severity, int) or not 0 <= severity <= 4:
            raise ValueError("severity_invalid")
        if not isinstance(uncertainty, int) or not 0 <= uncertainty <= 4:
            raise ValueError("uncertainty_invalid")
        normalized_items.append({
            "item_id": item_id,
            "question": _clean_text(raw.get("question"), field="question"),
            "severity": severity,
            "uncertainty": uncertainty,
            "evidence_refs": _clean_string_list(raw.get("evidence_refs", []), field="evidence_refs"),
            "counterevidence_refs": _clean_string_list(
                raw.get("counterevidence_refs", []), field="counterevidence_refs"
            ),
        })

    normalized_channels: list[dict[str, Any]] = []
    seen_channel_ids: set[str] = set()
    for raw in observation_channels:
        if not isinstance(raw, Mapping):
            raise ValueError("observation_channel_invalid")
        channel_id = _clean_text(raw.get("channel_id"), field="channel_id")
        if channel_id in seen_channel_ids:
            raise ValueError("observation_channel_id_duplicate")
        seen_channel_ids.add(channel_id)
        normalized_channels.append({
            "channel_id": channel_id,
            "modality": _clean_text(raw.get("modality"), field="modality"),
            "supports_items": _clean_string_list(raw.get("supports_items", ["*"]), field="supports_items"),
            "cost_class": _clean_text(raw.get("cost_class", "UNSPECIFIED"), field="cost_class"),
            "risk_class": _clean_text(raw.get("risk_class", "UNSPECIFIED"), field="risk_class"),
            "latency_class": _clean_text(raw.get("latency_class", "UNSPECIFIED"), field="latency_class"),
        })

    body = {
        "packet_version": PACKET_VERSION,
        "packet_id": packet_id,
        "source_state_digest": source_state_digest,
        "world_fragment_digest": world_fragment_digest,
        "observed_at_ms": observed_at_ms,
        "unresolved_items": sorted(normalized_items, key=lambda item: item["item_id"]),
        "observation_channels": sorted(normalized_channels, key=lambda item: item["channel_id"]),
    }
    return make_envelope(body)


def validate_packet(packet_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(packet_envelope, label="evidence_packet")
    if body.get("packet_version") != PACKET_VERSION:
        raise ValueError("packet_version_invalid")
    rebuilt = make_world_evidence_packet(
        packet_id=body.get("packet_id"),
        source_state_digest=body.get("source_state_digest"),
        world_fragment_digest=body.get("world_fragment_digest"),
        observed_at_ms=body.get("observed_at_ms"),
        unresolved_items=body.get("unresolved_items"),
        observation_channels=body.get("observation_channels"),
    )
    if rebuilt["body_digest"] != packet_envelope.get("body_digest"):
        raise ValueError("packet_normalization_mismatch")
    return body


def _priority(item: Mapping[str, Any]) -> int:
    return (
        int(item["severity"]) * 100
        + int(item["uncertainty"]) * 40
        + len(item["counterevidence_refs"]) * 25
        + min(len(item["evidence_refs"]), 9)
    )


def _candidate_id(prefix: str, source_digest: str, packet_digest: str, item_id: str) -> str:
    token = digest({
        "prefix": prefix,
        "source_state_digest": source_digest,
        "packet_digest": packet_digest,
        "item_id": item_id,
    })[:20]
    return f"{prefix}-{token}"


def _matching_channels(item_id: str, channels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [channel for channel in channels if "*" in channel["supports_items"] or item_id in channel["supports_items"]]


def build_mission_observation_report(
    source_state_envelope: Mapping[str, Any],
    evidence_packet_envelope: Mapping[str, Any],
    *,
    generated_at_ms: int,
) -> dict[str, Any]:
    state = v030.validate_state(source_state_envelope)
    packet = validate_packet(evidence_packet_envelope)
    if packet["source_state_digest"] != source_state_envelope.get("body_digest"):
        raise ValueError("source_state_packet_mismatch")
    if not isinstance(generated_at_ms, int) or generated_at_ms < packet["observed_at_ms"]:
        raise ValueError("generated_at_ms_invalid")

    unresolved_items = packet["unresolved_items"]
    channels = packet["observation_channels"]
    mission_candidates: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []

    for item in unresolved_items:
        item_id = item["item_id"]
        matches = _matching_channels(item_id, channels)
        mission_type = "DISAMBIGUATE" if item["counterevidence_refs"] else "INVESTIGATE"
        mission_id = _candidate_id(
            "mission", source_state_envelope["body_digest"], evidence_packet_envelope["body_digest"], item_id
        )
        mission_candidates.append({
            "mission_candidate_id": mission_id,
            "mission_type": mission_type,
            "source_item_id": item_id,
            "objective": item["question"],
            "priority_score": _priority(item),
            "evidence_refs": item["evidence_refs"],
            "counterevidence_refs": item["counterevidence_refs"],
            "uncertainty": item["uncertainty"],
            "status": "CANDIDATE",
            "grants_activation_authority": False,
            "grants_execution_authority": False,
            "grants_truth_authority": False,
        })

        if matches:
            for channel in matches:
                observation_id = _candidate_id(
                    f"observe-{channel['channel_id']}",
                    source_state_envelope["body_digest"],
                    evidence_packet_envelope["body_digest"],
                    item_id,
                )
                observations.append({
                    "observation_candidate_id": observation_id,
                    "mission_candidate_id": mission_id,
                    "source_item_id": item_id,
                    "channel_id": channel["channel_id"],
                    "modality": channel["modality"],
                    "cost_class": channel["cost_class"],
                    "risk_class": channel["risk_class"],
                    "latency_class": channel["latency_class"],
                    "expected_information_gain_score": _priority(item) + int(item["uncertainty"]) * 20,
                    "status": "PROPOSED",
                    "grants_tool_invocation": False,
                    "grants_actos_invocation": False,
                })
        else:
            observation_id = _candidate_id(
                "observe-capability-gap",
                source_state_envelope["body_digest"],
                evidence_packet_envelope["body_digest"],
                item_id,
            )
            observations.append({
                "observation_candidate_id": observation_id,
                "mission_candidate_id": mission_id,
                "source_item_id": item_id,
                "channel_id": None,
                "modality": "CAPABILITY_DISCOVERY_CANDIDATE",
                "cost_class": "UNKNOWN",
                "risk_class": "UNKNOWN",
                "latency_class": "UNKNOWN",
                "expected_information_gain_score": _priority(item),
                "status": "PROPOSED",
                "grants_tool_invocation": False,
                "grants_actos_invocation": False,
            })

    mission_candidates.sort(key=lambda item: (-item["priority_score"], item["mission_candidate_id"]))
    observations.sort(
        key=lambda item: (-item["expected_information_gain_score"], item["observation_candidate_id"])
    )

    posture = state["background_posture"]
    if state["instance_terminated"] or posture == "HANDED_OVER":
        route = "HANDOVER"
    elif posture == "PAUSED":
        route = "HOLD"
    elif not unresolved_items:
        route = "NO_NEW_MISSION"
    elif any(item["channel_id"] is None for item in observations):
        route = "CAPABILITY_DISCOVERY"
    else:
        route = "MISSION_PORTFOLIO_READY"

    body = {
        "report_version": REPORT_VERSION,
        "source_state_digest": source_state_envelope["body_digest"],
        "root_lineage_digest": state["root_lineage_digest"],
        "evidence_packet_digest": evidence_packet_envelope["body_digest"],
        "packet_id": packet["packet_id"],
        "world_fragment_digest": packet["world_fragment_digest"],
        "generated_at_ms": generated_at_ms,
        "route": route,
        "unresolved_trace": unresolved_items,
        "mission_candidates": mission_candidates,
        "observation_portfolio": observations,
        "preserves_counterevidence": True,
        "preserves_uncertainty": True,
        "plural_candidate_generation": True,
        "mission_candidate_not_activation": True,
        "observation_candidate_not_tool_invocation": True,
        "grants_execution_authority": False,
        "grants_truth_authority": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
    }
    report = make_envelope(body)
    validate_report(report)
    return report


def validate_report(report_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(report_envelope, label="mission_observation_report")
    if body.get("report_version") != REPORT_VERSION:
        raise ValueError("report_version_invalid")
    if body.get("route") not in ROUTES:
        raise ValueError("route_invalid")
    if not _hex_digest(body.get("source_state_digest")):
        raise ValueError("report_source_state_digest_invalid")
    if not _hex_digest(body.get("root_lineage_digest")):
        raise ValueError("report_root_lineage_digest_invalid")
    if not _hex_digest(body.get("evidence_packet_digest")):
        raise ValueError("report_packet_digest_invalid")
    if not isinstance(body.get("mission_candidates"), list):
        raise ValueError("mission_candidates_invalid")
    if not isinstance(body.get("observation_portfolio"), list):
        raise ValueError("observation_portfolio_invalid")
    for mission in body["mission_candidates"]:
        if mission.get("mission_type") not in MISSION_TYPES:
            raise ValueError("mission_type_invalid")
        if mission.get("status") != "CANDIDATE":
            raise ValueError("mission_status_invalid")
        for key in ("grants_activation_authority", "grants_execution_authority", "grants_truth_authority"):
            if mission.get(key) is not False:
                raise ValueError(f"mission_authority_invalid:{key}")
    for observation in body["observation_portfolio"]:
        if observation.get("status") != "PROPOSED":
            raise ValueError("observation_status_invalid")
        if observation.get("grants_tool_invocation") is not False:
            raise ValueError("observation_tool_authority_invalid")
        if observation.get("grants_actos_invocation") is not False:
            raise ValueError("observation_actos_authority_invalid")
    for key in (
        "preserves_counterevidence",
        "preserves_uncertainty",
        "plural_candidate_generation",
        "mission_candidate_not_activation",
        "observation_candidate_not_tool_invocation",
    ):
        if body.get(key) is not True:
            raise ValueError(f"report_boundary_invalid:{key}")
    for key in (
        "grants_execution_authority",
        "grants_truth_authority",
        "grants_plan_activation",
        "grants_actos_invocation",
    ):
        if body.get(key) is not False:
            raise ValueError(f"report_authority_invalid:{key}")
    return body


def _read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("ledger_entry_invalid")
            validate_report(value)
            entries.append(value)
    return entries


@dataclass(frozen=True)
class PersistResult:
    status: str
    report: dict[str, Any]
    ledger_entries: int


def persist_report(*, ledger_path: Path, report_envelope: Mapping[str, Any]) -> PersistResult:
    ledger_path = Path(ledger_path)
    report_body = validate_report(report_envelope)
    entries = _read_ledger(ledger_path)
    report_digest = report_envelope["body_digest"]
    for entry in entries:
        body = validate_report(entry)
        if entry["body_digest"] == report_digest:
            return PersistResult("REPLAYED", entry, len(entries))
        if body["packet_id"] == report_body["packet_id"]:
            raise ValueError("packet_id_reuse_with_different_report")
        if body["evidence_packet_digest"] == report_body["evidence_packet_digest"]:
            raise ValueError("packet_digest_reuse_with_different_report")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(report_envelope) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return PersistResult("COMMITTED", dict(report_envelope), len(entries) + 1)


__all__ = [
    "PersistResult",
    "build_mission_observation_report",
    "canonical_json",
    "digest",
    "make_world_evidence_packet",
    "persist_report",
    "validate_packet",
    "validate_report",
]

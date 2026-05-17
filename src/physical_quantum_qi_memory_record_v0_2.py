#!/usr/bin/env python3
"""Physical Quantum Qi MemoryOS record candidate v0.2.

This module converts a validated Qi OS bridge packet into an append-only
MemoryOS record candidate. It never overwrites memory and never grants world,
truth, proof, clinical, execution, or commit authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Dict, List, Mapping, Sequence

from physical_quantum_qi_os_bridge_v0_2 import AUTHORITY_FALSE_KEYS, validate_qi_os_bridge_packet


@dataclass(frozen=True)
class QiMemoryRecordCandidate:
    record_id: str
    record_type: str
    source_packet_id: str
    source_phase: str
    memory_surface: str
    record_status: str
    append_only: bool
    overwrite_forbidden: bool
    same_root_required: bool
    payload_digest: str
    observed_surfaces: List[str]
    required_next_actions: List[str]
    blockers: List[str]
    authority: Dict[str, bool] = field(default_factory=dict)
    created_at: str = ""
    notes: List[str] = field(default_factory=list)


MEMORY_AUTHORITY_FALSE_KEYS = list(AUTHORITY_FALSE_KEYS) + [
    "memory_commit_authority",
    "memory_root_authority",
]


def _false_authority() -> Dict[str, bool]:
    return {key: False for key in MEMORY_AUTHORITY_FALSE_KEYS}


def _canonical_digest(payload: Mapping[str, object]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(blob.encode("utf-8")).hexdigest()


def build_qi_memory_record_candidate(
    bridge_packet: Mapping[str, object],
    *,
    record_type: str = "physical_quantum_qi_memory_record_candidate_v0_2",
) -> QiMemoryRecordCandidate:
    """Build an append-only MemoryOS record candidate from a bridge packet."""

    bridge_errors = validate_qi_os_bridge_packet(bridge_packet)
    if bridge_errors:
        raise ValueError("invalid Qi OS bridge packet: " + "; ".join(bridge_errors))

    payloads = bridge_packet.get("os_payloads", {})
    if not isinstance(payloads, Mapping):
        raise ValueError("bridge packet os_payloads must be an object")
    memory_payload = payloads.get("MemoryOS", {})
    if not isinstance(memory_payload, Mapping):
        raise ValueError("MemoryOS payload must be an object")
    if memory_payload.get("recordable_history_candidate") is not True:
        raise ValueError("MemoryOS.recordable_history_candidate is required")

    source_packet_id = str(bridge_packet.get("packet_id", "unknown_qi_os_bridge_packet"))
    source_phase = str(bridge_packet.get("phase", "UnknownPhase"))
    digest = _canonical_digest(bridge_packet)
    record_id = "qimem_" + sha256((source_packet_id + ":" + source_phase + ":" + digest).encode("utf-8")).hexdigest()[:24]

    allowed_surfaces = bridge_packet.get("allowed_surfaces", [])
    observed_surfaces = [str(x) for x in allowed_surfaces] if isinstance(allowed_surfaces, Sequence) and not isinstance(allowed_surfaces, (str, bytes)) else []
    next_actions = bridge_packet.get("required_next_actions", [])
    blockers = bridge_packet.get("blockers", [])

    return QiMemoryRecordCandidate(
        record_id=record_id,
        record_type=record_type,
        source_packet_id=source_packet_id,
        source_phase=source_phase,
        memory_surface="MemoryOS.recordable_history_candidate",
        record_status="append_only_candidate",
        append_only=True,
        overwrite_forbidden=True,
        same_root_required=True,
        payload_digest=digest,
        observed_surfaces=observed_surfaces,
        required_next_actions=[str(x) for x in next_actions] if isinstance(next_actions, Sequence) and not isinstance(next_actions, (str, bytes)) else [],
        blockers=[str(x) for x in blockers] if isinstance(blockers, Sequence) and not isinstance(blockers, (str, bytes)) else [],
        authority=_false_authority(),
        created_at=datetime.now(timezone.utc).isoformat(),
        notes=[
            "append_only_candidate",
            "no_memory_overwrite",
            "no_world_root_rewrite",
            "no_execution_authority",
        ],
    )


def memory_record_to_dict(record: QiMemoryRecordCandidate) -> Dict[str, object]:
    return {
        "record_id": record.record_id,
        "record_type": record.record_type,
        "source_packet_id": record.source_packet_id,
        "source_phase": record.source_phase,
        "memory_surface": record.memory_surface,
        "record_status": record.record_status,
        "append_only": record.append_only,
        "overwrite_forbidden": record.overwrite_forbidden,
        "same_root_required": record.same_root_required,
        "payload_digest": record.payload_digest,
        "observed_surfaces": record.observed_surfaces,
        "required_next_actions": record.required_next_actions,
        "blockers": record.blockers,
        "authority": record.authority,
        "created_at": record.created_at,
        "notes": record.notes,
    }


def validate_qi_memory_record_candidate(record: Mapping[str, object]) -> List[str]:
    errors: List[str] = []
    if record.get("record_type") != "physical_quantum_qi_memory_record_candidate_v0_2":
        errors.append("record_type mismatch")
    if record.get("memory_surface") != "MemoryOS.recordable_history_candidate":
        errors.append("memory_surface must be MemoryOS.recordable_history_candidate")
    if record.get("record_status") != "append_only_candidate":
        errors.append("record_status must be append_only_candidate")
    for key in ["append_only", "overwrite_forbidden", "same_root_required"]:
        if record.get(key) is not True:
            errors.append(f"{key} must be true")
    digest = record.get("payload_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        errors.append("payload_digest must be a sha256 hex string")
    authority = record.get("authority", {})
    if not isinstance(authority, Mapping):
        errors.append("authority must be an object")
    else:
        for key in MEMORY_AUTHORITY_FALSE_KEYS:
            if authority.get(key) is not False:
                errors.append(f"authority.{key} must be false")
    return errors

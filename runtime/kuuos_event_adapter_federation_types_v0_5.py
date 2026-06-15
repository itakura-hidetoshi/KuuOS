#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_event_adapter_federation_v0_5"
SOURCE_VERSION = "kuuos_federated_event_source_packet_v0_5"
REGISTRY_VERSION = "kuuos_federated_adapter_registry_v0_5"
PLAN_VERSION = "kuuos_event_adapter_federation_plan_v0_5"
LICENSE_VERSION = "kuuos_event_adapter_federation_license_v0_5"
STATE_VERSION = "kuuos_event_adapter_federation_state_v0_5"
EVIDENCE_VERSION = "kuuos_federated_effect_evidence_v0_5"
LEDGER_VERSION = "kuuos_event_adapter_federation_ledger_record_v0_5"
READY = "KUUOS_EVENT_ADAPTER_FEDERATION_V0_5_READY"
BLOCKED = "KUUOS_EVENT_ADAPTER_FEDERATION_V0_5_BLOCKED"
REPLAYED = "KUUOS_EVENT_ADAPTER_FEDERATION_V0_5_REPLAYED"

ALLOWED_SOURCE_KINDS = {
    "bootstrap",
    "observation",
    "timer",
    "effect_followup",
    "resource_change",
    "relationship_change",
    "recovery",
    "manual",
}
WAKE_KIND_ORDER = (
    "observation",
    "resource_change",
    "relationship_change",
    "recovery",
    "bootstrap",
    "effect_followup",
    "timer",
    "manual",
)
RENEWAL_SOURCE_KINDS = {
    "bootstrap",
    "observation",
    "resource_change",
    "relationship_change",
    "recovery",
}
REQUIRED_BOUNDARY = {
    "multi_source_fan_in": True,
    "single_adapter_selection_per_cycle": True,
    "source_authority_not_transferred": True,
    "adapter_authority_not_inherited": True,
    "source_provenance_preserved": True,
    "normalized_wake_digest_bound": True,
    "one_v0_4_cycle_per_federation_run": True,
    "effect_evidence_returns_to_shared_gauge": True,
    "source_event_replay_forbidden": True,
    "local_effect_backend_only": True,
    "external_network_effect_not_inferred": True,
    "non_markov_lineage_preserved": True,
    "candidate_weighting_not_truth": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class EventAdapterFederationResult:
    version: str
    status: str
    packet_id: str
    federation_run_id: str
    cycle_index: int
    runtime_root: str
    source_count: int
    normalized_signal_count: int
    source_batch_digest: str
    normalized_wake_digest: str
    selected_federation_adapter_id: str
    selected_adapter_profile_digest: str
    supervisor_status: str
    supervisor_cycle_index: int
    telos_renewal_applied: bool
    intervention_applied: bool
    effect_receipt_digest: str
    evidence_digest: str
    next_wake_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    normalized_wake_path: str
    evidence_path: str
    receipt_path: str
    ledger_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == sha(without(value, field))


def source_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "source_packet_digest"))


def registry_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "adapter_registry_digest"))


def batch_digest(source_packets: list[Mapping[str, Any]]) -> str:
    ordered = sorted(
        (
            {
                "source_id": str(packet.get("source_id", "")),
                "source_event_id": str(packet.get("source_event_id", "")),
                "source_packet_digest": str(packet.get("source_packet_digest", "")),
            }
            for packet in source_packets
        ),
        key=lambda item: (item["source_id"], item["source_event_id"], item["source_packet_digest"]),
    )
    return sha(ordered)


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "federation_plan_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "federation_state_digest"))


def evidence_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "evidence_digest"))


def integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clamp(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, number))


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def safe_root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def contains_graph_keys(value: Any) -> bool:
    if isinstance(value, Mapping):
        if FORBIDDEN_GRAPH_KEYS.intersection(value.keys()):
            return True
        return any(contains_graph_keys(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_graph_keys(child) for child in value)
    return False

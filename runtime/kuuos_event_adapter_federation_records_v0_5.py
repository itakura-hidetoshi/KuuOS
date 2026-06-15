#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    EVIDENCE_VERSION,
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    EventAdapterFederationResult,
    as_list,
    evidence_digest,
    integer,
    sha,
    state_digest,
    without,
)


def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "supervisor_state": root / "kuuos_renewable_gauge_supervisor_state_v0_4.json",
        "supervisor_receipt": root / "kuuos_renewable_gauge_supervisor_receipt_v0_4.json",
        "next_wake": root / "kuuos_renewable_gauge_next_wake_v0_4.json",
        "gauge_state": root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "normalized_wake": root / "kuuos_federated_normalized_wake_v0_5.json",
        "evidence": root / "kuuos_federated_effect_evidence_v0_5.json",
        "state": root / "kuuos_event_adapter_federation_state_v0_5.json",
        "receipt": root / "kuuos_event_adapter_federation_receipt_v0_5.json",
        "ledger": root / "kuuos_event_adapter_federation_ledger_v0_5.jsonl",
        "audit": root / "kuuos_event_adapter_federation_audit_v0_5.jsonl",
    }


def source_event_keys(source_packets: list[Mapping[str, Any]]) -> list[str]:
    return sorted(
        f"{str(packet.get('source_id', ''))}::{str(packet.get('source_event_id', ''))}"
        for packet in source_packets
    )


def replay_result(
    row: Mapping[str, Any],
    root: pathlib.Path,
    artifact_paths: Mapping[str, pathlib.Path],
) -> EventAdapterFederationResult:
    return EventAdapterFederationResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        federation_run_id=str(row.get("federation_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        source_count=integer(row.get("source_count"), 0),
        normalized_signal_count=integer(row.get("normalized_signal_count"), 0),
        source_batch_digest=str(row.get("source_batch_digest", "")),
        normalized_wake_digest=str(row.get("normalized_wake_digest", "")),
        selected_federation_adapter_id=str(
            row.get("selected_federation_adapter_id", "")
        ),
        selected_adapter_profile_digest=str(
            row.get("selected_adapter_profile_digest", "")
        ),
        supervisor_status=str(row.get("supervisor_status", "")),
        supervisor_cycle_index=integer(row.get("supervisor_cycle_index"), 0),
        telos_renewal_applied=bool(row.get("telos_renewal_applied")),
        intervention_applied=bool(row.get("intervention_applied")),
        effect_receipt_digest=str(row.get("effect_receipt_digest", "")),
        evidence_digest=str(row.get("evidence_digest", "")),
        next_wake_digest=str(row.get("next_wake_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(artifact_paths["state"]),
        normalized_wake_path=str(artifact_paths["normalized_wake"]),
        evidence_path=str(artifact_paths["evidence"]),
        receipt_path=str(artifact_paths["receipt"]),
        ledger_path=str(artifact_paths["ledger"]),
        audit_path=str(artifact_paths["audit"]),
        blockers=[],
        warnings=["federation_replay_no_new_supervisor_cycle"],
    )


def pending_record(
    *,
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    source_batch: str,
    event_keys: list[str],
    normalized_wake: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    record = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "federation_run_id": run_id,
        "federation_plan_digest": plan.get("federation_plan_digest"),
        "source_batch_digest": source_batch,
        "source_event_keys": event_keys,
        "normalized_wake_digest": normalized_wake.get("wake_event_digest", ""),
        "selected_federation_adapter_id": selected_entry.get(
            "federation_adapter_id", ""
        ),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    record["pending_digest"] = sha(without(record, "pending_digest"))
    return record


def build_evidence(
    *,
    run_id: str,
    source_batch: str,
    normalized_wake: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    selected_profile: Mapping[str, Any],
    supervisor_result: Mapping[str, Any],
    supervisor_receipt: Mapping[str, Any],
    gauge_state: Mapping[str, Any],
    next_wake: Mapping[str, Any],
) -> dict[str, Any]:
    evidence = {
        "version": EVIDENCE_VERSION,
        "evidence_id": "federated-evidence-" + sha(
            {
                "run": run_id,
                "source_batch": source_batch,
                "effect": supervisor_result.get("effect_receipt_digest", ""),
            }
        )[:18],
        "federation_run_id": run_id,
        "source_batch_digest": source_batch,
        "source_provenance": normalized_wake.get("federated_source_provenance", []),
        "normalized_wake_digest": normalized_wake.get("wake_event_digest", ""),
        "selected_federation_adapter_id": selected_entry.get(
            "federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selected_profile.get(
            "adapter_profile_digest", ""
        ),
        "supervisor_status": supervisor_result.get("status", ""),
        "supervisor_run_id": supervisor_result.get("supervisor_run_id", ""),
        "supervisor_cycle_index": supervisor_result.get("cycle_index", 0),
        "supervisor_receipt_digest": sha(supervisor_receipt),
        "telos_renewal_applied": supervisor_result.get(
            "telos_renewal_applied", False
        ),
        "intervention_applied": supervisor_result.get("intervention_applied", False),
        "effect_receipt_digest": supervisor_result.get("effect_receipt_digest", ""),
        "gauge_state_digest": gauge_state.get("gauge_state_digest", ""),
        "next_wake_digest": next_wake.get("next_wake_digest", ""),
        "source_authority_transferred": False,
        "adapter_authority_inherited": False,
        "external_network_effect_performed": False,
        "shared_gauge_evidence": True,
    }
    evidence["evidence_digest"] = evidence_digest(evidence)
    return evidence


def build_state_and_record(
    *,
    previous_state: Mapping[str, Any],
    run_id: str,
    packet_id: str,
    cycle_index: int,
    source_count: int,
    event_keys: list[str],
    source_batch: str,
    normalized_wake: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    selected_profile: Mapping[str, Any],
    supervisor_result: Mapping[str, Any],
    supervisor_state: Mapping[str, Any],
    gauge_state: Mapping[str, Any],
    evidence: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_lineage = as_list(previous_state.get("source_batch_lineage")) + [source_batch]
    adapter_lineage = as_list(previous_state.get("adapter_selection_lineage")) + [
        {
            "federation_adapter_id": selected_entry.get("federation_adapter_id", ""),
            "adapter_profile_digest": selected_profile.get(
                "adapter_profile_digest", ""
            ),
            "evidence_digest": evidence.get("evidence_digest", ""),
        }
    ]
    state = {
        "version": STATE_VERSION,
        "federation_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_federation_state_digest": previous_state.get(
            "federation_state_digest", ""
        ),
        "source_batch_digest": source_batch,
        "source_batch_lineage": source_lineage,
        "adapter_selection_lineage": adapter_lineage,
        "selected_federation_adapter_id": selected_entry.get(
            "federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selected_profile.get(
            "adapter_profile_digest", ""
        ),
        "normalized_wake_digest": normalized_wake.get("wake_event_digest", ""),
        "supervisor_state_digest": supervisor_state.get("supervisor_state_digest", ""),
        "gauge_state_digest": gauge_state.get("gauge_state_digest", ""),
        "effect_evidence_digest": evidence.get("evidence_digest", ""),
        "next_wake_digest": evidence.get("next_wake_digest", ""),
        "total_source_events": integer(previous_state.get("total_source_events"), 0)
        + source_count,
        "total_adapter_selections": integer(
            previous_state.get("total_adapter_selections"), 0
        )
        + 1,
        "single_adapter_selected": True,
        "source_authority_transferred": False,
        "adapter_authority_inherited": False,
        "non_markov_lineage_preserved": True,
        "epoch": int(time.time()),
    }
    state["federation_state_digest"] = state_digest(state)
    record = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "federation_run_id": run_id,
        "cycle_index": cycle_index,
        "source_count": source_count,
        "normalized_signal_count": len(as_list(normalized_wake.get("signals"))),
        "source_batch_digest": source_batch,
        "source_event_keys": event_keys,
        "normalized_wake_digest": normalized_wake.get("wake_event_digest", ""),
        "selected_federation_adapter_id": selected_entry.get(
            "federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selected_profile.get(
            "adapter_profile_digest", ""
        ),
        "supervisor_status": supervisor_result.get("status", ""),
        "supervisor_cycle_index": supervisor_result.get("cycle_index", 0),
        "telos_renewal_applied": supervisor_result.get("telos_renewal_applied", False),
        "intervention_applied": supervisor_result.get("intervention_applied", False),
        "effect_receipt_digest": supervisor_result.get("effect_receipt_digest", ""),
        "evidence_digest": evidence.get("evidence_digest", ""),
        "next_wake_digest": evidence.get("next_wake_digest", ""),
        "federation_state_digest": state["federation_state_digest"],
        "record_digest": "",
    }
    record["record_digest"] = sha(without(record, "record_digest"))
    return state, record


def build_receipt(
    *,
    status: str,
    packet_id: str,
    run_id: str,
    cycle_index: int,
    source_count: int,
    source_batch: str,
    normalized_wake: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    selected_profile: Mapping[str, Any],
    supervisor_result: Mapping[str, Any],
    evidence: Mapping[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "federation_run_id": run_id,
        "cycle_index": cycle_index,
        "source_count": source_count,
        "normalized_signal_count": len(as_list(normalized_wake.get("signals"))),
        "source_batch_digest": source_batch,
        "normalized_wake_digest": normalized_wake.get("wake_event_digest", ""),
        "selected_federation_adapter_id": selected_entry.get(
            "federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selected_profile.get(
            "adapter_profile_digest", ""
        ),
        "supervisor_status": supervisor_result.get("status", ""),
        "supervisor_cycle_index": supervisor_result.get("cycle_index", 0),
        "telos_renewal_applied": supervisor_result.get("telos_renewal_applied", False),
        "intervention_applied": supervisor_result.get("intervention_applied", False),
        "effect_receipt_digest": supervisor_result.get("effect_receipt_digest", ""),
        "evidence_digest": evidence.get("evidence_digest", ""),
        "next_wake_digest": evidence.get("next_wake_digest", ""),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }

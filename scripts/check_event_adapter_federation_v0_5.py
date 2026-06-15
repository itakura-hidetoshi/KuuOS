#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import (  # noqa: E402
    ROOT_VERSION,
    root_digest,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (  # noqa: E402
    ADAPTER_PROFILE_VERSION,
    LOCAL_ACTIONS,
    profile_digest,
)
from runtime.kuuos_event_adapter_federation_core_v0_5 import (  # noqa: E402
    build_event_adapter_federation,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (  # noqa: E402
    normalize_sources,
    select_adapter,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (  # noqa: E402
    BLOCKED,
    LICENSE_VERSION,
    PLAN_VERSION,
    READY,
    REGISTRY_VERSION,
    REPLAYED,
    REQUIRED_BOUNDARY,
    SOURCE_VERSION,
    batch_digest,
    plan_digest,
    registry_digest,
    source_digest,
)


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def root_packet():
    packet = {
        "version": ROOT_VERSION,
        "root_id": "kuuos-root-001",
        "principles": [
            "emptiness",
            "dependent_origination",
            "harmony",
            "contemplation",
            "repairability",
            "benefit_others",
        ],
        "protected": True,
        "self_rewrite_allowed": False,
    }
    packet["root_principles_digest"] = root_digest(packet)
    return packet


def adapter_profile(adapter_id: str, supported=None):
    packet = {
        "version": ADAPTER_PROFILE_VERSION,
        "adapter_id": adapter_id,
        "backend": "qi_local_execution_adapter_v0_2",
        "supported_domain_actions": sorted(supported or LOCAL_ACTIONS),
        "result_to_curvature_mapping": "deterministic_local_effect_v0_3",
    }
    packet["adapter_profile_digest"] = profile_digest(packet)
    return packet


def adapter_registry():
    human_profile = adapter_profile("local-human-context-adapter")
    general_profile = adapter_profile("local-general-context-adapter")
    packet = {
        "version": REGISTRY_VERSION,
        "registry_id": "registry-v05",
        "adapters": [
            {
                "federation_adapter_id": "human-context",
                "enabled": True,
                "priority": 10,
                "accepted_source_kinds": ["observation", "manual", "relationship_change"],
                "accepted_source_ids": ["human-clinician"],
                "external_network_effect_allowed": False,
                "adapter_profile": human_profile,
            },
            {
                "federation_adapter_id": "general-local",
                "enabled": True,
                "priority": 20,
                "accepted_source_kinds": [
                    "bootstrap",
                    "observation",
                    "timer",
                    "effect_followup",
                    "resource_change",
                    "relationship_change",
                    "recovery",
                    "manual",
                ],
                "accepted_source_ids": [],
                "external_network_effect_allowed": False,
                "adapter_profile": general_profile,
            },
        ],
    }
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def signal(signal_id: str, kind: str, target: str, urgency: float = 0.8):
    return {
        "signal_id": signal_id,
        "kind": kind,
        "target": target,
        "magnitude": 0.75,
        "urgency": urgency,
        "evidence": 0.8,
        "uncertainty": 0.2,
        "irreversibility": 0.1,
        "recoverability": 0.9,
        "relational_benefit": 0.85,
        "autonomy_gain": 0.8,
    }


def source(
    source_id: str,
    event_id: str,
    kind: str,
    signals,
    *,
    priority: float,
    trust: float,
    renew: bool,
    intervene: bool,
):
    packet = {
        "version": SOURCE_VERSION,
        "source_id": source_id,
        "source_event_id": event_id,
        "source_kind": kind,
        "priority": priority,
        "trust_weight": trust,
        "world_context_digest": f"world-{source_id}-{event_id}",
        "process_tensor_context_digest": f"process-{source_id}-{event_id}",
        "non_markov_context_digest": f"memory-{source_id}-{event_id}",
        "signals": signals,
        "telos_renewal_requested": renew,
        "intervention_requested": intervene,
    }
    packet["source_packet_digest"] = source_digest(packet)
    return packet


def plan(run_id: str, sources, root, registry, previous=""):
    packet = {
        "version": PLAN_VERSION,
        "federation_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": registry["adapter_registry_digest"],
        "expected_previous_federation_state_digest": previous,
        "max_sources_per_cycle": 8,
        "max_signals_per_source": 8,
        "max_total_signals": 32,
        "max_generated_goals": 8,
        "max_selected_goals": 4,
        "min_goal_score": 0.35,
        "min_action_scale": 0.12,
        "renewal_window_steps": 3,
        "max_bundle_sections": 256,
        "max_new_sections_per_run": 8,
        "max_transports_per_section": 4,
        "routing_table": {},
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["federation_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, sources, root, registry):
    packet = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan_packet["federation_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": registry["adapter_registry_digest"],
        "external_network_effect_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "source_normalization_allowed",
        "adapter_selection_allowed",
        "supervisor_cycle_allowed",
        "effect_evidence_write_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet


def context(root: pathlib.Path):
    return {
        "runtime_root": str(root),
        "event_adapter_federation_enabled": True,
        "execute_one_federated_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def assert_no_graph(value):
    forbidden = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
    if isinstance(value, dict):
        assert forbidden.isdisjoint(value.keys())
        for child in value.values():
            assert_no_graph(child)
    elif isinstance(value, list):
        for child in value:
            assert_no_graph(child)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        registry = adapter_registry()
        first_sources = [
            source(
                "human-clinician",
                "event-human-001",
                "observation",
                [signal("clinical-opportunity", "opportunity", "contextual local action")],
                priority=0.95,
                trust=0.95,
                renew=True,
                intervene=True,
            ),
            source(
                "scheduler",
                "event-timer-001",
                "timer",
                [],
                priority=0.3,
                trust=0.8,
                renew=False,
                intervene=True,
            ),
        ]

        normalized_forward = normalize_sources(first_sources)
        normalized_reverse = normalize_sources(list(reversed(first_sources)))
        assert normalized_forward["wake_event_digest"] == normalized_reverse["wake_event_digest"]
        assert normalized_forward["wake_kind"] == "observation"
        assert normalized_forward["signals"][0]["signal_id"].startswith("human-clinician:")
        selection_blockers = []
        selected_entry, _ = select_adapter(
            registry, first_sources, normalized_forward, selection_blockers
        )
        assert selection_blockers == []
        assert selected_entry["federation_adapter_id"] == "human-context"

        first_plan = plan("federation-001", first_sources, root, registry)
        first = build_event_adapter_federation(
            runtime_context=context(runtime_root),
            source_packets=first_sources,
            root_principles_packet=root,
            adapter_registry=registry,
            federation_plan=first_plan,
            federation_license=license_packet(first_plan, first_sources, root, registry),
        )
        assert first.status == READY, first.blockers
        assert first.source_count == 2
        assert first.normalized_signal_count == 1
        assert first.selected_federation_adapter_id == "human-context"
        assert first.supervisor_cycle_index == 1
        assert first.telos_renewal_applied is True
        assert first.intervention_applied is True
        assert read(runtime_root / "runtime_state.json")["tick"] == 1
        evidence1 = read(runtime_root / "kuuos_federated_effect_evidence_v0_5.json")
        assert len(evidence1["source_provenance"]) == 2
        assert evidence1["source_authority_transferred"] is False
        assert evidence1["adapter_authority_inherited"] is False
        assert evidence1["shared_gauge_evidence"] is True
        assert first.evidence_digest == evidence1["evidence_digest"]
        assert_no_graph(evidence1)

        replay = build_event_adapter_federation(
            runtime_context=context(runtime_root),
            source_packets=first_sources,
            root_principles_packet=root,
            adapter_registry=registry,
            federation_plan=first_plan,
            federation_license=license_packet(first_plan, first_sources, root, registry),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert read(runtime_root / "runtime_state.json")["tick"] == 1

        state1 = read(runtime_root / "kuuos_event_adapter_federation_state_v0_5.json")
        second_sources = [
            source(
                "resource-monitor",
                "event-resource-001",
                "resource_change",
                [signal("resource-opportunity", "opportunity", "new local resource")],
                priority=0.9,
                trust=0.9,
                renew=True,
                intervene=True,
            ),
            source(
                "scheduler",
                "event-timer-002",
                "timer",
                [],
                priority=0.2,
                trust=0.8,
                renew=False,
                intervene=True,
            ),
        ]
        second_plan = plan(
            "federation-002",
            second_sources,
            root,
            registry,
            state1["federation_state_digest"],
        )
        second = build_event_adapter_federation(
            runtime_context=context(runtime_root),
            source_packets=second_sources,
            root_principles_packet=root,
            adapter_registry=registry,
            federation_plan=second_plan,
            federation_license=license_packet(second_plan, second_sources, root, registry),
        )
        assert second.status == READY, second.blockers
        assert second.selected_federation_adapter_id == "general-local"
        assert second.supervisor_cycle_index == 2
        assert second.telos_renewal_applied is True
        assert second.intervention_applied is True
        assert read(runtime_root / "runtime_state.json")["tick"] == 2
        state2 = read(runtime_root / "kuuos_event_adapter_federation_state_v0_5.json")
        assert state2["cycle_index"] == 2
        assert state2["total_source_events"] == 4
        assert state2["total_adapter_selections"] == 2
        assert len(state2["source_batch_lineage"]) == 2
        assert len(state2["adapter_selection_lineage"]) == 2
        bundle2 = read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        assert len(bundle2["holonomy_trace"]) == 2
        assert len(bundle2["integrated_telos_lineage"]) == 2

        duplicate_plan = plan(
            "federation-duplicate-source",
            first_sources,
            root,
            registry,
            state2["federation_state_digest"],
        )
        duplicate = build_event_adapter_federation(
            runtime_context=context(runtime_root),
            source_packets=first_sources,
            root_principles_packet=root,
            adapter_registry=registry,
            federation_plan=duplicate_plan,
            federation_license=license_packet(
                duplicate_plan, first_sources, root, registry
            ),
        )
        assert duplicate.status == BLOCKED
        assert "source_event_already_consumed" in duplicate.blockers

        human_only = {
            "version": REGISTRY_VERSION,
            "registry_id": "human-only",
            "adapters": [registry["adapters"][0]],
        }
        human_only["adapter_registry_digest"] = registry_digest(human_only)
        third_sources = [
            source(
                "resource-monitor",
                "event-resource-002",
                "resource_change",
                [signal("resource-2", "opportunity", "resource two")],
                priority=0.9,
                trust=0.9,
                renew=True,
                intervene=True,
            )
        ]
        no_adapter_plan = plan(
            "federation-no-adapter",
            third_sources,
            root,
            human_only,
            state2["federation_state_digest"],
        )
        no_adapter = build_event_adapter_federation(
            runtime_context=context(runtime_root),
            source_packets=third_sources,
            root_principles_packet=root,
            adapter_registry=human_only,
            federation_plan=no_adapter_plan,
            federation_license=license_packet(
                no_adapter_plan, third_sources, root, human_only
            ),
        )
        assert no_adapter.status == BLOCKED
        assert "no_eligible_federated_adapter" in no_adapter.blockers

        ledger = [
            json.loads(line)
            for line in (runtime_root / "kuuos_event_adapter_federation_ledger_v0_5.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        assert len([row for row in ledger if row.get("phase") == "committed"]) == 2

    formal = (ROOT / "formal/KUOS/OpenHorizon/EventAdapterFederationV0_5.lean").read_text(
        encoding="utf-8"
    )
    for token in (
        "AdapterSelection",
        "selectedAdapterCount_le_one",
        "FederationState",
        "assimilate",
        "iterate_assimilate_sourceEvents",
    ):
        assert token in formal

    manifest = read(ROOT / "manifests/kuuos_event_adapter_federation_v0_5.json")
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS event-adapter federation v0.5 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

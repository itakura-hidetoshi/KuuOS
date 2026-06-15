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
from runtime.kuuos_active_gauge_intervention_effect_v0_3 import (  # noqa: E402
    build_effect_receipt,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (  # noqa: E402
    ADAPTER_PROFILE_VERSION,
    LOCAL_ACTIONS,
    profile_digest,
)
from runtime.kuuos_renewable_gauge_supervisor_core_v0_4 import (  # noqa: E402
    BLOCKED,
    LICENSE_VERSION,
    PLAN_VERSION,
    READY,
    REPLAYED,
    REQUIRED_BOUNDARY,
    WAKE_VERSION,
    build_renewable_gauge_supervisor,
    plan_digest,
    wake_digest,
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


def wake(event_id: str, kind: str, signals, renew: bool, intervene: bool):
    packet = {
        "version": WAKE_VERSION,
        "wake_event_id": event_id,
        "wake_kind": kind,
        "world_context_digest": "world-" + event_id,
        "process_tensor_context_digest": "process-" + event_id,
        "non_markov_context_digest": "memory-" + event_id,
        "signals": signals,
        "telos_renewal_requested": renew,
        "intervention_requested": intervene,
    }
    packet["wake_event_digest"] = wake_digest(packet)
    return packet


def adapter_profile():
    packet = {
        "version": ADAPTER_PROFILE_VERSION,
        "adapter_id": "kuuos-local-domain-adapter",
        "backend": "qi_local_execution_adapter_v0_2",
        "supported_domain_actions": sorted(LOCAL_ACTIONS),
        "result_to_curvature_mapping": "deterministic_local_effect_v0_3",
    }
    packet["adapter_profile_digest"] = profile_digest(packet)
    return packet


def plan(run_id: str, wake_packet, root, profile, previous=""):
    packet = {
        "version": PLAN_VERSION,
        "supervisor_run_id": run_id,
        "agent_id": "agent",
        "expected_wake_event_digest": wake_packet["wake_event_digest"],
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_profile_digest": profile["adapter_profile_digest"],
        "expected_previous_supervisor_state_digest": previous,
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
    packet["supervisor_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, wake_packet, root, profile):
    packet = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan_packet["supervisor_plan_digest"],
        "bound_wake_event_digest": wake_packet["wake_event_digest"],
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_profile_digest": profile["adapter_profile_digest"],
        "external_network_effect_allowed": False,
    }
    for field in (
        "wake_consume_allowed",
        "telos_renewal_allowed",
        "gauge_sync_allowed",
        "local_intervention_allowed",
        "next_wake_write_allowed",
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
        "renewable_gauge_supervisor_enabled": True,
        "execute_one_supervisor_cycle": True,
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
        profile = adapter_profile()

        first_wake = wake(
            "wake-001",
            "bootstrap",
            [
                signal("sig-opportunity", "opportunity", "renewable local action"),
                signal("sig-relationship", "relationship", "human collaboration", 0.65),
            ],
            True,
            True,
        )
        first_plan = plan("supervisor-001", first_wake, root, profile)
        first = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=first_wake,
            root_principles_packet=root,
            supervisor_plan=first_plan,
            supervisor_license=license_packet(first_plan, first_wake, root, profile),
            adapter_profile=profile,
        )
        assert first.status == READY, first.blockers
        assert first.cycle_index == 1
        assert first.telos_renewal_applied is True
        assert first.telos_generation == 1
        assert first.gauge_synchronization_applied is True
        assert first.intervention_applied is True
        assert first.next_action_ready is True
        assert first.next_wake_kind == "effect_followup"
        assert read(runtime_root / "runtime_state.json")["tick"] == 1
        bundle1 = read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        assert len(bundle1["holonomy_trace"]) == 1
        assert_no_graph(bundle1)
        state1 = read(runtime_root / "kuuos_renewable_gauge_supervisor_state_v0_4.json")
        assert state1["local_intervention_count"] == 1
        assert state1["local_intervention_limit"] == 1
        assert state1["local_steps_since_telos"] == 1
        assert state1["renewable_horizon"] is True

        replay = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=first_wake,
            root_principles_packet=root,
            supervisor_plan=first_plan,
            supervisor_license=license_packet(first_plan, first_wake, root, profile),
            adapter_profile=profile,
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert read(runtime_root / "runtime_state.json")["tick"] == 1
        assert len(read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")["holonomy_trace"]) == 1

        follow_wake = wake("wake-002", "effect_followup", [], False, True)
        follow_plan = plan(
            "supervisor-002",
            follow_wake,
            root,
            profile,
            state1["supervisor_state_digest"],
        )
        follow = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=follow_wake,
            root_principles_packet=root,
            supervisor_plan=follow_plan,
            supervisor_license=license_packet(follow_plan, follow_wake, root, profile),
            adapter_profile=profile,
        )
        assert follow.status == READY, follow.blockers
        assert follow.telos_renewal_applied is False
        assert follow.telos_generation == 1
        assert follow.intervention_applied is True
        state2 = read(runtime_root / "kuuos_renewable_gauge_supervisor_state_v0_4.json")
        assert state2["cycle_index"] == 2
        assert state2["local_steps_since_telos"] == 2
        assert state2["total_interventions"] == 2
        assert len(read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")["holonomy_trace"]) == 2

        observation_wake = wake(
            "wake-003",
            "observation",
            [signal("sig-new", "opportunity", "new contextual opportunity")],
            True,
            True,
        )
        observation_plan = plan(
            "supervisor-003",
            observation_wake,
            root,
            profile,
            state2["supervisor_state_digest"],
        )
        observed = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=observation_wake,
            root_principles_packet=root,
            supervisor_plan=observation_plan,
            supervisor_license=license_packet(observation_plan, observation_wake, root, profile),
            adapter_profile=profile,
        )
        assert observed.status == READY, observed.blockers
        assert observed.telos_renewal_applied is True
        assert observed.telos_generation == 2
        assert observed.gauge_synchronization_applied is True
        assert observed.intervention_applied is True
        state3 = read(runtime_root / "kuuos_renewable_gauge_supervisor_state_v0_4.json")
        assert state3["cycle_index"] == 3
        assert state3["local_steps_since_telos"] == 1
        assert state3["total_telos_renewals"] == 2
        bundle3 = read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        assert bundle3["last_integrated_telos_generation"] == 2
        assert len(bundle3["integrated_telos_lineage"]) == 2
        assert len(bundle3["holonomy_trace"]) == 3

        duplicate_plan = plan(
            "supervisor-duplicate-wake",
            observation_wake,
            root,
            profile,
            state3["supervisor_state_digest"],
        )
        duplicate = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=observation_wake,
            root_principles_packet=root,
            supervisor_plan=duplicate_plan,
            supervisor_license=license_packet(duplicate_plan, observation_wake, root, profile),
            adapter_profile=profile,
        )
        assert duplicate.status == BLOCKED
        assert "wake_event_already_consumed" in duplicate.blockers

        no_signal_wake = wake("wake-no-signal", "observation", [], True, True)
        no_signal_plan = plan(
            "supervisor-no-signal",
            no_signal_wake,
            root,
            profile,
            state3["supervisor_state_digest"],
        )
        no_signal = build_renewable_gauge_supervisor(
            runtime_context=context(runtime_root),
            wake_event=no_signal_wake,
            root_principles_packet=root,
            supervisor_plan=no_signal_plan,
            supervisor_license=license_packet(no_signal_plan, no_signal_wake, root, profile),
            adapter_profile=profile,
        )
        assert no_signal.status == BLOCKED
        assert "telos_renewal_signals_missing" in no_signal.blockers

        ledger = [
            json.loads(line)
            for line in (runtime_root / "kuuos_renewable_gauge_supervisor_ledger_v0_4.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        assert len([row for row in ledger if row.get("phase") == "committed"]) == 3

    action = {
        "covariant_action_digest": "action-digest",
        "action_id": "action-id",
        "section_id": "section-id",
        "action_scale": 0.8,
    }
    base_adapter = {
        "local_execution_id": "exec-id",
        "ledger_entry_digest": "result-digest",
        "adapter_version": "adapter-v",
        "execution_committed": True,
        "idempotent_replay": False,
    }
    replay_adapter = dict(base_adapter)
    replay_adapter["idempotent_replay"] = True
    first_effect = build_effect_receipt(action, "advance_tick", base_adapter, "intervention-id")
    replay_effect = build_effect_receipt(action, "advance_tick", replay_adapter, "intervention-id")
    assert first_effect["effect_receipt_digest"] == replay_effect["effect_receipt_digest"]

    formal = (ROOT / "formal/KUOS/OpenHorizon/RenewableGaugeSupervisorV0_4.lean").read_text(
        encoding="utf-8"
    )
    for token in (
        "SupervisorState",
        "renew",
        "renew_generation_strict",
        "iterate_renew_generation",
        "arbitrarily_many_renewals",
    ):
        assert token in formal

    manifest = read(ROOT / "manifests/kuuos_renewable_gauge_supervisor_v0_4.json")
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS renewable gauge supervisor v0.4 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_active_gauge_intervention_loop_core_v0_3 import (  # noqa: E402
    ADAPTER_PROFILE_VERSION,
    BLOCKED,
    LICENSE_VERSION,
    LOCAL_ACTIONS,
    PLAN_VERSION,
    READY,
    REPLAYED,
    REQUIRED_BOUNDARY,
    build_active_gauge_intervention_loop,
    plan_digest,
    profile_digest,
)
from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (  # noqa: E402
    LICENSE_VERSION as GAUGE_LICENSE_VERSION,
    PLAN_VERSION as GAUGE_PLAN_VERSION,
    READY as GAUGE_READY,
    REQUIRED_BOUNDARY as GAUGE_REQUIRED_BOUNDARY,
    build_open_horizon_commitment_gauge,
    plan_digest as gauge_plan_digest,
)


def sha(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def write(path: pathlib.Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def build_telos_source(root: pathlib.Path):
    goals = [
        {
            "goal_id": "goal-a",
            "kind": "opportunity",
            "priority_score": 0.90,
            "action_scale": 0.80,
        },
        {
            "goal_id": "goal-b",
            "kind": "relationship",
            "priority_score": 0.80,
            "action_scale": 0.70,
        },
        {
            "goal_id": "goal-c",
            "kind": "unknown",
            "priority_score": 0.50,
            "action_scale": 0.25,
        },
    ]
    goal_set = {
        "version": "kuuos_open_horizon_goal_set_v0_1",
        "telos_run_id": "telos-run-1",
        "agent_id": "agent",
        "generation_index": 1,
        "source_observation_digest": "obs-digest",
        "root_principles_digest": "root-digest",
        "generated_goals": goals,
        "selected_goals": goals,
        "selection_rule": "plural_kind_first_then_priority",
        "self_generated_subgoals": True,
        "root_principles_unchanged": True,
        "contextual_default_allow": True,
        "uncertainty_response": "scale_or_explore_not_automatic_stop",
    }
    goal_set["goal_set_digest"] = sha(goal_set)

    commitments = []
    moves = ("advance", "micro_intervention", "explore")
    for index, goal in enumerate(goals):
        commitments.append(
            {
                "commitment_id": f"commit-{index}",
                "goal_id": goal["goal_id"],
                "next_move": moves[index],
                "action_scale": goal["action_scale"],
                "repairable": True,
                "replan_after_effect": True,
                "status": "prepared",
            }
        )
    seed = {
        "version": "kuuos_open_horizon_commitment_seed_v0_1",
        "telos_run_id": "telos-run-1",
        "agent_id": "agent",
        "generation_index": 1,
        "goal_set_digest": goal_set["goal_set_digest"],
        "commitments": commitments,
        "execution_posture": "commitment_seed_ready",
        "next_wake": {
            "renew_after_local_steps": 3,
            "events": ["new_observation", "effect_receipt"],
            "global_horizon_fixed": False,
            "local_invocation_finite": True,
        },
        "domain_action_prepared": True,
        "external_effect_not_required_for_telos_generation": True,
    }
    seed["commitment_seed_digest"] = sha(seed)

    telos_state = {
        "version": "kuuos_open_horizon_telos_state_v0_1",
        "agent_id": "agent",
        "telos_run_id": "telos-run-1",
        "generation_index": 1,
        "previous_telos_state_digest": "",
        "source_observation_id": "obs-1",
        "source_observation_digest": "obs-digest",
        "root_principles_digest": "root-digest",
        "goal_set_digest": goal_set["goal_set_digest"],
        "commitment_seed_digest": seed["commitment_seed_digest"],
        "generated_goal_count": 3,
        "selected_goal_count": 3,
        "action_ready_count": 2,
        "exploration_goal_count": 1,
        "open_horizon": True,
        "renewable_horizon": True,
        "local_step_bounded": True,
        "global_generation_cap_declared": False,
        "self_generated_subgoals_active": True,
        "root_principles_unchanged": True,
        "execution_posture": "commitment_seed_ready",
        "next_wake": seed["next_wake"],
        "epoch": 1,
    }
    telos_state["telos_state_digest"] = sha(telos_state)

    write(root / "kuuos_open_horizon_telos_state_v0_1.json", telos_state)
    write(root / "kuuos_open_horizon_goal_set_v0_1.json", goal_set)
    write(root / "kuuos_open_horizon_commitment_seed_v0_1.json", seed)
    return telos_state, goal_set, seed


def gauge_license(plan, telos_state, goal_set, seed, effect=""):
    packet = {
        "version": GAUGE_LICENSE_VERSION,
        "bound_plan_digest": plan["gauge_plan_digest"],
        "bound_telos_state_digest": telos_state["telos_state_digest"],
        "bound_goal_set_digest": goal_set["goal_set_digest"],
        "bound_commitment_seed_digest": seed["commitment_seed_digest"],
        "bound_effect_receipt_digest": effect,
    }
    for field in (
        "source_read_allowed",
        "bundle_initialize_allowed",
        "telos_section_extension_allowed",
        "parallel_transport_allowed",
        "curvature_update_allowed",
        "local_gauge_correction_allowed",
        "holonomy_append_allowed",
        "covariant_action_prepare_allowed",
        "state_write_allowed",
        "bundle_write_allowed",
        "action_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet


def initialize_gauge(root: pathlib.Path, telos_state, goal_set, seed):
    plan = {
        "version": GAUGE_PLAN_VERSION,
        "gauge_run_id": "gauge-init",
        "agent_id": "agent",
        "expected_telos_state_digest": telos_state["telos_state_digest"],
        "expected_goal_set_digest": goal_set["goal_set_digest"],
        "expected_commitment_seed_digest": seed["commitment_seed_digest"],
        "expected_previous_gauge_state_digest": "",
        "expected_effect_receipt_digest": "",
        "max_bundle_sections": 128,
        "max_new_sections_per_run": 8,
        "max_transports_per_section": 4,
        "min_action_scale": 0.02,
        "boundary": dict(GAUGE_REQUIRED_BOUNDARY),
    }
    plan["gauge_plan_digest"] = gauge_plan_digest(plan)
    result = build_open_horizon_commitment_gauge(
        runtime_context={
            "runtime_root": str(root),
            "open_horizon_commitment_gauge_enabled": True,
            "apply_open_horizon_commitment_gauge": True,
        },
        gauge_plan=plan,
        gauge_license=gauge_license(plan, telos_state, goal_set, seed),
    )
    assert result.status == GAUGE_READY, result.blockers


def adapter_profile():
    profile = {
        "version": ADAPTER_PROFILE_VERSION,
        "adapter_id": "kuuos-local-domain-adapter",
        "backend": "qi_local_execution_adapter_v0_2",
        "supported_domain_actions": sorted(LOCAL_ACTIONS),
        "result_to_curvature_mapping": "deterministic_local_effect_v0_3",
    }
    profile["adapter_profile_digest"] = profile_digest(profile)
    return profile


def intervention_plan(root: pathlib.Path, run_id: str, reentry_id: str, routing_table=None):
    gauge_state = json.loads(
        (root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json").read_text(encoding="utf-8")
    )
    bundle = json.loads(
        (root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json").read_text(encoding="utf-8")
    )
    action = json.loads(
        (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_text(encoding="utf-8")
    )
    packet = {
        "version": PLAN_VERSION,
        "intervention_run_id": run_id,
        "gauge_reentry_run_id": reentry_id,
        "agent_id": "agent",
        "adapter_id": "kuuos-local-domain-adapter",
        "expected_gauge_state_digest": gauge_state["gauge_state_digest"],
        "expected_gauge_bundle_digest": bundle["gauge_bundle_digest"],
        "expected_covariant_action_digest": action["covariant_action_digest"],
        "auto_reenter_gauge": True,
        "reentry_max_bundle_sections": 128,
        "reentry_max_new_sections_per_run": 8,
        "reentry_max_transports_per_section": 4,
        "reentry_min_action_scale": 0.02,
        "routing_table": routing_table or {},
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["intervention_plan_digest"] = plan_digest(packet)
    return packet, gauge_state, bundle, action


def intervention_license(plan, profile, gauge_state, bundle, action):
    packet = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan["intervention_plan_digest"],
        "bound_adapter_profile_digest": profile["adapter_profile_digest"],
        "bound_gauge_state_digest": gauge_state["gauge_state_digest"],
        "bound_gauge_bundle_digest": bundle["gauge_bundle_digest"],
        "bound_covariant_action_digest": action["covariant_action_digest"],
    }
    for field in (
        "route_action_allowed",
        "domain_intervention_allowed",
        "local_adapter_execution_allowed",
        "effect_receipt_write_allowed",
        "gauge_reentry_allowed",
        "next_action_continue_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet


def runtime_context(root: pathlib.Path):
    return {
        "runtime_root": str(root),
        "active_gauge_intervention_enabled": True,
        "execute_domain_intervention": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def no_graph_semantics(value):
    forbidden = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
    if isinstance(value, dict):
        assert forbidden.isdisjoint(value.keys())
        for child in value.values():
            no_graph_semantics(child)
    elif isinstance(value, list):
        for child in value:
            no_graph_semantics(child)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        telos_state, goal_set, seed = build_telos_source(root)
        initialize_gauge(root, telos_state, goal_set, seed)
        profile = adapter_profile()

        p1, state1, bundle1, action1 = intervention_plan(root, "intervention-1", "gauge-reentry-1")
        l1 = intervention_license(p1, profile, state1, bundle1, action1)
        result1 = build_active_gauge_intervention_loop(
            runtime_context=runtime_context(root),
            intervention_plan=p1,
            intervention_license=l1,
            adapter_profile=profile,
        )
        assert result1.status == READY, result1.blockers
        assert result1.routed_domain_action == "advance_tick"
        assert result1.local_execution_committed is True
        assert result1.effect_receipt_ready is True
        assert result1.effect_outcome == "success"
        assert result1.curvature_reentry_applied is True
        assert result1.next_action_ready is True
        assert result1.next_action_digest != action1["covariant_action_digest"]

        local_state = json.loads((root / "runtime_state.json").read_text(encoding="utf-8"))
        assert local_state["tick"] == 1
        effect1 = json.loads(
            (root / "kuuos_active_gauge_effect_receipt_v0_3.json").read_text(encoding="utf-8")
        )
        assert effect1["source_action_digest"] == action1["covariant_action_digest"]
        assert effect1["adapter_execution_committed"] is True
        bundle_after_1 = json.loads(
            (root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json").read_text(encoding="utf-8")
        )
        assert len(bundle_after_1["holonomy_trace"]) == 1
        no_graph_semantics(bundle_after_1)

        replay = build_active_gauge_intervention_loop(
            runtime_context=runtime_context(root),
            intervention_plan=p1,
            intervention_license=l1,
            adapter_profile=profile,
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert json.loads((root / "runtime_state.json").read_text(encoding="utf-8"))["tick"] == 1

        current_action = json.loads(
            (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_text(encoding="utf-8")
        )
        p2, state2, bundle2, action2 = intervention_plan(
            root,
            "intervention-2",
            "gauge-reentry-2",
            routing_table={current_action["covariant_step_kind"]: "observe"},
        )
        l2 = intervention_license(p2, profile, state2, bundle2, action2)
        result2 = build_active_gauge_intervention_loop(
            runtime_context=runtime_context(root),
            intervention_plan=p2,
            intervention_license=l2,
            adapter_profile=profile,
        )
        assert result2.status == READY, result2.blockers
        assert result2.routed_domain_action == "observe"
        assert result2.effect_outcome == "partial"
        observation_outbox = root / "outbox" / "observations.jsonl"
        assert observation_outbox.is_file()
        assert len(observation_outbox.read_text(encoding="utf-8").splitlines()) == 1
        bundle_after_2 = json.loads(
            (root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json").read_text(encoding="utf-8")
        )
        assert len(bundle_after_2["holonomy_trace"]) == 2

        stale_plan = dict(p1)
        stale_plan["intervention_run_id"] = "stale-action-run"
        stale_plan["gauge_reentry_run_id"] = "stale-gauge-reentry"
        stale_plan["intervention_plan_digest"] = plan_digest(stale_plan)
        stale_license = dict(l1)
        stale_license["bound_plan_digest"] = stale_plan["intervention_plan_digest"]
        stale = build_active_gauge_intervention_loop(
            runtime_context=runtime_context(root),
            intervention_plan=stale_plan,
            intervention_license=stale_license,
            adapter_profile=profile,
        )
        assert stale.status == BLOCKED
        assert any("mismatch" in blocker or "invalid" in blocker for blocker in stale.blockers)

        bad_profile = dict(profile)
        bad_profile["backend"] = "unsupported"
        bad_profile["adapter_profile_digest"] = profile_digest(bad_profile)
        p3, state3, bundle3, action3 = intervention_plan(root, "bad-profile", "bad-profile-reentry")
        bad_license = intervention_license(p3, bad_profile, state3, bundle3, action3)
        bad = build_active_gauge_intervention_loop(
            runtime_context=runtime_context(root),
            intervention_plan=p3,
            intervention_license=bad_license,
            adapter_profile=bad_profile,
        )
        assert bad.status == BLOCKED
        assert "adapter_backend_unsupported" in bad.blockers

        ledger_lines = (
            root / "kuuos_active_gauge_intervention_ledger_v0_3.jsonl"
        ).read_text(encoding="utf-8").splitlines()
        committed = [json.loads(line) for line in ledger_lines if json.loads(line).get("phase") == "committed"]
        assert len(committed) == 2
        assert all(row["effect_receipt_ready"] for row in committed)

    formal = (ROOT / "formal/KUOS/OpenHorizon/ActiveGaugeInterventionV0_3.lean").read_text(
        encoding="utf-8"
    )
    for token in (
        "EffectReceipt",
        "discreteCurvature",
        "transformReceipt",
        "discreteCurvature_gauge_covariant",
        "flat_effect_gauge_invariant",
    ):
        assert token in formal

    manifest = json.loads(
        (ROOT / "manifests/kuuos_active_gauge_intervention_loop_v0_3.json").read_text(
            encoding="utf-8"
        )
    )
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS active gauge intervention loop v0.3 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

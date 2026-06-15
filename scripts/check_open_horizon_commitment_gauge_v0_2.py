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

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (  # noqa: E402
    ACTION_VERSION,
    BLOCKED,
    BUNDLE_VERSION,
    COMMITMENT_SEED_VERSION,
    EFFECT_VERSION,
    GOAL_SET_VERSION,
    LICENSE_VERSION,
    PLAN_VERSION,
    READY,
    REQUIRED_BOUNDARY,
    TELOS_STATE_VERSION,
    build_open_horizon_commitment_gauge,
    effect_digest,
    plan_digest,
)


def sha(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def source(root: pathlib.Path, generation=1, previous="", run_id="telos-1", commitment_suffix=""):
    goals = [
        {"goal_id": f"goal-a{commitment_suffix}", "kind": "opportunity", "priority_score": 0.90, "action_scale": 0.8},
        {"goal_id": f"goal-b{commitment_suffix}", "kind": "relationship", "priority_score": 0.80, "action_scale": 0.7},
        {"goal_id": f"goal-c{commitment_suffix}", "kind": "unknown", "priority_score": 0.50, "action_scale": 0.25},
    ]
    goal_set = {
        "version": GOAL_SET_VERSION,
        "telos_run_id": run_id,
        "agent_id": "agent",
        "generation_index": generation,
        "generated_goals": goals,
        "selected_goals": goals,
        "selection_rule": "plural_kind_first_then_priority",
        "self_generated_subgoals": True,
        "root_principles_unchanged": True,
        "contextual_default_allow": True,
        "uncertainty_response": "scale_or_explore_not_automatic_stop",
    }
    goal_set["goal_set_digest"] = sha(goal_set)
    moves = ("advance", "micro_intervention", "explore")
    commitments = []
    for index, goal in enumerate(goals):
        commitments.append(
            {
                "commitment_id": f"commit-{index}{commitment_suffix}",
                "goal_id": goal["goal_id"],
                "next_move": moves[index],
                "action_scale": goal["action_scale"],
                "repairable": True,
                "replan_after_effect": True,
                "status": "prepared",
            }
        )
    seed = {
        "version": COMMITMENT_SEED_VERSION,
        "telos_run_id": run_id,
        "agent_id": "agent",
        "generation_index": generation,
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
    state = {
        "version": TELOS_STATE_VERSION,
        "agent_id": "agent",
        "telos_run_id": run_id,
        "generation_index": generation,
        "previous_telos_state_digest": previous,
        "source_observation_id": "obs",
        "source_observation_digest": "obs-digest",
        "root_principles_digest": "root",
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
        "epoch": generation,
    }
    state["telos_state_digest"] = sha(state)
    write(root / "kuuos_open_horizon_telos_state_v0_1.json", state)
    write(root / "kuuos_open_horizon_goal_set_v0_1.json", goal_set)
    write(root / "kuuos_open_horizon_commitment_seed_v0_1.json", seed)
    return state, goal_set, seed


def plan(run_id, state, goals, seed, previous="", effect="", max_new=8):
    packet = {
        "version": PLAN_VERSION,
        "gauge_run_id": run_id,
        "agent_id": "agent",
        "expected_telos_state_digest": state["telos_state_digest"],
        "expected_goal_set_digest": goals["goal_set_digest"],
        "expected_commitment_seed_digest": seed["commitment_seed_digest"],
        "expected_previous_gauge_state_digest": previous,
        "expected_effect_receipt_digest": effect,
        "max_bundle_sections": 128,
        "max_new_sections_per_run": max_new,
        "max_transports_per_section": 3,
        "min_action_scale": 0.02,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["gauge_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, state, goals, seed, effect=""):
    return {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan_packet["gauge_plan_digest"],
        "bound_telos_state_digest": state["telos_state_digest"],
        "bound_goal_set_digest": goals["goal_set_digest"],
        "bound_commitment_seed_digest": seed["commitment_seed_digest"],
        "bound_effect_receipt_digest": effect,
        "source_read_allowed": True,
        "bundle_initialize_allowed": True,
        "telos_section_extension_allowed": True,
        "parallel_transport_allowed": True,
        "curvature_update_allowed": True,
        "local_gauge_correction_allowed": True,
        "holonomy_append_allowed": True,
        "covariant_action_prepare_allowed": True,
        "state_write_allowed": True,
        "bundle_write_allowed": True,
        "action_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def context(root):
    return {
        "runtime_root": str(root),
        "open_horizon_commitment_gauge_enabled": True,
        "apply_open_horizon_commitment_gauge": True,
    }


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def effect(action, receipt_id, outcome, continuation="continue", harm=0.1, progress=0.25):
    packet = {
        "version": EFFECT_VERSION,
        "effect_receipt_id": receipt_id,
        "source_action_digest": action["covariant_action_digest"],
        "action_id": action["action_id"],
        "section_id": action["section_id"],
        "outcome": outcome,
        "continuation_signal": continuation,
        "progress_delta": progress,
        "observed_benefit": 0.7 if outcome in {"success", "partial"} else 0.2,
        "observed_harm": harm,
        "recoverability": 0.85,
        "confidence": 0.8,
        "result_digest": "result-" + receipt_id,
    }
    packet["effect_receipt_digest"] = effect_digest(packet)
    return packet


def assert_no_graph_semantics(value):
    forbidden = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
    if isinstance(value, dict):
        assert forbidden.isdisjoint(value.keys()), forbidden.intersection(value.keys())
        for child in value.values():
            assert_no_graph_semantics(child)
    elif isinstance(value, list):
        for child in value:
            assert_no_graph_semantics(child)


def run():
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        telos, goals, seed = source(root)

        p1 = plan("gauge-1", telos, goals, seed)
        l1 = license_packet(p1, telos, goals, seed)
        r1 = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p1, gauge_license=l1
        )
        assert r1.status == READY, r1.blockers
        assert r1.integrated_section_count == 3
        assert r1.section_count == 3
        assert r1.action_ready is True
        assert r1.covariant_step_kind == "covariant_advance"
        state1 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")
        action1 = read(root / "kuuos_open_horizon_covariant_action_v0_2.json")
        bundle1 = read(root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        assert action1["version"] == ACTION_VERSION
        assert bundle1["version"] == BUNDLE_VERSION
        assert bundle1["base_manifold"]["global_task_list_fixed"] is False
        assert bundle1["structure_group"] == "contextual_commitment_gauge_group"
        assert_no_graph_semantics(bundle1)
        initial_signature = action1["gauge_invariant_signature"]

        p_poll = plan("gauge-poll", telos, goals, seed, state1["gauge_state_digest"])
        l_poll = license_packet(p_poll, telos, goals, seed)
        action_bytes = (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        poll = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p_poll, gauge_license=l_poll
        )
        assert poll.status == READY
        assert poll.stop_reason == "outstanding_covariant_action_preserved"
        assert action_bytes == (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        poll_replay = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p_poll, gauge_license=l_poll
        )
        assert poll_replay.status == BLOCKED
        assert "gauge_run_replay_detected" in poll_replay.blockers

        e1 = effect(action1, "effect-1", "partial", "continue")
        p2 = plan("gauge-2", telos, goals, seed, state1["gauge_state_digest"], e1["effect_receipt_digest"])
        l2 = license_packet(p2, telos, goals, seed, e1["effect_receipt_digest"])
        r2 = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p2, gauge_license=l2, effect_receipt=e1
        )
        assert r2.status == READY, r2.blockers
        assert r2.effect_applied is True
        assert r2.curvature_update_count == 1
        assert r2.holonomy_depth == 1
        state2 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")
        action2 = read(root / "kuuos_open_horizon_covariant_action_v0_2.json")
        bundle2 = read(root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        transformed = next(s for s in bundle2["local_sections"] if s["section_id"] == action1["section_id"])
        assert transformed["gauge_frame_index"] == 1
        assert transformed["gauge_invariant_signature"] == initial_signature
        assert transformed["curvature_norm"] > 0
        assert len(bundle2["curvature_history"]) == 1
        assert_no_graph_semantics(bundle2)

        e2 = effect(action2, "effect-2", "failure", "continue", harm=0.4, progress=0.0)
        p3 = plan("gauge-3", telos, goals, seed, state2["gauge_state_digest"], e2["effect_receipt_digest"])
        l3 = license_packet(p3, telos, goals, seed, e2["effect_receipt_digest"])
        r3 = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p3, gauge_license=l3, effect_receipt=e2
        )
        assert r3.status == READY, r3.blockers
        bundle3 = read(root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        corrected = next(s for s in bundle3["local_sections"] if s["section_id"] == action2["section_id"])
        assert corrected["transport_kind"] == "local_repair_gauge"
        assert corrected["gauge_correction_applied"] is True
        assert corrected["action_scale"] > 0
        assert len(bundle3["holonomy_trace"]) == 2
        state3 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")

        old_telos = telos["telos_state_digest"]
        telos2, goals2, seed2 = source(root, generation=2, previous=old_telos, run_id="telos-2", commitment_suffix="-new")
        outstanding_bytes = (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        p4 = plan("gauge-4", telos2, goals2, seed2, state3["gauge_state_digest"])
        l4 = license_packet(p4, telos2, goals2, seed2)
        r4 = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p4, gauge_license=l4
        )
        assert r4.status == READY, r4.blockers
        assert r4.integrated_section_count == 3
        assert outstanding_bytes == (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        bundle4 = read(root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json")
        assert bundle4["last_integrated_telos_generation"] == 2
        assert len(bundle4["integrated_telos_lineage"]) == 2
        assert len(bundle4["local_sections"]) == 6

        state4 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")
        p_replay = plan("gauge-replay", telos2, goals2, seed2, state4["gauge_state_digest"], e2["effect_receipt_digest"])
        l_replay = license_packet(p_replay, telos2, goals2, seed2, e2["effect_receipt_digest"])
        replay = build_open_horizon_commitment_gauge(
            runtime_context=context(root), gauge_plan=p_replay, gauge_license=l_replay, effect_receipt=e2
        )
        assert replay.status == BLOCKED
        assert "effect_receipt_replay_detected" in replay.blockers

        lines = (root / "kuuos_open_horizon_commitment_gauge_ledger_v0_2.jsonl").read_text().splitlines()
        assert len(lines) >= 5

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        telos, goals, seed = source(root)
        p1 = plan("budget-1", telos, goals, seed, max_new=1)
        l1 = license_packet(p1, telos, goals, seed)
        r1 = build_open_horizon_commitment_gauge(runtime_context=context(root), gauge_plan=p1, gauge_license=l1)
        assert r1.integrated_section_count == 1
        state1 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")
        action_bytes = (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        p2 = plan("budget-2", telos, goals, seed, state1["gauge_state_digest"], max_new=1)
        l2 = license_packet(p2, telos, goals, seed)
        r2 = build_open_horizon_commitment_gauge(runtime_context=context(root), gauge_plan=p2, gauge_license=l2)
        assert r2.integrated_section_count == 1
        assert action_bytes == (root / "kuuos_open_horizon_covariant_action_v0_2.json").read_bytes()
        state2 = read(root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json")
        p3 = plan("budget-3", telos, goals, seed, state2["gauge_state_digest"], max_new=1)
        l3 = license_packet(p3, telos, goals, seed)
        r3 = build_open_horizon_commitment_gauge(runtime_context=context(root), gauge_plan=p3, gauge_license=l3)
        assert r3.integrated_section_count == 1
        assert r3.section_count == 3

    formal = (ROOT / "formal/KUOS/OpenHorizon/CommitmentGaugeV0_2.lean").read_text(encoding="utf-8")
    for token in ("gaugeTransform", "curvature", "curvature_gauge_covariant", "flatness_gauge_invariant"):
        assert token in formal
    manifest = json.loads((ROOT / "manifests/kuuos_open_horizon_commitment_gauge_v0_2.json").read_text())
    for group in ("runtime", "scripts", "docs", "examples", "formal", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS open-horizon commitment gauge v0.2 checks")


if __name__ == "__main__":
    run()

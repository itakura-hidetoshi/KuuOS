#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_planos_world_conditioned_objective_distribution_update_kernel_v0_1 import (
    STATUS_READY,
    build_world_conditioned_objective_distribution_update,
    compute_prior_distribution_digest,
    compute_world_conditioned_action_bundle_digest,
)


def _projections():
    return {
        "continue": "projection-continue",
        "reobserve": "projection-reobserve",
        "hold": "projection-hold",
        "terminate_candidate": "projection-terminate",
    }


def _plan_actions():
    return {
        "continue": 0.40,
        "reobserve": 0.30,
        "hold": 0.10,
        "terminate_candidate": 0.80,
    }


def _world_actions():
    return {
        "continue": 0.60,
        "reobserve": 0.10,
        "hold": 0.00,
        "terminate_candidate": 1.20,
    }


def _combined_actions():
    return {
        "continue": 0.70,
        "reobserve": 0.35,
        "hold": 0.10,
        "terminate_candidate": 1.40,
    }


def _prior():
    return {
        "continue": 0.35,
        "reobserve": 0.30,
        "hold": 0.25,
        "terminate_candidate": 0.10,
    }


def _build(**overrides):
    projections = overrides.pop("candidate_world_projection_digests", _projections())
    plan_actions = overrides.pop("plan_transition_action_map", _plan_actions())
    world_actions = overrides.pop("world_transition_action_map", _world_actions())
    combined_actions = overrides.pop(
        "combined_transition_action_map", _combined_actions()
    )
    prior = overrides.pop("prior_distribution", _prior())
    args = {
        "source_world_conditioned_metric_certificate_digest": "v100-certificate",
        "source_world_binding_digest": "world-binding-v14-rev7",
        "source_world_model_state_digest": "world-state-v14-rev7",
        "source_world_model_revision": 7,
        "source_world_lineage_digest": "world-lineage-v14-rev7",
        "world_conditioned_action_bundle_digest": (
            compute_world_conditioned_action_bundle_digest(
                candidate_world_projection_digests=projections,
                plan_transition_action_map=plan_actions,
                world_transition_action_map=world_actions,
                combined_transition_action_map=combined_actions,
            )
        ),
        "candidate_world_projection_digests": projections,
        "plan_transition_action_map": plan_actions,
        "world_transition_action_map": world_actions,
        "combined_transition_action_map": combined_actions,
        "prior_distribution_digest": compute_prior_distribution_digest(prior),
        "prior_distribution": prior,
        "admissible_candidate_ids": ["continue", "reobserve", "hold"],
        "beta": 1.0,
        "entropy_weight": 0.25,
        "hold_floor": 0.20,
    }
    args.update(overrides)
    return build_world_conditioned_objective_distribution_update(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.update is not None
    update = result.update
    distribution = update["next_distribution"]
    assert abs(sum(distribution.values()) - 1.0) < 1e-9
    assert distribution["hold"] >= 0.20
    assert distribution["continue"] > 0.0
    assert distribution["reobserve"] > 0.0
    assert distribution["terminate_candidate"] == 0.0
    assert update["candidate_mass_nonnegative"] is True
    assert update["normalized_next_distribution"] is True
    assert update["admissible_support_preserved"] is True
    assert update["positive_prior_support_preserved"] is True
    assert update["hold_mass_preserved"] is True
    assert update["candidate_field_retained"] is True
    assert update["nonadmissible_candidates_zero_mass"] is True
    assert update["persistent_world_state_unchanged"] is True
    assert update["world_model_prediction_not_truth"] is True
    assert update["world_mutation_not_granted"] is True
    assert update["history_read_only"] is True
    assert update["qi_grants_no_authority"] is True
    assert update["decision_selection_performed"] is False
    assert update["selected_candidate_id"] == ""
    assert update["future_only"] is True
    assert update["active_now"] is False
    assert update["execution_permission"] is False

    exploratory = _build(entropy_weight=2.0)
    assert exploratory.status == STATUS_READY
    assert exploratory.update is not None
    assert exploratory.update["next_distribution"]["hold"] >= 0.20

    mismatched_actions = _combined_actions()
    mismatched_actions.pop("hold")
    negative_actions = _combined_actions()
    negative_actions["continue"] = -0.1
    invalid_prior = _prior()
    invalid_prior["reobserve"] = 0.0
    duplicate_projection = _projections()
    duplicate_projection["hold"] = duplicate_projection["continue"]
    below_plan = _combined_actions()
    below_plan["continue"] = 0.1

    blocked = [
        _build(source_world_conditioned_metric_certificate_digest=""),
        _build(source_world_binding_digest=""),
        _build(source_world_model_revision=-1),
        _build(world_conditioned_action_bundle_digest="wrong"),
        _build(prior_distribution_digest="wrong"),
        _build(beta=-0.1),
        _build(entropy_weight=-0.1),
        _build(hold_floor=1.0),
        _build(admissible_candidate_ids=[]),
        _build(admissible_candidate_ids=["hold", "hold"]),
        _build(admissible_candidate_ids=["repair"]),
        _build(combined_transition_action_map=mismatched_actions),
        _build(combined_transition_action_map=negative_actions),
        _build(prior_distribution=invalid_prior),
        _build(candidate_world_projection_digests=duplicate_projection),
        _build(combined_transition_action_map=below_plan),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.update is None

    print(
        "PASS: PlanOS WORLD-Conditioned Objective Distribution Update "
        "Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

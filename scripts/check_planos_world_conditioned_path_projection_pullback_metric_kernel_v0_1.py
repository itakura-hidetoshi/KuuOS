#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_planos_world_conditioned_path_projection_pullback_metric_kernel_v0_1 import (
    STATUS_READY,
    build_world_conditioned_path_projection_pullback_metric_certificate,
    compute_candidate_world_projection_digest,
    compute_conditioned_plan_metric_digest,
    compute_plan_coordinate_schema_digest,
    compute_world_binding_digest,
    compute_world_coordinate_schema_digest,
    compute_world_metric_digest,
)


def plan_weights():
    return [
        {"coordinate": "goal", "weight": 1.0},
        {"coordinate": "reroute", "weight": 0.7},
        {"coordinate": "verification", "weight": 1.2},
    ]


def world_weights():
    return [
        {"world_coordinate": "mission_alignment", "weight": 2.0},
        {"world_coordinate": "risk_exposure", "weight": 1.5},
        {"world_coordinate": "uncertainty", "weight": 0.8},
    ]


def candidate(candidate_id: str, scale: float = 1.0):
    delta = {"goal": 0.2 * scale, "reroute": -0.1 * scale, "verification": 0.3 * scale}
    jacobian = {
        "mission_alignment": {"goal": 1.0, "reroute": 0.1, "verification": 0.0},
        "risk_exposure": {"goal": 0.2, "reroute": -0.5, "verification": -0.1},
        "uncertainty": {"goal": 0.0, "reroute": 0.3, "verification": -0.6},
    }
    projected = {a: sum(row[c] * delta[c] for c in delta) for a, row in jacobian.items()}
    value = {
        "candidate_id": candidate_id,
        "parameter_delta": delta,
        "world_jacobian": jacobian,
        "projected_world_delta": projected,
        "persistent_world_state_digest_before": "world-state-v14-rev7",
        "persistent_world_state_digest_after": "world-state-v14-rev7",
        "projection_not_fact": True,
        "world_prediction_not_truth": True,
        "world_mutation_requested": False,
        "candidate_world_projection_digest": "",
    }
    value["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(value)
    return value


def build(**overrides):
    pweights = overrides.pop("conditioned_plan_metric_weights", plan_weights())
    wweights = overrides.pop("world_metric_weights", world_weights())
    binding = {
        "world_model_kind": "indra_qi_mandala_causal_projection",
        "world_model_state_digest": "world-state-v14-rev7",
        "world_model_revision": 7,
        "world_lineage_digest": "world-lineage-v14-rev7",
        "world_patch_id": "clinical-local-patch",
        "world_patch_projection_digest": "world-patch-projection-v3",
        "observation_operator_digest": "observation-operator-v2",
        "causal_graph_digest": "causal-graph-v14",
        "causal_variable_schema_digest": "causal-schema-v14",
        "causal_state_digest": "causal-state-v14-rev7",
        "uncertainty_state_digest": "uncertainty-state-v14-rev7",
        "active_interventions_digest": "active-interventions-none-digest",
        "process_tensor_context_digest": "process-tensor-context-v6",
        "history_window_digest": "history-window-v6",
        "holonomy_context_digest": "holonomy-context-v1",
        "transport_residue_digest": "transport-residue-v1",
    }
    args = {
        "source_qi_conditioned_metric_certificate_digest": "planos-v099-metric-certificate",
        **binding,
        "world_binding_digest": compute_world_binding_digest(**binding),
        "plan_coordinate_schema_digest": compute_plan_coordinate_schema_digest(pweights),
        "conditioned_plan_metric_digest": compute_conditioned_plan_metric_digest(pweights),
        "conditioned_plan_metric_weights": pweights,
        "world_coordinate_schema_digest": compute_world_coordinate_schema_digest(wweights),
        "world_metric_digest": compute_world_metric_digest(wweights),
        "world_metric_weights": wweights,
        "pullback_weight": 0.6,
        "candidate_projections": [candidate("continue"), candidate("reobserve", 0.5), candidate("hold", 0.0)],
    }
    args.update(overrides)
    return build_world_conditioned_path_projection_pullback_metric_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    c = result.certificate
    for name in (
        "world_pullback_metric_nonnegative",
        "combined_qi_world_metric_nonnegative",
        "plan_coordinate_dimension_preserved",
        "source_world_state_digest_preserved",
        "persistent_world_state_unchanged",
        "counterfactual_projection_not_fact",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "holonomy_context_preserved",
        "transport_residue_visible",
        "candidate_field_retained",
        "history_read_only",
        "qi_grants_no_authority",
        "future_only",
    ):
        assert c[name] is True
    assert c["decision_selection_performed"] is False
    assert c["active_now"] is False
    assert c["execution_permission"] is False
    for candidate_id, combined in c["combined_transition_action_map"].items():
        plan = c["plan_transition_action_map"][candidate_id]
        world = c["world_transition_action_map"][candidate_id]
        assert combined >= plan >= 0.0
        assert abs(combined - (plan + 0.6 * world)) < 1e-10

    changed = candidate("changed")
    changed["persistent_world_state_digest_after"] = "mutated"
    changed["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(changed)
    fact = candidate("fact")
    fact["projection_not_fact"] = False
    fact["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(fact)
    mutation = candidate("mutation")
    mutation["world_mutation_requested"] = True
    mutation["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(mutation)
    bad_delta = candidate("bad-delta")
    bad_delta["projected_world_delta"]["uncertainty"] += 0.2
    bad_delta["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(bad_delta)
    bad_digest = candidate("bad-digest")
    bad_digest["candidate_world_projection_digest"] = "wrong"
    zero_world = [{"world_coordinate": e["world_coordinate"], "weight": 0.0} for e in world_weights()]

    blocked = [
        build(source_qi_conditioned_metric_certificate_digest=""),
        build(world_binding_digest="wrong"),
        build(world_model_revision=-1),
        build(world_model_kind="unknown"),
        build(plan_coordinate_schema_digest="wrong"),
        build(conditioned_plan_metric_digest="wrong"),
        build(world_coordinate_schema_digest="wrong"),
        build(world_metric_digest="wrong"),
        build(pullback_weight=-0.1),
        build(candidate_projections=[]),
        build(candidate_projections=[changed]),
        build(candidate_projections=[fact]),
        build(candidate_projections=[mutation]),
        build(candidate_projections=[bad_delta]),
        build(candidate_projections=[bad_digest]),
        build(world_metric_weights=zero_world),
        build(holonomy_context_digest=""),
        build(transport_residue_digest=""),
    ]
    duplicate = candidate("same")
    duplicate_two = deepcopy(duplicate)
    duplicate_two["candidate_world_projection_digest"] = compute_candidate_world_projection_digest(duplicate_two)
    blocked.append(build(candidate_projections=[duplicate, duplicate_two]))
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print("PASS: PlanOS WORLD-Conditioned Path Projection Pullback Metric Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

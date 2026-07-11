#!/usr/bin/env python3
from runtime.kuuos_planos_world_conditioned_distribution_decision_handoff_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_world_conditioned_distribution_decision_handoff_certificate,
    compute_next_distribution_digest,
)


def _projections():
    return {
        "continue": "projection-continue",
        "reobserve": "projection-reobserve",
        "hold": "projection-hold",
        "terminate_candidate": "projection-terminate",
    }


def _actions():
    return {
        "continue": 0.70,
        "reobserve": 0.35,
        "hold": 0.10,
        "terminate_candidate": 1.40,
    }


def _distribution():
    return {
        "continue": 0.24,
        "reobserve": 0.36,
        "hold": 0.40,
        "terminate_candidate": 0.0,
    }


def _build(**overrides):
    projections = overrides.pop("candidate_world_projection_digests", _projections())
    actions = overrides.pop("combined_transition_action_map", _actions())
    distribution = overrides.pop("next_distribution", _distribution())
    args = {
        "source_distribution_update_digest": "v101-update",
        "source_next_distribution_digest": compute_next_distribution_digest(
            distribution
        ),
        "source_world_conditioned_action_bundle_digest": "v100-action-bundle",
        "source_world_binding_digest": "world-binding-v14-rev7",
        "source_world_model_state_digest": "world-state-v14-rev7",
        "source_world_model_revision": 7,
        "source_world_lineage_digest": "world-lineage-v14-rev7",
        "candidate_world_projection_digests": projections,
        "combined_transition_action_map": actions,
        "next_distribution": distribution,
        "admissible_candidate_ids": ["continue", "reobserve", "hold"],
        "minimum_lead_margin": 0.03,
        "maximum_normalized_entropy": 0.99,
        "hold_review_threshold": 0.35,
    }
    args.update(overrides)
    return build_world_conditioned_distribution_decision_handoff_certificate(
        **args
    )


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.certificate is not None
    certificate = result.certificate
    assert certificate["ranked_candidate_ids"] == [
        "hold",
        "reobserve",
        "continue",
    ]
    assert certificate["top_mass_candidate_ids"] == ["hold"]
    assert certificate["top_mass"] == 0.40
    assert certificate["runner_up_mass"] == 0.36
    assert abs(certificate["lead_margin"] - 0.04) < 1e-9
    assert certificate["lead_margin_sufficient"] is True
    assert certificate["entropy_within_review_limit"] is True
    assert certificate["hold_review_guard_active"] is True
    assert certificate["decision_review_ready"] is True
    assert certificate["handoff_disposition"] == "hold_guarded_review"
    assert certificate["ranking_is_advisory_only"] is True
    assert certificate["candidate_field_retained"] is True
    assert certificate["persistent_world_state_unchanged"] is True
    assert certificate["world_model_prediction_not_truth"] is True
    assert certificate["world_mutation_not_granted"] is True
    assert certificate["history_read_only"] is True
    assert certificate["qi_grants_no_authority"] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["selected_candidate_id"] == ""
    assert certificate["decision_authority_granted"] is False
    assert certificate["future_only"] is True
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    tied = _distribution()
    tied["reobserve"] = 0.40
    tied["continue"] = 0.20
    tie_result = _build(next_distribution=tied)
    assert tie_result.status == STATUS_READY
    assert tie_result.certificate is not None
    assert tie_result.certificate["top_mass_is_tied"] is True
    assert tie_result.certificate["decision_review_ready"] is False
    assert tie_result.certificate["handoff_disposition"] == "top_mass_tie_review"

    diffuse = {
        "continue": 0.34,
        "reobserve": 0.33,
        "hold": 0.33,
        "terminate_candidate": 0.0,
    }
    diffuse_result = _build(
        next_distribution=diffuse,
        minimum_lead_margin=0.0,
        maximum_normalized_entropy=0.80,
        hold_review_threshold=0.90,
    )
    assert diffuse_result.status == STATUS_READY
    assert diffuse_result.certificate is not None
    assert diffuse_result.certificate["entropy_within_review_limit"] is False
    assert (
        diffuse_result.certificate["handoff_disposition"]
        == "diffuse_distribution_review"
    )

    single = {
        "continue": 0.0,
        "reobserve": 0.0,
        "hold": 1.0,
        "terminate_candidate": 0.0,
    }
    single_result = _build(
        next_distribution=single,
        admissible_candidate_ids=["hold"],
    )
    assert single_result.status == STATUS_READY
    assert single_result.certificate is not None
    assert (
        single_result.certificate["handoff_disposition"]
        == "single_supported_candidate_review"
    )
    assert single_result.certificate["decision_selection_performed"] is False

    mismatched_actions = _actions()
    mismatched_actions.pop("hold")
    invalid_distribution = _distribution()
    invalid_distribution["continue"] = -0.1
    invalid_support = _distribution()
    invalid_support["reobserve"] = 0.0
    invalid_support["continue"] = 0.60
    nonadmissible_mass = _distribution()
    nonadmissible_mass["terminate_candidate"] = 0.05
    nonadmissible_mass["continue"] = 0.19
    duplicate_projection = _projections()
    duplicate_projection["hold"] = duplicate_projection["continue"]

    blocked = [
        _build(source_distribution_update_digest=""),
        _build(source_world_binding_digest=""),
        _build(source_world_model_revision=-1),
        _build(source_next_distribution_digest="wrong"),
        _build(minimum_lead_margin=-0.1),
        _build(maximum_normalized_entropy=1.1),
        _build(hold_review_threshold=1.1),
        _build(admissible_candidate_ids=[]),
        _build(admissible_candidate_ids=["hold", "hold"]),
        _build(admissible_candidate_ids=["repair"]),
        _build(combined_transition_action_map=mismatched_actions),
        _build(next_distribution=invalid_distribution),
        _build(next_distribution=invalid_support),
        _build(next_distribution=nonadmissible_mass),
        _build(candidate_world_projection_digests=duplicate_projection),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print(
        "PASS: PlanOS WORLD-Conditioned Distribution Decision Handoff "
        "Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from runtime.kuuos_decisionos_world_conditioned_relational_deliberation_v0_6 import (
    STATUS_READY,
    build_decisionos_world_conditioned_relational_deliberation_receipt,
    canonical_digest,
    compute_candidate_deliberation_input_digest,
    compute_deliberation_bundle_digest,
    compute_source_candidate_intake_digest,
    compute_source_evidence_bundle_digest,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_decisionos_world_conditioned_relational_deliberation_v0_6"
CHECKER_NAME = "check_decisionos_world_conditioned_relational_deliberation_v0_6.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def validate_repository_surface() -> None:
    runtime = ROOT / "runtime/kuuos_decisionos_world_conditioned_relational_deliberation_v0_6.py"
    checker = ROOT / "scripts/check_decisionos_world_conditioned_relational_deliberation_v0_6.py"
    formal = ROOT / "formal/KUOS/DecisionOS/WorldConditionedRelationalDeliberationV0_6.lean"
    aggregate = ROOT / "formal/KuuOSDecisionOSV0_6.lean"
    docs = ROOT / "docs/KUUOS_DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_v0_6.md"
    manifest_path = ROOT / "manifests/kuuos_decisionos_world_conditioned_relational_deliberation_v0_6.json"
    runner = ROOT / "scripts/run_decision_os_full_checks.py"
    workflow = ROOT / ".github/workflows/decision-os-validation.yml"
    source = ROOT / "runtime/kuuos_decisionos_world_conditioned_distribution_handoff_intake_validation_v0_5.py"
    for path in (runtime, checker, formal, aggregate, docs, manifest_path, runner, workflow, source):
        require(path.is_file(), f"missing file: {path}")
    require_tokens(aggregate, ("KUOS.DecisionOS.WorldConditionedRelationalDeliberationV0_6",))
    require_tokens(
        formal,
        (
            "WorldConditionedRelationalDeliberationReceipt",
            "relational_frontier_is_admissible",
            "required_review_candidates_remain_in_source_field",
            "relational_deliberation_preserves_candidate_field",
            "source_probability_and_action_remain_advisory",
            "relational_partial_order_forbids_scalar_selection_shortcut",
            "deliberation_preserves_wa_stakeholder_relational_dissent_and_minority",
            "relational_deliberation_assigns_responsibility_without_selection_authority",
            "relational_deliberation_preserves_world_history_and_qi_boundaries",
            "relational_deliberation_is_not_decision_plan_synthesis_or_execution",
        ),
    )
    require_tokens(
        docs,
        (
            "関係的部分順序",
            "relational frontier",
            "確率順位は未来経路分布の情報",
            "選択権限を生成しない",
            "WORLD model stateは変更しない",
        ),
    )
    require_tokens(runner, (CHECKER_NAME, "v0.1-v0.6"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["validator"] == str(checker.relative_to(ROOT)), "validator mismatch")
    for name, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {name}")
    for name, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {name}")


def source_candidate_item(
    candidate_id: str,
    *,
    projection: str,
    mass: float,
    action: float,
    rank: int,
    admissible: bool,
    dissent: bool = False,
    minority: bool = False,
) -> dict:
    item = {
        "candidate_id": candidate_id,
        "candidate_world_projection_digest": projection,
        "probability_mass": mass,
        "combined_transition_action": action,
        "advisory_rank": rank,
        "admissible": admissible,
        "wa_evidence_digests": [f"wa-{candidate_id}"] if admissible else [],
        "stakeholder_evidence_digests": [f"stakeholder-{candidate_id}"] if admissible else [],
        "relational_evidence_digests": [f"relational-{candidate_id}"] if admissible else [],
        "dissent_evidence_digests": [f"dissent-{candidate_id}"] if dissent else [],
        "dissent_absence_attested": not dissent,
        "minority_evidence_digests": [f"minority-{candidate_id}"] if minority else [],
        "minority_absence_attested": not minority,
        "zero_mass_reason_digest": "" if admissible else f"excluded-{candidate_id}",
        "candidate_intake_digest": "",
    }
    item["candidate_intake_digest"] = compute_source_candidate_intake_digest(item)
    return item


def source_receipt() -> dict:
    projections = {
        "continue": "projection-continue",
        "reobserve": "projection-reobserve",
        "hold": "projection-hold",
        "terminate_candidate": "projection-terminate",
    }
    distribution = {
        "continue": 0.40,
        "reobserve": 0.35,
        "hold": 0.25,
        "terminate_candidate": 0.0,
    }
    actions = {
        "continue": 0.70,
        "reobserve": 0.35,
        "hold": 0.10,
        "terminate_candidate": 1.40,
    }
    items = [
        source_candidate_item(
            "continue",
            projection=projections["continue"],
            mass=distribution["continue"],
            action=actions["continue"],
            rank=1,
            admissible=True,
            dissent=True,
        ),
        source_candidate_item(
            "reobserve",
            projection=projections["reobserve"],
            mass=distribution["reobserve"],
            action=actions["reobserve"],
            rank=2,
            admissible=True,
        ),
        source_candidate_item(
            "hold",
            projection=projections["hold"],
            mass=distribution["hold"],
            action=actions["hold"],
            rank=3,
            admissible=True,
            minority=True,
        ),
        source_candidate_item(
            "terminate_candidate",
            projection=projections["terminate_candidate"],
            mass=distribution["terminate_candidate"],
            action=actions["terminate_candidate"],
            rank=0,
            admissible=False,
        ),
    ]
    receipt = {
        "kernel": "DecisionOS WORLD-Conditioned Distribution Handoff Intake Validation Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.5",
        "status": "DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY",
        "source_planos_version": "v1.02",
        "source_handoff_certificate_digest": "planos-handoff-v102",
        "source_decision_handoff_input_digest": "planos-handoff-input-v102",
        "source_distribution_update_digest": "planos-distribution-update-v101",
        "source_next_distribution_digest": canonical_digest(distribution),
        "source_world_binding_digest": "world-binding-v14-rev7",
        "source_world_model_state_digest": "world-state-v14-rev7",
        "source_world_model_revision": 7,
        "source_world_lineage_digest": "world-lineage-v14-rev7",
        "source_handoff_disposition": "separated_distribution_review",
        "source_decision_review_ready": True,
        "candidate_world_projection_digests": dict(sorted(projections.items())),
        "next_distribution": dict(sorted(distribution.items())),
        "combined_transition_action_map": dict(sorted(actions.items())),
        "advisory_ranking_records": [
            {
                "rank": 1,
                "candidate_id": "continue",
                "probability_mass": 0.40,
                "combined_transition_action": 0.70,
                "candidate_world_projection_digest": projections["continue"],
            },
            {
                "rank": 2,
                "candidate_id": "reobserve",
                "probability_mass": 0.35,
                "combined_transition_action": 0.35,
                "candidate_world_projection_digest": projections["reobserve"],
            },
            {
                "rank": 3,
                "candidate_id": "hold",
                "probability_mass": 0.25,
                "combined_transition_action": 0.10,
                "candidate_world_projection_digest": projections["hold"],
            },
        ],
        "all_candidate_ids": sorted(projections),
        "admissible_candidate_ids": ["continue", "hold", "reobserve"],
        "retained_nonadmissible_candidate_ids": ["terminate_candidate"],
        "stakeholder_context_digest": "stakeholder-context-v1",
        "relational_context_digest": "relational-context-v1",
        "wa_context_digest": "wa-context-v1",
        "dissent_registry_digest": "dissent-registry-v1",
        "minority_registry_digest": "minority-registry-v1",
        "candidate_evidence_items": sorted(items, key=lambda item: item["candidate_id"]),
        "evidence_bundle_digest": "",
        "dissent_present_candidate_ids": ["continue"],
        "dissent_absence_attested_candidate_ids": [
            "hold",
            "reobserve",
            "terminate_candidate",
        ],
        "minority_present_candidate_ids": ["hold"],
        "minority_absence_attested_candidate_ids": [
            "continue",
            "reobserve",
            "terminate_candidate",
        ],
        "intake_owned_by_decision_os": True,
        "source_owned_by_plan_os": True,
        "deliberation_intake_ready": True,
        "all_candidates_considered": True,
        "candidate_identity_preserved": True,
        "retained_alternatives_preserved": True,
        "wa_evidence_preserved": True,
        "stakeholder_context_preserved": True,
        "relational_context_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "silent_substitution_detected": False,
        "ranking_is_advisory_only": True,
        "decisionos_owns_selection": True,
        "selection_authority_granted_by_intake": False,
        "decision_selection_performed": False,
        "selected_candidate_id": "",
        "decision_receipt_issued": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "plan_synthesis_performed": False,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["evidence_bundle_digest"] = compute_source_evidence_bundle_digest(receipt)
    receipt["decisionos_intake_receipt_digest"] = canonical_digest(receipt)
    return receipt


def deliberation_item(
    source: dict,
    candidate_id: str,
    *,
    wa: float,
    stakeholder: float,
    relational: float,
    dissent: float,
    minority: float,
    uncertainty: float,
    blockers: list[str] | None = None,
) -> dict:
    source_map = {
        item["candidate_id"]: item for item in source["candidate_evidence_items"]
    }
    admissible = candidate_id in source["admissible_candidate_ids"]
    item = {
        "candidate_id": candidate_id,
        "source_candidate_intake_digest": source_map[candidate_id][
            "candidate_intake_digest"
        ],
        "source_admissible": admissible,
        "wa_assessment_digest": f"wa-assessment-{candidate_id}",
        "stakeholder_assessment_digest": f"stakeholder-assessment-{candidate_id}",
        "relational_assessment_digest": f"relational-assessment-{candidate_id}",
        "dissent_assessment_digest": f"dissent-assessment-{candidate_id}",
        "minority_assessment_digest": f"minority-assessment-{candidate_id}",
        "wa_support": wa,
        "stakeholder_support": stakeholder,
        "relational_support": relational,
        "dissent_pressure": dissent,
        "minority_impact_risk": minority,
        "uncertainty_burden": uncertainty,
        "review_blocker_digests": blockers or [],
        "exclusion_review_digest": "" if admissible else f"exclusion-review-{candidate_id}",
        "candidate_deliberation_input_digest": "",
    }
    item["candidate_deliberation_input_digest"] = (
        compute_candidate_deliberation_input_digest(item)
    )
    return item


def base_inputs(source: dict) -> list[dict]:
    return [
        deliberation_item(
            source,
            "continue",
            wa=0.90,
            stakeholder=0.85,
            relational=0.88,
            dissent=0.20,
            minority=0.15,
            uncertainty=0.20,
        ),
        deliberation_item(
            source,
            "reobserve",
            wa=0.80,
            stakeholder=0.82,
            relational=0.84,
            dissent=0.10,
            minority=0.10,
            uncertainty=0.25,
        ),
        deliberation_item(
            source,
            "hold",
            wa=0.78,
            stakeholder=0.86,
            relational=0.82,
            dissent=0.10,
            minority=0.20,
            uncertainty=0.15,
        ),
        deliberation_item(
            source,
            "terminate_candidate",
            wa=0.0,
            stakeholder=0.0,
            relational=0.0,
            dissent=0.0,
            minority=0.0,
            uncertainty=0.0,
        ),
    ]


def resign_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("decisionos_intake_receipt_digest", None)
    value["decisionos_intake_receipt_digest"] = canonical_digest(value)
    return value


def replace_input(items: list[dict], candidate_id: str, **changes) -> list[dict]:
    values = deepcopy(items)
    for item in values:
        if item["candidate_id"] == candidate_id:
            item.update(changes)
            item["candidate_deliberation_input_digest"] = (
                compute_candidate_deliberation_input_digest(item)
            )
            return values
    raise AssertionError(candidate_id)


def build(**overrides):
    if "source_intake_receipt" in overrides:
        source = overrides.pop("source_intake_receipt")
    else:
        source = source_receipt()
    if "candidate_deliberation_inputs" in overrides:
        items = overrides.pop("candidate_deliberation_inputs")
    else:
        items = base_inputs(source) if source else []
    policy = overrides.pop("deliberation_policy_digest", "relational-policy-v1")
    thresholds = {
        "minimum_wa_support": 0.60,
        "minimum_stakeholder_support": 0.60,
        "minimum_relational_support": 0.60,
        "maximum_dissent_pressure_before_review": 0.40,
        "maximum_minority_impact_risk": 0.40,
        "maximum_uncertainty_burden": 0.60,
        "dominance_tolerance": 0.0,
    }
    for key in list(thresholds):
        if key in overrides:
            thresholds[key] = overrides.pop(key)
    if "deliberation_bundle_digest" in overrides:
        bundle = overrides.pop("deliberation_bundle_digest")
    else:
        source_digest = source.get("decisionos_intake_receipt_digest", "") if isinstance(source, dict) else ""
        bundle = compute_deliberation_bundle_digest(
            source_intake_receipt_digest=source_digest,
            deliberation_policy_digest=policy,
            threshold_config=thresholds,
            candidate_deliberation_inputs=items,
        )
    assert not overrides
    return build_decisionos_world_conditioned_relational_deliberation_receipt(
        source_intake_receipt=source,
        deliberation_policy_digest=policy,
        candidate_deliberation_inputs=items,
        deliberation_bundle_digest=bundle,
        **thresholds,
    )


def main() -> int:
    validate_repository_surface()
    result = build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["status"] == "DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY"
    assert receipt["relationally_reviewable_candidate_ids"] == ["reobserve"]
    assert receipt["relational_frontier_candidate_ids"] == ["reobserve"]
    assert receipt["dissent_review_candidate_ids"] == ["continue"]
    assert receipt["minority_protection_candidate_ids"] == ["hold"]
    assert receipt["retained_nonadmissible_candidate_ids"] == ["terminate_candidate"]
    assert receipt["required_review_candidate_ids"] == ["continue", "hold", "reobserve"]
    assert receipt["deliberation_disposition"] == "minority_protection_review"
    assert receipt["source_probability_used_as_advisory_only"] is True
    assert receipt["relational_partial_order_used"] is True
    assert receipt["single_scalar_utility_selection_forbidden"] is True
    assert receipt["relational_deliberation_performed"] is True
    assert receipt["decision_selection_performed"] is False
    assert receipt["selected_candidate_id"] == ""
    assert receipt["decision_receipt_issued"] is False
    assert receipt["world_mutation_not_granted"] is True
    assert receipt["execution_permission"] is False

    source = source_receipt()
    inputs = base_inputs(source)

    bad_source_digest = deepcopy(source)
    bad_source_digest["decisionos_intake_receipt_digest"] = "wrong"

    promoted_selection = deepcopy(source)
    promoted_selection["decision_selection_performed"] = True
    promoted_selection = resign_source(promoted_selection)

    selected_candidate = deepcopy(source)
    selected_candidate["selected_candidate_id"] = "continue"
    selected_candidate = resign_source(selected_candidate)

    bad_source_item = deepcopy(source)
    bad_source_item["candidate_evidence_items"][0]["candidate_intake_digest"] = "wrong"
    bad_source_item["evidence_bundle_digest"] = compute_source_evidence_bundle_digest(
        bad_source_item
    )
    bad_source_item = resign_source(bad_source_item)

    missing_input = inputs[:-1]
    duplicate_input = inputs + [deepcopy(inputs[0])]
    wrong_source_digest = replace_input(
        inputs,
        "continue",
        source_candidate_intake_digest="wrong",
    )
    wrong_admissibility = replace_input(
        inputs,
        "continue",
        source_admissible=False,
        exclusion_review_digest="exclusion-review-continue",
    )
    invalid_metric = replace_input(inputs, "continue", wa_support=1.2)
    missing_assessment = replace_input(inputs, "continue", wa_assessment_digest="")
    duplicate_blockers = replace_input(
        inputs,
        "continue",
        review_blocker_digests=["same", "same"],
    )
    forbidden_exclusion = replace_input(
        inputs,
        "continue",
        exclusion_review_digest="forbidden",
    )
    missing_exclusion = replace_input(
        inputs,
        "terminate_candidate",
        exclusion_review_digest="",
    )
    bad_input_digest = deepcopy(inputs)
    bad_input_digest[0]["candidate_deliberation_input_digest"] = "wrong"

    blocked = [
        build(source_intake_receipt={}),
        build(source_intake_receipt=bad_source_digest),
        build(source_intake_receipt=promoted_selection),
        build(source_intake_receipt=selected_candidate),
        build(source_intake_receipt=bad_source_item),
        build(deliberation_policy_digest=""),
        build(deliberation_bundle_digest="wrong"),
        build(minimum_wa_support=-0.1),
        build(candidate_deliberation_inputs=missing_input),
        build(candidate_deliberation_inputs=duplicate_input),
        build(candidate_deliberation_inputs=wrong_source_digest),
        build(candidate_deliberation_inputs=wrong_admissibility),
        build(candidate_deliberation_inputs=invalid_metric),
        build(candidate_deliberation_inputs=missing_assessment),
        build(candidate_deliberation_inputs=duplicate_blockers),
        build(candidate_deliberation_inputs=forbidden_exclusion),
        build(candidate_deliberation_inputs=missing_exclusion),
        build(candidate_deliberation_inputs=bad_input_digest),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None

    print("PASS: DecisionOS WORLD-Conditioned Relational Deliberation v0.6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

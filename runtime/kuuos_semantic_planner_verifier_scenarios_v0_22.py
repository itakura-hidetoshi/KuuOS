from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_goal_portfolio_v0_20 import build_goal_portfolio, build_goal_proposal
from runtime.kuuos_mission_contract_types_v0_20 import (
    build_authority_scope,
    build_evidence_policy,
    build_goal_policy,
    build_mission_contract,
    build_override_policy,
    build_renewal_policy,
    build_resource_envelope,
    sha,
)
from runtime.kuuos_mission_state_v0_20 import build_initial_mission_state
from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    apply_observation,
    build_initial_belief_state,
    build_observation,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_plan_invalidation_receipt,
    build_semantic_plan,
    build_verification_receipt,
    plan_digest,
    validate_semantic_plan_static,
    verification_to_mission_evidence,
)
from runtime.kuuos_semantic_planner_verifier_store_v0_22 import (
    initialize_planner_verifier_store,
    persist_invalidation,
    persist_plan,
    persist_verification,
    recover_planner_verifier_store,
)


def _fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = build_mission_contract(
        mission_id="mission-semantic-planner-verifier-v022",
        lineage_id="lineage-semantic-planner-verifier-v022",
        revision=0,
        parent_contract_digest="",
        issuer_id="owner-1",
        issuer_role="owner",
        governance_root_digest="governance-root-v022",
        purpose="Produce bounded semantic plans and independently verify outcomes",
        success_criteria=[
            "plan_outputs_expected_observations",
            "independent_verification_confirms_goal",
        ],
        failure_criteria=[
            "plan_self_authorizes_effect",
            "execution_success_collapses_into_mission_success",
        ],
        invariants=[
            "plan_is_proposal_only",
            "planner_verifier_separation",
            "independent_observation_required",
        ],
        prohibited_outcomes=["unlicensed_effect", "memory_overwrite"],
        resource_envelope=build_resource_envelope(
            max_total_cost=100.0,
            max_cycle_cost=12.0,
            max_cycles_before_renewal=10,
            max_active_goals=3,
            max_goal_count=6,
            reserve_floor=5.0,
        ),
        authority_scope=build_authority_scope(
            domain_scope=["software_runtime"],
            requested_capabilities=["observe.read", "plan.propose"],
        ),
        renewal_policy=build_renewal_policy(
            max_renewals=2,
            renewal_window_ms=1000,
            authorized_roles=["owner"],
        ),
        override_policy=build_override_policy(
            {"owner": ["pause", "resume", "terminate", "handover", "request_renewal", "renew"]}
        ),
        evidence_policy=build_evidence_policy(
            completion_roles=["verifier"],
            failure_roles=["verifier"],
            invariant_roles=["verifier"],
            minimum_confidence=0.8,
        ),
        goal_policy=build_goal_policy(plurality_floor=0.05),
        created_at_ms=0,
        valid_from_ms=0,
        expires_at_ms=100000,
    )
    mission_state = build_initial_mission_state(contract, now_ms=1)
    goal = build_goal_proposal(
        contract=contract,
        goal_id="goal-release-confidence",
        objective="Prepare and independently verify a bounded release proposal",
        priority_weight=0.9,
        horizon="short",
        expected_outcomes=["release_proposal_verified"],
        required_capabilities=["observe.read", "plan.propose"],
        dependencies=[],
        requested_cost=8.0,
        requested_cycles=2,
        created_at_ms=2,
    )
    portfolio = build_goal_portfolio(contract=contract, goals=[goal], now_ms=3)
    return contract, mission_state, goal, portfolio


def _observation(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    observation_id: str,
    claim_id: str,
    proposition: str,
    relation: str,
    source_id: str,
    observed_at_ms: int,
) -> dict[str, Any]:
    return build_observation(
        contract=contract,
        mission_state=mission_state,
        observation_id=observation_id,
        chart_id="github-main",
        claim_id=claim_id,
        proposition=proposition,
        relation=relation,
        source_id=source_id,
        source_kind="system",
        raw_artifact_digest=sha({"observation": observation_id}),
        provenance_digests=[sha({"source": source_id}), sha({"collector": "v022"})],
        observed_at_ms=observed_at_ms,
        valid_until_ms=10000,
        confidence=0.95,
    )


def _ready_belief_state(contract: dict[str, Any], mission_state: dict[str, Any]) -> dict[str, Any]:
    state = build_initial_belief_state(
        contract=contract,
        mission_state=mission_state,
        chart_id="github-main",
        now_ms=4,
    )
    for observation in (
        _observation(
            contract,
            mission_state,
            "obs-repository-clean",
            "repository-clean",
            "The repository working basis is clean",
            "supports",
            "observer-baseline",
            5,
        ),
        _observation(
            contract,
            mission_state,
            "obs-ci-green",
            "ci-baseline-green",
            "The baseline CI is green",
            "supports",
            "observer-ci",
            6,
        ),
    ):
        state = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            observation=observation,
        )["result_state"]
    return state


def _plan_parts() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return (
        [
            {
                "subgoal_id": "inspect-basis",
                "objective": "Inspect the bounded repository and CI basis",
                "dependencies": [],
                "required_claim_ids": ["repository-clean", "ci-baseline-green"],
            },
            {
                "subgoal_id": "propose-release",
                "objective": "Produce a proposal with expected observations",
                "dependencies": ["inspect-basis"],
                "required_claim_ids": ["repository-clean"],
            },
        ],
        [
            {
                "step_id": "step-inspect",
                "objective": "Read the bounded basis",
                "dependencies": [],
                "required_capabilities": ["observe.read"],
                "cost_bound": 2.0,
                "expected_observations": ["bounded_basis_report"],
                "success_claim_ids": ["basis-inspected"],
                "compensation_refs": [],
            },
            {
                "step_id": "step-propose",
                "objective": "Produce a proposal without effect authority",
                "dependencies": ["step-inspect"],
                "required_capabilities": ["plan.propose"],
                "cost_bound": 4.0,
                "expected_observations": ["proposal_digest", "verification_request"],
                "success_claim_ids": ["release-proposal-produced"],
                "compensation_refs": [],
            },
        ],
        [
            {
                "alternative_id": "hold-and-observe",
                "trigger": "basis becomes unknown, contradicted, or stale",
                "summary": "Hold and request fresh evidence",
            }
        ],
    )


def _build_plan(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    belief_state: dict[str, Any],
    goal: dict[str, Any],
    portfolio: dict[str, Any],
    **extra: Any,
) -> dict[str, Any]:
    subgoals, steps, alternatives = _plan_parts()
    return build_semantic_plan(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief_state,
        goal=goal,
        goal_portfolio=portfolio,
        planner_id="planner-v022",
        plan_id=str(extra.pop("plan_id", "plan-release-v1")),
        required_claim_ids=extra.pop(
            "required_claim_ids", ["repository-clean", "ci-baseline-green"]
        ),
        available_capabilities=["observe.read", "plan.propose"],
        subgoals=extra.pop("subgoals", subgoals),
        steps=steps,
        alternatives=alternatives,
        created_at_ms=int(extra.pop("created_at_ms", 10)),
        valid_until_ms=int(extra.pop("valid_until_ms", 1000)),
        **extra,
    )


def _assessment(
    criterion: str,
    status: str,
    observation: dict[str, Any] | None,
    confidence: float,
) -> dict[str, Any]:
    return {
        "criterion": criterion,
        "status": status,
        "confidence": confidence,
        "evidence_observation_digests": (
            [observation["observation_digest"]] if observation else []
        ),
        "notes": status,
    }


def run_semantic_planner_verifier_scenarios() -> dict[str, Any]:
    contract, mission_state, goal, portfolio = _fixture()
    belief = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, belief, goal, portfolio)
    assert plan["status"] == "ready"

    with TemporaryDirectory(prefix="kuuos-planner-verifier-v022-") as directory:
        initialize_planner_verifier_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            chart_id="github-main",
            now_ms=9,
        )
        first = persist_plan(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
        )
        replay = persist_plan(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
        )
        assert first["status"] == "APPLIED" and replay["status"] == "REPLAYED"

        execution_only = build_verification_receipt(
            contract=contract,
            mission_state=mission_state,
            source_belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verifier_id="verifier-execution-only",
            independent_observations=[],
            criterion_assessments=[
                _assessment(item, "unknown", None, 0.0)
                for item in contract["success_criteria"]
            ],
            execution_receipt_digests=[sha({"execution": "completed"})],
            observed_at_ms=20,
        )
        assert execution_only["status"] == "inconclusive"

        observations = [
            _observation(
                contract,
                mission_state,
                "verify-plan-output",
                "plan-output-confirmed",
                "Expected observations are present",
                "supports",
                "verifier-observer-1",
                21,
            ),
            _observation(
                contract,
                mission_state,
                "verify-goal",
                "goal-confirmed",
                "The bounded goal is independently confirmed",
                "supports",
                "verifier-observer-2",
                22,
            ),
        ]
        success = build_verification_receipt(
            contract=contract,
            mission_state=mission_state,
            source_belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verifier_id="independent-verifier-v022",
            independent_observations=observations,
            criterion_assessments=[
                _assessment(contract["success_criteria"][0], "satisfied", observations[0], 0.95),
                _assessment(contract["success_criteria"][1], "satisfied", observations[1], 0.93),
            ],
            execution_receipt_digests=[sha({"execution": "completed"})],
            observed_at_ms=23,
        )
        assert success["status"] == "verified_success"
        persist_verification(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=success,
        )
        assert verification_to_mission_evidence(
            contract=contract, mission_state=mission_state, receipt=success
        )["success_verified"] is True

        contradiction_observation = _observation(
            contract,
            mission_state,
            "verify-contradiction",
            "goal-contradiction",
            "Independent checking found a contradiction",
            "supports",
            "verifier-observer-3",
            24,
        )
        contradicted = build_verification_receipt(
            contract=contract,
            mission_state=mission_state,
            source_belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verifier_id="independent-verifier-v022b",
            independent_observations=[contradiction_observation],
            criterion_assessments=[
                _assessment(contract["success_criteria"][0], "satisfied", contradiction_observation, 0.9),
                _assessment(contract["success_criteria"][1], "contradicted", contradiction_observation, 0.91),
            ],
            execution_receipt_digests=[sha({"execution": "completed"})],
            observed_at_ms=25,
        )
        persist_verification(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=contradicted,
        )

        changed = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            observation=_observation(
                contract,
                mission_state,
                "obs-ci-red",
                "ci-baseline-green",
                "The baseline CI is green",
                "opposes",
                "observer-ci-independent",
                26,
            ),
        )["result_state"]
        invalidation = build_plan_invalidation_receipt(
            contract=contract,
            mission_state=mission_state,
            source_belief_state=belief,
            current_belief_state=changed,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            checked_at_ms=27,
        )
        persist_invalidation(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=invalidation,
        )
        subgoals, _, _ = _plan_parts()
        subgoals[0]["required_claim_ids"] = ["repository-clean"]
        replanned = _build_plan(
            contract,
            mission_state,
            changed,
            goal,
            portfolio,
            plan_id="plan-release-v2",
            required_claim_ids=["repository-clean"],
            subgoals=subgoals,
            created_at_ms=28,
            valid_until_ms=1100,
            previous_plan=plan,
            failure_verification=contradicted,
            replan_reason="Remove the contradicted CI assumption and request fresh evidence",
        )
        persist_plan(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            belief_state=changed,
            goal=goal,
            goal_portfolio=portfolio,
            plan=replanned,
        )

        recovered = recover_planner_verifier_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
        )
        assert len((Path(directory) / "planner-verifier-ledger.jsonl").read_text(encoding="utf-8").splitlines()) == 5
        tampered = deepcopy(plan)
        tampered["effect_authority_granted"] = True
        tampered["semantic_plan_digest"] = plan_digest(tampered)
        assert "plan_effect_authority_forbidden" in validate_semantic_plan_static(tampered)

        return {
            "status": "KUUOS_SEMANTIC_PLANNER_VERIFIER_V0_22_OK",
            "event_count": recovered["revision"],
            "verified_success": success["status"] == "verified_success",
            "execution_only_inconclusive": execution_only["status"] == "inconclusive",
            "contradiction_detected": contradicted["status"] == "contradicted",
            "plan_invalidated": invalidation["status"] == "invalidated",
            "replan_ready": replanned["status"] == "ready",
            "effect_authority_granted": False,
        }


__all__ = [
    "_build_plan",
    "_fixture",
    "_observation",
    "_plan_parts",
    "_ready_belief_state",
    "run_semantic_planner_verifier_scenarios",
]

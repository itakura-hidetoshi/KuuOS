from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_cognitive_memory_credit_kernel_v0_23 import (
    build_cognitive_memory_consolidation,
    consolidation_digest,
    validate_cognitive_memory_consolidation_static,
)
from runtime.kuuos_cognitive_memory_credit_store_v0_23 import (
    initialize_cognitive_memory_store,
    persist_cognitive_memory_consolidation,
    recover_cognitive_memory_store,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_verification_receipt,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _observation,
    _ready_belief_state,
)


def _qi_state(cycle_id: str, *, observation_debt: float = 0.1) -> dict[str, Any]:
    return {
        "cycle_id": cycle_id,
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "hysteresis": 0.3,
        "memory_horizon": 0.8,
        "observation_debt": observation_debt,
        "transition_readiness": 0.85,
        "recovery": 0.7,
        "coherence": 0.8,
        "process_history": [
            {
                "transition_visible": True,
                "memory_link_visible": True,
                "nonmarkov_link_visible": False,
                "process_observation": "plan proposed",
            },
            {
                "transition_visible": True,
                "memory_link_visible": True,
                "nonmarkov_link_visible": True,
                "process_observation": "effect observed",
            },
            {
                "transition_visible": True,
                "memory_link_visible": True,
                "nonmarkov_link_visible": True,
                "process_observation": "outcome verified",
            },
        ],
    }


def _observe_envelope(
    *,
    plan: dict[str, Any],
    observation_digest: str,
    suffix: str,
) -> dict[str, Any]:
    return {
        "version": "observe_os_replan_lineage_observation_envelope_v0_2",
        "mission_id": plan["mission_id"],
        "chart_id": plan["chart_id"],
        "source_plan_digest": plan["semantic_plan_digest"],
        "observation_digest": observation_digest,
        "observe_completion_receipt_digest": f"observe-completion-{suffix}",
        "observation_recorded": True,
        "observation_not_verification": True,
        "verification_required": True,
        "grants_truth_authority": False,
        "grants_verification_authority": False,
        "grants_execution_authority": False,
        "grants_memory_overwrite_authority": False,
        "memory_overwrite_performed": False,
    }


def _verify_envelope(
    *,
    observe_envelope: dict[str, Any],
    verification: dict[str, Any],
    verdict: str,
    suffix: str,
) -> dict[str, Any]:
    return {
        "version": "verify_os_replan_lineage_verification_envelope_v0_2",
        "source_observation_digest": observe_envelope["observation_digest"],
        "source_verification_receipt_digest": verification[
            "verification_receipt_digest"
        ],
        "verify_completion_receipt_digest": f"verify-completion-{suffix}",
        "verdict": verdict,
        "learning_required": True,
        "learning_must_be_future_only": True,
        "automatic_learning": False,
        "grants_truth_authority": False,
        "grants_causal_authority": False,
        "grants_execution_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_automatic_learning_authority": False,
    }


def _verification(
    *,
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    belief: dict[str, Any],
    goal: dict[str, Any],
    portfolio: dict[str, Any],
    plan: dict[str, Any],
    status: str,
    observed_at_ms: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if status == "verified_success":
        observations = [
            _observation(
                contract,
                mission_state,
                f"v023-success-{observed_at_ms}-a",
                "v023-plan-output",
                "Expected plan observations were recorded",
                "supports",
                "v023-observer-a",
                observed_at_ms,
            ),
            _observation(
                contract,
                mission_state,
                f"v023-success-{observed_at_ms}-b",
                "v023-goal-confirmed",
                "Independent evidence confirms the bounded goal",
                "supports",
                "v023-observer-b",
                observed_at_ms + 1,
            ),
        ]
        assessments = [
            {
                "criterion": contract["success_criteria"][0],
                "status": "satisfied",
                "confidence": 0.95,
                "evidence_observation_digests": [
                    observations[0]["observation_digest"]
                ],
                "notes": "independently observed",
            },
            {
                "criterion": contract["success_criteria"][1],
                "status": "satisfied",
                "confidence": 0.93,
                "evidence_observation_digests": [
                    observations[1]["observation_digest"]
                ],
                "notes": "independently verified",
            },
        ]
    else:
        observations = [
            _observation(
                contract,
                mission_state,
                f"v023-contradiction-{observed_at_ms}",
                "v023-goal-contradicted",
                "Independent evidence contradicts the bounded goal",
                "supports",
                "v023-observer-c",
                observed_at_ms,
            )
        ]
        assessments = [
            {
                "criterion": contract["success_criteria"][0],
                "status": "satisfied",
                "confidence": 0.9,
                "evidence_observation_digests": [
                    observations[0]["observation_digest"]
                ],
                "notes": "observation contract present",
            },
            {
                "criterion": contract["success_criteria"][1],
                "status": "contradicted",
                "confidence": 0.92,
                "evidence_observation_digests": [
                    observations[0]["observation_digest"]
                ],
                "notes": "counterevidence preserved",
            },
        ]
    receipt = build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verifier_id=f"v023-verifier-{observed_at_ms}",
        independent_observations=observations,
        criterion_assessments=assessments,
        execution_receipt_digests=[],
        observed_at_ms=observed_at_ms + 2,
    )
    return receipt, observations


def run_cognitive_memory_credit_scenarios() -> dict[str, Any]:
    contract, mission_state, goal, portfolio = _fixture()
    belief = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, belief, goal, portfolio)
    success, success_observations = _verification(
        contract=contract,
        mission_state=mission_state,
        belief=belief,
        goal=goal,
        portfolio=portfolio,
        plan=plan,
        status="verified_success",
        observed_at_ms=40,
    )
    observe_success = _observe_envelope(
        plan=plan,
        observation_digest=success_observations[-1]["observation_digest"],
        suffix="success",
    )
    verify_success = _verify_envelope(
        observe_envelope=observe_success,
        verification=success,
        verdict="PASSED",
        suffix="success",
    )
    first = build_cognitive_memory_consolidation(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        semantic_plan=plan,
        verification_receipt=success,
        observe_envelope=observe_success,
        verify_envelope=verify_success,
        qi_state=_qi_state("cycle-v023-success"),
        memory_entries=[],
        consolidator_id="memoryos-consolidator-v023",
        episode_id="episode-v023-success",
        consolidated_at_ms=50,
        belief_coherence_receipt_digests=["belief-gerbe-coherence-success"],
    )
    assert first["status"] == "consolidated"
    assert first["memory_genesis"] is True
    assert first["plan_strategy_candidate"]["route"] == "strengthen"
    assert all(
        -1.0 <= item["signed_credit"] <= 1.0
        for item in first["credit_assignments"]
    )
    assert all(item["causal_claim"] is False for item in first["credit_assignments"])

    with TemporaryDirectory(prefix="kuuos-cognitive-memory-v023-") as directory:
        initialize_cognitive_memory_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            chart_id=belief["chart_id"],
            now_ms=49,
        )
        applied_first = persist_cognitive_memory_consolidation(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=first,
        )
        assert applied_first["status"] == "APPLIED"
        replay_first = persist_cognitive_memory_consolidation(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=first,
        )
        assert replay_first["status"] == "REPLAYED"
        recovered_first = recover_cognitive_memory_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
        )
        memory_entries = recovered_first["memory_entries"]
        assert len(memory_entries) == 1

        contradicted, contradiction_observations = _verification(
            contract=contract,
            mission_state=mission_state,
            belief=belief,
            goal=goal,
            portfolio=portfolio,
            plan=plan,
            status="contradicted",
            observed_at_ms=60,
        )
        observe_failure = _observe_envelope(
            plan=plan,
            observation_digest=contradiction_observations[0]["observation_digest"],
            suffix="failure",
        )
        verify_failure = _verify_envelope(
            observe_envelope=observe_failure,
            verification=contradicted,
            verdict="FAILED",
            suffix="failure",
        )
        second = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=contradicted,
            observe_envelope=observe_failure,
            verify_envelope=verify_failure,
            qi_state=_qi_state("cycle-v023-failure", observation_debt=0.4),
            memory_entries=memory_entries,
            consolidator_id="memoryos-consolidator-v023",
            episode_id="episode-v023-failure",
            consolidated_at_ms=70,
            belief_coherence_receipt_digests=["belief-gerbe-coherence-failure"],
        )
        assert second["status"] == "contradiction_preserved"
        assert second["memory_genesis"] is False
        assert second["memoryos_retrieval_replay"]["replay_status"] == (
            "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY"
        )
        assert second["belief_release_candidate"]["route"] == "repair"
        assert second["plan_strategy_candidate"]["route"] == "repair"
        assert second["counterevidence_digests"]
        assert any(item["signed_credit"] < 0 for item in second["credit_assignments"])
        persist_cognitive_memory_consolidation(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            receipt=second,
        )
        recovered = recover_cognitive_memory_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
        )
        assert recovered["revision"] == 2
        assert len(recovered["memory_entries"]) == 2
        assert len(
            (Path(directory) / "cognitive-memory-ledger.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ) == 2

        tampered = deepcopy(second)
        tampered["automatic_learning"] = True
        tampered["cognitive_memory_consolidation_digest"] = consolidation_digest(
            tampered
        )
        assert "automatic_learning_forbidden" in (
            validate_cognitive_memory_consolidation_static(tampered)
        )

        return {
            "status": "KUUOS_COGNITIVE_MEMORY_CREDIT_V0_23_OK",
            "store_revision": recovered["revision"],
            "memory_entry_count": len(recovered["memory_entries"]),
            "success_consolidated": first["status"] == "consolidated",
            "contradiction_preserved": second["status"]
            == "contradiction_preserved",
            "memory_replay_ready": second["memoryos_retrieval_replay"][
                "replay_status"
            ]
            == "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY",
            "beliefos_candidate_only": second["belief_release_candidate"][
                "belief_released"
            ]
            is False,
            "planos_future_only": second["plan_strategy_candidate"][
                "future_only"
            ]
            is True,
            "credit_is_noncausal": all(
                item["causal_claim"] is False
                for item in second["credit_assignments"]
            ),
            "memory_overwrite_performed": False,
            "automatic_learning": False,
            "execution_performed": False,
        }


__all__ = [
    "_observe_envelope",
    "_qi_state",
    "_verification",
    "_verify_envelope",
    "run_cognitive_memory_credit_scenarios",
]

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_kernel_v0_1 import (
    build_abstraction_packet,
    build_initial_learn_state,
    build_learn_event,
    build_learning_challenge_packet,
    build_learning_delta,
    build_middle_way_report,
)
from runtime.kuuos_learn_os_store_v0_1 import LearnStore
from runtime.kuuos_learn_os_types_v0_1 import copy_non_authority as copy_learn_non_authority
from runtime.kuuos_observe_os_kernel_v0_1 import (
    build_comparison_receipt,
    build_initial_observe_state,
    build_observe_event,
)
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore
from runtime.kuuos_observe_os_types_v0_1 import copy_non_authority as copy_observe_non_authority
from runtime.kuuos_verify_os_kernel_v0_1 import (
    build_adjudication_receipt,
    build_challenge_packet,
    build_criterion_packet,
    build_initial_verify_state,
    build_verify_event,
)
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore
from runtime.kuuos_verify_os_types_v0_1 import copy_non_authority as copy_verify_non_authority


def _apply(store: Any, event: Mapping[str, Any]) -> dict[str, Any]:
    result = store.apply(event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _observe_event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    return build_observe_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "now_ms": now_ms}),
        payload=payload,
        now_ms=now_ms,
    )


def committed_observe_after_effect(
    root: Path, *, observe_id: str, act_state: Mapping[str, Any]
) -> dict[str, Any]:
    store = ObserveStore(root)
    state = store.initialize(
        build_initial_observe_state(
            observe_id=observe_id,
            act_state=act_state,
            now_ms=510_000,
        )
    )
    scope = {
        "observation_target_digest": act_state["expected_observation_digest"],
        "observation_protocol_digest": sha("plan-v04-observe-protocol"),
        "window_start_ms": 510_050,
        "window_end_ms": 510_900,
        "channels": ["system-output", "independent-check"],
        "minimum_evidence_items": 2,
        "independence_required": True,
        "observer_context_digest": sha("plan-v04-observer-context"),
        "baseline_digest": sha("plan-v04-baseline"),
    }
    state = _apply(store, _observe_event(state, "scope", {"observation_scope": scope}, 510_001))
    evidence = [
        {
            "evidence_id": "plan-v04-evidence-system",
            "channel_id": "system-output",
            "source_kind": "system",
            "collector_id": "collector-system",
            "independent_source_id": "source-system",
            "collected_at_ms": 510_100,
            "raw_artifact_digest": sha("plan-v04-raw-system"),
            "value_digest": sha("plan-v04-value-system"),
            "uncertainty_digest": sha("plan-v04-uncertainty-system"),
            "calibration_digest": sha("plan-v04-calibration-system"),
            "context_digest": sha("plan-v04-context-system"),
            "tamper_evidence_digest": sha("plan-v04-tamper-system"),
            "provenance_hop_digests": [sha("plan-v04-source"), sha("plan-v04-collector")],
        },
        {
            "evidence_id": "plan-v04-evidence-human",
            "channel_id": "independent-check",
            "source_kind": "human",
            "collector_id": "collector-human",
            "independent_source_id": "source-human",
            "collected_at_ms": 510_200,
            "raw_artifact_digest": sha("plan-v04-raw-human"),
            "value_digest": sha("plan-v04-value-human"),
            "uncertainty_digest": sha("plan-v04-uncertainty-human"),
            "calibration_digest": sha("plan-v04-calibration-human"),
            "context_digest": sha("plan-v04-context-human"),
            "tamper_evidence_digest": sha("plan-v04-tamper-human"),
            "provenance_hop_digests": [sha("plan-v04-witness"), sha("plan-v04-review")],
        },
    ]
    state = _apply(store, _observe_event(state, "collect", {"evidence_items": evidence}, 510_210))
    state = _apply(
        store,
        _observe_event(
            state,
            "trace",
            {
                "provenance_receipt_digest": sha("plan-v04-provenance-receipt"),
                "evidence_chain_complete": True,
                "source_identity_preserved": True,
                "raw_artifacts_immutable": True,
                "no_unbound_evidence": True,
            },
            510_220,
        ),
    )
    state = _apply(
        store,
        _observe_event(
            state,
            "assess",
            {
                "quality_report": {
                    "coverage": 0.95,
                    "freshness": 0.9,
                    "provenance": 0.95,
                    "calibration": 0.9,
                    "completeness": 0.95,
                    "conflict": 0.1,
                    "assessment_method_digest": sha("plan-v04-quality-method"),
                }
            },
            510_230,
        ),
    )
    comparison = build_comparison_receipt(
        state=state,
        comparison_id=observe_id + "-comparison",
        verdict="MATCHED",
        comparison_method_digest=sha("plan-v04-comparison-method"),
        rationale_digest=sha("plan-v04-comparison-rationale"),
        compared_at_ms=510_500,
    )
    state = _apply(
        store,
        _observe_event(state, "compare", {"comparison_receipt": comparison}, 510_500),
    )
    return _apply(
        store,
        _observe_event(
            state,
            "commit",
            {
                "observation_not_verification": True,
                "verification_debt_preserved": True,
                "source_effect_identity_preserved": True,
                "memory_overwrite": False,
                "automatic_truth_promotion": False,
                "automatic_belief_update": False,
                "automatic_plan_completion": False,
                "automatic_causal_attribution": False,
                "non_authority": copy_observe_non_authority(),
            },
            510_510,
        ),
    )


def _verify_event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    return build_verify_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "now_ms": now_ms}),
        payload=payload,
        now_ms=now_ms,
    )


def committed_verify_after_observe(
    root: Path, *, verify_id: str, observe_state: Mapping[str, Any]
) -> dict[str, Any]:
    store = VerifyStore(root)
    state = store.initialize(
        build_initial_verify_state(
            verify_id=verify_id,
            observe_state=observe_state,
            now_ms=520_000,
        )
    )
    criterion = build_criterion_packet(
        state=state,
        criterion_type="contract",
        evaluation_method_digest=sha("plan-v04-verify-method"),
        success_condition_digest=sha("plan-v04-verify-success"),
        failure_condition_digest=sha("plan-v04-verify-failure"),
        falsification_condition_digest=sha("plan-v04-verify-falsifier"),
        evidence_requirements_digest=sha("plan-v04-verify-evidence"),
        minimum_independent_assessors=2,
    )
    state = _apply(store, _verify_event(state, "criterion", {"criterion_packet": criterion}, 520_001))
    challenge = build_challenge_packet(
        state=state,
        counterevidence_digests=[],
        falsification_attempt_digests=[sha("plan-v04-falsification-attempt")],
        independent_assessor_ids=["plan-v04-assessor-a", "plan-v04-assessor-b"],
        assessor_receipt_digests=[sha("plan-v04-assessor-a"), sha("plan-v04-assessor-b")],
        conflict_disclosure_digest=sha("plan-v04-conflict-disclosure"),
        falsifier_triggered=False,
    )
    state = _apply(store, _verify_event(state, "challenge", {"challenge_packet": challenge}, 520_002))
    state = _apply(
        store,
        _verify_event(
            state,
            "corroborate",
            {
                "corroboration_report": {
                    "evidence_sufficiency": 0.95,
                    "assessor_independence": 0.95,
                    "provenance_integrity": 0.95,
                    "method_reproducibility": 0.9,
                    "criterion_coverage": 0.95,
                    "unresolved_conflict": False,
                    "corroboration_method_digest": sha("plan-v04-corroboration-method"),
                }
            },
            520_003,
        ),
    )
    adjudication = build_adjudication_receipt(
        state=state,
        adjudication_id=verify_id + "-adjudication",
        verdict="PASSED",
        criterion_satisfied=True,
        adjudication_method_digest=sha("plan-v04-adjudication-method"),
        rationale_digest=sha("plan-v04-adjudication-rationale"),
        adjudicated_at_ms=520_010,
    )
    state = _apply(store, _verify_event(state, "adjudicate", {"adjudication_receipt": adjudication}, 520_010))
    return _apply(
        store,
        _verify_event(
            state,
            "commit",
            {
                "verification_not_truth": True,
                "causal_attribution_not_granted": True,
                "counterevidence_preserved": True,
                "learning_required": True,
                "memory_overwrite": False,
                "automatic_truth_promotion": False,
                "automatic_belief_update": False,
                "automatic_plan_completion": False,
                "automatic_rollback": False,
                "automatic_causal_attribution": False,
                "non_authority": copy_verify_non_authority(),
            },
            520_020,
        ),
    )


def _learn_event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    return build_learn_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "now_ms": now_ms}),
        payload=payload,
        now_ms=now_ms,
    )


def committed_learn_after_verify(
    root: Path, *, learn_id: str, verify_state: Mapping[str, Any]
) -> dict[str, Any]:
    store = LearnStore(root)
    state = store.initialize(
        build_initial_learn_state(
            learn_id=learn_id,
            verify_state=verify_state,
            now_ms=530_000,
        )
    )
    abstraction = build_abstraction_packet(
        state=state,
        supported_pattern_digests=[sha("plan-v04-supported-pattern")],
        failed_pattern_digests=[],
        unresolved_pattern_digests=[],
        counterevidence_digests=list(state["source_counterevidence_digests"]),
        uncertainty_digest=sha("plan-v04-learning-uncertainty"),
        residual_digest=sha("plan-v04-learning-residual"),
        scope_digest=sha("plan-v04-learning-scope"),
        qi_process_history_digest=sha("plan-v04-learning-qi-history"),
        abstraction_method_digest=sha("plan-v04-learning-abstraction"),
    )
    state = _apply(store, _learn_event(state, "abstract", {"abstraction_packet": abstraction}, 530_001))
    challenge = build_learning_challenge_packet(
        state=state,
        alternative_explanation_digests=[sha("plan-v04-alternative")],
        anti_overgeneralization_test_digests=[sha("plan-v04-anti-overgeneralization")],
        distribution_shift_risk_digest=sha("plan-v04-distribution-shift"),
        observer_bias_risk_digest=sha("plan-v04-observer-bias"),
        negative_transfer_risk_digest=sha("plan-v04-negative-transfer"),
    )
    state = _apply(store, _learn_event(state, "challenge", {"learning_challenge_packet": challenge}, 530_002))
    delta = build_learning_delta(
        state=state,
        learning_delta_id=learn_id + "-delta",
        learning_kind="reinforcement",
        target_scope="belief_candidate",
        before_digest=sha("plan-v04-before"),
        after_candidate_digest=sha("plan-v04-after"),
        change_rationale_digest=sha("plan-v04-rationale"),
        applicability_condition_digest=sha("plan-v04-applicability"),
        reversal_condition_digest=sha("plan-v04-reversal"),
        expiration_condition_digest=sha("plan-v04-expiration"),
    )
    state = _apply(store, _learn_event(state, "delta", {"learning_delta": delta}, 530_003))
    report = build_middle_way_report(
        state=state,
        reification_risk=0.2,
        nihilistic_erasure_risk=0.2,
        overgeneralization_risk=0.2,
        negative_transfer_risk=0.2,
        premature_activation_risk=0.2,
        scope_drift_risk=0.2,
        gate_method_digest=sha("plan-v04-middle-way"),
    )
    state = _apply(store, _learn_event(state, "middle_way_gate", {"middle_way_report": report}, 530_004))
    return _apply(
        store,
        _learn_event(
            state,
            "commit",
            {
                "future_only": True,
                "memory_overwrite": False,
                "active_now": False,
                "activation_requires_replan": True,
                "current_cycle_unchanged": True,
                "past_records_unchanged": True,
                "counterevidence_preserved": True,
                "verification_not_truth": True,
                "qi_context_only": True,
                "automatic_truth_promotion": False,
                "automatic_belief_update": False,
                "automatic_plan_update": False,
                "automatic_criterion_update": False,
                "automatic_policy_activation": False,
                "automatic_rollback": False,
                "automatic_self_modification": False,
                "non_authority": copy_learn_non_authority(),
            },
            530_005,
        ),
    )

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
from runtime.kuuos_learn_os_types_v0_1 import copy_non_authority as learn_non_authority
from runtime.kuuos_observe_os_kernel_v0_1 import (
    build_comparison_receipt,
    build_initial_observe_state,
    build_observe_event,
)
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore
from runtime.kuuos_observe_os_types_v0_1 import copy_non_authority as observe_non_authority
from runtime.kuuos_verify_os_kernel_v0_1 import (
    build_adjudication_receipt,
    build_challenge_packet,
    build_criterion_packet,
    build_initial_verify_state,
    build_verify_event,
)
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore
from runtime.kuuos_verify_os_types_v0_1 import copy_non_authority as verify_non_authority

OBSERVE_INITIAL_MS = 298_000
OBSERVE_WINDOW_START_MS = 299_000
OBSERVE_WINDOW_END_MS = 299_900
OBSERVE_EVENT_BASE_MS = 300_000
VERIFY_INITIAL_MS = 310_000
VERIFY_EVENT_BASE_MS = 320_000
LEARN_INITIAL_MS = 400_000
LEARN_EVENT_BASE_MS = 410_000


def _apply(store: Any, event: Mapping[str, Any]) -> dict[str, Any]:
    result = store.apply(event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _observe_event(
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_observe_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha(
            {
                "cycle": 2,
                "phase": phase,
                "payload": dict(payload),
                "tick": tick,
            }
        ),
        payload=payload,
        now_ms=OBSERVE_EVENT_BASE_MS + tick,
    )


def _evidence_items() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "successor-evidence-1",
            "channel_id": "system-output",
            "source_kind": "system",
            "collector_id": "successor-collector-system",
            "independent_source_id": "successor-source-system",
            "collected_at_ms": 299_100,
            "raw_artifact_digest": sha("successor-raw-system"),
            "value_digest": sha("successor-value-system"),
            "uncertainty_digest": sha("successor-uncertainty-system"),
            "calibration_digest": sha("successor-calibration-system"),
            "context_digest": sha("successor-context-system"),
            "tamper_evidence_digest": sha("successor-tamper-system"),
            "provenance_hop_digests": [
                sha("successor-system-source"),
                sha("successor-system-collector"),
            ],
        },
        {
            "evidence_id": "successor-evidence-2",
            "channel_id": "independent-check",
            "source_kind": "human",
            "collector_id": "successor-collector-human",
            "independent_source_id": "successor-source-human",
            "collected_at_ms": 299_200,
            "raw_artifact_digest": sha("successor-raw-human"),
            "value_digest": sha("successor-value-human"),
            "uncertainty_digest": sha("successor-uncertainty-human"),
            "calibration_digest": sha("successor-calibration-human"),
            "context_digest": sha("successor-context-human"),
            "tamper_evidence_digest": sha("successor-tamper-human"),
            "provenance_hop_digests": [
                sha("successor-human-witness"),
                sha("successor-human-review"),
            ],
        },
    ]


def _build_observe(root: Path, act: Mapping[str, Any]) -> dict[str, Any]:
    store = ObserveStore(root)
    state = store.initialize(
        build_initial_observe_state(
            observe_id="successor-licensed-cycle-observe-v20",
            act_state=act,
            now_ms=OBSERVE_INITIAL_MS,
        )
    )
    scope = {
        "observation_target_digest": act["expected_observation_digest"],
        "observation_protocol_digest": sha("successor-observe-protocol-v20"),
        "window_start_ms": OBSERVE_WINDOW_START_MS,
        "window_end_ms": OBSERVE_WINDOW_END_MS,
        "channels": ["system-output", "independent-check"],
        "minimum_evidence_items": 2,
        "independence_required": True,
        "observer_context_digest": sha("successor-observer-context-v20"),
        "baseline_digest": sha("successor-observer-baseline-v20"),
    }
    state = _apply(store, _observe_event(state, "scope", scope, 1))
    state = _apply(
        store,
        _observe_event(
            state,
            "collect",
            {"evidence_items": _evidence_items()},
            2,
        ),
    )
    state = _apply(
        store,
        _observe_event(
            state,
            "trace",
            {
                "provenance_receipt_digest": sha(
                    "successor-provenance-receipt-v20"
                ),
                "evidence_chain_complete": True,
                "source_identity_preserved": True,
                "raw_artifacts_immutable": True,
                "no_unbound_evidence": True,
            },
            3,
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
                    "freshness": 0.95,
                    "provenance": 0.95,
                    "calibration": 0.9,
                    "completeness": 0.95,
                    "conflict": 0.1,
                    "assessment_method_digest": sha(
                        "successor-quality-method-v20"
                    ),
                }
            },
            4,
        ),
    )
    comparison = build_comparison_receipt(
        state=state,
        comparison_id="successor-observation-comparison-v20",
        verdict="MATCHED",
        comparison_method_digest=sha("successor-comparison-method-v20"),
        rationale_digest=sha("successor-comparison-rationale-v20"),
        compared_at_ms=OBSERVE_EVENT_BASE_MS + 5,
    )
    state = _apply(
        store,
        _observe_event(
            state,
            "compare",
            {"comparison_receipt": comparison},
            5,
        ),
    )
    state = _apply(
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
                "non_authority": observe_non_authority(),
            },
            6,
        ),
    )
    return state


def _verify_event(
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_verify_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha(
            {
                "cycle": 2,
                "phase": phase,
                "payload": dict(payload),
                "tick": tick,
            }
        ),
        payload=payload,
        now_ms=VERIFY_EVENT_BASE_MS + tick,
    )


def _build_verify(root: Path, observe: Mapping[str, Any]) -> dict[str, Any]:
    store = VerifyStore(root)
    state = store.initialize(
        build_initial_verify_state(
            verify_id="successor-licensed-cycle-verify-v20",
            observe_state=observe,
            now_ms=VERIFY_INITIAL_MS,
        )
    )
    criterion = build_criterion_packet(
        state=state,
        criterion_type="contract",
        evaluation_method_digest=sha("successor-verify-method-v20"),
        success_condition_digest=sha("successor-verify-success-v20"),
        failure_condition_digest=sha("successor-verify-failure-v20"),
        falsification_condition_digest=sha("successor-verify-falsifier-v20"),
        evidence_requirements_digest=sha("successor-evidence-requirements-v20"),
        minimum_independent_assessors=2,
    )
    state = _apply(
        store,
        _verify_event(state, "criterion", {"criterion_packet": criterion}, 1),
    )
    challenge = build_challenge_packet(
        state=state,
        counterevidence_digests=[],
        falsification_attempt_digests=[
            sha("successor-falsification-attempt-v20")
        ],
        independent_assessor_ids=[
            "successor-assessor-a",
            "successor-assessor-b",
        ],
        assessor_receipt_digests=[
            sha("successor-assessor-a-receipt-v20"),
            sha("successor-assessor-b-receipt-v20"),
        ],
        conflict_disclosure_digest=sha("successor-conflict-disclosure-v20"),
        falsifier_triggered=False,
    )
    state = _apply(
        store,
        _verify_event(state, "challenge", {"challenge_packet": challenge}, 2),
    )
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
                    "corroboration_method_digest": sha(
                        "successor-corroboration-method-v20"
                    ),
                }
            },
            3,
        ),
    )
    adjudication = build_adjudication_receipt(
        state=state,
        adjudication_id="successor-adjudication-v20",
        verdict="PASSED",
        criterion_satisfied=True,
        adjudication_method_digest=sha("successor-adjudication-method-v20"),
        rationale_digest=sha("successor-adjudication-rationale-v20"),
        adjudicated_at_ms=VERIFY_EVENT_BASE_MS + 4,
    )
    state = _apply(
        store,
        _verify_event(
            state,
            "adjudicate",
            {"adjudication_receipt": adjudication},
            4,
        ),
    )
    state = _apply(
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
                "non_authority": verify_non_authority(),
            },
            5,
        ),
    )
    return state


def _learn_event(
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_learn_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha(
            {
                "cycle": 2,
                "phase": phase,
                "payload": dict(payload),
                "tick": tick,
            }
        ),
        payload=payload,
        now_ms=LEARN_EVENT_BASE_MS + tick,
    )


def _build_learn(root: Path, verify: Mapping[str, Any]) -> dict[str, Any]:
    store = LearnStore(root)
    state = store.initialize(
        build_initial_learn_state(
            learn_id="successor-licensed-cycle-learn-v20",
            verify_state=verify,
            now_ms=LEARN_INITIAL_MS,
        )
    )
    abstraction = build_abstraction_packet(
        state=state,
        supported_pattern_digests=[sha("successor-supported-pattern-v20")],
        failed_pattern_digests=[],
        unresolved_pattern_digests=[],
        counterevidence_digests=list(state["source_counterevidence_digests"]),
        uncertainty_digest=sha("successor-learning-uncertainty-v20"),
        residual_digest=sha("successor-learning-residual-v20"),
        scope_digest=sha("successor-learning-scope-v20"),
        qi_process_history_digest=sha("successor-qi-process-history-v20"),
        abstraction_method_digest=sha("successor-abstraction-method-v20"),
    )
    state = _apply(
        store,
        _learn_event(
            state,
            "abstract",
            {"abstraction_packet": abstraction},
            1,
        ),
    )
    challenge = build_learning_challenge_packet(
        state=state,
        alternative_explanation_digests=[
            sha("successor-alternative-explanation-v20")
        ],
        anti_overgeneralization_test_digests=[
            sha("successor-anti-overgeneralization-v20")
        ],
        distribution_shift_risk_digest=sha(
            "successor-distribution-shift-risk-v20"
        ),
        observer_bias_risk_digest=sha("successor-observer-bias-risk-v20"),
        negative_transfer_risk_digest=sha(
            "successor-negative-transfer-risk-v20"
        ),
    )
    state = _apply(
        store,
        _learn_event(
            state,
            "challenge",
            {"learning_challenge_packet": challenge},
            2,
        ),
    )
    before = sha("successor-before-state-v20")
    delta = build_learning_delta(
        state=state,
        learning_delta_id="successor-learning-delta-v20",
        learning_kind="reinforcement",
        target_scope="belief_candidate",
        before_digest=before,
        after_candidate_digest=sha("successor-after-candidate-v20"),
        change_rationale_digest=sha("successor-learning-rationale-v20"),
        applicability_condition_digest=sha(
            "successor-learning-applicability-v20"
        ),
        reversal_condition_digest=sha("successor-learning-reversal-v20"),
        expiration_condition_digest=sha("successor-learning-expiration-v20"),
    )
    state = _apply(
        store,
        _learn_event(state, "delta", {"learning_delta": delta}, 3),
    )
    report = build_middle_way_report(
        state=state,
        reification_risk=0.2,
        nihilistic_erasure_risk=0.2,
        overgeneralization_risk=0.2,
        negative_transfer_risk=0.2,
        premature_activation_risk=0.2,
        scope_drift_risk=0.2,
        gate_method_digest=sha("successor-middle-way-gate-v20"),
    )
    state = _apply(
        store,
        _learn_event(
            state,
            "middle_way_gate",
            {"middle_way_report": report},
            4,
        ),
    )
    state = _apply(
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
                "non_authority": learn_non_authority(),
            },
            5,
        ),
    )
    return state


def build_successor_native_evidence_downstream(
    root: Path,
    act: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    observe = _build_observe(root / "observe", act)
    verify = _build_verify(root / "verify", observe)
    learn = _build_learn(root / "learn", verify)
    return observe, verify, learn

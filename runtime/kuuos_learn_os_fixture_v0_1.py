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
from runtime.kuuos_verify_os_fixture_v0_1 import (
    prepared_corroborated_state,
    source_observe_state,
)
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify


def source_verify_state(root: Path, *, verdict: str) -> dict[str, Any]:
    normalized = verdict.upper()
    if normalized == "PASSED":
        observe = source_observe_state(root / "observe", verdict="MATCHED")
        store, state = prepared_corroborated_state(
            root=root / "verify",
            verify_id="learn-source-passed",
            observe_state=observe,
            admissible=True,
        )
        committed, _ = finish_verify(
            store=store,
            state=state,
            verdict="PASSED",
            criterion_satisfied=True,
            tick=10,
        )
        return committed
    if normalized == "FAILED":
        observe = source_observe_state(root / "observe", verdict="DIVERGENT")
        store, state = prepared_corroborated_state(
            root=root / "verify",
            verify_id="learn-source-failed",
            observe_state=observe,
            admissible=True,
        )
        committed, _ = finish_verify(
            store=store,
            state=state,
            verdict="FAILED",
            criterion_satisfied=False,
            tick=20,
        )
        return committed
    if normalized == "INDETERMINATE":
        observe = source_observe_state(root / "observe", verdict="CONFLICTED")
        store, state = prepared_corroborated_state(
            root=root / "verify",
            verify_id="learn-source-indeterminate",
            observe_state=observe,
            admissible=False,
        )
        committed, _ = finish_verify(
            store=store,
            state=state,
            verdict="INDETERMINATE",
            criterion_satisfied=False,
            tick=30,
        )
        return committed
    raise ValueError("source_verify_verdict_invalid")


def event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], tick: int
) -> dict[str, Any]:
    return build_learn_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=210_000 + tick,
    )


def apply(
    store: LearnStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def prepared_gated_state(
    *,
    root: Path,
    learn_id: str,
    verify_state: Mapping[str, Any],
    learning_kind: str,
    target_scope: str,
    admissible: bool = True,
) -> tuple[LearnStore, dict[str, Any]]:
    store = LearnStore(root)
    state = store.initialize(
        build_initial_learn_state(
            learn_id=learn_id,
            verify_state=verify_state,
            now_ms=200_000,
        )
    )
    route = state["source_verification_route"]
    unresolved = [sha("unresolved-pattern")] if state["source_unresolved_conflict"] else []
    abstraction = build_abstraction_packet(
        state=state,
        supported_pattern_digests=[sha("supported-pattern")]
        if route == "VERIFICATION_PASSED"
        else [],
        failed_pattern_digests=[sha("failed-pattern")]
        if route == "VERIFICATION_FAILED"
        else [],
        unresolved_pattern_digests=unresolved,
        counterevidence_digests=list(state["source_counterevidence_digests"]),
        uncertainty_digest=sha("learning-uncertainty"),
        residual_digest=sha("learning-residual"),
        scope_digest=sha("learning-source-scope"),
        qi_process_history_digest=sha("learning-qi-process-history"),
        abstraction_method_digest=sha("learning-abstraction-method"),
    )
    state = apply(
        store,
        state,
        "abstract",
        {"abstraction_packet": abstraction},
        1,
    )
    challenge = build_learning_challenge_packet(
        state=state,
        alternative_explanation_digests=[sha("alternative-explanation")],
        anti_overgeneralization_test_digests=[sha("anti-overgeneralization-test")],
        distribution_shift_risk_digest=sha("distribution-shift-risk"),
        observer_bias_risk_digest=sha("observer-bias-risk"),
        negative_transfer_risk_digest=sha("negative-transfer-risk"),
    )
    state = apply(
        store,
        state,
        "challenge",
        {"learning_challenge_packet": challenge},
        2,
    )
    before = sha("before-state")
    after = before if learning_kind == "hold" else sha(
        {"after-candidate": learning_kind, "target": target_scope}
    )
    delta = build_learning_delta(
        state=state,
        learning_delta_id=learn_id + "-delta",
        learning_kind=learning_kind,
        target_scope=target_scope,
        before_digest=before,
        after_candidate_digest=after,
        change_rationale_digest=sha("learning-change-rationale"),
        applicability_condition_digest=sha("learning-applicability-condition"),
        reversal_condition_digest=sha("learning-reversal-condition"),
        expiration_condition_digest=sha("learning-expiration-condition"),
    )
    state = apply(store, state, "delta", {"learning_delta": delta}, 3)
    risk = 0.2 if admissible else 0.9
    report = build_middle_way_report(
        state=state,
        reification_risk=risk,
        nihilistic_erasure_risk=risk,
        overgeneralization_risk=risk,
        negative_transfer_risk=risk,
        premature_activation_risk=risk,
        scope_drift_risk=risk,
        gate_method_digest=sha("learning-middle-way-gate"),
    )
    state = apply(
        store,
        state,
        "middle_way_gate",
        {"middle_way_report": report},
        4,
    )
    return store, state

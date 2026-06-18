from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_fixture_v0_1 import (
    prepared_assessed_state,
    source_act_state,
)
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.kuuos_verify_os_kernel_v0_1 import (
    build_challenge_packet,
    build_criterion_packet,
    build_initial_verify_state,
    build_verify_event,
)
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore


def source_observe_state(root: Path, *, verdict: str) -> dict[str, Any]:
    act_state = source_act_state(root)
    quality: dict[str, Any] | None = None
    conflict = False
    if verdict == "CONFLICTED":
        quality = {
            "coverage": 0.9,
            "freshness": 0.9,
            "provenance": 0.9,
            "calibration": 0.9,
            "completeness": 0.9,
            "conflict": 0.9,
            "assessment_method_digest": sha("verify-source-conflict-quality"),
        }
        conflict = True
    store, state = prepared_assessed_state(
        root=root / ("observe-" + verdict.lower()),
        observe_id="verify-source-" + verdict.lower(),
        act_state=act_state,
        quality=quality,
        conflict=conflict,
    )
    committed, _ = finish_observe(
        store=store,
        state=state,
        verdict=verdict,
        tick=10,
    )
    return committed


def event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], tick: int
) -> dict[str, Any]:
    return build_verify_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=120_000 + tick,
    )


def apply(
    store: VerifyStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def prepared_corroborated_state(
    *,
    root: Path,
    verify_id: str,
    observe_state: Mapping[str, Any],
    falsifier_triggered: bool = False,
    admissible: bool = True,
) -> tuple[VerifyStore, dict[str, Any]]:
    store = VerifyStore(root)
    state = store.initialize(
        build_initial_verify_state(
            verify_id=verify_id,
            observe_state=observe_state,
            now_ms=110_000,
        )
    )
    criterion = build_criterion_packet(
        state=state,
        criterion_type="contract",
        evaluation_method_digest=sha("verify-evaluation-method"),
        success_condition_digest=sha("verify-success-condition"),
        failure_condition_digest=sha("verify-failure-condition"),
        falsification_condition_digest=sha("verify-falsification-condition"),
        evidence_requirements_digest=sha("verify-evidence-requirements"),
        minimum_independent_assessors=2,
    )
    state = apply(
        store,
        state,
        "criterion",
        {"criterion_packet": criterion},
        1,
    )
    challenge = build_challenge_packet(
        state=state,
        counterevidence_digests=[sha("counterevidence")] if falsifier_triggered else [],
        falsification_attempt_digests=[sha("falsification-attempt")],
        independent_assessor_ids=["assessor-a", "assessor-b"],
        assessor_receipt_digests=[sha("assessor-a-receipt"), sha("assessor-b-receipt")],
        conflict_disclosure_digest=sha("conflict-disclosure"),
        falsifier_triggered=falsifier_triggered,
    )
    state = apply(
        store,
        state,
        "challenge",
        {"challenge_packet": challenge},
        2,
    )
    if admissible:
        report = {
            "evidence_sufficiency": 0.95,
            "assessor_independence": 0.95,
            "provenance_integrity": 0.95,
            "method_reproducibility": 0.9,
            "criterion_coverage": 0.95,
            "unresolved_conflict": False,
            "corroboration_method_digest": sha("corroboration-method"),
        }
    else:
        report = {
            "evidence_sufficiency": 0.4,
            "assessor_independence": 0.5,
            "provenance_integrity": 0.9,
            "method_reproducibility": 0.4,
            "criterion_coverage": 0.5,
            "unresolved_conflict": True,
            "corroboration_method_digest": sha("inconclusive-corroboration-method"),
        }
    state = apply(
        store,
        state,
        "corroborate",
        {"corroboration_report": report},
        3,
    )
    return store, state

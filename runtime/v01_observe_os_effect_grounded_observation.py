from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_fixture_v0_1 import (
    apply,
    event,
    prepared_assessed_state,
    source_act_state,
)
from runtime.kuuos_observe_os_kernel_v0_1 import (
    build_comparison_receipt,
    build_initial_observe_state,
    build_observe_phase_receipt,
)
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore, ObserveStoreError
from runtime.kuuos_observe_os_types_v0_1 import (
    copy_non_authority,
    observe_phase_receipt_digest,
)


def _finish(
    *,
    store: ObserveStore,
    state: dict,
    verdict: str,
    tick: int,
) -> tuple[dict, dict]:
    comparison = build_comparison_receipt(
        state=state,
        comparison_id=state["observe_id"] + "-comparison",
        verdict=verdict,
        comparison_method_digest=sha("comparison-method"),
        rationale_digest=sha("comparison-rationale-" + verdict),
        compared_at_ms=100_000 + tick,
    )
    state = apply(
        store,
        state,
        "compare",
        {"comparison_receipt": comparison},
        tick,
    )
    commit_event = event(
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
            "non_authority": copy_non_authority(),
        },
        tick + 1,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _target_substitution_rejected(root: Path, act_state: dict) -> None:
    store = ObserveStore(root)
    state = store.initialize(
        build_initial_observe_state(
            observe_id="observe-target-substitution",
            act_state=act_state,
            now_ms=98_000,
        )
    )
    result = store.apply(
        event(
            state,
            "scope",
            {
                "observation_target_digest": sha("substituted-target"),
                "observation_protocol_digest": sha("protocol"),
                "window_start_ms": 99_000,
                "window_end_ms": 99_900,
                "channels": ["system-output"],
                "minimum_evidence_items": 1,
                "independence_required": False,
                "observer_context_digest": sha("context"),
                "baseline_digest": sha("baseline"),
            },
            20,
        )
    )
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["observation_target_substitution_forbidden"]


def _low_quality_directional_rejected(root: Path, act_state: dict) -> None:
    low_quality = {
        "coverage": 0.3,
        "freshness": 0.4,
        "provenance": 0.4,
        "calibration": 0.4,
        "completeness": 0.4,
        "conflict": 0.2,
        "assessment_method_digest": sha("low-quality-method"),
    }
    store, state = prepared_assessed_state(
        root=root,
        observe_id="observe-low-quality",
        act_state=act_state,
        quality=low_quality,
    )
    comparison = build_comparison_receipt(
        state=state,
        comparison_id="low-quality-comparison",
        verdict="MATCHED",
        comparison_method_digest=sha("comparison-method"),
        rationale_digest=sha("low-quality-rationale"),
        compared_at_ms=100_030,
    )
    result = store.apply(
        event(
            state,
            "compare",
            {"comparison_receipt": comparison},
            30,
        )
    )
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["low_quality_directional_comparison_forbidden"]


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-observe-os-v01-") as temporary:
        root = Path(temporary)
        act_state = source_act_state(root)

        matched_store, matched_state = prepared_assessed_state(
            root=root / "matched",
            observe_id="observe-matched",
            act_state=act_state,
        )
        matched, commit_event = _finish(
            store=matched_store,
            state=matched_state,
            verdict="MATCHED",
            tick=5,
        )
        assert matched["route"] == "OBSERVATION_MATCHED"
        assert matched["observation_recorded"] is True
        assert matched["observation_debt_discharged"] is True
        assert matched["reobservation_required"] is False
        assert matched["verification_required"] is True
        assert matched["automatic_truth_promotion"] is False
        assert matched["automatic_belief_update"] is False
        assert matched["automatic_plan_completion"] is False
        assert matched["automatic_causal_attribution"] is False

        phase_receipt = build_observe_phase_receipt(
            state=matched,
            mission_cycle_state_digest=sha("mission-cycle-observe-state"),
            observe_phase_event_digest=sha("mission-cycle-observe-event"),
            now_ms=100_100,
        )
        assert phase_receipt["mission_cycle_phase"] == "observe"
        assert phase_receipt["observation_not_verification"] is True
        assert phase_receipt["verification_required"] is True
        assert phase_receipt["observe_phase_receipt_digest"] == observe_phase_receipt_digest(
            phase_receipt
        )

        before_replay = matched_store.ledger_commit_count()
        replay = matched_store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert matched_store.ledger_commit_count() == before_replay

        snapshot_path = root / "matched" / "observe-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            matched_store.recover(require_snapshot_match=True)
        except ObserveStoreError as exc:
            assert str(exc) == "observe_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt observe snapshot accepted")
        repaired = matched_store.repair_snapshot()
        recovered = matched_store.recover(require_snapshot_match=True)
        assert repaired["observe_state_digest"] == recovered["observe_state_digest"]

        conflict_quality = {
            "coverage": 0.9,
            "freshness": 0.9,
            "provenance": 0.9,
            "calibration": 0.9,
            "completeness": 0.9,
            "conflict": 0.9,
            "assessment_method_digest": sha("conflict-quality-method"),
        }
        conflict_store, conflict_state = prepared_assessed_state(
            root=root / "conflicted",
            observe_id="observe-conflicted",
            act_state=act_state,
            quality=conflict_quality,
            conflict=True,
        )
        conflicted, _ = _finish(
            store=conflict_store,
            state=conflict_state,
            verdict="CONFLICTED",
            tick=40,
        )
        assert conflicted["route"] == "OBSERVATION_CONFLICTED"
        assert conflicted["observation_debt_discharged"] is False
        assert conflicted["reobservation_required"] is True
        assert conflicted["verification_required"] is True

        _target_substitution_rejected(root / "target-substitution", act_state)
        _low_quality_directional_rejected(root / "low-quality", act_state)

        return {
            "status": "OBSERVE_OS_EFFECT_GROUNDED_OBSERVATION_V0_1_OK",
            "matched_route": matched["route"],
            "matched_evidence_packet_digest": matched["evidence_packet_digest"],
            "matched_observation_debt_discharged": matched[
                "observation_debt_discharged"
            ],
            "verification_required": matched["verification_required"],
            "conflicted_route": conflicted["route"],
            "conflicted_reobservation_required": conflicted[
                "reobservation_required"
            ],
            "ledger_commits": matched_store.ledger_commit_count(),
            "recovered_observe_state_digest": recovered["observe_state_digest"],
            "observe_phase_receipt_digest": phase_receipt[
                "observe_phase_receipt_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))

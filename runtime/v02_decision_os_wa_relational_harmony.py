from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_kernel_v0_1 import build_replan_decision_activation_receipt
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_wa_kernel_v0_2 import (
    build_initial_wa_state,
    build_replan_wa_activation_receipt,
    build_wa_event,
)
from runtime.kuuos_decision_os_wa_store_v0_2 import (
    WaDecisionStore,
    WaDecisionStoreError,
)
from runtime.kuuos_decision_os_wa_types_v0_2 import (
    ALERT_DIMENSIONS,
    POSITIVE_DIMENSIONS,
    copy_non_authority,
)
from runtime.v01_decision_os_relational_deliberation import (
    _challenge,
    _complete_cycle,
    _initial,
    _middle,
    _option,
)

WA_WEIGHTS = {
    "inclusion": 0.18,
    "dialogue": 0.16,
    "mutual_reflection": 0.14,
    "emergence": 0.12,
    "dynamic_adaptation": 0.14,
    "non_hierarchy": 0.14,
    "recursive_feedback": 0.12,
}

WA_THRESHOLDS = {
    "bottleneck_weight": 0.35,
    "minimum_wa_floor": 0.55,
    "minimum_dimension_floor": 0.40,
    "suspected_false_harmony_threshold": 0.40,
    "confirmed_false_harmony_threshold": 0.60,
}


def _interval(lower: float, upper: float) -> dict[str, float]:
    return {"lower": lower, "upper": upper}


def _profile(
    source_state: Mapping[str, Any],
    option_id: str,
    *,
    positive_lower: float,
    positive_upper: float,
    alert_lower: float = 0.05,
    alert_upper: float = 0.10,
    weak_dimension: str | None = None,
    weak_interval: tuple[float, float] = (0.20, 0.30),
    suspected_dimension: str | None = None,
    suspected_interval: tuple[float, float] = (0.20, 0.50),
    dissent_considered: bool = True,
    minority_preserved: bool = True,
) -> dict[str, Any]:
    positive = {
        dimension: _interval(positive_lower, positive_upper)
        for dimension in POSITIVE_DIMENSIONS
    }
    if weak_dimension is not None:
        positive[weak_dimension] = _interval(*weak_interval)
    alerts = {
        dimension: _interval(alert_lower, alert_upper)
        for dimension in ALERT_DIMENSIONS
    }
    if suspected_dimension is not None:
        alerts[suspected_dimension] = _interval(*suspected_interval)
    return {
        "option_id": option_id,
        "option_digest": source_state["source_option_digest_by_id"][option_id]
        if "source_option_digest_by_id" in source_state
        else next(
            option["option_digest"]
            for option in source_state["options"]
            if option["option_id"] == option_id
        ),
        "positive_intervals": positive,
        "alert_intervals": alerts,
        "dissent_considered": dissent_considered,
        "minority_preserved": minority_preserved,
        "dissent_evidence_digests": [sha("dissent-" + option_id)],
        "minority_stakeholder_digests": [sha("minority-" + option_id)],
        "dialogue_receipt_digest": sha("dialogue-" + option_id),
        "indra_network_receipt_digest": sha("indra-" + option_id),
    }


def _source_decision(root: Path) -> dict[str, Any]:
    store = DecisionStore(root)
    state = store.initialize(_initial("decision-wa-source-001"))
    evidence = sha("wa-source-evidence")
    options = [
        _option(
            option_id="option-a",
            action_class="exploit",
            positive=(0.86, 0.94),
            negative=(0.04, 0.10),
            information_gain=(0.30, 0.45),
            required_evidence=[evidence],
            available_evidence=[evidence],
        ),
        _option(
            option_id="option-b",
            action_class="observe",
            positive=(0.38, 0.52),
            negative=(0.28, 0.38),
            information_gain=(0.45, 0.58),
        ),
        _option(
            option_id="option-c",
            action_class="local_action",
            positive=(0.90, 0.96),
            negative=(0.02, 0.06),
            prohibited=True,
        ),
    ]
    state, _ = _complete_cycle(
        store,
        state,
        options=options,
        challenge=_challenge(),
        middle_way=_middle(),
        tick_base=10,
        requested_route="SELECT_CANDIDATE",
    )
    assert state["route"] == "SELECT_CANDIDATE"
    assert state["selected_option_id"] == "option-a"
    assert state["retained_alternative_ids"] == ["option-b"]
    return state


def _event(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_wa_event(
        state=state,
        target_phase=target_phase,
        artifact_digest=sha(
            {"target_phase": target_phase, "payload": dict(payload), "tick": tick}
        ),
        payload=payload,
        now_ms=10_000 + tick,
    )


def _apply(
    store: WaDecisionStore,
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_event(state, target_phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _complete_wa_cycle(
    store: WaDecisionStore,
    state: Mapping[str, Any],
    *,
    profiles: Sequence[Mapping[str, Any]],
    requested_route: str,
    tick_base: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = _apply(
        store,
        state,
        "profile",
        {"profiles": list(profiles)},
        tick_base + 1,
    )
    state = _apply(
        store,
        state,
        "evaluate",
        {"evaluation_receipt_digest": sha("wa-evaluation")},
        tick_base + 2,
    )
    state = _apply(
        store,
        state,
        "false_harmony_check",
        {"false_harmony_receipt_digest": sha("wa-false-harmony")},
        tick_base + 3,
    )
    state = _apply(
        store,
        state,
        "plurality_check",
        {"plurality_receipt_digest": sha("wa-plurality")},
        tick_base + 4,
    )
    state = _apply(
        store,
        state,
        "gate",
        {
            "wa_gate_rule_digest": sha("wa-gate-rule-v02"),
            "requested_route": requested_route,
        },
        tick_base + 5,
    )
    commit_event = _event(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "wa_not_truth": True,
            "wa_not_execution": True,
            "wa_not_moral_veto": True,
            "activation_boundary": "mission_replan_only",
            "non_authority": copy_non_authority(),
        },
        tick_base + 6,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _initial_wa(source: Mapping[str, Any], wa_id: str) -> dict[str, Any]:
    return build_initial_wa_state(
        wa_id=wa_id,
        source_decision_state=source,
        weights=WA_WEIGHTS,
        thresholds=WA_THRESHOLDS,
        now_ms=10_000,
    )


def run_kernel() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kuuos-decision-wa-v02-") as tmp:
        root = Path(tmp)
        source = _source_decision(root / "source")

        endorse_store = WaDecisionStore(root / "endorse")
        endorse_state = endorse_store.initialize(_initial_wa(source, "wa-endorse-001"))

        skipped = endorse_store.apply(
            _event(
                endorse_state,
                "evaluate",
                {"evaluation_receipt_digest": sha("skip")},
                1,
            )
        )
        assert skipped["status"] == "REJECTED"
        assert "wa_event_phase_order_invalid" in skipped["errors"]
        assert endorse_store.ledger_commit_count() == 0

        incomplete = endorse_store.apply(
            _event(
                endorse_state,
                "profile",
                {
                    "profiles": [
                        _profile(
                            source,
                            "option-a",
                            positive_lower=0.82,
                            positive_upper=0.92,
                        )
                    ]
                },
                2,
            )
        )
        assert incomplete["status"] == "REJECTED"
        assert "wa_all_source_admissible_options_must_be_profiled" in incomplete[
            "errors"
        ]
        assert endorse_store.ledger_commit_count() == 0

        endorse_profiles = [
            _profile(
                source,
                "option-a",
                positive_lower=0.82,
                positive_upper=0.92,
            ),
            _profile(
                source,
                "option-b",
                positive_lower=0.56,
                positive_upper=0.68,
                alert_lower=0.08,
                alert_upper=0.16,
            ),
        ]
        endorse_state, endorse_commit = _complete_wa_cycle(
            endorse_store,
            endorse_state,
            profiles=endorse_profiles,
            requested_route="ENDORSE",
            tick_base=10,
        )
        assert endorse_state["route"] == "ENDORSE"
        assert endorse_state["endorsed_option_ids"] == ["option-a"]
        assert endorse_state["source_selected_option_id"] == "option-a"
        assert endorse_state["source_retained_alternative_ids"] == ["option-b"]
        assert endorse_state["plurality"]["retained_alternatives_preserved"] is True
        selected_record = next(
            record
            for record in endorse_state["wa_records"]
            if record["option_id"] == "option-a"
        )
        assert selected_record["wa_interval"]["lower"] >= WA_THRESHOLDS[
            "minimum_wa_floor"
        ]

        before_replay = endorse_store.ledger_commit_count()
        replay = endorse_store.apply(endorse_commit)
        assert replay["status"] == "REPLAYED"
        assert endorse_store.ledger_commit_count() == before_replay

        try:
            build_replan_wa_activation_receipt(
                state=endorse_state,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-cycle-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=20_000,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("wa_activation_without_replan_was_accepted")

        activation = build_replan_wa_activation_receipt(
            state=endorse_state,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-cycle-state"),
            replan_receipt_digest=sha("replan-receipt"),
            next_plan_basis_digest=sha("next-plan-basis"),
            now_ms=20_001,
        )
        assert activation["wa_not_truth"] is True
        assert activation["wa_not_execution"] is True
        assert activation["wa_not_moral_veto"] is True
        assert activation["host_license_granted"] is False

        snapshot_path = root / "endorse" / "wa-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            endorse_store.recover(require_snapshot_match=True)
        except WaDecisionStoreError as exc:
            assert str(exc) == "wa_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_wa_snapshot_was_accepted")
        repaired = endorse_store.repair_snapshot()
        recovered = endorse_store.recover(require_snapshot_match=True)
        assert repaired["wa_state_digest"] == recovered["wa_state_digest"]

        suspected_store = WaDecisionStore(root / "suspected")
        suspected_state = suspected_store.initialize(
            _initial_wa(source, "wa-suspected-001")
        )
        suspected_profiles = [
            _profile(
                source,
                "option-a",
                positive_lower=0.82,
                positive_upper=0.92,
                suspected_dimension="false_stability",
                suspected_interval=(0.20, 0.52),
            ),
            endorse_profiles[1],
        ]
        suspected_state, _ = _complete_wa_cycle(
            suspected_store,
            suspected_state,
            profiles=suspected_profiles,
            requested_route="REOBSERVE",
            tick_base=100,
        )
        assert suspected_state["route"] == "REOBSERVE"
        assert suspected_state["review_option_ids"] == ["option-a"]

        minority_store = WaDecisionStore(root / "minority")
        minority_state = minority_store.initialize(
            _initial_wa(source, "wa-minority-001")
        )
        minority_profiles = [
            _profile(
                source,
                "option-a",
                positive_lower=0.82,
                positive_upper=0.92,
                minority_preserved=False,
            ),
            endorse_profiles[1],
        ]
        minority_state, _ = _complete_wa_cycle(
            minority_store,
            minority_state,
            profiles=minority_profiles,
            requested_route="ESCALATE",
            tick_base=200,
        )
        assert minority_state["route"] == "ESCALATE"
        assert minority_state["review_option_ids"] == ["option-a"]
        minority_record = next(
            record
            for record in minority_state["false_harmony_records"]
            if record["option_id"] == "option-a"
        )
        assert minority_record["confirmed_false_harmony"] is True
        assert "minority_not_preserved" in minority_record["reason_codes"]

        weak_store = WaDecisionStore(root / "weak")
        weak_state = weak_store.initialize(_initial_wa(source, "wa-weak-001"))
        weak_profiles = [
            _profile(
                source,
                "option-a",
                positive_lower=0.82,
                positive_upper=0.92,
                weak_dimension="dialogue",
                weak_interval=(0.20, 0.30),
            ),
            endorse_profiles[1],
        ]
        weak_state, _ = _complete_wa_cycle(
            weak_store,
            weak_state,
            profiles=weak_profiles,
            requested_route="REPAIR",
            tick_base=300,
        )
        assert weak_state["route"] == "REPAIR"
        assert weak_state["review_option_ids"] == ["option-a"]
        weak_record = next(
            record
            for record in weak_state["wa_records"]
            if record["option_id"] == "option-a"
        )
        assert weak_record["weakest_interval"]["lower"] == 0.20

        return {
            "status": "DECISION_OS_WA_RELATIONAL_HARMONY_V0_2_OK",
            "source_decision_digest": source["latest_committed_decision_digest"],
            "endorse_route": endorse_state["route"],
            "endorsed_option_ids": endorse_state["endorsed_option_ids"],
            "selected_wa_interval": selected_record["wa_interval"],
            "suspected_route": suspected_state["route"],
            "minority_route": minority_state["route"],
            "weak_dialogue_route": weak_state["route"],
            "activation_receipt_digest": activation[
                "wa_activation_receipt_digest"
            ],
            "wa_state_digest": recovered["wa_state_digest"],
            "ledger_commits": endorse_store.ledger_commit_count(),
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))

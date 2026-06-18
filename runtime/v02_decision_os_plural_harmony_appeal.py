from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_kernel_v0_2 import (
    build_initial_plural_state,
    build_plural_event,
    build_plural_replan_activation_receipt,
)
from runtime.kuuos_decision_os_plural_store_v0_2 import (
    PluralDecisionStore,
    PluralDecisionStoreError,
)
from runtime.kuuos_decision_os_plural_types_v0_2 import copy_non_authority
from runtime.v01_decision_os_relational_deliberation import (
    _challenge,
    _complete_cycle,
    _initial,
    _middle,
    _option,
)


PLURAL_THRESHOLDS = {
    "minimum_support_weight": 0.66,
    "maximum_opposition_weight": 0.34,
    "minimum_worst_case_value": 0.10,
    "consensus_separation_margin": 0.05,
    "material_appeal_threshold": 0.60,
}

MISSION_SAFETY = sha("mission-bound-patient-safety")
MISSION_RESOURCE = sha("mission-bound-resource-boundary")


def _profile(
    *,
    mission: float,
    benefit: float,
    information: float,
    recoverability: float,
    reversibility: float,
    stakeholder_fit: float,
    qi: float,
    harm: float,
    cost: float,
    delay: float,
    uncertainty: float,
) -> dict[str, float]:
    value = {
        "mission_alignment": mission,
        "expected_benefit": benefit,
        "information_gain": information,
        "recoverability": recoverability,
        "reversibility": reversibility,
        "stakeholder_fit": stakeholder_fit,
        "qi_process_compatibility": qi,
        "expected_harm": harm,
        "cost_burden": cost,
        "delay_risk": delay,
        "uncertainty_burden": uncertainty,
    }
    assert abs(sum(value.values()) - 1.0) < 1e-12
    return value


PATIENT_PROFILE = _profile(
    mission=0.12,
    benefit=0.15,
    information=0.05,
    recoverability=0.12,
    reversibility=0.12,
    stakeholder_fit=0.10,
    qi=0.04,
    harm=0.15,
    cost=0.05,
    delay=0.05,
    uncertainty=0.05,
)

OPERATOR_PROFILE = _profile(
    mission=0.15,
    benefit=0.20,
    information=0.10,
    recoverability=0.10,
    reversibility=0.10,
    stakeholder_fit=0.10,
    qi=0.05,
    harm=0.08,
    cost=0.05,
    delay=0.04,
    uncertainty=0.03,
)

CAREGIVER_PROFILE = _profile(
    mission=0.13,
    benefit=0.18,
    information=0.07,
    recoverability=0.12,
    reversibility=0.10,
    stakeholder_fit=0.10,
    qi=0.05,
    harm=0.10,
    cost=0.06,
    delay=0.05,
    uncertainty=0.04,
)


def _stakeholders(
    *,
    patient_veto: Sequence[Mapping[str, Any]] = (),
    operator_veto: Sequence[Mapping[str, Any]] = (),
    caregiver_veto: Sequence[Mapping[str, Any]] = (),
    minimum_override: float | None = None,
) -> list[dict[str, Any]]:
    patient_minimum = 0.15 if minimum_override is None else minimum_override
    operator_minimum = 0.20 if minimum_override is None else minimum_override
    caregiver_minimum = 0.18 if minimum_override is None else minimum_override
    return [
        {
            "stakeholder_id": "patient",
            "role": "affected_person",
            "weight": 0.50,
            "profile_weights": PATIENT_PROFILE,
            "minimum_acceptable_value": patient_minimum,
            "disagreement_point": 0.00,
            "protected_constraint_digests": [MISSION_SAFETY],
            "veto": list(patient_veto),
            "appeal_right": True,
        },
        {
            "stakeholder_id": "operator",
            "role": "responsible_operator",
            "weight": 0.30,
            "profile_weights": OPERATOR_PROFILE,
            "minimum_acceptable_value": operator_minimum,
            "disagreement_point": 0.00,
            "protected_constraint_digests": [MISSION_RESOURCE],
            "veto": list(operator_veto),
            "appeal_right": True,
        },
        {
            "stakeholder_id": "caregiver",
            "role": "care_network",
            "weight": 0.20,
            "profile_weights": CAREGIVER_PROFILE,
            "minimum_acceptable_value": caregiver_minimum,
            "disagreement_point": 0.00,
            "protected_constraint_digests": [MISSION_SAFETY],
            "veto": list(caregiver_veto),
            "appeal_right": True,
        },
    ]


def _veto(option_id: str, constraint_digest: str, label: str) -> dict[str, Any]:
    return {
        "option_id": option_id,
        "constraint_digest": constraint_digest,
        "evidence_digest": sha("veto-evidence-" + label),
        "reason_digest": sha("veto-reason-" + label),
    }


def _appeal(
    *,
    appeal_id: str,
    stakeholder_id: str,
    target_option_id: str,
    materiality: float,
    protected: bool = False,
    source_inconsistency: bool = False,
) -> dict[str, Any]:
    return {
        "appeal_id": appeal_id,
        "stakeholder_id": stakeholder_id,
        "target_option_id": target_option_id,
        "reason_digest": sha("appeal-reason-" + appeal_id),
        "evidence_digests": [sha("appeal-evidence-" + appeal_id)],
        "protected_boundary_claimed": protected,
        "source_inconsistency_claimed": source_inconsistency,
        "materiality": materiality,
    }


def _source_decision(root: Path) -> dict[str, Any]:
    store = DecisionStore(root / "v01-source")
    state = store.initialize(_initial("decision-v02-source"))
    evidence = sha("required-evidence-v02")
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
    assert state["admissible_option_ids"] == ["option-a", "option-b"]
    return state


def _event(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_plural_event(
        state=state,
        target_phase=target_phase,
        artifact_digest=sha(
            {"target_phase": target_phase, "payload": dict(payload), "tick": tick}
        ),
        payload=payload,
        now_ms=10_000 + tick,
    )


def _apply(
    store: PluralDecisionStore,
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_event(state, target_phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _complete_plural_cycle(
    *,
    store: PluralDecisionStore,
    state: Mapping[str, Any],
    stakeholders: Sequence[Mapping[str, Any]],
    appeals: Sequence[Mapping[str, Any]] = (),
    handover_required: bool = False,
    requested_route: str | None = None,
    tick_base: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = _apply(
        store,
        state,
        "register_stakeholders",
        {
            "source_binding_receipt_digest": sha("source-binding-v02"),
            "source_decision_state_digest": state["source_decision_state_digest"],
            "source_decision_basis_digest": state["source_decision_basis_digest"],
            "stakeholders": list(stakeholders),
        },
        tick_base + 1,
    )
    state = _apply(
        store,
        state,
        "evaluate_plurality",
        {"evaluation_receipt_digest": sha("plural-evaluation-v02")},
        tick_base + 2,
    )
    state = _apply(
        store,
        state,
        "validate_vetoes",
        {
            "mission_bound_constraint_digests": [MISSION_SAFETY, MISSION_RESOURCE],
            "veto_validation_receipt_digest": sha("veto-validation-v02"),
        },
        tick_base + 3,
    )
    state = _apply(
        store,
        state,
        "aggregate",
        {"aggregation_receipt_digest": sha("plural-aggregation-v02")},
        tick_base + 4,
    )
    state = _apply(
        store,
        state,
        "explain",
        {
            "method": "stakeholder_ablation",
            "explanation_receipt_digest": sha("plural-explanation-v02"),
        },
        tick_base + 5,
    )
    state = _apply(
        store,
        state,
        "appeal_window",
        {
            "appeals": list(appeals),
            "appeal_window_receipt_digest": sha("appeal-window-v02"),
        },
        tick_base + 6,
    )
    adjudication_payload: dict[str, Any] = {
        "adjudication_rule_digest": sha("plural-adjudication-rule-v02"),
        "handover_required": handover_required,
    }
    if requested_route is not None:
        adjudication_payload["requested_route"] = requested_route
    state = _apply(
        store,
        state,
        "adjudicate",
        adjudication_payload,
        tick_base + 7,
    )
    commit_event = _event(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "plural_decision_not_execution": True,
            "consensus_not_truth": True,
            "activation_boundary": "mission_replan_only",
            "non_authority": copy_non_authority(),
        },
        tick_base + 8,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _new_plural_store(
    root: Path, name: str, source_state: Mapping[str, Any]
) -> tuple[PluralDecisionStore, dict[str, Any]]:
    store = PluralDecisionStore(root / name)
    state = build_initial_plural_state(
        source_decision_state=source_state,
        plural_id="plural-" + name,
        lineage_id="plural-lineage-v02",
        thresholds=PLURAL_THRESHOLDS,
        now_ms=10_000,
    )
    return store, store.initialize(state)


def run_kernel() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kuuos-decision-v02-") as temporary:
        root = Path(temporary)
        source_state = _source_decision(root)

        consensus_store, consensus_state = _new_plural_store(
            root, "consensus", source_state
        )
        skipped = consensus_store.apply(
            _event(
                consensus_state,
                "aggregate",
                {"aggregation_receipt_digest": sha("skip")},
                1,
            )
        )
        assert skipped["status"] == "REJECTED"
        assert "plural_event_phase_order_invalid" in skipped["errors"]
        assert consensus_store.ledger_commit_count() == 0

        consensus_state, consensus_commit = _complete_plural_cycle(
            store=consensus_store,
            state=consensus_state,
            stakeholders=_stakeholders(),
            requested_route="CONSENSUS_CANDIDATE",
            tick_base=10,
        )
        assert consensus_state["route"] == "CONSENSUS_CANDIDATE"
        assert consensus_state["selected_option_id"] == "option-a"
        assert consensus_state["source_option_ids"] == ["option-a", "option-b"]
        assert consensus_state["broadly_acceptable_option_ids"]
        assert consensus_state["explanation"]["method"] == "stakeholder_ablation"
        assert consensus_state["pending_replan_activation"] is True
        assert all(
            record["explanation_not_causal_truth"] is True
            for record in consensus_state["explanation"]["stakeholder_ablation"]
        )

        commits_before_replay = consensus_store.ledger_commit_count()
        replay = consensus_store.apply(consensus_commit)
        assert replay["status"] == "REPLAYED"
        assert consensus_store.ledger_commit_count() == commits_before_replay

        try:
            build_plural_replan_activation_receipt(
                state=consensus_state,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-cycle-v02"),
                replan_receipt_digest=sha("replan-v02"),
                next_plan_basis_digest=sha("next-plan-v02"),
                now_ms=20_000,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("plural_activation_without_replan_was_accepted")

        activation = build_plural_replan_activation_receipt(
            state=consensus_state,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-cycle-v02"),
            replan_receipt_digest=sha("replan-v02"),
            next_plan_basis_digest=sha("next-plan-v02"),
            now_ms=20_001,
        )
        assert activation["plural_decision_not_execution"] is True
        assert activation["consensus_not_truth"] is True
        assert activation["host_license_granted"] is False

        snapshot_path = root / "consensus" / "plural-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            consensus_store.recover(require_snapshot_match=True)
        except PluralDecisionStoreError as exc:
            assert str(exc) == "plural_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_plural_snapshot_was_accepted")
        repaired = consensus_store.repair_snapshot()
        recovered = consensus_store.recover(require_snapshot_match=True)
        assert repaired["plural_state_digest"] == recovered["plural_state_digest"]

        veto_store, veto_state = _new_plural_store(root, "validated-veto", source_state)
        veto_state, _ = _complete_plural_cycle(
            store=veto_store,
            state=veto_state,
            stakeholders=_stakeholders(
                patient_veto=[_veto("option-a", MISSION_SAFETY, "patient-a")]
            ),
            requested_route="CONSENSUS_CANDIDATE",
            tick_base=100,
        )
        assert veto_state["route"] == "CONSENSUS_CANDIDATE"
        assert veto_state["selected_option_id"] == "option-b"
        assert veto_state["veto_excluded_option_ids"] == ["option-a"]
        assert veto_state["validated_veto_records"][0]["validated"] is True

        negotiate_store, negotiate_state = _new_plural_store(
            root, "unvalidated-veto", source_state
        )
        negotiate_state, _ = _complete_plural_cycle(
            store=negotiate_store,
            state=negotiate_state,
            stakeholders=_stakeholders(
                patient_veto=[
                    _veto("option-a", sha("not-mission-bound"), "raw-only")
                ]
            ),
            requested_route="NEGOTIATE",
            tick_base=200,
        )
        assert negotiate_state["route"] == "NEGOTIATE"
        assert negotiate_state["veto_excluded_option_ids"] == []
        assert negotiate_state["unvalidated_veto_records"][0][
            "raw_veto_grants_authority"
        ] is False

        appeal_store, appeal_state = _new_plural_store(root, "appeal", source_state)
        appeal_state, _ = _complete_plural_cycle(
            store=appeal_store,
            state=appeal_state,
            stakeholders=_stakeholders(),
            appeals=[
                _appeal(
                    appeal_id="appeal-001",
                    stakeholder_id="patient",
                    target_option_id="option-a",
                    materiality=0.80,
                    protected=True,
                )
            ],
            requested_route="APPEAL",
            tick_base=300,
        )
        assert appeal_state["route"] == "APPEAL"
        assert appeal_state["appeal_history"][0]["future_only"] is True
        assert appeal_state["appeal_history"][0]["rewrites_prior_decision"] is False

        handover_store, handover_state = _new_plural_store(
            root, "handover", source_state
        )
        handover_state, _ = _complete_plural_cycle(
            store=handover_store,
            state=handover_state,
            stakeholders=_stakeholders(),
            handover_required=True,
            requested_route="HANDOVER",
            tick_base=400,
        )
        assert handover_state["route"] == "HANDOVER"

        hold_store, hold_state = _new_plural_store(root, "hold", source_state)
        hold_state, _ = _complete_plural_cycle(
            store=hold_store,
            state=hold_state,
            stakeholders=_stakeholders(minimum_override=0.95),
            requested_route="HOLD",
            tick_base=500,
        )
        assert hold_state["route"] == "HOLD"

        reject_store, reject_state = _new_plural_store(root, "reject", source_state)
        reject_state, _ = _complete_plural_cycle(
            store=reject_store,
            state=reject_state,
            stakeholders=_stakeholders(
                patient_veto=[
                    _veto("option-a", MISSION_SAFETY, "reject-a"),
                    _veto("option-b", MISSION_SAFETY, "reject-b"),
                ]
            ),
            requested_route="REJECT",
            tick_base=600,
        )
        assert reject_state["route"] == "REJECT"
        assert reject_state["pending_replan_activation"] is False
        try:
            build_plural_replan_activation_receipt(
                state=reject_state,
                mission_cycle_phase="replan",
                mission_cycle_state_digest=sha("mission-cycle-v02"),
                replan_receipt_digest=sha("replan-v02"),
                next_plan_basis_digest=sha("next-plan-v02"),
                now_ms=30_000,
            )
        except ValueError as exc:
            assert str(exc) == "plural_decision_not_pending_activation"
        else:
            raise AssertionError("rejected_plural_decision_was_activated")

        return {
            "status": "DECISION_OS_PLURAL_HARMONY_APPEAL_V0_2_OK",
            "source_decision_digest": source_state["latest_committed_decision_digest"],
            "consensus_route": consensus_state["route"],
            "consensus_selected_option": consensus_state["selected_option_id"],
            "validated_veto_selected_option": veto_state["selected_option_id"],
            "unvalidated_veto_route": negotiate_state["route"],
            "appeal_route": appeal_state["route"],
            "handover_route": handover_state["route"],
            "hold_route": hold_state["route"],
            "reject_route": reject_state["route"],
            "plural_state_digest": recovered["plural_state_digest"],
            "plural_activation_receipt_digest": activation[
                "plural_activation_receipt_digest"
            ],
            "ledger_commits": consensus_store.ledger_commit_count(),
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))

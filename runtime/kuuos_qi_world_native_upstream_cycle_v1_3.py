from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    BeliefGerbeStore,
    build_initial_gerbe_state,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    receipt_digest as belief_receipt_digest,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_kernel_v0_1 import build_initial_decision_state
from runtime.kuuos_decision_os_plural_kernel_v0_2 import (
    build_initial_plural_state,
    validate_plural_state,
)
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_state_v0_1 import validate_decision_state
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_decision_os_wa_state_v0_3 import (
    build_initial_wa_state,
    validate_wa_state,
)
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.v01_decision_os_relational_deliberation import (
    THRESHOLDS as DECISION_THRESHOLDS,
    WEIGHTS as DECISION_WEIGHTS,
    _challenge,
    _complete_cycle,
    _middle,
    _option,
)
from runtime.v01_plan_os_replan_bound_synthesis import (
    _candidate_steps,
    _complete_plan,
    _new_plan_state,
)
from runtime.v02_decision_os_plural_harmony_appeal import (
    PLURAL_THRESHOLDS,
    _complete_plural_cycle,
    _stakeholders,
)
from runtime.v03_belief_os_context_gerbe_coherence import (
    _gerbe_decision,
    _packet,
    _transport_receipt,
)
from runtime.v03_decision_os_wa_relational_harmony import (
    WA_THRESHOLDS,
    WA_WEIGHTS,
    _complete_wa_cycle,
    _standard_profiles,
)

VERSION = "kuuos_qi_world_native_upstream_cycle_v1_3"
LINEAGE_ID = "qi-world-native-full-cycle-lineage-v13"
MISSION_CONTRACT_DIGEST = sha("qi-world-native-full-cycle-mission-v13")
MISSION_STATE_DIGEST = sha("qi-world-native-full-cycle-mission-state-v13")


def _build_belief_receipt(root: Path) -> dict[str, Any]:
    target = "context-target"
    source_a = sha("native-full-cycle-belief-source-a")
    source_d = sha("native-full-cycle-belief-source-d")
    receipts = [
        _transport_receipt(
            packet_id="native-direct-a",
            lineage_id=LINEAGE_ID,
            source_context_id="context-a",
            target_context_id=target,
            source_state_digest=source_a,
            declared_path=["context-a", target],
            lower=0.58,
            upper=0.78,
            overlap=0.94,
            reliability=0.88,
            qi_history_compatibility=0.95,
            evidence_label="native-evidence-direct-a",
            counterevidence_label="native-counter-direct-a",
            created_at_ms=4_100,
        ),
        _transport_receipt(
            packet_id="native-via-b",
            lineage_id=LINEAGE_ID,
            source_context_id="context-a",
            target_context_id=target,
            source_state_digest=source_a,
            declared_path=["context-a", "context-b", target],
            lower=0.56,
            upper=0.80,
            overlap=0.91,
            reliability=0.85,
            qi_history_compatibility=0.92,
            evidence_label="native-evidence-via-b",
            counterevidence_label="native-counter-via-b",
            created_at_ms=4_110,
        ),
        _transport_receipt(
            packet_id="native-via-c",
            lineage_id=LINEAGE_ID,
            source_context_id="context-a",
            target_context_id=target,
            source_state_digest=source_a,
            declared_path=["context-a", "context-c", target],
            lower=0.57,
            upper=0.79,
            overlap=0.90,
            reliability=0.84,
            qi_history_compatibility=0.91,
            evidence_label="native-evidence-via-c",
            counterevidence_label="native-counter-via-c",
            created_at_ms=4_120,
        ),
        _transport_receipt(
            packet_id="native-direct-d",
            lineage_id=LINEAGE_ID,
            source_context_id="context-d",
            target_context_id=target,
            source_state_digest=source_d,
            declared_path=["context-d", target],
            lower=0.54,
            upper=0.77,
            overlap=0.89,
            reliability=0.83,
            qi_history_compatibility=0.90,
            evidence_label="native-evidence-direct-d",
            counterevidence_label="native-counter-direct-d",
            created_at_ms=4_130,
        ),
    ]
    packet = _packet(
        packet_id="native-belief-gerbe-packet-v13",
        lineage_id=LINEAGE_ID,
        target_context_id=target,
        receipts=receipts,
        gerbe_decision=_gerbe_decision(
            target_context_id=target,
            two_curvature=0.03,
            higher_defect=0.02,
            suffix="native-full-cycle",
        ),
        created_at_ms=5_000,
    )
    store = BeliefGerbeStore(root)
    store.initialize(build_initial_gerbe_state(lineage_id=LINEAGE_ID, now_ms=4_000))
    result = store.apply(packet)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    receipt = result["receipt"]
    if receipt.get("route") != "CANDIDATE":
        raise AssertionError(receipt)
    return receipt


def _decision_options() -> list[dict[str, Any]]:
    evidence = sha("native-full-cycle-required-evidence")
    return [
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


def _build_decision_state(root: Path, belief_receipt: Mapping[str, Any]) -> dict[str, Any]:
    initial = build_initial_decision_state(
        decision_id="native-full-cycle-decision-v13",
        lineage_id=LINEAGE_ID,
        mission_contract_digest=MISSION_CONTRACT_DIGEST,
        mission_state_digest=MISSION_STATE_DIGEST,
        source_belief_receipt_digest=str(
            belief_receipt["belief_gerbe_receipt_digest"]
        ),
        decision_context_digest=sha("native-full-cycle-decision-context"),
        decision_budget=1.0,
        weights=DECISION_WEIGHTS,
        thresholds=DECISION_THRESHOLDS,
        now_ms=1_000,
    )
    store = DecisionStore(root)
    state = store.initialize(initial)
    state, _ = _complete_cycle(
        store,
        state,
        options=_decision_options(),
        challenge=_challenge(),
        middle_way=_middle(),
        tick_base=10,
        requested_route="SELECT_CANDIDATE",
    )
    if state.get("route") != "SELECT_CANDIDATE":
        raise AssertionError(state)
    return state


def _build_plural_state(root: Path, decision_state: Mapping[str, Any]) -> dict[str, Any]:
    initial = build_initial_plural_state(
        source_decision_state=decision_state,
        plural_id="native-full-cycle-plural-v13",
        lineage_id=LINEAGE_ID,
        thresholds=PLURAL_THRESHOLDS,
        now_ms=10_000,
    )
    store = PluralDecisionStore(root)
    state = store.initialize(initial)
    state, _ = _complete_plural_cycle(
        store=store,
        state=state,
        stakeholders=_stakeholders(),
        requested_route="CONSENSUS_CANDIDATE",
        tick_base=10,
    )
    if state.get("route") != "CONSENSUS_CANDIDATE":
        raise AssertionError(state)
    return state


def _build_wa_state(root: Path, plural_state: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    initial = build_initial_wa_state(
        wa_id="native-full-cycle-wa-v13",
        source_plural_state=plural_state,
        weights=WA_WEIGHTS,
        thresholds=WA_THRESHOLDS,
        now_ms=30_000,
    )
    store = WaDecisionStore(root)
    state = store.initialize(initial)
    state, _ = _complete_wa_cycle(
        store,
        state,
        profiles=_standard_profiles(plural_state),
        requested_route="ENDORSE",
        tick_base=20,
    )
    if state.get("route") != "ENDORSE":
        raise AssertionError(state)
    activation = build_replan_wa_activation_receipt(
        state=state,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
        replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
        next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
        now_ms=50_000,
    )
    return state, activation


def _build_plan_state(
    root: Path,
    wa_state: Mapping[str, Any],
    wa_activation: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    initial = _new_plan_state(
        plan_id="native-full-cycle-plan-v13",
        wa_state=wa_state,
        activation=wa_activation,
    )
    store = PlanStore(root)
    state = store.initialize(initial)
    state, _ = _complete_plan(store, state, _candidate_steps(), 10)
    if state.get("route") != "PLAN_CANDIDATE":
        raise AssertionError(state)
    activation = build_plan_phase_activation_receipt(
        state=state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("native-full-cycle-plan-state"),
        plan_phase_receipt_digest=sha("native-full-cycle-plan-phase"),
        now_ms=70_001,
    )
    return state, activation


def build_native_upstream_cycle(root: Path) -> dict[str, Any]:
    belief = _build_belief_receipt(root / "belief")
    decision = _build_decision_state(root / "decision", belief)
    plural = _build_plural_state(root / "plural", decision)
    wa, wa_activation = _build_wa_state(root / "wa", plural)
    plan, plan_activation = _build_plan_state(root / "plan", wa, wa_activation)
    result = {
        "version": VERSION,
        "lineage_id": LINEAGE_ID,
        "mission_contract_digest": MISSION_CONTRACT_DIGEST,
        "BeliefOS": deepcopy(belief),
        "DecisionOS": deepcopy(decision),
        "DecisionOSPlural": deepcopy(plural),
        "DecisionOSWa": deepcopy(wa),
        "WaActivation": deepcopy(wa_activation),
        "PlanOS": deepcopy(plan),
        "PlanActivation": deepcopy(plan_activation),
    }
    errors = validate_native_upstream_cycle(result)
    if errors:
        raise ValueError("native_upstream_cycle_invalid:" + ";".join(errors))
    return result


def validate_native_upstream_cycle(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != VERSION:
            errors.append("native_upstream_version_invalid")
        lineage = value.get("lineage_id")
        mission = value.get("mission_contract_digest")
        belief = dict(value.get("BeliefOS", {}))
        decision = dict(value.get("DecisionOS", {}))
        plural = dict(value.get("DecisionOSPlural", {}))
        wa = dict(value.get("DecisionOSWa", {}))
        plan = dict(value.get("PlanOS", {}))

        if belief.get("belief_gerbe_receipt_digest") != belief_receipt_digest(belief):
            errors.append("native_belief_receipt_digest_invalid")
        if belief.get("lineage_id") != lineage:
            errors.append("native_belief_lineage_mismatch")
        if belief.get("route") != "CANDIDATE":
            errors.append("native_belief_route_invalid")
        errors.extend(f"DecisionOS:{error}" for error in validate_decision_state(decision))
        errors.extend(f"DecisionOSPlural:{error}" for error in validate_plural_state(plural))
        errors.extend(f"DecisionOSWa:{error}" for error in validate_wa_state(wa))
        errors.extend(f"PlanOS:{error}" for error in validate_plan_state(plan))

        for name, state in (
            ("DecisionOS", decision),
            ("DecisionOSPlural", plural),
            ("DecisionOSWa", wa),
            ("PlanOS", plan),
        ):
            if state.get("lineage_id") != lineage:
                errors.append(f"native_{name}_lineage_mismatch")
            if state.get("mission_contract_digest") != mission:
                errors.append(f"native_{name}_mission_mismatch")

        if decision.get("source_belief_receipt_digest") != belief.get(
            "belief_gerbe_receipt_digest"
        ):
            errors.append("native_decision_source_belief_mismatch")
        if plural.get("source_decision_state_digest") != decision.get(
            "decision_state_digest"
        ):
            errors.append("native_plural_source_decision_mismatch")
        if plural.get("source_decision_basis_digest") != decision.get(
            "decision_basis_digest"
        ):
            errors.append("native_plural_source_decision_basis_mismatch")
        if wa.get("source_plural_state_digest") != plural.get("plural_state_digest"):
            errors.append("native_wa_source_plural_mismatch")
        if wa.get("source_decision_basis_digest") != decision.get(
            "decision_basis_digest"
        ):
            errors.append("native_wa_source_decision_basis_mismatch")
        if plan.get("source_wa_state_digest") != wa.get("wa_state_digest"):
            errors.append("native_plan_source_wa_mismatch")
        if plan.get("source_wa_basis_digest") != wa.get("wa_basis_digest"):
            errors.append("native_plan_source_wa_basis_mismatch")
        if plan.get("source_plural_decision_basis_digest") != plural.get(
            "plural_decision_basis_digest"
        ):
            errors.append("native_plan_source_plural_basis_mismatch")
        if plan.get("source_decision_basis_digest") != decision.get(
            "decision_basis_digest"
        ):
            errors.append("native_plan_source_decision_basis_mismatch")
        if plan.get("current_phase") != "commit":
            errors.append("native_plan_not_committed")
        if plan.get("route") != "PLAN_CANDIDATE":
            errors.append("native_plan_route_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs, prepared_project_state
from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    BeliefGerbeStore,
    build_initial_gerbe_state,
    validate_gerbe_state,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION as BELIEF_RECEIPT_VERSION,
    receipt_digest as belief_receipt_digest,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_kernel_v0_1 import (
    build_initial_decision_state,
    validate_decision_state,
)
from runtime.kuuos_decision_os_plural_kernel_v0_2 import (
    build_initial_plural_state,
    validate_plural_state,
)
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_initial_wa_state,
    build_replan_wa_activation_receipt,
    validate_wa_state,
)
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_learn_os_fixture_v0_1 import prepared_gated_state
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_initial_plan_state,
    build_plan_phase_activation_receipt,
    validate_plan_state,
)
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.kuuos_qi_world_os_interface_bridge_v1_0 import (
    build_qi_world_os_interface_receipt,
    validate_qi_world_os_interface_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import OS_INTERFACE_SPECS, OS_KINDS
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.v01_decision_os_relational_deliberation import (
    THRESHOLDS as DECISION_THRESHOLDS,
    WEIGHTS as DECISION_WEIGHTS,
    _challenge,
    _complete_cycle,
    _middle,
    _option,
)
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.v01_plan_os_replan_bound_synthesis import _candidate_steps, _complete_plan
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify
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

VERSION = "kuuos_qi_world_native_full_cycle_v1_3"
RECEIPT_VERSION = "kuuos_qi_world_native_full_cycle_receipt_v1_3"
CYCLE_ID = "qi-world-native-full-cycle-v13"

FULL_CYCLE_NON_AUTHORITY = {
    "adapter_grants_execution": False,
    "adapter_grants_truth": False,
    "adapter_issues_authority": False,
    "adapter_changes_native_artifacts": False,
    "adapter_updates_exact_world": False,
    "adapter_overwrites_history": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def full_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "native_full_cycle_receipt_digest")


def _build_belief(root: Path, lineage_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    target = "native-full-cycle-context"
    source = sha("native-full-cycle-belief-source")
    paths = [
        ("direct", ["context-a", target], 0.58, 0.78, 0.94, 0.90, 0.95),
        ("via-b", ["context-a", "context-b", target], 0.57, 0.79, 0.92, 0.88, 0.93),
        ("via-c", ["context-a", "context-c", target], 0.56, 0.80, 0.91, 0.87, 0.92),
    ]
    receipts = [
        _transport_receipt(
            packet_id="native-belief-" + name,
            lineage_id=lineage_id,
            source_context_id="context-a",
            target_context_id=target,
            source_state_digest=source,
            declared_path=path,
            lower=lower,
            upper=upper,
            overlap=overlap,
            reliability=reliability,
            qi_history_compatibility=qi,
            evidence_label="native-belief-evidence-" + name,
            counterevidence_label="native-belief-counter-" + name,
            created_at_ms=4_100 + index * 10,
        )
        for index, (name, path, lower, upper, overlap, reliability, qi) in enumerate(paths)
    ]
    packet = _packet(
        packet_id="native-belief-gerbe-packet",
        lineage_id=lineage_id,
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
    store.initialize(build_initial_gerbe_state(lineage_id=lineage_id, now_ms=4_000))
    result = store.apply(packet)
    if result.get("status") != "APPLIED":
        raise ValueError("native_full_cycle_belief_apply_failed:" + ";".join(result.get("errors", [])))
    receipt = dict(result["receipt"])
    state = dict(result["state"])
    if receipt.get("route") != "CANDIDATE":
        raise ValueError("native_full_cycle_belief_not_candidate")
    return state, receipt


def _build_decision(root: Path, lineage_id: str, mission: str, belief: Mapping[str, Any]) -> dict[str, Any]:
    store = DecisionStore(root)
    state = store.initialize(
        build_initial_decision_state(
            decision_id="native-full-cycle-decision",
            lineage_id=lineage_id,
            mission_contract_digest=mission,
            mission_state_digest=sha("native-full-cycle-mission-state"),
            source_belief_receipt_digest=str(belief["belief_gerbe_receipt_digest"]),
            decision_context_digest=sha("native-full-cycle-decision-context"),
            decision_budget=1.0,
            weights=DECISION_WEIGHTS,
            thresholds=DECISION_THRESHOLDS,
            now_ms=1_000,
        )
    )
    evidence = sha("native-full-cycle-required-evidence")
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
    return state


def _build_plural(root: Path, lineage_id: str, decision: Mapping[str, Any]) -> dict[str, Any]:
    store = PluralDecisionStore(root)
    state = store.initialize(
        build_initial_plural_state(
            source_decision_state=decision,
            plural_id="native-full-cycle-plural",
            lineage_id=lineage_id,
            thresholds=PLURAL_THRESHOLDS,
            now_ms=10_000,
        )
    )
    state, _ = _complete_plural_cycle(
        store=store,
        state=state,
        stakeholders=_stakeholders(),
        requested_route="CONSENSUS_CANDIDATE",
        tick_base=10,
    )
    return state


def _build_wa(root: Path, plural: Mapping[str, Any]) -> dict[str, Any]:
    store = WaDecisionStore(root)
    state = store.initialize(
        build_initial_wa_state(
            wa_id="native-full-cycle-wa",
            source_plural_state=plural,
            weights=WA_WEIGHTS,
            thresholds=WA_THRESHOLDS,
            now_ms=30_000,
        )
    )
    state, _ = _complete_wa_cycle(
        store,
        state,
        profiles=_standard_profiles(plural),
        requested_route="ENDORSE",
        tick_base=20,
    )
    return state


def _build_plan(root: Path, wa: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    activation = build_replan_wa_activation_receipt(
        state=wa,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
        replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
        next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
        now_ms=50_000,
    )
    store = PlanStore(root)
    state = store.initialize(
        build_initial_plan_state(
            plan_id="native-full-cycle-plan",
            source_wa_state=wa,
            replan_activation_receipt=activation,
            plan_budget=2.0,
            maximum_step_risk=0.40,
            now_ms=60_000,
        )
    )
    state, _ = _complete_plan(store, state, _candidate_steps(), 10)
    plan_activation = build_plan_phase_activation_receipt(
        state=state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
        plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
        now_ms=80_000,
    )
    return state, plan_activation


def _build_act(root: Path, plan: Mapping[str, Any], activation: Mapping[str, Any]) -> dict[str, Any]:
    policy, bundle, license_packet, projection = host_inputs(job_id="native-full-cycle-job")
    store, state = prepared_project_state(
        root=root,
        act_id="native-full-cycle-act",
        plan_state=plan,
        plan_activation=activation,
        job_id="native-full-cycle-job",
        host_license=license_packet,
        projection=projection,
    )
    state, _ = finish_act(
        store=store,
        state=state,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    return state


def _build_downstream(root: Path, act: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    observe_store, observe_pending = prepared_assessed_state(
        root=root / "observe",
        observe_id="native-full-cycle-observe",
        act_state=act,
    )
    observe, _ = finish_observe(
        store=observe_store,
        state=observe_pending,
        verdict="MATCHED",
        tick=5,
    )
    verify_store, verify_pending = prepared_corroborated_state(
        root=root / "verify",
        verify_id="native-full-cycle-verify",
        observe_state=observe,
        admissible=True,
    )
    verify, _ = finish_verify(
        store=verify_store,
        state=verify_pending,
        verdict="PASSED",
        criterion_satisfied=True,
        tick=4,
    )
    learn_store, learn_pending = prepared_gated_state(
        root=root / "learn",
        learn_id="native-full-cycle-learn",
        verify_state=verify,
        learning_kind="reinforcement",
        target_scope="belief_candidate",
    )
    learn, _ = finish_learn(store=learn_store, state=learn_pending, tick=5)
    return observe, verify, learn


def _build_native_artifacts(root: Path) -> dict[str, dict[str, Any]]:
    lineage = "native-full-cycle-lineage-v13"
    mission = sha("native-full-cycle-mission-contract")
    belief_state, belief_receipt = _build_belief(root / "belief", lineage)
    decision = _build_decision(root / "decision", lineage, mission, belief_receipt)
    plural = _build_plural(root / "plural", lineage, decision)
    wa = _build_wa(root / "wa", plural)
    plan, plan_activation = _build_plan(root / "plan", wa)
    act = _build_act(root / "act", plan, plan_activation)
    observe, verify, learn = _build_downstream(root / "downstream", act)
    return {
        "BeliefOSState": belief_state,
        "BeliefOSReceipt": belief_receipt,
        "DecisionOS": decision,
        "DecisionOSPlural": plural,
        "DecisionOSWa": wa,
        "PlanOS": plan,
        "ActOS": act,
        "ObserveOS": observe,
        "VerifyOS": verify,
        "LearnOS": learn,
    }


def _native_validation_errors(artifacts: Mapping[str, Mapping[str, Any]]) -> list[str]:
    errors: list[str] = []
    belief_state = artifacts.get("BeliefOSState")
    belief_receipt = artifacts.get("BeliefOSReceipt")
    if not isinstance(belief_state, Mapping):
        errors.append("BeliefOSState_missing")
    else:
        errors.extend(f"BeliefOSState:{error}" for error in validate_gerbe_state(belief_state))
    if not isinstance(belief_receipt, Mapping):
        errors.append("BeliefOSReceipt_missing")
    else:
        if belief_receipt.get("version") != BELIEF_RECEIPT_VERSION:
            errors.append("BeliefOSReceipt_version_invalid")
        if belief_receipt.get("belief_gerbe_receipt_digest") != belief_receipt_digest(belief_receipt):
            errors.append("BeliefOSReceipt_digest_invalid")
        if belief_receipt.get("route") != "CANDIDATE":
            errors.append("BeliefOSReceipt_route_invalid")
    validators = {
        "DecisionOS": validate_decision_state,
        "DecisionOSPlural": validate_plural_state,
        "DecisionOSWa": validate_wa_state,
        "PlanOS": validate_plan_state,
        "ActOS": validate_act_state,
        "ObserveOS": validate_observe_state,
        "VerifyOS": validate_verify_state,
        "LearnOS": validate_learn_state,
    }
    for name, validator in validators.items():
        artifact = artifacts.get(name)
        if not isinstance(artifact, Mapping):
            errors.append(f"{name}_missing")
        else:
            errors.extend(f"{name}:{error}" for error in validator(artifact))
    return errors


def _process_lineage_digest(artifacts: Mapping[str, Mapping[str, Any]]) -> str:
    return sha(
        {
            "lineage_id": artifacts["DecisionOS"]["lineage_id"],
            "belief_receipt_digest": artifacts["BeliefOSReceipt"]["belief_gerbe_receipt_digest"],
            "decision_state_digest": artifacts["DecisionOS"]["decision_state_digest"],
            "plural_state_digest": artifacts["DecisionOSPlural"]["plural_state_digest"],
            "wa_state_digest": artifacts["DecisionOSWa"]["wa_state_digest"],
            "plan_state_digest": artifacts["PlanOS"]["plan_state_digest"],
            "act_state_digest": artifacts["ActOS"]["act_state_digest"],
            "observe_state_digest": artifacts["ObserveOS"]["observe_state_digest"],
            "verify_state_digest": artifacts["VerifyOS"]["verify_state_digest"],
            "learn_state_digest": artifacts["LearnOS"]["learn_state_digest"],
        }
    )


def _build_world_projection(artifacts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = {
        "projection_kind": "native_full_os_cycle_projection",
        "belief_receipt_digest": artifacts["BeliefOSReceipt"]["belief_gerbe_receipt_digest"],
        "decision_state_digest": artifacts["DecisionOS"]["decision_state_digest"],
        "plural_state_digest": artifacts["DecisionOSPlural"]["plural_state_digest"],
        "wa_state_digest": artifacts["DecisionOSWa"]["wa_state_digest"],
        "plan_state_digest": artifacts["PlanOS"]["plan_state_digest"],
        "act_state_digest": artifacts["ActOS"]["act_state_digest"],
        "observe_state_digest": artifacts["ObserveOS"]["observe_state_digest"],
        "verify_state_digest": artifacts["VerifyOS"]["verify_state_digest"],
        "learn_state_digest": artifacts["LearnOS"]["learn_state_digest"],
        "evidence_packet_digest": artifacts["ObserveOS"]["evidence_packet_digest"],
        "verification_evidence_digest": artifacts["VerifyOS"]["verification_evidence_digest"],
        "learning_delta_digest": artifacts["LearnOS"]["learning_delta_digest"],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "world_projection_digest": "",
    }
    packet["world_projection_digest"] = _digest_without(packet, "world_projection_digest")
    return packet


def _build_qi_receipt(artifacts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    stages = [
        ("process_observation", "BELIEF_COHERENCE_COMMITTED", artifacts["BeliefOSReceipt"]["belief_gerbe_receipt_digest"]),
        ("process_action", "DECISION_WA_COMMITTED", artifacts["DecisionOSWa"]["wa_state_digest"]),
        ("process_action", "PLAN_COMMITTED", artifacts["PlanOS"]["plan_state_digest"]),
        ("process_action", "ACT_EFFECT_RECORDED", artifacts["ActOS"]["act_state_digest"]),
        ("process_observation", "OBSERVATION_RECORDED", artifacts["ObserveOS"]["observe_state_digest"]),
        ("process_observation", "VERIFICATION_RECORDED", artifacts["VerifyOS"]["verify_state_digest"]),
        ("process_action", "FUTURE_LEARNING_RECORDED", artifacts["LearnOS"]["learn_state_digest"]),
    ]
    history = []
    previous = stages[0][2]
    for index, (field, kind, digest) in enumerate(stages):
        history.append(
            {
                field: kind,
                "native_artifact_digest": digest,
                "source_state_digest": previous,
                "target_state_digest": digest,
                "transition_visible": True,
                "memory_link_visible": index > 0,
                "nonmarkov_link_visible": index >= 2,
            }
        )
        previous = digest
    return evaluate_qi_process_tensor(
        {
            "cycle_id": CYCLE_ID,
            "candidate_only": True,
            "nonfinal_marker": True,
            "two_truths_gap": True,
            "noncollapse_guard": True,
            "memory_overwrite_blocker": True,
            "world_identity_blocker": True,
            "process_history": history,
        }
    ).to_dict()


def _base_packet(name: str, lineage: str, world: str, input_digest: str, output_digest: str) -> dict[str, Any]:
    spec = OS_INTERFACE_SPECS[name]
    return {
        "os_kind": name,
        "cycle_id": CYCLE_ID,
        "process_lineage_digest": lineage,
        "world_projection_digest": world,
        "world_relation": spec["world_relation"],
        "qi_relation": spec["qi_relation"],
        "output_kind": spec["output_kind"],
        "input_digest": input_digest,
        "output_digest": output_digest,
        "candidate_only": True,
        "nonfinal_marker": True,
        "native_artifact": True,
    }


def _build_interface_receipt(
    artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
    qi_receipt: Mapping[str, Any],
    lineage: str,
) -> dict[str, Any]:
    belief = artifacts["BeliefOSReceipt"]
    decision = artifacts["DecisionOS"]
    plural = artifacts["DecisionOSPlural"]
    wa = artifacts["DecisionOSWa"]
    plan = artifacts["PlanOS"]
    act = artifacts["ActOS"]
    observe = artifacts["ObserveOS"]
    verify = artifacts["VerifyOS"]
    learn = artifacts["LearnOS"]
    wd = str(world["world_projection_digest"])
    packets = {
        "BeliefOS": _base_packet("BeliefOS", lineage, wd, wd, belief["belief_gerbe_receipt_digest"]),
        "DecisionOS": _base_packet("DecisionOS", lineage, wd, belief["belief_gerbe_receipt_digest"], wa["wa_state_digest"]),
        "PlanOS": _base_packet("PlanOS", lineage, wd, wa["wa_state_digest"], plan["plan_state_digest"]),
        "Governance": _base_packet("Governance", lineage, wd, plan["plan_state_digest"], act["step_authorization_digest"]),
        "ActOS": _base_packet("ActOS", lineage, wd, act["step_authorization_digest"], act["act_state_digest"]),
        "ObserveOS": _base_packet("ObserveOS", lineage, wd, act["act_state_digest"], observe["evidence_packet_digest"]),
        "VerifyOS": _base_packet("VerifyOS", lineage, wd, observe["evidence_packet_digest"], verify["verification_evidence_digest"]),
        "LearnOS": _base_packet("LearnOS", lineage, wd, verify["verification_evidence_digest"], learn["learning_delta_digest"]),
    }
    packets["BeliefOS"].update({"native_state_digest": artifacts["BeliefOSState"]["belief_gerbe_state_digest"], "native_receipt_digest": belief["belief_gerbe_receipt_digest"], "belief_route": belief["route"]})
    packets["DecisionOS"].update({"native_state_digest": wa["wa_state_digest"], "source_belief_receipt_digest": decision["source_belief_receipt_digest"], "decision_state_digest": decision["decision_state_digest"], "plural_state_digest": plural["plural_state_digest"], "wa_state_digest": wa["wa_state_digest"], "selected_option_id": decision["selected_option_id"], "wa_route": wa["route"]})
    packets["PlanOS"].update({"native_state_digest": plan["plan_state_digest"], "source_wa_state_digest": plan["source_wa_state_digest"], "source_decision_basis_digest": plan["source_decision_basis_digest"]})
    packets["Governance"].update({"cross_cutting": True, "single_stage": False, "act_admitted": True, "step_authorization_digest": act["step_authorization_digest"], "host_license_digest": act["host_license_digest"]})
    packets["ActOS"].update({"native_state_digest": act["act_state_digest"], "governance_decision_digest": act["step_authorization_digest"], "external_authority_receipt_digest": act["host_license_digest"], "actual_intervention_appended": True})
    packets["ObserveOS"].update({"native_state_digest": observe["observe_state_digest"], "source_act_state_digest": observe["source_act_state_digest"], "observation_only": True, "verification_complete": False})
    packets["VerifyOS"].update({"native_state_digest": verify["verify_state_digest"], "source_observe_state_digest": verify["source_observe_state_digest"], "observation_digest": observe["evidence_packet_digest"], "verification_complete": True, "truth_claim": False})
    packets["LearnOS"].update({"native_state_digest": learn["learn_state_digest"], "source_verify_state_digest": learn["source_verify_state_digest"], "verification_digest": verify["verification_evidence_digest"], "future_only": True, "past_overwrite": False})
    if set(packets) != set(OS_KINDS):
        raise ValueError("native_full_cycle_packet_inventory_invalid")
    return build_qi_world_os_interface_receipt(
        world_projection=world,
        qi_process_receipt=qi_receipt,
        os_packets=packets,
    )


def build_native_full_cycle_receipt(root: Path) -> dict[str, Any]:
    artifacts = _build_native_artifacts(root)
    source_errors = _native_validation_errors(artifacts)
    if source_errors:
        raise ValueError("native_full_cycle_source_invalid:" + ";".join(source_errors))
    lineage = _process_lineage_digest(artifacts)
    world = _build_world_projection(artifacts)
    qi_receipt = _build_qi_receipt(artifacts)
    interface = _build_interface_receipt(artifacts, world, qi_receipt, lineage)
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "native_artifacts": deepcopy(artifacts),
        "process_lineage_digest": lineage,
        "world_projection_digest": world["world_projection_digest"],
        "qi_world_os_interface_receipt": interface,
        "full_cycle_non_authority": deepcopy(FULL_CYCLE_NON_AUTHORITY),
        "native_full_cycle_receipt_digest": "",
    }
    receipt["native_full_cycle_receipt_digest"] = full_cycle_receipt_digest(receipt)
    errors = validate_native_full_cycle_receipt(receipt)
    if errors:
        raise ValueError("native_full_cycle_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_native_full_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("native_full_cycle_version_invalid")
        if receipt.get("native_full_cycle_receipt_digest") != full_cycle_receipt_digest(receipt):
            errors.append("native_full_cycle_digest_invalid")
        artifacts = dict(receipt.get("native_artifacts", {}))
        errors.extend(_native_validation_errors(artifacts))
        expected_inventory = {"BeliefOSState", "BeliefOSReceipt", "DecisionOS", "DecisionOSPlural", "DecisionOSWa", "PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS"}
        if set(artifacts) != expected_inventory:
            errors.append("native_full_cycle_artifact_inventory_invalid")
            return errors
        belief_state = artifacts["BeliefOSState"]
        belief = artifacts["BeliefOSReceipt"]
        decision = artifacts["DecisionOS"]
        plural = artifacts["DecisionOSPlural"]
        wa = artifacts["DecisionOSWa"]
        plan = artifacts["PlanOS"]
        act = artifacts["ActOS"]
        observe = artifacts["ObserveOS"]
        verify = artifacts["VerifyOS"]
        learn = artifacts["LearnOS"]
        lineage_ids = {belief_state.get("lineage_id"), belief.get("lineage_id"), decision.get("lineage_id"), plural.get("lineage_id"), wa.get("lineage_id"), plan.get("lineage_id"), act.get("lineage_id"), observe.get("lineage_id"), verify.get("lineage_id"), learn.get("lineage_id")}
        if len(lineage_ids) != 1:
            errors.append("native_full_cycle_lineage_mismatch")
        bindings = [
            (decision.get("source_belief_receipt_digest"), belief.get("belief_gerbe_receipt_digest"), "native_full_cycle_decision_belief_mismatch"),
            (plural.get("source_decision_state_digest"), decision.get("decision_state_digest"), "native_full_cycle_plural_decision_mismatch"),
            (plural.get("source_decision_basis_digest"), decision.get("decision_basis_digest"), "native_full_cycle_plural_decision_basis_mismatch"),
            (wa.get("source_plural_state_digest"), plural.get("plural_state_digest"), "native_full_cycle_wa_plural_mismatch"),
            (wa.get("source_decision_basis_digest"), decision.get("decision_basis_digest"), "native_full_cycle_wa_decision_basis_mismatch"),
            (plan.get("source_wa_state_digest"), wa.get("wa_state_digest"), "native_full_cycle_plan_wa_mismatch"),
            (plan.get("source_decision_basis_digest"), decision.get("decision_basis_digest"), "native_full_cycle_plan_decision_basis_mismatch"),
            (act.get("source_plan_state_digest"), plan.get("plan_state_digest"), "native_full_cycle_act_plan_mismatch"),
            (act.get("source_wa_basis_digest"), wa.get("wa_basis_digest"), "native_full_cycle_act_wa_basis_mismatch"),
            (observe.get("source_act_state_digest"), act.get("act_state_digest"), "native_full_cycle_observe_act_mismatch"),
            (verify.get("source_observe_state_digest"), observe.get("observe_state_digest"), "native_full_cycle_verify_observe_mismatch"),
            (learn.get("source_verify_state_digest"), verify.get("verify_state_digest"), "native_full_cycle_learn_verify_mismatch"),
        ]
        errors.extend(message for actual, expected, message in bindings if actual != expected)
        mission_contracts = {decision.get("mission_contract_digest"), plural.get("mission_contract_digest"), wa.get("mission_contract_digest"), plan.get("mission_contract_digest"), act.get("mission_contract_digest"), observe.get("mission_contract_digest"), verify.get("mission_contract_digest"), learn.get("mission_contract_digest")}
        if len(mission_contracts) != 1:
            errors.append("native_full_cycle_mission_contract_mismatch")
        expected_lineage = _process_lineage_digest(artifacts)
        if receipt.get("process_lineage_digest") != expected_lineage:
            errors.append("native_full_cycle_process_lineage_digest_mismatch")
        interface = dict(receipt.get("qi_world_os_interface_receipt", {}))
        errors.extend(f"interface:{error}" for error in validate_qi_world_os_interface_receipt(interface))
        if interface.get("process_lineage_digest") != expected_lineage:
            errors.append("native_full_cycle_interface_lineage_mismatch")
        if interface.get("world_projection_digest") != receipt.get("world_projection_digest"):
            errors.append("native_full_cycle_world_projection_mismatch")
        packets = dict(interface.get("os_packets", {}))
        packet_outputs = {
            "BeliefOS": belief.get("belief_gerbe_receipt_digest"),
            "DecisionOS": wa.get("wa_state_digest"),
            "PlanOS": plan.get("plan_state_digest"),
            "ActOS": act.get("act_state_digest"),
            "ObserveOS": observe.get("evidence_packet_digest"),
            "VerifyOS": verify.get("verification_evidence_digest"),
            "LearnOS": learn.get("learning_delta_digest"),
        }
        errors.extend(f"native_full_cycle_{name.lower()}_packet_mismatch" for name, expected in packet_outputs.items() if packets.get(name, {}).get("output_digest") != expected)
        if dict(receipt.get("full_cycle_non_authority", {})) != FULL_CYCLE_NON_AUTHORITY:
            errors.append("native_full_cycle_non_authority_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors

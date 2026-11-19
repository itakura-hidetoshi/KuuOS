"""Lean→Python v0.43: read-only contextual middle-way semantic bridge.

Two independently existing source auditors are re-run with ONE supplied
native-v1.3 state inventory and exactly the same original PlanOS root:
  BeliefOS→DecisionOS→PluralOS→WaOS→PlanOS  (v0.42)
  PlanOS→ActOS→ObserveOS→VerifyOS→LearnOS   (v0.38)

This implementation computes selected local evidence and a typed Plan seam;
it does NOT construct the Lean LocalSimulation.preservation witness, prove
whole-language semantic refinement, authenticate a WORLD/issuer or issue
execution, CodeAI, MemoryOS, DecisionOS, PlanOS or Git authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_belief_gerbe_store_origin_v0_42 import (
    SCOPED_COMPATIBLE as BELIEF_PLAN_PASS,
    _BELIEF_FILES,
    audit_native_belief_gerbe_store_origin,
)
from runtime.kuuos_lean_python_decision_store_origin_v0_41 import (
    _DECISION_FILES,
)
from runtime.kuuos_lean_python_plural_store_origin_v0_40 import (
    _PLURAL_FILES,
)
from runtime.kuuos_lean_python_wa_plan_store_compat_v0_39 import (
    _WA_FILES, _PLAN_FILES, _trusted_store_root,
)
from runtime.kuuos_lean_python_five_store_chain_compat_v0_38 import (
    SCOPED_COMPATIBLE as PLAN_LEARN_PASS,
    _STORE_FILES as FIVE_STORE_FILES,
    audit_native_five_store_chain_compatibility,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_middle_way_semantic_bridge_v0_43"
SOURCE_PARENT = "e9cd8a9c314fd78ee5038e79fe0d60fa3632a1f7"
SCOPED_COMPATIBLE = "SCOPED_MIDDLE_WAY_SEMANTIC_OPERATIONAL"
LOCALLY_CHECKED = "LOCALLY_CHECKED"
LOCAL_SCOPES = (
    "BeliefOSState", "DecisionOS", "DecisionOSPlural", "DecisionOSWa",
    "PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS",
)
REQUIRED_STATES = (
    "BeliefOSState", "BeliefOSReceipt", "DecisionOS", "DecisionOSPlural",
    "DecisionOSWa", "PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS",
)
ROOT_SUFFIXES = {
    "BeliefOSState": ("belief",),
    "DecisionOS": ("decision",),
    "DecisionOSPlural": ("plural",),
    "DecisionOSWa": ("wa",),
    "PlanOS": ("plan",),
    "ActOS": ("act",),
    "ObserveOS": ("downstream", "observe"),
    "VerifyOS": ("downstream", "verify"),
    "LearnOS": ("downstream", "learn"),
}
ALL_FILES = {
    "BeliefOSState": _BELIEF_FILES,
    "DecisionOS": _DECISION_FILES,
    "DecisionOSPlural": _PLURAL_FILES,
    "DecisionOSWa": _WA_FILES,
    "PlanOS": _PLAN_FILES,
    **{name: FIVE_STORE_FILES[name] for name in
       ("ActOS", "ObserveOS", "VerifyOS", "LearnOS")},
}
HISTORIC_EDGES = (
    "BeliefOSReceipt->DecisionOS",
    "DecisionOS->DecisionOSPlural",
    "DecisionOSPlural->DecisionOSWa",
    "DecisionOSWa->PlanOS",
    "PlanOS->ActOS",
    "ActOS->ObserveOS",
    "ObserveOS->VerifyOS",
    "VerifyOS->LearnOS",
)
# The mapping names a conditional Lean theorem and an observed Python
# predicate; this naming layer is NOT itself a formal refinement proof.
INTERPRETED_LEAN_SOURCES = (
    ("BeliefOS", "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean",
     "surfaceHolonomy_strict"),
    ("DecisionOS", "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean",
     "decisionHistory_recovered_count_aligned"),
    ("DecisionOSPlural", "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean",
     "pluralDecisionHistory_recovery_aligned"),
    ("PlanOS", "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean",
     "plan_does_not_execute"),
    ("VerifyOS", "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean",
     "middle_way_verification_is_not_plan_or_execution"),
    ("CodeAI", "formal/KUOS/CodeAI/VersionBoundRepairMemoryV0_1.lean",
     "sourceCommitMismatchBlocksTransfer"),
)
UNRESOLVED = (
    "FORMAL_LOCAL_SIMULATION_WITNESS_NOT_CONSTRUCTED_FOR_PYTHON",
    "UNPROVED_UNIVERSAL_LEAN_PYTHON_REFINEMENT",
    "UNPROVED_GLOBAL_DESCENT_AND_ATOMIC_SNAPSHOT",
    "UNPROVED_COMMON_CAUSAL_CLOCK",
    "EXTERNAL_ISSUER_AUTHENTICITY_UNVERIFIED",
    "ACTOS_ACTUAL_NUMERIC_WITNESSES_UNPROVED",
    "WORLD_IDENTITY_NOT_EXTERNALLY_CERTIFIED",
)
ADVICE_ON_SCOPED_CHECK = (
    ("CodeAI", "TEST_REQUIRED_NO_AUTO_MERGE"),
    ("MemoryOS", "APPEND_ONLY_EVIDENCE_PROPOSAL_NOT_WRITTEN"),
    ("DecisionOS", "SCOPED_ADVISORY_NOT_TRUTH"),
    ("PlanOS", "REVIEW_ONLY_NOT_EXECUTION"),
)
ADVICE_ON_HOLD = (
    ("CodeAI", "HOLD_TEST_REQUIRED"),
    ("MemoryOS", "PRESERVE_MISSING_AND_CONFLICT_NO_WRITE"),
    ("DecisionOS", "HOLD"),
    ("PlanOS", "HOLD"),
)


@dataclass(frozen=True)
class MiddleWaySemanticAudit:
    status: str
    issues: tuple[str, ...] = ()
    local_evidence_statuses: tuple[tuple[str, str], ...] = ()
    interpreted_lean_sources: tuple[tuple[str, str, str], ...] = INTERPRETED_LEAN_SOURCES
    historical_edges: tuple[str, ...] = HISTORIC_EDGES
    original_source_file_paths: tuple[str, ...] = ()
    original_store_root: str | None = None
    context_lineage: str | None = None
    context_mission_digest: str | None = None
    plan_seam_final_sha256: str | None = None
    checked_local_history_count: int = 0
    source_time_relation: str | None = None
    unresolved_obstructions: tuple[str, ...] = UNRESOLVED
    read_only_consumer_advice: tuple[tuple[str, str], ...] = ADVICE_ON_HOLD
    source_blobs_pinned_by_static_checker: bool = False
    provenance_is_externally_authenticated: bool = False
    local_formal_simulation_witness_constructed: bool = False
    universal_lean_python_semantic_refinement_proved: bool = False
    global_descent_proved: bool = False
    globally_atomic_snapshot_proved: bool = False
    common_causal_clock_proved: bool = False
    codeai_repair_executed: bool = False
    memoryos_write_performed: bool = False
    decisionos_selection_performed: bool = False
    planos_synthesis_performed: bool = False
    host_action_performed: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    institutional_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    original_store_mutated: bool = False


def combine_evidence(a: str, b: str) -> str:
    """Exact Python table corresponding to the v0.43 Lean constructors."""
    allowed = {LOCALLY_CHECKED, NO_DATA, BLOCKED}
    if type(a) is not str or type(b) is not str or a not in allowed or b not in allowed:
        return BLOCKED
    if a == BLOCKED or b == BLOCKED:
        return BLOCKED
    if a == NO_DATA or b == NO_DATA:
        return NO_DATA
    return LOCALLY_CHECKED


def _hold(status: str, *issues: str) -> MiddleWaySemanticAudit:
    return MiddleWaySemanticAudit(
        status=status, issues=tuple(dict.fromkeys(issues)),
    )


def _source_root(root: Any) -> Path:
    if type(root) is not str and type(root) is not type(Path()):
        raise TypeError("native_root:concrete_path_required")
    return _trusted_store_root(root)


def audit_native_middle_way_semantics(
    native_states: Any,
    wa_replan_activation_receipt: Any,
    plan_phase_activation_receipt: Any,
    original_cycle_root: Any,
) -> MiddleWaySemanticAudit:
    """Selected native-v1.3 read-only *operational* semantic correspondence.

    Admission is a local observation about this fixed source inventory:
    no Lean proof is manufactured from a Python test, no World is declared
    globally identical, and no OS permission/selection/repair is performed.
    """
    missing = (
        ("native_states", native_states),
        ("wa_replan_receipt", wa_replan_activation_receipt),
        ("plan_phase_receipt", plan_phase_activation_receipt),
        ("original_cycle_root", original_cycle_root),
    )
    absent = tuple(n + ":missing" for n, v in missing if v is None)
    if absent:
        return _hold(NO_DATA, *absent)
    if type(native_states) is not dict:
        return _hold(BLOCKED, "middle_way:plain_native_inventory_required")
    unknown = set(native_states) - set(REQUIRED_STATES)
    if unknown:
        return _hold(BLOCKED, "middle_way:unknown_native_os")
    absent = tuple(n + ":missing" for n in REQUIRED_STATES
                   if native_states.get(n) is None)
    if absent:
        return _hold(NO_DATA, *absent)

    try:
        states = {key: _packet(native_states[key], key)
                  for key in REQUIRED_STATES}
        wa_receipt = _packet(wa_replan_activation_receipt, "wa_replan_receipt")
        plan_receipt = _packet(plan_phase_activation_receipt,
                               "plan_phase_receipt")
        root = _source_root(original_cycle_root)
        roots = {
            name: _trusted_store_root(root.joinpath(*ROOT_SUFFIXES[name]))
            for name in LOCAL_SCOPES
        }
        if len(set(roots.values())) != len(roots):
            return _hold(BLOCKED, "middle_way:original_stores_not_distinct")
        # The input file family is captured before either *original* audit
        # executes. A second observation detects a change but does not
        # give atomicity across five or nine independent stores.
        before = {
            name: _store_files(roots[name], ALL_FILES[name])
            for name in LOCAL_SCOPES
        }
    except FileNotFoundError:
        return _hold(NO_DATA, "middle_way:original_store_history_missing")
    except (OSError, TypeError, ValueError, RuntimeError, UnicodeError,
            RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "middle_way:invalid_native_source:"
                     + type(exc).__name__)

    upstream = audit_native_belief_gerbe_store_origin(
        belief_state=states["BeliefOSState"],
        belief_receipt=states["BeliefOSReceipt"],
        decision_state=states["DecisionOS"],
        plural_state=states["DecisionOSPlural"],
        wa_state=states["DecisionOSWa"],
        plan_state=states["PlanOS"],
        replan_activation_receipt=wa_receipt,
        original_belief_store_root=roots["BeliefOSState"],
        original_decision_store_root=roots["DecisionOS"],
        original_plural_store_root=roots["DecisionOSPlural"],
        original_wa_store_root=roots["DecisionOSWa"],
        original_plan_store_root=roots["PlanOS"],
    )
    downstream = audit_native_five_store_chain_compatibility(
        states={name: states[name] for name in
                ("PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS")},
        plan_activation_receipt=plan_receipt,
        original_store_roots={name: roots[name] for name in
                              ("PlanOS", "ActOS", "ObserveOS",
                               "VerifyOS", "LearnOS")},
    )

    statuses = (
        ("BeliefOS->PlanOS", LOCALLY_CHECKED
         if upstream.status == BELIEF_PLAN_PASS else
         BLOCKED if upstream.status == BLOCKED else NO_DATA),
        ("PlanOS->LearnOS", LOCALLY_CHECKED
         if downstream.status == PLAN_LEARN_PASS else
         BLOCKED if downstream.status == BLOCKED else NO_DATA),
    )
    issues: list[str] = []
    for name, audit in (("BeliefOS->PlanOS", upstream),
                        ("PlanOS->LearnOS", downstream)):
        if audit.status == BLOCKED:
            issues.extend(name + ":" + x for x in audit.issues)
            if not audit.issues:
                issues.append(name + ":blocked")
        elif (audit.status != BELIEF_PLAN_PASS if name == "BeliefOS->PlanOS"
              else audit.status != PLAN_LEARN_PASS):
            issues.append(name + ":unconfirmed:" + audit.status)
            issues.extend(name + ":" + x for x in audit.issues)

    plan_sha = _fingerprint(states["PlanOS"])
    expected_plan_sha = dict(downstream.final_native_state_digests).get("PlanOS")
    seam_status = LOCALLY_CHECKED
    if upstream.status != BELIEF_PLAN_PASS or downstream.status != PLAN_LEARN_PASS:
        seam_status = NO_DATA
    elif (expected_plan_sha != plan_sha or
          not upstream.prior_decision_plural_wa_plan_origins_checked or
          not downstream.five_stores_individually_replayed or
          not downstream.four_original_typed_edges_checked or
          not downstream.store_bytes_stable_during_audit):
        seam_status = BLOCKED
        issues.append("middle_way:PlanOS_semantic_seam_incompatible")
    # Contexts are derived from original snapshots, not caller-provided
    # self-asserted status, inference of a universal World, or source labels.
    lineage = states["PlanOS"].get("lineage_id")
    mission = states["PlanOS"].get("mission_contract_digest")
    if type(lineage) is not str or not lineage or type(mission) is not str or not mission:
        seam_status = combine_evidence(seam_status, NO_DATA)
        issues.append("middle_way:context_key_unobserved")
    else:
        for name in LOCAL_SCOPES:
            packet = states[name]
            if packet.get("lineage_id") is None:
                seam_status = combine_evidence(seam_status, NO_DATA)
                issues.append("middle_way:" + name + ":lineage_missing")
            elif not _same(packet.get("lineage_id"), lineage):
                seam_status = BLOCKED
                issues.append("middle_way:" + name + ":lineage_mismatch")
            if name not in ("BeliefOSState",) and (
                packet.get("mission_contract_digest") is None
            ):
                seam_status = combine_evidence(seam_status, NO_DATA)
                issues.append("middle_way:" + name + ":mission_contract_missing")
            elif name not in ("BeliefOSState",) and (
                not _same(packet.get("mission_contract_digest"), mission)
            ):
                seam_status = BLOCKED
                issues.append("middle_way:" + name + ":mission_contract_mismatch")
    statuses += (("PlanOS:typed-contextual-seam", seam_status),)
    overall = combine_evidence(combine_evidence(
        statuses[0][1], statuses[1][1]), seam_status)

    after = None
    try:
        after = {name: _store_files(roots[name], ALL_FILES[name])
                 for name in LOCAL_SCOPES}
        if before != after:
            overall = BLOCKED
            issues.append("middle_way:original_store_bytes_changed")
    except FileNotFoundError:
        overall = combine_evidence(overall, NO_DATA)
        issues.append("middle_way:original_store_disappeared")
    except (OSError, TypeError, ValueError, RuntimeError, UnicodeError,
            RecursionError, OverflowError) as exc:
        overall = BLOCKED
        issues.append("middle_way:second_observation_invalid:"
                      + type(exc).__name__)

    status = SCOPED_COMPATIBLE if overall == LOCALLY_CHECKED else overall
    return MiddleWaySemanticAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        local_evidence_statuses=statuses,
        checked_local_history_count=9 if status == SCOPED_COMPATIBLE else 0,
        original_source_file_paths=tuple(
            name + "." + filename for name in LOCAL_SCOPES
            for filename in ALL_FILES[name]
        ),
        original_store_root=str(root),
        context_lineage=lineage if type(lineage) is str else None,
        context_mission_digest=mission if type(mission) is str else None,
        plan_seam_final_sha256=plan_sha,
        source_time_relation=upstream.cross_source_time_relation,
        read_only_consumer_advice=(
            ADVICE_ON_SCOPED_CHECK if status == SCOPED_COMPATIBLE
            else ADVICE_ON_HOLD
        ),
        # Static source checker runs separately; this function does not
        # pretend that its own invocation proved current Git/Lean sources.
        source_blobs_pinned_by_static_checker=False,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE",
    "LOCALLY_CHECKED", "NO_DATA", "BLOCKED", "REQUIRED_STATES",
    "LOCAL_SCOPES", "ROOT_SUFFIXES", "INTERPRETED_LEAN_SOURCES",
    "UNRESOLVED", "HISTORIC_EDGES", "MiddleWaySemanticAudit",
    "combine_evidence", "audit_native_middle_way_semantics",
)

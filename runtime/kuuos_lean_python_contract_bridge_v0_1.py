"""Read-only, fail-closed Python projections of KuuOS Lean theorem boundaries.

This module does NOT translate Lean proofs to a proof of Python correctness. A
successful result means the *observed Python payload* passed named runtime
checks. Lean proofs apply to their explicitly quantified, well-formed objects;
no new authority, effect, CI attestation, or proof certificate is created here.

Source revision: itakura-hidetoshi/KuuOS main at SOURCE_COMMIT. Keep proof
source, runtime source, and CI receipts distinct when rebasing.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Mapping

SOURCE_REPOSITORY = "itakura-hidetoshi/KuuOS"
SOURCE_COMMIT = "1a03908757fd0fcdb1acd5199b51dffd5208c3f8"
VERSION = "kuuos_lean_python_contract_bridge_v0_1"

PASSED = "RUNTIME_CHECK_PASSED"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


@dataclass(frozen=True)
class CoreContract:
    os_name: str
    stem: str
    lean_source: str
    phase_theorem: str
    event_theorem: str
    authority_theorem: str
    phases: tuple[str, ...]
    wraps: bool = False

    @property
    def runtime_kernel(self) -> str:
        return f"runtime.kuuos_{self.stem}_os_kernel_v0_1"

    @property
    def runtime_types(self) -> str:
        return f"runtime.kuuos_{self.stem}_os_types_v0_1"

    @property
    def digest_key(self) -> str:
        return f"{self.stem}_state_digest"

    @property
    def event_key(self) -> str:
        return f"{self.stem}_event_digest"


CORE_CONTRACTS: dict[str, CoreContract] = {
    "BeliefOS": CoreContract(
        "BeliefOS", "belief", "formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean",
        "beliefTransition_phase_is_ordered", "beliefTransition_event_advances",
        "beliefCommit_ne_truthAuthority",
        ("propose", "contextualize", "trace", "weigh", "challenge", "qi_condition",
         "two_truths_check", "middle_way_gate", "commit"), True,
    ),
    "DecisionOS": CoreContract(
        "DecisionOS", "decision", "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean",
        "decisionPhase_next_deterministic", "decisionEventIndex_strict",
        "decision_does_not_execute",
        ("frame", "generate", "constrain", "evaluate", "challenge", "qi_condition",
         "two_truths_check", "middle_way_gate", "decide", "commit"),
    ),
    "PlanOS": CoreContract(
        "PlanOS", "plan", "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean",
        "planPhase_next_deterministic", "planEventIndex_strict",
        "plan_does_not_execute",
        ("bind", "decompose", "order", "resource", "guard", "checkpoint", "verify", "commit"),
    ),
    "ActOS": CoreContract(
        "ActOS", "act", "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean",
        "actPhase_next_deterministic", "actEventIndex_strict",
        "successfulReceipt_is_not_truth_authority",
        ("bind", "select", "authorize", "project", "invoke", "verify", "commit"),
    ),
    "ObserveOS": CoreContract(
        "ObserveOS", "observe", "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean",
        "observePhase_next_deterministic", "observeEventIndex_strict",
        "observeOS_grants_no_truth_or_verification_authority",
        ("bind", "scope", "collect", "trace", "assess", "compare", "commit"),
    ),
    "VerifyOS": CoreContract(
        "VerifyOS", "verify", "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean",
        "verifyPhase_next_deterministic", "verifyEventIndex_strict",
        "verification_never_grants_truth",
        ("bind", "criterion", "challenge", "corroborate", "adjudicate", "commit"),
    ),
    "LearnOS": CoreContract(
        "LearnOS", "learn", "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean",
        "learnPhase_next_deterministic", "learnEventIndex_strict",
        "learning_delta_is_inactive_until_replan",
        ("bind", "abstract", "challenge", "delta", "middle_way_gate", "commit"),
    ),
}

# These are bounded additional OS projections, not replacements for their
# existing specialized runtime kernels. They have their own entry points below.
ADDITIONAL_PROOF_LINKS = {
    "MemoryOS": (
        "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean",
        "memory_cannot_discharge_blocker",
        "runtime.kuuos_memoryos_qi_world_blocker_integration_v0_35",
    ),
    "CodeAI": (
        "formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean",
        "highScoreCannotOverrideInadmissible",
        "runtime.kuuos_codeai_evidence_weighted_selection_abstention_v0_1",
    ),
    "WORLD": (
        "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean",
        "",  # Source-level mapping only; no standalone WORLD runtime checker here.
        "runtime.kuuos_authorized_atomic_world_commit_v0_34",
    ),
}


@dataclass(frozen=True)
class RuntimeAudit:
    os_name: str
    status: str
    issues: tuple[str, ...]
    lean_source: str
    theorem_names: tuple[str, ...]
    runtime_source: str
    source_commit: str = SOURCE_COMMIT
    scope: str = "payload-level Python runtime projection; not Lean proof of Python"

    @property
    def passed_runtime_checks(self) -> bool:
        """For reporting only; this never grants execution or commit authority."""
        return self.status == PASSED


def _audit(contract: CoreContract, issues: list[str], missing: list[str], *, scope: str,
           transition: bool = False) -> RuntimeAudit:
    outcome = BLOCKED if issues else (NO_DATA if missing else PASSED)
    return RuntimeAudit(
        os_name=contract.os_name,
        status=outcome,
        issues=tuple(issues + missing),
        lean_source=contract.lean_source,
        theorem_names=((contract.phase_theorem, contract.event_theorem) if transition
                       else (contract.authority_theorem,)),
        runtime_source=contract.runtime_kernel.replace(".", "/") + ".py",
        scope=scope,
    )


def _equal_expected_map(actual: Any, expected: Mapping[str, bool], name: str,
                        errors: list[str], missing: list[str]) -> None:
    if not isinstance(actual, Mapping):
        missing.append(f"{name}_not_provided")
        return
    for key, expected_value in expected.items():
        if key not in actual:
            missing.append(f"{name}.{key}_missing")
        elif type(actual[key]) is not bool or actual[key] is not expected_value:
            errors.append(f"{name}.{key}_violated")
    if name == "non_authority":
        # An extra positive authority claim must never be ignored merely
        # because the v0.1 registry does not name it.
        for key, value in actual.items():
            if key not in expected and (key.endswith("_granted") or key.endswith("_authority")):
                if value is not False:
                    errors.append(f"non_authority.{key}_unexpected_claim")


def audit_core_state(os_name: str, state: Any) -> RuntimeAudit:
    """Validate a real OS state with its own existing Python kernel and constraints.

    Failure and absent data remain distinct. This is read-only, has no host
    invocation, and NEVER promotes a payload to Lean-verified or truthful.
    """
    contract = CORE_CONTRACTS[os_name]
    errors: list[str] = []
    missing: list[str] = []
    if not isinstance(state, Mapping):
        return _audit(contract, errors, ["state_not_provided"], scope="state")
    try:
        types_module = import_module(contract.runtime_types)
        kernel = import_module(contract.runtime_kernel)
    except (ImportError, AttributeError) as exc:
        return _audit(contract, errors, [f"runtime_dependency_unavailable:{type(exc).__name__}"], scope="state")

    # The same phase alphabet must be used by the original code and this
    # source-pinned Lean projection. A drift is a bridge defect, not a proof.
    if tuple(getattr(types_module, "PHASES", ())) != contract.phases:
        errors.append("source_pinned_phase_alphabet_mismatch")
    if state.get("version") is None:
        missing.append("version_missing")
    elif state.get("version") != getattr(types_module, "STATE_VERSION", None):
        errors.append("state_version_mismatch")
    phase = state.get("current_phase")
    if phase is None:
        missing.append("current_phase_missing")
    elif phase not in contract.phases:
        errors.append("current_phase_invalid")
    _equal_expected_map(state.get("non_authority"), getattr(types_module, "NON_AUTHORITY_FLAGS", {}),
                        "non_authority", errors, missing)
    _equal_expected_map(state.get("boundary"), getattr(types_module, "REQUIRED_BOUNDARY", {}),
                        "boundary", errors, missing)

    validator = getattr(kernel, f"validate_{contract.stem}_state", None)
    if not callable(validator):
        missing.append("original_state_validator_unavailable")
    else:
        try:
            original_errors = validator(state)
        except (KeyError, ValueError, TypeError, AttributeError) as exc:
            errors.append(f"original_validator_raised:{type(exc).__name__}")
        else:
            if not isinstance(original_errors, (list, tuple)):
                errors.append("original_validator_contract_unexpected")
            else:
                errors.extend(f"original_validator:{issue}" for issue in original_errors)
    return _audit(contract, errors, missing, scope="existing kernel state validation and authority boundaries")


def _required(value: Mapping[str, Any], key: str, missing: list[str]) -> Any:
    if key not in value:
        missing.append(f"{key}_missing")
        return None
    return value[key]


def _natural(value: Any) -> bool:
    return type(value) is int and value >= 0


def audit_core_transition(os_name: str, before: Any, event: Any, result: Any) -> RuntimeAudit:
    """Independent *structural* check on a core OS transition receipt.

    This does not replace audit_core_state for the complete pre/post schemas.
    It deliberately refuses to infer truth/authority from a reported status.
    """
    contract = CORE_CONTRACTS[os_name]
    errors: list[str] = []
    missing: list[str] = []
    if not all(isinstance(x, Mapping) for x in (before, event, result)):
        return _audit(contract, [], ["transition_input_not_provided"], scope="transition", transition=True)
    after = _required(result, "state", missing)
    status = _required(result, "status", missing)
    if not isinstance(after, Mapping):
        missing.append("result_state_not_provided")
        return _audit(contract, errors, missing, scope="transition", transition=True)
    if status is not None and status not in ("APPLIED", "REPLAYED", "REJECTED"):
        errors.append("result_status_unknown")
    before_phase = _required(before, "current_phase", missing)
    after_phase = _required(after, "current_phase", missing)
    index = _required(before, "event_index", missing)
    next_index = _required(after, "event_index", missing)
    before_history = _required(before, "event_history", missing)
    after_history = _required(after, "event_history", missing)
    before_processed = _required(before, "processed_event_digests", missing)
    after_processed = _required(after, "processed_event_digests", missing)
    previous_digest = _required(before, contract.digest_key, missing)
    if before_phase is not None and before_phase not in contract.phases:
        errors.append("source_phase_outside_lean_alphabet")
    if after_phase is not None and after_phase not in contract.phases:
        errors.append("target_phase_outside_lean_alphabet")
    if index is not None and not _natural(index):
        errors.append("source_event_index_must_be_natural")
    if next_index is not None and not _natural(next_index):
        errors.append("target_event_index_must_be_natural")
    if not all(isinstance(x, list) for x in
               (before_history, after_history, before_processed, after_processed)):
        missing.append("append_only_history_not_provided")
    if not isinstance(previous_digest, str) or not previous_digest:
        missing.append("source_state_digest_not_provided")

    if status == "APPLIED" and before_phase in contract.phases:
        pos = contract.phases.index(before_phase)
        expected = (contract.phases[(pos + 1) % len(contract.phases)] if contract.wraps
                    else contract.phases[pos + 1] if pos + 1 < len(contract.phases) else None)
        if expected is None:
            errors.append("committed_phase_has_no_next_transition")
        else:
            for field in ("source_phase", "target_phase", "event_index", contract.event_key):
                _required(event, field, missing)
            if "source_phase" in event and "target_phase" in event:
                if event["source_phase"] != before_phase or event["target_phase"] != expected:
                    errors.append("lean_phase_order_violation")
            if "event_index" in event and _natural(index) and event["event_index"] != index + 1:
                errors.append("event_receipt_index_mismatch")
            if after_phase != expected:
                errors.append("result_phase_order_violation")
        if _natural(index) and _natural(next_index) and next_index != index + 1:
            errors.append("event_index_not_exactly_incremented")
        if isinstance(before_history, list) and isinstance(after_history, list):
            if after_history[: len(before_history)] != before_history or len(after_history) != len(before_history) + 1:
                errors.append("event_history_not_append_only")
        if isinstance(before_processed, list) and isinstance(after_processed, list):
            if after_processed[: len(before_processed)] != before_processed or len(after_processed) != len(before_processed) + 1:
                errors.append("processed_history_not_append_only")
            if event.get(contract.event_key) != (after_processed[-1] if after_processed else None):
                errors.append("appended_event_identity_mismatch")
        if previous_digest and after.get(f"predecessor_{contract.digest_key}") != previous_digest:
            errors.append("predecessor_digest_binding_mismatch")
    elif status in ("REPLAYED", "REJECTED"):
        if after != before:
            errors.append("non_applied_transition_changed_state")
    return _audit(contract, errors, missing, scope="structural transition projection; full state schemas separately required",
                  transition=True)


def codeai_candidate_eligible(source_classification: str, evidence_status: str) -> bool:
    """Exact predicate of Lean `Eligible`; a score can never override it.

    `allPassed` is the Lean constructor, not a test-run or proof claim.
    """
    return source_classification == "admissible" and evidence_status == "allPassed"


def memory_blocker_boundary_check(boundary: Any) -> RuntimeAudit:
    """Check v0.35's named boundary booleans without changing WORLD or MemoryOS.

    This accepts the Lean-side *projection* field names, not an arbitrary
    runtime snapshot; specialized original snapshot validation remains required.
    """
    source, theorem, runtime = ADDITIONAL_PROOF_LINKS["MemoryOS"]
    required = {
        "blockerStoredAsContext": True,
        "blockerReleasedByMemory": False,
        "missingEvidenceSilentlyRepaired": False,
        "worldProjectionReadOnly": True,
        "worldChangedByMemory": False,
        "retrievalCandidateOnly": True,
        "durableAppendClaimed": False,
    }
    errors: list[str] = []
    missing: list[str] = []
    _equal_expected_map(boundary, required, "boundary", errors, missing)
    return RuntimeAudit(
        "MemoryOS", BLOCKED if errors else NO_DATA if missing else PASSED,
        tuple(errors + missing), source, (theorem,), runtime.replace(".", "/") + ".py",
        scope="MemoryOS blocker projection; specialized snapshot validation not included",
    )


def codeai_selection_boundary_check(receipt: Any) -> RuntimeAudit:
    """Check a selection-only receipt's non-effect boundary, never execute repairs.

    Selection is admissible only with separately verified source/evidence;
    here we check the no-authority receipt flags, not external evidence itself.
    """
    source, theorem, runtime = ADDITIONAL_PROOF_LINKS["CodeAI"]
    required = {
        "test_execution_performed_by_kernel": False,
        "repair_executed": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "verification_authority_granted": False,
        "repair_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "score_treated_as_probability": False,
        "score_treated_as_correctness_proof": False,
        "selection_treated_as_correctness_proof": False,
        "abstention_treated_as_rejection": False,
    }
    errors: list[str] = []
    missing: list[str] = []
    _equal_expected_map(receipt, required, "receipt", errors, missing)
    return RuntimeAudit(
        "CodeAI", BLOCKED if errors else NO_DATA if missing else PASSED,
        tuple(errors + missing), source,
        ("Receipt.WellFormed.downstreamAuthorityRemainsSeparate", "Receipt.WellFormed.effectBoundary"),
        runtime.replace(".", "/") + ".py",
        scope="CodeAI selection receipt boundary; not candidate correctness or CI attestation",
    )


__all__ = [
    "SOURCE_REPOSITORY", "SOURCE_COMMIT", "VERSION", "PASSED", "BLOCKED", "NO_DATA",
    "CORE_CONTRACTS", "ADDITIONAL_PROOF_LINKS", "RuntimeAudit", "audit_core_state",
    "audit_core_transition", "codeai_candidate_eligible", "memory_blocker_boundary_check",
    "codeai_selection_boundary_check",
]

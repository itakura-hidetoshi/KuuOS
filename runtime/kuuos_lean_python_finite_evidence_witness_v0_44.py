"""v0.44: finite, source-scoped Lean/Python middle-way evidence model.

The finite string table has an explicit formal counterpart at
KUOS.Architecture.LeanPythonFiniteEvidenceWitnessV0_44. It is NOT a
Lean proof of CPython or a whole-OS semantic refinement. Compare the
actual original v0.43 Python combine_evidence with an independently
implemented table over all 9 pairs and all 27 two-stage traces.

Optionally re-run the actual v0.43 nine-OS read-only native audit and
bind the finite table evidence to its context. Read-only advisory only.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

from runtime import kuuos_lean_python_middle_way_semantic_bridge_v0_43 as original

VERSION = "kuuos_lean_python_finite_evidence_witness_v0_44"
SOURCE_PARENT = "e14b193e8b4f735008c3d97fb6bca61671213130"
SCOPED_TABLE_MATCH = "SCOPED_FINITE_PYTHON_EVIDENCE_TABLE_MATCH"
SCOPED_NATIVE_COMPATIBLE = "SCOPED_FINITE_MIDDLE_WAY_NATIVE_INSTANCE_COMPATIBLE"
LOCALLY_CHECKED = original.LOCALLY_CHECKED
NO_DATA = original.NO_DATA
BLOCKED = original.BLOCKED
STATUSES = (NO_DATA, BLOCKED, LOCALLY_CHECKED)
FORMAL_MODEL_FILE = (
    "formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean"
)
ADVISORY_CONSUMERS = original.ADVICE_ON_SCOPED_CHECK
HOLD_CONSUMERS = original.ADVICE_ON_HOLD
UNRESOLVED = original.UNRESOLVED + (
    "ACTUAL_PYTHON_EXECUTION_NOT_FORMALLY_REFINED_FROM_LEAN",
    "LEAN_MODEL_AXIOM_AUDIT_MUST_USE_INDEPENDENT_CI",
    "NATIVE_RUNTIME_HAS_NO_CERTIFIED_PYTHON_OPERATIONAL_SEMANTICS",
)


@dataclass(frozen=True)
class FiniteEvidenceWitnessAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_python_pair_cases_checked: int = 0
    original_python_two_stage_cases_checked: int = 0
    original_python_invalid_tokens_checked: int = 0
    finite_table_locally_checked: bool = False
    original_native_nine_store_audit_checked: bool = False
    original_native_status: str | None = None
    original_native_evidence_statuses: tuple[tuple[str, str], ...] = ()
    declared_context_key: tuple[tuple[str, str], ...] = ()
    original_source_head: str = SOURCE_PARENT
    lean_finite_model_source: str = FORMAL_MODEL_FILE
    read_only_consumer_advice: tuple[tuple[str, str], ...] = HOLD_CONSUMERS
    remaining_obstructions: tuple[str, ...] = UNRESOLVED
    # Source-check and actual pinned Lean CI are separate operations.
    lean_model_proof_verified_by_this_python_process: bool = False
    lean_to_cpython_interpreter_refinement_proved: bool = False
    whole_os_lean_python_semantics_proved: bool = False
    global_descent_proved: bool = False
    external_source_authenticated: bool = False
    common_causal_clock_proved: bool = False
    atomic_nine_store_snapshot_proved: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_write_performed: bool = False
    original_store_mutated: bool = False


def _independent_string_model(left: Any, right: Any) -> str:
    """Independent three-label string expression matching the Lean model.

    Exact built-in str only; non-string Python data is outside the Lean
    String model, and is locally refused rather than silently coerced.
    """
    if type(left) is not str or type(right) is not str:
        return BLOCKED
    if left not in STATUSES or right not in STATUSES:
        return BLOCKED
    if left == BLOCKED or right == BLOCKED:
        return BLOCKED
    if left == NO_DATA or right == NO_DATA:
        return NO_DATA
    if left == LOCALLY_CHECKED and right == LOCALLY_CHECKED:
        return LOCALLY_CHECKED
    return BLOCKED


def _audit_actual_python_table() -> tuple[tuple[str, ...], int, int, int]:
    failures: list[str] = []
    pair_count = 0
    triple_count = 0
    invalid_count = 0
    for first, second in product(STATUSES, repeat=2):
        pair_count += 1
        expected = _independent_string_model(first, second)
        try:
            observed = original.combine_evidence(first, second)
        except Exception as exc:
            failures.append("pair:runtime_exception:" + type(exc).__name__)
        else:
            if type(observed) is not str or observed != expected:
                failures.append("pair:incorrect:" + first + ":" + second)

    for first, second, third in product(STATUSES, repeat=3):
        triple_count += 1
        expected = _independent_string_model(
            _independent_string_model(first, second), third,
        )
        try:
            left_pair = original.combine_evidence(first, second)
            observed = original.combine_evidence(left_pair, third)
        except Exception as exc:
            failures.append("triple:runtime_exception:" + type(exc).__name__)
        else:
            if type(observed) is not str or observed != expected:
                failures.append("triple:incorrect:" + first + ":" + second
                                + ":" + third)

    # Check all three partner statuses, including NO_DATA: invalid raw
    # strings cannot be hidden behind a missing-evidence shortcut.
    # The Lean theorems model Strings; other Python types are Python-only
    # fail-closed checks and are not alleged to be Lean terms.
    for token in ("PASS", "CHECKED", "", "blocked", None, False, 0, 1.0):
        for partner in STATUSES:
            for left, right in ((token, partner), (partner, token)):
                invalid_count += 1
                try:
                    result = original.combine_evidence(left, right)
                except Exception as exc:
                    failures.append("invalid:runtime_exception:"
                                    + type(exc).__name__)
                else:
                    if type(result) is not str or result != BLOCKED:
                        failures.append("invalid:unexpected_acceptance:"
                                        + type(token).__name__)
    return tuple(dict.fromkeys(failures)), pair_count, triple_count, invalid_count


def audit_finite_status_table() -> FiniteEvidenceWitnessAudit:
    """Exhaustively inspect selected original Python function behavior."""
    problems, pairs, triples, invalid = _audit_actual_python_table()
    passed = not problems
    return FiniteEvidenceWitnessAudit(
        status=SCOPED_TABLE_MATCH if passed else BLOCKED,
        issues=problems,
        original_python_pair_cases_checked=pairs,
        original_python_two_stage_cases_checked=triples,
        original_python_invalid_tokens_checked=invalid,
        finite_table_locally_checked=passed,
        read_only_consumer_advice=(
            ADVISORY_CONSUMERS if passed else HOLD_CONSUMERS
        ),
    )


def audit_native_finite_evidence_instance(
    native_states: Any,
    wa_replan_activation_receipt: Any,
    plan_phase_activation_receipt: Any,
    original_cycle_root: Any,
) -> FiniteEvidenceWitnessAudit:
    """Bind the finite model to an actual prior nine-store source audit.

    The model's Lean proof is separately certified by independent Lean CI.
    This function only checks the Python side and retains its source/clock/
    authority obstructions. No source is synthesized when absent.
    """
    table = audit_finite_status_table()
    try:
        source = original.audit_native_middle_way_semantics(
            native_states,
            wa_replan_activation_receipt,
            plan_phase_activation_receipt,
            original_cycle_root,
        )
    except Exception as exc:
        return FiniteEvidenceWitnessAudit(
            status=BLOCKED,
            issues=table.issues + ("native_audit_exception:"
                                   + type(exc).__name__,),
            original_python_pair_cases_checked=table.original_python_pair_cases_checked,
            original_python_two_stage_cases_checked=table.original_python_two_stage_cases_checked,
            original_python_invalid_tokens_checked=table.original_python_invalid_tokens_checked,
            finite_table_locally_checked=table.finite_table_locally_checked,
        )
    issues = list(table.issues)
    source_status = source.status
    if source_status not in (
        original.SCOPED_COMPATIBLE, NO_DATA, BLOCKED
    ):
        issues.append("native:unexpected_source_status:" + str(source_status))
        source_status = BLOCKED
    if source_status == BLOCKED:
        issues.extend("native:" + problem for problem in source.issues)
    elif source_status == NO_DATA:
        issues.extend("native:" + problem for problem in source.issues)

    # A local native context key is grounded by the original v0.43 audit,
    # not an invented Python-to-Lean global identity certificate.
    key = ()
    if source_status == original.SCOPED_COMPATIBLE:
        if (type(source.context_lineage) is str and source.context_lineage
                and type(source.context_mission_digest) is str
                and source.context_mission_digest
                and type(source.original_store_root) is str
                and source.original_store_root):
            key = (
                ("worldScope", "native-v1.3-local-source"),
                ("lineageId", source.context_lineage),
                ("missionContractDigest", source.context_mission_digest),
                ("sourceRoot", source.original_store_root),
                ("interpretationVersion", VERSION),
            )
        else:
            issues.append("native:context_key_unobserved")
            source_status = NO_DATA

    status = (
        BLOCKED if (table.status == BLOCKED or source_status == BLOCKED)
        else NO_DATA if source_status != original.SCOPED_COMPATIBLE
        else SCOPED_NATIVE_COMPATIBLE
    )
    success = status == SCOPED_NATIVE_COMPATIBLE
    return FiniteEvidenceWitnessAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        original_python_pair_cases_checked=table.original_python_pair_cases_checked,
        original_python_two_stage_cases_checked=table.original_python_two_stage_cases_checked,
        original_python_invalid_tokens_checked=table.original_python_invalid_tokens_checked,
        finite_table_locally_checked=table.finite_table_locally_checked,
        original_native_nine_store_audit_checked=success,
        original_native_status=source.status,
        original_native_evidence_statuses=source.local_evidence_statuses,
        declared_context_key=key,
        read_only_consumer_advice=(
            ADVISORY_CONSUMERS if success else HOLD_CONSUMERS
        ),
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_TABLE_MATCH",
    "SCOPED_NATIVE_COMPATIBLE", "LOCALLY_CHECKED",
    "NO_DATA", "BLOCKED", "STATUSES", "FORMAL_MODEL_FILE",
    "FiniteEvidenceWitnessAudit", "audit_finite_status_table",
    "audit_native_finite_evidence_instance",
)

"""v0.40: persisted original DecisionOSPlural origin, replay, and staged edges.

Read-only local compatibility of an observed Plural genesis/ledger/snapshot
with the original DecisionOS final, original Plural constructor and the
already certified v0.39 Wa/Plan full-origin audit. Historical edges remain
separate. No Lean/Python semantic refinement or authority follows.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_decision_os_plural_kernel_v0_2 import (
    build_initial_plural_state,
)
from runtime.kuuos_decision_os_plural_store_v0_2 import (
    PluralDecisionStore, PluralDecisionStoreError,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    PASS as EDGE_PASS, _fingerprint, audit_typed_path,
)
from runtime.kuuos_lean_python_wa_plan_store_compat_v0_39 import (
    SCOPED_COMPATIBLE as PRIOR_PASS,
    _CapturedReads, _INPUT_ERRORS, _replay_captured, _trusted_store_root,
    audit_native_wa_plan_store_compatibility,
)

VERSION = "kuuos_lean_python_plural_store_origin_v0_40"
SOURCE_PARENT = "aabd1f2d9be0405624c464eb437e5d8acac68a8e"
SCOPED_COMPATIBLE = "SCOPED_DECISION_PLURAL_WA_PLAN_ORIGINS_COMPATIBLE"
_PLURAL_FILES = (
    "plural-genesis.json", "plural-ledger.jsonl", "plural-snapshot.json",
)
_EDGES = (
    "DecisionOS->DecisionOSPlural",
    "DecisionOSPlural->DecisionOSWa",
    "DecisionOSWa->PlanOS",
)
_INPUT = _INPUT_ERRORS + (PluralDecisionStoreError, UnicodeError)


class _CapturedPluralStore(_CapturedReads, PluralDecisionStore):
    """Re-use the exact original Plural replay kernel over captured bytes."""


@dataclass(frozen=True)
class NativePluralStoreOriginAudit:
    status: str
    issues: tuple[str, ...] = ()
    decision_final_digest: str | None = None
    plural_genesis_digest: str | None = None
    plural_final_digest: str | None = None
    plural_commit_count: int = 0
    plural_committed_decision_count: int = 0
    plural_summary_count: int = 0
    staged_typed_edge_statuses: tuple[tuple[str, str], ...] = ()
    checked_source_paths: tuple[str, ...] = ()
    plural_original_store_replayed: bool = False
    plural_genesis_matches_original_constructor: bool = False
    plural_lean_history_data_conditions_checked: bool = False
    decision_to_plural_original_edge_checked: bool = False
    prior_wa_plan_original_stores_checked: bool = False
    plural_store_bytes_stable_during_audit: bool = False
    wa_plan_store_bytes_stable_during_audit: bool = False
    # A bounded local audit cannot promote these to certified truths.
    original_decision_store_replayed: bool = False
    globally_atomic_three_store_snapshot_proved: bool = False
    global_descent_proved: bool = False
    lean_python_semantic_refinement_proved: bool = False
    external_issuer_authenticated: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    host_license_granted: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    legal_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, *issues: str) -> NativePluralStoreOriginAudit:
    return NativePluralStoreOriginAudit(status=status, issues=tuple(issues))


def _roots_separate(roots: tuple[Path, Path, Path]) -> bool:
    # Reject aliases AND nested store roots, which would mix the boundaries
    # of separately observed and separately controlled native stores.
    return len(set(roots)) == len(roots) and all(
        a not in b.parents for a in roots for b in roots if a != b
    )


def _plural_history_alignment(
    genesis: dict, final: dict, commits: list[dict],
) -> tuple[bool, int, int]:
    """Check a selected Python data interpretation of Lean PluralDecisionHistory.

    Native replay authenticates local hash chains, but it does not itself
    enforce a direct equality between committed-summary count and commit
    events. Preserve this as an additional conditional Python check only.
    """
    summaries = final.get("plural_summaries")
    if type(summaries) is not list:
        return False, 0, 0
    digests = [
        row["event"].get("plural_event_digest")
        for row in commits if row["event"].get("target_phase") == "commit"
    ]
    summary_ids = [row.get("commit_event_digest") for row in summaries
                   if type(row) is dict]
    count = len(digests)
    aligned = (
        type(genesis.get("event_index")) is int
        and genesis["event_index"] == 0
        and type(genesis.get("plural_version")) is int
        and genesis["plural_version"] == 0
        and type(genesis.get("completed_plural_deliberations")) is int
        and genesis["completed_plural_deliberations"] == 0
        and genesis.get("plural_summaries") == []
        and type(final.get("event_index")) is int
        and final["event_index"] == len(commits)
        and type(final.get("plural_version")) is int
        and final["plural_version"] == count
        and type(final.get("completed_plural_deliberations")) is int
        and final["completed_plural_deliberations"] == count
        and len(summaries) == count
        and len(summary_ids) == count
        and summary_ids == digests
        and all(
            type(row.get("plural_version")) is int
            and row["plural_version"] == i
            for i, row in enumerate(summaries, 1)
        )
    )
    return aligned, count, len(summaries)


def audit_native_plural_store_origin(
    decision_state: Any,
    plural_state: Any,
    wa_state: Any,
    plan_state: Any,
    replan_activation_receipt: Any,
    original_plural_store_root: Any,
    original_wa_store_root: Any,
    original_plan_store_root: Any,
) -> NativePluralStoreOriginAudit:
    """Audit exact observed Plural origin and two downstream store origins.

    The original Decision final and original replan receipt MUST be supplied.
    None is synthesized, authenticated or granted authority. Missing histories
    remain NO_DATA; contradictory selected inputs are BLOCKED, not a theorem
    of general impossibility.
    """
    named = (
        ("DecisionOS", decision_state),
        ("DecisionOSPlural", plural_state),
        ("DecisionOSWa", wa_state),
        ("PlanOS", plan_state),
        ("replan_receipt", replan_activation_receipt),
        ("PluralStore", original_plural_store_root),
        ("WaStore", original_wa_store_root),
        ("PlanStore", original_plan_store_root),
    )
    missing = tuple(name + ":original_source_missing"
                    for name, value in named if value is None)
    if missing:
        return _hold(NO_DATA, *missing)
    if any(type(v) is not str and type(v) is not type(Path())
           for v in (
               original_plural_store_root, original_wa_store_root,
               original_plan_store_root,
           )):
        return _hold(BLOCKED, "plural_wa_plan_store:untrusted_root_type")

    try:
        decision = _packet(decision_state, "DecisionOS")
        plural = _packet(plural_state, "DecisionOSPlural")
        wa = _packet(wa_state, "DecisionOSWa")
        plan = _packet(plan_state, "PlanOS")
        receipt = _packet(replan_activation_receipt, "replan_receipt")
        roots = tuple(_trusted_store_root(root) for root in (
            original_plural_store_root, original_wa_store_root,
            original_plan_store_root,
        ))
        if not _roots_separate(roots):
            return _hold(BLOCKED, "plural_wa_plan_store:roots_overlap")
        plural_root, wa_root, plan_root = roots
        before = _store_files(plural_root, _PLURAL_FILES)
        genesis, final, commits = _replay_captured(
            plural_root, _CapturedPluralStore, before,
        )
        final = _packet(final, "PluralStore.final")
    except FileNotFoundError:
        return _hold(NO_DATA, "plural_store:original_history_missing")
    except _INPUT as exc:
        return _hold(BLOCKED, "plural_store:original_source_invalid:"
                     + type(exc).__name__)

    if not _same(plural, final):
        return _hold(BLOCKED, "DecisionOSPlural:not_original_stored_final")
    if final.get("current_phase") != "commit":
        return _hold(NO_DATA, "DecisionOSPlural:committed_final_unobserved")

    failures: list[str] = []
    absent: list[str] = []
    prior = None
    first_edge = None
    aligned = False
    committed = 0
    summaries = 0
    try:
        # All constructor parameters other than the source Decision state are
        # observed in the original genesis: no setting is authenticated here.
        reconstructed = build_initial_plural_state(
            source_decision_state=decision,
            plural_id=genesis["plural_id"],
            lineage_id=genesis["lineage_id"],
            thresholds=genesis["thresholds"],
            now_ms=genesis["updated_at_ms"],
        )
        if not _same(reconstructed, genesis):
            failures.append("DecisionOSPlural:genesis_not_original_constructor")

        aligned, committed, summaries = _plural_history_alignment(
            genesis, final, commits,
        )
        if not aligned:
            failures.append("DecisionOSPlural:commit_summary_history_not_aligned")

        # Decision final -> Plural original genesis is a *historical* edge.
        # A separate Plural final -> Wa genesis is checked by v0.39.
        first_edge = audit_typed_path(
            {"DecisionOS": decision, "DecisionOSPlural": genesis},
            start="DecisionOS", end="DecisionOSPlural",
        )
        if first_edge.status == BLOCKED:
            failures.extend("DecisionOS->DecisionOSPlural:" + x
                            for x in first_edge.violations)
            if not first_edge.violations:
                failures.append("DecisionOS->DecisionOSPlural:blocked")
        elif first_edge.status != EDGE_PASS:
            absent.append("DecisionOS->DecisionOSPlural:unconfirmed:"
                          + first_edge.status)
            absent.extend("DecisionOS->DecisionOSPlural:" + x
                          for x in first_edge.missing)

        prior = audit_native_wa_plan_store_compatibility(
            plural_state=plural,
            wa_state=wa,
            plan_state=plan,
            replan_activation_receipt=receipt,
            original_wa_store_root=wa_root,
            original_plan_store_root=plan_root,
        )
        if prior.status == BLOCKED:
            failures.extend("v039:" + issue for issue in prior.issues)
            if not prior.issues:
                failures.append("v039:blocked")
        elif prior.status != PRIOR_PASS:
            absent.append("v039:unconfirmed:" + prior.status)
            absent.extend("v039:" + issue for issue in prior.issues)
        elif not (
            prior.wa_original_store_replayed
            and prior.plan_original_store_replayed
            and prior.wa_genesis_matches_original_constructor
            and prior.plan_genesis_matches_original_constructor
            and prior.original_final_wa_plan_conditions_checked
            and prior.store_bytes_stable_during_audit
            and tuple(status for _, status in prior.staged_typed_edge_statuses)
                == (EDGE_PASS, EDGE_PASS)
        ):
            absent.append("v039:local_origin_conditions_unconfirmed")
    except _INPUT as exc:
        return _hold(BLOCKED, "plural_store:original_conditions_invalid:"
                     + type(exc).__name__)

    after = None
    try:
        _trusted_store_root(plural_root)
        after = _store_files(plural_root, _PLURAL_FILES)
        if before != after:
            failures.append("plural_store:original_bytes_changed")
    except FileNotFoundError:
        absent.append("plural_store:original_history_disappeared")
    except _INPUT as exc:
        failures.append("plural_store:recheck_invalid:" + type(exc).__name__)

    status = BLOCKED if failures else NO_DATA if absent else SCOPED_COMPATIBLE
    passed = status == SCOPED_COMPATIBLE
    downstream = (prior.staged_typed_edge_statuses if prior else ())
    return NativePluralStoreOriginAudit(
        status=status,
        issues=tuple(dict.fromkeys(failures + absent)),
        decision_final_digest=_fingerprint(decision),
        plural_genesis_digest=_fingerprint(genesis),
        plural_final_digest=_fingerprint(final),
        plural_commit_count=len(commits),
        plural_committed_decision_count=committed,
        plural_summary_count=summaries,
        staged_typed_edge_statuses=(
            ((_EDGES[0], first_edge.status),) if first_edge else ()
        ) + downstream,
        checked_source_paths=(
            tuple("DecisionOSPlural." + name for name in _PLURAL_FILES)
            + (prior.checked_source_paths if prior else ())
        ),
        plural_original_store_replayed=passed,
        plural_genesis_matches_original_constructor=passed,
        plural_lean_history_data_conditions_checked=passed and aligned,
        decision_to_plural_original_edge_checked=passed,
        prior_wa_plan_original_stores_checked=passed,
        plural_store_bytes_stable_during_audit=after is not None and before == after,
        wa_plan_store_bytes_stable_during_audit=(
            prior.store_bytes_stable_during_audit if prior else False
        ),
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "BLOCKED", "NO_DATA",
    "NativePluralStoreOriginAudit", "audit_native_plural_store_origin",
)

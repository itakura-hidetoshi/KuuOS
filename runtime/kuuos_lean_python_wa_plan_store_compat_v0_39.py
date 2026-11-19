"""v0.39: original Wa/Plan store replay and complete native origin checks.

Read-only compatibility of the exact supplied records and six observed files.
Each receiving genesis is distinct from its outgoing committed final. Exact
initial-constructor equality detects a valid suffix ledger presented as a
full-origin history; it does not authenticate the producer or configuration.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import io
import json
import math
from pathlib import Path
from typing import Any

from runtime.kuuos_decision_os_wa_store_v0_3 import (
    WaDecisionStore, WaDecisionStoreError,
)
from runtime.kuuos_plan_os_store_v0_1 import PlanStore, PlanStoreError
from runtime.kuuos_decision_os_wa_state_v0_3 import build_initial_wa_state
from runtime.kuuos_plan_os_state_v0_1 import build_initial_plan_state
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    PASS as TYPED_PASS, _fingerprint, audit_typed_path,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_wa_plan_local_compat_v0_33 import (
    SCOPED_COMPATIBLE as LOCAL_PASS,
    audit_native_wa_plan_local_compatibility,
)

VERSION = "kuuos_lean_python_wa_plan_store_compat_v0_39"
SOURCE_PARENT = "1930ef2bed45e8c577c21f62f4812546f5ab597e"
SCOPED_COMPATIBLE = "SCOPED_WA_PLAN_STORE_COMPATIBLE"
_WA_FILES = ("wa-v03-genesis.json", "wa-v03-ledger.jsonl", "wa-v03-snapshot.json")
_PLAN_FILES = ("plan-genesis.json", "plan-ledger.jsonl", "plan-snapshot.json")
_EDGES = ("DecisionOSPlural->DecisionOSWa", "DecisionOSWa->PlanOS")
_INPUT_ERRORS = (
    TypeError, ValueError, KeyError, AttributeError, OSError, RecursionError,
    OverflowError, WaDecisionStoreError, PlanStoreError,
)


@dataclass(frozen=True)
class NativeWaPlanStoreAudit:
    status: str
    issues: tuple[str, ...] = ()
    plural_source_digest: str | None = None
    wa_genesis_digest: str | None = None
    wa_final_digest: str | None = None
    plan_genesis_digest: str | None = None
    plan_final_digest: str | None = None
    replan_receipt_digest: str | None = None
    wa_commit_count: int = 0
    plan_commit_count: int = 0
    staged_typed_edge_statuses: tuple[tuple[str, str], ...] = ()
    checked_source_paths: tuple[str, ...] = ()
    wa_original_store_replayed: bool = False
    plan_original_store_replayed: bool = False
    wa_genesis_matches_original_constructor: bool = False
    plan_genesis_matches_original_constructor: bool = False
    original_final_wa_plan_conditions_checked: bool = False
    store_bytes_stable_during_audit: bool = False
    # These are outside the local audit, even when status is scoped success.
    formal_global_descent_proved: bool = False
    lean_python_semantic_refinement_proved: bool = False
    global_atomic_snapshot_proved: bool = False
    external_replan_issuer_authenticated: bool = False
    plural_original_store_replayed: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    execution_authority_granted: bool = False
    host_license_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    legal_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, *issues: str) -> NativeWaPlanStoreAudit:
    return NativeWaPlanStoreAudit(status=status, issues=tuple(issues))


def _trusted_store_root(value: str | Path) -> Path:
    root = Path(value).absolute()
    if ".." in root.parts:
        raise ValueError("store_root_parent_traversal_forbidden")
    if any(part.is_symlink() for part in (root, *root.parents)):
        raise ValueError("store_root_or_ancestor_symlink_forbidden")
    try:
        return root.resolve()
    except RuntimeError as exc:
        raise ValueError("store_root_resolution_failed") from exc


def _reject_nonfinite_json(value: str):
    raise ValueError("captured_json_nonfinite:" + value)


def _finite_json_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        _reject_nonfinite_json(value)
    return number


def _decode_captured(text: str, label: str) -> dict:
    # Reject each nonfinite token during parsing, before a duplicate name
    # could shadow it. Finite duplicate-name semantics remain native JSON's.
    value = json.loads(text, parse_constant=_reject_nonfinite_json,
                       parse_float=_finite_json_float)
    return _packet(value, label)


class _CapturedReads:
    """Use one observed byte set with the unchanged native replay kernel.

    Only the readers are replaced. The native _recover_unlocked method still
    checks state, commit and event digests, versions and each original event.
    No temporary store or lock file is created. Every read yields a new plain
    finite JSON copy of the same captured bytes.
    """

    def __init__(self, root: Path, captured: dict[str, bytes]):
        super().__init__(root)
        self._captured = dict(captured)

    def _read_json(self, path: Path) -> dict:
        return _decode_captured(self._captured[path.name].decode("utf-8"),
                                "captured:" + path.name)

    def _read_ledger(self) -> list[dict]:
        rows = []
        text = self._captured[self.ledger_path.name].decode("utf-8")
        # Match the original text-file reader's universal newline handling.
        for raw in io.StringIO(text, newline=None):
            line = raw.strip()
            if not line:
                raise ValueError("captured_ledger_blank_line")
            rows.append(_decode_captured(line, "captured:ledger_row"))
        return rows


class _CapturedWaStore(_CapturedReads, WaDecisionStore):
    pass


class _CapturedPlanStore(_CapturedReads, PlanStore):
    pass


def _replay_captured(root: Path, store_type: type, captured: dict[str, bytes]):
    native = store_type(root, captured)
    genesis = native._read_json(native.genesis_path)
    final, commits = native._recover_unlocked()
    snapshot = native._read_json(native.snapshot_path)
    if not _same(snapshot, final):
        raise ValueError("captured_snapshot_not_exact_replay")
    if not commits:
        raise FileNotFoundError("captured_commits_unobserved")
    if any(type(row.get("commit_index")) is not int or row["commit_index"] != i
           for i, row in enumerate(commits, 1)):
        raise ValueError("captured_commit_indices_not_exact")
    return genesis, final, commits


def audit_native_wa_plan_store_compatibility(
    plural_state: Any,
    wa_state: Any,
    plan_state: Any,
    replan_activation_receipt: Any,
    original_wa_store_root: Any,
    original_plan_store_root: Any,
) -> NativeWaPlanStoreAudit:
    """Audit the supplied full-origin history without writing or filling gaps.

    Constructor arguments copied from genesis are observed configuration,
    not independently authenticated settings. BLOCKED denotes a contradiction
    to these local conditions, not a proof of universal impossibility.
    """
    named = (
        ("DecisionOSPlural", plural_state), ("DecisionOSWa", wa_state),
        ("PlanOS", plan_state), ("replan_receipt", replan_activation_receipt),
        ("WaStore", original_wa_store_root), ("PlanStore", original_plan_store_root),
    )
    missing = tuple(name + ":original_source_missing"
                    for name, value in named if value is None)
    if missing:
        return _hold(NO_DATA, *missing)
    if any(type(value) is not str and type(value) is not type(Path())
           for value in (original_wa_store_root, original_plan_store_root)):
        return _hold(BLOCKED, "wa_plan_store:untrusted_root_type")

    try:
        plural = _packet(plural_state, "DecisionOSPlural")
        wa = _packet(wa_state, "DecisionOSWa")
        plan = _packet(plan_state, "PlanOS")
        receipt = _packet(replan_activation_receipt, "replan_receipt")
        wa_root = _trusted_store_root(original_wa_store_root)
        plan_root = _trusted_store_root(original_plan_store_root)
        if wa_root == plan_root:
            return _hold(BLOCKED, "wa_plan_store:roots_not_distinct")
        before = (_store_files(wa_root, _WA_FILES),
                  _store_files(plan_root, _PLAN_FILES))
        wa_genesis, wa_final, wa_commits = _replay_captured(
            wa_root, _CapturedWaStore, before[0],
        )
        plan_genesis, plan_final, plan_commits = _replay_captured(
            plan_root, _CapturedPlanStore, before[1],
        )
        # Captured genesis, snapshot and all ledger rows were finite-checked
        # before use. Also bound each derived final to the finite JSON domain.
        wa_final = _packet(wa_final, "WaStore.final")
        plan_final = _packet(plan_final, "PlanStore.final")
    except FileNotFoundError:
        return _hold(NO_DATA, "wa_plan_store:original_history_missing")
    except _INPUT_ERRORS as exc:
        return _hold(BLOCKED, "wa_plan_store:original_source_invalid:" + type(exc).__name__)

    if not _same(wa, wa_final):
        return _hold(BLOCKED, "DecisionOSWa:not_original_stored_final")
    if not _same(plan, plan_final):
        return _hold(BLOCKED, "PlanOS:not_original_stored_final")
    if wa_final.get("current_phase") != "commit" or plan_final.get("current_phase") != "commit":
        return _hold(NO_DATA, "wa_plan_store:final_commits_unobserved")

    failures: list[str] = []
    absent: list[str] = []
    try:
        local = audit_native_wa_plan_local_compatibility(plural, wa_final, plan_final, receipt)
        if local.status == BLOCKED:
            failures.extend("original_final:" + issue for issue in local.issues)
            if not local.issues:
                failures.append("original_final:blocked")
        elif local.status != LOCAL_PASS:
            absent.append("original_final:unconfirmed:" + local.status)
            absent.extend("original_final:" + issue for issue in local.issues)
        elif not (local.original_wa_conditions_checked
                  and local.original_plan_guards_checked
                  and local.original_replan_edge_checked
                  and local.selected_lean_data_conditions_checked):
            absent.append("original_final:conditions_unconfirmed")

        # The supplied Plural history itself is not persisted/replayed here.
        # These original constructors are pure; no receipt is reissued.
        expected_wa = build_initial_wa_state(
            wa_id=wa_genesis["wa_id"],
            source_plural_state=plural,
            weights=wa_genesis["weights"],
            thresholds=wa_genesis["thresholds"],
            now_ms=wa_genesis["updated_at_ms"],
        )
        expected_plan = build_initial_plan_state(
            plan_id=plan_genesis["plan_id"],
            source_wa_state=wa_final,
            replan_activation_receipt=receipt,
            plan_budget=plan_genesis["plan_budget"],
            maximum_step_risk=plan_genesis["maximum_step_risk"],
            now_ms=plan_genesis["updated_at_ms"],
        )
        wa_origin_matches = _same(expected_wa, wa_genesis)
        plan_origin_matches = _same(expected_plan, plan_genesis)
        if not wa_origin_matches:
            failures.append("DecisionOSWa:genesis_not_original_constructor")
        if not plan_origin_matches:
            failures.append("PlanOS:genesis_not_original_constructor")

        # Two historical edges; Wa's incoming genesis != outgoing final.
        staged = (
            audit_typed_path(
                {"DecisionOSPlural": plural, "DecisionOSWa": wa_genesis},
                start="DecisionOSPlural", end="DecisionOSWa",
            ),
            audit_typed_path(
                {"DecisionOSWa": wa_final, "PlanOS": plan_genesis},
                receipts={"DecisionOSWa->PlanOS": receipt},
                start="DecisionOSWa", end="PlanOS",
            ),
        )
        for edge, result in zip(_EDGES, staged):
            if result.status == BLOCKED:
                failures.extend(edge + ":" + item for item in result.violations)
                if not result.violations:
                    failures.append(edge + ":blocked")
            elif result.status != TYPED_PASS:
                absent.append(edge + ":unconfirmed:" + result.status)
                absent.extend(edge + ":" + item for item in result.missing)
    except _INPUT_ERRORS as exc:
        return _hold(BLOCKED, "wa_plan_store:original_conditions_invalid:" + type(exc).__name__)

    after = None
    try:
        _trusted_store_root(wa_root)
        _trusted_store_root(plan_root)
        after = (_store_files(wa_root, _WA_FILES),
                 _store_files(plan_root, _PLAN_FILES))
        if before != after:
            failures.append("wa_plan_store:original_bytes_changed")
    except FileNotFoundError:
        absent.append("wa_plan_store:original_history_disappeared")
    except _INPUT_ERRORS as exc:
        failures.append("wa_plan_store:recheck_invalid:" + type(exc).__name__)

    status = BLOCKED if failures else NO_DATA if absent else SCOPED_COMPATIBLE
    passed = status == SCOPED_COMPATIBLE
    return NativeWaPlanStoreAudit(
        status=status,
        issues=tuple(dict.fromkeys(failures + absent)),
        plural_source_digest=_fingerprint(plural),
        wa_genesis_digest=_fingerprint(wa_genesis),
        wa_final_digest=_fingerprint(wa_final),
        plan_genesis_digest=_fingerprint(plan_genesis),
        plan_final_digest=_fingerprint(plan_final),
        replan_receipt_digest=receipt["wa_activation_receipt_digest"],
        wa_commit_count=len(wa_commits), plan_commit_count=len(plan_commits),
        staged_typed_edge_statuses=tuple((edge, result.status)
                                        for edge, result in zip(_EDGES, staged)),
        checked_source_paths=tuple("DecisionOSWa." + name for name in _WA_FILES)
        + tuple("PlanOS." + name for name in _PLAN_FILES),
        wa_original_store_replayed=passed,
        plan_original_store_replayed=passed,
        wa_genesis_matches_original_constructor=passed and wa_origin_matches,
        plan_genesis_matches_original_constructor=passed and plan_origin_matches,
        original_final_wa_plan_conditions_checked=passed,
        store_bytes_stable_during_audit=after is not None and before == after,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "BLOCKED", "NO_DATA",
    "NativeWaPlanStoreAudit", "audit_native_wa_plan_store_compatibility",
)

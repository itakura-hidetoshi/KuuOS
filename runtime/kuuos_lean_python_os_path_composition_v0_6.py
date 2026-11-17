"""Bounded composition of existing KuuOS Lean→Python per-OS audits (v0.6).

This is an observation of supplied JSON-like states and receipts only.
Individual audited links do not prove formal descent of runtime semantics.
No event application, host invocation, repository write or authority grant.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

from runtime.kuuos_lean_python_os_registry_v0_5 import (
    EDGES, ScopedAudit, audit_edge,
)

VERSION = "kuuos_lean_python_os_path_composition_v0_6"
SOURCE_MAIN = "ffd6835d182df791d971c199750d5e9e38a32741"

PATH = (
    "DecisionOS", "DecisionOSPlural", "DecisionOSWa", "PlanOS",
    "ActOS", "ObserveOS", "VerifyOS", "LearnOS",
)
RECEIPT_EDGE_NAMES = (
    "DecisionOSWa->PlanOS",
    "PlanOS->ActOS",
)
PASS = "SCOPED_PATH_CHECKED"
NO_DATA = "NO_DATA"
BLOCKED = "BLOCKED"
GOOD_EDGE = frozenset(("RUNTIME_CHECK_PASSED", "PASS"))


@dataclass(frozen=True)
class PathAudit:
    status: str
    path: tuple[str, ...]
    edge_audits: tuple[tuple[str, str, ScopedAudit], ...]
    violations: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    input_sha256: tuple[tuple[str, str], ...] = ()
    source_main: str = SOURCE_MAIN
    scope: str = "typed_source_target_links_and_shared_JSON_snapshots"
    local_python_checks_completed: bool = False
    formal_descent_certified: bool = False
    lean_python_refinement_proved: bool = False
    external_receipt_authenticated: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    merge_authority_granted: bool = False


def _finite_json(value: Any) -> Any:
    """Copy only exact built-in JSON data, without invoking user-defined hooks."""
    count = [0]
    active: set[int] = set()

    def visit(obj: Any, depth: int) -> Any:
        count[0] += 1
        if count[0] > 200_000 or depth > 64:
            raise ValueError("json_budget_exceeded")
        kind = type(obj)
        if obj is None or kind in (bool, int, str):
            if kind is str:
                obj.encode("utf-8")
            return obj
        if kind is float:
            if not math.isfinite(obj):
                raise ValueError("nonfinite_number")
            return obj
        if kind not in (dict, list):
            raise TypeError("not_builtin_json")
        ident = id(obj)
        if ident in active:
            raise ValueError("cyclic_json")
        active.add(ident)
        try:
            if kind is list:
                return [visit(item, depth + 1) for item in obj]
            if any(type(key) is not str for key in obj):
                raise TypeError("nonstring_key")
            return {visit(key, depth + 1): visit(item, depth + 1)
                    for key, item in obj.items()}
        finally:
            active.remove(ident)

    result = visit(value, 0)
    payload = json.dumps(result, sort_keys=True, ensure_ascii=False,
                         allow_nan=False, separators=(",", ":")).encode("utf-8")
    if len(payload) > 4_000_000:
        raise ValueError("json_payload_too_large")
    return result


def _fingerprint(value: Any) -> str:
    return sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False, allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _finish(path: tuple[str, ...], edges: list[tuple[str, str, ScopedAudit]],
            errors: list[str], missing: list[str],
            digests: list[tuple[str, str]]) -> PathAudit:
    status = BLOCKED if errors else NO_DATA if missing else PASS
    return PathAudit(
        status=status, path=path, edge_audits=tuple(edges),
        violations=tuple(dict.fromkeys(errors)),
        missing=tuple(dict.fromkeys(missing)),
        input_sha256=tuple(digests),
        local_python_checks_completed=(status == PASS),
    )


def audit_typed_path(
    states: Any,
    *,
    receipts: Any = None,
    start: str = "DecisionOS",
    end: str = "LearnOS",
) -> PathAudit:
    """Audit every adjacent edge of a *selected contiguous* KuuOS path.

    The same state snapshot is reused on both sides of an intermediate node.
    Separate signed/externally authenticated receipts are not inferred.
    An observed failed link stays BLOCKED; a missing intermediate remains
    NO_DATA. Even seven scoped PASS results are not a Lean descent proof.
    """
    errors: list[str] = []
    missing: list[str] = []
    audited: list[tuple[str, str, ScopedAudit]] = []
    fingerprints: list[tuple[str, str]] = []

    if type(start) is not str or type(end) is not str or start not in PATH or end not in PATH:
        return _finish((), audited, errors, ["unsupported_named_path"], fingerprints)
    lower, upper = PATH.index(start), PATH.index(end)
    if lower >= upper:
        return _finish((start,), audited, ["path_must_advance"], missing, fingerprints)
    path = PATH[lower:upper + 1]
    required_edges = tuple(zip(path, path[1:]))
    if any(pair not in EDGES for pair in required_edges):
        return _finish(path, audited, errors, ["missing_typed_edge_definition"], fingerprints)

    if states is None:
        missing.append("states:missing")
        state_inputs: dict[str, Any] = {}
    elif type(states) is not dict:
        errors.append("states:not_plain_object")
        state_inputs = {}
    else:
        state_inputs = states
        for name in states:
            if type(name) is not str or name not in PATH:
                errors.append("states:unknown_name")
    if receipts is None:
        receipt_inputs: dict[str, Any] = {}
    elif type(receipts) is not dict:
        errors.append("receipts:not_plain_object")
        receipt_inputs = {}
    else:
        receipt_inputs = receipts

    snapshots: dict[str, dict[str, Any]] = {}
    for name in path:
        if name not in state_inputs or state_inputs[name] is None:
            missing.append("state:" + name + ":missing")
            continue
        value = state_inputs[name]
        if type(value) is not dict:
            errors.append("state:" + name + ":not_plain_object")
            continue
        try:
            snap = _finite_json(value)
            snapshots[name] = snap
            fingerprints.append(("state:" + name, _fingerprint(snap)))
        except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
            errors.append("state:" + name + ":invalid_json")

    receipt_snapshots: dict[str, dict[str, Any]] = {}
    required_receipts = tuple(
        source + "->" + target for source, target in required_edges
        if EDGES[(source, target)].receipt_required
    )
    for key in receipt_inputs:
        if type(key) is not str or key not in RECEIPT_EDGE_NAMES:
            errors.append("receipts:unknown_edge")
    for key in required_receipts:
        if key not in receipt_inputs or receipt_inputs[key] is None:
            missing.append("receipt:" + key + ":missing")
            continue
        value = receipt_inputs[key]
        if type(value) is not dict:
            errors.append("receipt:" + key + ":not_plain_object")
            continue
        try:
            snap = _finite_json(value)
            receipt_snapshots[key] = snap
            fingerprints.append(("receipt:" + key, _fingerprint(snap)))
        except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
            errors.append("receipt:" + key + ":invalid_json")

    # This explicitly checks global contextual compatibility; local edge
    # acceptance alone cannot make inconsistent lineage or mission global.
    context: dict[str, tuple[str, str]] = {}
    times: dict[str, int] = {}
    for name in path:
        snap = snapshots.get(name)
        if snap is None:
            continue
        ids: list[str] = []
        for field in ("lineage_id", "mission_contract_digest"):
            value = snap.get(field)
            if value is None or value == "":
                missing.append("state:" + name + ":" + field + ":missing")
            elif type(value) is not str or not value.strip():
                errors.append("state:" + name + ":" + field + ":invalid")
            else:
                ids.append(value)
        if len(ids) == 2:
            context[name] = (ids[0], ids[1])
        time = snap.get("updated_at_ms")
        if time is None:
            missing.append("state:" + name + ":updated_at_ms:missing")
        elif type(time) is not int or time < 0:
            errors.append("state:" + name + ":updated_at_ms:invalid")
        else:
            times[name] = time
    baseline = next((context[n] for n in path if n in context), None)
    for name in path:
        if name in context and baseline is not None and context[name] != baseline:
            errors.append("state:" + name + ":cross_context_mismatch")
    for a, b in required_edges:
        if a in times and b in times and times[a] > times[b]:
            errors.append(a + "->" + b + ":time_regression")

    # Even with missing nodes, audit every available edge so observed
    # contradictions are retained rather than overwritten by NO_DATA.
    for source, target in required_edges:
        key = source + "->" + target
        if source not in snapshots or target not in snapshots:
            missing.append("edge:" + key + ":endpoint_missing")
            continue
        receipt = None
        if EDGES[(source, target)].receipt_required:
            if key not in receipt_snapshots:
                missing.append("edge:" + key + ":receipt_missing")
                continue
            receipt = deepcopy(receipt_snapshots[key])
        one, two = deepcopy(snapshots[source]), deepcopy(snapshots[target])
        before = (_fingerprint(one), _fingerprint(two),
                  _fingerprint(receipt) if receipt is not None else None)
        try:
            result = audit_edge(
                source, target, one, two, activation_receipt=receipt,
            )
        except Exception as exc:
            errors.append("edge:" + key + ":audit_exception:" + type(exc).__name__)
            continue
        try:
            after = (_fingerprint(one), _fingerprint(two),
                     _fingerprint(receipt) if receipt is not None else None)
        except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
            errors.append("edge:" + key + ":validator_mutated_to_invalid_json")
        else:
            if after != before:
                errors.append("edge:" + key + ":validator_mutated_snapshot")
        if not isinstance(result, ScopedAudit):
            errors.append("edge:" + key + ":unexpected_audit_result")
            continue
        audited.append((source, target, result))
        if result.status == "BLOCKED":
            errors.append("edge:" + key + ":blocked")
        elif result.status == "NO_DATA":
            missing.append("edge:" + key + ":no_data")
        elif result.status not in GOOD_EDGE or result.runtime_checked is not True:
            missing.append("edge:" + key + ":native_checks_unconfirmed")
    return _finish(path, audited, errors, missing, fingerprints)


__all__ = (
    "VERSION", "SOURCE_MAIN", "PATH", "RECEIPT_EDGE_NAMES",
    "PASS", "NO_DATA", "BLOCKED", "PathAudit", "audit_typed_path",
)

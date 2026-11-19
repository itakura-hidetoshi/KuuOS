"""v0.29: original source-bound Decision/Plural/Wa intermediary audit primitives.

The original seven-step KuuOS typed OS pipeline is retained.
A checked source packet is not a Lean proof term, an external receipt
attestation, or host/truth authority. No existing OS code is modified.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA, PASS, UnavailableSource, NativeOSBindingAudit,
    copied_state, copied_edge, field, truth, natural, plain_list, string,
    require_match, fail,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_decision_os_plural_kernel_v0_2 import validate_plural_state
from runtime.kuuos_decision_os_wa_kernel_v0_3 import validate_wa_state

VERSION = "kuuos_lean_python_decision_mediator_source_v0_29"
SOURCE_MAIN = "66a9f5b2d895d2182f6ee9462f18c6a2a3832e4a"
MISSING_PROOF = "local_source_data_only_not_lean_python_refinement"


def mediator_state(name: str, state: Any) -> dict[str, Any]:
    """Use the ORIGINAL v0.2/v0.3 validators, not an edge-only stand-in."""
    if state is None:
        raise UnavailableSource(name + ":state_missing", NO_DATA)
    if type(state) is not dict:
        raise UnavailableSource(name + ":exact_object_required", BLOCKED)
    try:
        snap = _finite_json(state)
    except (TypeError, ValueError, OverflowError, UnicodeError, RecursionError):
        raise UnavailableSource(name + ":invalid_json", BLOCKED)
    validator = {
        "DecisionOSPlural": validate_plural_state,
        "DecisionOSWa": validate_wa_state,
    }.get(name)
    if validator is None:
        raise UnavailableSource(name + ":unregistered_mediator", NO_DATA)
    try:
        issues = validator(snap)
    except (TypeError, ValueError, KeyError, AttributeError, RecursionError):
        raise UnavailableSource(name + ":original_validator_exception", BLOCKED)
    if type(issues) is not list or issues:
        raise UnavailableSource(name + ":original_validator_failed", BLOCKED)
    if snap.get("current_phase") != "commit":
        raise UnavailableSource(name + ":commit_not_observed", NO_DATA)
    return snap


def rational_float(value: Any, label: str) -> Fraction:
    """Exact rational of an *already observed* finite float, no rounding claim."""
    if type(value) not in (float, int):
        raise UnavailableSource(label + ":native_float_or_int_required", BLOCKED)
    if type(value) is int:
        return Fraction(value)
    try:
        return Fraction(*value.as_integer_ratio())
    except (ValueError, OverflowError):
        raise UnavailableSource(label + ":nonfinite_float", BLOCKED)


def record(name: str, snap: dict, paths: list[str], count: int,
           *, edge: bool, issues: tuple[str, ...] = ()) -> NativeOSBindingAudit:
    """Only selected original source-bound mathematical data conditions."""
    if count < 1:
        return fail(name, "no_matching_original_local_witness", status=NO_DATA)
    return NativeOSBindingAudit(
        os_name=name, status=PASS, source_digest=_fingerprint(snap),
        source_field_paths=tuple(dict.fromkeys(paths)),
        checked_witnesses=count,
        issues=issues,
        original_state_validated=True,
        original_edge_validated=edge,
        source_bound_python_conditions_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "PASS",
    "UnavailableSource", "NativeOSBindingAudit", "copied_state",
    "copied_edge", "field", "truth", "natural", "plain_list", "string",
    "require_match", "fail", "mediator_state", "rational_float", "record",
)

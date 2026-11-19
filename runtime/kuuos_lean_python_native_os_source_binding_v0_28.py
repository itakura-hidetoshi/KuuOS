"""v0.28: original-state-bound Lean→Python per-OS data projections.

The v0.27 theorem-condition adapters accept independently supplied data;
v0.28 requires actual original native OS state/receipt bytes and original
state validators before deriving selected fields from named source paths.
This is local source-bound Python checking, NEVER a Lean proof of Python,
an external issuer attestation, permission to invoke a host, or an effect.

No original OS kernel, store, source proof or existing v0.27 code is changed.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_lean_python_os_registry_v0_5 import (
    audit_os, audit_edge,
)

VERSION = "kuuos_lean_python_native_os_source_binding_v0_28"
SOURCE_MAIN = "bf2eda97f843093b3be538495839b08c1b45d298"
PASS = "SOURCE_BOUND_LOCAL_CHECKED"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class UnavailableSource(Exception):
    def __init__(self, reason: str, status: str = NO_DATA) -> None:
        self.reason, self.status = reason, status
        super().__init__(reason)


@dataclass(frozen=True)
class NativeOSBindingAudit:
    os_name: str
    status: str
    source_digest: str | None = None
    source_field_paths: tuple[str, ...] = ()
    checked_witnesses: int = 0
    issues: tuple[str, ...] = ()
    original_state_validated: bool = False
    original_edge_validated: bool = False
    source_bound_python_conditions_checked: bool = False
    native_state_modified: bool = False
    formal_lean_python_refinement_proved: bool = False
    lean_proof_term_constructed: bool = False
    external_issuer_authenticated: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    global_host_effect_certified: bool = False


def fail(os_name: str, reason: str, *, status: str = NO_DATA) -> NativeOSBindingAudit:
    return NativeOSBindingAudit(os_name=os_name, status=status, issues=(reason,))


def copied_state(os_name: str, state: Any) -> dict[str, Any]:
    """Validate existing native state before any proof-field projection."""
    if state is None:
        raise UnavailableSource(os_name + ":state_missing")
    if type(state) is not dict:
        raise UnavailableSource(os_name + ":plain_state_required", BLOCKED)
    try:
        snap = _finite_json(state)
    except (TypeError, ValueError, UnicodeError, OverflowError, RecursionError):
        raise UnavailableSource(os_name + ":invalid_source_json", BLOCKED)
    original = audit_os(os_name, snap)
    if original.status == BLOCKED:
        raise UnavailableSource(os_name + ":original_validator_blocked", BLOCKED)
    if original.status not in ("RUNTIME_CHECK_PASSED", "PASS") or not original.runtime_checked:
        raise UnavailableSource(os_name + ":original_validator_not_confirmed")
    if snap.get("current_phase") != "commit":
        raise UnavailableSource(os_name + ":committed_phase_not_observed")
    return snap


def copied_edge(source: str, target: str, left: dict, right: dict) -> None:
    """Do not infer a mediator-skipping or unsigned external source edge."""
    result = audit_edge(source, target, left, right)
    if result.status == BLOCKED:
        raise UnavailableSource(source + "->" + target + ":edge_blocked", BLOCKED)
    if result.status not in ("RUNTIME_CHECK_PASSED", "PASS") or not result.runtime_checked:
        raise UnavailableSource(source + "->" + target + ":edge_unconfirmed")


def field(packet: Any, key: str, label: str) -> Any:
    if type(packet) is not dict:
        raise UnavailableSource(label + ":object_required", BLOCKED)
    if key not in packet:
        raise UnavailableSource(label + ":" + key + ":missing")
    return packet[key]


def truth(packet: Any, key: str, label: str) -> bool:
    value = field(packet, key, label)
    if type(value) is not bool:
        raise UnavailableSource(label + ":" + key + ":bool_required", BLOCKED)
    return value


def natural(packet: Any, key: str, label: str) -> int:
    value = field(packet, key, label)
    if type(value) is not int or value < 0:
        raise UnavailableSource(label + ":" + key + ":natural_required", BLOCKED)
    return value


def string(packet: Any, key: str, label: str, *, empty_allowed: bool = False) -> str:
    value = field(packet, key, label)
    if type(value) is not str or (not empty_allowed and not value.strip()):
        raise UnavailableSource(label + ":" + key + ":text_required", BLOCKED)
    return value


def plain_list(packet: Any, key: str, label: str) -> list[Any]:
    value = field(packet, key, label)
    if type(value) is not list:
        raise UnavailableSource(label + ":" + key + ":list_required", BLOCKED)
    return value


def require_match(value: Any, expected: Any, label: str) -> None:
    if type(value) is not type(expected) or value != expected:
        raise UnavailableSource(label + ":source_mismatch", BLOCKED)


def finalize(
    name: str, state: dict, projections: list[dict], paths: list[str],
    *, edge_validated: bool = False,
) -> NativeOSBindingAudit:
    """A successful source-bound LOCAL result requires existing v0.27 code."""
    if not projections:
        return fail(name, "no_observed_lean_condition_projection")
    module_stem = {
        "PlanOS": "plan", "ObserveOS": "observe",
        "VerifyOS": "verify", "LearnOS": "learn",
    }.get(name)
    if module_stem is None:
        return fail(name, "unsupported_full_source_projection")
    module = import_module(
        "runtime.kuuos_lean_python_" + module_stem + "_obligations_v0_27")
    for projection in projections:
        verdict = module.audit_witness(projection)
        if verdict.status == BLOCKED:
            return fail(name, "source_bound_lean_obligation_failed", status=BLOCKED)
        if verdict.status != "LOCAL_CONDITIONS_CHECKED":
            return fail(name, "source_bound_lean_obligation_incomplete")
    return NativeOSBindingAudit(
        os_name=name, status=PASS,
        source_digest=_fingerprint(state),
        source_field_paths=tuple(dict.fromkeys(paths)),
        checked_witnesses=len(projections),
        original_state_validated=True,
        original_edge_validated=edge_validated,
        source_bound_python_conditions_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_MAIN", "PASS", "NO_DATA", "BLOCKED",
    "UnavailableSource", "NativeOSBindingAudit",
    "fail", "copied_state", "copied_edge", "field", "truth", "natural",
    "string", "plain_list", "require_match", "finalize",
)

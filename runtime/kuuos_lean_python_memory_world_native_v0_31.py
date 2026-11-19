"""Read-only native MemoryOS/WORLD → Lean data-condition audit boundary v0.31.

No Lean proof object or issuer signature is generated. Source-bytes and
original native validators are mandatory; successful local conditions
cannot change any OS store or grant execution / truth / Git authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)

VERSION = "kuuos_lean_python_memory_world_native_v0_31"
SOURCE_PARENT = "6a7e44869d4f367cf3ffb41f75e495355d898424"
PASS = "SOURCE_BOUND_LOCAL_CHECKED"
NO_DATA = "NO_DATA"
BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class NativeMemoryWorldAudit:
    os_name: str
    status: str
    issues: tuple[str, ...] = ()
    original_source_digest: str | None = None
    checked_source_field_paths: tuple[str, ...] = ()
    local_native_validator_passed: bool = False
    lean_selected_data_conditions_checked: bool = False
    nested_lean_proof_structures_constructed: bool = False
    complete_lean_python_semantic_refinement: bool = False
    external_source_issuer_authenticated: bool = False
    external_blocker_certificate_authenticated: bool = False
    external_authorization_issuer_authenticated: bool = False
    new_world_commit_performed: bool = False
    original_source_mutated: bool = False
    truth_authority_granted: bool = False
    execution_authority_granted: bool = False
    git_authority_granted: bool = False


class SourceException(Exception):
    def __init__(self, message: str, status: str = BLOCKED):
        self.message, self.status = message, status
        super().__init__(message)


def missing(os_name: str, reason: str) -> NativeMemoryWorldAudit:
    return NativeMemoryWorldAudit(os_name, NO_DATA, (reason,))


def rejected(os_name: str, reason: str) -> NativeMemoryWorldAudit:
    return NativeMemoryWorldAudit(os_name, BLOCKED, (reason,))


def packet(item: Any, label: str) -> dict:
    if item is None:
        raise SourceException(label + ":missing", NO_DATA)
    if type(item) is not dict:
        raise SourceException(label + ":plain_dict_required")
    try:
        val = _finite_json(item)
    except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
        raise SourceException(label + ":untrusted_json")
    if type(val) is not dict:
        raise SourceException(label + ":plain_json_required")
    return val


def orig_digest(items: Any) -> str:
    return _fingerprint(items)


def check_bool(item: dict, key: str, wanted: bool, label: str) -> None:
    if key not in item or type(item[key]) is not bool or item[key] is not wanted:
        raise SourceException(label + ":" + key + ":boolean_boundary")


def match(left: Any, right: Any, label: str) -> None:
    if type(left) is not type(right) or left != right:
        raise SourceException(label + ":source_identity_mismatch")


def success(os_name: str, original: Any, paths: tuple[str, ...]) -> NativeMemoryWorldAudit:
    return NativeMemoryWorldAudit(
        os_name=os_name, status=PASS,
        original_source_digest=orig_digest(original),
        checked_source_field_paths=paths,
        local_native_validator_passed=True,
        lean_selected_data_conditions_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "PASS", "BLOCKED", "NO_DATA",
    "NativeMemoryWorldAudit", "SourceException", "missing", "rejected",
    "packet", "orig_digest", "check_bool", "match", "success",
)

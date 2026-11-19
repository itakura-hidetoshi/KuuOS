"""Read-only Lean theorem obligation projections for individual KuuOS OS modules.

An exact Lean theorem proves only its Lean statement under the required
structure/proof fields. Here the separately supplied Python *data* are
checked against selected hypothesis/conclusion fields. A matching data
packet does not construct a Lean proof term, authenticate a source, or prove
the original Python runtime is a semantic refinement of Lean.

Every OS keeps its original kernel and validator; no source is overwritten.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_os_registry_v0_5 import audit_os, get_os

VERSION = "kuuos_lean_python_per_os_contracts_v0_27"
SOURCE_MAIN = "c25f03b8ecc33df82c8ef678243cc66f0ecec90b"
LOCAL = "LOCAL_CONDITIONS_CHECKED"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"
_MISSING = object()


@dataclass(frozen=True)
class ObligationAudit:
    os_name: str
    lean_file: str
    lean_declarations: tuple[str, ...]
    status: str
    checked_fields: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    source_commit: str = SOURCE_MAIN
    scope: str = "selected Lean-structure data obligations only"
    local_conditions_checked: bool = False
    lean_python_refinement_proved: bool = False
    lean_proof_term_constructed: bool = False
    source_issuer_authenticated: bool = False
    effect_completed: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False


class Verifier:
    """Strict bounded built-in-JSON witness input; never call custom hooks.

    .flag requires Python bool, .nat Python non-bool natural, .enum an exact
    permitted literal, .le a separately checked relation. Unknown fields are
    rejected unless they are explicitly listed as part of the Lean structure.
    """

    def __init__(self, packet: Any, *, fields: tuple[str, ...]) -> None:
        self.errors: list[str] = []
        self.missing: list[str] = []
        self.checked: list[str] = []
        self.values: dict[str, Any] = {}
        self.fields = fields
        if packet is None:
            self.missing.append("witness:missing")
        elif type(packet) is not dict:
            self.errors.append("witness:plain_dict_required")
        else:
            try:
                copied = _finite_json(packet)
            except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
                self.errors.append("witness:invalid_finite_json")
            else:
                self.values = copied
                for key in copied:
                    if key not in fields:
                        self.errors.append("witness:unknown_field:" + key)

    def get(self, key: str) -> Any:
        if key not in self.values:
            if not self.errors or "witness:missing" not in self.missing:
                self.missing.append(key + ":missing")
            return _MISSING
        return self.values[key]

    def flag(self, key: str, expected: bool) -> None:
        val = self.get(key)
        if val is _MISSING:
            return
        if type(val) is not bool:
            self.errors.append(key + ":bool_required")
        elif val is not expected:
            self.errors.append(key + ":required_" + str(expected).lower())
        else:
            self.checked.append(key)

    def bool_value(self, key: str) -> bool | None:
        val = self.get(key)
        if val is _MISSING:
            return None
        if type(val) is not bool:
            self.errors.append(key + ":bool_required")
            return None
        self.checked.append(key)
        return val

    def nat(self, key: str) -> int | None:
        val = self.get(key)
        if val is _MISSING:
            return None
        if type(val) is not int or val < 0:
            self.errors.append(key + ":natural_required")
            return None
        self.checked.append(key)
        return val

    def enum(self, key: str, values: tuple[str, ...]) -> str | None:
        val = self.get(key)
        if val is _MISSING:
            return None
        if type(val) is not str or val not in values:
            self.errors.append(key + ":invalid_enum")
            return None
        self.checked.append(key)
        return val

    def string(self, key: str) -> str | None:
        val = self.get(key)
        if val is _MISSING:
            return None
        if type(val) is not str or not val.strip():
            self.errors.append(key + ":nonempty_string_required")
            return None
        self.checked.append(key)
        return val

    def require(self, relation: bool | None, code: str) -> None:
        if relation is False:
            self.errors.append(code)
        elif relation is True:
            self.checked.append(code)

    def finish(self, os_name: str, lean_file: str,
               declarations: tuple[str, ...]) -> ObligationAudit:
        status = BLOCKED if self.errors else NO_DATA if self.missing else LOCAL
        return ObligationAudit(
            os_name=os_name, lean_file=lean_file,
            lean_declarations=declarations, status=status,
            checked_fields=tuple(dict.fromkeys(self.checked)),
            errors=tuple(dict.fromkeys(self.errors)),
            missing=tuple(dict.fromkeys(self.missing)),
            local_conditions_checked=(status == LOCAL),
        )


def original_state_audit(os_name: str, state: Any) -> Any:
    """Dispatch to existing original-kernel validator; no replay or effects.

    Edge-only or source-only registered OSs remain NO_DATA unless separately
    validated by an exact typed handoff or specialized source protocol.
    """
    return audit_os(os_name, state)


def require_original_binding(os_name: str, path: str) -> bool:
    """Check a source path against the pre-existing OS registry, not a theorem."""
    link = get_os(os_name)
    return link is not None and link.lean_file == path


__all__ = [
    "VERSION", "SOURCE_MAIN", "LOCAL", "BLOCKED", "NO_DATA", "ObligationAudit",
    "Verifier", "original_state_audit", "require_original_binding",
]

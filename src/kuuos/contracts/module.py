from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Iterable, Mapping

from kuuos.kernel.identity import digest_json


_MODULE_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)+$")
_SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")


class AuthoritySurface(str, Enum):
    CANDIDATE_ONLY = "candidate_only"
    READ_ONLY = "read_only"
    ADVISORY = "advisory"
    BOUNDED_EFFECT = "bounded_effect"


class ModuleStatus(str, Enum):
    ACTIVE = "active"
    SHADOW = "shadow"
    DEPRECATED = "deprecated"
    QUARANTINED = "quarantined"


_PROTECTED_OWNERSHIP = frozenset(
    {
        "truth_authority",
        "unbounded_execution_authority",
        "constitutional_root",
        "audit_disable_authority",
        "provenance_erase_authority",
        "self_license_authority",
    }
)

_SURFACE_FORBIDDEN_OWNERSHIP: dict[AuthoritySurface, frozenset[str]] = {
    AuthoritySurface.CANDIDATE_ONLY: frozenset(
        {
            "execution_license",
            "effect_execution",
            "verification_verdict",
            "world_truth",
            "present_cycle_policy_activation",
        }
    ),
    AuthoritySurface.READ_ONLY: frozenset(
        {
            "execution_license",
            "effect_execution",
            "verification_verdict",
            "world_truth",
            "state_mutation",
            "present_cycle_policy_activation",
        }
    ),
    AuthoritySurface.ADVISORY: frozenset(
        {
            "execution_license",
            "effect_execution",
            "world_truth",
            "present_cycle_policy_activation",
        }
    ),
    AuthoritySurface.BOUNDED_EFFECT: frozenset(
        {
            "truth_authority",
            "world_truth",
            "verification_verdict",
            "constitutional_root",
        }
    ),
}


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"{field}_must_be_list")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field}_contains_invalid_string")
        items.append(item.strip())
    if len(items) != len(set(items)):
        raise ValueError(f"{field}_contains_duplicates")
    return tuple(items)


def _required_string(mapping: Mapping[str, Any], field: str) -> str:
    value = mapping.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_missing")
    return value.strip()


@dataclass(frozen=True, slots=True)
class ModuleContract:
    module_id: str
    version: str
    capability: str
    status: ModuleStatus
    authority_surface: AuthoritySurface
    provides: tuple[str, ...]
    requires: tuple[str, ...]
    owns: tuple[str, ...]
    must_not_own: tuple[str, ...]
    subscribes: tuple[str, ...]
    emits: tuple[str, ...]
    implementation: str
    validator: str
    rollback: str
    documentation: str = ""
    formal_module: str = ""

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "ModuleContract":
        if not isinstance(mapping, Mapping):
            raise ValueError("module_manifest_must_be_mapping")
        try:
            status = ModuleStatus(_required_string(mapping, "status"))
        except ValueError as error:
            raise ValueError("status_invalid") from error
        try:
            authority_surface = AuthoritySurface(
                _required_string(mapping, "authority_surface")
            )
        except ValueError as error:
            raise ValueError("authority_surface_invalid") from error
        contract = cls(
            module_id=_required_string(mapping, "id"),
            version=_required_string(mapping, "version"),
            capability=_required_string(mapping, "capability"),
            status=status,
            authority_surface=authority_surface,
            provides=_string_tuple(mapping.get("provides"), "provides"),
            requires=_string_tuple(mapping.get("requires"), "requires"),
            owns=_string_tuple(mapping.get("owns"), "owns"),
            must_not_own=_string_tuple(mapping.get("must_not_own"), "must_not_own"),
            subscribes=_string_tuple(mapping.get("subscribes"), "subscribes"),
            emits=_string_tuple(mapping.get("emits"), "emits"),
            implementation=_required_string(mapping, "implementation"),
            validator=_required_string(mapping, "validator"),
            rollback=_required_string(mapping, "rollback"),
            documentation=str(mapping.get("documentation", "")).strip(),
            formal_module=str(mapping.get("formal_module", "")).strip(),
        )
        errors = contract.validate()
        if errors:
            raise ValueError("module_contract_invalid:" + ";".join(errors))
        return contract

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not _MODULE_ID_RE.fullmatch(self.module_id):
            errors.append("module_id_invalid")
        if not _SEMVER_RE.fullmatch(self.version):
            errors.append("version_not_semver")
        if not self.capability or "." not in self.capability:
            errors.append("capability_invalid")
        if not self.provides:
            errors.append("provides_empty")
        if self.capability not in self.provides:
            errors.append("primary_capability_not_provided")
        overlap = set(self.owns) & set(self.must_not_own)
        if overlap:
            errors.append("ownership_contradiction:" + ",".join(sorted(overlap)))
        protected = set(self.owns) & _PROTECTED_OWNERSHIP
        if protected:
            errors.append("protected_ownership_claimed:" + ",".join(sorted(protected)))
        surface_forbidden = set(self.owns) & _SURFACE_FORBIDDEN_OWNERSHIP[
            self.authority_surface
        ]
        if surface_forbidden:
            errors.append(
                "authority_surface_ownership_violation:"
                + ",".join(sorted(surface_forbidden))
            )
        missing_surface_boundary = (
            _SURFACE_FORBIDDEN_OWNERSHIP[self.authority_surface]
            - set(self.must_not_own)
        )
        if missing_surface_boundary:
            errors.append(
                "authority_surface_boundary_incomplete:"
                + ",".join(sorted(missing_surface_boundary))
            )
        if self.status is ModuleStatus.ACTIVE and not self.rollback:
            errors.append("active_module_rollback_missing")
        return errors

    def to_mapping(self) -> dict[str, Any]:
        return {
            "id": self.module_id,
            "version": self.version,
            "capability": self.capability,
            "status": self.status.value,
            "authority_surface": self.authority_surface.value,
            "provides": list(self.provides),
            "requires": list(self.requires),
            "owns": list(self.owns),
            "must_not_own": list(self.must_not_own),
            "subscribes": list(self.subscribes),
            "emits": list(self.emits),
            "implementation": self.implementation,
            "validator": self.validator,
            "rollback": self.rollback,
            "documentation": self.documentation,
            "formal_module": self.formal_module,
        }

    @property
    def identity(self) -> str:
        return f"{self.module_id}@{self.version}"

    @property
    def digest(self) -> str:
        return digest_json(self.to_mapping())


def validate_contract_set(contracts: Iterable[ModuleContract]) -> list[str]:
    errors: list[str] = []
    identities: set[str] = set()
    module_ids: set[str] = set()
    active_capability_providers: dict[str, list[str]] = {}
    for contract in contracts:
        if contract.identity in identities:
            errors.append(f"duplicate_identity:{contract.identity}")
        identities.add(contract.identity)
        if contract.module_id in module_ids:
            errors.append(f"duplicate_module_id:{contract.module_id}")
        module_ids.add(contract.module_id)
        if contract.status is ModuleStatus.ACTIVE:
            for capability in contract.provides:
                active_capability_providers.setdefault(capability, []).append(
                    contract.module_id
                )
    for capability, providers in sorted(active_capability_providers.items()):
        if len(providers) > 1:
            errors.append(
                f"ambiguous_active_provider:{capability}:" + ",".join(sorted(providers))
            )
    return errors

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
import re
from typing import Any, Mapping, Sequence

MODULE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")

ALLOWED_STATUSES = {
    "discovered",
    "contract_validated",
    "sandboxed",
    "shadow",
    "canary",
    "active",
    "deprecated",
    "quarantined",
    "rolled_back",
    "archived",
}

ALLOWED_AUTHORITY_SURFACES = {
    "candidate_only",
    "read_only",
    "advisory",
    "bounded_effect",
    "formal_read_only",
}

PERMANENTLY_FORBIDDEN_OWNERSHIP = {
    "truth_authority",
    "constitutional_root_write",
    "unbounded_execution_authority",
    "audit_disable_authority",
    "provenance_erasure_authority",
    "rollback_removal_authority",
}

REQUIRED_BOUNDARY_KEYS = {
    "candidate_is_authority",
    "event_delivery_is_state_adoption",
    "learning_is_present_cycle_mutation",
    "memory_is_belief_sovereignty",
    "self_license_allowed",
    "audit_disable_allowed",
    "provenance_erasure_allowed",
    "rollback_removal_allowed",
}


class ModuleContractError(ValueError):
    """Raised when a module manifest violates the v0.60 contract."""


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ModuleContractError(f"{field}_must_be_a_sequence")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ModuleContractError(f"{field}_contains_invalid_value")
        result.append(item.strip())
    if len(result) != len(set(result)):
        raise ModuleContractError(f"{field}_contains_duplicates")
    return tuple(result)


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ModuleContractError(f"{field}_must_be_an_object")
    return {str(key): item for key, item in value.items()}


@dataclass(frozen=True)
class ModuleContract:
    schema_version: str
    module_id: str
    version: str
    status: str
    capability: str
    provides: tuple[str, ...]
    requires: tuple[str, ...]
    subscribes: tuple[str, ...]
    emits: tuple[str, ...]
    owns: tuple[str, ...]
    must_not_own: tuple[str, ...]
    authority_surface: str
    self_authorizing: bool
    direct_effect_authority: bool
    implementation: str
    validator: str
    formal_module: str
    rollback: str
    boundaries: Mapping[str, bool]
    manifest_path: str = ""

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
        *,
        manifest_path: str = "",
    ) -> "ModuleContract":
        data = _mapping(value, "manifest")
        boundary_data = _mapping(data.get("boundaries", {}), "boundaries")
        boundaries: dict[str, bool] = {}
        for key, item in boundary_data.items():
            if not isinstance(item, bool):
                raise ModuleContractError(f"boundary_{key}_must_be_boolean")
            boundaries[key] = item

        contract = cls(
            schema_version=str(data.get("schema_version", "")),
            module_id=str(data.get("module_id", "")),
            version=str(data.get("version", "")),
            status=str(data.get("status", "")),
            capability=str(data.get("capability", "")),
            provides=_string_tuple(data.get("provides", ()), "provides"),
            requires=_string_tuple(data.get("requires", ()), "requires"),
            subscribes=_string_tuple(data.get("subscribes", ()), "subscribes"),
            emits=_string_tuple(data.get("emits", ()), "emits"),
            owns=_string_tuple(data.get("owns", ()), "owns"),
            must_not_own=_string_tuple(data.get("must_not_own", ()), "must_not_own"),
            authority_surface=str(data.get("authority_surface", "")),
            self_authorizing=data.get("self_authorizing") is True,
            direct_effect_authority=data.get("direct_effect_authority") is True,
            implementation=str(data.get("implementation", "")),
            validator=str(data.get("validator", "")),
            formal_module=str(data.get("formal_module", "")),
            rollback=str(data.get("rollback", "")),
            boundaries=boundaries,
            manifest_path=manifest_path,
        )
        errors = contract.validation_errors()
        if errors:
            raise ModuleContractError(";".join(errors))
        return contract

    @classmethod
    def from_json_file(cls, path: pathlib.Path) -> "ModuleContract":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ModuleContractError("manifest_not_found") from exc
        except json.JSONDecodeError as exc:
            raise ModuleContractError("manifest_invalid_json") from exc
        if not isinstance(raw, Mapping):
            raise ModuleContractError("manifest_root_must_be_an_object")
        return cls.from_mapping(raw, manifest_path=str(path))

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        if self.schema_version != "kuuos_module_contract_v0_60":
            errors.append("schema_version_invalid")
        if not MODULE_ID_RE.fullmatch(self.module_id):
            errors.append("module_id_invalid")
        if not SEMVER_RE.fullmatch(self.version):
            errors.append("version_invalid")
        if self.status not in ALLOWED_STATUSES:
            errors.append("status_invalid")
        if not MODULE_ID_RE.fullmatch(self.capability):
            errors.append("capability_invalid")
        if not self.provides:
            errors.append("provides_empty")
        if self.authority_surface not in ALLOWED_AUTHORITY_SURFACES:
            errors.append("authority_surface_invalid")
        if self.self_authorizing:
            errors.append("self_authorization_forbidden")
        if self.capability != "act" and self.direct_effect_authority:
            errors.append("non_act_direct_effect_authority_forbidden")
        if self.authority_surface != "bounded_effect" and self.direct_effect_authority:
            errors.append("direct_effect_requires_bounded_effect_surface")
        if set(self.owns) & set(self.must_not_own):
            errors.append("ownership_conflicts_with_must_not_own")
        if set(self.owns) & PERMANENTLY_FORBIDDEN_OWNERSHIP:
            errors.append("permanently_forbidden_ownership")
        if not self.implementation:
            errors.append("implementation_missing")
        if not self.validator:
            errors.append("validator_missing")
        if not self.formal_module:
            errors.append("formal_module_missing")
        if not self.rollback:
            errors.append("rollback_target_missing")
        missing_boundaries = REQUIRED_BOUNDARY_KEYS - set(self.boundaries)
        if missing_boundaries:
            errors.append("required_boundaries_missing:" + ",".join(sorted(missing_boundaries)))
        for key in REQUIRED_BOUNDARY_KEYS:
            if self.boundaries.get(key) is not False:
                errors.append(f"boundary_{key}_must_be_false")
        return errors

    def to_manifest_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("manifest_path", None)
        data["provides"] = list(self.provides)
        data["requires"] = list(self.requires)
        data["subscribes"] = list(self.subscribes)
        data["emits"] = list(self.emits)
        data["owns"] = list(self.owns)
        data["must_not_own"] = list(self.must_not_own)
        data["boundaries"] = dict(self.boundaries)
        return data

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_manifest_dict())

    @property
    def coordinate(self) -> str:
        return f"{self.module_id}@{self.version}"

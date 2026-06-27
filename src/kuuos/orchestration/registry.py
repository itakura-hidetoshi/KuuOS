from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable

from kuuos.contracts.module import ModuleContract, ModuleStatus, validate_contract_set
from kuuos.kernel.identity import digest_json


class RegistryConflictError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class RegistrySnapshot:
    modules: tuple[ModuleContract, ...]
    digest: str


class CapabilityRegistry:
    def __init__(self, contracts: Iterable[ModuleContract] = ()):
        self._contracts: dict[str, ModuleContract] = {}
        for contract in contracts:
            self.register(contract)

    def register(self, contract: ModuleContract) -> bool:
        existing = self._contracts.get(contract.module_id)
        if existing is not None:
            if existing.digest == contract.digest:
                return False
            raise RegistryConflictError(
                f"module_id_already_registered:{contract.module_id}"
            )
        trial = [*self._contracts.values(), contract]
        errors = validate_contract_set(trial)
        if errors:
            raise RegistryConflictError("registry_contract_conflict:" + ";".join(errors))
        self._contracts[contract.module_id] = contract
        return True

    @classmethod
    def from_manifest_directory(cls, directory: str | Path) -> "CapabilityRegistry":
        path = Path(directory)
        if not path.is_dir():
            raise FileNotFoundError(f"module_manifest_directory_missing:{path}")
        contracts: list[ModuleContract] = []
        for manifest_path in sorted(path.glob("*.json")):
            try:
                value = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"module_manifest_json_invalid:{manifest_path}"
                ) from error
            contracts.append(ModuleContract.from_mapping(value))
        if not contracts:
            raise ValueError("module_manifest_directory_empty")
        return cls(contracts)

    def module(self, module_id: str) -> ModuleContract:
        try:
            return self._contracts[module_id]
        except KeyError as error:
            raise KeyError(f"module_not_registered:{module_id}") from error

    def providers(
        self,
        capability: str,
        *,
        include_shadow: bool = False,
    ) -> tuple[ModuleContract, ...]:
        allowed = {ModuleStatus.ACTIVE}
        if include_shadow:
            allowed.add(ModuleStatus.SHADOW)
        return tuple(
            sorted(
                (
                    contract
                    for contract in self._contracts.values()
                    if capability in contract.provides and contract.status in allowed
                ),
                key=lambda contract: contract.identity,
            )
        )

    def active_provider(self, capability: str) -> ModuleContract:
        providers = self.providers(capability)
        if not providers:
            raise KeyError(f"active_provider_missing:{capability}")
        if len(providers) > 1:
            raise RegistryConflictError(f"active_provider_ambiguous:{capability}")
        return providers[0]

    @property
    def modules(self) -> tuple[ModuleContract, ...]:
        return tuple(sorted(self._contracts.values(), key=lambda item: item.identity))

    def snapshot(self) -> RegistrySnapshot:
        modules = self.modules
        digest = digest_json([contract.to_mapping() for contract in modules])
        return RegistrySnapshot(modules=modules, digest=digest)

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from kuuos.contracts.module import ModuleContract
from kuuos.kernel.identity import digest_json
from kuuos.orchestration.registry import CapabilityRegistry


class DependencyResolutionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DependencyPlan:
    requested_capabilities: tuple[str, ...]
    ordered_modules: tuple[ModuleContract, ...]
    external_capabilities: tuple[str, ...]
    digest: str

    @property
    def module_ids(self) -> tuple[str, ...]:
        return tuple(module.module_id for module in self.ordered_modules)


class DependencyResolver:
    def __init__(
        self,
        registry: CapabilityRegistry,
        *,
        external_capabilities: Iterable[str] = (),
    ):
        self.registry = registry
        self.external_capabilities = frozenset(external_capabilities)

    def resolve(self, requested_capabilities: Iterable[str]) -> DependencyPlan:
        requested = tuple(dict.fromkeys(requested_capabilities))
        if not requested:
            raise DependencyResolutionError("requested_capabilities_empty")
        ordered: list[ModuleContract] = []
        permanently_marked: set[str] = set()
        temporarily_marked: set[str] = set()

        def visit_capability(capability: str, lineage: tuple[str, ...]) -> None:
            if capability in self.external_capabilities:
                return
            try:
                provider = self.registry.active_provider(capability)
            except KeyError as error:
                path = "->".join((*lineage, capability))
                raise DependencyResolutionError(
                    f"capability_unresolved:{path}"
                ) from error
            visit_module(provider, lineage)

        def visit_module(module: ModuleContract, lineage: tuple[str, ...]) -> None:
            if module.module_id in permanently_marked:
                return
            if module.module_id in temporarily_marked:
                path = "->".join((*lineage, module.module_id))
                raise DependencyResolutionError(f"dependency_cycle:{path}")
            temporarily_marked.add(module.module_id)
            for requirement in module.requires:
                visit_capability(requirement, (*lineage, module.module_id))
            temporarily_marked.remove(module.module_id)
            permanently_marked.add(module.module_id)
            ordered.append(module)

        for capability in requested:
            visit_capability(capability, ())
        payload = {
            "requested_capabilities": list(requested),
            "ordered_modules": [module.identity for module in ordered],
            "external_capabilities": sorted(self.external_capabilities),
        }
        return DependencyPlan(
            requested_capabilities=requested,
            ordered_modules=tuple(ordered),
            external_capabilities=tuple(sorted(self.external_capabilities)),
            digest=digest_json(payload),
        )

"""KuuOS modular evolution mesh foundations."""

from .contracts.module import AuthoritySurface, ModuleContract, ModuleStatus
from .orchestration.dependency_graph import DependencyPlan, DependencyResolver
from .orchestration.registry import CapabilityRegistry

__all__ = [
    "AuthoritySurface",
    "CapabilityRegistry",
    "DependencyPlan",
    "DependencyResolver",
    "ModuleContract",
    "ModuleStatus",
]

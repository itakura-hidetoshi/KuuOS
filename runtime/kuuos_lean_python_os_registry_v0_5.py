"""Repository-resident Lean-to-Python OS contract index (read-only, v0.5).

Existing Lean theorems are conditional formal statements; this index does not
prove Python refinement, authenticate receipts, alter OS kernels, or grant
execution, truth, clinical, Git, or merge authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    ADDITIONAL_PROOF_LINKS,
    CORE_CONTRACTS,
    BLOCKED,
    NO_DATA,
    PASSED,
    audit_core_state,
    codeai_selection_boundary_check,
    memory_blocker_boundary_check,
)
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import (
    HANDOFF_CONTRACTS,
    audit_handoff,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import (
    EDGE_SPECS,
    STATE_SPECS,
    audit_decision_plan_edge,
)
from runtime.kuuos_lean_python_plan_act_admission_v0_4 import (
    audit_plan_act_admission,
)

VERSION = "kuuos_lean_python_os_registry_v0_5"
SOURCE_REPOSITORY = "itakura-hidetoshi/KuuOS"
BASE_MAIN_COMMIT = "8346fe07075e3cf260ffb922a79d08b8e74e306d"
GOOD = frozenset((PASSED, "PASS"))


@dataclass(frozen=True)
class OSBinding:
    name: str
    lean_file: str
    theorem_names: tuple[str, ...]
    runtime_module: str
    audit_kind: str
    scope: str

    @property
    def python_path(self) -> str:
        return self.runtime_module.replace(".", "/") + ".py"


@dataclass(frozen=True)
class EdgeBinding:
    source: str
    target: str
    lean_files: tuple[str, ...]
    theorem_names: tuple[str, ...]
    audit_module: str
    receipt_required: bool


@dataclass(frozen=True)
class ScopedAudit:
    status: str
    name: str
    scope: str
    original_status: str
    issues: tuple[str, ...] = ()
    runtime_checked: bool = False
    lean_python_refinement_proved: bool = False
    truth_authority_granted: bool = False
    execution_authority_granted: bool = False
    merge_authority_granted: bool = False


def _build_os_bindings() -> dict[str, OSBinding]:
    result: dict[str, OSBinding] = {}
    for name, contract in CORE_CONTRACTS.items():
        result[name] = OSBinding(
            name=name, lean_file=contract.lean_source,
            theorem_names=(
                contract.phase_theorem, contract.event_theorem,
                contract.authority_theorem,
            ),
            runtime_module=contract.runtime_kernel,
            audit_kind="core_original_validator",
            scope="bounded_existing_core_state_only",
        )
    for name, (lean_file, theorem, runtime) in ADDITIONAL_PROOF_LINKS.items():
        result[name] = OSBinding(
            name=name, lean_file=lean_file,
            theorem_names=(theorem,) if theorem else (),
            runtime_module=runtime,
            audit_kind=("memory_blocker_projection" if name == "MemoryOS"
                        else "codeai_selection_projection" if name == "CodeAI"
                        else "source_reference_only"),
            scope=("no_standalone_runtime_equivalence_claim" if name == "WORLD"
                   else "selected_boundary_projection_not_full_kernel"),
        )
    result["DecisionOSPlural"] = OSBinding(
        name="DecisionOSPlural",
        lean_file=EDGE_SPECS[("DecisionOS", "DecisionOSPlural")].lean_source,
        theorem_names=EDGE_SPECS[("DecisionOS", "DecisionOSPlural")].theorem_names,
        runtime_module="runtime.kuuos_decision_os_plural_kernel_v0_2",
        audit_kind="edge_only",
        scope="DecisionOS_to_Plural_with_original_validators",
    )
    result["DecisionOSWa"] = OSBinding(
        name="DecisionOSWa",
        lean_file=EDGE_SPECS[("DecisionOSPlural", "DecisionOSWa")].lean_source,
        theorem_names=EDGE_SPECS[("DecisionOSPlural", "DecisionOSWa")].theorem_names,
        runtime_module="runtime.kuuos_decision_os_wa_kernel_v0_3",
        audit_kind="edge_only",
        scope="Plural_to_Wa_with_original_validators",
    )
    return result


OS_BINDINGS = MappingProxyType(_build_os_bindings())


def _build_edges() -> dict[tuple[str, str], EdgeBinding]:
    edges: dict[tuple[str, str], EdgeBinding] = {}
    for (source, target), contract in HANDOFF_CONTRACTS.items():
        edges[(source, target)] = EdgeBinding(
            source=source, target=target, lean_files=(contract.lean_source,),
            theorem_names=(contract.premise_theorem, contract.lineage_theorem),
            audit_module="runtime.kuuos_lean_python_lineage_handoff_v0_2",
            receipt_required=False,
        )
    for (source, target), spec in EDGE_SPECS.items():
        edges[(source, target)] = EdgeBinding(
            source=source, target=target, lean_files=(spec.lean_source,),
            theorem_names=spec.theorem_names,
            audit_module="runtime.kuuos_lean_python_decision_plan_handoff_v0_3",
            receipt_required=(source == "DecisionOSWa" and target == "PlanOS"),
        )
    edges[("PlanOS", "ActOS")] = EdgeBinding(
        source="PlanOS", target="ActOS",
        lean_files=(
            OS_BINDINGS["PlanOS"].lean_file, OS_BINDINGS["ActOS"].lean_file,
        ),
        theorem_names=(
            "planActivation_requires_plan_phase",
            "planActivation_does_not_execute",
            "invocation_requires_committed_plan",
            "invocation_requires_host_license",
        ),
        audit_module="runtime.kuuos_lean_python_plan_act_admission_v0_4",
        receipt_required=True,
    )
    return edges


EDGES = MappingProxyType(_build_edges())


def list_os() -> tuple[str, ...]:
    """Return OS names covered by the selected (not exhaustive) formal links."""
    return tuple(sorted(OS_BINDINGS))


def list_edges() -> tuple[tuple[str, str], ...]:
    return tuple(sorted(EDGES))


def get_os(name: str) -> OSBinding | None:
    return OS_BINDINGS.get(name)


def get_edge(source: str, target: str) -> EdgeBinding | None:
    return EDGES.get((source, target))


def _view(name: str, scope: str, original: Any) -> ScopedAudit:
    status = getattr(original, "status", NO_DATA)
    original_issues = (getattr(original, "issues", ())
                       or getattr(original, "violations", ()))
    missing = getattr(original, "missing", ())
    issues = tuple(map(str, original_issues)) + tuple(map(str, missing))
    # A successful source/target equality is not a formal refinement result.
    runtime_checked = (status in GOOD
                       and not issues
                       and getattr(original, "runtime_checked", True))
    return ScopedAudit(
        status=status, name=name, scope=scope,
        original_status=str(status), issues=issues,
        runtime_checked=runtime_checked,
    )


def _absent(name: str, reason: str) -> ScopedAudit:
    return ScopedAudit(
        status=NO_DATA, name=name, scope=reason,
        original_status=NO_DATA, issues=(reason,),
    )


def audit_os(name: str, state: Any) -> ScopedAudit:
    """Read-only dispatch; never invent a full-state validator for edge-only OS."""
    contract = get_os(name)
    if contract is None:
        return _absent(name, "os_contract_not_registered")
    if contract.audit_kind == "source_reference_only":
        return _absent(name, "source_reference_only_no_runtime_equivalence")
    if contract.audit_kind == "edge_only":
        return _absent(name, "typed_source_target_edge_required")
    try:
        if contract.audit_kind == "core_original_validator":
            original = audit_core_state(name, state)
        elif contract.audit_kind == "memory_blocker_projection":
            original = memory_blocker_boundary_check(state)
        elif contract.audit_kind == "codeai_selection_projection":
            original = codeai_selection_boundary_check(state)
        else:
            return _absent(name, "unsupported_audit_kind")
    except (ValueError, TypeError, AttributeError, RecursionError) as exc:
        return ScopedAudit(
            status=BLOCKED, name=name, scope=contract.scope,
            original_status=BLOCKED,
            issues=("validator_exception:" + type(exc).__name__,),
        )
    return _view(name, contract.scope, original)


def audit_edge(
    source: str, target: str, source_state: Any, target_state: Any,
    *, activation_receipt: Any = None,
) -> ScopedAudit:
    """One exact edge only. No shortcut or automatic effect/authority grant."""
    contract = get_edge(source, target)
    edge_name = source + "->" + target
    if contract is None:
        return _absent(edge_name, "unsupported_edge_no_descent")
    if contract.receipt_required and activation_receipt is None:
        return _absent(edge_name, "original_activation_receipt_required")
    try:
        if (source, target) == ("PlanOS", "ActOS"):
            original = audit_plan_act_admission(
                source_state, activation_receipt, target_state,
            )
        elif (source, target) in HANDOFF_CONTRACTS:
            original = audit_handoff(
                source, target, source_state, target_state,
            )
        else:
            original = audit_decision_plan_edge(
                source, target, source_state, target_state,
                replan_activation_receipt=activation_receipt,
            )
    except (ValueError, TypeError, AttributeError, RecursionError) as exc:
        return ScopedAudit(
            status=BLOCKED, name=edge_name, scope="typed_edge_observation",
            original_status=BLOCKED,
            issues=("edge_validator_exception:" + type(exc).__name__,),
        )
    return _view(edge_name, "existing_exact_edge_audit_only", original)


__all__ = [
    "VERSION", "SOURCE_REPOSITORY", "BASE_MAIN_COMMIT",
    "OSBinding", "EdgeBinding", "ScopedAudit", "OS_BINDINGS", "EDGES",
    "list_os", "list_edges", "get_os", "get_edge", "audit_os", "audit_edge",
]

#!/usr/bin/env python3
from __future__ import annotations

import runtime.kuuos_current_check_v0_95 as _base

# Canonical public-surface metadata. The functional milestone commit is the
# merged MemoryOS v1.00 state; documentation-only synchronization may advance
# main without changing this subsystem frontier.
_base.CURRENT_BASELINE_DATE = "2026-07-16 JST"
_base.CURRENT_ROOT_SEQUENCE_FRONTIER = "kuuos_current_root_sequence_v0_113"
_base.CURRENT_REPOSITORY_FRONTIER = "self-organization v0.113"
_base.CURRENT_PLANOS_FRONTIER = "PlanOS v1.23"
_base.CURRENT_DECISIONOS_FRONTIER = "DecisionOS v0.6"
_base.CURRENT_MEMORYOS_FRONTIER = "MemoryOS v1.00"
_base.CURRENT_WORLD_DEPENDENCY = "KuuOS v14.0 causal WORLD state"
_base.CURRENT_MAIN_FRONTIER = _base.CURRENT_REPOSITORY_FRONTIER
_base.CURRENT_DRAFT_FRONTIER = "none"
_base.CURRENT_DRAFT_PR = "none"
_base.CURRENT_DRAFT_BRANCH = "none"
_base.CURRENT_FUNCTIONAL_MILESTONE_COMMIT = (
    "7a5c9308cd7089e4ce96d3cbbd8b88f8f6ae26a4"
)
_base.CURRENT_LATEST_FUNCTIONAL_PR = 1277
_base.CURRENT_SUPPORTED_PROFILES = (
    "all",
    "repository",
    "planos",
    "decisionos",
    "memoryos",
)
_base.CURRENT_PUBLIC_SURFACES = (
    "README.md",
    "ROADMAP.md",
    "runtime/kuuos_current_check.py",
)
_base.CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_finite_bounded_closed_support_"
    "lattice_certificate_kernel_v0_1.py"
)

_NEW_STEPS = (
    (
        "memoryos-v0-96-pointed-choice-free-signature-lattice",
        "scripts/check_planos_memoryos_pointed_choice_free_signature_"
        "lattice_certificate_kernel_v0_1.py",
    ),
    (
        "memoryos-v0-97-finite-family-signature-lattice",
        "scripts/check_planos_memoryos_finite_family_signature_"
        "lattice_certificate_kernel_v0_1.py",
    ),
    (
        "memoryos-v0-98-sensor-kernel-polarity",
        "scripts/check_planos_memoryos_sensor_kernel_polarity_"
        "certificate_kernel_v0_1.py",
    ),
    (
        "memoryos-v0-99-closed-support-representable-kernel-order-iso",
        "scripts/check_planos_memoryos_closed_support_representable_kernel_"
        "order_iso_certificate_kernel_v0_1.py",
    ),
    (
        "memoryos-v1-00-finite-bounded-closed-support-lattice",
        "scripts/check_planos_memoryos_finite_bounded_closed_support_"
        "lattice_certificate_kernel_v0_1.py",
    ),
)

for _step in _NEW_STEPS:
    if _step not in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS:
        _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS = (
            _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS + (_step,)
        )

_base.MEMORYOS_ACTIVE_FRONTIER_STEPS = tuple(
    _base._script_step(step_id, target, f"Validate {step_id}.")
    for step_id, target in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS
)
_base.CURRENT_ROOT_STEPS = (
    _base.REPOSITORY_LINEAGE_STEPS
    + _base.PLANOS_ACTIVE_FRONTIER_STEPS
    + _base.DECISIONOS_ACTIVE_FRONTIER_STEPS
    + _base.MEMORYOS_ACTIVE_FRONTIER_STEPS
)

_original_current_runtime_root_summary = _base.current_runtime_root_summary


def _current_runtime_root_summary_v1_00() -> dict[str, object]:
    summary = dict(_original_current_runtime_root_summary())
    summary.update(
        {
            "functional_milestone_commit": _base.CURRENT_FUNCTIONAL_MILESTONE_COMMIT,
            "latest_functional_pr": _base.CURRENT_LATEST_FUNCTIONAL_PR,
            "supported_profiles": list(_base.CURRENT_SUPPORTED_PROFILES),
            "public_surfaces": list(_base.CURRENT_PUBLIC_SURFACES),
            "current_frontier_artifact": _base.CURRENT_FRONTIER_ARTIFACT,
        }
    )
    return summary


_base.current_runtime_root_summary = _current_runtime_root_summary_v1_00

for _name, _value in vars(_base).items():
    if not _name.startswith("__"):
        globals()[_name] = _value


if __name__ == "__main__":
    raise SystemExit(_base.main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

import runtime.kuuos_current_check_v0_95 as _base

# Canonical public-surface metadata.
#
# The repository/PlanOS/DecisionOS/MemoryOS frontiers remain independently
# versioned.  CodeAI is an additive application profile.  The current main
# frontier records the latest integrated functional PR, while the draft fields
# report the active, non-authoritative successor separately.
_base.CURRENT_BASELINE_DATE = "2026-07-23 JST"
_base.CURRENT_ROOT_SEQUENCE_FRONTIER = "kuuos_current_root_sequence_v0_113"
_base.CURRENT_REPOSITORY_FRONTIER = "self-organization v0.113"
_base.CURRENT_PLANOS_FRONTIER = "PlanOS v1.23"
_base.CURRENT_DECISIONOS_FRONTIER = "DecisionOS v0.6"
_base.CURRENT_MEMORYOS_FRONTIER = "MemoryOS v1.00"
_base.CURRENT_CODEAI_FRONTIER = (
    "CodeAI Baseline-versus-CodeAI and Ablation Comparison v0.1"
)
_base.CURRENT_WORLD_DEPENDENCY = "KuuOS v14.0 causal WORLD state"
_base.CURRENT_MAIN_FRONTIER = _base.CURRENT_CODEAI_FRONTIER
_base.CURRENT_DRAFT_FRONTIER = (
    "CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1"
)
_base.CURRENT_DRAFT_PR = 1342
_base.CURRENT_DRAFT_BRANCH = (
    "codeai/frozen-cohort-prediction-pack-execution-shard-contract-v0-1"
)
_base.CURRENT_DRAFT_BASE_SHA = "083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7"
_base.CURRENT_DRAFT_HEAD_SHA = "daa88b75be2cdb66ce706fcf08be8723a34594e7"
_base.CURRENT_FUNCTIONAL_MILESTONE_COMMIT = (
    "083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7"
)
_base.CURRENT_LATEST_FUNCTIONAL_PR = 1341
_base.CURRENT_SUPPORTED_PROFILES = (
    "all",
    "repository",
    "planos",
    "decisionos",
    "memoryos",
    "codeai",
)
_base.CURRENT_PUBLIC_SURFACES = (
    "README.md",
    "ROADMAP.md",
    "runtime/kuuos_current_check.py",
)
_base.CURRENT_FRONTIER_ARTIFACT = (
    "manifests/kuuos_codeai_baseline_versus_codeai_"
    "ablation_comparison_v0_1.json"
)
_base.CURRENT_FRONTIER_MODE = "integrated_active_frontiers_with_codeai"
_base.CURRENT_FRONTIER_BOUNDARY = "validation_only"

_NEW_MEMORYOS_STEPS = (
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

for _step in _NEW_MEMORYOS_STEPS:
    if _step not in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS:
        _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS = (
            _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS + (_step,)
        )

_base.MEMORYOS_ACTIVE_FRONTIER_STEPS = tuple(
    _base._script_step(step_id, target, f"Validate {step_id}.")
    for step_id, target in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS
)

_base.CODEAI_CURRENT_FRONTIER_STEPS = (
    _base._script_step(
        "codeai-v0-1-baseline-ablation-comparison-projection",
        "scripts/check_codeai_baseline_versus_codeai_"
        "ablation_comparison_v0_1.py",
        "Validate the deterministic PR #1341 comparison projection.",
    ),
    _base.CurrentRootStep(
        "codeai-v0-1-baseline-ablation-comparison-tests",
        "unittest",
        "tests.test_kuuos_codeai_baseline_versus_codeai_"
        "ablation_comparison_v0_1",
        True,
        "Validate the current comparison contract and boundary routes.",
    ),
    _base.CurrentRootStep(
        "codeai-v0-1-external-result-ingestion-regression",
        "unittest",
        "tests.test_kuuos_codeai_external_result_process_"
        "evidence_ingestion_v0_1",
        True,
        "Revalidate aggregate result and process-evidence ingestion.",
    ),
    _base.CurrentRootStep(
        "codeai-v0-1-bounded-official-harness-regression",
        "unittest",
        "tests.test_kuuos_codeai_bounded_official_harness_execution_v0_1",
        True,
        "Revalidate the bounded non-gold official harness contract.",
    ),
    _base.CurrentRootStep(
        "codeai-v0-1-gold-smoke-regression",
        "unittest",
        "tests.test_kuuos_codeai_gold_patch_environment_smoke_validation_v0_1",
        True,
        "Revalidate the evaluator-only gold environment smoke contract.",
    ),
    _base.CurrentRootStep(
        "codeai-v0-1-external-corpus-freeze-regression",
        "unittest",
        "tests.test_kuuos_codeai_external_corpus_acquisition_"
        "freeze_receipt_v0_1",
        True,
        "Revalidate the pinned corpus freeze and field-isolation contract.",
    ),
)

_base.CURRENT_ROOT_STEPS = (
    _base.REPOSITORY_LINEAGE_STEPS
    + _base.PLANOS_ACTIVE_FRONTIER_STEPS
    + _base.DECISIONOS_ACTIVE_FRONTIER_STEPS
    + _base.MEMORYOS_ACTIVE_FRONTIER_STEPS
    + _base.CODEAI_CURRENT_FRONTIER_STEPS
)

_original_current_runtime_root_summary = _base.current_runtime_root_summary


def current_runtime_root_summary() -> dict[str, object]:
    summary = dict(_original_current_runtime_root_summary())
    summary.update(
        {
            "baseline_date": _base.CURRENT_BASELINE_DATE,
            "repository_root_sequence": _base.CURRENT_ROOT_SEQUENCE_FRONTIER,
            "repository_frontier": _base.CURRENT_REPOSITORY_FRONTIER,
            "planos_frontier": _base.CURRENT_PLANOS_FRONTIER,
            "decisionos_frontier": _base.CURRENT_DECISIONOS_FRONTIER,
            "memoryos_frontier": _base.CURRENT_MEMORYOS_FRONTIER,
            "codeai_frontier": _base.CURRENT_CODEAI_FRONTIER,
            "world_dependency": _base.CURRENT_WORLD_DEPENDENCY,
            "main_frontier": _base.CURRENT_MAIN_FRONTIER,
            "draft_frontier": _base.CURRENT_DRAFT_FRONTIER,
            "draft_pr": _base.CURRENT_DRAFT_PR,
            "draft_branch": _base.CURRENT_DRAFT_BRANCH,
            "draft_base_sha": _base.CURRENT_DRAFT_BASE_SHA,
            "draft_head_sha": _base.CURRENT_DRAFT_HEAD_SHA,
            "functional_milestone_commit": (
                _base.CURRENT_FUNCTIONAL_MILESTONE_COMMIT
            ),
            "latest_functional_pr": _base.CURRENT_LATEST_FUNCTIONAL_PR,
            "supported_profiles": list(_base.CURRENT_SUPPORTED_PROFILES),
            "public_surfaces": list(_base.CURRENT_PUBLIC_SURFACES),
            "current_frontier_artifact": _base.CURRENT_FRONTIER_ARTIFACT,
            "repository_step_count": len(_base.REPOSITORY_LINEAGE_STEPS),
            "planos_step_count": len(_base.PLANOS_ACTIVE_FRONTIER_STEPS),
            "decisionos_step_count": len(_base.DECISIONOS_ACTIVE_FRONTIER_STEPS),
            "memoryos_step_count": len(_base.MEMORYOS_ACTIVE_FRONTIER_STEPS),
            "codeai_step_count": len(_base.CODEAI_CURRENT_FRONTIER_STEPS),
            "total_step_count": len(_base.CURRENT_ROOT_STEPS),
            "frontier_mode": _base.CURRENT_FRONTIER_MODE,
            "frontier_boundary": _base.CURRENT_FRONTIER_BOUNDARY,
        }
    )
    return summary


def _steps_for_profile(profile: str) -> tuple[_base.CurrentRootStep, ...]:
    profiles = {
        "repository": _base.REPOSITORY_LINEAGE_STEPS,
        "planos": _base.PLANOS_ACTIVE_FRONTIER_STEPS,
        "decisionos": _base.DECISIONOS_ACTIVE_FRONTIER_STEPS,
        "memoryos": _base.MEMORYOS_ACTIVE_FRONTIER_STEPS,
        "codeai": _base.CODEAI_CURRENT_FRONTIER_STEPS,
        "all": _base.CURRENT_ROOT_STEPS,
    }
    try:
        return profiles[profile]
    except KeyError as exc:
        raise ValueError("unknown_current_root_profile:" + profile) from exc


def run_current(profile: str = "all") -> int:
    steps = _steps_for_profile(profile)
    failures: list[str] = []
    total = len(steps)
    for ordinal, step in enumerate(steps, start=1):
        print(f"\n[{ordinal}/{total}] {step.step_id}", flush=True)
        try:
            status = _base._run_step(step.runner, step.target)
        except Exception as exc:
            status = 1
            print(
                f"current_root_exception:{step.step_id}:"
                f"{type(exc).__name__}:{exc}",
                file=sys.stderr,
            )
        if status == 0:
            print(f"PASS: {step.step_id}", flush=True)
        else:
            print(f"FAIL: {step.step_id} exited with {status}", flush=True)
            if step.required:
                failures.append(step.step_id)

    if failures:
        print("\nCURRENT ROOT FAILED", file=sys.stderr)
        for step_id in failures:
            print(f"- {step_id}", file=sys.stderr)
        return 1

    print(
        "\nPASS: KuuOS integrated current root "
        f"({_base.CURRENT_REPOSITORY_FRONTIER}; "
        f"{_base.CURRENT_PLANOS_FRONTIER}; "
        f"{_base.CURRENT_DECISIONOS_FRONTIER}; "
        f"{_base.CURRENT_MEMORYOS_FRONTIER}; "
        f"{_base.CURRENT_CODEAI_FRONTIER})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the KuuOS integrated current root."
    )
    parser.add_argument(
        "--profile",
        choices=_base.CURRENT_SUPPORTED_PROFILES,
        default="all",
        help="Select one bounded validation surface. The default is all.",
    )
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    if args.summary:
        print(
            json.dumps(
                current_runtime_root_summary(),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if args.list:
        for ordinal, step in enumerate(
            _steps_for_profile(args.profile),
            start=1,
        ):
            print(
                f"{ordinal:03d}\t{step.step_id}\t"
                f"{step.runner}\t{step.target}"
            )
        return 0
    return run_current(args.profile)


_base.current_runtime_root_summary = current_runtime_root_summary
_base._steps_for_profile = _steps_for_profile
_base.run_current = run_current
_base.main = main

for _name, _value in vars(_base).items():
    if not _name.startswith("__"):
        globals()[_name] = _value


if __name__ == "__main__":
    raise SystemExit(main())

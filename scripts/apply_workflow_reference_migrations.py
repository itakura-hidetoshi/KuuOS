#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    ".github/workflows/cbf_membrane_gap_kernel_validation.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/actos-authorization-intake-v0-3.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/actos-bounded-invocation-v0-4.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/learnos-vacuum-expectation-verification-future-only-v0-3.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/memoryos-analytic-hilbert-context-v0-38.yml": ".github/workflows/memoryos-world-observe-intake-v0-39.yml",
    ".github/workflows/memoryos-qi-world-blocker-integration-v0-35.yml": ".github/workflows/memoryos-qi-world-validation-matrix-v0-36.yml",
    ".github/workflows/observeos-vacuum-expectation-intake-commit-v0-3.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/observeos-world-host-effect-v0-4.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/planos-activation-admission-actos-handoff-v0-23.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/planos-compiler-materialization-v0-22.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/planos-history-qi-candidate-generation-v0-19.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/planos-hysteresis-constraint-decision-handoff-v0-20.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/planos-selected-candidate-next-cycle-synthesis-v0-21.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/planos-vacuum-expectation-learning-replan-intake-v0-18.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/verifyos-vacuum-expectation-commit-verification-v0-3.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/teni_observability_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/validator_tiering_policy_validation.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/kuuos_qi_meridian_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    ".github/workflows/kuuos_qi_sanjiao_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    ".github/workflows/physical_quantum_qi_deepening_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/physical_quantum_qi_runtime_evolution_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/physical_quantum_qi_runtime_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/qi_bounded_tick_manual_runner_example_validation.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/qi_bounded_tick_executor_receipt_contract_validation.yml": ".github/workflows/kuuos_runtime_full_check.yml",
}


def main() -> int:
    changed: list[Path] = []
    for directory, suffixes in (("scripts", {".py"}), ("manifests", {".json"})):
        for path in sorted((ROOT / directory).rglob("*")):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            migrated = text
            for old, new in MAPPINGS.items():
                migrated = migrated.replace(old, new)
            if migrated != text:
                path.write_text(migrated, encoding="utf-8")
                changed.append(path.relative_to(ROOT))

    for path in changed:
        print(path)
    print(f"updated={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

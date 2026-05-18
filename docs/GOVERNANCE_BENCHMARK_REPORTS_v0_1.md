# Governance Benchmark Reports v0.1

## Purpose

This document describes the public benchmark-report surface for KuuOS governance benchmarks.

## Components

| Component | Role |
|---|---|
| `benchmarks/governance_stress_tests_v0_1.json` | Governance stress-test corpus |
| `scripts/governance_benchmark_runner_v0_1.py` | Benchmark runner scaffold |
| `scripts/governance_benchmark_score_v0_1.py` | Benchmark scoring scaffold |
| `.github/workflows/governance_benchmark.yml` | Benchmark CI workflow |
| `benchmark_reports/governance_benchmark_report_v0_1.json` | Generated benchmark report |

## Benchmark Flow

```text
Governance stress-test corpus
    ↓
Benchmark runner
    ↓
Scoring engine
    ↓
Benchmark report
    ↓
GitHub artifact publication
```

## Current Evaluation Focus

The benchmark currently evaluates governance-aware handling of:

- candidate-versus-authority separation
- validation-versus-proof separation
- reference-boundary preservation
- provenance preservation
- fail-closed preference
- deployment-boundary preservation

## Important Clarification

Current scoring is intentionally conservative and governance-oriented.

High fluency alone does not imply high governance score.

## Boundary

Benchmark reports evaluate governance-oriented behavior only.

They do not automatically imply:

- theorem closure
- institutional approval
- deployment authorization
- clinical authority

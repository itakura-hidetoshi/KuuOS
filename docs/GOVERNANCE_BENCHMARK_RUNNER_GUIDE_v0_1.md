# Governance Benchmark Runner Guide v0.1

## Purpose

This document explains the minimal public governance benchmark runner scaffold.

## Runner

```text
scripts/governance_benchmark_runner_v0_1.py
```

## Corpus

```text
benchmarks/governance_stress_tests_v0_1.json
```

## Run Command

```bash
python3 scripts/governance_benchmark_runner_v0_1.py
```

## Current Behavior

The runner currently:

- loads governance stress-test cases
- prints scenarios
- prints expected governance responses
- prints risk tags
- preserves explicit governance boundaries

## Intended Future Direction

Potential future extensions:

- governance scoring
- automated rubric evaluation
- provenance checks
- claim-level transition detection
- rollback-preservation evaluation
- multi-agent governance tests

## Important Boundary

This runner is a governance benchmark scaffold.

It does not automatically imply:

- theorem evaluation
- deployment authorization
- institutional approval
- clinical authority

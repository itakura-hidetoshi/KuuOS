# Validator Dependency Overview v0.1

## Purpose

This document summarizes the public validator surfaces currently exposed by KuuOS.

## Validation Layers

```text
Core governance validators
    ↓
AI Yogacara validators
    ↓
Invariant and pipeline validators
    ↓
Qi and IndraNet validators
    ↓
Physics-facing bridge validators
    ↓
Aggregate governance validation
```

## Public Entry Points

| Entry Point | Purpose |
|---|---|
| `make core-governance-checks` | Core governance consistency |
| `make ai-yogacara-checks` | Yogacara and Ten'i layer checks |
| `make invariant-pipeline-checks` | Governance pipeline validation |
| `make physical-quantum-qi-runtime-checks` | Qi runtime validation |
| `make physical-quantum-qi-deepening-checks` | Extended Qi and transport validation |
| `make superstring-emptiness-sbm-checks` | String-brane-membrane validation |
| `make all-governance-checks` | Aggregate governance validation |

## Dependency Orientation

Aggregate governance validation assumes:

- lower-level validators complete successfully
- governance boundaries remain explicit
- validator outputs remain structurally interpretable

## Important Clarification

Validator success indicates structural consistency only.

Validator success does not automatically imply:

- theorem closure
- institutional acceptance
- deployment readiness
- execution authority

## Reviewer Guidance

Reviewers should distinguish:

- validator success
- theorem verification
- operational deployment
- institutional authorization

These are intentionally separated surfaces.

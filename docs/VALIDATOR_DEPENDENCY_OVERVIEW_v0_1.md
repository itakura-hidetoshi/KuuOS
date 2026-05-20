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
Qi runtime validators
    ↓
Qi motion chain validators
    ↓
Qi and IndraNet deepening validators
    ↓
Physics-facing bridge validators
    ↓
Aggregate governance validation
```

## Qi Motion Chain Internal Dependency

```text
Samvrti Qi Runtime
    ↓
Samvrti Qi to Physical Motion Evidence Builder
    ↓
Physical Quantum Qi Runtime
    ↓
Physical Quantum Qi Dynamics Kernel
    ↓
Physical Quantum Qi Motion Pipeline
    ↓
Qi Motion Chain Runner
```

The internal dependency is conservative: Samvrti Qi acceptance opens packet construction only; it does not promote a packet to FullPathQi by assertion.

## Public Entry Points

| Entry Point | Purpose |
|---|---|
| `make core-governance-checks` | Core governance consistency |
| `make ai-yogacara-checks` | Yogacara and Ten'i layer checks |
| `make invariant-pipeline-checks` | Governance pipeline validation |
| `make physical-quantum-qi-runtime-checks` | Qi runtime validation |
| `make qi-motion-chain-checks` | Samvrti Qi to conservative evidence, evidence-bound classification, licensed dynamics, and observe-only Qi motion candidate validation |
| `make physical-quantum-qi-deepening-checks` | Extended Qi and transport validation |
| `make superstring-emptiness-sbm-checks` | String-brane-membrane validation |
| `make all-governance-checks` | Aggregate governance validation |

## Dependency Orientation

Aggregate governance validation assumes:

- lower-level validators complete successfully
- governance boundaries remain explicit
- validator outputs remain structurally interpretable
- Qi motion chain outputs remain observe-only and non-authoritative

## Important Clarification

Validator success indicates structural consistency only.

Validator success does not automatically imply:

- theorem closure
- institutional acceptance
- deployment readiness
- execution authority
- clinical authority
- Qi-based treatment authorization

## Reviewer Guidance

Reviewers should distinguish:

- validator success
- theorem verification
- operational deployment
- institutional authorization
- Qi motion candidate review

These are intentionally separated surfaces.
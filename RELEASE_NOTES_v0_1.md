# KuuOS Public Core Release Notes v0.1

## Release Type

Public governance-core release surface.

## Purpose

This release prepares KuuOS for external review as a boundary-preserving AI governance architecture.

It emphasizes:

- public reviewer onboarding
- governance boundary visibility
- reproducibility of validation surfaces
- non-authority preservation
- explicit separation from canonical theorem proof repositories
- Qi motion chain reviewability from Samvrti Qi observation to observe-only physical motion candidate output

## Main Public Entry Points

```text
README.md
GOVERNANCE.md
SECURITY.md
CONTRIBUTING.md
docs/QUICKSTART_v0_1.md
docs/ARCHITECTURE_OVERVIEW_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/EXTERNAL_REVIEW_GUIDE_v0_1.md
docs/VALIDATION_COVERAGE_MATRIX_v0_1.md
docs/REPRODUCIBILITY_MATRIX_v0_1.md
docs/LEAN_COVERAGE_MAP_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
```

## Validation Entry Point

```bash
make all-governance-checks
```

or:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

For the Qi motion chain specifically:

```bash
make qi-motion-chain-checks
```

or:

```bash
python3 scripts/run_qi_motion_chain_checks_v0_1.py
```

## Qi Motion Chain Surface

This release includes a public Qi motion chain surface:

```text
Samvrti Qi Runtime
  -> Samvrti Qi to Physical Motion Evidence Builder
  -> Physical Quantum Qi Runtime
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
```

The chain preserves this invariant:

```text
observed conventional flow
  -> conservative evidence packet
  -> evidence-bound validated_type
  -> licensed dynamics terms
  -> bounded motion candidate
  -> observe-only output
```

The Qi motion chain is validated locally, through all-governance checks, and through the dedicated GitHub Actions workflow:

```text
.github/workflows/qi_motion_chain_validation.yml
```

## What This Release Claims

This release claims that KuuOS has a public governance-oriented repository surface that can be reviewed structurally.

It exposes:

- governance documentation
- validation entrypoints
- non-authority policies
- reproducibility boundaries
- architecture overview
- external review guidance
- Qi motion chain implementation, validation, reproducibility, CI, and audit surfaces

## What This Release Does Not Claim

This release does not claim:

- institutional authority
- clinical authority
- production deployment readiness
- independent theorem closure
- replacement of the canonical 4D mass gap proof repository
- autonomous execution authority
- Qi-based execution authorization
- Qi motion candidate as treatment authorization
- Samvrti Qi acceptance as FullPathQi promotion

## Canonical Boundary

The canonical Lean proof repository for the 4D mass gap proof architecture remains:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS references it as a governance-facing bridge but does not replace it.

## Recommended Release Checklist

Before creating a GitHub Release:

- [ ] `make all-governance-checks` passes
- [ ] `make qi-motion-chain-checks` passes when Qi motion chain surfaces are included
- [ ] README links are current
- [ ] governance documents are present
- [ ] Qi motion chain runbook is present
- [ ] validation matrix is present
- [ ] reproducibility matrix is present
- [ ] public audit checklist includes Qi motion chain boundaries
- [ ] known limitations are explicit
- [ ] non-authority statement is visible
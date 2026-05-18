# Contributing to KuuOS

Thank you for your interest in KuuOS.

## Before Contributing

Please read:

```text
README.md
GOVERNANCE.md
SECURITY.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
```

## Contribution Philosophy

KuuOS prioritizes:

- explicit boundaries
- provenance preservation
- non-authority preservation
- fail-closed behavior
- structural clarity
- reviewer reproducibility

## Preferred Contribution Types

Examples:

- documentation clarification
- validator improvements
- test additions
- reproducibility improvements
- CI improvements
- architecture diagrams
- formalization scaffolding
- auditability improvements

## Changes Requiring Careful Review

Examples:

- governance-boundary modifications
- validator weakening
- execution-surface expansion
- authority escalation logic
- provenance bypasses
- physics-facing theorem interpretation changes

## Pull Request Guidance

A pull request should ideally explain:

1. what changed
2. why the change is needed
3. whether governance boundaries changed
4. whether validation behavior changed
5. whether reproducibility changed

## Validation

Before submitting:

```bash
make all-governance-checks
```

If a change only affects a subset of the repository, run the narrowest relevant validator as well.

## Style

Prefer:

- explicit naming
- boundary visibility
- stable terminology
- append-only evolution where possible
- minimal silent behavior

## Important Boundary

KuuOS contributors should not present repository validation as automatic theorem, institutional, or clinical authority.

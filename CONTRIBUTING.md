# Contributing to KuuOS

Thank you for your interest in KuuOS.

## Before Contributing

Please read:

```text
README.md
GOVERNANCE.md
SECURITY.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
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
- Qi motion chain changes that might promote Samvrti Qi acceptance into FullPathQi by assertion
- Qi dynamics changes that might allow unlicensed motion terms to influence motion candidates

## Pull Request Guidance

A pull request should ideally explain:

1. what changed
2. why the change is needed
3. whether governance boundaries changed
4. whether validation behavior changed
5. whether reproducibility changed
6. whether Qi motion chain semantics changed

## Validation

Before submitting:

```bash
make all-governance-checks
```

If a change touches Qi motion chain surfaces, also run:

```bash
make qi-motion-chain-checks
```

If a change only affects a subset of the repository, run the narrowest relevant validator as well.

## Qi Motion Chain Contribution Boundary

Changes touching Qi motion chain surfaces must preserve:

```text
samvrti_acceptance_not_fullpath_promotion
conservative_evidence_builder_required
evidence_bound_classification_required
validated_type_licenses_dynamics_terms
unlicensed_motion_terms_ignored
observe_only_motion_candidate
direct_execution_allowed_false
authority_expansion_false
clinical_authority_false
```

## Style

Prefer:

- explicit naming
- boundary visibility
- stable terminology
- append-only evolution where possible
- minimal silent behavior

## Important Boundary

KuuOS contributors should not present repository validation as automatic theorem, institutional, clinical, Qi-based treatment, or execution authority.
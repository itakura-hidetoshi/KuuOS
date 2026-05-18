# External Review Guide v0.1

## Intended Audience

This guide is for:

- researchers
- engineers
- governance reviewers
- formal methods reviewers
- AI safety reviewers
- systems architects

## Recommended Reading Order

1. README.md
2. docs/QUICKSTART_v0_1.md
3. docs/ARCHITECTURE_OVERVIEW_v0_1.md
4. docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
5. docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
6. docs/VALIDATION_COVERAGE_MATRIX_v0_1.md
7. docs/REPRODUCIBILITY_MATRIX_v0_1.md
8. Makefile
9. scripts/run_all_governance_full_checks_v0_1.py

## Primary Review Questions

A reviewer should ask:

### Boundary Questions

- Are authority boundaries explicit?
- Are candidate and authority separated?
- Is rollback visibility preserved?
- Is provenance preserved?

### Governance Questions

- Is fail-closed behavior preserved?
- Are validators explicit?
- Are packet chains reviewable?
- Are manifests inspectable?

### Architecture Questions

- Are layers distinguishable?
- Are bridges explicitly scoped?
- Are governance and theorem authority separated?

### Reproducibility Questions

- Can validators be run locally?
- Are workflow entrypoints visible?
- Are dependencies understandable?

## Important Clarification

KuuOS is currently strongest as:

- a governance architecture
- a boundary-preserving AI framework
- a relational systems architecture
- a validation and audit structure

It should not currently be interpreted as:

- a fully autonomous AGI deployment stack
- a final institutional theorem authority
- a production clinical platform

## Minimal External Validation

```bash
make all-governance-checks
```

This is the primary public review entrypoint.

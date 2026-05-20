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
8. docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
9. Makefile
10. scripts/run_all_governance_full_checks_v0_1.py
11. scripts/run_qi_motion_chain_checks_v0_1.py

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

### Qi Motion Chain Questions

- Is Samvrti Qi acceptance prevented from becoming automatic FullPathQi promotion?
- Is conservative evidence building explicit and stage-gated?
- Is classification evidence-bound rather than claim-bound?
- Does the validated Qi type license dynamics terms?
- Are unlicensed motion terms ignored even when numeric values are present?
- Does the motion candidate remain observe-only?
- Is direct execution request blocked?
- Is Qi motion validation separated from clinical, institutional, theorem, and execution authority?

## Qi Motion Chain Review Path

For Qi-specific review, inspect:

```text
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
docs/SAMVRTI_QI_RUNTIME_IMPLEMENTATION_v0_1.md
docs/SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md
docs/PHYSICAL_QUANTUM_QI_DYNAMICS_KERNEL_v0_1.md
docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md
examples/samvrti_qi_runtime_adapter_minimal.py
examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py
examples/physical_quantum_qi_dynamics_kernel_minimal.py
examples/physical_quantum_qi_motion_pipeline_minimal.py
scripts/run_qi_motion_chain_checks_v0_1.py
.github/workflows/qi_motion_chain_validation.yml
```

Run:

```bash
make qi-motion-chain-checks
```

Expected interpretation:

```text
PASS = structural consistency of the Qi motion chain
PASS != execution authority
PASS != clinical authority
PASS != theorem authority
PASS != treatment authorization
```

## Important Clarification

KuuOS is currently strongest as:

- a governance architecture
- a boundary-preserving AI framework
- a relational systems architecture
- a validation and audit structure
- a public, observe-only Qi motion chain validation surface

It should not currently be interpreted as:

- a fully autonomous AGI deployment stack
- a final institutional theorem authority
- a production clinical platform
- a Qi-based execution or treatment authorization system

## Minimal External Validation

```bash
make all-governance-checks
```

This is the primary public review entrypoint.

For Qi motion chain-only review:

```bash
make qi-motion-chain-checks
```
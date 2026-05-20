# KuuOS Public Documentation Index v0.1

This index provides a stable public entrypoint for external reviewers.

## Start Here

| Document | Purpose |
|---|---|
| `README.md` | Main repository introduction |
| `docs/QUICKSTART_v0_1.md` | Minimal reviewer and validation path |
| `docs/EXTERNAL_REVIEW_GUIDE_v0_1.md` | Review order and review questions |
| `docs/ARCHITECTURE_OVERVIEW_v0_1.md` | High-level KuuOS architecture |

## Diagrams

| Document | Purpose |
|---|---|
| `docs/ARCHITECTURE_DIAGRAM_v0_1.md` | Mermaid architecture flow diagram |
| `docs/GOVERNANCE_DIAGRAM_v0_1.md` | Mermaid governance flow diagram |
| `docs/VALIDATOR_GRAPH_v0_1.md` | Mermaid validator dependency graph |
| `docs/GOVERNANCE_FLOW_OVERVIEW_v0_1.md` | Text overview of governance flow |
| `docs/VALIDATOR_DEPENDENCY_OVERVIEW_v0_1.md` | Text overview of validator dependencies |

## Governance and Boundaries

| Document | Purpose |
|---|---|
| `GOVERNANCE.md` | Repository governance rules |
| `SECURITY.md` | Security and disclosure policy |
| `CONTRIBUTING.md` | Contribution guidance |
| `docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md` | Non-authority and boundary policy |
| `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md` | Medical-modality-neutral Qi boundary |
| `docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md` | Theorem/reference authority separation |

## Validation and Reproducibility

| Document | Purpose |
|---|---|
| `docs/VALIDATION_COVERAGE_MATRIX_v0_1.md` | Validator coverage overview |
| `docs/REPRODUCIBILITY_MATRIX_v0_1.md` | Reproducibility scope matrix |
| `docs/PUBLIC_AUDIT_CHECKLIST_v0_1.md` | Public audit checklist |
| `docs/LEAN_COVERAGE_MAP_v0_1.md` | Lean-facing coverage boundary |
| `docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md` | Governance check runbook |
| `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md` | Qi motion chain runbook |

## Core Governance Surface

| Document | Purpose |
|---|---|
| `docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md` | Current core governance index |
| `docs/KUOS_FOURFOLD_CORE_v0_1.md` | Fourfold core specification |
| `docs/KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md` | Emptiness superposition non-collapse addendum |
| `docs/GOVERNANCE_RELEASE_GATE_v0_1.md` | Release gate governance surface |

## Physics-Facing Boundary

| Document | Purpose |
|---|---|
| `docs/KUOS_PHYSICS_GAP_BRIDGE_v0_1.md` | Physics-facing bridge |
| `docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md` | Canonical proof repository reference |
| `docs/MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md` | Mass gap to Two Truths Engine bridge |
| `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md` | Qi motion chain operational bridge |
| `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md` | Qi medical-boundary wording clarification |

## Release Preparation

| Document | Purpose |
|---|---|
| `RELEASE_NOTES_v0_1.md` | v0.1 release notes draft |
| `RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md` | v0.2 emptiness non-collapse release notes |
| `docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md` | Proposed v0.1 public release package |

## Minimal Validation Command

```bash
make all-governance-checks
```

## Qi Motion Chain Validation

```bash
make qi-motion-chain-checks
```

## Emptiness Superposition Non-Collapse Validation

```bash
make emptiness-superposition-noncollapse-checks
```

## Interpretation

This index is a public navigation surface. It does not grant theorem, standalone diagnosis, standalone treatment authorization, medical act authorization, institutional authority, or execution authority.
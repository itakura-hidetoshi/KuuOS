# Public Release Package Manifest v0.1

## Purpose

This document summarizes the intended public release package for the KuuOS public-core governance surface.

## Intended Public Release Contents

### Repository Entry Surface

- README.md
- GOVERNANCE.md
- SECURITY.md
- CONTRIBUTING.md
- RELEASE_NOTES_v0_1.md
- RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md

### Reviewer and Onboarding Surface

- docs/PUBLIC_DOCS_INDEX_v0_1.md
- docs/QUICKSTART_v0_1.md
- docs/EXTERNAL_REVIEW_GUIDE_v0_1.md
- docs/ARCHITECTURE_OVERVIEW_v0_1.md

### Diagram Surface

- docs/ARCHITECTURE_DIAGRAM_v0_1.md
- docs/GOVERNANCE_DIAGRAM_v0_1.md
- docs/VALIDATOR_GRAPH_v0_1.md
- docs/GOVERNANCE_FLOW_OVERVIEW_v0_1.md
- docs/VALIDATOR_DEPENDENCY_OVERVIEW_v0_1.md

### Governance Surface

- docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
- docs/KUOS_FOURFOLD_CORE_v0_1.md
- docs/KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md
- docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
- docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
- docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md
- docs/GOVERNANCE_RELEASE_GATE_v0_1.md

### Validation Surface

- Makefile
- scripts/run_all_governance_full_checks_v0_1.py
- scripts/run_core_governance_full_checks_v0_1.py
- scripts/run_qi_motion_chain_checks_v0_1.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_v0_2.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_release_packet_v0_2.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_established_baseline_packet_v0_2.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.py
- scripts/validate_kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.py
- validation_cases/kuos_emptiness_superposition_non_collapse_validation_cases_v0_2.json
- docs/VALIDATION_COVERAGE_MATRIX_v0_1.md
- docs/REPRODUCIBILITY_MATRIX_v0_1.md
- docs/PUBLIC_AUDIT_CHECKLIST_v0_1.md
- docs/LEAN_COVERAGE_MAP_v0_1.md

### Qi Motion Chain Surface

- docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
- docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
- docs/SAMVRTI_QI_RUNTIME_IMPLEMENTATION_v0_1.md
- docs/SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md
- docs/PHYSICAL_QUANTUM_QI_DYNAMICS_KERNEL_v0_1.md
- docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md
- specs/samvrti_qi_runtime_contract_v0_1.yaml
- specs/physical_quantum_qi_dynamics_kernel_v0_1.json
- examples/samvrti_qi_runtime_adapter_minimal.py
- examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py
- examples/physical_quantum_qi_dynamics_kernel_minimal.py
- examples/physical_quantum_qi_motion_pipeline_minimal.py
- scripts/validate_samvrti_qi_runtime_v0_1.py
- scripts/validate_samvrti_qi_to_physical_motion_evidence_builder_v0_1.py
- scripts/validate_physical_quantum_qi_dynamics_kernel_v0_1.py
- scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py
- scripts/run_qi_motion_chain_checks_v0_1.py
- validation_cases/samvrti_qi_runtime_validation_cases_v0_1.yaml
- validation_cases/samvrti_qi_to_physical_motion_evidence_builder_cases_v0_1.json
- validation_cases/physical_quantum_qi_dynamics_kernel_cases_v0_1.json
- validation_cases/physical_quantum_qi_motion_pipeline_cases_v0_1.json
- .github/workflows/all_governance_validation.yml

### Spec and Release Packet Surface

- specs/kuos_emptiness_superposition_non_collapse_contract_v0_2.yaml
- specs/kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml
- specs/kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.yaml
- specs/kuos_emptiness_superposition_non_collapse_established_baseline_packet_v0_2.yaml
- specs/kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.yaml
- specs/kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.yaml

### Formal Surface

- formal/KUOS/Emptiness/SuperpositionNonCollapse.lean

### Physics-Facing Boundary Surface

- docs/KUOS_PHYSICS_GAP_BRIDGE_v0_1.md
- docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md
- docs/MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md
- docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
- docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md

## Validation Entry Point

```bash
make all-governance-checks
```

For the Qi motion chain:

```bash
make qi-motion-chain-checks
```

For the v0.2 emptiness superposition non-collapse addendum:

```bash
make emptiness-superposition-noncollapse-checks
```

## Intended Interpretation

The public release package is intended to expose:

- governance structure
- architecture structure
- validation structure
- reproducibility boundaries
- authority boundaries
- catuskoti superposition non-collapse governance checks
- Qi motion chain checks from Samvrti Qi observation to conservative evidence, evidence-bound classification, licensed dynamics, and observe-only motion candidate output
- medical-modality-neutral Qi boundary wording that does not deny Qi or East Asian medical reasoning

It is not intended to imply:

- final theorem closure
- institutional approval
- production deployment authorization
- standalone diagnosis authority
- standalone treatment authorization
- medical act authorization
- execution authority
- Qi-based execution authorization
- reduction of Madhyamaka to quantum mechanics
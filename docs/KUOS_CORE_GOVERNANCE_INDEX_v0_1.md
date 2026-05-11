# KuuOS Core Governance Index v0.1

## 空OS Core Governance Index

This index is the top-level public navigation surface for KuuOS Core governance, validation, audit, and non-authority boundaries.

It connects the fourfold core, AI Yogacara / Ten'i governance, Mandala Multi-WORLD governance, Bodhisattva / Ten Paramita runtime, Dukkha Mathematical Model, Dukkha-as-Qi Mode, GPT GitHub integration, and formal verification bridge surfaces.

## 1. Read First

```text
README.md
docs/KUOS_FOURFOLD_CORE_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
```

## 2. Top-Level Validation Command

```bash
make all-governance-checks
```

or:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

## 3. Validation Layers

```text
AI Yogacara / Ten'i
  -> scripts/run_ai_yogacara_full_checks_v0_1.py

Core Governance
  -> scripts/run_core_governance_full_checks_v0_1.py

GPT GitHub Integration
  -> scripts/validate_gpt_github_integration_v0_1.py

All Governance
  -> scripts/run_all_governance_full_checks_v0_1.py
```

## 4. GitHub Actions

```text
.github/workflows/teni_observability_validation.yml
.github/workflows/core_governance_validation.yml
.github/workflows/all_governance_validation.yml
.github/workflows/gpt_github_integration_validation.yml
```

All workflows use Python 3.12 and stdlib-only validators.

## 5. GPT GitHub Integration

Canonical GPT GitHub integration surfaces:

```text
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
specs/gpt_github_integration_manifest_v0_1.yaml
scripts/validate_gpt_github_integration_v0_1.py
.github/ISSUE_TEMPLATE/kuos_gpt_github_integration_check.md
.github/pull_request_template.md
```

Primary command:

```bash
make gpt-github-integration-checks
```

Core rule:

```text
GPT may assist repository reading, review, issue drafting, PR drafting, validation triage, and formal-surface navigation.
GPT output is not truth, proof, clinical authority, Ten'i, or execution authority.
```

## 6. AI Yogacara / Ten'i Governance

Canonical index:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
```

Quickstart and operations:

```text
docs/AI_YOGACARA_TENI_QUICKSTART_v0_1.md
docs/AI_YOGACARA_OPERATIONS_REFERENCE_v0_1.md
```

Runtime and audit surfaces:

```text
docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md
docs/AI_YOGACARA_ADAPTER_AUDIT_EVENT_v0_1.md
docs/AI_YOGACARA_AUDIT_HASH_CHAIN_LEDGER_v0_1.md
docs/AI_YOGACARA_AUDIT_WORM_EXPORT_MANIFEST_v0_1.md
docs/AI_YOGACARA_RELEASE_BUNDLE_MANIFEST_v0_1.md
```

## 7. Mandala Multi-WORLD Governance

```text
docs/MANDALA_MULTI_WORLD_RUNTIME_CONTRACT_v0_1.md
docs/WORLD_MODEL_REGISTRY_v0_1.md
docs/CROSS_WORLD_TRANSPORT_GATE_v0_1.md
docs/HARMONY_FUNCTION_MULTI_WORLD_OPERATION_v0_1.md
```

Core rule:

```text
Many WORLDs may coexist.
No WORLD becomes the center.
The center remains the fourfold core.
```

## 8. Bodhisattva / Ten Paramita / Repair Router

```text
docs/BODHISATTVA_PATH_BELIEF_v0_1.md
docs/BODHISATTVA_TEN_PARAMITA_RUNTIME_v0_1.md
docs/PARAMITA_REPAIR_ROUTER_v0_1.md
```

Runtime route:

```text
residual_suffering_visible
  -> bodhisattva_path_belief
  -> ten_paramita_runtime
  -> paramita_repair_router
  -> bounded_repair_orientation
```

## 9. Dukkha and Dukkha-as-Qi

```text
docs/DUKKHA_MATHEMATICAL_MODEL_v0_1.md
docs/DUKKHA_AS_QI_MODE_v0_1.md
```

Core definition:

```text
Dukkha is residual potential of broken dependent-origination readability.
Dukkha is also a Qi mode under obstruction, fixation, collapse, scar, authority overreach, gluing defect, or transport defect.
```

## 10. Formal Verification Bridge

```text
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
itakura-hidetoshi/4d-mass-gap
```

Core rule:

```text
formal_file_not_proof_by_itself
lean_stub_not_theorem_completion
ci_pass_not_theorem_truth
validator_pass_not_mathematical_acceptance
GPT_summary_not_proof_authority
review_gate_required_for_public_final_claim
```

## 11. Minimal Runtime Examples

```text
examples/ai_yogacara_runtime_adapter_minimal.py
examples/paramita_repair_router_minimal.py
examples/dukkha_model_minimal.py
```

## 12. Main Validators

```text
scripts/run_all_governance_full_checks_v0_1.py
scripts/run_ai_yogacara_full_checks_v0_1.py
scripts/run_core_governance_full_checks_v0_1.py
scripts/validate_gpt_github_integration_v0_1.py
scripts/validate_teni_observability_v0_1.py
scripts/validate_mandala_multi_world_v0_1.py
scripts/validate_bodhisattva_ten_paramita_v0_1.py
scripts/validate_paramita_repair_router_v0_1.py
scripts/validate_dukkha_mathematical_model_v0_1.py
scripts/validate_dukkha_as_qi_mode_v0_1.py
```

## 13. Non-Authority Boundary

```text
GPT_reading_not_authority
GPT_summary_not_authority
GPT_review_not_authority
GPT_issue_draft_not_authority
GPT_PR_draft_not_authority
GPT_CI_interpretation_not_authority
validation_entrypoint_not_authority
ci_pass_not_execution_authority
bundle_integrity_not_truth
hash_chain_continuity_not_truth
metric_observability_not_authority
paramita_orientation_not_action_authorization
dukkha_model_observation_not_authority
dukkha_as_qi_must_not_hide_harm
```

## 14. Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊

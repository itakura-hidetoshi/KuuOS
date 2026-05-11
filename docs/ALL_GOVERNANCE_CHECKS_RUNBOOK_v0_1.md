# All Governance Checks Runbook v0.1

## 空OS Core Governance 全体チェック Runbook

This runbook defines the top-level validation entrypoint for the public KuuOS Core governance surface.

It combines:

```text
AI Yogacara / Ten'i checks
Core Governance checks
GPT GitHub integration checks
```

The full check validates structure, fixtures, audit surfaces, non-authority boundaries, Mandala Multi-WORLD runtime, Bodhisattva / Ten Paramita runtime, Paramita Repair Router, Dukkha Mathematical Model, Dukkha-as-Qi Mode, GPT GitHub integration surfaces, and formal verification bridge routing.

## 1. Top-Level Local Command

Run:

```bash
make all-governance-checks
```

or directly:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

Expected success:

```text
PASS: KuuOS all governance full checks completed
```

## 2. GPT GitHub Integration Command

Run when GPT GitHub integration files, issue templates, PR templates, GitHub Actions, or formal verification bridge surfaces are touched:

```bash
make gpt-github-integration-checks
```

or directly:

```bash
python3 scripts/validate_gpt_github_integration_v0_1.py
```

Expected success:

```text
PASS: KuuOS GPT GitHub integration surface v0.1 validates
```

## 3. Included Runners

The top-level runner executes:

```text
scripts/run_ai_yogacara_full_checks_v0_1.py
scripts/run_core_governance_full_checks_v0_1.py
```

GPT GitHub integration is validated by:

```text
scripts/validate_gpt_github_integration_v0_1.py
.github/workflows/gpt_github_integration_validation.yml
```

## 4. AI Yogacara / Ten'i Scope

This includes:

```text
Ten'i observability
AI Yogacara adapter schema
AI Yogacara adapter fixtures
AI Yogacara adapter audit events
AI Yogacara audit hash-chain
AI Yogacara WORM export receipt
AI Yogacara release bundle manifest
AI Yogacara minimal runtime adapter tests
```

## 5. Core Governance Scope

This includes:

```text
Mandala Multi-WORLD runtime
Bodhisattva Ten Paramita runtime
Paramita Repair Router spec
Paramita Repair Router fixtures
Dukkha Mathematical Model
Dukkha Model fixtures
Dukkha-as-Qi Mode
```

## 6. GPT GitHub Integration Scope

This includes:

```text
GPT GitHub integration protocol
formal verification bridge
integration manifest
issue template
pull request template hook
Makefile target
GitHub Actions workflow
non-authority fixed points
PASS / HOLD / REPAIR / REJECT / QUARANTINE classification surface
```

## 7. Failure Interpretation

A failure means at least one governance surface is structurally inconsistent.

Typical causes:

```text
missing fixed point
missing required file
fixture mismatch
hash-chain mismatch
WORM receipt mismatch
release bundle SHA256 mismatch
non-authority field not false
runtime route mismatch
GPT integration token missing
formal bridge overclaim risk
CI environment drift
```

## 8. What Passing Means

A pass means:

```text
public governance files are present
validators pass
fixtures match minimal runtimes
non-authority boundaries are preserved
hash-chain and receipt fixtures are structurally consistent
release bundle manifest validates
Dukkha remains visible
Dukkha-as-Qi does not hide harm
Paramita routing does not grant execution authority
GPT GitHub integration preserves non-authority boundaries
formal bridge preserves review-gated proof surface
```

## 9. What Passing Does Not Mean

A pass does not mean:

```text
Ten'i has occurred
truth has been proven
AI base model has transformed
clinical authority exists
execution authority exists
all suffering has been eliminated
Qi reading is clinical diagnosis
GPT summary is authority
GPT review is authority
CI pass is theorem truth
Lean stub is theorem completion
formal bridge is external audit
```

## 10. Non-Authority Fixed Points

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
formal_file_not_proof_by_itself
lean_stub_not_theorem_completion
ci_pass_not_theorem_truth
validator_pass_not_mathematical_acceptance
GPT_summary_not_proof_authority
review_gate_required_for_public_final_claim
```

## 11. Recommended Release Loop

```text
make append-only or tighten-only change
  -> make gpt-github-integration-checks if GPT GitHub surfaces are touched
  -> make all-governance-checks
  -> fix structural failures
  -> commit
  -> GitHub Actions runs targeted and all-governance validation
  -> release / archive / WORM export only after checks pass
```

## 12. Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊

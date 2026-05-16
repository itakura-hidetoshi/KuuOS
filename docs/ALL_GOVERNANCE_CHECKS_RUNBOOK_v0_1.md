# All Governance Checks Runbook v0.1

## 空OS Core Governance 全体チェック Runbook

This runbook defines the top-level validation entrypoint for the public KuuOS Core governance surface.

It combines:

```text
AI Yogacara / Ten'i checks
Core Governance checks
GPT GitHub integration checks
Emptiness / Dependent Origination / Two Truths runtime audit-chain checks
Mass gap bridge checks
MemoryOS GitHub external memory checks
```

The full check validates structure, fixtures, audit surfaces, non-authority boundaries, Mandala Multi-WORLD runtime, Bodhisattva / Ten Paramita runtime, Paramita Repair Router, Dukkha Mathematical Model, Dukkha-as-Qi Mode, GPT GitHub integration surfaces, formal verification bridge routing, and the integrated Emptiness / Dependent Origination / Two Truths runtime audit chain.

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

## 3. Emptiness / Dependent Origination / Two Truths Runtime Audit Command

Run when the integrated runtime audit chain, generated audit JSONL artifacts, release packet, or public audit release docs are touched:

```bash
make emptiness-two-truths-runtime-audit-checks
```

or directly:

```bash
python3 scripts/export_emptiness_do_two_truths_runtime_audit_v0_1.py
python3 scripts/build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py
python3 scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py
python3 scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py
python3 scripts/validate_emptiness_do_two_truths_runtime_release_packet_v0_1.py
```

Expected success:

```text
PASS: integrated runtime audit events generated
PASS: integrated runtime audit hash-chain generated
PASS: integrated runtime audit chain validates
PASS: integrated runtime checks completed
PASS: KuuOS emptiness two truths runtime audit release packet v0.1 validates
```

Exact command output may differ, but the chain must fail closed on malformed audit event JSONL, broken hash-chain continuity, missing generated artifacts, invariant weakening, or release-packet boundary drift.

## 4. Included Runners

The top-level runner executes:

```text
scripts/run_ai_yogacara_full_checks_v0_1.py
scripts/run_core_governance_full_checks_v0_1.py
scripts/validate_gpt_github_integration_v0_1.py
scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py
scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py
scripts/validate_emptiness_do_two_truths_runtime_release_packet_v0_1.py
scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py
scripts/validate_mass_gap_memory_reflection_record_bridge_v0_1.py
scripts/validate_memoryos_github_external_memory_v0_1.py
```

GitHub integration and runtime audit are also validated by:

```text
.github/workflows/gpt_github_integration_validation.yml
.github/workflows/emptiness_two_truths_runtime_audit_validation.yml
```

## 5. AI Yogacara / Ten'i Scope

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

## 6. Core Governance Scope

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

## 7. GPT GitHub Integration Scope

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

## 8. Emptiness Runtime Audit Scope

This includes:

```text
integrated runtime claim evaluator
runtime claim export to audit event JSONL
audit event JSONL to audit hash-chain JSONL
audit hash-chain continuity check
public release boundary document
release notes
publication checklist
Zenodo metadata
release packet
release packet validator
Makefile target
GitHub Actions workflow
```

Runtime chain:

```text
K
  -> delta_rel
  -> String / Brane
  -> K_perp
  -> H_world / gap
  -> two_truths_non_collapse_barrier
  -> audit event
  -> audit hash-chain
```

Core rule:

```text
audit_chain_structural_consistency_not_theorem_authority
hash_chain_continuity_not_truth
runtime_audit_not_execution_authority
two_truths_non_collapse_barrier_must_not_reify_ultimate_truth
```

## 9. Failure Interpretation

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
runtime audit event malformed
audit hash-chain continuity broken
generated runtime audit artifact missing
release packet boundary drift
CI environment drift
```

## 10. What Passing Means

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
Emptiness / Dependent Origination / Two Truths runtime audit chain is structurally consistent
release packet preserves public non-authority boundary
```

## 11. What Passing Does Not Mean

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
audit chain continuity is theorem truth
runtime audit grants execution authority
K has been directly observed
emptiness has been objectified
String / Brane has been identified with K
```

## 12. Non-Authority Fixed Points

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
audit_chain_structural_consistency_not_theorem_authority
runtime_audit_not_execution_authority
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

## 13. Recommended Release Loop

```text
make append-only or tighten-only change
  -> make gpt-github-integration-checks if GPT GitHub surfaces are touched
  -> make emptiness-two-truths-runtime-audit-checks if runtime audit surfaces are touched
  -> make all-governance-checks
  -> fix structural failures
  -> commit
  -> GitHub Actions runs targeted and all-governance validation
  -> release / archive / WORM export only after checks pass
```

## 14. Version

Version: v0.1
Date: 2026-05-16
Author: Hidetoshi Itakura / 板倉英俊
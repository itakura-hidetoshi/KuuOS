# All Governance Checks Runbook v0.1

## 空OS Core Governance 全体チェック Runbook

This runbook defines the top-level validation entrypoint for the public KuuOS Core governance surface.

It combines:

```text
AI Yogacara / Ten'i checks
Core Governance checks
GPT GitHub integration checks
MemoryOS GitHub external memory checks
```

The full check validates structure, fixtures, audit surfaces, non-authority boundaries, Mandala Multi-WORLD runtime, Bodhisattva / Ten Paramita runtime, Paramita Repair Router, Dukkha Mathematical Model, Dukkha-as-Qi Mode, GPT GitHub integration surfaces, MemoryOS GitHub external memory surfaces, and formal verification bridge routing.

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

## 3. MemoryOS GitHub External Memory Command

Run when MemoryOS external memory docs, manifests, examples, validators, recall indexes, or GitHub pointer records are touched:

```bash
make memoryos-github-external-memory-checks
```

or directly:

```bash
python3 scripts/validate_memoryos_github_external_memory_v0_1.py
```

Expected success:

```text
PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates
```

## 4. Included Runners

The top-level runner executes:

```text
scripts/run_ai_yogacara_full_checks_v0_1.py
scripts/run_core_governance_full_checks_v0_1.py
scripts/validate_gpt_github_integration_v0_1.py
scripts/validate_memoryos_github_external_memory_v0_1.py
```

GPT GitHub integration is also validated by:

```text
.github/workflows/gpt_github_integration_validation.yml
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

## 8. MemoryOS GitHub External Memory Scope

This includes:

```text
MemoryOS GitHub external memory protocol
external memory manifest
minimal GitHub pointer record example
Makefile target
validator
pointer memory
evidence memory
semantic digest memory
repair lineage memory
conflict visibility memory
stable commit SHA preference
branch HEAD non-stability warning
non-authority fixed points
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
MemoryOS external memory token missing
GitHub branch HEAD treated as pinned memory
semantic digest treated as source evidence
GitHub CI or release treated as truth
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
MemoryOS GitHub external memory preserves pointer/evidence boundaries
formal bridge preserves review-gated proof surface
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
GitHub memory is MemoryOS authority
GitHub commit is truth
GitHub CI pass is theorem truth
GitHub release is proof completion
Lean stub is theorem completion
formal bridge is external audit
```

## 12. Non-Authority Fixed Points

```text
GPT_reading_not_authority
GPT_summary_not_authority
GPT_review_not_authority
GPT_issue_draft_not_authority
GPT_PR_draft_not_authority
GPT_CI_interpretation_not_authority
GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority
GitHub_commit_is_evidence_not_truth
GitHub_issue_is_discussion_not_memory_authority
GitHub_PR_is_proposal_not_memory_authority
GitHub_CI_pass_is_validation_signal_not_truth
GitHub_branch_HEAD_is_not_stable_memory
GitHub_release_is_public_surface_not_proof_completion
semantic_digest_is_not_source_evidence
MemoryOS_compile_context_must_expose_uncertainty
MemoryOS_no_silent_overwrite
MemoryOS_lineage_preserved
MemoryOS_conflict_visible
MemoryOS_append_only_external_pointer
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
no_execution_authority
no_clinical_authority
no_teni_authority
no_world_update_authority
```

## 13. Recommended Release Loop

```text
make append-only or tighten-only change
  -> make gpt-github-integration-checks if GPT GitHub surfaces are touched
  -> make memoryos-github-external-memory-checks if MemoryOS GitHub external memory surfaces are touched
  -> make all-governance-checks
  -> fix structural failures
  -> commit
  -> GitHub Actions runs targeted and all-governance validation
  -> release / archive / WORM export only after checks pass
```

## 14. Version

Version: v0.1
Date: 2026-05-13
Author: Hidetoshi Itakura / 板倉英俊

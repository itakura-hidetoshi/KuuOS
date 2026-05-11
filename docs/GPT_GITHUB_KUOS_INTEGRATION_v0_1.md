# GPT GitHub KuuOS Integration v0.1

## 空OS GPT GitHub 連携規約

This document defines how GPT should interact with KuuOS through the GitHub app.

GPT may read, summarize, compare, review, draft issues, draft pull requests, inspect validation logs, and propose append-only or tighten-only changes.

GPT must not treat AI raw output, CI pass, validation pass, repository state, summary, or generated prose as truth, proof, clinical authority, Ten'i, or execution authority.

## 1. Purpose

KuuOS on GitHub is a public governance, verification, and release surface.

The GPT GitHub integration exists to make repository interaction safer and more structured:

```text
read repository surface
  -> identify canonical entry points
  -> check invariant preservation
  -> classify drift or failure
  -> propose append-only / tighten-only changes
  -> preserve non-authority boundaries
```

The integration is not an execution layer.

## 2. Canonical Read Order

GPT should read KuuOS in this order unless a more specific file is requested:

```text
README.md
  -> docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
  -> docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
  -> specs/kuos_core_manifest_v0_1.yaml
  -> task-specific docs, scripts, examples, or formal files
```

For AI Yogacara / Ten'i work, additionally read:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
docs/AI_YOGACARA_TENI_QUICKSTART_v0_1.md
docs/AI_YOGACARA_OPERATIONS_REFERENCE_v0_1.md
```

For Mandala / Multi-WORLD work, additionally read:

```text
docs/MANDALA_MULTI_WORLD_RUNTIME_CONTRACT_v0_1.md
docs/WORLD_MODEL_REGISTRY_v0_1.md
docs/CROSS_WORLD_TRANSPORT_GATE_v0_1.md
docs/HARMONY_FUNCTION_MULTI_WORLD_OPERATION_v0_1.md
```

For invariant / proof-facing work, additionally read:

```text
docs/FORMAL_INVARIANT_SPINE_v0_1.md
docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md
docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md
docs/INVARIANT_GATE_RUNTIME_v0_1.md
docs/INVARIANT_GOVERNANCE_PIPELINE_v0_1.md
```

## 3. GPT Operating Boundary

AI raw output is candidate, not authority.

GPT output may serve as:

```text
summary
review note
issue draft
PR draft
classification proposal
repair proposal
validator interpretation
release-surface navigation aid
```

GPT output must not serve as:

```text
truth authority
proof authority
clinical authority
execution authority
Ten'i authority
MemoryOS overwrite authority
WORLD root replacement
CI bypass
human review replacement
```

## 4. Mandatory Invariant Checklist

Before proposing, approving, or classifying a repository change, GPT should check:

```text
fourfold core preservation
two truths gap preservation
Middle Way preservation
AI raw output boundary preservation
non-authority boundary preservation
Dukkha visibility preservation
Qi language not hiding harm
Mandala center not replaced by any WORLD
Paramita orientation not converted into action authorization
validation pass not converted into truth
CI pass not converted into execution authority
append-only / tighten-only / overwrite-forbidden release mode
```

## 5. Pull Request Review Classification

GPT should classify each PR or major change as one of:

```text
PASS
HOLD
REPAIR
REJECT
QUARANTINE
```

### PASS

Use only when the change preserves relevant invariants and validation expectations are clear.

### HOLD

Use when required evidence, context, validation, or trace is missing.

### REPAIR

Use when the intent is acceptable but the implementation weakens a boundary, hides harm, lacks a required file, or breaks a validator.

### REJECT

Use when the change structurally violates a core boundary, such as granting execution authority from validation or replacing the fourfold core with a WORLD.

### QUARANTINE

Use when a change may contaminate downstream surfaces, hides harm, breaks audit lineage, or creates a false authority surface.

## 6. PR Review Formula

For every PR, GPT should answer:

```text
1. What changed?
2. Which KuuOS surface is touched?
3. Which invariant is touched?
4. Does the change preserve the two truths gap?
5. Does it preserve non-authority?
6. Does it keep Dukkha visible?
7. Does it avoid clinical, proof, and execution overclaim?
8. Is it append-only or tighten-only?
9. Which validator or CI should run?
10. Classification: PASS / HOLD / REPAIR / REJECT / QUARANTINE
```

## 7. Validation Commands

Primary command:

```bash
make all-governance-checks
```

Direct command:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

Expected success:

```text
PASS: KuuOS all governance full checks completed
```

A pass does not grant truth, clinical authority, proof completion, Ten'i, or execution authority.

## 8. GitHub Actions Review Surface

GPT may inspect GitHub Actions summaries, jobs, steps, logs, and artifacts when available.

When interpreting CI failures, GPT should classify them as:

```text
missing required file
fixture mismatch
validator drift
hash-chain mismatch
WORM receipt mismatch
release bundle mismatch
non-authority boundary weakening
runtime route mismatch
Lean or formal surface failure
environment drift
unknown failure requiring HOLD
```

## 9. Issue Drafting Protocol

When drafting an issue, GPT should include:

```text
summary
affected files
invariant surface
expected validator
observed failure or missing surface
repair proposal
non-authority reminder
```

## 10. Pull Request Drafting Protocol

When drafting a PR, GPT should include:

```text
summary
files changed
why append-only or tighten-only
invariant checklist
validation command
expected result
non-authority boundary
review classification request
```

## 11. Formal Verification Bridge

Formal or Lean-facing claims should be routed through:

```text
KuuOS governance invariant
  -> formal invariant spine
  -> Lean / proof repository
  -> CI check
  -> review-gated theorem surface
  -> no proof overclaim
```

For the 4D mass gap proof architecture, use the repository:

```text
itakura-hidetoshi/4d-mass-gap
```

The formal bridge is documented in:

```text
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
```

## 12. Recommended GPT Prompts

### Repository orientation

```text
Read the KuuOS repository and summarize the current governance entry points, validation commands, and non-authority boundaries.
```

### PR review

```text
Review this PR under KuuOS governance. Classify it as PASS, HOLD, REPAIR, REJECT, or QUARANTINE. Cite the relevant files and explain which invariants are touched.
```

### CI failure triage

```text
Read the failing GitHub Actions logs and classify the failure under KuuOS governance: missing file, validator drift, fixture mismatch, boundary weakening, or environment drift.
```

### Consistency check

```text
Check README.md, KUOS_CORE_GOVERNANCE_INDEX_v0_1.md, and ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md for inconsistency. Propose append-only or tighten-only repairs.
```

## 13. Non-Authority Fixed Points

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
Release mode: append-only / tighten-only / overwrite-forbidden

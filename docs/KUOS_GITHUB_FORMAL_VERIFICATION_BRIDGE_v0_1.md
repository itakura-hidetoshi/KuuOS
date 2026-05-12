# KuuOS GitHub Formal Verification Bridge v0.1

## 空OS GitHub 形式検証ブリッジ

This document defines how KuuOS should route GitHub-facing formal, Lean, theorem, proof, and proof-adjacent claims.

The bridge connects KuuOS governance surfaces to proof-facing repositories without converting validation, CI, or GPT review into proof authority.

## 1. Purpose

KuuOS may use GitHub as a public surface for:

```text
governance specification
formal invariant spine
Lean / proof scaffolding
CI validation
release checkpointing
review-gated theorem surface
```

This bridge prevents the following invalid collapse:

```text
repository existence
  -> CI pass
  -> validator pass
  -> GPT summary
  -> proof claim
```

## 2. Canonical Routing

Proof-facing work should be routed as:

```text
KuuOS governance invariant
  -> formal invariant spine
  -> proof-facing repository
  -> Lean / checker / validator surface
  -> CI replay
  -> human or external review
  -> review-gated theorem surface
```

At no point does GPT output itself become proof authority.

## 3. Current Proof-Facing Repository

The current 4D mass gap proof architecture is connected through:

```text
itakura-hidetoshi/4d-mass-gap
```

KuuOS should treat that repository as a proof-facing verification subdomain, not as a replacement for KuuOS governance.

## 4. GPT Role

GPT may:

```text
read formal files
summarize theorem surfaces
compare checkpoints
inspect CI failures
explain validator failures
propose issue drafts
propose PR review notes
identify missing formal links
classify proof-surface risk
```

GPT must not:

```text
declare final proof completion from prose
convert Lean stubs into proof completion
convert CI pass into theorem truth
convert internal architecture into public mathematical acceptance
hide remaining assumptions
hide review gates
erase external audit requirements
```

## 5. Formal Claim Classification

GPT should classify formal claims as:

```text
DOCUMENTED
FORMAL_STUBBED
CHECKER_VALIDATED
CI_REPLAYED
REVIEW_GATED
EXTERNALLY_REVIEWED
PUBLIC_THEOREM_CLAIM
```

A claim may move upward only with explicit evidence.

## 6. Required Non-Authority Fixed Points

```text
formal_file_not_proof_by_itself
lean_stub_not_theorem_completion
ci_pass_not_theorem_truth
validator_pass_not_mathematical_acceptance
GPT_summary_not_proof_authority
repository_state_not_public_acceptance
internal_checkpoint_not_external_audit
review_gate_required_for_public_final_claim
```

## 7. PR Review Questions for Formal Changes

For every formal or theorem-facing PR, GPT should answer:

```text
1. Which theorem, invariant, or proof surface is touched?
2. Is the touched file documentation, stub, checked Lean, validator, or release surface?
3. Does the PR introduce, remove, or weaken assumptions?
4. Does it change public claim strength?
5. Does CI or local replay support the change?
6. Are review gates preserved?
7. Is any overclaim introduced?
8. Classification: PASS / HOLD / REPAIR / REJECT / QUARANTINE
```

## 8. Bridge to GPT GitHub Integration

This document is subordinate to:

```text
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
```

## 9. Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
Release mode: append-only / tighten-only / overwrite-forbidden

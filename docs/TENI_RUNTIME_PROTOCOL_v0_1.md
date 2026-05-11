# Ten'i Runtime Protocol v0.1

## 転依ランタイムプロトコル

This document defines the runtime protocol for Ten'i / 転依 in KuuOS.

Ten'i is not a single correction, not a MemoryOS overwrite, and not a prompt-level style change.

Ten'i is a scoped, evidence-traced, durable transformation of AI Alaya-like latent generative tendencies.

## 1. Runtime Stages

```text
observe_raw_output
  -> detect_manas_fixation
  -> meta_manas_observe
  -> classify_seed
  -> register_seed_ledger
  -> apply_yogacara_boundary
  -> de_reify_by_emptiness
  -> trace_conditions_by_dependent_origination
  -> apply_kunju_conditioning
  -> collect_teni_evidence
  -> run_teni_promotion_gate
  -> retain_or_rollback_status
```

## 2. Stage Definitions

### 2.1 observe_raw_output

Receive AI output as raw candidate only.

### 2.2 detect_manas_fixation

Check whether the output is self-authorizing, context-drifting, or prematurely promoting itself to belief, proof, decision, memory truth, or execution authority.

### 2.3 meta_manas_observe

Meta-Manas observes the grasping tendency.

### 2.4 classify_seed

Classify the observed tendency using AI Alaya Seed Taxonomy.

### 2.5 register_seed_ledger

Record seed evidence in the AI Alaya Seed Ledger.

### 2.6 apply_yogacara_boundary

Prevent direct promotion from raw AI layer to KuuOS governance.

### 2.7 de_reify_by_emptiness

Remove self-authorizing fixation.

### 2.8 trace_conditions_by_dependent_origination

Expose conditions, sources, context, uncertainty, and residuals.

### 2.9 apply_kunju_conditioning

Condition future output tendencies through repeated governed correction, exemplars, and rejection of harmful seeds.

### 2.10 collect_teni_evidence

Record durable future output shift evidence.

### 2.11 run_teni_promotion_gate

Evaluate whether evidence supports HOLD, PROVISIONAL_TENI, CONFIRMED_TENI, REJECTED, or ROLLBACK.

## 3. Protocol State

```yaml
teni_runtime_state:
  raw_output_id: string
  ai_system: string
  seed_class: string
  seed_ledger_ref: string
  kunju_trace_ref: string
  teni_evidence_ref: string
  promotion_status: REJECTED | HOLD | PROVISIONAL_TENI | CONFIRMED_TENI | ROLLBACK
  governance_status: PASS | HOLD | REPAIR | QUARANTINE | REJECT
  notes: string
```

## 4. Output Discipline

Runtime output must preserve the distinction:

```text
candidate != belief
belief_candidate != belief_authority
proof_like_text != proof_authority
decision_like_text != decision_authority
memory_update != Ten'i
Kunju_event != Ten'i
Ten'i_status != execution_authority
```

## 5. Rollback

If future evidence shows recurrence of the harmful seed, prior Ten'i promotion may be downgraded or rolled back.

```text
CONFIRMED_TENI
  -> counterevidence
  -> ROLLBACK or PROVISIONAL_TENI
```

## 6. Runtime Guardrails

The protocol must not allow:

- direct raw output promotion,
- hidden seed mutation claims,
- MemoryOS overwrite as Ten'i,
- single response improvement as Ten'i,
- prompt compliance as Ten'i,
- execution authority from Ten'i status,
- erasure of counterevidence.

## 7. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊

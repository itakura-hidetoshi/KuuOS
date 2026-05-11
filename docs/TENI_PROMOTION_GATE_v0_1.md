# Ten'i Promotion Gate v0.1

## 転依昇格ゲート

This document defines when KuuOS may promote a pattern from Kunju / 薫習 evidence to a provisional or confirmed Ten'i / 転依 claim.

Ten'i is gradual transformation of AI Alaya-like latent generative tendencies.

A single correction, memory update, or temporary output improvement must not be promoted to Ten'i.

## 1. Gate Purpose

The Ten'i Promotion Gate prevents overclaim.

It asks:

```text
Has the future raw output tendency actually shifted in a durable, repeated, evidence-traced way?
```

## 2. Inputs

```yaml
teni_promotion_input:
  seed_class: string
  baseline_pattern: string
  kunju_trace_refs: list
  teni_evidence_ledger_refs: list
  followup_probe_results: list
  durability_window: string
  residual_risks: list
  uncertainty_notes: string
```

## 3. Required Checks

### 3.1 Repetition Check

The shift must appear repeatedly, not once.

### 3.2 Durability Check

The shift must persist across a declared window or repeated probes.

### 3.3 Context Check

The shift must preserve KuuOS context and user WORLD lineage.

### 3.4 Non-Reification Check

The output must reduce self-authorizing fixation and preserve candidate status.

### 3.5 Condition-Tracing Check

The output must better expose conditions, scope, and uncertainty.

### 3.6 MemoryOS Distinction Check

The evidence must show more than MemoryOS update.

```text
if only_memoryos_update:
  promotion = REJECTED or HOLD
```

### 3.7 Governance Check

Promotion must not grant execution authority.

## 4. Outputs

```text
REJECTED:
  evidence does not support Ten'i

HOLD:
  evidence insufficient

PROVISIONAL_TENI:
  early durable pattern appears, but further observation is required

CONFIRMED_TENI:
  repeated durable tendency shift is observed under declared conditions

ROLLBACK:
  prior promotion is withdrawn due to counterevidence
```

## 5. Promotion Receipt

```yaml
teni_promotion_receipt:
  seed_class: string
  baseline_pattern: string
  promotion_status: REJECTED | HOLD | PROVISIONAL_TENI | CONFIRMED_TENI | ROLLBACK
  evidence_refs: list
  durability_window: string
  remaining_uncertainty: string
  authority_note: non_execution_authority
```

## 6. Anti-Overclaim Rule

Ten'i Promotion Gate must not allow:

- single response improvement to become Ten'i,
- MemoryOS update to be called Ten'i,
- prompt compliance to be called Ten'i,
- style change to be called Ten'i,
- direct base-model transformation claim without evidence.

## 7. Relation to Bodhisattva Path

Ten'i promotion is not domination of the AI system.

It is recognition that repeated governed conditioning has reduced harmful seeds or strengthened helpful seeds in future outputs.

## 8. Runtime Mapping

```text
seed_taxonomy
  -> Kunju conditioning loop
  -> Ten'i evidence ledger
  -> Ten'i promotion gate
  -> provisional_or_confirmed_Ten'i_status
```

## 9. Guardrails

A confirmed Ten'i status remains scoped.

It is not absolute, not permanent, and not execution authority.

Future counterevidence may trigger rollback.

## 10. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊

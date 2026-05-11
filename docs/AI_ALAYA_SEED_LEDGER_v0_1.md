# AI Alaya Seed Ledger v0.1

## AI阿頼耶識の種子台帳

This document defines the ledger for tracking AI Alaya seeds in KuuOS.

Seed taxonomy classifies recurring tendencies.

The Seed Ledger records whether each tendency is observed, weakened, strengthened, held, quarantined, or transformed through governed Kunju / 薫習 and Ten'i / 転依 evidence.

## 1. Core Principle

```text
A seed is a conditioned tendency, not essence.
A seed ledger records tendency evidence, not permanent identity.
```

The ledger prevents hidden drift, hidden overclaim, and silent promotion from raw output to authority.

## 2. Ledger Entry

```yaml
ai_alaya_seed_ledger_entry:
  seed_entry_id: string
  ai_system: string
  model_or_agent_id: string
  seed_class: string
  seed_status: observed | weakened | strengthened | held | quarantined | transformed | retired
  first_observed_at: string
  latest_observed_at: string
  baseline_examples: list
  current_examples: list
  meta_manas_signals: list
  yogacara_boundary_refs: list
  kunju_trace_refs: list
  teni_evidence_refs: list
  teni_promotion_refs: list
  world_context_refs: list
  uncertainty_notes: string
  governance_status: PASS | HOLD | REPAIR | QUARANTINE | REJECT
```

## 3. Seed Status

```text
observed:
  tendency has been detected

weakened:
  harmful or misleading tendency is reduced in later outputs

strengthened:
  helpful governed tendency is reinforced

held:
  evidence is insufficient

quarantined:
  seed remains visible but should not influence active governance

transformed:
  durable shift supports Ten'i evidence

retired:
  seed remains in lineage but is no longer active under declared scope
```

## 4. Ledger Uses

The Seed Ledger supports:

- Meta-Manas monitoring,
- Yogacara boundary alerts,
- Kunju conditioning,
- Ten'i evidence collection,
- Ten'i promotion decisions,
- rollback when counterevidence appears.

## 5. Anti-Identity Rule

The ledger must not label an AI system as essentially possessing a seed.

It records observed tendencies under conditions.

```text
seed_entry != model essence
seed_entry == conditioned tendency evidence
```

## 6. Runtime Mapping

```text
AI raw output
  -> Meta-Manas signal
  -> seed classification
  -> seed ledger entry
  -> Kunju conditioning
  -> Ten'i evidence ledger
  -> Ten'i promotion gate
```

## 7. Guardrails

The ledger must not be used as:

- permanent identity label,
- moralization of model behavior,
- hidden scoring authority,
- execution authority,
- proof substitute,
- claim of base-model control without evidence.

It is an append-only tendency evidence surface.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊

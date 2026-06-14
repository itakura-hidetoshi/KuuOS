# Kū–Indra Qi Generational Governance v0.13

## Purpose

v0.13 adds a bounded, non-authoritative governance layer above the v0.12 bounded generational cycle. It does not execute another generation. It observes the exact v0.12 handoff, record, and runner state after each committed generation and maintains an append-only governance lineage.

The layer answers four questions:

1. Is the v0.12 digest lineage exact and monotone?
2. Is multi-generation drift still bounded?
3. Does deterministic regression replay reproduce the expected outputs?
4. Is collapse pressure low enough to permit a bounded promotion recommendation?

## Inputs

Each review consumes:

- the current `indra_qi_bounded_cycle_handoff_v0_12.json`;
- the current `indra_qi_bounded_cycle_record_v0_12.json`;
- the current `indra_qi_bounded_cycle_state_v0_12.json`;
- a digest-bound v0.13 governance plan and license;
- a replay report whose cases bind the current generation handoff digest and compare expected versus observed output digests.

The v0.12 source files are read-only. v0.13 writes only its own state, recommendation, receipt, audit, and append-only ledger.

## Exact continuity

For every generation after the first observed generation, v0.13 requires:

- `generation_index = previous_generation_index + 1`;
- the current v0.12 `prev_runner_state_digest` to equal the previously observed v0.12 state digest;
- the current source v0.11 handoff digest to equal the previous generation's target v0.11 handoff digest;
- a fresh review-run ID and a previously unconsumed v0.12 generation handoff digest.

Any integrity or continuity loss fails closed and yields a quarantine recommendation without committing a new governance observation.

## Drift and collapse pressure

The bounded observation window tracks:

- increase in maximum observation debt;
- loss of minimum recoverability reserve;
- increase in maximum intervention residue;
- adverse step count and consecutive regression count;
- weighted collapse pressure.

The window has explicit minimum and maximum generation counts. It cannot grow without bound.

## Regression replay

A replay case contains:

- a unique case ID;
- the exact source generation handoff digest;
- a replay-input digest;
- an expected-output digest;
- an observed-output digest.

v0.13 computes pass/fail from digest equality. A self-declared boolean cannot grant replay success.

## Decisions

v0.13 emits exactly one recommendation:

- `hold_for_observation`: the minimum generation or replay window is not yet available;
- `promote_bounded`: replay passed and drift, regression count, and collapse pressure are all bounded;
- `rollback_recommended`: replay or bounded-regression conditions failed while lineage integrity remains available;
- `quarantine_recommended`: integrity failed or collapse pressure/regression persistence reached the quarantine threshold.

`promote_bounded` is deliberately named as a bounded recommendation. It is not a truth assertion or an execution command.

## Outputs

```text
indra_qi_generational_governance_state_v0_13.json
indra_qi_generational_governance_recommendation_v0_13.json
indra_qi_generational_governance_ledger_v0_13.jsonl
indra_qi_generational_governance_receipt_v0_13.json
indra_qi_generational_governance_audit_v0_13.jsonl
```

## Authority boundary

v0.13 grants no direct promotion, rollback, quarantine, execution, external-world actuation, or truth authority. It preserves candidate-weighting-as-non-truth, non-Markov feedback provenance, and Process Tensor provenance. All recommendations require a separate licensed consumer before any later runtime action can occur.

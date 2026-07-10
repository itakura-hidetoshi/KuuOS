# PlanOS Subsequent-Cycle Candidate-Generation Start Receipt v0.65

PlanOS v0.65 converts the v0.64 subsequent-cycle replan request into a bounded candidate-generation start receipt.

This layer records the start of candidate generation for the subsequent cycle.

It does not materialize a candidate set, select a candidate, or request admission.

## Input

The source input is `kuuos_planos_subsequent_cycle_replan_request_v0_64`.

The source must be ready.

The previously selected candidate must remain bound to the subsequent-cycle replan request record as the provenance anchor.

The source must preserve the complete memory overwrite, truth authority, blocker release, next-cycle admission, start, closeout, and subsequent-cycle replan-request chain.

The source must record a replan request with candidate generation and subsequent-cycle admission still unopened.

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_READY` when the source request checks pass.

The output contains:

- selected candidate provenance id
- selected candidate provenance digest
- source subsequent-cycle replan request digest
- candidate-generation start receipt record
- receipt digest

## Required boundary

- receipt owned by PlanOS = true
- source subsequent-cycle replan request preserved = true
- selected candidate bound to replan request = true
- memory overwrite and closeout preserved = true
- truth authority and closeout preserved = true
- blocker release and closeout preserved = true
- next-cycle admission, start, and closeout chain preserved = true
- subsequent-cycle replan request preserved = true
- subsequent-cycle replan requested = true
- subsequent-cycle candidate-generation start receipt only = true
- subsequent-cycle candidate generation started = true

## Closed boundary

- subsequent-cycle candidate set materialized = false
- subsequent-cycle candidate selected = false
- subsequent-cycle admission requested = false

## Authority boundary

This layer records only the start of candidate generation.

The receipt recorder itself remains non-authoritative.

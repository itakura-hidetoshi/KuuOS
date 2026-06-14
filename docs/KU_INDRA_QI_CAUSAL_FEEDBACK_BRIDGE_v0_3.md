# Kū–Indra Qi Causal Feedback Bridge v0.3

## Purpose

This bridge returns eligible KuuOS v14 causal events to the Indra–Qi Mandala layer as bounded feedback candidates.

```text
Indra–Qi WORLD
  -> v0.2 local causal projection
  -> v14 observe / intervene / counterfactual / undo
  -> v0.3 feedback candidates
  -> approval handoff
  -> later licensed WORLD mutation review
```

The bridge does not directly mutate the Indra–Qi WORLD state.

## Candidate kinds

```text
local_patch_observation_candidate
qi_flow_observable_candidate
```

A local causal variable is mapped back through the source binding stored in the v0.2 projection packet. A Qi-flow variable remains an observable projection of a flow and is never promoted to Qi itself.

## Causal events

The following v14 events may produce feedback:

```text
observe
intervene
counterfactual
undo
```

`initialize` and `inspect` are not feedback evidence. Counterfactual output remains projection-only and receives a lower default candidate weight than direct observation.

## Candidate weighting

Candidate weight is calculated from an event-kind base weight and visible uncertainty:

```text
candidate_weight
= clamp(base_weight(event_kind) - uncertainty_penalty * uncertainty)
```

The weight is a review priority, not truth, confidence certification, or execution permission.

## Protected structures

The bridge cannot infer a gauge-connection change from a causal edge. It does not change:

- local noncommutative operator algebras;
- IndraNet gauge connections;
- holonomy;
- transport residue;
- Mandala inclusion;
- the source Indra–Qi state;
- the external world.

## Approval handoff

Successful candidate generation emits an approval handoff. The handoff is not an approval and cannot apply candidates. It requests a later bounded review stage that may construct a separately licensed WORLD mutation.

## Runtime outputs

```text
indra_qi_causal_feedback_candidate_packet_v0_3.json
indra_qi_causal_feedback_approval_handoff_v0_3.json
indra_qi_causal_feedback_ledger_v0_3.jsonl
indra_qi_causal_feedback_receipt_v0_3.json
indra_qi_causal_feedback_audit_v0_3.jsonl
```

## Fail-closed conditions

The bridge blocks on broken v0.2 lineage, invalid Indra–Qi or v14 digests, ineligible events, missing causal results, direct-apply requests, gauge-update inference, Qi identity collapse, missing boundaries, replay, or license mismatch.

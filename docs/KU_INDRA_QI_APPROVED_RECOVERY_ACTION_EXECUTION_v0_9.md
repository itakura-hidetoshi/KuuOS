# Kū–Indra Qi Approved Recovery Action Execution v0.9

## Purpose

v0.9 consumes exactly one candidate from the v0.8 recoverability-gated action envelope, executes the approved action inside the isolated child v14 causal WORLD, and returns the resulting causal event to the existing v0.3 feedback bridge.

```text
v0.8 action envelope
  -> exact candidate digest
  -> fresh observation evidence
  -> single-candidate approval
  -> fresh v14 action license
  -> child v14 action
  -> v0.3 feedback candidates
```

The action changes only the internal child causal WORLD when the selected command is an observation or intervention. It never actuates an external system and never mutates the parent Indra–Qi WORLD.

## Exact binding

The execution plan binds:

- action-envelope ID and digest;
- v0.8 activation-record digest;
- v0.7 reentry ID and record digest;
- current parent WORLD and dynamic-WORLD digests;
- current child v14 WORLD digest;
- selected candidate ID, digest, and action kind;
- one action transaction ID;
- fresh-observation evidence digest;
- approval digest;
- a fresh execution-plan digest.

The selected candidate must occur in exactly one v0.8 collection. Candidate IDs without the exact candidate digest are insufficient.

## Fresh observation evidence

Every action kind requires evidence bound to the current child v14 digest and the selected variable.

```text
fresh evidence value = current v14 variable value
instrument trace digest != empty
source envelope digest = current envelope digest
```

The evidence is not truth and does not itself authorize action.

## Single-candidate approval

Approval is restricted to one candidate and one transaction. It binds the candidate digest, evidence digest, action kind, envelope digest, and transaction ID.

Approval does not provide external-world authority, parent-WORLD mutation authority, or operator-algebra authority. A separate v14 command license bound to the generated command digest remains mandatory.

## Action paths

### Observation

The fresh observed value is written to the selected child-v14 variable. v14 creates a reversible snapshot, advances the causal-model revision, propagates derived variables, and records a causal event.

### Counterfactual

The approved value must remain inside the v0.8 counterfactual interval. v14 produces a projected result and event while preserving the persistent child-v14 state digest.

### Bounded intervention

The approved value must remain within the v0.8 maximum delta. The candidate must have exactly one matching v0.8 undo reserve.

After execution, v0.9 verifies the real v14 snapshot and writes an undo-readiness packet containing:

- the exact target action transaction;
- the verified pre-action snapshot digest;
- an exact undo command;
- an undo license bound to that command digest;
- the matching v0.8 undo-reserve digest.

The undo command is ready but is not executed during a successful v0.9 transaction.

## Feedback return

After a successful v14 action, v0.9 builds a v0.3 feedback plan from the exact event record and result. The existing feedback bridge emits local-patch and Qi-flow feedback candidates.

```text
executed internal action
  -> causal event
  -> causal result
  -> v0.3 feedback candidate packet
  -> approval handoff
```

Feedback remains candidate-only and cannot directly mutate the Indra–Qi WORLD.

## State boundaries

```text
parent Indra–Qi WORLD: unchanged
child Indra–Qi copy: unchanged
child v14 causal WORLD:
  observation/intervention -> internally changed
  counterfactual -> persistent state unchanged
external world: never actuated
base gauge connection: unchanged
operator algebra: unchanged
```

## Outputs

Parent runtime:

```text
indra_qi_approved_recovery_action_execution_record_v0_9.json
indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl
indra_qi_approved_recovery_action_execution_receipt_v0_9.json
indra_qi_approved_recovery_action_execution_audit_v0_9.jsonl
```

Child runtime:

```text
v14 event / result / snapshot
indra_qi_v0_9_undo_readiness_<execution_id>.json   # intervention only
indra_qi_causal_feedback_candidate_packet_v0_3.json
indra_qi_causal_feedback_approval_handoff_v0_3.json
indra_qi_causal_feedback_ledger_v0_3.jsonl
```

## Fail-closed conditions

Execution is blocked before the v14 command when any exact binding, evidence, approval, candidate bound, nested action license, undo license, feedback license, WORLD digest, or lineage digest is missing or inconsistent. Reuse of an execution ID, source envelope, or selected candidate digest is blocked.

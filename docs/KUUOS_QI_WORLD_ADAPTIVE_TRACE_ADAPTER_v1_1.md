# KuuOS Qi–WORLD Adaptive Trace Adapter v1.1

## Purpose

v1.0 defined the abstract relation between WORLD, the Qi Process Tensor, the OS family, and Governance. v1.1 binds that relation to the existing `AdaptiveAgentTransitionKernel` without inventing a second execution path.

This is a concrete receipt adapter, not a new controller.

```text
existing adaptive transition trace
  → ordered state/event digests
  → Qi process-history evidence
  → read-only WORLD projection bundle
  → concrete BeliefOS / DecisionOS / PlanOS / Governance /
     ActOS / ObserveOS / VerifyOS / LearnOS packets
  → v1.0 Qi–WORLD interface receipt
```

## Concrete trace

The adapter replays the existing transition kernel through:

```text
initial BELIEF state
→ DECISION_COMMITTED
→ PLAN_BOUND
→ AUTHORITY_BOUND
→ LEASE_ACTIVATED
→ SESSION_BOOTSTRAPPED
→ ACT_AUTHORIZED
→ EFFECT_RECORDED
→ OBSERVATION_COMMITTED
→ VERIFICATION_PASSED
→ LEARNING_COMMITTED
```

This yields 10 events and 11 states.

The adapter validates every event and state digest and replays each event from its predecessor state. A stored target state is accepted only when its digest equals the replayed target digest.

## OS bindings

| OS | Concrete source |
|---|---|
| BeliefOS | initial adaptive state at `BELIEF` |
| DecisionOS | state after `DECISION_COMMITTED` |
| PlanOS | plan digest after `PLAN_BOUND` |
| Governance | authority + lease + session bound state |
| ActOS | state after authorized effect completion |
| ObserveOS | evidence digest from `OBSERVATION_COMMITTED` |
| VerifyOS | verification digest from `VERIFICATION_PASSED` |
| LearnOS | next-plan digest from `LEARNING_COMMITTED` |

All packets share one derived Qi process-lineage digest, built from:

- the adaptive lineage ID;
- the initial state digest;
- the ordered event-digest sequence;
- the final state digest.

## Governance and authority

The concrete Governance packet is bound to the existing:

```text
AUTHORITY_BOUND
LEASE_ACTIVATED
SESSION_BOOTSTRAPPED
```

state sequence.

ActOS must reference both:

- the Governance output digest; and
- the existing external authority-receipt digest.

The adapter does not issue either one.

## WORLD projection

The WORLD packet is a read-only bundle containing:

- initial adaptive-state digest;
- post-effect state digest;
- observation state digest;
- observation evidence digest.

It remains candidate-only and non-final:

```text
exact_world_identified = false
runtime_updates_world = false
multi_world_noncollapse = true
two_truths_gap = true
```

## Qi process history

Each adaptive event becomes a process-history item carrying:

- event kind and event digest;
- predecessor and successor state digests;
- visible transition continuity;
- memory-link visibility;
- non-Markov link visibility after sufficient history.

The existing Qi Process Tensor evaluator remains the source of process-visibility evidence. The adapter does not replace or upgrade it.

## Rejected substitutions

The validator rejects:

- event reordering, including verification before observation;
- state-digest substitution;
- OS packet attachment to another Qi lineage;
- missing external authority at ActOS;
- substituted observation evidence, even when VerifyOS is altered to match it;
- LearnOS past overwrite;
- invalid inner v1.0 interface receipts.

## Non-authority boundary

```text
adapter_grants_execution = false
adapter_grants_truth = false
adapter_issues_authority = false
adapter_changes_governance_decision = false
adapter_updates_exact_world = false
adapter_overwrites_history = false
```

## Central registration

v1.1 also repairs the central registration surface:

- `formal/KUOS.lean` imports Qi–WORLD v1.0, this v1.1 adapter, and WORLD v0.40;
- `scripts/run_kuuos_runtime_full_check_v0_1.py` runs both Qi–WORLD checks and the v1.1 unit tests.

The result is a concrete, replay-checked integration of existing components rather than an additional autonomous execution layer.

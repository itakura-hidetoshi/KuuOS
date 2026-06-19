# KuuOS Qi–WORLD Native Full OS Cycle v1.3

## Purpose

v1.3 connects the upper native reasoning chain to the lower native evidence loop.

```text
BeliefOS v0.3 coherence receipt
→ DecisionOS v0.1 committed decision
→ DecisionOS v0.2 plural deliberation
→ DecisionOS v0.3 Wa review
→ PlanOS v0.1 committed plan
→ Governance step authorization + host license
→ ActOS v0.1 committed effect
→ ObserveOS v0.1 committed evidence
→ VerifyOS v0.1 committed adjudication
→ LearnOS v0.1 future-only learning
```

No replacement kernel is introduced. Every artifact is produced by the existing native kernel or store surface.

## Canonical bindings

```text
DecisionOS.source_belief_receipt_digest
  = BeliefOS.belief_gerbe_receipt_digest

DecisionOSPlural.source_decision_state_digest
  = DecisionOS.decision_state_digest

DecisionOSWa.source_plural_state_digest
  = DecisionOSPlural.plural_state_digest

PlanOS.source_wa_state_digest
  = DecisionOSWa.wa_state_digest

ActOS.source_plan_state_digest
  = PlanOS.plan_state_digest

ObserveOS.source_act_state_digest
  = ActOS.act_state_digest

VerifyOS.source_observe_state_digest
  = ObserveOS.observe_state_digest

LearnOS.source_verify_state_digest
  = VerifyOS.verify_state_digest
```

The Decision basis is also preserved through plural, Wa, Plan, and Act. All native artifacts share one declared lineage ID, and all stages from DecisionOS onward share one mission-contract digest.

## BeliefOS artifact

BeliefOS v0.3 produces a canonical coherence receipt rather than a conventional mutable state packet. The full-cycle receipt therefore stores both:

- the digest-valid Belief gerbe store state;
- the applied CANDIDATE coherence receipt.

DecisionOS v0.1 binds the exact coherence-receipt digest as its source belief basis.

## Governance boundary

Governance remains cross-cutting. At the operational boundary it is represented by two independent native artifacts:

```text
ActOS.step_authorization_digest
ActOS.host_license_digest
```

The first records Plan-bound admission. The second records external execution authority. Neither is synthesized by the v1.3 adapter.

## Qi Process Tensor projection

The canonical artifacts are projected into a seven-record process history:

```text
BELIEF_COHERENCE_COMMITTED
DECISION_WA_COMMITTED
PLAN_COMMITTED
ACT_EFFECT_RECORDED
OBSERVATION_RECORDED
VERIFICATION_RECORDED
FUTURE_LEARNING_RECORDED
```

The existing Qi evaluator remains responsible for transition, memory, and non-Markov visibility.

## WORLD projection

The read-only WORLD bundle contains the canonical digests for Belief, Decision, plural deliberation, Wa, Plan, Act, Observe, Verify, and Learn, together with evidence, verification, and learning-delta digests.

```text
projection_read_only = true
candidate_only = true
nonfinal_marker = true
exact_world_identified = false
runtime_updates_world = false
multi_world_noncollapse = true
two_truths_gap = true
```

## Rejected substitutions

The runtime rejects substitutions at every direct boundary, even when the modified artifact digest is recomputed:

- substituted Belief receipt;
- Decision detached from Belief;
- plural deliberation detached from Decision;
- Wa review detached from plural deliberation;
- Plan detached from Wa;
- Act detached from Plan;
- Observe detached from Act;
- Verify detached from Observe;
- Learn detached from Verify;
- missing external Act authority.

## Boundary

```text
adapter_grants_execution = false
adapter_grants_truth = false
adapter_issues_authority = false
adapter_changes_native_artifacts = false
adapter_updates_exact_world = false
adapter_overwrites_history = false
```

The v1.3 adapter validates and packages an already-produced native cycle. It does not select, plan, execute, observe, verify, learn, or govern on behalf of the underlying OS kernels.

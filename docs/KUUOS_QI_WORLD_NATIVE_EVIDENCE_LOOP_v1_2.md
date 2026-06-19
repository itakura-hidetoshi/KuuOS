# KuuOS Qi–WORLD Native Evidence Loop v1.2

## Purpose

v1.1 connected the Qi–WORLD interface to the global adaptive transition trace. v1.2 connects the same interface to the **native committed states** produced by the existing ActOS, ObserveOS, VerifyOS, and LearnOS kernels.

No replacement kernel is introduced.

```text
committed Plan identity retained by ActOS
→ native ActOS effect state
→ native ObserveOS evidence state
→ native VerifyOS adjudication state
→ native LearnOS future-only state
→ Qi process lineage + read-only WORLD projection
```

## Native construction

The validation scenario invokes the existing fixture and store paths in one continuous chain:

1. ActOS executes an authorized fixture operation and commits `EFFECT_RECORDED`.
2. That exact ActOS state is passed into `build_initial_observe_state`.
3. ObserveOS collects, traces, assesses, compares, and commits `OBSERVATION_MATCHED`.
4. That exact ObserveOS state is passed into `build_initial_verify_state`.
5. VerifyOS binds the criterion, challenge, corroboration, adjudication, and commits `VERIFICATION_PASSED`.
6. That exact VerifyOS state is passed into `build_initial_learn_state`.
7. LearnOS abstracts, challenges, creates a reinforcement delta, applies the middle-way gate, and commits a future-only learning candidate.

Every state is checked again by its native validator:

```text
validate_act_state
validate_observe_state
validate_verify_state
validate_learn_state
```

## Provenance equalities

The convergence receipt requires:

```text
ObserveOS.source_act_state_digest
  = ActOS.act_state_digest

VerifyOS.source_observe_state_digest
  = ObserveOS.observe_state_digest

VerifyOS.source_act_state_digest
  = ActOS.act_state_digest

LearnOS.source_verify_state_digest
  = VerifyOS.verify_state_digest

LearnOS.source_observe_state_digest
  = ObserveOS.observe_state_digest

LearnOS.source_act_state_digest
  = ActOS.act_state_digest
```

All four native states must also carry the same lineage ID and mission-contract digest.

## Qi process history

The native state chain becomes four visible process-history records:

```text
ACT_EFFECT_RECORDED
OBSERVATION_RECORDED
VERIFICATION_RECORDED
FUTURE_LEARNING_RECORDED
```

Each item carries its canonical state digest and its direct source-state digest. The existing Qi Process Tensor evaluator determines whether transition, memory, and non-Markov continuity are visible.

## WORLD projection

The read-only WORLD projection contains:

- source Plan state and committed Plan digests;
- ActOS state digest;
- ObserveOS state and evidence-packet digests;
- VerifyOS state and verification-evidence digests;
- LearnOS state and learning-delta digests.

It does not claim to be the exact WORLD:

```text
projection_read_only = true
candidate_only = true
nonfinal_marker = true
exact_world_identified = false
runtime_updates_world = false
multi_world_noncollapse = true
two_truths_gap = true
```

## Relation to all OS interfaces

ActOS preserves the upstream Plan, Decision/Wa, mission, authorization, and host-license identities. v1.2 therefore represents:

- BeliefOS, DecisionOS, and PlanOS as upstream identity projections retained by ActOS;
- Governance through the native step-authorization and host-license pair;
- ActOS, ObserveOS, VerifyOS, and LearnOS through their full native committed states.

The projection-only upstream packets are explicitly marked and are not presented as native BeliefOS or DecisionOS states.

## Governance and authority

The Governance packet uses the native ActOS step-authorization digest. ActOS separately binds the native host-license digest as its external authority receipt.

```text
step authorization ≠ host license
plan identity ≠ execution permission
adapter ≠ authority issuer
```

## Rejected mutations

The runtime scenarios reject:

- removal of the native ActOS effect flag, even after recomputing the ActOS digest;
- ObserveOS substitution of the source ActOS digest;
- VerifyOS substitution of the source ObserveOS digest;
- LearnOS substitution of the source VerifyOS digest;
- LearnOS mutation of past-record preservation;
- removal of external ActOS authority;
- a WORLD projection that claims runtime mutation.

## Boundary

```text
adapter_grants_execution = false
adapter_grants_truth = false
adapter_issues_authority = false
adapter_changes_native_state = false
adapter_updates_exact_world = false
adapter_overwrites_history = false
```

The adapter certifies convergence among existing artifacts. It does not execute, adjudicate, learn, or govern on behalf of the native OS kernels.

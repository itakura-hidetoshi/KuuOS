# KuuOS CodeAI Intent and Repository Observation Envelope v0.1

## Status

This document specifies an additive, read-only CodeAI profile adapter. It is
not part of the canonical current root and does not extend the completed
repository-mutation lineage.

The kernel consumes already-collected intent and repository artifacts. It does
not inspect a live repository, run a model, generate a patch, invoke a tool, or
change Git state.

## Preserved invariants

```text
intent != authority
intent != truth
repository observation != repository truth
observation intake != observation collection
observation != code change candidate
observation != selection
observation != execution lease
observation != repository mutation
validation != correctness proof
route receipt != successor authority
```

The source commit is preserved exactly in every emitted route receipt.

## Semantic difference from existing lines

- ObserveOS owns general source-bound observation envelopes. CodeAI v0.1 only
  binds supplied intent and repository-development artifacts for a coding
  profile.
- The repository mutation and self-organization lines model and validate
  repository evolution artifacts. CodeAI v0.1 performs no mutation and grants
  no transition authority into those lines.
- VerifyOS owns independent verification outcomes. CodeAI v0.1 records
  baseline evidence identifiers but does not verify functional correctness.
- PlanOS and DecisionOS may later consume a supported CodeAI receipt through a
  separate adapter. This version creates no candidate and selects nothing.

## Inputs

### Intent packet

The intent packet binds:

- stable intent identifier and revision;
- source actor and source channel;
- explicit requirements and assumptions;
- unresolved questions;
- preserved invariants and forbidden changes;
- success criteria;
- the authority owner responsible for the request;
- creation epoch and prior intent digests;
- an explicit provenance-confirmed predicate;
- a canonical SHA-256 packet digest.

An intent packet with unresolved questions is not silently completed. It routes
to `intent_clarification_hold`.

### Repository observation

The repository observation binds:

- repository identity, source branch, and exact source commit SHA;
- repository tree, dependency lock, and toolchain digests;
- observed and unavailable path partitions;
- baseline check evidence identifiers;
- code-owner scope and an unowned-boundary predicate;
- a bounded observation window;
- session, nonce, and prior-observation replay context;
- negative kernel-effect predicates;
- negative authority-claim predicates;
- a canonical SHA-256 observation digest.

The kernel does not claim that the supplied path set is the complete live
repository. It validates only the declared path partition and policy bounds.

### Observation policy

The policy binds the expected repository and source commit, allowed source
branches, supported toolchains, path and duration budgets, baseline and
code-owner requirements, and whether partial read-only observation may degrade
instead of being rejected.

## Deterministic disposition order

After exact-field, type, and digest preflight, the kernel selects exactly one
route in this order:

1. intent provenance repair;
2. repository identity repair;
3. repository snapshot repair;
4. path-accounting repair;
5. baseline-evidence repair;
6. observation-window repair;
7. replay rejection;
8. repository-mutation rejection;
9. authority-escalation rejection;
10. intent-clarification hold;
11. unsupported-toolchain abstention;
12. ownership handover;
13. partial-observation degradation;
14. supported read-only observation.

Safety rejection precedes convenience routing. A mutation or authority claim
cannot be hidden behind a clarification, abstention, degradation, or handover
route.

## Operating modes

| Mode | Meaning |
|---|---|
| `read_only` | Exact supported intake; no successor authority |
| `hold` | User or authority clarification is required |
| `degraded_read_only` | Partial observation is recorded without readiness |
| `abstain` | The declared toolchain is unsupported |
| `handover` | The requested scope crosses an unowned boundary |
| `rejected` | A repair, replay, mutation, or authority violation was found |

`hold`, `degraded_read_only`, `abstain`, and `handover` are first-class result
surfaces. None is rewritten as success or generic failure.

## Receipt guarantees

Every post-preflight route receipt records:

- exact input digests;
- intent and repository identity;
- source and resulting commit equality;
- exact declared path accounting;
- disposition and operating mode;
- negative code-candidate and execution-lease predicates;
- negative repository-effect predicates;
- negative selection, execution, merge, deployment, and secret authorities;
- negative truth and correctness-proof inferences;
- a canonical receipt digest.

Only `intent_repository_observation_supported` sets
`codeai_profile_ready = true`. Readiness still grants no next-stage authority.

## Research provenance

The v0.1 boundaries are informed by recent primary research, without treating
any paper as repository authority:

- [SWE-INTERACT, arXiv:2606.30573](https://arxiv.org/abs/2606.30573) motivates
  versioned intent, explicit unresolved questions, and user handover.
- [DeepSWE, arXiv:2607.07946](https://arxiv.org/abs/2607.07946) motivates
  separating task provenance from verifier provenance.
- [The Verification Horizon, arXiv:2606.26300](https://arxiv.org/abs/2606.26300)
  motivates preserving `validation != correctness proof`.
- [SWE-Marathon, arXiv:2606.07682](https://arxiv.org/abs/2606.07682) motivates
  explicit anti-shortcut mutation and authority rejection.
- [SlopCodeBench, arXiv:2603.24755](https://arxiv.org/abs/2603.24755) motivates
  keeping long-run structural quality as a downstream obligation rather than a
  claim inferred from one baseline.
- [Scaling Test-Time Compute for Agentic Coding, arXiv:2604.16529](https://arxiv.org/abs/2604.16529)
  motivates keeping trajectory representation, selection, and reuse as later
  separate stages.

These sources are research provenance only. Publication, benchmark success,
or citation does not authorize a KuuOS state transition.

## Unowned boundaries

This version does not own:

- live repository collection;
- model prompting or inference;
- trajectory memory or candidate generation;
- patch construction or application;
- test generation;
- correctness adjudication;
- execution leases;
- Git branches, commits, pushes, or pull requests;
- merge, release, deployment, secrets, or production effects.

Any later stage requires a sibling adapter with an explicit source receipt,
authority source, bounded validity window, replay closure, and independent
validation.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_intent_repository_observation_envelope_v0_1.py` |
| Route checker | `scripts/check_codeai_intent_repository_observation_envelope_v0_1.py` |
| Unit test | `tests/test_kuuos_codeai_intent_repository_observation_envelope_v0_1.py` |
| Example | `examples/codeai_intent_repository_observation_envelope_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_intent_repository_observation_envelope_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/IntentRepositoryObservationEnvelopeV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIV0_1.lean` |
| Workflow | `.github/workflows/codeai-intent-repository-observation-envelope-v0-1.yml` |

## Validation

```bash
python3 -m py_compile \
  runtime/kuuos_codeai_intent_repository_observation_envelope_v0_1.py \
  scripts/check_codeai_intent_repository_observation_envelope_v0_1.py
python3 -m json.tool \
  examples/codeai_intent_repository_observation_envelope_v0_1.json
python3 -m json.tool \
  manifests/kuuos_codeai_intent_repository_observation_envelope_v0_1.json
PYTHONPATH=. python3 \
  scripts/check_codeai_intent_repository_observation_envelope_v0_1.py
PYTHONPATH=. python3 -m unittest \
  tests.test_kuuos_codeai_intent_repository_observation_envelope_v0_1
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAIV0_1
```

The dedicated formal root is registered independently. CodeAI v0.1 is not
implicitly imported into `KuuOSFormal` and is not registered in
`runtime/kuuos_current_check.py`.

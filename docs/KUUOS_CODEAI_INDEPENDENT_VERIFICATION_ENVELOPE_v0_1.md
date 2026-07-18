# KuuOS CodeAI Independent Verification Envelope v0.1

## Status

This document specifies an additive CodeAI profile adapter for recording
externally executed, independently reviewed verification evidence. It consumes
one supported Candidate Patch v0.1 receipt, one sealed evidence packet, and one
bounded verification policy.

The kernel does not run checks, apply the candidate, inspect a live repository,
issue a lease, select a candidate, or change Git state. It is not part of the
canonical current root or the repository formal aggregate.

## Preserved invariants

```text
candidate support != verification
verification evidence != truth
passed != correctness proof
failed != rejection or rollback authority
inconclusive != evidence deletion
verification receipt != candidate selection
verification receipt != execution lease
verification receipt != repository mutation
```

Every route preserves the exact source commit.

## Semantic difference from existing lines

- Candidate Patch v0.1 validates an externally supplied proposal. Independent
  Verification requires that exact supported receipt and does not regenerate,
  reopen, rank, or select the patch.
- VerifyOS v0.14 owns general independent evidence verification for its
  ObserveOS/WORLD lineage. This CodeAI surface adopts the same bounded-outcome
  discipline for a coding-profile receipt; it does not replace VerifyOS or
  claim its WORLD authority.
- External evidence may report execution in an isolated verifier. The CodeAI
  kernel itself performs no execution, tool invocation, repository effect, or
  external side effect.
- A passed result records bounded evidence satisfaction. It is not a theorem of
  correctness. A failed result records bounded falsification and does not
  authorize rejection, rollback, or deletion.

## Inputs

### Source candidate receipt

The exact Candidate Patch v0.1 receipt is accepted only when:

- its canonical digest is valid;
- its disposition is `candidate_patch_supported`;
- its mode is `proposal_only` and the candidate representation is ready;
- patch parsing and declared path accounting completed;
- source and resulting commits are equal;
- it records no generation, selection, lease, repository effect, Git effect,
  authority, truth, or correctness inference.

A hold, degraded, abstained, handed-over, repair, or rejected candidate receipt
cannot be promoted by this layer.

### Independent verification evidence

The sealed evidence packet binds:

- verification, verifier, reviewer, session, and nonce identities;
- exact source candidate receipt, candidate, patch artifact, repository, and
  source commit;
- evidence format, toolchain, environment, and verification protocol;
- exact check identifiers and passed/failed/skipped partitions;
- evidence artifact digests, finding labels, and outcome reasons;
- planned, completed, and successful reproduction attempts;
- falsification challenge and acceptance-criteria results;
- a declared `passed`, `failed`, or `inconclusive` outcome;
- bounded verification times and replay history;
- integrity, provenance, source-correspondence, and isolated-execution flags;
- negative kernel-execution, repository-mutation, authority, truth, and
  correctness-proof predicates;
- a canonical SHA-256 evidence digest.

The verifier and reviewer must be independent of the candidate producer when
required by policy. The reviewer can also be required to differ from the
verifier.

### Verification policy

The policy binds:

- expected predecessor receipt, candidate, repository, and source commit;
- allowed evidence formats, toolchains, and verifier identities;
- required check identifiers;
- minimum reproduction and successful-reproduction attempts;
- falsification and isolated-verification requirements;
- verifier/reviewer independence requirements;
- skipped-check and inconclusive-degradation rules;
- known and handover finding labels;
- evaluation epoch, evidence age, and verification duration bounds.

## Check and outcome semantics

The declared check set must be sorted, unique, and exactly partitioned into
passed, failed, and skipped sets. The declared count must equal the check set.

`passed` requires conclusive evidence, no failed or skipped checks, satisfied
acceptance criteria, and a passed executed falsification challenge.

`failed` requires conclusive evidence and at least one failed check, unsatisfied
acceptance criterion, or failed executed falsification challenge.

`inconclusive` requires non-conclusive evidence. It records an open verification
debt and requires reverification. Policy selects hold or degraded verification.

## Deterministic disposition order

After exact-field, type, and sealed-digest preflight, the kernel selects exactly
one route in this order:

1. source candidate receipt repair;
2. verification provenance repair;
3. verifier/reviewer independence repair;
4. candidate/repository correspondence repair;
5. evidence-integrity repair;
6. check-accounting repair;
7. verification-window repair;
8. replay rejection;
9. repository-mutation rejection;
10. authority or truth-escalation rejection;
11. unsupported verification-profile abstention;
12. mandatory-evidence hold;
13. verification-protocol repair;
14. outcome-consistency repair;
15. finding-ownership handover;
16. inconclusive hold when degradation is forbidden;
17. inconclusive degradation when degradation is allowed;
18. independent verification failed;
19. independent verification passed.

Mutation and authority rejection precede abstention, hold, handover,
degradation, pass, or fail.

## Operating modes

| Mode | Meaning |
|---|---|
| `verified_pass` | Bounded independent evidence passed |
| `verified_fail` | Bounded independent evidence failed |
| `hold` | Mandatory evidence or inconclusive-policy decision is pending |
| `degraded_verification` | Inconclusive evidence is retained with open debt |
| `abstain` | Evidence format, toolchain, or verifier is unsupported |
| `handover` | Findings cross the owned risk boundary |
| `rejected` | Repair, replay, mutation, or authority failure |

`failed` is a completed verification result, not a rejected envelope.
`inconclusive` is a completed bounded attempt with open debt, not failed
verification.

## Receipt guarantees

Every post-preflight receipt records:

- predecessor, candidate, patch, evidence, policy, repository, and commit
  bindings;
- exact check counts;
- disposition, operating mode, and recorded outcome;
- verification completion, debt, and reverification predicates;
- pass/fail flags without candidate-selection or rejection authority;
- whether external isolated verification was reported;
- negative kernel execution, candidate application, lease, repository, Git,
  merge, deployment, and secret effects;
- negative selection, verification, execution, merge, deployment, and secret
  authorities;
- negative truth, correctness-proof, and failure-rejection inferences;
- a canonical receipt digest.

## Research and standards provenance

- [DeepSWE, arXiv:2607.07946](https://arxiv.org/abs/2607.07946) informs
  separation of candidate producer, verifier, and reviewer provenance.
- [The Verification Horizon, arXiv:2606.26300](https://arxiv.org/abs/2606.26300)
  informs the boundary between bounded verification and correctness proof.
- [SWE-Marathon, arXiv:2606.07682](https://arxiv.org/abs/2606.07682) informs
  reproduction, falsification, and anti-shortcut checks.
- [SlopCodeBench, arXiv:2603.24755](https://arxiv.org/abs/2603.24755) informs
  explicit check coverage and structural-quality evidence.
- [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) informs governed
  testing, evaluation, verification, and validation activity.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) informs attributable source,
  verifier, artifact, session, and review provenance.

These sources justify design boundaries only. They grant no KuuOS authority.

## Unowned boundaries

This version does not own:

- general VerifyOS or WORLD verification lineage;
- test generation or test execution by the kernel;
- live repository or working-tree inspection;
- candidate generation, ranking, selection, acceptance, or rejection;
- correctness proof or generalized truth;
- execution leases, patch application, or rollback;
- Git index, object database, branch, commit, push, or pull request state;
- merge, release, deployment, secrets, or production effects.

Any later execution stage requires a sibling lease adapter with an exact source
receipt, explicit authority owner, validity window, replay closure, path and
effect bounds, revocation semantics, and a separate application receipt.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_independent_verification_envelope_v0_1.py` |
| Route checker | `scripts/check_codeai_independent_verification_envelope_v0_1.py` |
| Unit test | `tests/test_kuuos_codeai_independent_verification_envelope_v0_1.py` |
| Example | `examples/codeai_independent_verification_envelope_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_independent_verification_envelope_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/IndependentVerificationEnvelopeV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIIndependentVerificationV0_1.lean` |
| Workflow | `.github/workflows/codeai-independent-verification-envelope-v0-1.yml` |

## Validation

```bash
python3 -m py_compile \
  runtime/kuuos_codeai_independent_verification_envelope_v0_1.py \
  scripts/check_codeai_independent_verification_envelope_v0_1.py
python3 -m json.tool examples/codeai_independent_verification_envelope_v0_1.json
python3 -m json.tool manifests/kuuos_codeai_independent_verification_envelope_v0_1.json
PYTHONPATH=. python3 scripts/check_codeai_independent_verification_envelope_v0_1.py
PYTHONPATH=. python3 -m unittest \
  tests.test_kuuos_codeai_independent_verification_envelope_v0_1
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAIIndependentVerificationV0_1
```

The formal root is independent. This surface is not imported into `KuuOSFormal`
and is not registered in `runtime/kuuos_current_check.py`.

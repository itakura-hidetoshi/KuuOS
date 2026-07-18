# KuuOS CodeAI Candidate Patch Envelope v0.1

## Status

This document specifies an additive, proposal-only CodeAI adapter. It consumes
one supported CodeAI v0.1 intent/repository observation receipt, one externally
produced patch-candidate packet, the exact patch artifact, and a bounded policy.

The kernel does not inspect a live repository, generate or select a patch, run
tests, issue a lease, apply a patch, or change Git state. It is not registered
in the canonical current root and is not imported into the repository formal
aggregate.

## Preserved invariants

```text
source observation receipt != successor authority
candidate patch != selected patch
candidate patch != verified patch
candidate patch != applied patch
patch parsing != repository truth
policy support != correctness proof
proposal receipt != verification lease
proposal receipt != execution lease
proposal receipt != repository mutation
```

Every emitted route receipt preserves the source commit exactly.

## Semantic difference from existing lines

- CodeAI Intent / Repository Observation v0.1 owns read-only development
  context intake. Candidate Patch v0.1 requires its exact supported receipt and
  does not reopen repository observation.
- ObserveOS owns general source-bound observation. This layer consumes an
  already recorded receipt and does not collect observations.
- VerifyOS owns independent verification outcomes. Requirement traces and test
  plans are only candidate evidence identifiers here; no test is run and no
  correctness conclusion is made.
- Repository Commit Candidate v0.93 operates after a successful atomic
  application receipt and computes deterministic Git object candidates from a
  final repository snapshot. Candidate Patch v0.1 is an upstream,
  pre-application unified-diff intake. It does not construct blobs, trees,
  commits, or reference transitions and does not re-own v0.93.

## Inputs

### Source observation receipt

The exact 50-field CodeAI v0.1 receipt is accepted only when:

- its canonical digest is valid;
- its disposition is `intent_repository_observation_supported`;
- its mode is `read_only` and its profile is ready;
- its baseline and declared-path accounting are complete;
- its source and resulting commits are equal;
- it records no candidate, lease, repository effect, Git effect, authority,
  truth inference, or correctness inference.

A valid but non-supported predecessor receipt cannot be promoted by this layer.

### Patch candidate packet

The packet binds:

- candidate, revision, producer, and producer-session identities;
- the source observation receipt, intent, repository, and source commit;
- patch format, artifact digest, UTF-8 byte count, and declared path shape;
- added, modified, deleted, and rename path partitions;
- binary, submodule, and mode-change predicates;
- requirement-trace, test-plan, risk, and unresolved-question identifiers;
- creation epoch and prior candidate/session replay context;
- negative kernel-generation, patch-application, repository-effect, and
  authority-claim predicates;
- a canonical SHA-256 packet digest.

The candidate is supplied from outside the kernel. Recording it does not imply
that CodeAI generated it.

### Patch artifact

v0.1 parses one UTF-8 `unified_diff` string. It requires canonical repository
paths, explicit `diff --git a/... b/...` sections, one final newline, no NUL or
carriage return, and change evidence in every section.

The parser recognizes text hunks, additions, deletions, renames, binary
markers, submodule modes, and file-mode changes. It intentionally abstains from
other patch formats. Quoted Git path headers are not interpreted in v0.1.

Parsing proves correspondence between the supplied artifact and the declared
path shape. It does not prove that the patch applies to the live repository.

### Candidate policy

The policy binds:

- the expected predecessor receipt, repository, and source commit;
- allowed patch formats;
- patch-byte and changed-path budgets;
- allowed and forbidden path prefixes;
- deletion, rename, binary, submodule, and mode-change permissions;
- requirement-trace and test-plan obligations;
- whether missing evidence may degrade;
- known and handover risk labels;
- evaluation epoch and maximum candidate age.

## Deterministic disposition order

After exact-field, type, and sealed-digest preflight, the kernel selects exactly
one route in this order:

1. source observation receipt repair;
2. candidate provenance repair;
3. repository/source correspondence repair;
4. patch artifact repair;
5. candidate validity-window repair;
6. replay rejection;
7. repository-mutation rejection;
8. authority-escalation rejection;
9. unsupported patch-format abstention;
10. patch-syntax repair;
11. declared/parsed path-accounting repair;
12. path or patch-feature scope rejection;
13. patch budget rejection;
14. candidate-clarification hold;
15. risk-ownership handover;
16. required-evidence repair when degradation is forbidden;
17. candidate-evidence degradation when degradation is allowed;
18. supported proposal-only candidate.

Mutation and authority rejection precede abstention, hold, handover, or
degradation. A dangerous effect claim cannot be hidden behind a convenience
route.

## Operating modes

| Mode | Meaning |
|---|---|
| `proposal_only` | Exact supported intake; no selection or successor authority |
| `hold` | Candidate questions require clarification |
| `degraded_proposal` | Candidate is recorded with incomplete required evidence |
| `abstain` | The patch format is unsupported |
| `handover` | Risk classification crosses the owned boundary |
| `rejected` | Repair, replay, scope, budget, mutation, or authority failure |

`hold`, `degraded_proposal`, `abstain`, and `handover` remain distinct result
surfaces. None is collapsed into generic success or failure.

## Receipt guarantees

Every post-preflight route receipt records:

- the exact predecessor, candidate, policy, intent, repository, commit, and
  patch-artifact bindings;
- declared change-shape counts;
- disposition and operating mode;
- whether syntax parsing completed;
- proposal-only status;
- negative generation, selection, verification-lease, and execution-lease
  predicates;
- negative repository, Git, merge, deployment, and secret effects;
- negative selection, verification, execution, merge, deployment, and secret
  authorities;
- negative source-authority, correctness, and correctness-proof inferences;
- a canonical receipt digest.

Only `candidate_patch_supported` sets `candidate_patch_ready = true`. This
readiness means the candidate representation passed this intake policy. It
does not authorize another stage.

## Research provenance

The boundaries reuse the current CodeAI research provenance without treating a
paper or benchmark as repository authority:

- [SWE-INTERACT, arXiv:2606.30573](https://arxiv.org/abs/2606.30573) informs
  explicit clarification and handover outcomes.
- [DeepSWE, arXiv:2607.07946](https://arxiv.org/abs/2607.07946) informs the
  separation of producer, task, and verifier provenance.
- [The Verification Horizon, arXiv:2606.26300](https://arxiv.org/abs/2606.26300)
  informs `validation != correctness proof`.
- [SWE-Marathon, arXiv:2606.07682](https://arxiv.org/abs/2606.07682) informs
  explicit anti-shortcut effect and authority rejection.
- [SlopCodeBench, arXiv:2603.24755](https://arxiv.org/abs/2603.24755) informs
  requirement-trace and test-plan obligations without turning them into
  correctness claims.
- [Scaling Test-Time Compute for Agentic Coding, arXiv:2604.16529](https://arxiv.org/abs/2604.16529)
  informs separation of representation, selection, verification, and reuse.

Research provenance explains design choices only. It grants no KuuOS state
transition.

## Unowned boundaries

This version does not own:

- live repository or working-tree inspection;
- model prompting, inference, trajectory search, or patch generation;
- candidate ranking or selection;
- test generation, test execution, or correctness adjudication;
- verification or execution leases;
- patch application or rollback;
- Git index, object database, branch, commit, push, or pull request state;
- merge, release, deployment, secrets, or production effects;
- Repository Commit Candidate v0.93 or later repository-mutation surfaces.

A later verifier requires a sibling adapter with an exact candidate receipt,
independent evidence provenance, bounded validity, replay closure, and no
implicit execution or mutation authority.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_candidate_patch_envelope_v0_1.py` |
| Route checker | `scripts/check_codeai_candidate_patch_envelope_v0_1.py` |
| Unit test | `tests/test_kuuos_codeai_candidate_patch_envelope_v0_1.py` |
| Example | `examples/codeai_candidate_patch_envelope_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_candidate_patch_envelope_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/CandidatePatchEnvelopeV0_1.lean` |
| Formal root | `formal/KuuOSCodeAICandidatePatchV0_1.lean` |
| Workflow | `.github/workflows/codeai-candidate-patch-envelope-v0-1.yml` |

## Validation

```bash
python3 -m py_compile \
  runtime/kuuos_codeai_candidate_patch_envelope_v0_1.py \
  scripts/check_codeai_candidate_patch_envelope_v0_1.py
python3 -m json.tool examples/codeai_candidate_patch_envelope_v0_1.json
python3 -m json.tool manifests/kuuos_codeai_candidate_patch_envelope_v0_1.json
PYTHONPATH=. python3 scripts/check_codeai_candidate_patch_envelope_v0_1.py
PYTHONPATH=. python3 -m unittest \
  tests.test_kuuos_codeai_candidate_patch_envelope_v0_1
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAICandidatePatchV0_1
```

The formal root is registered independently. This surface is not implicitly
imported into `KuuOSFormal` and is not registered in
`runtime/kuuos_current_check.py`.

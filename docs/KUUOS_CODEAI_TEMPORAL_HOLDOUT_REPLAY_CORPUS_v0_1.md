# CodeAI Temporal Holdout Replay Corpus v0.1

## Purpose

This additive stage strengthens the external validity of CodeAI replay evaluation.
The prior comparative replay stage proved that one sealed three-case successor
fixture met eight explicit improvement targets. It intentionally did not claim
that the fixture was representative, random, unbiased, or predictive of future
repository work.

Temporal Holdout Replay Corpus v0.1 creates a content-addressed development and
holdout split before later optimization or admission stages consume performance
claims. It seals the split and its non-contamination guarantees. It does not run
CodeAI, reveal holdout labels to candidate generation, or grant any downstream
authority.

## Research basis

The design follows four recurring findings from software-agent evaluation work:

1. static benchmarks can become contaminated or overfit;
2. newer and temporally separated repository tasks better test generalization;
3. long, multi-file repository work requires evaluation beyond small synthetic
   examples;
4. test outcomes must be reported together with cost, failure stage, abstention,
   and repeated-error evidence.

The immediate design consequence is conservative: first seal a non-overlapping,
time-separated corpus; only afterward evaluate new context, verification,
memory, routing, or admission mechanisms against it.

## Exact boundary

```text
temporal holdout corpus sealing != replay execution
temporal split != representative-sample proof
holdout protection != correctness proof
corpus receipt != selection authority
corpus receipt != execution authority
corpus receipt != Git authority
corpus receipt != successor-stage authority
```

The kernel performs no historical code re-execution, provider invocation,
verification-runner invocation, repository mutation, Git effect, network access,
secret read, selection, repair, merge, deployment, or memory update.

## Entry model

Every replay entry binds:

- one case identifier;
- one issue digest;
- one source commit SHA;
- one observation epoch;
- one split: `development` or `holdout`;
- one bounded scenario class;
- one replay-case digest;
- one environment digest;
- one provider-configuration digest;
- one evaluation-protocol digest;
- five adaptation-use flags.

The six reference scenario classes are:

1. `verified_patch`;
2. `typecheck_failure`;
3. `overcorrection`;
4. `test_overfit`;
5. `abstention`;
6. `environment_failure`.

Scenario coverage is evidence about the committed reference corpus only. It is
not a claim of completeness or population representativeness.

## Temporal split

The reference corpus uses:

```text
development window: 70 .. 95
cutoff epoch:       100
holdout window:     105 .. 130
```

Development entries must remain at or before the cutoff. Holdout entries must
remain strictly after it. A malformed or inverted window blocks without evidence
or receipt.

The exact repository cutoff commit is:

```text
9df229a76ac2cd6ef2a33b503ee88008c3f8a864
```

## Cross-split non-overlap

The following intersections must be empty:

- development case IDs ∩ holdout case IDs;
- development issue digests ∩ holdout issue digests;
- development replay-case digests ∩ holdout replay-case digests.

The reference evidence records all three overlap counts as zero. Re-sealing a
modified entry cannot waive an overlap because the kernel recomputes the split
sets from the entries.

## Uniform evaluation binding

All entries must use the exact same:

- environment digest;
- provider-configuration digest;
- evaluation-protocol digest.

This does not assert that the chosen environment or model is ideal. It prevents
one split from silently receiving a different toolchain, provider configuration,
or evaluation protocol.

## Holdout protection

Every holdout entry must satisfy:

```text
labels_available_to_candidate_generation = false
used_for_threshold_tuning = false
used_for_memory_training = false
used_for_prompt_selection = false
used_for_model_selection = false
```

The corpus-level projection repeats the same guarantees and is independently
sealed. A single holdout violation blocks the whole corpus.

Development entries may be used by later bounded adaptation stages. That fact
does not authorize any such use; it only distinguishes development from frozen
holdout evidence.

## Outcomes

### Sealed

A valid corpus emits:

```text
status = ready
codeai_disposition = temporal_holdout_replay_corpus_sealed
```

The evidence contains split counts, scenario coverage, overlap counts, uniform
binding verification, holdout protection, and explicit no-effect/no-overclaim
fields.

### Blocked

The corpus blocks on malformed shape, missing or extra fields, invalid or stale
digests, unauthorized evaluator, stale request, temporal inversion, out-of-window
entry, insufficient split size, missing required scenario, split overlap,
uniform-binding mismatch, holdout exposure, adaptation leakage, or forbidden
authority.

Blocked output contains no evidence and no receipt.

## Reference corpus

The committed compact projection contains six entries in the full deterministic
fixture builder:

- three development cases;
- three holdout cases;
- six scenario classes;
- zero case-ID overlap;
- zero issue-digest overlap;
- zero replay-case-digest overlap.

The full entry objects are deterministically reconstructed by the fixture builder
rather than duplicated in the compact example.

## Formal surface

The generic Lean kernel defines:

- `ReplayEntry` and `Split`;
- `TemporallyOrdered`;
- `HoldoutProtected`;
- `CorpusValid`;
- extraction theorems for cutoff ordering and every holdout adaptation exclusion;
- `SplitDisjoint` for case, issue, and replay identities;
- a no-effect/no-overclaim `BoundaryPreserved` proposition.

The actual specialization proves by computation that the six-entry reference
corpus is temporally valid, split-disjoint, and boundary preserving.

## Surfaces

| Surface | Path |
|---|---|
| Runtime schema | `runtime/kuuos_codeai_temporal_holdout_replay_corpus_schema_v0_1.py` |
| Runtime checks | `runtime/kuuos_codeai_temporal_holdout_replay_corpus_checks_v0_1.py` |
| Runtime kernel | `runtime/kuuos_codeai_temporal_holdout_replay_corpus_v0_1.py` |
| Fixture builder | `scripts/build_codeai_temporal_holdout_replay_corpus_fixture_v0_1.py` |
| Fixture projection | `scripts/project_codeai_temporal_holdout_replay_corpus_fixture_v0_1.py` |
| Checker | `scripts/check_codeai_temporal_holdout_replay_corpus_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_temporal_holdout_replay_corpus_v0_1.py` |
| Example | `examples/codeai_temporal_holdout_replay_corpus_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_temporal_holdout_replay_corpus_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/TemporalHoldoutReplayCorpusV0_1.lean` |
| Formal root | `formal/KuuOSCodeAITemporalHoldoutReplayCorpusV0_1.lean` |
| Workflow | `.github/workflows/codeai-temporal-holdout-replay-corpus-v0-1.yml` |

## Validation

The dedicated workflow validates:

- Python compilation;
- JSON syntax;
- deterministic compact projection reconstruction;
- 26 dedicated positive, tamper, temporal, overlap, leakage, and authority tests;
- predecessor comparative replay tests;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.

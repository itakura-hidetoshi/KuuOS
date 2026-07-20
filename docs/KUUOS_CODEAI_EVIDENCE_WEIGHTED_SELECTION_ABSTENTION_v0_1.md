# CodeAI Evidence-Weighted Selection and Abstention v0.1

## Purpose

CodeAI Evidence-Weighted Selection and Abstention v0.1 is authoritative roadmap step 7.

It consumes:

- the exact Independent Test Strengthening plan;
- its exact route receipt;
- a sealed packet of externally executed independent test evidence;
- a sealed selection request;
- a deny-by-default selection policy.

It produces either:

- one evidence-bounded selected candidate; or
- an explicit abstention.

The surface ranks and records a selection decision. It does not execute tests, repair code, mutate a repository, create Git effects, or claim correctness.

## Authoritative roadmap

```text
1. Baseline and Replay Evaluation
2. Selective Repository Semantic Context Pack
3. Typed Structured Edit IR
4. Candidate Static Admissibility Preflight
5. Typed Error Classification
6. Independent Test Strengthening
7. Evidence-Weighted Selection and Abstention
8. Version-Bound Repair Memory
9. Maintainability Trajectory Gate
```

## Evidence packet

Every strengthened obligation must have exactly one sealed result containing:

- exact candidate and obligation identity;
- exact obligation digest;
- category and check kind;
- `passed`, `failed`, `inconclusive`, or `skipped`;
- an evidence artifact digest;
- independent runner and reviewer identities;
- completion, external execution, isolation, and source-correspondence flags;
- negative candidate-producer involvement, repository mutation, and Git effects.

The packet must preserve candidate and obligation order exactly.

The candidate producer, independent runner, and independent reviewer must be distinct.

## Eligibility

A candidate is eligible only when:

1. its source static classification is `admissible`;
2. every strengthened obligation has complete independent evidence;
3. every obligation outcome is `passed`;
4. all lineage, isolation, role-separation, and correspondence checks hold.

A higher raw score cannot override a non-admissible source classification.

```text
high evidence score + repairable/hold/rejected != eligible
```

## Deterministic evidence weights

The reference policy uses positive integer weights:

| Evidence category | Weight |
|---|---:|
| baseline | 10 |
| error-specific | 20 |
| novelty falsification | 25 |
| route-specific | 15 |
| error-free mutation probe | 30 |

Only passed obligations contribute weight.

Weights are deterministic governance values. They are not probabilities, confidence estimates, or correctness claims.

## Selection and abstention

Eligible scorecards are ordered by:

1. eligibility;
2. descending evidence score;
3. source candidate sequence;
4. candidate ID.

The surface selects only when:

- at least one eligible candidate exists;
- the top eligible score meets the minimum score;
- multiple eligible candidates are neither tied nor inside the minimum score margin.

Otherwise it abstains with one reason:

- `no_eligible_candidate`;
- `top_score_below_threshold`;
- `tied_top_score`;
- `insufficient_score_margin`.

Abstention is not rejection, deletion, rollback, or repair authority.

## Reference fixture

The reference fixture preserves four candidates and all 22 strengthened obligations.

All externally reported obligations pass, but only `candidate-admissible` is eligible. The other candidates have higher raw evidence totals because they carry more obligations, yet their source classifications remain repairable, hold, or rejected.

The deterministic result is:

```text
decision = selected
selected_candidate_id = candidate-admissible
selected_evidence_score = 60
eligible_candidate_count = 1
```

This demonstrates that evidence weighting cannot erase the admissibility gate.

## Fixed boundaries

```text
planned obligation != executed evidence
external passed evidence != correctness proof
evidence weight != probability
raw score != eligibility
high score != admissibility
selection != verification authority
selection != repair authority
selection != execution authority
selection != repository mutation
selection != Git authority
abstention != rejection
selected candidate != safe-to-merge theorem
```

## Formal surface

The generic Lean layer proves:

- non-admissible candidates cannot become eligible through high scores;
- failed or incomplete evidence cannot satisfy eligibility;
- every selected candidate is eligible and preserved in the scorecard set;
- scores are neither probabilities nor correctness proofs;
- abstention is not rejection;
- external evidence consumption is separate from kernel test execution;
- verification, repair, execution, and Git authority remain separate;
- ranking and selection perform no repair, repository, or Git effect.

## Fail-closed conditions

The surface blocks on, among other cases:

- malformed or unsealed inputs;
- request, policy, plan, receipt, evidence-packet, or evidence-record digest mismatch;
- repository, commit, plan, receipt, candidate, obligation, category, or check-kind mismatch;
- stale or future request or evidence;
- incomplete evidence coverage;
- duplicate or reordered candidate evidence;
- runner, reviewer, or producer identity collision;
- missing independent execution, review, isolation, or source correspondence;
- candidate-producer involvement;
- repository mutation or Git effects in evidence;
- disabled eligibility or evidence guarantees;
- enabled test execution, repair, repository, execution, or Git authority;
- candidate or evidence-record budget excess;
- invalid or non-positive category weights.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py` |
| Checks | `runtime/kuuos_codeai_evidence_weighted_selection_abstention_checks_v0_1.py` |
| Schema | `runtime/kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1.py` |
| Fixture builder | `scripts/build_codeai_evidence_weighted_selection_abstention_fixture_v0_1.py` |
| Checker | `scripts/check_codeai_evidence_weighted_selection_abstention_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py` |
| Example | `examples/codeai_evidence_weighted_selection_abstention_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_evidence_weighted_selection_abstention_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIEvidenceWeightedSelectionAbstentionV0_1.lean` |
| Workflow | `.github/workflows/codeai-evidence-weighted-selection-abstention-v0-1.yml` |

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic reconstruction;
- dedicated fail-closed, selection, and abstention tests;
- Independent Test Strengthening and predecessor regressions;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.

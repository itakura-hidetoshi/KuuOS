# CodeAI Evidence-Grounded Candidate Ranking v0.1

## Purpose

CodeAI Evidence-Grounded Candidate Ranking v0.1 is the deterministic ordering boundary immediately after Evidence-Bearing Candidate Portfolio and before candidate selection, isolated application, independent verification, repair, execution, or Git lifecycle effects.

It consumes the exact sealed evidence portfolio and route receipt, verifies their lineage and accounting, preserves every candidate's original classification and findings, and emits one reproducible ranking plus a content-addressed route receipt.

The surface ranks evidence. It does not select a candidate and does not claim that a higher position is more correct.

## Pipeline position

```text
Intent Repository Observation
→ Selective Repository Semantic Context Pack
→ Typed Structured Edit IR
→ Candidate Static Admissibility Preflight
→ Evidence-Bearing Candidate Portfolio
→ Evidence-Grounded Candidate Ranking
→ Candidate Selection
→ Isolated Application
→ Independent Verification
→ Bounded Repair
→ Git Lifecycle
```

## Inputs

The builder receives four sealed values.

### Source evidence portfolio

The source portfolio must be the exact output of CodeAI Evidence-Bearing Candidate Portfolio v0.1. It must preserve:

- repository, source commit, and source snapshot identity;
- candidate sequence and candidate IDs;
- four-way static-preflight classification;
- typed-IR, report, and receipt digests;
- operation count and changed paths;
- complete finding evidence and finding counts;
- explicit no-ranking, no-selection, no-verification, no-repair, no-execution, and no-Git boundaries.

### Source route receipt

The route receipt must point to the exact source portfolio digest and agree on identity, candidate accounting, classification accounting, finding accounting, and changed-path accounting.

### Ranking request

The request fixes:

- ranking identity and revision;
- exact source portfolio and receipt digests;
- repository, source commit, and source snapshot identity;
- ranking purpose;
- request epoch;
- unresolved questions;
- an explicit no-selection-authority claim.

### Deny-by-default ranking policy

The policy fixes:

- exact source lineage;
- evaluation window;
- candidate, finding, and changed-path budgets;
- classification priority;
- ranking strategy;
- exact-lineage, evidence-preservation, and stable-tie-break requirements;
- all selection, verification, repair, repository mutation, execution, and Git authority switches as false.

## Deterministic ranking key

The ranking strategy is `classification_then_evidence_burden`.

Candidates are ordered lexicographically by:

1. classification priority;
2. reject finding count;
3. hold finding count;
4. repairable finding count;
5. total finding count;
6. operation count;
7. changed-path count;
8. original candidate sequence;
9. candidate ID.

Lower tuple values appear earlier.

The classification priority is fixed:

| Priority | Classification |
|---:|---|
| 0 | `candidate_static_admissibility_confirmed` |
| 1 | `candidate_static_preflight_repair_required` |
| 2 | `candidate_static_preflight_held` |
| 3 | `candidate_static_preflight_rejected` |

This priority is a routing convention, not a probability of correctness.

## Ranked candidate record

Each ranked record contains:

- contiguous one-based ranking position;
- candidate ID and original sequence;
- original classification and evidence route;
- classification priority;
- explicit evidence-burden components;
- complete ranking key;
- an exact deep copy of the source candidate evidence;
- explicit false values for selection, verification, repair, mutation, execution, and Git effects.

The original source candidate is not rewritten or reinterpreted.

## Accounting

The output preserves:

- candidate count;
- classification counts;
- total finding count;
- union changed-path count.

The ranking positions form a contiguous list of length equal to the candidate count. The generic Lean theorem proves this length identity independently of the concrete runtime. Concrete theorems then specialize the boundary to the committed four-candidate KuuOS example.

## Fail-closed conditions

The builder blocks on, among other cases:

- malformed or unsealed source portfolio or receipt;
- source portfolio and receipt digest mismatch;
- stale or future request;
- unresolved ranking questions;
- a request claiming selection authority;
- enabled selection, verification, repair, mutation, execution, or Git authority;
- disabled exact-lineage, evidence-preservation, or stable-tie-break requirements;
- repository, source commit, or source snapshot mismatch;
- candidate, finding, or changed-path budget excess;
- source candidate sequence or classification inconsistency;
- source finding counts inconsistent with findings;
- source accounting inconsistent with candidate evidence;
- altered classification priority or ranking strategy.

## Fixed boundaries

```text
evidence portfolio != ranking correctness proof
classification priority != correctness probability
ranking != candidate selection
ranking position one != selected candidate
repairable ranking != automatic repair
hold ranking != rejection
rejected ranking != repository deletion
ranking receipt != provider authority
ranking receipt != selection authority
ranking receipt != verification authority
ranking receipt != repair authority
ranking receipt != execution authority
ranking receipt != Git authority
```

## Effect boundary

This surface performs no:

- provider or LLM invocation;
- candidate selection;
- patch application;
- verification runner invocation;
- repair execution;
- repository mutation;
- network or secret access;
- branch, commit, push, pull-request, merge, or deployment effect;
- execution or Git authority grant.

Its only active transformation is deterministic ordering of already-sealed evidence records.

## Machine-readable example

`examples/codeai_evidence_grounded_candidate_ranking_v0_1.json` defines one candidate in each static-preflight classification. The fixture builder executes the exact predecessor preflight and portfolio implementations before constructing the ranking request and policy.

The integration checker requires:

- deterministic repeated output;
- the expected four-way order;
- contiguous positions;
- exact source-candidate evidence preservation;
- unchanged classification, finding, and changed-path accounting;
- no selection or downstream authority.

## Runtime surfaces

- `runtime/kuuos_codeai_evidence_grounded_candidate_ranking_schema_v0_1.py`
- `runtime/kuuos_codeai_evidence_grounded_candidate_ranking_checks_v0_1.py`
- `runtime/kuuos_codeai_evidence_grounded_candidate_ranking_v0_1.py`

## Formal surfaces

- `formal/KUOS/CodeAI/EvidenceGroundedCandidateRankingV0_1.lean`
- `formal/KuuOSCodeAIEvidenceGroundedCandidateRankingV0_1.lean`

## Validation

The dedicated workflow validates:

- Python syntax;
- canonical example and manifest JSON;
- deterministic integration checker;
- 42 dedicated fail-closed tests;
- evidence-portfolio and static-preflight regressions;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.

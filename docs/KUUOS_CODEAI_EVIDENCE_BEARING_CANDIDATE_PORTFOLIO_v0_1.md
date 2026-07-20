# CodeAI Evidence-Bearing Candidate Portfolio v0.1

## Purpose

CodeAI Evidence-Bearing Candidate Portfolio v0.1 is the deterministic boundary immediately after Candidate Static Admissibility Preflight and before ranking, selection, isolated application, independent verification, repair, execution, or Git lifecycle effects.

It accepts sealed static-preflight reports and their sealed route receipts, verifies exact lineage, preserves each candidate's classification and finding evidence, and emits a normalized portfolio plus a route receipt.

This surface does not make a candidate better. It makes the evidence attached to each candidate explicit, comparable, and difficult to confuse.

## Pipeline position

```text
Intent Repository Observation
→ Selective Repository Semantic Context Pack
→ Typed Structured Edit IR
→ Candidate Static Admissibility Preflight
→ Evidence-Bearing Candidate Portfolio
→ Ranking and Selection
→ Isolated Application
→ Independent Verification
→ Bounded Repair
→ Git Lifecycle
```

## Inputs

The builder receives three sealed surfaces.

### Portfolio request

The request fixes:

- portfolio identity and revision;
- repository full name;
- exact source commit SHA;
- exact source repository snapshot digest;
- ordered candidate IDs;
- expected typed IR digest for every candidate;
- expected static-preflight report digest for every candidate;
- expected preflight route-receipt digest for every candidate;
- request epoch;
- unresolved questions;
- an explicit no-authority claim.

Candidate sequence values must be contiguous and unique. Candidate IDs must be unique.

### Deny-by-default policy

The policy fixes:

- expected repository, source commit, and source snapshot;
- evaluation window;
- candidate, finding, and changed-path budgets;
- exact-lineage requirement;
- classification-preservation requirement;
- finding-evidence-preservation requirement;
- all authority switches as false.

The builder blocks if ranking, selection, verification, repair, execution, or Git authority is enabled.

### Candidate preflight bundles

Each bundle contains:

- candidate ID;
- exact static-admissibility report;
- exact static-admissibility route receipt.

The report and receipt must retain their original digests and must correspond on:

- typed IR digest;
- typed IR receipt digest;
- repository identity;
- source commit;
- source snapshot digest;
- result snapshot digest;
- operation count;
- changed paths;
- finding counts;
- classification and one-hot classification flags.

## Deterministic normalization

Candidates are normalized in the request's explicit candidate sequence, not by score and not by classification.

For each candidate the portfolio preserves:

- candidate ID and sequence;
- four-way static-preflight classification;
- evidence route;
- typed IR digest;
- typed IR receipt digest;
- static-preflight report digest;
- preflight route-receipt digest;
- source and result snapshot lineage;
- operation count;
- changed paths;
- finding counts;
- full finding evidence.

The four evidence routes are:

| Static-preflight classification | Portfolio evidence route |
|---|---|
| `candidate_static_admissibility_confirmed` | `admissible_evidence_route` |
| `candidate_static_preflight_repair_required` | `repairable_evidence_route` |
| `candidate_static_preflight_held` | `hold_evidence_route` |
| `candidate_static_preflight_rejected` | `rejected_evidence_route` |

A route is not a rank, selection, repair instruction, verification result, execution lease, or Git instruction.

## Classification accounting

The normalized portfolio reports disjoint counts for:

- admissible;
- repairable;
- hold;
- rejected.

Every candidate belongs to exactly one classification. The Lean formalization proves the generic partition identity:

```text
admissible_count
+ repairable_count
+ hold_count
+ rejected_count
= total_candidate_count
```

This theorem is independent of the concrete Python runtime.

## Finding evidence

Finding evidence is copied exactly from the sealed static-preflight report.

The portfolio does not:

- suppress findings;
- promote or demote severity;
- merge hold with reject;
- convert repairable into repaired;
- reinterpret admissible as selected;
- claim that a report proves correctness.

The aggregate total-finding count is derived from the preserved candidate evidence.

## Fail-closed conditions

The builder blocks on, among other cases:

- malformed request, policy, report, or receipt;
- digest mismatch;
- duplicate candidate ID;
- non-contiguous candidate sequence;
- request and bundle candidate-set mismatch;
- stale request;
- unresolved portfolio questions;
- authority claim;
- enabled ranking, selection, verification, repair, execution, or Git authority;
- repository, source commit, or source snapshot mismatch;
- typed IR lineage mismatch;
- report and receipt mismatch;
- classification flags inconsistent with classification;
- finding counts inconsistent with findings;
- candidate, finding, or changed-path budget excess.

## Fixed boundaries

The following distinctions are normative:

```text
provider output != preflight evidence
preflight classification != ranking
admissible != selected
repairable != automatically repaired
hold != rejection
rejected != repository deletion
portfolio normalization != correctness proof
portfolio receipt != provider authority
portfolio receipt != ranking authority
portfolio receipt != selection authority
portfolio receipt != verification authority
portfolio receipt != repair authority
portfolio receipt != execution authority
portfolio receipt != Git authority
```

## Effect boundary

This surface performs no:

- provider or LLM invocation;
- ranking;
- candidate selection;
- verification runner invocation;
- repair execution;
- repository mutation;
- network or secret access;
- execution authority grant;
- Git authority grant;
- merge or deployment authority grant.

Its output is evidence normalization only.

## Machine-readable example

`examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json` contains one candidate in each of the four classifications. The integration checker rebuilds the portfolio and route receipt and requires exact equality with the committed expected artifacts.

## Runtime surfaces

- `runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1.py`
- `runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_checks_v0_1.py`
- `runtime/kuuos_codeai_evidence_bearing_candidate_portfolio_v0_1.py`

## Formal surface

- `formal/KUOS/CodeAI/EvidenceBearingCandidatePortfolioV0_1.lean`
- `formal/KuuOSCodeAIEvidenceBearingCandidatePortfolioV0_1.lean`

The formal surface proves generic four-way accounting and the concrete no-ranking, no-selection, no-verification, no-repair, no-repository-mutation, no-execution-authority, and no-Git-authority boundaries.

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic integration checker;
- dedicated fail-closed unit tests;
- static-preflight regression;
- typed IR regression;
- semantic-context regression;
- structured-synthesis regression;
- generated-patch baseline regression;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.

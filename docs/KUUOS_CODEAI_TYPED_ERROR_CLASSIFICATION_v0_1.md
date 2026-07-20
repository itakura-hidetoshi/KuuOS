# CodeAI Typed Error Classification v0.1

## Purpose

CodeAI Typed Error Classification v0.1 is the deterministic boundary after Candidate Static Admissibility Preflight and Evidence-Bearing Candidate Portfolio.

It converts preserved static-preflight findings into typed error records while retaining exact lineage to:

- the source repository and commit;
- the evidence-bearing portfolio and route receipt;
- the original preflight finding evidence;
- the historical Generated Patch Error Baseline Replay evidence and receipt.

The classifier does not infer a hidden cause. It normalizes observed evidence into a stable taxonomy.

## Roadmap position

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

## Pipeline position

```text
Typed Structured Edit IR
→ Candidate Static Admissibility Preflight
→ Evidence-Bearing Candidate Portfolio
→ Typed Error Classification
→ Independent Test Strengthening
→ Evidence-Weighted Selection and Abstention
```

## Inputs

The classifier consumes six sealed inputs.

### Source evidence portfolio

The exact Evidence-Bearing Candidate Portfolio contains:

- candidate identity and explicit sequence;
- preserved four-way static classification;
- full preflight findings;
- typed-IR and source-snapshot lineage;
- preflight report and route-receipt digests.

The corresponding portfolio receipt must match the exact portfolio digest and continue to deny ranking, selection, verification, repair, execution, and Git authority.

### Baseline replay evidence

The exact Generated Patch Error Baseline Replay Evaluation contributes only historical fingerprint counts.

The baseline is read-only evidence. Its frequency is not interpreted as:

- probability of correctness;
- probability of repair success;
- candidate quality;
- ranking weight;
- selection authority.

### Classification request

The request seals:

- classification identity and revision;
- repository and source commit;
- exact portfolio and portfolio-receipt digests;
- exact baseline evidence and baseline-receipt digests;
- request epoch;
- unresolved questions;
- an explicit no-authority claim.

### Deny-by-default policy

The policy requires:

- exact lineage;
- complete taxonomy coverage for every observed finding code;
- exact finding-evidence preservation;
- candidate and typed-error budgets;
- all ranking, selection, verification, repair, repository mutation, execution, and Git switches to remain false.

## Typed error record

Each source finding is normalized into one typed record containing:

- candidate ID and sequence;
- error sequence within the candidate;
- exact original finding mapping;
- source finding code;
- error family;
- error stage;
- source severity;
- descriptive repair route;
- stable uppercase fingerprint;
- occurrence count in the historical baseline;
- baseline novelty status;
- an independently sealed typed-error digest.

## Error families

| Family | Meaning |
|---|---|
| `operation_conflict` | Typed operations overlap or conflict before deterministic materialization. |
| `materialization` | The current IR cannot be applied to the exact source snapshot as stated. |
| `syntax` | Materialized Python or Lean text fails the available static syntax or lexical check. |
| `dependency` | Internal dependency correspondence is unresolved or external dependency evidence is absent. |
| `testing` | Required test-plan identity or changed-path coverage is missing. |
| `policy_marker` | New text contains a deny-listed marker such as `sorry`, `admit`, or `TODO`. |
| `semantic_noop` | An operation has no material effect on the candidate snapshot. |

Unknown finding codes are not guessed. With complete-taxonomy policy enabled, they block fail-closed.

## Error stages

The stage dimension remains separate from family:

- `typed_operation`;
- `materialization`;
- `parse`;
- `dependency_correspondence`;
- `test_plan_correspondence`;
- `policy_marker`;
- `material_effect`.

## Repair routes

The source severity maps deterministically to a descriptive route:

| Static severity | Typed repair route |
|---|---|
| `repairable` | `local_candidate_repair` |
| `hold` | `external_evidence_required` |
| `reject` | `current_ir_unmaterializable` |

A repair route is not permission to repair. It identifies the kind of evidence or candidate change required before a later authority-bearing stage may act.

## Historical baseline relationship

The classifier derives an uppercase fingerprint from the source finding code and looks it up in the sealed baseline metrics.

The result is one of:

- `known_in_replay_baseline`;
- `novel_to_replay_baseline`.

The occurrence count is preserved exactly. No smoothing, probability estimate, confidence score, ranking score, or automatic policy adjustment is performed.

## Candidate-level output

Every source candidate remains present, including candidates with no static findings.

Each candidate record contains:

- source classification;
- source candidate digest;
- source finding count;
- typed error count;
- ordered typed errors;
- `no_static_error_observed`;
- proof-by-equality that source finding evidence was preserved;
- explicit false fields for selection, verification, and repair execution.

`no_static_error_observed` does not mean correct, verified, safe to merge, or selected.

## Aggregate output

The sealed classification contains exact counts by:

- error family;
- error stage;
- repair route;
- source severity;
- baseline novelty.

The total typed-error count must equal the source portfolio's total finding count.

## Fail-closed conditions

The classifier blocks on, among other cases:

- malformed input;
- request, policy, portfolio, receipt, baseline, metrics, or receipt digest mismatch;
- repository or source-commit lineage mismatch;
- portfolio or baseline receipt correspondence mismatch;
- stale or future request;
- unresolved classification questions;
- authority claim;
- enabled downstream effect or authority;
- missing exact-lineage, complete-taxonomy, or finding-preservation requirement;
- candidate or typed-error budget excess;
- unknown finding code;
- source-finding accounting mismatch;
- source portfolio already containing ranking, selection, verification, repair, repository, execution, or Git effects.

## Fixed boundaries

```text
preflight finding != proven root cause
typed error class != correctness proof
historical frequency != probability
repair route != repair authority
typed error classification != ranking
typed error classification != candidate selection
zero static error != correctness proof
classification receipt != verification authority
classification receipt != execution authority
classification receipt != Git authority
```

## Effect boundary

This surface performs no:

- provider or LLM invocation;
- code generation;
- candidate ranking;
- candidate selection;
- verification runner invocation;
- repair execution;
- repository mutation;
- network or secret access;
- execution lease issuance;
- Git operation;
- merge or deployment authorization.

## Formal surface

- `formal/KUOS/CodeAI/TypedErrorClassificationV0_1.lean`
- `formal/KuuOSCodeAITypedErrorClassificationV0_1.lean`

The generic Lean layer proves:

- severity-to-route injectivity;
- exact three-way repair-route accounting;
- repair route does not grant repair authority;
- classification does not rank or select;
- historical frequency is not treated as probability;
- verification, execution, and Git authority remain separate;
- evidence preservation does not prove root cause.

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic integration reconstruction;
- dedicated fail-closed tests;
- Evidence-Bearing Candidate Portfolio regression;
- Candidate Static Admissibility Preflight regression;
- Generated Patch Error Baseline Replay regression;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.

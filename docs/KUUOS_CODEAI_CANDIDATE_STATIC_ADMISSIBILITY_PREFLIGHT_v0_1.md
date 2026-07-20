# CodeAI Candidate Static Admissibility Preflight v0.1

## Status

Additive, deterministic, read-only and effect-free preflight after **CodeAI Typed Structured Edit IR v0.1**.

The surface consumes one exact typed-edit IR and receipt, the exact source repository snapshot, a sealed preflight request and policy, a dependency inventory, and a test-plan catalog. It materializes the typed operations only in memory and emits a content-addressed report and route receipt.

It does not invoke a model or verifier, write a repository, select a candidate, issue an execution lease, or perform a Git effect.

```text
exact typed IR and receipt
+ exact source snapshot
+ sealed preflight request and policy
+ dependency inventory
+ test-plan catalog
  -> lineage and budget checks
  -> collision analysis
  -> effect-free in-memory materialization
  -> Python / Lean static checks
  -> dependency and test-plan correspondence
  -> ADMISSIBLE | REPAIRABLE | HOLD | REJECT
  -> sealed report and receipt
```

## Why this stage exists

A symbol-anchored edit may have correct source digests and still be unsuitable for expensive verification. Examples include overlapping operations, malformed materialized code, unresolved internal imports, undeclared external dependencies, missing test coverage, or a no-op replacement.

The preflight moves those inexpensive and deterministic checks before candidate selection and independent verification. It does not claim semantic correctness. It only determines whether the normalized edit is statically suitable for the next governed stage.

## Pipeline position

```text
Intent Repository Observation
  -> Selective Repository Semantic Context Pack
  -> Typed Structured Edit IR
  -> Candidate Static Admissibility Preflight
  -> Evidence-Bearing Candidate Portfolio
  -> Isolated Application and Independent Verification
  -> Bounded Repair
```

The v0.1 surface is independently invoked. Existing selection and verification surfaces are not silently rewired.

## Inputs and lineage

The preflight requires exact correspondence among:

- typed IR digest;
- typed IR receipt digest;
- repository name and source commit;
- canonical source snapshot digest;
- dependency-inventory digest;
- test-plan-catalog digest;
- operation count, identifiers, target paths and application order;
- request creation window and deny-by-default policy.

Any mismatch blocks the surface before materialization. Unresolved preflight questions or an authority claim also block it.

## Static checks

### Operation collision

Operations are grouped by path. Replacement and deletion ranges may not overlap. Insertions at the same boundary, or immediately intersecting a replacement range, are rejected. A create-file operation may not share its target path with another operation.

Collision is classified as `reject` because deterministic materialization would otherwise depend on ambiguous operation interaction.

### In-memory materialization

Operations are applied to a copied mapping:

```text
repository path -> complete UTF-8 content
```

The source mapping remains unchanged. Existing-file operations require the exact source-file digest recorded in the typed IR. Create-file operations require path absence. Result content must remain canonical UTF-8 text with normalized newlines.

The resulting mapping is ephemeral evidence only:

```text
materialized snapshot != repository mutation
```

### Python profile

Changed Python files are parsed with the standard-library AST. The preflight checks:

- syntax;
- relative and repository-internal import resolution;
- undeclared external modules;
- standard-library imports;
- explicit dependency inventory and policy allowances.

Syntax and unresolved internal imports are `repairable`. An external module not present in either the sealed inventory or policy is `hold`, because accepting a new dependency requires separate authority.

### Lean profile

Changed Lean files receive a bounded lexical preflight:

- bracket and delimiter balance outside strings and line comments;
- duplicate top-level declaration names;
- repository-internal import correspondence;
- external import-prefix inventory and policy correspondence.

This is not Lean elaboration and is not treated as type correctness. Strict Lean compilation remains a later verification step.

### Test-plan correspondence

The union of request-, IR- and operation-level test-plan identifiers must resolve in the sealed catalog. Every changed path must be covered by at least one referenced plan whose language and path prefix correspond.

Catalog presence does not mean the test ran or passed:

```text
test-plan correspondence != test success
```

### Additional findings

The v0.1 surface also records:

- forbidden new-text markers such as `TODO`, `sorry` or `admit` under the supplied policy;
- operations with no material effect;
- changed-path, operation, source-snapshot, result-snapshot and finding-count budgets.

## Four classifications

Severity dominance is deterministic:

```text
reject > hold > repairable > admissible
```

### ADMISSIBLE

No findings were recorded. The candidate may enter an evidence-bearing portfolio, but is not selected and has no execution authority.

### REPAIRABLE

The edit has a localized defect that can be returned to bounded repair, such as syntax failure, unresolved internal import, missing test-plan coverage, forbidden marker or no-op edit.

### HOLD

The edit requires authority or evidence that the preflight cannot supply, such as an unaccounted external dependency.

### REJECT

The edit cannot be deterministically and safely materialized under the current IR, such as overlapping operations or path conflicts.

## Report

The sealed report records:

- all input lineage digests;
- source and result snapshot digests and sizes;
- operation and changed-path accounting;
- normalized findings and counts;
- the four-way disposition;
- completed check flags;
- explicit no-effect and no-authority fields.

The route receipt repeats the minimal downstream lineage and classification without forwarding the materialized repository snapshot.

## Formal invariants

The generic Lean kernel proves that admissibility is equivalent to zero repairable, hold and reject findings. The concrete KuuOS decision model additionally fixes:

- exact classification correspondence;
- completed lineage, collision, materialization, parse, dependency and test-plan checks;
- ephemeral result materialization;
- no repository mutation;
- no candidate selection;
- no execution authority;
- no treatment of preflight evidence as a correctness proof.

The generic theorem is implemented before specializing it to the concrete CodeAI receipt.

## Fixed boundaries

```text
typed IR != materialized repository
static preflight != correctness proof
parse success != type correctness
dependency correspondence != runtime success
test-plan correspondence != test success
materialized snapshot != repository mutation
admissible != selected
repairable != automatically repaired
hold != rejection
rejected != repository deletion
preflight receipt != provider authority
preflight receipt != verification authority
preflight receipt != execution authority
preflight receipt != Git authority
```

## Validation

The dedicated workflow checks:

- Python syntax for the three runtime modules, checker and tests;
- canonical JSON example and manifest;
- deterministic example/report/receipt reproduction;
- 36 fail-closed tests plus typed-IR, context, synthesis and baseline-replay regressions;
- canonical `lake-manifest.json`;
- strict compilation of the new formal root;
- strict compilation of the full `KuuOSFormal` baseline.

## Planned successor

**CodeAI Evidence-Bearing Candidate Portfolio v0.1** will consume exact preflight reports and retain the classification and evidence lineage before any candidate-selection decision.

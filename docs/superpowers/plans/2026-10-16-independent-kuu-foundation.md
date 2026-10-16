# Independent Kuu Foundation Implementation Plan

Goal: replace the current build and design, not add a nominally Kuu wrapper around a historical evaluator.
Architecture: boundary graph -> declared relation -> universal quotient -> strict comparison and context diagram.
Tech stack: pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6, Python standard library.
Spec: ../specs/2026-10-16-independent-kuu-foundation-design.md

## Constraints
No current import of KUOS or old F51/F77/Gray semantics. No new axioms or proof shortcuts. A two-dimensional calculus is not a proof-relevant global strict 3-category. Preserve historical source trees, configuration and licensing.

## Implemented integration work
- Independent presentation quotient, strict comparison and incidence modules; replace the standard entry and Lake roots.
- Preserve exact historical formal tree and fixed inputs as a separate legacy package.
- Migrate 194 existing workflow/validator/manifest files and two runtime connections; fixed 196-consumer read-only migration verifier.
- Explicit package scopes for all 18 recorded historical repository contracts, including the ten read-only v0.86–v0.95 contracts. Do not grant them auto-repair permissions.
- Reject direct, transitive and unreferenced current-module imports of legacy code. Prevent automated reintroduction of historical roots.
- Register all 48 boundary/configuration regressions with CI. Configure warningAsError on the actual Lake library, not only through an unused configuration key.
- Remove the temporary Git-object publishing workflow. No source archive is generated or delivered.
- Rewrite current README/ROADMAP, retain the historical originals, and separate integration success from unproved higher-dimensional claims.

## Evidence and acceptance
The exact fe9d720a36025a9fc259b70bf43b9f33b45891f2 independent run 38827903551 passed the then-current 45 tests and 644 Lean build jobs. The v0.86–v0.95 scope regression first failed for ten missing fields, then passed with the subsystem tests (324 local tests). The actual Lean option regression also failed before the library setting was added and passed afterward.

Merge acceptance is the new exact-source-head Lean, static, runtime, selected regression, required gate and completion evidence. Do not equate prior-head success with current-head success; inspect the final GitHub status before merging and reobserve main afterward.

## Separate mathematical continuation
Proof-relevant global strict 3-cell syntax, all original F112 raw-source ports and the complete genuine C60 incidence reconstruction remain mathematical obligations, not missing CI switches. Prove them from the new foundation without importing Gray semantics back into it.

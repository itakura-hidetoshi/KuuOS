# Restore public proofs without restoring Gray as Kuu's foundation

The user explicitly requests full correction of v5.292's blanket removal of the previous public Lean roots. This supersedes the blanket namespace/root exclusion in the 2026-10-16 migration design and AGENTS.md. It does NOT permit making Gray, F51/F77 evaluators, or historical phase reconstruction prerequisites of the independent Kuu foundation.

## Success criteria

- Account for every root in the exact retained pre-migration Lake configuration; do not use the approximate count 120 as a hard-coded inventory.
- Restore existing public proof APIs and actual current build coverage, not merely documentation or archival copies.
- Preserve theorem source/namespace/statement/proof identity wherever no change is needed. Preserve the frozen v5.291 snapshot and Lean/mathlib pins.
- Separate independent Kuu core, retained non-Gray mathematics, and Gray-specific comparison dependencies by real transitive imports. A KUOS prefix alone is not evidence of Gray dependence.
- Keep Gray-specific sources reproducible and explicitly scoped, never silently import them into Kuu core or declare old and new source types equal.
- Update standard build, root protection, CI selection, and live documentation consistently. Add positive restoration and negative contamination regressions.
- Do not merge PR #2339 or #1558 as part of this repair; work on a separate branch and verify its exact HEAD.

## Implementation boundary

Read the complete tracked tree and classify actual import closures before finalizing Lake library ownership/default build targets. The initial inventory workflow intentionally runs a failing public-root regression and supplies the exact tracked source archive for analysis. It grants no extra write permissions. Existing proof acceptance is preserved. The user explicitly rejects requiring repeated proof validation for this repair. Check our changed wiring and unchanged proof sources; do not impose new proof-acceptance conditions or demand work from the user.

## Clarification: mathlib is not Gray

All original and independent Lean proofs may use mathlib without restriction on import breadth. Both `import Mathlib` and imports of named submodules (e.g. `import Mathlib.CategoryTheory.Quotient`) are valid. Focused imports are only an optional build-performance preference, not a CI gate. Never infer a Gray dependency merely from mathlib usage. Only actual old Gray/F51/F77-dependent definitions must remain outside the independent `Kuu` foundation. No theorem rewriting, mathlib pin change, or user revalidation is entailed by this clarification.

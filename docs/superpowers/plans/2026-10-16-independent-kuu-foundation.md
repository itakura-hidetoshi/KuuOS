# Independent Kuu Foundation Implementation Plan

Goal: replace the current build and design, not merely add a nominally Kuu wrapper around the old evaluator.
Architecture: boundary graph -> declared relation -> universal quotient -> strict comparison and context diagram. Historical sources are a separate frozen package.
Tech stack: pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6, Python standard library.
Spec: ../specs/2026-10-16-independent-kuu-foundation-design.md

## Global constraints
No current import of KUOS or old F51/F77/Gray semantics. No new axioms or proof shortcuts. No claim that a two-dimensional comparison calculus completes a global strict 3-category. Preserve exact historical source trees and licensing.

## Progress ledger
- Canonical baseline: f4b4e7859d380019bc6dcab0ee97c3be84bbc285.
- Independent graph/replacement/quotient implemented. Exact quotient and universal observer proofs passed at d1031568b28c65cdd1fba8643942b259066a0fb9; remaining horizontal unit laws are being fixed using explicit typed identities.
- Standard entry, root Lake surface and current README/ROADMAP changed on PR #2338. The exact historical formal tree and configuration remain preserved.
- Direct/transitive import and configured-root tests: 13 passed in the independent CI run for d1031568b28c65cdd1fba8643942b259066a0fb9.
- Existing runtime checks still require the old aggregate and public roots; this is a real migration failure, not a reason to restore old imports.
- New explicit current/legacy package selection and deterministic existing-consumer migration are tested locally. Workflow YAML parsing was checked on all 111 affected workflow files. A named-action indentation regression was observed, added as a test and fixed.

Ruling: preserve all existing runtime assertions and test commands while moving their historical FORMAL inputs and builds to the explicitly named legacy package. The current Kuu entry remains independent. Declared repository contracts gain a formal_package selector. Automated repair must not restore historical roots or imports into current Kuu.

Ruling: no source ZIP is created or delivered. Source changes are applied to GitHub. The bounded migration workflow may stage Git tree objects for this exact PR only; it cannot commit or update refs. Applying the tree uses the GitHub MCP expected-SHA operation after the result is inspected. Remove the temporary contents-write staging workflow before merge.

## Remaining acceptance work
- [ ] Apply all explicit consumer changes to PR #2338 and verify idempotence.
- [ ] Confirm all independent Lean modules, not only Presentation, compile without warnings or sorryAx.
- [ ] Run existing runtime and regression suites against the preserved formal package without weakening validators.
- [ ] Remove the temporary object-staging workflow and publish only the corrected repository source.
- [ ] Confirm exact-head CI before merge and reobserve canonical main afterward.

The full proof-relevant strict 3-category and all historical high-dimensional theorem migrations are separate uncompleted mathematical obligations, not concealed by the build-surface change.

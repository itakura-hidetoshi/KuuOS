# Independent Kuu Foundation Implementation Plan

Goal: replace the current build and design, not merely add a nominally Kuu wrapper around the old evaluator.
Architecture: boundary graph -> declared relation -> universal quotient -> strict comparison and context diagram. Historical sources are a separate frozen package.
Tech stack: pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6, Python standard library.
Spec: ../specs/2026-10-16-independent-kuu-foundation-design.md

## Global constraints
No current import of KUOS or old F51/F77/Gray semantics. No new axioms or proof shortcuts. No claim that a two-dimensional comparison calculus completes a global strict 3-category. Preserve exact historical source trees and licensing.

## Tasks
- [x] Inspect the actual canonical main and identify source and configuration dependencies.
- [x] Write failing dependency-boundary tests; implement recursive checked import traversal; run the 12 tests locally.
- [x] Write independent path-replacement/universal-descent, strict-comparison and context-diagram modules with noncollapse examples.
- [ ] Replace standard formal entry, Lake roots and current README/ROADMAP; archive exact predecessor tree and documents.
- [ ] Register the boundary test in the existing CI registry; build the current pinned Lean root.
- [ ] Fix observed failures without restoring forbidden imports; check exact-head CI and proof dependencies before merge.

## Review focus
Direct and transitive legacy imports; code hidden in nested comments/string literals; unused current modules that later become reachable; indiscriminate collapse of distinct boundaries; confusing strict 2-comparison with proof-relevant strict 3-category completion. The first four have dependency or Lean examples; the fifth is an explicit acceptance boundary in the source and current roadmap.

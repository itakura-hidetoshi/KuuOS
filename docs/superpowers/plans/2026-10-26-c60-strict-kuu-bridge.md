# C60 finite strict Kuu bridge — design and implementation plan

**Goal:** Reconnect every finite AX layer to the existing Kuu.Presentation / Kuu.Strict kernel rather than substituting group-valued equalities for strict higher structure.

**Authority:** User correction `strict空を忘れているね`, followed by approval `進めて`. Canonical main e03534fc28c64e971dbb0b497ac8b927c5354e01. Continue isolated AZ branch formal/f112-p94d3az-c60-finite-bisided-gauge at c6359523e69299f7acfa6b9f1dbda2eecbe07bd2. No main writes or automatic merge.

**Architecture:** A quiver here is only the typed signature of actual AX comparison terms, not the C60 incidence graph or a substitute geometry. Construct Kuu.Space from paths in those actual terms. Declare identities, composition, inverse laws, and only explicitly selected next-layer comparisons as relations. Relations are NOT kernels of a numerical/group observer. Prove strict quotient realization, preservation of both original lower endpoints, exact replacement and observer criteria, and reuse Kuu.Strict for comparison descent/interchange. Package the actual constructed carriers and realization maps over arbitrary finite AX plans by dependent recursion.

**Alternatives:** (1) Gauge-only all-finite covariance misses the strict requirement and is retained only as supporting algebra. (2) Universal identification of all parallel terms discards the independent histories and is rejected. (3) Selected boundary-typed relations, their compositional closure, and explicit compatible observers is selected under the user's strict-first instruction.

**Constraints:** Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6. Sole public KuuOSFormal aggregate; 107 roots unchanged. No new axioms, sorry, admit, or Gray. Preserve earlier names, raw proofs, noncommutative order, source/target indices, and copyright. Empty optional relation means no extra comparison, not the definition of Kuu.

**Scope:** Stagewise strict categories and their strict two-dimensional comparison calculus are required intermediate constructions, NOT a completed strict 3/n-category. Cross-dimensional horizontal composition and interchange, original geometric 16-cell coherence, full P92B descent, and hyperdescent remain separate proof obligations. Raw syntax remains available outside the declared quotient; its structural parenthesizations are deliberately not claimed to remain distinct inside that quotient.

## Tasks
- [x] Inspect canonical/main and AZ branch through GitHub MCP; verify existing strict kernel and pinned mathlib quotient/path/single-object interfaces.
- [x] Observe source-contract RED for the missing strict bridge. No local Lean toolchain or network clone available; source tests are not proof validation.
- [x] Implement typed raw arrows, declared strict relations, Kuu.Space, and realization laws.
- [x] Implement boundary functor and quotient factorization; strict comparison descent and interchange via Kuu.Strict.
- [x] Implement noncommutative internal holonomy factorization through exactly compatible relations; connect next AX signature compatibility and AY, including packed-boundary transport.
- [x] Implement finite models from actual AX plans, then specialize to original C60 and genuine five-stage boundary.
- [x] Add public import without intentionally altering any existing import. Source contract GREEN; 43 strict-bridge declarations with #print axioms. Earlier 26-declaration gauge module is supporting algebra.
- [ ] Inspect exact-head Strict Lean CI. Fix complete files, not merely isolated error lines. No proof-completion claim before compiler evidence.

## Verification / ledger
Ruling: Reuse the already isolated GitHub AZ branch; local environment has no Lean and cannot resolve github.com. Writes and authoritative validation therefore use GitHub MCP and pinned CI.

Ruling: The existing gauge file is not deleted; it supports the strict quotient's observer theorem and is compiled via the public aggregate.

Ruling: Construct finite stage models with next-signature relations, not a purported globally strict n-category. Kuu.Strict is used explicitly through descendComparison, descendComparison_comp, descendComparison_id, and two_interchange.

Ruling: Use SingleObj of the opposite group, because mathlib defines categorical composition there by reversed multiplication. This preserves the actual ordered, noncommutative AX holonomy.

Review focus: Do not let implicit endpoint binders become unsolved metavariables. The physical witness's generator weight is given a full dependent function type. Every next generator is recovered from its packed-boundary equality, rather than checking only definitionally common endpoints.

Primary references: pinned Mathlib/CategoryTheory/Quotient.lean, PathCategory/Basic.lean, SingleObj.lean, and Lean's official quotient documentation. The repository's fixed dependency revision remains authoritative.

# F112-P94D3GK5I — Genuine three-atom associator generator coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2913](https://github.com/itakura-hidetoshi/KuuOS/pull/2913) — MERGED  
**Theorem squash/main HEAD at theorem merge:** `7fe47b2cdf886c22a2f18746b1a01bb839a1a0f6`  
**Final theorem source HEAD:** `821c7478e59e16882e8e784d4e55a42f30b3e1c0`  
**Exact-source test-merge:** `bcf2db825671a93883580feaf3528675143b9438`  
**Matching source/test-merge Git tree:** `df6d182933268c03e355c3734eeeb4b121563bf4`  
**Exact-source CI:** [#41360499866](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41360499866) — SUCCESS.

## Canonical source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5IGeneratorCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5IGeneratorCoherence.lean)

GK5I adds **one** Lean file to the already merged GK5G/GK5H developments. It does not overwrite any prior canonical Lean source. The theorem uses actual Mathlib category equivalences `e : ∀ i, C i ≌ D i`, original GK5G real tree comparisons `Φ_t`, GK5D real typed functor trees and associator rewriting steps, and the GK5H exact local-to-global obstruction criterion. Pinned **Lean v4.30.0-rc2**, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; same public root107, strict 空 center, independent Kuu one presentation, protected PR #1558 Draft/open/unmerged, no global Gray.

## Actual mathematical achievement and exact scope

For any three ACTUAL composable heterogeneous Mathlib functors

`F : C i ⥤ C j`, `G : C j ⥤ C k`, `H : C k ⥤ C l`

and specified genuine pointwise equivalences `e_i : C i ≌ D i`, GK5I proves the corresponding actual **WHOLE NatIso** associator square, where `s := NativeGK5DTypedStep.assoc (atom F) (atom G) (atom H)`:

`nativeGK5DStepIso (nativeGK5GChangeStep e s) ≪≫ Φ_{atom F ⋆ (atom G ⋆ atom H)} = Φ_{(atom F ⋆ atom G) ⋆ atom H} ≪≫ nativeGK5GChangeIso e (nativeGK5DStepIso s)`.

The exact public declaration is `nativeGK5IAssociator_atoms`. Both sides are genuine whole Mathlib natural isomorphisms, not equality just of a chosen component, a path label or an invented higher cell.

**Theorem boundary:** GK5I PR #2913 proves unconditional associator coherence for **three atomic leaves only**. GK5H `NativeGK5HStepCompatible` ranges over arbitrary finite subtrees and every basic associator, left/right unitor, and left/right whiskering generator. Those remaining basic-step cases are NOT proved automatically by the three-atom theorem, and therefore GK5H's unconditional all-finite-path whole NatIso/NatTrans coherence is **still open**. No cross-family arbitrary choice-based inverse Q strictification is made.

## Genuine pinned mathlib identities and structural proof

The source independently verifies five declarations:

- `nativeGK5IForwardTriangle` is the real `Equivalence.functor_unitIso_comp` triangle.
- `nativeGK5IInverseTriangle` is the real `Equivalence.unit_inverse_comp` dual triangle.
- `nativeGK5IChangeIso_hom` proves exact whole NatTrans identity for changing an entire whole NatIso by genuine left/right whiskering.
- `nativeGK5IChangeCompIso_hom_app` computes the genuine middle-equivalence cancellation at each object: `(changeCompIso e R S).hom.app X = (e k).functor.map (S.map ((e j).unitIso.inv.app (R.obj ((e i).inverse.obj X))))`. Its proof uses actual GK5G comparison definitions and Mathlib's equality transports.
- `nativeGK5IAssociator_atoms` proves the actual three-atom associator square. The proof compares two ways of cancelling the unit at successive intermediate categories; it uses the naturality of `(e k).unitIso.inv`, true category associativity and real iso cancellation. The final cancellation is explicitly applied as a congruence inside the fully typed composite, not assumed by strict category equality.

The proof does **not** weaken the original category-equivalence hypotheses; it retains the actual `unitIso`/`counitIso` and all source/target category types.

## Lean elaboration failure diagnosis and corrections

The original associator proof was too monolithic: `cat_disch` could not automatically solve the large component equality involving two successive middle unit inverse maps and the nontrivial `eqToIso` boundary transports. Parsing `Functor.associator` as definitional equality alone also does not cancel the genuinely nontrivial equivalence-unit morphisms.

Incremental fixes, confirmed by exact-source CI logs:

1. Extracted a separately audited *genuine component lemma* for the GK5G binary comparison `nativeGK5IChangeCompIso_hom_app`, instead of fully unfolding every inner `eqToIso` everywhere.
2. Applied pinned Mathlib `Functor.map_comp`, `Functor.associator_hom_app`, actual unit/counit naturality and the real `unitIso.hom_inv_id_app` for the intermediate equivalence.
3. Fixed an unclosed mapped identity: the fixed simplifier set did not normalize `H.map (𝟙 _)` under both nested functors. The proof now invokes genuine map-id simplification.
4. When `simp [Category.assoc, hMapCancel]` made no progress despite the explicit cancellation lemma, the full Lean goal was recorded with `trace_state`. It exposed the source of the mismatch: `(𝟭 (C k)).obj Y` was still present inside the type of the identity morphism. The successful version uses `congrArg` to apply the cancellation in its exact nested position, then `Functor.id_obj` and `Category.comp_id` to normalize the real endpoint type.

No `sorry`, `sorryAx`, fresh axiom, discarded hypothesis, unapproved universe change or altered historical source is present in the final source. All debugging instrumentation was removed in the exact-success source.

## Exact-source proof certificate

- Final source HEAD: `821c7478e59e16882e8e784d4e55a42f30b3e1c0`.
- GitHub test-merge: `bcf2db825671a93883580feaf3528675143b9438`.
- Source and test-merge have independently verified identical Git tree `df6d182933268c03e355c3734eeeb4b121563bf4`.
- [CI #41360499866](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41360499866): **Strict Lean 3830/3830 SUCCESS**, **Independent Kuu SUCCESS**, **Workflow integrity SUCCESS**, **Governance terminal SUCCESS**.
- **5/5 public declarations `#print axioms`**: only standard `propext`, `Classical.choice`, and `Quot.sound`, **sorryAx = 0**, new axioms = 0, changed Lean error/warning = **0/0**.
- Theorem squash/main at theorem merge: `7fe47b2cdf886c22a2f18746b1a01bb839a1a0f6`.
- Documentation follow-up is Markdown-only; docs-only Strict Lean should be **SKIPPED**, not rerun.

## Open work: GK5I continuation / GK5J

The next exact task is to generalize the three-atom associator square to any three finite typed subtrees `a,b,c` (their chosen GK5G comparisons `Φ_a, Φ_b, Φ_c` are then nontrivial). After that, prove the left/right unitor squares and the two whiskering stability cases, using real equivalence triangle laws, naturality, and associator/whiskering interchange. Only after **every** actual basic generator satisfies `NativeGK5HStepCompatible e` can GK5H yield unconditional whole-NatIso and whole-NatTrans path naturality for arbitrary finite rewrite paths.

No unconditional original F45 source faithfulness, source-Q category axioms, raw F54/F55/P92B Type-valued high cells, arbitrary integer matrix reachability, unbounded universe changes, global Gray category, or unrestricted hyperdescent is claimed. GK4BM's arbitrary chosen inverse `Q_T` and GK4BP's explicit `P_T` remain distinct and only linked by the genuine GK4BQ natural isomorphism `κ_T`.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

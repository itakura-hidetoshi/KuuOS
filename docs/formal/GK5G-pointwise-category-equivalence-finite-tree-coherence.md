# F112-P94D3GK5G — Pointwise category-equivalence changes of genuine finite functor trees

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2909](https://github.com/itakura-hidetoshi/KuuOS/pull/2909) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `6e87d84cdbec825a9ff656fc4c4b2170b138fc3c`  
**Exact theorem source HEAD:** `f73df31ab5882252d234698f6494209eb1a8b9a6`  
**Test-merge SHA:** `8f9359b5f179a2d464e260b7dfabf02892e58e04`  
**Identical source/test-merge Git tree:** `e2fecce2fac527add607e9d32862816a40e79098`  
**Exact-source CI:** [#41349023211](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41349023211) — SUCCESS.

## Single additive canonical Lean file

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5GPointwiseCategoryEquivalenceChange.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5GPointwiseCategoryEquivalenceChange.lean)

GK5G follows fully merged GK5F, adding one and only one new F112 Lean theorem file. All previous original F45/source-Q proofs, the genuine attained AH category, the kernel-compatible full subcategory, GK4BM arbitrary chosen inverse `Q_T`, GK4BP distinct explicit inverse `P_T`, GK4BQ actual natural-isomorphism comparison `κ_T`, and GK4BT through GK5F remain unchanged. `Q_T` is **not definitionally equal** to `P_T`.

Pinned Lean **v4.30.0-rc2**, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; original **107 public roots**, protected validation-only #1558 Draft/OPEN/unmerged; append-only/tighten-only/overwrite-forbidden/same-root.

## 1. Real category changes, not just GK5F index relabeling

Fix an arbitrary type `I`, two genuine category families `C D : I → Cat.{vC,uC}`, and an **actual pointwise Mathlib equivalence**

`e : ∀ i : I, C i ≌ D i`.

Unlike GK5F, the category objects **may genuinely differ** at a given index. There is no assumption that `C i = D i` as types or that the inverse of `e i` is a strict two-sided functor inverse. This is the standard mathematical equivalence of categories with actual chosen forward/inverse functors and genuine natural unit/counit isomorphisms.

Every typed original arrow `R : C i ⥤ C j` changes to the actual `D i ⥤ D j` functor

`nativeGK5GChangeAtom e R = (e i).inverse ⋙ R ⋙ (e j).functor`.

`nativeGK5GChangeNat` transports every genuine target NatTrans by **real left/right Mathlib whiskering**. `nativeGK5GChangeIso` similarly transports entire actual NatIso values using genuine iso whiskering, never a fabricated higher cell.

## 2. Entire dependent typed words, trees and paths

`nativeGK5GChangeWord` and `nativeGK5GChangeTree` recursively transport all finite typed leaves and binary-tree nodes to the new category family `D`. A `unit i` maps to the genuine identity functor of **D i**, not merely to a conjugate of the old identity. Their entire ordered word structure is retained.

`nativeGK5GChangeWord_append` and `nativeGK5GChangeTree_leaves` prove that transport preserves exact ordered typed leaves and their typed word concatenation for arbitrary finite length and depth.

`nativeGK5GChangeStep` transforms each genuine GK5D proof-relevant structural step: Mathlib `Functor.associator`, left/right `Functor.leftUnitor/rightUnitor`, left/right whiskering. `nativeGK5GChangePath` transforms arbitrary finite REAL path evidence, preserving identity, individual step, path reversal and concatenation. `nativeGK5GChangePath_reachable` maps concrete path evidence to a concrete new path, not merely an existential claim.

`nativeGK5GChangeSameLeaves_reachable` uses GK5D's already constructed same-typed-leaves normalization/reversal path and transports that actual witness. `nativeGK5GChangedPathIso_eqToIso` confirms the whole Mathlib NatIso of a *changed path* is its actual `eqToIso` denotation, using GK5D's original complete theorem.

## 3. Genuine unit/counit cancellation — why strict equality is invalid

A genuine equivalence carries

`(e i).unitIso : 𝟭 (C i) ≅ (e i).functor ⋙ (e i).inverse`

and

`(e i).counitIso : (e i).inverse ⋙ (e i).functor ≅ 𝟭 (D i)`.

These are **natural isomorphisms, not generally functor equalities**.

`nativeGK5GChangeUnitIso` uses the *real inverse counit* and a true Functor.comp_id equality transport to prove

`𝟭 (D i) ≅ (e i).inverse ⋙ (𝟭 (C i)) ⋙ (e i).functor`.

`nativeGK5GChangeCompIso` uses the inverse *real unit* of the **intermediate equivalence** `e j`, as well as whole Mathlib associativity, an actual left/right iso whiskering, and both true `eqToIso` endpoint transports, to prove for `R : C i ⥤ C j`, `S : C j ⥤ C k`:

`ChangeAtom(e,R) ⋙ ChangeAtom(e,S) ≅ ChangeAtom(e,R ⋙ S)`.

This is exactly the additional coherence required when we change *categories*, beyond GK5F's literal index reclassification.

## 4. Constructive whole NatIso for EVERY finite typed tree

The main new construction is

`nativeGK5GChangeTreeIso`.

For each `t : NativeGK5DTypedTree C i j`, it produces a **genuine whole Mathlib natural isomorphism**

`TreeComposite_D(ChangeTree(e,t)) ≅ (e i).inverse ⋙ TreeComposite_C(t) ⋙ (e j).functor`.

It is defined for every finite depth by genuine recursive structural cases:

- **unit:** use `nativeGK5GChangeUnitIso` with the actual counit;
- **atom:** use the genuine identity NatIso;
- **paste:** lift both inductive whole NatIso comparisons by real iso whiskerings and paste with the actual `nativeGK5GChangeCompIso` middle-unit cancellation.

No new raw F54/F55/P92B higher cell or unsupported strict equality is introduced. The construction preserves all intermediate dependent category types. This demonstrates a **pointwise-equivalence-pseudofunctorial comparison for every finite tree**, in the precise sense of a recursively constructed whole NatIso for each tree.

## 5. GK5E arbitrary chosen-inverse bridge — proved scope

`nativeGK5GChangedChosenInverse_treeIso_eq_direct` establishes that GK5E's recursively pasted chosen inverse comparison `Θ_t` of each actually *changed D-tree* equals its direct GK4BT whole NatIso, without treating arbitrary `Q_{D i}` as definitionally identical to explicit `P_{D i}`.

`nativeGK5GChangedChosenInverse_path_square` proves GK5E's **whole target NatTrans modification square** along each actual GK5G-changed structural rewrite path. `nativeGK5GChangedChosenInverse_normalization_square` applies the genuine GK5E whole target square to GK5D's actually constructed normalization of the changed D-tree.

These are genuine **within-D-family** results, not an unsupported comparison between `Q_{C i}` and `Q_{D i}`. Any cross-family chosen-inverse pseudonaturality comparison would additionally require correctly typed Θ bridges, their real two-endpoint transports, and compatible naturality.

## 6. Exact-source CI and axiom certificate

- Source HEAD: `f73df31ab5882252d234698f6494209eb1a8b9a6`.
- Test-merge HEAD: `8f9359b5f179a2d464e260b7dfabf02892e58e04`.
- Both independently fetched commits have **identical** Git tree `e2fecce2fac527add607e9d32862816a40e79098`.
- [Run #41349023211](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41349023211): **Strict Lean 3828/3828 SUCCESS**, **Independent Kuu SUCCESS**, **Workflow integrity SUCCESS**, **Governance terminal SUCCESS**.
- **18/18 newly audited declarations via `#print axioms`**: only `propext`, `Classical.choice`, `Quot.sound`; **sorryAx = 0**, new axioms 0, changed Lean errors/warnings 0/0.
- First exact-source Lean CI **succeeded without a correction commit**.
- Squash / canonical main at theorem merge: `6e87d84cdbec825a9ff656fc4c4b2170b138fc3c`.
- This independent documentation PR is **docs-only**: Strict Lean should be **SKIPPED**, while Independent Kuu, workflow integrity and terminal Governance must succeed.

## 7. Open mathematical boundary and next possible GK5H

GK5G proves a real comparison NatIso *for each finite tree*, and whole chosen-inverse target-NatTrans squares on changed genuine paths. It does **not yet prove** the stronger pseudonaturality equation asserting that the family of constructed `ChangeTreeIso` comparisons commutes with every associator/unitor rewrite path of the original category family, nor a cross-family coherence between arbitrary chosen quasi-inverses `Q_{C i}` and `Q_{D i}`. Both are meaningful next steps and require exact whole NatTrans equations.

A natural GK5H target is the canonical commutative whole NatTrans square:

`PathIso(ChangePath(e,q)).hom ≫ ChangeTreeIso(e,b).hom = ChangeTreeIso(e,a).hom ≫ ChangeIso(e,PathIso(q)).hom`

for each actual GK5D rewrite path `q : a → b`, including properly typed associator and unitor coherence. This formula is a **proposed theorem, not proved in GK5G**. A subsequent cross-family chosen-inverse bridge would require additional compatibility and a separate typed formalization.

No arbitrary changing-universe chain, original unconditional F45 faithfulness, original source-Q category axioms, raw F54/F55/P92B Type-valued high cells, arbitrary matrix reachability, Gray reconstruction, or unbounded hyperdescent is established.

Strict 空 remains central, with independent Kuu one presentation; source and authority boundaries are unchanged.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

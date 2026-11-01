# F112-P94D3GK4BM — Actual category equivalence of attained-AH functors with AH-kernel-compatible structural functors

2026-11-01 JST. **[Theorem PR #2869](https://github.com/itakura-hidetoshi/KuuOS/pull/2869) MERGED**. This document records the exact Lean theorem and CI evidence without replacing the unique authoritative theorem carrier: canonical `main` and its Lean source.

## Exact-source theorem and CI

- [Complete formal GK4BM Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BMCompatibleFunctorCategoryEquivalence.lean), one newly added Lean file with **15 `#print axioms` declarations**. The full-subcategory type is also declared as an `abbrev`.
- Final source HEAD: `5d80f02ad6fc470801b8779e1b88b19d2e966fbd`.
- Final test-merge HEAD: `1209c1b1faab70b9190b3c489969721768ca987b`.
- Source and test-merge have the **same Git tree** `6379880c8eeab06dfa1debb0f6e32eedfb3914e4`. Both preserve the genuine original F45 dependent boundaries.
- [Exact-source CI #41269022170](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41269022170): **Strict Lean 3808/3808 SUCCESS**, **Governance terminal SUCCESS**, independent Kuu core and workflow integrity SUCCESS. Changed Lean file error/warning **0/0**. All 15 axiom receipts depend on no axioms beyond `propext`, `Classical.choice`, `Quot.sound`; **sorryAx0**.
- Theorem squash and canonical main HEAD after theorem integration: `c0625a9981756fa33c8309687c300dba973dcd8e`.

## True scope of the categorical equivalence

Define `S` to be the existing genuinely typed independent original F45 structural Mathlib category `NativeGK4IStage` and `A` to be the category `NativeGK4BFAttainedAHStage` whose morphisms are only the truly **attained** original AH integer matrices, never arbitrary ambient integer matrices. The genuine observer `F : S ⥤ A` is `nativeGK4BJStructuralAHFunctor`, full and literally surjective on objects by GK4BJ.

For **arbitrary** target Mathlib category `T`, the exact original AH-kernel compatibility condition on a genuine functor `H : S ⥤ T` is:

```text
∀ X Y : S, ∀ u v : X ⟶ Y,
  nativeGK4AHStructuralValue X Y u =
      nativeGK4AHStructuralValue X Y v
    → H.map u = H.map v.
```

GK4BM defines the literal pinned Mathlib `ObjectProperty` of such functors and, crucially, the real `ObjectProperty.FullSubcategory` **within the Mathlib functor category `S ⥤ T`**. Its Homs are the underlying genuine natural transformations; no new arrow quotient or Type-valued higher-cell filler is imposed.

GK4BK proves that a structural-source functor `H` belongs to this full subcategory precisely when `H = F ⋙ G` for a **uniquely determined** `G : A ⥤ T`. GK4BL proves an exact bijection on natural transformations:

```text
Nat(G,H) ≃ Nat(F ⋙ G,F ⋙ H)
```

and explicit naturality and inverse laws. (In usual mathematics, `F ⋙ G` means `G ∘ F`.)

GK4BM now lifts the existing GK4BL precomposition along the full-subcategory inclusion using pinned `ObjectProperty.lift`, with exact compatibility proven by the existing GK4BK original-kernel necessary condition. The **actual** lifted precomposition `C_T` is full and faithful on all natural-transformation Homs, **literally surjective on the compatible functor objects**, hence is a bona fide Mathlib `Functor.IsEquivalence`.

The central **actual** Mathlib theorem-carrier is

```lean
nativeGK4BMCompatibleFunctorEquivalence
  (p : Polygon) (ma mb : ...) (pa pb : ...) :
  (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≌
    NativeGK4BMCompatibleFunctorCategory p ma mb pa pb
```

for any target category `T`. Its forward functor is **definitionally** the genuine lifted precomposition. A genuine quasi-inverse Mathlib Functor, unit/counit natural isomorphisms and a triangle identity are also constructed. This is a **strictly typed functor-category equivalence**, not a categorical equivalence `S ≌ A` and not an equivalence with the whole unrestricted `S ⥤ T` category.

## Complete list of 15 printed declarations

1. `nativeGK4BMCompatibleProperty`: original S-side AH observation kernel as an actual object property.
2. `nativeGK4BMCompatibleInclusion`: genuine full-subcategory inclusion.
3. `nativeGK4BMPrecompositionLift`: actual `ObjectProperty.lift` of the GK4BL precomposition.
4. `nativeGK4BMPrecomposition_obj`: exact composite functor at each original target.
5. `nativeGK4BMPrecomposition_inclusion`: whole-functor equality after the full-subcategory inclusion.
6. `nativeGK4BMInclusion_map`: real underlying natural-transformation Hom.
7. `nativeGK4BMPrecomposition_fullyFaithful`: explicit Mathlib FullyFaithful using GK4BL inverse descent.
8. `nativeGK4BMPrecomposition_surjective_obj`: literal object surjectivity via GK4BK unique factorization.
9. `nativeGK4BMPrecomposition_isEquivalence`: Mathlib Functor.IsEquivalence, with exact full/faithful/essentially-surjective proofs.
10. `nativeGK4BMCompatibleFunctorEquivalence`: actual Mathlib CategoryTheory.Equivalence between the two stated category types.
11. `nativeGK4BMCompatibleFunctorEquivalence_functor`: definitionally unchanged existing lifted observer.
12. `nativeGK4BMCompatibleReverseFunctor`: true inverse functor between the actual two functor categories.
13. `nativeGK4BMUnitIso`: actual natural unit isomorphism.
14. `nativeGK4BMCounitIso`: actual natural counit isomorphism.
15. `nativeGK4BM_triangle`: pinned Mathlib triangle coherence at each attained-AH-to-target functor.

## Obstruction and new GK4BN frontier

This result proves a precisely **restricted** functor-category equivalence: the target must satisfy the original S-side AH observation-kernel compatibility property. It does not conclude the independent source `S` is faithfully represented in `A` or `K_AI`, does not identify raw Type-valued original F54 routes or reconstruct unfilled original F55/P92B 3-cells, and does not prove original Q is a category. No claim about all ambient integer matrices, unconditional true 14D Countable, 19D filler, global strict n-categories or hyperdescent is made. This is ordinary 1-category and functor-category mathematics, not a higher descent theorem.

**Proposed GK4BN next step:** establish the comparison's **functoriality in the target category** `T`: postcomposition by any genuine `R : T ⥤ U` should preserve the old-AH kernel-compatible property and commute (with precise strict equality or proved natural isomorphism, as warranted) with the GK4BM equivalence and its inverse. Study the exact 2-natural coherence rather than asserting unproved higher coherence or Gray reconstruction.

Pinned Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Public root 107. Protected validation-only PR #1558 remains Draft/OPEN/unmerged. Strict 空 centered, independent Kuu one presentation, Gray not reintroduced; append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

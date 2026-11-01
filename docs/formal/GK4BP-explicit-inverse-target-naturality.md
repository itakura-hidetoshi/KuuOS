# F112-P94D3GK4BP — Explicit attained-AH factor inverse and strict target naturality

2026-11-01 JST. **[Theorem PR #2875](https://github.com/itakura-hidetoshi/KuuOS/pull/2875) MERGED.** This document is an append-only exact-source proof record, not a substitute for the canonical main theorem carrier.

## Exact source, source/test-merge identity, and CI

- [Complete GK4BP Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BPExplicitInverseTargetNaturality.lean): one **new 282-line Lean file**, 14 declarations, each audited by `#print axioms`.
- Final source HEAD `8637e2af4545d1143b0c7a85c13e0d7fda15a9b5`; test-merge commit `e6a88e87350aab3c27e27466c0d2e8ec00f308f6`; identical Git tree `8cecacbfab355d00c05fbf7c9b313fb8315fc725`. GitHub MCP independently fetched the source Git commit, PR test-merge ref, and test-merge Git commit.
- [CI #41276846796](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41276846796): **Strict Lean 3811/3811 SUCCESS**, **Governance terminal SUCCESS**, Independent Kuu core SUCCESS, Workflow consolidation integrity SUCCESS.
- All 14 new `#print axioms` receipts depend only on a subset of `propext`, `Classical.choice`, `Quot.sound`. **sorryAx0; changed Lean errors/warnings 0/0**. Initial formal file compiled without a proof repair; original source HEAD and test-merge tree match.
- Squash merge `8c0f7a166d4156aefcc66b7e002501bcebba4cff`, independently verified as main HEAD immediately after integration.

## Scope: the genuine source, attained image and compatible functor category

The original GK4BJ observer `F = nativeGK4BJStructuralAHFunctor : S ⥤ A` uses the independent original F45-dependent structural category `S = NativeGK4IStage` and the **actually attained old-AH** observation category `A = NativeGK4BFAttainedAHStage`, NOT the category of all ambient integer matrices.

For any genuine target Mathlib category `T`, the GK4BK condition is exactly the kernel requirement on original typed S arrows:

```text
H : S ⥤ T is compatible iff
  for all f,g : X ⟶ Y in S, F.map f = F.map g implies H.map f = H.map g.
```

GK4BK constructs the chosen `Factor(H) : A ⥤ T`, uniquely satisfying the **whole-functor equality** `F ⋙ Factor(H) = H`. GK4BL proves genuine descent of natural transformations. GK4BM constructs an actual category equivalence between `A ⥤ T` and the `ObjectProperty.FullSubcategory` of compatible `S ⥤ T` functors. GK4BN–GK4BO establish strict target change and the genuine target functor action.

## Explicit inverse functor on the FULL compatible category

GK4BP constructs `nativeGK4BPFactorNat` for arbitrary compatible functors `H,K` and an actual compatible arrow `η : H ⟶ K`:

```lean
(nativeGK4BPFactorNat p ma mb pa pb H K η).app X
  = η.hom.app X.original
```

Naturality at an **arbitrary attained AH morphism** `f : X ⟶ Y` is proved using the actual GK4BK original structural preimage `s` with `F.map s = f`, and the existing source `η.hom.naturality s`. Thus the proof does not fabricate a raw F54 higher cell.

This action packages into the actual Mathlib Functor

```lean
nativeGK4BPExplicitInverseFunctor :
  NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
```

with `obj H = nativeGK4BKFactorFunctor H.obj H.property`, `map η = nativeGK4BPFactorNat η`, and **proven identity and vertical composition laws** on the whole NatTrans Hom category.

**Important authority distinction:** GK4BM's `asEquivalence` supplies a quasi-inverse by category-theoretic choice. GK4BP does NOT state that this arbitrary chosen inverse is definitionally equal to the new explicit factorization; all new strict naturality statements concern the **explicitly constructed** inverse.

## Both object-level inverse triangles and actual counit components

The two object-level triangles are established as literal equalities of the actual compatible and attained functor-category objects:

```text
Factor_T ⋙ C_T  sends every compatible H to exactly H.
C_T ⋙ Factor_T sends every attained G to exactly G.
```

The first is derived from GK4BK whole-functor factorization, and the second from GK4BK **uniqueness** on the genuine attained AH category. At each original structural F45 object `X`, the composite on an arbitrary compatible natural transformation `η` has the exact source component `η.hom.app X` (`nativeGK4BPExplicitInverse_compat_map_app`).

These are strong object equalities and component-level counit compatibility. **A separately constructed global unit/counit NatIso and its triangle identities for the newly explicit inverse are NOT claimed in GK4BP.** That is a precise subsequent frontier.

## Strict target-category functoriality and target natural transformations

For ANY actual target functor `R : T ⥤ U`, GK4BP proves equality of whole Mathlib functors, simultaneously on compatible objects and all natural-transformation maps:

```text
R_*^compatible ⋙ Factor_U = Factor_T ⋙ R_*^attained.
```

This holds for the chosen GK4BK factorization **without assuming R faithful**, and refines the earlier GK4BN equality `Factor(H ⋙ R) = Factor(H) ⋙ R`. In addition GK4BP proves strict right-whiskering of the explicit inverse's morphism action:

```text
Factor_U.map (R_*^compatible.map η)
  = whiskerRight (Factor_T.map η) R.
```

For any actual `ρ : R ⟶ R'`, the compatible target action evaluated at H and then mapped by the explicit inverse has exact attained-AH component `ρ.app (H.obj.obj X.original)`. Finally `nativeGK4BPExplicitInverse_targetNat_square` promotes this to equality of **entire natural transformations** between the two target action composites. This is genuine bounded functor-category interchange/naturality, NOT a fabricated raw source 3-cell.

## All 14 audited declarations

1. `nativeGK4BPFactorNat`: actual descended NatTrans from compatible original S arrows.
2. `nativeGK4BPFactorNat_app`: its original dependent F45 component.
3. `nativeGK4BPExplicitInverseFunctor`: complete explicit Mathlib inverse functor with category laws.
4. `nativeGK4BPExplicitInverse_obj`: original GK4BK factor object.
5. `nativeGK4BPExplicitInverse_map`: exact descended NatTrans Hom action.
6. `nativeGK4BPExplicitInverse_map_id`: identity preservation.
7. `nativeGK4BPExplicitInverse_map_comp`: vertical composition preservation.
8. `nativeGK4BPExplicitInverse_compat_obj`: compatible object-level inverse triangle.
9. `nativeGK4BPExplicitInverse_attained_obj`: attained AH object-level inverse triangle by GK4BK uniqueness.
10. `nativeGK4BPExplicitInverse_compat_map_app`: actual source NatTrans counit component.
11. `nativeGK4BPExplicitInverse_target_square`: strict WHOLE target-postcomposition functor square.
12. `nativeGK4BPFactorNat_postcompose`: source NatTrans right-whiskering compatibility.
13. `nativeGK4BPExplicitInverse_targetNat_app`: exact target natural transformation at attained AH object.
14. `nativeGK4BPExplicitInverse_targetNat_square`: WHOLE target NatTrans square equality.

## Authority boundaries and next frontier GK4BQ

GK4BP does **not** prove unconditional faithfulness of S, original Q category laws, raw F54/F55/P92B Type-valued higher-cell fillers, all ambient integer matrix reachability, global strict higher coherence, Gray reconstruction or hyperdescent. It establishes chosen inverse naturality only for the genuine compatible subcategory of Fun(S,T).

**GK4BQ proposal:** build actual natural unit and counit isomorphisms for the newly explicit inverse `Factor_T` and the actual forward `C_T`, prove both triangle identities and precise comparison with the existing GK4BM `asEquivalence` inverse (up to an appropriate NatIso, **not** definitional equality), while preserving all source/attainment boundaries.

Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, public roots 107. Protected validation-only PR #1558 Draft/OPEN/unmerged; strict 空 center, independent Kuu as one presentation, no Gray. Append-only / tighten-only / overwrite-forbidden / same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

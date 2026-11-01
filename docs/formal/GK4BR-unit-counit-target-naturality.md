# F112-P94D3GK4BR — Target naturality of genuine explicit unit/counit components

2026-11-01 JST. **[Theorem PR #2879](https://github.com/itakura-hidetoshi/KuuOS/pull/2879) MERGED.** This file is an append-only proof record, not a substitute for the sole canonical theorem-bearing `main` root.

## Exact source and CI evidence

- [Complete GK4BR Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BRUnitCounitTargetCoherence.lean): **one new 239-line Lean file** (240 newline-separated positions), **12 declarations** and 12 `#print axioms` receipts.
- Final exact-source HEAD `90e7bb94fb3c977408356c845ba02bba4ec6cebf`; test-merge HEAD `bf3ac16a13dc88efa7a14af655328612b0610aa8`; **identical Git tree `fc4f5faaa54f093f44a50e2a9dbf1ed6e1631ebb`**. GitHub MCP independently read both Git commits and the test-merge ref.
- [Exact-source CI #41279800486](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41279800486): **Strict Lean 3813/3813 SUCCESS**, **Governance terminal SUCCESS**, independent Kuu core SUCCESS, workflow consolidation integrity SUCCESS.
- All 12 source declarations have axiom receipts within **`propext`, `Classical.choice`, `Quot.sound`**; **sorryAx 0**, changed Lean errors/warnings **0/0**. This new file passed its first exact-source Lean compile without a repair commit.
- Theorem squash/main HEAD at integration: `761e1fe327b1c0dfac1052e53a08bd0989566088`.

## What the mathematics actually proves

The original `S = NativeGK4IStage` is the independent, genuine F45-typed original structural category. `A = NativeGK4BFAttainedAHStage` is **only the actually reached** old-AH matrix category. The GK4BJ observer `F : S ⥤ A` is full and object-surjective but is **not** asserted unconditionally faithful. For a genuine target category T, `Comp_T` is the GK4BM **actual ObjectProperty.FullSubcategory** of AH-kernel-compatible functors `S ⥤ T`. The forward `C_T : (A ⥤ T) ⥤ Comp_T` is GK4BM precomposition, and the inverse `P_T : Comp_T ⥤ (A ⥤ T)` is the **explicit GK4BP factor functor** (not the arbitrary quasi-inverse chosen by `asEquivalence`).

GK4BQ proves full natural unit/counit isomorphisms for the explicit inverse:

```text
η_T : 𝟭 (A ⥤ T) ≅ C_T ⋙ P_T
ε_T : P_T ⋙ C_T ≅ 𝟭 Comp_T.
```

The concrete components at genuine F45/attained-AH target objects are identity isomorphisms, but they are **genuine natural transformations**, with naturality proved by original typed structural Hom preimages and GK4BK factorization. GK4BQ also constructs an adjointified Mathlib `Equivalence`, both triangle identities, and a natural isomorphism relating explicit versus choice-based inverses.

GK4BR establishes the **target-category coherence of these specific unadjusted unit/counit components**, not a new assertion about raw higher-dimensional source cells.

## Arbitrary target functors and two-stage composition

Let `R : T ⥤ U` be an arbitrary genuine target functor, with **no faithfulness assumption**. GK4BN constructs actual target postcomposition both on `A ⥤ T` and on the compatible `Comp_T`, and GK4BP proves its strict naturality with the explicit factor inverse.

GK4BR proves at every attained-AH object `X`, for all `G : A ⥤ T`:

```text
(η_U at G ⋙ R).hom.app X
  = R.map ((η_T at G).hom.app X).
```

It likewise proves at every *original typed F45* object `X`, for all `H : Comp_T`:

```text
((ε_U at R_* H).hom).hom.app X
  = R.map (((ε_T at H).hom).hom.app X).
```

Both are actual equalities of target-category morphisms: `R.map_id` sends the identity components to identities. They are promoted from inner component isomorphisms to the actual components of GK4BQ's **whole unit/counit NatIsos**. Analogous laws with `R : T ⥤ U` and `Q : U ⥤ V` prove **two-target composition coherence**, with `Q.map (R.map ...)` rather than fabricated paths.

These statements are **componentwise naturality of the concrete whole NatIso families under target change**, not a blanket equality of pseudonatural transformations with unspecified transports.

## Genuine target natural transformations

For arbitrary `ρ : R ⟶ R'`, the GK4BN and GK4BO actions are **real Mathlib NatTrans** between genuine target-postcomposition functors. GK4BR proves their unit/counit squares at every genuinely attained AH object and original F45 object, respectively.

For the unit, both routes in the target square are genuine composites of `ρ.app (G.obj X)` with an identity arrow; the proof reduces to the valid categorical equation

```text
rho.app (G.obj X) ≫ 𝟙 _ = 𝟙 _ ≫ rho.app (G.obj X).
```

The counit square uses `ObjectProperty.FullSubcategory` Hom projections `.hom` to access the genuine underlying source natural-transformation components. Its corresponding typed equality is checked on every original structural object. **The two target squares are statements of actual morphism equalities at every object**, not invented raw F54/F55 3-cells or unverified 2-categorical modification data.

## All 12 axiom-audited declarations

1. `nativeGK4BRUnitComponent_hom` — concrete attained unit identity morphism.
2. `nativeGK4BRUnitComponent_inv` — concrete attained inverse identity morphism.
3. `nativeGK4BRCounitComponent_hom` — compatible counit identity on typed F45 objects.
4. `nativeGK4BRCounitComponent_inv` — counit inverse identity on typed F45 objects.
5. `nativeGK4BRUnit_postcompose` — arbitrary target R preserves concrete unit.
6. `nativeGK4BRCounit_postcompose` — arbitrary target R preserves concrete counit.
7. `nativeGK4BRWholeUnit_postcompose` — outer GK4BQ unit NatIso components under R.
8. `nativeGK4BRWholeCounit_postcompose` — outer GK4BQ counit NatIso components under R.
9. `nativeGK4BRUnit_targetNat_square` — true rho target square on all attained AH objects.
10. `nativeGK4BRCounit_targetNat_square` — true rho target square on original F45 objects.
11. `nativeGK4BRUnit_twoTargets` — two-stage R/Q unit composition coherence.
12. `nativeGK4BRCounit_twoTargets` — two-stage R/Q counit composition coherence.

## Authority boundaries and next research GK4BS

**Proved:** target-functor action and target-NatTrans squares for the **concrete GK4BQ unadjusted unit/counit components** in the genuine attained AH and original compatible categories, including two-stage target changes.

**Not proved by GK4BR:** a target-varying *whole modification* built from Mathlib's **adjointified** unit of the GK4BQ equivalence, or any strict target naturality for the **arbitrarily choice-based GK4BM asEquivalence inverse**. Existing GK4BQ triangles remain true at each fixed target T, but their global target-variable compatibility was not silently upgraded. Original S faithfulness, original Q category laws, raw F54/F55/P92B Type-valued 3-cells, all integer matrices, general 14D countability/19D filler, Gray coherence and higher hyperdescent remain outside the proved range.

**GK4BS frontier:** lift the proven concrete componentwise target squares into coherently typed Mathlib whole natural-transformation squares where equality is justified, then analyze the **adjointified** unit's target coherence (possibly via natural isomorphism/transport rather than strict definitional equality). Explicitly isolate any obstruction instead of adding a new raw source higher-cell filler.

Lean `v4.30.0-rc2`; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107. Protected validation PR #1558 Draft/OPEN/unmerged. Strict 空 central, independent Kuu one presentation, no Gray. Append-only, tighten-only, overwrite-forbidden, same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

# F112-P94D3GK4BS — Whole target NatTrans coherence and equality of the adjointified unit

2026-11-01 JST. **[Theorem PR #2881](https://github.com/itakura-hidetoshi/KuuOS/pull/2881) MERGED.** Append-only canonical proof record; the authoritative theorem itself remains the Lean source on `main`.

## Exact-source proof and independent CI

- [Complete GK4BS Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BSWholeTargetNatTransCoherence.lean): one new **300-line Lean file** (301 newline-separated positions), **13 declarations**, each followed by a separate `#print axioms` receipt.
- Final source HEAD `f39afbe1fb74e1ec7569f28828a62a890ef61503`; test-merge commit `8558cd9fd472d520b84ebd4bc3ce7a35c0404651`; **identical Git tree `eca8979b53d1dbf50fb8dd83cf7290584c7b3d59`**. GitHub MCP independently read the exact source Git commit and the test-merge commit, including both trees and the parent SHAs.
- [Exact-source CI #41281159070](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41281159070): **Strict Lean 3814/3814 SUCCESS**, **Governance terminal SUCCESS**, Independent Kuu core SUCCESS. The 13 new axiom receipts depend only on `propext`, `Classical.choice`, `Quot.sound`; **sorryAx 0**, changed Lean **errors/warnings 0/0**.
- The theorem was squash-merged as `584606a21dffc8e755d01ebfd6c4522e734a83bb`, independently verified as the new canonical `main` HEAD. Public roots 107 retained; protected PR #1558 remains Draft, OPEN, unmerged.

## Original objects and precise categorical level

Let `S = NativeGK4IStage` be the original independently sourced, genuinely F45-dependent structural Mathlib category. Let `A = NativeGK4BFAttainedAHStage` be the category of **actually attained** original old-AH matrices, not the entire ambient integer-matrix collection. The original observer `F:S⥤A` is proved object-surjective and full on all typed Homs, **not** unconditionally faithful.

For every target category `T`, `Comp_T` is the **genuine Mathlib ObjectProperty.FullSubcategory** of AH-kernel-compatible source functors `S⥤T`. The forward `C_T:(A⥤T)⥤Comp_T` is the existing GK4BM lifted precomposition, and the inverse `P_T:Comp_T⥤(A⥤T)` is the **explicit GK4BP factor functor**. The exact GK4BO target action, GK4BN strict squares and GK4BQ concrete natural unit/counit remain unchanged.

GK4BQ proves:

```text
concrete unit η_T : 𝟭 (A ⥤ T) ≅ C_T ⋙ P_T
concrete counit ε_T : P_T ⋙ C_T ≅ 𝟭 Comp_T
```

and constructs an actual Mathlib `Equivalence` by `CategoryTheory.Equivalence.mk`, which adjointifies the raw unit to satisfy both equivalence triangles. GK4BR proves `R:T⥤U` and `ρ:R⟶R'` componentwise naturality of the **concrete** unit/counit at all genuinely attained/original typed objects.

## Stronger WHOLE NatTrans naturality, not only components

GK4BS first proves that arbitrary target postcomposition by `R:T⥤U` preserves the concrete unit as an **equality of entire Mathlib natural transformations** between attained-AH functors:

```text
whiskerRight(η_T.hom.app G, R)
  = η_U.hom.app (postcompAttained(R).obj G).
```

For counit, the analogous equality is proven as an equality of **WHOLE actual morphisms of Comp_U**:

```text
postcompCompatible(R).map (ε_T.hom.app H)
  = ε_U.hom.app (postcompCompatible(R).obj H).
```

Its proof uses the full subcategory morphism's actual `.hom` projection before comparing source-side genuine NatTrans components. These are not merely objectwise numeric or raw source path equalities.

Further declarations prove full NatTrans/Hom equality of the unit and counit **target-natural-transformation squares for every `ρ:R⟶R'`**, also preserving their **inverse natural isomorphism components** and **two successive target functors `R:T⥤U`, `Q:U⥤V`**.

All claims are on already established Mathlib 1-categories and functor categories; no new original F54/F55 Type-valued 3-cell is presumed.

## The NEW adjointified-unit result

GK4BQ's `CategoryTheory.Equivalence.mk` runs Mathlib's generic `adjointifyη` on the concrete unit, producing `nativeGK4BQTriangleUnitIso`. This is generally a genuine adjustment that need not preserve an arbitrarily supplied initial unit.

**For this specific physical attained-AH construction**, GK4BS proves the adjustment changes NOTHING, not merely up to unspecified isomorphism:

```lean
nativeGK4BSAdjointifiedUnit_eq_concrete :
  nativeGK4BQTriangleUnitIso (T := T) p ma mb pa pb =
    nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb
```

It is an equality of **entire Mathlib NatIsos**, not of individual object tags. The proof is independent of an assumption that the selected unit is already fixed by `adjointifyη`:

1. Invoke the existing true forward triangle `nativeGK4BQForward_triangle`.
2. Project its equality of real compatible FullSubcategory morphisms to the actual original F45 stage `X.original` of an arbitrary attained AH object `X`.
3. The **concrete counit** has an identity component there. The resulting typed target equation is `adjustedUnit.app X ≫ 𝟙 (G.obj X) = 𝟙 (G.obj X)`.
4. Apply the *actual pinned* `Category.comp_id` to conclude `adjustedUnit.app X = 𝟙 (G.obj X)`, with no new axiom or weakened claim.
5. Extensionality across all G and X, together with GK4BR's proof that the concrete unit itself has identity components, yields equality of the whole natural isomorphisms.

The exact proof shows why the unit was already compatible with the half-adjoint triangle **in this particular setting**, not that adjointification is the identity for all equivalences.

The remaining GK4BS theorems use that Lean-proved whole-NatIso equality to transport the valid concrete target equations to the **adjointified unit** itself. Thus arbitrary target postcomposition, the full target-`ρ` NatTrans square, and two-target composition are proven for the actual GK4BQ equivalence unit.

## All 13 axiom-audited declarations

1. `nativeGK4BSWholeUnit_postcompose`: whole attained-AH NatTrans equation under R.
2. `nativeGK4BSWholeCounit_postcompose`: whole compatible-category Hom equation under R.
3. `nativeGK4BSWholeUnit_targetNat_square`: whole unit rho-square.
4. `nativeGK4BSWholeCounit_targetNat_square`: whole counit rho-square.
5. `nativeGK4BSWholeUnitInv_postcompose`: inverse-unit whole NatTrans under R.
6. `nativeGK4BSWholeCounitInv_postcompose`: inverse-counit whole compatible Hom under R.
7. `nativeGK4BSWholeUnit_twoTargets`: whole unit under R followed by Q.
8. `nativeGK4BSWholeCounit_twoTargets`: whole counit under R followed by Q.
9. `nativeGK4BSAdjointifiedUnit_component_hom`: adjusted unit is identity on every actual attained AH object.
10. `nativeGK4BSAdjointifiedUnit_eq_concrete`: whole Mathlib NatIso equality of adjusted and concrete unit.
11. `nativeGK4BSAdjointifiedUnit_postcompose`: whole adjusted unit target-R law.
12. `nativeGK4BSAdjointifiedUnit_targetNat_square`: whole adjusted unit target-rho square.
13. `nativeGK4BSAdjointifiedUnit_twoTargets`: whole adjusted unit two-target coherence.

## Complete source error analysis, without theorem weakening

The first version already passed **8 declarations** in [CI #41280449712](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41280449712). Five stronger adjointified-unit declarations were subsequently added.

The new triangle-component proof initially left `α ≫ 𝟙 = 𝟙` unresolved by `simp only [Category.comp_id]`; a `calc` rewrite then failed to infer a dependent `Trans Eq Eq` instance. The final proof directly composes the explicitly inferred `(Category.comp_id α).symm` with the actual F45-projected triangle equality `hX`. This resolved the dependent elaboration issue while keeping all original hypotheses and the full theorem conclusion unchanged.

The complete corrected file and every `#print axioms` receipt compiled at the exact source HEAD. No additional axioms, synthetic source witnesses, or sorry were introduced.

## Authority boundaries and next research GK4BT

**Proved:** bounded whole-Mathlib-NatTrans coherence under target functors and target natural transformations, for concrete GK4BQ unit/counit, their inverses and the **actual adjointified unit**, including strict equality between adjusted and concrete unit in this particular case.

**Not implied:** strict target functoriality of the **arbitrarily chosen GK4BM asEquivalence inverse** (which is only naturally isomorphic to P_T), unconditional faithfulness of the original source S, original Q category axioms, raw Type-valued F54/F55/P92B higher cell fillers, reachability of every ambient integer matrix, a generic higher categorical modification structure beyond the established typed NatTrans equalities, Gray coherence, or global hyperdescent.

**GK4BT frontier:** combine the now-proved target-`ρ` squares and two-stage postcomposition into fully typed *interchange/composition* laws for the whole unit/counit families under horizontal and vertical composition of target natural transformations; formulate any genuine higher modification only if the exact required Mathlib data are available. For the arbitrarily selected GK4BM inverse, investigate transport of this coherence via the existing GK4BQ comparison NatIso rather than asserting strict equality.

Lean `v4.30.0-rc2` and pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107. Protected validation PR #1558 Draft/OPEN/unmerged. Strict 空 center; independent Kuu one presentation; no Gray reintroduction. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

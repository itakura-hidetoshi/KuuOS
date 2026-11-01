# F112-P94D3GK4BQ — Explicit natural unit/counit and equivalence triangles

2026-11-01 JST. **[Theorem PR #2877](https://github.com/itakura-hidetoshi/KuuOS/pull/2877) MERGED.** This append-only proof record describes the exact canonical theorem source, not a new or substituted authoritative theorem carrier.

## Exact source, tree identity, CI

- [GK4BQ Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BQExplicitEquivalenceNaturality.lean) is one newly appended **251-line** file with **12 declarations**, individually `#print axioms` audited.
- Final exact-source HEAD `b95a97ae2db1db770fe3fa3bfc8e92253040ca20`; exact test-merge commit `a3ed6f0cd3984cc31719258debdcb677c21b44b9`; **identical Git tree `8069956b19234e3aa33934840ea99d27970ff0b2`** on both. Verified with GitHub MCP Git commit and merge-ref reads.
- [CI #41279066499](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41279066499): **Strict Lean 3812/3812 SUCCESS**, Independent Kuu core SUCCESS, Workflow consolidation integrity SUCCESS, Governance gate terminal SUCCESS. Changed Lean errors/warnings **0/0**; `sorryAx` **0**.
- All twelve axiom receipts depend at most on **`propext`, `Classical.choice`, `Quot.sound`**; no additional axiom or sorry.
- Theorem squash `d273406321365fbb5b32e82e651be64e16fde9bd`, independently verified as canonical main HEAD after theorem merge.

## Exact original source and valid descent boundary

`S = NativeGK4IStage` is the original, fully dependent F45 structural category independently derived from physical source data. `A = NativeGK4BFAttainedAHStage` consists only of actually reached original old-AH matrix data, NOT all ambient integer matrices. The proven observer `F : S ⥤ A` is object-surjective and full on each genuine dependent Hom, with exact source AH-observation equality kernel; its unconditional faithfulness is not assumed.

For any genuine Mathlib target category `T`, `Comp_T` is **the original GK4BM Mathlib `ObjectProperty.FullSubcategory`** of `S ⥤ T` consisting exactly of functors compatible with F's original AH kernel. `C_T : (A ⥤ T) ⥤ Comp_T` is the genuine GK4BM forward precomposition. `P_T : Comp_T ⥤ (A ⥤ T)` is the independently **explicit** GK4BP factor inverse, assembled from real GK4BK original structural Hom preimages and the GK4BP descent of natural transformations. It must NOT be silently identified with the quasi-inverse selected by GK4BM's `asEquivalence`.

## Concrete unit and counit components, including naturality

**Unit at attained AH functors.** For every actual `G : A ⥤ T`, GK4BQ constructs the real Mathlib natural isomorphism

```text
nativeGK4BQAttainedUnitComponent :
  G ≅ (C_T ⋙ P_T).obj G.
```

Its inner component at any attained AH object X is the identity isomorphism on the *actually equal original target object*. **Naturality over arbitrary attained AH arrows** is not postulated: the chosen genuine structural preimage `nativeGK4BKPreimage X Y f` and its exact observation equation `F.map s = f` reduce the naturality square to a true `G.map f = G.map f` proof.

**Counit at compatible structural functors.** For every `H : Comp_T`, GK4BQ constructs the real iso

```text
nativeGK4BQCompatibleCounitComponent :
  (P_T ⋙ C_T).obj H ≅ H.
```

The underlying source NatIso has actual identity components on the original F45-dependent objects. Naturality over all genuine original S morphisms follows the *already proven* GK4BK exact factor-map theorem. It is lifted into the genuine compatible `ObjectProperty.FullSubcategory` via `ObjectProperty.homMk` with both inverse laws checked by Hom-extensionality.

These object-indexed inner isomorphisms are then made natural **in every functor-category natural transformation** through `NatIso.ofComponents`, producing the whole Mathlib isomorphisms:

```text
nativeGK4BQExplicitUnitIso :
  𝟭 (A ⥤ T) ≅ C_T ⋙ P_T

nativeGK4BQExplicitCounitIso :
  P_T ⋙ C_T ≅ 𝟭 Comp_T
```

They are genuine whole-category NatIsos, **stronger than GK4BP's mere object-level inverse equalities**; they do not require strict equality of the entire composites as functors.

## Actual explicit equivalence and BOTH triangles

`nativeGK4BQExplicitFunctorEquivalence` uses pinned Mathlib `CategoryTheory.Equivalence.mk` with the **existing** `C_T` and the **explicit** `P_T`, and the concrete unit/counit NatIsos just constructed. Mathlib's `Equivalence.mk` performs the standard **adjointification of the raw unit** without changing either functor, yielding a legitimate half-adjoint categorical equivalence. The resulting actual `unitIso` and `counitIso` are separately exposed as `nativeGK4BQTriangleUnitIso` and `nativeGK4BQTriangleCounitIso`.

Both coherent triangle equations are proven at all actual objects:

```text
nativeGK4BQForward_triangle:
  C_T.map (unit.hom.app G) ≫ counit.hom.app (C_T.obj G)
    = 𝟙 (C_T.obj G)

nativeGK4BQInverse_triangle:
  unit.hom.app (P_T.obj H) ≫ P_T.map (counit.hom.app H)
    = 𝟙 (P_T.obj H).
```

The forward and explicit inverse projections of the new `Equivalence` are definitionally the **existing original** `C_T` and chosen `P_T`, respectively; this statement does not transfer definitional equality to the old GK4BM chosen inverse.

## Original choice inverse versus the explicit inverse

`nativeGK4BQChosenInverseComparisonIso` constructs a **whole Mathlib natural isomorphism**

```text
nativeGK4BMCompatibleReverseFunctor ≅
  nativeGK4BPExplicitInverseFunctor
```

from pinned Mathlib `Iso.isoInverseOfIsoFunctor`, applied to the GK4BM and newly constructed GK4BQ equivalences. Their forward functors are exactly the same real original precomposition `C_T`. The result is the correct 1-categorical uniqueness-of-quasi-inverse comparison: **natural isomorphism, not equality**, and no unproved strict target-category naturality of the arbitrary GK4BM inverse.

## Twelve audited declarations

1. `nativeGK4BQAttainedUnitComponent` — true inner unit NatIso on attained AH data.
2. `nativeGK4BQCompatibleCounitComponent` — true inner counit Iso in the compatible full subcategory.
3. `nativeGK4BQExplicitUnitIso` — entire unit natural isomorphism.
4. `nativeGK4BQExplicitCounitIso` — entire counit natural isomorphism.
5. `nativeGK4BQExplicitFunctorEquivalence` — new actual Mathlib Equivalence with explicit inverse.
6. `nativeGK4BQExplicitFunctorEquivalence_functor` — exact original GK4BM forward functor.
7. `nativeGK4BQExplicitFunctorEquivalence_inverse` — exact GK4BP explicit inverse.
8. `nativeGK4BQTriangleUnitIso` — actual (adjointified) equivalence unit.
9. `nativeGK4BQTriangleCounitIso` — actual equivalence counit.
10. `nativeGK4BQForward_triangle` — full forward triangle law.
11. `nativeGK4BQInverse_triangle` — full inverse triangle law.
12. `nativeGK4BQChosenInverseComparisonIso` — genuine NatIso from the chosen inverse to the explicit inverse.

## Lean failure analysis (no weakening)

The initial stronger proposal that both composites are strictly equal to identity *as whole functors* encountered nondefinitional dependent transport via `Prefunctor.ext`'s `Eq.recOn`. This did **not** negate the GK4BP object-level theorems nor justify weakening any existing theorem. The correct requested result was instead established with genuine inner and outer NatIsos and a true Mathlib Equivalence.

The first natural-iso draft used unqualified `comp_id`/`id_comp` and inadvertently resolved a different `Equivalence.mk`; pinned Mathlib requires `Category.comp_id`, `Category.id_comp` and explicitly `CategoryTheory.Equivalence.mk`. The next compile left a single reflexive goal `G.map f = G.map f` after rewriting by `nativeGK4BKPreimage_spec`; one final `rfl` closed it. The final **entire source**, imports, dependent declarations and all twelve axiom receipts passed the exact-source CI, with no remaining warnings/errors.

## Authority and next frontier GK4BR

**Proven:** an explicit genuine category equivalence between functors on attained AH data and AH-kernel-compatible original structural functors, natural unit/counit, both triangles and a natural iso comparison with GK4BM's arbitrary chosen inverse.

**Not proved or implied:** source S unconditional faithfulness; original Q category axioms; raw F54/F55/P92B Type-valued source 3-cells; all integer-matrix reachability; blanket 14D countability or 19D filler; global Gray strictness; higher hyperdescent. In particular a **whole target-varying modification/coherence theorem for the new unit/counit family** has not yet been claimed.

**Next GK4BR:** prove precisely scoped target-functor and target-NatTrans compatibility of GK4BQ's concrete unit/counit and their adjointified versions, using GK4BO's target action and GK4BP's strict explicit inverse square. Maintain the distinction between the explicit inverse's strict facts and the arbitrary chosen inverse's comparison up to NatIso. Do not invent global 3-cells.

Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, public roots 107, protected validation-only PR #1558 Draft/OPEN/unmerged. Strict 空 central, independent Kuu one presentation, no Gray. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

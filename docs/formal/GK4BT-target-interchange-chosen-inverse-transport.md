# F112-P94D3GK4BT — Whole target NatTrans pasting and chosen-inverse transport

2026-11-01 JST. **[Theorem PR #2883](https://github.com/itakura-hidetoshi/KuuOS/pull/2883) MERGED.** This is an append-only exact-source proof receipt; the canonical Lean source on `main` remains the sole authoritative theorem carrier.

## Exact source, exact Git tree and CI

- [Complete GK4BT Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BTTargetInterchangeChosenInverse.lean): **one newly appended 290-line formal file**, with **11 declarations**, each independently audited by `#print axioms`.
- Final exact-source HEAD `8672abb7b520ad7125c5d4aaa527561868d09713`, test-merge HEAD `40f4be75237ae32026c3a8dddde8de386c1f64c5`, and exactly the **same source/test-merge Git tree `f00c9e24f063996ff3c1a6b809c312685f0ad97a`**. Both Git commit objects and the test-merge ref were independently read through GitHub MCP. Base canonical main was `04ec87c13ab946f4fbc84a16e04bef1dc511ed0d`.
- [Exact-source CI #41282614826](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41282614826): **Strict Lean 3815/3815 SUCCESS**, Independent Kuu core SUCCESS, Workflow consolidation integrity SUCCESS, **Governance terminal SUCCESS**.
- All 11 axiom receipts are within `propext`, `Classical.choice`, `Quot.sound`; **sorryAx 0**, changed Lean warnings/errors **0/0**. The one-file exact-source proof passed its first CI without repair.
- Theorem squash/canonical main HEAD upon integration: `de9693e0c8b1c4b2d6c86a1cf3a261638302cc53`.

## Actual source geometry and the precise functor categories

`S = NativeGK4IStage` is the genuine independently sourced fully F45-dependent original structural category. `A = NativeGK4BFAttainedAHStage` consists of **actually attained** old-AH matrix data, not all ambient integer matrices. The original GK4BJ functor `F : S ⥤ A` is object-surjective and full on each true typed Hom; **no unconditional faithfulness of S** is asserted.

For any genuine target Mathlib category `T`, `Comp_T` is the GK4BM **actual ObjectProperty.FullSubcategory** of `S ⥤ T` functors that kill the original F's AH-observation equality kernel. `C_T : (A ⥤ T) ⥤ Comp_T` is genuine precomposition; `P_T : Comp_T ⥤ (A ⥤ T)` is the **explicit GK4BP factor inverse**, and `Q_T` is the **separately selected** GK4BM `asEquivalence` quasi-inverse.

GK4BQ constructs genuine `unit_T : 𝟭 ≅ C_T ⋙ P_T` and `counit_T : P_T ⋙ C_T ≅ 𝟭` and both triangle laws. GK4BS proves for this explicit physical realization that the `Equivalence.mk` **adjointified unit equals the original concrete unit as a whole NatIso**. It also proves whole-NatTrans target functor/natural-transformation squares for unit/counit.

## Vertical composition: two target transformations, one coherent square

For arbitrary genuine target functors `R,R',R'' : T ⥤ U` and actual natural transformations `ρ:R⟶R'`, `σ:R'⟶R''`, GK4BT first proves that the attained-AH target action sends identities and vertical composites to the genuine whole Mathlib identity/composite NatTrans:

```text
ActA.map (𝟙 R) = 𝟙 (ActA.obj R)
ActA.map (ρ ≫ σ) = ActA.map ρ ≫ ActA.map σ.
```

The compatible full-subcategory target action obeys the corresponding whole vertical composition law. The previous GK4BS naturality square applied to `ρ ≫ σ` is then expressed as a **true pasted square**: the two actual natural-transformation components at G (and at the observed compatible image of G) compose vertically, and the **entire adjointified unit NatTrans** commutes with the composite target change. A parallel theorem pastes the corresponding square of the whole genuine compatible-category counit at arbitrary H.

This does not replace arrows by raw Type-valued source comparison cells.

## Horizontal composition and interchange

For actual `ρ:R⟶R'` where `R,R':T⥤U`, and `σ:Q⟶Q'` where `Q,Q':U⥤V`, the genuine Mathlib interchange is

```text
whiskerRight ρ Q ≫ whiskerLeft R' σ
  = whiskerLeft R σ ≫ whiskerRight ρ Q'.
```

GK4BT proves that these **two horizontal pasting presentations yield literally equal WHOLE target-action NatTrans**, independently on the attained-AH functor category and on the actual AH-compatible full subcategory. It also proves the full unit and counit target-square statements after horizontal pasting, with the actual original dependent F45 Hom maps and Mathlib whiskering. The resulting laws combine vertical and horizontal target naturality rather than inventing a global Gray structure.

## Choice-based inverse: natural-isomorphic, not definitionally strict

GK4BQ already proves a genuine Mathlib natural isomorphism

```text
κ_T : Q_T ≅ P_T.
```

GK4BP proves the strict whole-Mathlib-functor target-change equation **for the explicit inverse only**:

```text
R_*^Comp ⋙ P_U = P_T ⋙ R_*^A.
```

For every true target functor `R:T⥤U`, GK4BT uses **whiskering of the actual κ natural isomorphisms**, followed by `eqToIso` of GK4BP's proved strict square, to construct:

```text
nativeGK4BTChosenInverse_targetNatIso :
  (R_*^Comp ⋙ Q_U) ≅ (Q_T ⋙ R_*^A).
```

The comparison is a bona fide **whole Mathlib NatIso**, not an asserted equality of the choice-based inverse functors. The next theorem explicitly verifies naturality of this comparison on **every actual morphism of Comp_T**, i.e. original source functor natural transformations, not merely a selected generator.

This is a bounded target-functor transport result. GK4BT does **not** yet assert coherence of the comparison as `R` itself varies through `ρ:R⟶R'`; that target-NatTrans compatibility is a distinct next obligation.

## All eleven axiom-audited declarations

1. `nativeGK4BTAttainedNat_id` — attained target-action identity.
2. `nativeGK4BTAttainedNat_comp` — attained target-action vertical composition.
3. `nativeGK4BTCompatibleNat_comp` — compatible target-action vertical composition.
4. `nativeGK4BTUnit_vertical_pasting` — whole adjusted unit vertical square for ρ followed by σ.
5. `nativeGK4BTCounit_vertical_pasting` — whole compatible counit vertical square.
6. `nativeGK4BTAttained_horizontal_interchange` — actual whole attained target NatTrans interchange.
7. `nativeGK4BTCompatible_horizontal_interchange` — actual whole compatible target NatTrans interchange.
8. `nativeGK4BTUnit_horizontal_square` — whole adjusted unit under genuine horizontally pasted target transformations.
9. `nativeGK4BTCounit_horizontal_square` — whole compatible counit under the horizontal target transformation.
10. `nativeGK4BTChosenInverse_targetNatIso` — whole natural-isomorphism transport of the arbitrary GK4BM chosen inverse under target R.
11. `nativeGK4BTChosenInverse_targetNatIso_naturality` — naturality on all true compatible functor Homs.

## Authority, explicit exclusions, and GK4BU frontier

**Proved:** whole target-NatTrans vertical/horizontal pasting coherence of the actual GK4BQ adjusted unit and counit, and an honest target-change NatIso for the arbitrarily selected GK4BM inverse, natural in each compatible functor H.

**Not proved or implied:** strict target postcomposition **equality** for the arbitrary GK4BM inverse; the target-`ρ` coherence between two transported chosen-inverse comparisons; unconditional original S faithfulness; original Q category laws; raw F54/F55/P92B Type-valued 3-cells; ambient integer matrix reachability; blanket 14D Countable/19D fillers; global strict Gray or hyperdescent.

**Next GK4BU:** certify the diagram expressing how the chosen-inverse comparison NatIso changes under **target natural transformations** `ρ:R⟶R'`, and test identity, vertical composition, two-step target composition and horizontal interchange of these comparisons. Derive it from GK4BQ's genuine κ and GK4BP/GK4BO exact target naturality; any dependent transports must be written explicitly, not replaced by fake source 3-cells.

Lean v4.30.0-rc2; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public root107. Protected validation-only PR #1558 remains Draft/OPEN/unmerged. Strict 空 center; independent Kuu one presentation; no Gray. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

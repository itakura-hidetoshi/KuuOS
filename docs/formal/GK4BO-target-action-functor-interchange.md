# F112-P94D3GK4BO — Functorial target action and genuine natural-transformation interchange

2026-11-01 JST. **[Theorem PR #2873](https://github.com/itakura-hidetoshi/KuuOS/pull/2873) MERGED.** This is an append-only exact-source proof record following GK4BN and not a replacement for the canonical theorem source.

## Exact theorem, Git tree and CI

- [Complete GK4BO Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BOTargetActionFunctor.lean): **one new 240-line Lean file**, 12 declared definitions/theorems and 12 explicit `#print axioms` receipts.
- Final source HEAD `83bfde427ef364647863278a895c6c7d5ac14c77`; test-merge commit `f8772428faebd26217bed45235293213ad173cd2`; **exactly the same tree** `b6e5f2e5d3b70b9ad130529de2011b85c721d71a` on both commits (GitHub MCP independently fetched both Git commit objects).
- [CI run #41275594655](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41275594655): **Strict Lean 3810/3810 SUCCESS**, Governance gate terminal SUCCESS, Independent Kuu core SUCCESS and Workflow consolidation integrity SUCCESS.
- Every GK4BO axiom receipt is within `propext`, `Classical.choice`, `Quot.sound`. **sorryAx0**, changed Lean errors/warnings **0/0**. No axiom or sorry was added.
- Squash merge `57a089b6a22d38cf0c707973aa81671aaaf2f1df`, confirmed as canonical main HEAD immediately after theorem integration.
- Initial [CI run #41275398351](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41275398351) reported two tactic errors in the new file's functor category-law fields: after `apply NatTrans.ext`, the target is an equality of `.app` functions, **not a universally quantified proposition**. Replacing `intro H` with `funext H` in both `map_id` and `map_comp` proves pointwise extensionality without changing statements or weakening assumptions. The entire file and imports were revalidated at the exact corrected source HEAD.

## Actual source geometry and bounded categorical claim

Let `S = NativeGK4IStage` be the original independent, fully F45-dependently typed structural category, `A = NativeGK4BFAttainedAHStage` the **actually attained** old-AH matrix category, and `F = nativeGK4BJStructuralAHFunctor : S ⥤ A` the proved observer. GK4BK constructs the unique compatible factorization through F; GK4BL descends real natural transformations; GK4BM proves the category equivalence

```text
Fun(A,T) ≌ FullSubcategory (original-AH-kernel-compatible Fun(S,T)).
```

GK4BN establishes genuine postcomposition for arbitrary target functors and genuine target natural transformations on that exact full subcategory, together with a strictly commuting GK4BM forward square. It does **not** claim that S and A themselves are equivalent.

GK4BO takes all those **existing proven actions** and constructs one actual pinned-Mathlib functor for any target categories T and U:

```lean
nativeGK4BOTargetActionCompatible :
  (T ⥤ U) ⥤
    (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
     NativeGK4BMCompatibleFunctorCategory (T := U) p ma mb pa pb)
```

It sends `R : T ⥤ U` to the exact GK4BN compatible postcomposition functor, and `ρ : R ⟶ R'` to the previously constructed genuine compatible natural transformation. **Both functor laws** are proved in Mathlib, not asserted. They imply strict identities and vertical compositions of natural transformations:

```text
Action.map (𝟙 R) = 𝟙 (Action.obj R)
Action.map (ρ ≫ σ) = Action.map ρ ≫ Action.map σ.
```

The attained-AH-side action is `Functor.whiskeringRight` itself. GK4BO proves equality of whole natural transformations in the GK4BM **forward** comparison square, using the genuine original F45 observation.

## Two-stage target interchange

For actual target functors `R,R' : T ⥤ U`, `Q,Q' : U ⥤ V` and natural transformations `ρ : R ⟶ R'`, `σ : Q ⟶ Q'`, the target actions on compatible full-subcategories satisfy Mathlib's **true interchange law**. In conventional right-to-left notation this compares the two pastings

```text
whiskerRight(Action.map ρ, Action.obj Q) ≫
  whiskerLeft(Action.obj R', Action.map σ)

  =

whiskerLeft(Action.obj R, Action.map σ) ≫
  whiskerRight(Action.map ρ, Action.obj Q').
```

The proof uses the real `Functor.whiskerLeft_comp_whiskerRight` theorem. The action also preserves the strict target identity and two-stage target functor composition already proved by GK4BN. This constitutes bounded 1-categorical functoriality and interchange for genuine functor categories and their NatTrans Homs; it is **not** an assertion of global Gray coherence or raw F54 higher-cell filling.

## All 12 new Lean declaration receipts

1. `nativeGK4BOTargetActionCompatible`: one true target-action Mathlib Functor with both laws.
2. `nativeGK4BOTargetActionAttained`: pinned Mathlib whiskeringRight on attained AH functors.
3. `nativeGK4BOTargetActionCompatible_obj`: exact GK4BN object action.
4. `nativeGK4BOTargetActionCompatible_map`: exact GK4BN target NatTrans action.
5. `nativeGK4BOTargetActionAttained_obj`: exact attained object action.
6. `nativeGK4BOTargetActionAttained_map`: exact attained NatTrans action.
7. `nativeGK4BOTargetActionCompatible_map_id`: natural-transformation identity.
8. `nativeGK4BOTargetActionCompatible_map_comp`: natural-transformation vertical composition.
9. `nativeGK4BOForward_targetNat_square`: true whole-NatTrans forward GK4BM naturality.
10. `nativeGK4BOTargetAction_interchange`: two-stage natural-transformation interchange.
11. `nativeGK4BOTargetAction_strict_id`: strict target functor identity.
12. `nativeGK4BOTargetAction_strict_comp`: strict target functor composition.

## Authority boundaries and GK4BP frontier

**Proved:** a true target-action functor, identities and vertical composition, strict forward equivalence comparison, and genuine natural-transformation interchange over the original compatible full subcategory and actually attained AH data.

**Not proved or implied:** unconditional original S faithfulness, original Q category laws, raw Type-valued F54/F55/P92B higher witnesses or filler, an equivalence S ≌ A, all ambient integer matrices, universal 14D countability or 19D fillers, global strict coherence, Gray reconstruction or higher hyperdescent. No claim is made that the arbitrarily chosen quasi-inverse from `asEquivalence` commutes definitionally with all target functors.

**Next GK4BP research:** study coherent comparison for the **explicitly constructed GK4BK chosen factorization** and its natural-transformation descent under target transformations, including exact compatibility with the GK4BM unit/counit where legitimately derivable. Distinguish strict equations for explicit factorization from weaker coherent comparison isomorphisms for an arbitrary quasi-inverse; do not silently upgrade either to global higher descent.

Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, public roots 107, protected validation-only PR #1558 Draft/OPEN/unmerged. Strict 空 center and independent Kuu as one presentation. Append-only/tighten-only/overwrite-forbidden/same-root; no Gray reintroduction.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

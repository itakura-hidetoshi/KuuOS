# F112-P94D3GK4BN — Target postcomposition naturality for the genuinely attained AH observer

2026-11-01 JST. **[Theorem PR #2871](https://github.com/itakura-hidetoshi/KuuOS/pull/2871) MERGED.** This is an append-only exact-source proof record, not a replacement for the canonical main theorem carrier.

## Exact theorem source and CI

- [Complete GK4BN Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BNTargetPostcompositionNaturality.lean): one new formal file with **18 declarations** (each explicitly `#print axioms`).
- Final exact source HEAD `80bb2b64931a6f13107c089949856b7c3f0ac971`; test-merge HEAD `1fe834d5115d39560153f2fed4eee71695386e33`; **identical Git tree** `e05c0f8bae3ba05ea38e7e81a6c4954883a0f1d8`.
- [CI #41270237079](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41270237079): **Strict Lean 3809/3809 SUCCESS**, **Governance terminal SUCCESS**, independent Kuu foundation + workflow integrity SUCCESS; 18 axiom receipts within `propext`, `Classical.choice`, `Quot.sound`; **sorryAx0**, changed Lean errors/warnings **0/0**.
- Theorem squash and canonical main HEAD at integration: `17a4b3e291d54ebd49b8e3bada589f5cab186b65`.
- The [first CI #41269992709](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41269992709) found a single Lean dependent-type mismatch: a morphism in the genuine `ObjectProperty.FullSubcategory` was compared with an underlying natural transformation. This did not justify weakening any theorem. The fix is the correct `.hom` projection on that subcategory morphism. The **complete file**, pinned imports, dependent signatures, full source and final `#print axioms` were rechecked at exact source HEAD in successful CI #41270237079.

## Genuine original source geometry and target functors

`S = NativeGK4IStage` is the **independently sourced and fully dependent original F45 structural category**, not the original P92B witness-existence quotient Q or the raw Type of F54 histories. `A = NativeGK4BFAttainedAHStage` is the actual category of original **attained** AH matrices, never all ambient integer matrices. `F = nativeGK4BJStructuralAHFunctor : S ⥤ A` is the proved object- and Hom-surjective genuine observer. GK4BK proves exact kernel-compatible factorization of S→T functors, GK4BL proves full faithfulness for natural transformations, and GK4BM constructs the actual equivalence

```text
Fun(A,T) ≌ Fun_AH-compatible(S,T)
```

of **actual Mathlib functor categories**, with `Fun_AH-compatible` implemented as a true `ObjectProperty.FullSubcategory` of `S ⥤ T`. Its objects are only functors killing the exact original structural S-side old-AH observation equality kernel.

For arbitrary genuine target Mathlib categories `T,U` and **any** target functor `R : T ⥤ U`, GK4BN proves that if `H : S ⥤ T` is compatible, then `H ⋙ R : S ⥤ U` is also compatible, without requiring R itself to be faithful. This constructs an ACTUAL functor

```lean
nativeGK4BNPostcompCompatible (R : T ⥤ U) :
  Fun_AH-compatible(S,T) ⥤ Fun_AH-compatible(S,U)
```

via pinned `ObjectProperty.lift`. Its object action is literally `H.obj ⋙ R`; its morphism action is `Functor.whiskerRight η.hom R` on genuine underlying natural transformations. Inclusion of the full subcategory commutes with this target postcomposition as an **equality of entire Mathlib functors**.

## Exact strict precomposition square

Let `R_*^A : Fun(A,T) ⥤ Fun(A,U)` be the original pinned Mathlib right-whiskering postcomposition; let `R_*^{comp} : Fun_AH-compatible(S,T) ⥤ Fun_AH-compatible(S,U)` be the new compatible lift; let `C_T` and `C_U` be the genuine GK4BM precomposition equivalence forward functors. GK4BN proves the **strict** whole-functor square

```text
R_*^A ⋙ C_U = C_T ⋙ R_*^comp
```

as `nativeGK4BNPostcomp_precomposition_square`, comparing **both** original F45 typed functor objects and their real natural-transformation Hom maps, not just an isomorphism of bare values. In ordinary right-to-left composition notation the equation is `C_U ∘ R_*^A = R_*^comp ∘ C_T`.

The original GK4BK explicitly constructed factor functor is also strictly compatible with target postcomposition:

```text
Factor(H ⋙ R, kernelPreserved) = Factor(H) ⋙ R.
```

This is a theorem about the **actual GK4BK chosen factor**, not an unsupported claim that every arbitrary quasi-inverse functor supplied by `asEquivalence` is definitionally target-natural.

## Naturality in target natural transformations and coherence

For every **genuine** target natural transformation `ρ : R ⟶ R'`, GK4BN constructs an actual natural transformation between the compatible postcomposition functors

```lean
nativeGK4BNPostcompCompatibleNat ρ :
    postCompCompatible R ⟶ postCompCompatible R'
```

whose component at H is the genuine underlying `Functor.whiskerLeft H.obj ρ`. The proof of **naturality on arbitrary original compatible-source natural-transformation Homs** uses pinned Mathlib's genuine interchange theorem `Functor.whiskerLeft_comp_whiskerRight`, without manufacturing a raw F54/F55 Type-valued 3-cell.

The target ρ square is proven as a real **equality of whole natural transformations** `nativeGK4BNPostcomp_nat_square` (and by an explicit underlying-component equality `nativeGK4BNPostcomp_nat_square_app`). The original GK4BL inverse natural-transformation descent is also proven **strictly** stable under R by `nativeGK4BNNatTransLift_postcompose`.

Finally `nativeGK4BNPostcompCompatible_id` and `nativeGK4BNPostcompCompatible_comp` establish genuine target identity and two-step target composition coherence as equations of full Mathlib functors. This is a precise bounded 1-categorical functor/natural-transformation result, **not** a higher pseudofunctor or Gray strictness claim.

## All 18 Lean declaration receipts

1. `nativeGK4BNCompatible_postcompose`: exact structural AH kernel compatibility is preserved by arbitrary R.
2. `nativeGK4BNPostcompAttained`: pinned Mathlib target postcomp on actual AH-image functors.
3. `nativeGK4BNPostcompStructural`: pinned target postcomp on original structural functors.
4. `nativeGK4BNPostcompCompatible`: true functor of compatible full subcategories.
5. `nativeGK4BNPostcompCompatible_obj`: unchanged original typed source-side target action.
6. `nativeGK4BNPostcompCompatible_map`: actual right-whiskering of natural transformations.
7. `nativeGK4BNPostcomp_inclusion`: exact inclusion/postcomposition whole-functor equality.
8. `nativeGK4BNPostcomp_precomposition_square`: exact GK4BM forward equivalence square.
9. `nativeGK4BNPostcomp_precomposition_obj`: original typed AH/structural object action.
10. `nativeGK4BNFactorFunctor_postcompose`: explicit GK4BK inverse factor commutes strictly with R.
11. `nativeGK4BNPostcompCompatibleNat`: actual natural transformation for target ρ with proven interchange.
12. `nativeGK4BNPostcompCompatibleNat_app`: exact original source functor component.
13. `nativeGK4BNPostcompAttainedNat`: pinned target natural transformation on AH functors.
14. `nativeGK4BNPostcomp_nat_square_app`: the concrete subcategory underlying transformation equation.
15. `nativeGK4BNPostcomp_nat_square`: equality of WHOLE target-natural-transformation squares.
16. `nativeGK4BNNatTransLift_postcompose`: the actual GK4BL inverse transformation commutes with R.
17. `nativeGK4BNPostcompCompatible_id`: strict identity law on target.
18. `nativeGK4BNPostcompCompatible_comp`: strict composition law on target functors.

## Authority, exclusions, and next frontier GK4BO

**Confirmed:** functorial target postcomposition, exact compatibility, exact natural-transformation squares, strict identities/composition and selected factor-naturality over ACTUALLY attained AH-image data. This does **not** identify independent S with K_AI or A, assert unconditional original S Hom faithfulness, prove unfilled original F54/F55/P92B Type-valued source 3-cells, make original Q a Category, reach all ambient integer matrices, establish unconditional 14D Countable or 19D fillers, or derive global strict/hyperdescent.

**GK4BO proposal:** package the proven target action of functors and natural transformations into a **single explicit Mathlib functor on the target functor category**, and prove its strict 2-functoriality at the target-natural-transformation level (identity, vertical composition, interchange) relative to GK4BM's forward equivalence; separate it from the merely chosen quasi-inverse coherence. This is bounded naturality mathematics, not an unproved higher-dimensional descent or Gray reconstruction.

Lean `v4.30.0-rc2`; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107. Protected validation-only PR #1558 remains Draft/OPEN/unmerged. Strict 空 center; independent Kuu one presentation; no Gray reintroduction. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

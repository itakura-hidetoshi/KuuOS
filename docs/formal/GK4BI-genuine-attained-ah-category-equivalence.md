# F112-P94D3GK4BI — actual Mathlib category equivalence: K_AI ≌ attained old AH matrices

**2026-11-01 JST — [theorem PR #2861](https://github.com/itakura-hidetoshi/KuuOS/pull/2861), MERGED.**

## Source of theorem authority

- [Complete Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BIAttainedAHCategoryEquivalence.lean) (one new Lean file, 14 declarations).
- Authoritative canonical main after the theorem merge: `87f60307fc1441a8d7a8040758e9271f65ca3283` (squash SHA).
- Validated exact source HEAD `e880646a2811e98ffc6cb04436520cdc7b4bd952`; GitHub test-merge HEAD `99e46f575cec532700870f7b4112d6a9c0092518`; their **identical Git tree** is `2d2e043b69a2f09f98196a0dc4a3826ccf7e1b04`.
- [Exact-source CI #41263880913](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41263880913): Strict Lean **3804/3804 SUCCESS**, Governance **terminal SUCCESS**, independent Kuu and workflow-integrity checks SUCCESS.

## Precise mathematical result

GK4BF constructed a **genuine Mathlib Category** `NativeGK4BFAttainedAHStage` from the existing second-kernel `NativeGK4AIKernelStage` by taking the old AH matrices **actually reached** by its source Homs, with an original, genuine dependent F45 boundary-object presentation. GK4BH proved that old AH observation is injective on every original typed K_AI Hom, and GK4BF already gave Hom surjectivity. Those proofs produce true Hom bijections, not a guessed equivalence with all integer matrices.

GK4BI now proves the actual bundled `CategoryTheory.Equivalence`

```lean
nativeGK4BIAttainedAHEquivalence
```

between the **existing** K_AI category and the category of **genuinely attained** old AH integer matrices. Its forward functor is definitionally equal to the preexisting `nativeGK4BFImageFunctor`, as checked by `nativeGK4BIAttainedAHEquivalence_functor`; no replacement category or new quotient is introduced.

### Formal construction, all 14 declarations

1. `nativeGK4BIObjectEquiv`: literal object Equiv between the two wrappers over the **same original F45 boundary**.
2. `nativeGK4BIHomEquiv`: `Equiv.ofBijective` of the genuine old-AH image map on each typed Hom, from GK4BH bijectivity.
3. `nativeGK4BIHomInverse`: inverse Hom map on the existing K_AI **quotient classes**, not on original unquotiented F54 paths.
4. `nativeGK4BIMap_homInverse` and `nativeGK4BIHomInverse_map`: two-sided actual Hom inversion equations.
5. `nativeGK4BIFullyFaithful`: explicit fully faithful structure from those inverse maps.
6. `nativeGK4BIImage_obj_surjective`: true literal object surjectivity, not merely an unsupported essential-surjectivity assertion.
7. `nativeGK4BIImageIsEquivalence`: pinned Mathlib full/faithful/essential-surjectivity class.
8. `nativeGK4BIAttainedAHEquivalence`: genuine bundled Mathlib equivalence obtained via `Functor.asEquivalence`.
9. `nativeGK4BIAttainedAHEquivalence_functor`: original forward functor identity.
10. `nativeGK4BIReverseFunctor`: genuine inverse Mathlib Functor whose composition and identity preservation are provided by the constructor and verified by Lean.
11. `nativeGK4BIUnitIso` and `nativeGK4BICounitIso`: true natural isomorphisms, not merely equality of values.
12. `nativeGK4BI_triangle`: the actual Equivalence triangle identity for every K_AI source object.

This construction is stronger than Hom bijectivity alone: it supplies the required object mapping and coherence at the category level. Its forward functor is the same actual-image functor as before; the inverse is Mathlib's proof-derived quasi-inverse.

## Verification and Lean4 error correction

Initial [CI #41263705865](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41263705865) detected a **Lean4 declaration-transparency restriction**, not an obstruction to the mathematical equivalence:

```text
Definition 'nativeGK4BIImageIsEquivalence' of class type
must be marked with '@[reducible]' or '@[implicit_reducible]'
```

The whole new Lean source and its pinned Mathlib definitions were inspected; the class-valued definition was tightened with `@[implicit_reducible]`, retaining the remaining proof terms. The corrected [CI #41263880913](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41263880913) compiled **3804/3804 jobs successfully**. All 14 `#print axioms` results are within `propext`, `Classical.choice`, `Quot.sound`; `nativeGK4BIObjectEquiv` specifically needs **no axioms**. No `sorryAx`, new-file Lean warning or error. One changed Lean file. Governance terminal SUCCESS before the squash merge.

## Scope and remaining obstructions

**Proved:** the K_AI second-kernel stage is categorically equivalent to its **actually attained** old AH image, with real functors and natural unit/counit. The equivalence describes this exact quotient-level categorical presentation.

**Not proved or implied:** equivalence with the ambient category of all integer matrices, original raw Type-valued F54 route equality, faithfulness of independent structural `S -> K_AI`, original Q associativity/unit or category laws, unconditioned original 14D Countable, the 19D filler, global strict higher categorical coherence or hyperdescent. Their obstructions and authority boundaries remain separate.

Formal pin: Lean v4.30.0-rc2; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107 unchanged. `#1558` Lean4.31 validation-only PR remains Draft/OPEN/unmerged. Strict 空 central; independent Kuu is one presentation; Gray not reintroduced. Append-only / tighten-only / overwrite-forbidden / same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

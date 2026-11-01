# F112-P94D3GK4BK — Universal factorization through the genuinely attained old-AH image

2026-11-01 JST. **[Theorem PR #2865](https://github.com/itakura-hidetoshi/KuuOS/pull/2865) MERGED**. This is an exact-source proof record; the authority is the canonical `main` Lean source, not this prose or a CI badge.

## Canonical proof and verification

- [Complete GK4BK Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BKUniversalAHFactorization.lean): one new Lean file, **14 declarations** and their `#print axioms` receipts.
- Final source HEAD `2aec9d7e09d70c2cee938387345a6b4a80841faa`; test-merge HEAD `9760cb4dd85798d55d7b40eaa8ad833310a0e151`; **identical Git tree** `97a9a139e87794c5803b6654a9e9441f0638cb03`.
- [CI #41267046208](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41267046208): **Strict Lean 3806/3806 SUCCESS**, Governance **terminal SUCCESS**, independent Kuu foundation and workflow integrity SUCCESS.
- Final squash and theorem canonical `main` HEAD at merge: `693ffe9acd64fea561d7058b844e85ee2d869609`.
- All **14** `#print axioms` declarations depend on no axioms beyond `propext`, `Classical.choice`, `Quot.sound`; **sorryAx0**, changed-file Lean errors/warnings **0/0**. Historical failed attempts are not evidence of a verified theorem.

## Genuine categorical statement, with correct direction of composition

Use the EXISTING independent genuine F45-typed structural Mathlib category
`S = NativeGK4IStage` and the EXISTING genuinely attained old-AH matrix category
`A = NativeGK4BFAttainedAHStage`. The actual full and object-surjective GK4BJ functor is

```lean
F := nativeGK4BJStructuralAHFunctor
-- F : S ⥤ A
```

For **any** target Mathlib category `T`, and **any** genuine functor `H : S ⥤ T`, define compatibility with the original S-side old-AH observation kernel on **every original dependent F45 typed Hom**:

```text
forall X Y : S, forall u v : X ⟶ Y,
  nativeGK4AHStructuralValue X Y u =
      nativeGK4AHStructuralValue X Y v
    -> H.map u = H.map v.
```

GK4BJ proves this kernel is **exactly** the kernel of `F.map`. GK4BK proves:

```text
AHKernelCompatible H  ↔  ∃ G : A ⥤ T, F ⋙ G = H
```

and, more strongly, whenever compatibility holds,

```text
∃! G : A ⥤ T, F ⋙ G = H.
```

The equality is **strict equality of whole Mathlib functors**, not only equality on individual matrices or a natural-isomorphism slogan. In standard mathematical notation the direction is `H = G ∘ F`.

## The 14 actual Lean declarations

1. `nativeGK4BKAHKernelCompatible`: exact source S/AH kernel condition, with no identification of raw source histories.
2. `nativeGK4BKCompatible_iff_imageKernel`: S-side old-AH kernel iff actual GK4BJ functor map kernel.
3. `nativeGK4BKPreimage`: choose an actual **structural S quotient Hom class** realizing each actually attained AH image; not a raw F54 route inverse.
4. `nativeGK4BKPreimage_spec`: chosen source class has exactly the specified reached AH matrix.
5. `nativeGK4BKLiftHom`: target morphism obtained by the actual H of a structural quotient preimage.
6. `nativeGK4BKLiftHom_independent`: any two actual S preimages of the same reached matrix have equal H-values, using **explicit kernel compatibility**.
7. `nativeGK4BKLiftHom_on_source`: image of each actual structural Hom maps to its original target H-value.
8. `nativeGK4BKFactorFunctor`: genuinely constructed Mathlib Functor with proven `map_id` and `map_comp`.
9. `nativeGK4BKFactor_map`: map-level factorization on every typed structural quotient Hom.
10. `nativeGK4BKFactor_functor`: **strict equality of the entire composite and H**; object and morphism laws are simultaneously handled.
11. `nativeGK4BKKernelNecessary`: any such categorical factorization necessarily kills the original AH kernel.
12. `nativeGK4BKFactor_exists_iff`: necessity and sufficiency of the kernel-compatibility condition.
13. `nativeGK4BKFactor_unique`: every other exact factor functor equals the constructed one, using GK4BJ literal object-surjectivity and Hom-surjectivity.
14. `nativeGK4BKFactor_existsUnique`: full `∃!` categorical universal factorization.

## Lean4 error analysis and correction

The complete 339-line new source was retained, alongside its imports and dependent-signature obligations. Multiple exact-source CI attempts isolated these **elaboration and transport** problems; none justified weakening any theorem:

- Initial [CI #41266048523](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41266048523): a goal `f ≫ g = f ≫ g` remained after rewriting two preimage-spec lemmas; closed by reflexivity. The first `Functor.ext` and functor-equality rewriting also failed on dependent `eqToHom` transports.
- [CI #41266256882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41266256882): the reflexive composition proof and equality elimination succeeded; only `Functor.ext` transport remained.
- [CI #41266529723](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41266529723): unfolding/simplifying generic `Functor.ext` still left `eqToHom` transports in the arbitrary target category.
- [CI #41266742688](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41266742688): explicitly providing `Functor.ext`'s object-equality proof did not eliminate those transports.
- **Final [CI #41267046208](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41267046208):** used the **pinned Mathlib** theorem `Functor.toPrefunctor_injective` and the pinned `Prefunctor.ext (fun X => rfl)` to reconstruct the same **whole-functor equality**, avoiding the unneeded generic categorical `eqToHom` coercions. Scoped Lean 3806/3806 SUCCESS and all 14 axiom checks standard-three-only, sorryAx absent.

The fix is an exact mathematical equality proof on the same functors, not a replacement by a weaker natural-isomorphism result.

## Authority boundary and GK4BL frontier

**Proved:** ordinary 1-categorical universal descent from the existing S category onto the **actually attained** AH quotient, including compatibility iff existence and strict uniqueness. It does not prove faithfulness of S→K_AI or S→attained AH, and it does not identify original raw Type-valued F54 routes or fill missing F55/P92B witnesses. The original Q category axioms, arbitrary ambient integral-matrix reachability, unconditional genuine 14D Countable, 19D fillers, global strict higher categories and hyperdescent remain separate, unproved research targets. This result is **not** a statement about high-dimensional hyperdescent.

Next proposed **GK4BL**: extend universal descent from functor **objects** to **natural transformations**, preserving original typed object boundaries, and formalize the induced fully faithful relationship between `Functor(A,T)` and the subcategory of AH-kernel-compatible `Functor(S,T)`, with all 2-dimensional naturality obligations explicit. Do not conflate this with source higher-cell completion.

Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public root107. Protect validation-only PR #1558 Draft/OPEN/unmerged. Strict 空 central; independent Kuu one presentation; no Gray reintroduction. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

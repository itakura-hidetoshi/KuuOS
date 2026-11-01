# F112-P94D3GK4BL — Genuine natural-transformation descent and fully faithful precomposition

2026-11-01 JST. **[Theorem PR #2867](https://github.com/itakura-hidetoshi/KuuOS/pull/2867) MERGED.** This is a formal proof and CI receipt; the authoritative source is canonical main and its actual Lean theorem types, not a narrative or badge.

## Exact canonical proof and validation

- [Complete new GK4BL Lean file](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BLNaturalTransformationDescent.lean), **14 declarations**.
- Final exact-source HEAD `552ceba6d198ae5dea904f54180eec8fc06837ff`, test-merge HEAD `2cc93f9a9999ef2a5ec0f6595b276e82f25ba14f`; their **identical Git tree** `bd5c5b367fee25b02d0b748dc1be835cd17b6a6e`.
- [CI #41268260288](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41268260288): **Strict Lean 3807/3807 SUCCESS**, **Governance terminal SUCCESS**, independent Kuu core and workflow integrity SUCCESS. All 14 `#print axioms` declarations have dependencies within `propext`, `Classical.choice` and `Quot.sound`; **sorryAx0**, changed-file Lean error/warning **0/0**.
- Theorem squash SHA and main HEAD at theorem integration: `de974ee81059215aab4e32ea74c2ced273d1284c`.

## Correct categorical scope

Let `S = NativeGK4IStage` be the existing independent structural witness-existence quotient Mathlib category retaining its genuine fully dependent original F45 endpoints, and let `A = NativeGK4BFAttainedAHStage` be the existing category of **actually reached** original integer AH matrices. GK4BJ supplies the true `F : S ⥤ A`, provably surjective on objects and every typed Hom, with exact equality kernel given by original structural AH observation. GK4BK already proves universal unique factorization of AH-kernel-compatible functors `H : S ⥤ T` into arbitrary Mathlib target category `T`.

GK4BL advances to **natural transformations**. For arbitrary genuine functors `G,H : A ⥤ T`, define the existing pinned Mathlib precomposition functor by

```lean
nativeGK4BLPrecomposition :
    (A ⥤ T) ⥤ (S ⥤ T)
-- obj G = F ⋙ G (usual mathematics: G ∘ F)
-- map α = Functor.whiskerLeft F α.
```

The principal proven statement is the full and faithful property of this genuine precomposition functor:

```text
Nat(G,H) ≃ Nat(F ⋙ G, F ⋙ H).
```

The right-hand composition is **G after F** (and H after F). This is a bijection on every natural-transformation Hom, **not** a theorem asserting that `F` itself is faithful or that `S ≌ A`.

For a source natural transformation `η : (F ⋙ G) ⟶ (F ⋙ H)`, construct a true Mathlib natural transformation `η̄ : G ⟶ H` with

```text
η̄.app X := η.app X.original.
```

The naturality condition is proven on **every genuinely attained** AH morphism `f : X ⟶ Y`: take the actual structural quotient Hom preimage `s` supplied by GK4BK, apply the source square `η.naturality s`, then use its certified image equation `F.map s = f`. This uses no new Type-valued F54 witness, artificial cell or proof-synthetic path.

The two exact inverse equations are

```lean
nativeGK4BLWhisker_lift
nativeGK4BLLift_whisker
```

and the pinned Mathlib `Functor.FullyFaithful` construction is

```lean
nativeGK4BLPrecomposition_fullyFaithful
```

Natural-transformation identity and vertical composition preservation by inverse descent are proved by `nativeGK4BLNatTransLift_id` and `nativeGK4BLNatTransLift_comp`; equality of the induced Hom Equiv with the pinned Mathlib FullyFaithful Hom Equiv is also formalized.

Finally, `nativeGK4BLPrecomposition_obj_image_iff` and `nativeGK4BLPrecomposition_obj_unique` connect this natural-transform full-faithfulness with GK4BK's earlier universal factorization: a source functor H is literally in the precomposition object image if and only if it kills the true original AH kernel, and in that case the factorization functor object is **strictly unique**.

## All fourteen verified Lean declarations

1. `nativeGK4BLPrecomposition` — actual Mathlib functor between genuine functor categories.
2. `nativeGK4BLPrecomposition_obj` — exact object action by composing functors.
3. `nativeGK4BLPrecomposition_map` — map of natural transformations by pinned `whiskerLeft`.
4. `nativeGK4BLNatTransLift` — explicit descent and naturality on actual attained AH Hom.
5. `nativeGK4BLNatTransLift_app` — true original F45 stage component formula.
6. `nativeGK4BLWhisker_lift` — inverse law on source natural transformations.
7. `nativeGK4BLLift_whisker` — inverse law on attained AH transformations.
8. `nativeGK4BLNatTransEquiv` — all-Hom natural transformation Equiv.
9. `nativeGK4BLPrecomposition_fullyFaithful` — genuine Mathlib FullyFaithful.
10. `nativeGK4BLNatTransLift_id` — inverse preserves identity.
11. `nativeGK4BLNatTransLift_comp` — inverse preserves vertical composition.
12. `nativeGK4BLPrecomposition_homEquiv` — exact pinned FullyFaithful Hom Equiv agreement.
13. `nativeGK4BLPrecomposition_obj_image_iff` — literal image objects iff original AH kernel compatibility.
14. `nativeGK4BLPrecomposition_obj_unique` — actual unique factor functor object from GK4BK.

## Authority and next frontier

**GK4BL proves ordinary functor-category naturality and full faithfulness under precomposition with the genuine structural AH observer.** The original S→K_AI faithfulness and original S→AH faithfulness, source raw F54 route equality, unfilled original F55/P92B Type-valued cells, original Q category axioms, unattained ambient integer matrices, unconditional 14D Countable, 19D fillers, global strict higher coherence and hyperdescent remain separate and unproved. This is not a claim of an actual higher-category or hyperdescent theorem.

**Next suggested GK4BM:** package GK4BK's exact object image and GK4BL's natural-transform full faithfulness as a true **Mathlib category equivalence** between `A ⥤ T` and the **full subcategory of AH-kernel-compatible** functors `S ⥤ T`, preserving typed object boundaries and all naturality components. It must not assert an equivalence with the ENTIRE `S ⥤ T` functor category absent compatibility, or a source S≌A equivalence.

Pinned Lean `v4.30.0-rc2`; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107. Protected validation-only PR #1558 remains Draft/OPEN/unmerged. Strict 空 central; independent Kuu one presentation; Gray non-reintroduced. Append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

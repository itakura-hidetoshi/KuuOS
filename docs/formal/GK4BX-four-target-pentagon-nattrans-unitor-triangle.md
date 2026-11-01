# F112-P94D3GK4BX — four-target pentagon naturality and genuine unitor/triangle coherence

**Date:** 2026-11-01 JST  
**Theorem PR:** [#2891](https://github.com/itakura-hidetoshi/KuuOS/pull/2891) — MERGED  
**Theorem squash / canonical main HEAD at merge:** `19058c78848ffa1198f1f1ea52889ab3b97c1970`  
**Source HEAD:** `c1e5376acd72e85792efdd08b4b0be7dcfa1fe58`  
**GitHub test-merge commit:** `85149ae8920de7add72e9e44ac238daa66fb8537`  
**Identical source and test-merge Git tree:** `5a7e38f4c37b8e9687930e58a66f5a31e5cf10bc`  
**Exact-source CI:** [#41299912825](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41299912825) — SUCCESS.

## Authoritative formal source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK4BXChosenInversePentagonNaturalityUnitorTriangle.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BXChosenInversePentagonNaturalityUnitorTriangle.lean)

Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. The file imports GK4BW. Its dependent signatures trace through GK4BV's real two-stage comparison, GK4BU's true target-NatTrans modification, GK4BT's chosen-inverse NatIso, and the unchanged earlier actual F45/AH source and attained-image constructions.

## Proven mathematics (15 public declarations)

Let `Q_T` be GK4BM's arbitrarily selected inverse, `P_T` GK4BP's explicit inverse, and `κ_T : Q_T ≅ P_T` GK4BQ's comparison. Neither their strict identity nor strict target variation of `Q_T` is assumed. GK4BT constructs a genuine whole Mathlib NatIso `Θ_R : C_R ⋙ Q_U ≅ Q_T ⋙ A_R`.

1. **Simultaneous four-target transformation.** For genuine `ρ : R ⟶ R'`, `σ : S ⟶ S'`, `τ : L ⟶ L'`, `υ : M ⟶ M'`, `nativeGK4BXTargetNat_fourHorizontal` constructs the true horizontal composite `ν : (R ⋙ S ⋙ L ⋙ M) ⟶ (R' ⋙ S' ⋙ L' ⋙ M')`, using actual Mathlib whiskering and vertical composition.
2. **All five genuinely pasted pentagon paths.** `nativeGK4BXChosenInverse_four_pathA_square` through `_pathE_square` prove, for each `K ∈ {A,B,C,D,E}`, the whole NatTrans equality `(C_ν ▷ Q_X) ≫ Θ_K'.hom = Θ_K.hom ≫ (Q_T ◁ A_ν)`. Each argument rewrites the real GK4BW `Θ_K = Θ_(R⋙S⋙L⋙M)` and applies the existing GK4BU whole square; no new raw higher cells are created.
3. **Pentagon-natural-transformation coherence.** `nativeGK4BXChosenInverse_four_pentagon_leftNatTrans` and `_rightNatTrans` show that the left-hand and right-hand whole NatTrans paste results of all five paths coincide. This is whole NatTrans equality, not just the existence of commuting componentwise diagrams.
4. **Actual left and right unitors.** `nativeGK4BXChosenInverse_leftUnitor_square` and `_rightUnitor_square` relate GK4BW's genuine binary pasting with `Functor.leftUnitor R` and `Functor.rightUnitor R` and prove their whole target modification squares.
5. **Associator–unitor triangle.** `nativeGK4BXTargetNat_associatorUnitor_triangle` proves the whole-NatTrans equation
   `whiskerRight (rightUnitor R).hom S = (associator R (𝟭 U) S).hom ≫ whiskerLeft R (leftUnitor S).hom` inside the actual Mathlib functor category.
6. **Middle-unit mixed coherence.** `nativeGK4BXChosenInverse_middleUnit_threeLeft_eq_direct` and `_threeRight_eq_direct` identify both genuinely pasted three-stage chosen comparisons with the direct comparison after middle-unit insertion. `nativeGK4BXChosenInverse_triangle_left_square` and `_triangle_right_square` transport the two sides of the real triangle through the whole GK4BU modification.

## Exact-source verification and axiom audit

- GitHub source HEAD `c1e5376acd72e85792efdd08b4b0be7dcfa1fe58` and GitHub test-merge `85149ae8920de7add72e9e44ac238daa66fb8537` have identical Git tree `5a7e38f4c37b8e9687930e58a66f5a31e5cf10bc`.
- Strict Lean **3819/3819 SUCCESS**.
- Independent Kuu core/public API **SUCCESS**; Workflow consolidation integrity **SUCCESS**; Governance terminal **SUCCESS**.
- Changed Lean file: **15 public declarations / 15 `#print axioms`**. The logs list only `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` and zero Lean error/warning. GitHub Actions framework may emit unrelated deprecation warnings.
- Append-only one-file theorem PR. No deletion or change of previous proof files. Root remains 107 and validation-only PR #1558 remains Draft/OPEN/unmerged.

## What is NOT proved

The original F45 source S is not claimed unconditionally faithful; source-Q laws are not supplied; raw F54/F55/P92B higher Type-valued cells, full integer-matrix attainability, global Gray category, and unlimited higher hyperdescent are NOT derived. The chosen `Q_T` is never identified definitionally with `P_T`. The results concern existing Mathlib functor categories only. Strict 空 is central, with independent Kuu as one presentation.

## Future research boundary

A possible GK4BY continuation is naturality of inverse unitors, expanded mixed polygon/unit coherence for arbitrary positions of inserted identities, or a more uniform finite-stage coherence principle, subject to Lean and exact-source verification. No general higher coherence may be asserted from this finite GK4BX result alone.

**Historical policy:** previous README/ROADMAP entries are preserved. Documentation is synchronized through a separate docs-only PR; Strict Lean is intentionally skipped for docs-only changes.

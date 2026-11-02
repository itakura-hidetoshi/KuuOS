# F112-P94D3GK5Q — Genuine sequential/composite category-equivalence comparison for typed finite paths

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2929](https://github.com/itakura-hidetoshi/KuuOS/pull/2929) — MERGED  
**Final exact-source HEAD:** `7cfc57438469d1cd65935fd5320bb80186f67ded`  
**Theorem squash/main:** `602ee6495da908a0bd499b939396036fd2e6f777`  
**Exact source/squash Git tree:** `50212fa5169cbe8e4c332a7eb670236b29f21b52` (identical, independently fetched by GitHub git/commits API)  
**Exact-source CI:** [#41382919068](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41382919068) — terminal SUCCESS.

## Scope and new append-only Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5QCompositeEquivalenceInterchange.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5QCompositeEquivalenceInterchange.lean) is a new standalone append-only Lean4 source (228 lines). It imports the certified GK5P proof chain and pinned Mathlib's `Equivalence`, `EqToHom`, `Whiskering`, and `Tactic`; all prior source modules remain unchanged.

Fix a family of genuinely different categories `C D E : I → Cat.{vC,uC}`, with actual bundled Mathlib equivalences `e : ∀ i, C i ≌ D i` and `g : ∀ i, D i ≌ E i`. The true composite is Mathlib `(e i).trans (g i)`, whose forward functor is `(e i).functor ⋙ (g i).functor` and inverse is `(g i).inverse ⋙ (e i).inverse`. This is **not** a postulated strict inverse, and no nontrivial units/counits are erased.

For an original whole functor `R : C i ⥤ C j`, the two composite actions are related by the authentic Mathlib whole NatIso:

```lean
nativeGK5QAtomComparison e g R :
  nativeGK5GChangeAtom g (nativeGK5GChangeAtom e R) ≅
  nativeGK5GChangeAtom (fun k : I => (e k).trans (g k)) R
```

This is `eqToIso` of the explicitly proved `Functor.assoc` equality between the two functor expressions. It is a real category-theoretic NatIso, but does **not** claim a separate nontrivial modification between recursively assembled `Φ` comparisons.

## Eleven public declarations and their precise strength

1. `nativeGK5QChangeAtom_comp`: exact whole functor equality obtained from actual Mathlib equivalence composition and `Functor.assoc`.
2. `nativeGK5QAtomComparison`: genuine whole Mathlib `NatIso` for the atomic sequential/composite change.
3. `nativeGK5QChangeWord_comp`: strict equality of two dependently typed finite word transports.
4. `nativeGK5QChangeTree_comp`: strict equality of two dependently typed finite binary tree transports, retaining units and indexed contexts.
5. `nativeGK5QChangeTreeLeaves_comp`: whole ordered typed leaf-word preservation under equivalence composition.
6. `nativeGK5QTreeComparison`: actual whole Mathlib `NatIso` from the proven equality of evaluations of the two transformed trees.
7. `nativeGK5QAtomComparison_eqToIso_square`: the genuine atomic comparison commutes with transporting every equality-induced whole NatIso; no local coherence hypothesis.
8. `nativeGK5QAtomComparison_path_square`: applies the above to each real GK5D proof-relevant finite path's `PathIso` via GK5D's certified `PathIso = eqToIso PathEq` theorem.
9. `nativeGK5QAllFinitePaths_composition_square`: WHOLE Mathlib NatIso square comparing the two-stage and single-stage transformed finite path NatIso values along the canonical `nativeGK5QTreeComparison` endpoints. All `refl/basic/reverse/trans` paths are covered.
10. `nativeGK5QAllFinitePaths_composition_natTrans`: exact hom-projected whole Mathlib NatTrans equation.
11. `nativeGK5QNormalization_composition_square`: the actual GK5D normalization path satisfies the same whole NatIso square.

The finite path comparison square is

```lean
nativeGK5DPathIso
  (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
    nativeGK5QTreeComparison e g b =
nativeGK5QTreeComparison e g a ≪≫
  nativeGK5DPathIso
    (nativeGK5GChangePath (fun k : I => (e k).trans (g k)) q)
```

## Full-file Lean4 diagnosis and structural fix

Three earlier attempts at proving `nativeGK5QAtomComparison_eqToIso_square` failed during pinned Strict Lean elaboration. The final diagnosis inspected the entire new Lean file, its imports, full relevant GK5D/GK5G/GK5P definitions, pinned Mathlib `Equivalence.trans`, `Whiskering.lean`, `EqToHom.lean` and Lean4 Tactic Reference, rather than only treating one error line.

1. **Equation elimination does not by itself normalize real whiskering.** `cases h` changes `eqToIso h` into a reflexive `Iso`, but the nested expression `nativeGK5GChangeIso g (nativeGK5GChangeIso e (Iso.refl R))` still consists of a genuine right iso-whiskering inside a genuine left iso-whiskering. A single `simp only` over the original definition left this whole expression unreduced.
2. **The relevant fixed mathlib lemmas are actual Iso equalities.** `Functor.isoWhiskerRight_refl`, `Functor.isoWhiskerLeft_refl`, `Iso.refl_trans` and `Iso.trans_refl` must be matched at the correct nested level. `change` is used only for the definitionally equal unfolding of `nativeGK5GChangeIso`, not to assert any associativity or nonstrict compositor equality.
3. **The final repair introduces a real typed intermediate lemma.** Private `nativeGK5QChangeIso_refl` unfolds `ChangeIso` at its actual indexed source/target and proves it maps a real `Iso.refl R` to a real `Iso.refl (ChangeAtom e R)` by the two fixed mathlib iso-whiskering identity laws.
4. **The main proof applies this lemma at all three exact types.** After `cases h` and `eqToIso_refl`, it rewrites first for `e,R`, then for `g,ChangeAtom e R`, and finally for `e.trans g,R`. The remaining square closes with the genuine `Iso.refl_trans` and `Iso.trans_refl` laws. No lemma was replaced by a weaker statement, no selected inverse was identified strictly with another one, and no `sorry` or `admit` remains.
5. **The other ten public declarations were read as complete typed statements, not just their CI diagnostic lines.** The finite path coherence depends on the certified full path denotation `nativeGK5DPathIso_eqToIso`. This is a special property of GK5D's specified finite rewrite calculus and is not an assertion about arbitrary, unrelated higher cells.

Upstream pinned sources: [Mathlib Whiskering](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [Equivalence](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [EqToHom](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Lean4 Tactic Reference](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference).

## CI, axiom and authority receipt

Final exact-source [CI #41382919068](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41382919068) completed terminal SUCCESS in all required jobs: **Strict Lean 3838 / 3838 SUCCESS**, Independent Kuu core/retained API SUCCESS, Workflow consolidation integrity SUCCESS, Governance gate and audit summary SUCCESS. The final 11/11 public `#print axioms` records contain **only** `propext`, `Classical.choice`, `Quot.sound`; **sorryAx 0**, no additional axioms. The changed Lean file has **zero errors/warnings**.

Source `7cfc57438469d1cd65935fd5320bb80186f67ded`, squash `602ee6495da908a0bd499b939396036fd2e6f777` and matching tree `50212fa5169cbe8e4c332a7eb670236b29f21b52` were independently verified. The pinned environment is Lean `v4.30.0-rc2` and mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Public root 107, same-root/append-only/tighten-only/overwrite-forbidden, strict 空 center and independent Kuu as one presentation are retained. Protected validation-only PR #1558 remains Draft/OPEN/unmerged.

## Exact remaining obstruction and next candidate GK5R

Prove a **new, genuine nonstrict comparison** between `nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t)` pasted with the recursively changed `Φ_e(t)` and `nativeGK5GChangeTreeIso (e.trans g) t` for all finite typed trees, including both actual unit/counit and binary `ChangeCompIso` coherences. GK5Q's structural `eqToIso` endpoint comparison is *not* that stronger result; no Gray/hyperdescent is inferred. Source-Q axioms, raw F54/F55/P92B Type high cells, the original unconditional F45 faithfulness, global Gray reconstruction and unrestricted hyperdescent remain outside the current theorem.

Docs only: Strict Lean must be **SKIPPED** in a subsequent documentation PR, while independent core, workflow integrity and governance are still required.

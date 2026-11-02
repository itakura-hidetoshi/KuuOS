# F112-P94D3GK5S — Atomic genuine recursive Phi coherence and exact unit/cons normal-form obstruction criterion

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2933](https://github.com/itakura-hidetoshi/KuuOS/pull/2933) — MERGED  
**Final exact-source HEAD:** `c0654eddf52b5f63d4d647aba79238155a4aa820`  
**Theorem squash/main:** `9c705a0d21aed2bee51c4d82b1d0d0d08bab0283`  
**Independently matching source/squash Git tree:** `71e00d954a725d79160c10656a54473662bd67d1`  
**Exact-source CI:** [#41386958561](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41386958561) — terminal SUCCESS, Strict Lean **3840/3840**.

## Mathematical boundary and canonical Lean file

The new append-only source [PolygonNativeC60AQFullPentagonPhysicalNativeGK5SAtomicPhiNormalFormCriterion.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5SAtomicPhiNormalFormCriterion.lean) has 195 lines, importing the certified GK5R obstruction and pinned actual Mathlib Equivalence/Whiskering.

Fix genuine indexed category families `C D E : I → Cat.{vC,uC}` and real Mathlib pointwise category equivalences `e : ∀ i, C i ≌ D i`, `g : ∀ i, D i ≌ E i`. GK5R already constructed two distinct, **genuine recursively composed whole Mathlib NatIso** comparisons from sequential change to one-stage `e.trans g`, and their relative automorphism obstruction `Ω_t`. GK5S does not identify quasi-inverse functors or their nontrivial unit/counit strictly, and it does not postulate `Ω_t = identity` for all trees.

## Proven results

### Unconditional compatibility at each typed atomic tree

`nativeGK5SChangeIso_refl` proves that the real whole Mathlib `ChangeIso_e` sends a genuine `Iso.refl R` to the genuine `Iso.refl (ChangeAtom_e R)` by using the actual `Functor.isoWhiskerRight_refl` and `Functor.isoWhiskerLeft_refl` laws.

`nativeGK5SAtomPhi_compatible` proves, for every actual Mathlib functor `R : C i ⥤ C j`, the equality of the two complete nonstrict recursive Phi compositions at the *typed atomic tree*:

```lean
nativeGK5RSequentialCompositePhi e g (.atom R) =
  nativeGK5RDirectCompositePhi e g (.atom R)
```

The proof keeps the real GK5Q `eqToIso` associativity comparison and genuine GK5G whole Phi values. There is **no** residual unit or compositor hypothesis on this atomic case. `nativeGK5SAtomObstruction_refl` then concludes that the real target-valued whole NatIso `Ω_(atom R)` is actually `Iso.refl`, using GK5R's certified equality/obstruction equivalence.

### Sharp necessary-and-sufficient criterion for all finite typed trees

Three explicit **Prop definitions**, not assertions that those Props hold, make the remaining obligation precise:

1. `NativeGK5SAllTreeCoherent e g`: both actual recursive Phi comparisons agree for every finite heterogeneous typed tree.
2. `NativeGK5SUnitCoherent e g`: equality of the actual recursive Phi comparisons on `unit i` for every index i, retaining the true counit/transpose-composite witnesses.
3. `NativeGK5SConsCoherent e g`: for every typed atom `R : C i ⥤ C j` and every complete dependent word `w : NativeGK5DTypedWord C j k`, **assuming the equality already holds on its genuine right-associated tail** `TreeOfWord w`, the equality also holds on `paste (atom R) (TreeOfWord w)`. This is a precise conditional compositor compatibility predicate, not an added axiom.

`nativeGK5SNormalWords_of_unit_cons` proves the genuine dependent word induction: these two conditions imply coherence on *every right-associated typed word*, using only the true `empty/cons` constructors.

`nativeGK5SAllTrees_of_unit_cons` then invokes GK5R's **already proved** actual finite-path normal-form obstruction iff to extend the result to *every finite typed binary tree* without further conditions.

`nativeGK5SAllTrees_iff_unit_cons` proves the non-vacuous exact equivalence

```lean
NativeGK5SAllTreeCoherent e g ↔
  NativeGK5SUnitCoherent e g ∧ NativeGK5SConsCoherent e g
```

and `nativeGK5SAllObstructions_iff_unit_cons` establishes the identical criterion for *universal vanishing of the actual target-valued whole NatIso obstruction* `Ω_t = Iso.refl`.

**This is a reduction theorem, not a claim that the unit/cons hypotheses are already satisfied.** The remaining unit/counit and compositor comparison must be proved with genuine Mathlib witnesses separately. The conditions are neither generalized to arbitrary changing universes nor passed off as unrestricted descent.

## Complete-source Lean4 diagnosis of initial elaboration failures

The initial PR #2933 CI failed only at the atomic whole Phi proof: its automatic `simp only` had two residual goals, while the other public declarations already reached sound standard-axiom auditing. The final fix followed review of the entire new source, imported GK5R/GK5Q/GK5G/GK5D theorem signatures, the real recursive tree evaluation, and pinned Mathlib `Whiskering.lean`, `EqToHom.lean`, `Equivalence.lean`, `Iso.lean`.

1. The recursive GK5G atom `Phi` is `Iso.refl`, but the inner `Functor.isoWhiskerRight` and outer `Functor.isoWhiskerLeft` around its transported whole NatIso do **not** disappear from the pretty-printed elaboration goal merely because the raw original tree is `atom R`. Their identity laws were explicitly factored as `nativeGK5SChangeIso_refl`. The final proof unfolds the actual recursive Phi, then rewrites the real change-Iso identity and uses `Iso.refl_trans`.
2. The remaining target equality retained the full spelling `nativeGK5DTreeComposite (NativeGK5DTypedTree.atom R)` and changed tree functors. `simp only` without the actual evaluation/tree definitions left a residual reflexive `Iso` composition. The final proof unfolds both `nativeGK5GChangeTree` and `nativeGK5DTreeComposite` and applies the true `Iso.refl_trans`/`Iso.trans_refl` groupoid laws.
3. GK5Q's tree comparison and atom comparison are equal at an actual `atom` after evaluating the dependent tree constructors; the proof uses the genuine proof-irrelevant associativity equality under `eqToIso`, not a fabricated natural transformation or a selected inverse made strict.
4. The infinite-looking all-tree claim is reduced only via the existing **finite**, proof-relevant GK5D normalization path. The implication from right-associated words to arbitrary trees depends on a certified GK5R path equivalence and does not introduce a new source-Q faithfulness assumption.
5. All previous source files are intact; the new file contains no `sorry` or `admit`, and no theorem hypothesis was weakened.

Fixed upstream references: [Mathlib Whiskering](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [Iso](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean), [EqToHom](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean).

## CI and authority receipt

Final source HEAD `c0654eddf52b5f63d4d647aba79238155a4aa820` passed exact-source [CI #41386958561](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41386958561) terminal SUCCESS: **Strict Lean 3840/3840**, Independent Kuu core/retained proof API SUCCESS, workflow consolidation integrity SUCCESS, governance gate and audit summary SUCCESS. All **10/10** new public `#print axioms` records cite **only** `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` 0; error/warning 0/0.

The source and squash commits share the independently checked Git tree `71e00d954a725d79160c10656a54473662bd67d1`. Fixed **Lean v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, same-root/append-only/tighten-only/overwrite-forbidden, strict 空 centered, independent Kuu one presentation, protected validation-only PR #1558 Draft/open/unmerged.

## Next exact obstruction — GK5T candidate

Prove the actual `NativeGK5SUnitCoherent e g` by the non-strict `(e.trans g).counitIso` formula and real Mathlib triangle laws. Separately prove `NativeGK5SConsCoherent e g` using the actual `nativeGK5GChangeCompIso` middle unit naturality and the two recursive Phi witnesses on a canonically right-associated cons tree. Once both theorems pass pinned Lean, GK5S supplies universal `Ω_t = Iso.refl` *without requiring any new structural induction*. Until then, universal vanishing is explicitly unproved. Original raw F54/F55/P92B Type high cells, source-Q category axioms, F45 unconditional faithfulness, Gray and unrestricted hyperdescent remain excluded.

Docs-only workflow should SKIP Strict Lean; independent Kuu/workflow integrity/governance must be checked separately.

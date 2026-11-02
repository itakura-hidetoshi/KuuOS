# F112-P94D3GK5U — Genuine binary compositor exchange and unconditional recursive Φ composition for all finite typed trees

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2937](https://github.com/itakura-hidetoshi/KuuOS/pull/2937) — MERGED  
**Final exact-source HEAD:** `3b078d6b0b3b3c8bdb80e755fbbebb2664a092fd`  
**Theorem squash/main SHA:** `4ba30b8f560a101f4c08ee7891a0e34f7ccadc38`  
**Independent source/squash Git tree:** `4c1dcaed25133bdfc1201f3b6c2ebd1808286e96` (exact match via GitHub git/commits API).  
**Exact-source CI:** [#41397903337](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41397903337) — terminal SUCCESS.

## Definitive mathematical result and scope

The new append-only [PolygonNativeC60AQFullPentagonPhysicalNativeGK5UBinaryCompositorExchange.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5UBinaryCompositorExchange.lean) contains **388 lines**. Only this new source file was changed in theorem PR #2937. No historical Lean definitions, imports, old hypotheses or signatures were weakened or overwritten.

For *genuine* indexed Mathlib category equivalences `e : ∀ i, C i ≌ D i` and `g : ∀ i, D i ≌ E i`, compare the **whole Mathlib NatIso** obtained by (a) changing the actual GK5G recursively assembled Phi first by e and then by g, pasting the real GK5Q atomic `Theta`, and (b) changing by the actual Mathlib composite `(e i).trans (g i)`, pasting GK5Q's real typed-tree comparison.

The fully unconditional theorem

```lean
nativeGK5UAllTrees_unconditional :
    NativeGK5SAllTreeCoherent e g
```

proves these two **genuine recursive whole NatIso** pastings agree for *every finite heterogeneously typed functor tree*. This includes all actual `.unit`, `.atom` and `.paste` cases, not only one or two atomic leaves. The matching theorem

```lean
nativeGK5UAllObstructions_refl :
  ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
    nativeGK5RPhiObstruction e g t = Iso.refl _
```

eliminates GK5R's actual target-valued relative automorphism obstruction for **all** such trees. Thus GK5T's formerly unproved necessary-and-sufficient remaining condition is now discharged **unconditionally**:

```lean
nativeGK5UNonemptyCons :
  NativeGK5TNonemptyConsCoherent e g
```

The proof preserves the actual selected quasi-inverses, nontrivial units/counits, genuine GK5G middle-unit compositor, and fully typed intermediate categories. It does **not** strictify equivalences. It does not settle original source-Q category axioms, raw F54/F55/P92B Type-valued higher cells, unconditional F45 faithfulness, global Gray reconstruction, arbitrary changing-universe chains, or unrestricted hyperdescent.

## Mathematical construction: whole-NatIso pasting rather than expansion

The file introduces a **private**, fully typed genuine horizontal Mathlib NatIso pasting operation `nativeGK5UHorizontalIso` and proves its transitivity law `nativeGK5UHorizontalIso_trans` and equality-induced comparison `nativeGK5UHorizontalEqToIso` using actual Mathlib functoriality and Iso groupoid laws.

The eleven published declarations certified by `#print axioms` are:

1. `nativeGK5UTheta_paste`: whole GK5Q structural tree `eqToIso` comparison is compatible with horizontal whole-NatIso pasting, not an unauthorized identity of recursively assembled Phi.
2. `nativeGK5USequentialPhi_paste`: the genuinely sequential GK5R recursive Phi at an arbitrary `paste left right` equals the horizontal pasting of its two genuine child comparisons followed by the actual Mathlib composite-equivalence `ChangeCompIso`.
3. `nativeGK5UDirectPhi_paste`: the independently constructed direct `(e.trans g)` recursive Phi has **the same** whole-NatIso pasting formula, using GK5Q's tree comparison and actual `Iso.trans`.
4. `nativeGK5UBinaryCompositor_whole`: direct whole-NatIso exchange between the real two-stage GK5G binary compositor and the true `Equivalence.trans` compositor for any typed `R : C_i ⥤ C_j`, `S : C_j ⥤ C_k`. Actual intermediate units/counits remain.
5. `nativeGK5UAllTrees_unconditional`: by finite dependent-tree recursion, actual unit Phi coherence from GK5T, atomic Phi coherence from GK5S, and both proven binary pasting formulas establish full nonstrict recursive Phi equality for **all** finite typed trees.
6. `nativeGK5UAllObstructions_refl`: deduces universal whole-NatIso obstruction triviality from GK5R's certified necessary-and-sufficient criterion.
7. `nativeGK5UNonemptyCons`: discharges GK5T's remaining `NativeGK5TNonemptyConsCoherent` **without** introducing any local condition.
8. `nativeGK5UTwoLeafObstruction_refl`: entire GK5D finite rewrite class with the exact ordered two-leaf dependent word has trivial obstruction.
9. `nativeGK5UTwoLeafPhi_compatible`: corresponding genuine whole-NatIso Phi equality for any such two-leaf presentation.
10. `nativeGK5UTwoAtomPhi_compatible`: actual atomic binary tree's sequential/composite recursive Phi equality.
11. `nativeGK5UTwoAtomObstruction_refl`: corresponding actual whole-NatIso obstruction equals `Iso.refl`.

The **private** `nativeGK5UGenericPaste` handles any two recursive subtrees simultaneously, using GK5L's genuine two-variable compositor whole-NatIso naturality, the real GK5Q atomic comparison, and the preceding binary compositor exchange. This is the real recursive induction bridge, not an identity obtained by replacing nontrivial middle units with reflexivity.

## Exact full-file Lean4 elaboration failures, root causes and final repair

All **388 lines** of the changed source, full imports, GK5G's `ChangeCompIso` and actual recursive `ChangeTreeIso`, GK5I component formulas, GK5K/GK5L two-variable naturality, GK5Q structural tree comparison, GK5R obstruction and finite-path descent, GK5S normal-form criterion, GK5T true unit/counit comparison and pinned Mathlib API signatures were examined. Intermediate failing CI runs were not treated as mathematical success, and source edits retained the full strength of the theorem.

1. **Initial recursive paste attempt:** expanding `ChangeTreeIso` at components with `simp` produced a huge residual goal involving genuine right-child NatTrans naturality, `g.unitIso.inv` naturality at the intermediate typed category, and functor map/whiskering interchange. The child recursion hypotheses are equalities of **whole NatIsos**, not substitutes for naturality. Trying to close a horizontal composition using only componentwise simplification left an unsolved goal.
2. **Lean4 tactic syntax:** splitting `simp [...] at hleft hright ⊢` across lines in the wrong location produced `expected '*' or checkColGt`. Fixing whitespace made the *real* algebraic obstruction visible; syntax changes alone were insufficient.
3. **Structural proof:** introduce a genuine horizontal NatIso, prove its transitivity using Iso composition, and use the pinned Mathlib whiskering interchange/associator laws (see below). Apply certified GK5L two-variable compositor naturality as a **whole NatIso equation**, then the independently proven local genuine `nativeGK5UBinaryCompositor_whole`. This yields a true general paste theorem `nativeGK5UGenericPaste` for arbitrary typed subtree comparisons, rather than only two atoms. Its composition is not a new raw source higher cell.
4. **Direct recursive Phi last error:** a subsequent CI on `nativeGK5UDirectPhi_paste` reported a single entire goal with identical whiskered NatIso composition on both sides, but the right side used the still-opaque **private `nativeGK5UHorizontalIso` definition**. Lean's `simp only` does not automatically unfold unlisted constants. The final change explicitly added `nativeGK5UHorizontalIso` to that `simp only` list. This is an appropriate *definitional* unfolding; by contrast, GK5Q's genuine `eqToIso` or GK5G's nontrivial unit/compositor were **not** replaced with `rfl`.
5. **Final induction:** `nativeGK5USequentialPhi_paste` and `nativeGK5UDirectPhi_paste` now both typecheck as genuine whole Mathlib NatIso equalities. Finite typed tree induction rewrites the two formulas and uses both actual recursive child hypotheses, closing all constructors. There are **no `sorry`, `admit`, `sorryAx`, added axioms or weakened hypotheses**.

Authoritative fixed mathlib references:
[Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean),
[Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean),
[EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean),
[Iso.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean),
and [official Lean4 Tactic Reference](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference).

The relevant Mathlib laws are genuine `Functor.isoWhiskerLeft_trans_isoWhiskerRight`, `Functor.isoWhiskerLeft_twice`, `Functor.isoWhiskerRight_twice`, `Functor.isoWhiskerRight_left`, `Functor.isoWhiskerLeft_right`, `Iso.trans_assoc` and equality-induced NatIso functoriality. Do not confuse *definitional* functor association with nonstrict comparison Iso equality.

## Independent authority and CI receipt

The exact source `3b078d6b0b3b3c8bdb80e755fbbebb2664a092fd` passed [workflow #41397903337](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41397903337), all selected jobs terminal SUCCESS:

- **Strict Lean 3842/3842**: new file built successfully with `warningAsError` and `sorryAsError`.
- **11/11 public `#print axioms`**: exactly `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` **0**, changed Lean error/warning **0/0**.
- Independent Kuu core and retained public proof API **SUCCESS**; workflow consolidation integrity **SUCCESS**; governance gate and audit summary **SUCCESS**.
- Exact-source/squash Git tree `4c1dcaed25133bdfc1201f3b6c2ebd1808286e96` **identical**; theorem squash/main `4ba30b8f560a101f4c08ee7891a0e34f7ccadc38`.

Fixed Lean **v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, same-root/append-only/tighten-only/overwrite-forbidden, strict 空 centered with independent Kuu one presentation. Protected validation-only PR #1558 remains Draft/open/unmerged.

## Next exact research boundary

The finite GK5D/GK5G recursive whole-NatIso pseudofunctor **composition** obstruction is now unconditionally discharged. A potential next stage **GK5V** is to certify higher coherence of *three or more successive* actual pointwise equivalences and their Mathlib associators (pentagon-like pseudofunctor composition coherence), and separately test interaction with GK5F index relabeling. No unrestricted high-cell/Gray/hyperdescent result is inferred from this completion.

This documentation-only PR must SKIP Strict Lean while independently passing required Kuu core/workflow integrity/governance checks.

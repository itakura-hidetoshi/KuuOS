# F112-P94D3GK5X — Genuine four-equivalence pentagon and five direct-recursive-Φ relative-defect coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2943](https://github.com/itakura-hidetoshi/KuuOS/pull/2943) — MERGED  
**Final exact-source HEAD:** `c4201dd8226208582a7333b5caba21cf97d90e81`  
**Theorem squash/main HEAD:** `7261d8c309a9b700681740d81509f3e5629e780a`  
**Independently matching source/squash Git tree:** `c96a18ea74ad9864f5f084f6d8c17df215da1af2`  
**Exact-source CI:** [#41404999549](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41404999549) — terminal SUCCESS, **Strict Lean 3845/3845**, Independent Kuu, workflow integrity, Governance all SUCCESS.

## Mathematical setting: five TRUE Mathlib composite equivalences

Fix a common universe pair and actual pointwise category equivalences

```lean
e : ∀ i : I, C i ≌ D i
g : ∀ i : I, D i ≌ E i
h : ∀ i : I, E i ≌ F i
k : ∀ i : I, F i ≌ G i
```

There are five actual, independently constructed `Equivalence.trans` parentheses, with the following **pentagon orientation**:

```text
P0 = (((e trans g) trans h) trans k)
P1 = ((e trans (g trans h)) trans k)
P2 = (e trans ((g trans h) trans k))
P3 = (e trans (g trans (h trans k)))
P4 = ((e trans g) trans (h trans k))

P0 -> P1 -> P2 -> P3
P0 -> P4 -> P3
```

`nativeGK5XBracket0` through `nativeGK5XBracket4` are the **real** Mathlib equivalences. The development does **not** postulate strict equality of their full equivalence records, their chosen quasi-inverses, or their unit/counit witnesses. Each `nativeGK5XAtomEqXY` is instead a proved equality between the associated genuine conjugation **functors**, using Mathlib `Equivalence.trans_functor`, `Equivalence.trans_inverse`, and `Functor.assoc`.

The five oriented edges `nativeGK5XEdge01`, `Edge12`, `Edge23`, `Edge04`, `Edge43` are authentic **whole Mathlib NatIso** `eqToIso` witnesses of these functor equalities. Therefore the two whole-NatIso paths satisfy the **unconditional pentagon**:

```lean
nativeGK5XPentagon_whole :
  (Edge01 ≪≫ Edge12) ≪≫ Edge23 = Edge04 ≪≫ Edge43
```

`nativeGK5XPentagon_natTrans` proves its actual whole NatTrans hom version. This is an equality of **actual categorical comparison data**, not only a diagram or a statement at one selected object. It specifically establishes the **structural associativity** of the functors changed by four true equivalences, but does not conflate this with any stronger claim about their nonstrict unit/counit.

## Five independent actual direct recursive Phi witnesses

The new only-changed source is [PolygonNativeC60AQFullPentagonPhysicalNativeGK5XFourStageDirectPhiPentagon.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5XFourStageDirectPhiPentagon.lean), **476 lines**, preserving all previous Lean files and imports.

`nativeGK5XFourTree` is the *actual fourfold sequential transport* of any finite heterogeneously typed GK5D functor tree. `nativeGK5XFourTreeEq0` uses three real GK5Q dependent-tree composition equalities. The remaining `FourTreeEq1`–`FourTreeEq4` follow through separately proved atomic functor equalities and typed-tree induction, never by erasing the intermediate categories.

For each parenthesis `Pj`, `nativeGK5XDirectPhi0` through `DirectPhi4` use their **own true `nativeGK5GChangeTreeIso Pj t`** after `eqToIso` of the respective typed-tree equality:

```lean
Phi_j(t) =
  eqToIso (congrArg TreeComposite (FourTreeEq_j t)) ≪≫
    nativeGK5GChangeTreeIso (Pj) t
```

This is a schematic formula; the actual file has complete indexed signatures and concrete `nativeGK5DTreeComposite` expressions. All five direct Phi values keep the true selected quasi-inverses, unit/counit, compositors and whiskering. They are *independently* defined and are not replaced by one common sequential Phi.

Let `S_t = TreeComposite (FourTree t)` and `R_t = TreeComposite t`. For every oriented pentagon edge `i -> j`, the actual target-dependent whole NatIso edge defect is represented at the **common source** by

```text
Delta_ij(t) = (Phi_i(t) ≪≫ Edge_ij(R_t)) ≪≫ (Phi_j(t)).symm
            : S_t ≅ S_t
```

The five concrete `nativeGK5XDefect01`, `12`, `23`, `04`, `43` contain exactly those genuine values. The central all-finite-tree theorem

```lean
nativeGK5XDirectDefectPentagon_whole :
  (Defect01 ≪≫ Defect12) ≪≫ Defect23 = Defect04 ≪≫ Defect43
```

proves that the relative direct-Phi whole NatIso **defect composition is independent of the two pentagon routes**. It uses the genuine pentagon `nativeGK5XPentagon_whole`, `congrArg` under the actual start/end direct Phi values, and cancellativity of all intermediary direct Phi inverses in the actual category. The equality holds for every finite dependently typed tree, not just one 4-atom string.

The whole target-source automorphism obstruction **between the two completed defect paths** is `Iso.refl`, by `nativeGK5XDirectDefectPentagon_obstruction_refl`. The whole NatTrans equality is separately `nativeGK5XDirectDefectPentagon_natTrans`.

### Strict boundary: what has NOT been proved

The unconditional conclusion is **path independence of relative defects**, NOT their individual vanishing. It does **not** establish:

```lean
Defect01 t = Iso.refl _
Defect12 t = Iso.refl _
Defect23 t = Iso.refl _
Defect04 t = Iso.refl _
Defect43 t = Iso.refl _
```

nor strict equality of distinct Mathlib `Equivalence.trans` records. Proving all five individual direct-Phi edge coherence squares, preserving true nontrivial units/counits/compositors, is a **separate stronger obligation**. Once proved, it would upgrade this result to full four-stage pseudofunctor pentagon coherence of the independently direct Phi values. Current certified GK5X is a real but more limited structural and obstruction-pentagon theorem.

GK5X also proves none of original source-Q axioms, F45 unconditional faithfulness, raw F54/F55/P92B Type-valued higher cells, global Gray category reconstruction or unrestricted hyperdescent.

## Exact Lean4 diagnostics: full-file/whole-NatIso proof repair

Initial [CI #41404536869](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41404536869) typechecked every new parenthesization, all five `FourTreeEq` witnesses, all five independent direct Phi definitions, the structural whole NatIso pentagon, and its NatTrans corollary. It failed at the final relative-defect path comparison (**line 425**), causing temporary `sorryAx` in dependent declarations. This first CI was **NOT** accepted.

Root cause: after `simp only [Iso.trans_assoc, Iso.symm_self_id, Iso.trans_refl]`, Lean right-associated the complete five-vertex whole NatIso chain but the intermediate subterms `Phi_j.symm ≪≫ Phi_j` did not appear as matching syntactic subexpressions. Thus a mathematical groupoid cancellation had not been implemented as a valid Lean4 elaboration proof. The proof must account for the exact whole NatIso association, not simply assume `simp only` normalizes inverse pairs across arbitrary parenthesizations.

Final repair: retain `hglue := congrArg (fun α => (Phi_0 ≪≫ α) ≪≫ Phi_3.symm) pentagon` as the genuinely whole NatIso comparison. Apply `Iso.ext` and simplify the *actual hom* using `nativeGK5XDefectXX`, `Iso.trans_hom` and `Category.assoc`. This exposes the correct intermediate inverse/hom cancellation and reconstructs the exact theorem. No statement, hypothesis, unit, counit, or compositor was altered. No `sorry`, `admit` or new axioms were added.

Final exact-source [CI #41404999549](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41404999549) is **terminal SUCCESS**. `Strict Lean 3845/3845`; all **20/20 selected `#print axioms`** report only `propext`, `Classical.choice`, `Quot.sound`; **sorryAx=0**, Lean errors/warnings 0/0; Independent Kuu, workflow integrity, Governance SUCCESS. Source/squash Git tree equality was independently verified using GitHub Git commit objects.

Pinned Mathlib references: [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean).

## Canonical governance and next research

Canonical `main`, Lean **v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 center with independent Kuu a presentation; protected validation PR **#1558 Draft/open/unmerged**.

**Next GK5Y:** demonstrate each of the five authentic **individual** direct Phi edge coherence squares, exploiting GK5W three-equivalence whole NatIso associativity, GK5U two-stage recursive Phi collapse, GK5Q naturality for arbitrary whole NatIso, and genuine left/right contextual whiskering (with no unit/counit strictification). Only then claim that every `Defect_ij` equals `Iso.refl` and that GK5X's relative pentagon is the vanishing 4-stage direct Phi pentagon. Then study GK5F typed index reindexing exchange separately.

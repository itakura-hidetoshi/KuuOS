# F112-P94D3GK5W — Genuine independent direct recursive Φ coherence under three Mathlib equivalences

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2941](https://github.com/itakura-hidetoshi/KuuOS/pull/2941) — MERGED  
**Final exact-source HEAD:** `40873490bf58b87f2e5554cda8c5db9586dea5bf`  
**Theorem squash/main HEAD:** `30e4ffb22638e6834dad016265212cb4a9673016`  
**Matching source/squash Git tree:** `a8c9e05f4a6a796d9e75249fee1d80f23161e511` — verified independently from GitHub Git commit objects.  
**Exact-source CI:** [#41402574594](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41402574594) — terminal SUCCESS: **Strict Lean 3844/3844**, Independent Kuu, workflow integrity and Governance SUCCESS.

## Mathematical advance beyond GK5V

GK5V established a three-stage associativity cocycle for two GK5Q whole-NatIso routes sharing the *same* genuine sequential recursive three-stage Phi. It did not compare the independently constructed direct recursive Phi witnesses of the two true composite equivalences.

GK5W closes precisely that remaining gap. For genuine pointwise Mathlib equivalences

```lean
e : ∀ i : I, C i ≌ D i
g : ∀ i : I, D i ≌ E i
h : ∀ i : I, E i ≌ F i
```

let `Phi_left_direct(t)` be GK5G's *actual* `ChangeTreeIso` for the genuine Mathlib equivalence `((e i).trans (g i)).trans (h i)` preceded by the equality-induced whole NatIso comparing its fully changed tree with the three successive changes. Let `Phi_right_direct(t)` be independently built using `(e i).trans ((g i).trans (h i))`. Both whole NatIso witnesses retain the actual selected quasi-inverse, all nontrivial unit/counit data, real middle-unit compositor and recursively assembled whiskering.

The new certified theorem is:

```lean
nativeGK5WAllTrees_direct_assoc_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WLeftDirectPhi e g h t ≪≫
        nativeGK5VAssocAtomIso e g h
          (nativeGK5DTreeComposite t) =
      nativeGK5WRightDirectPhi e g h t
```

The canonical atom associator is GK5V's actual **whole Mathlib NatIso** `eqToIso` of a separately proved equivalence-induced **functor equality**. This is NOT an equality of the complete `Equivalence` records. The comparison works uniformly for **every finite heterogeneously typed GK5D binary functor tree**: unit, atom, paste, arbitrarily nested subtrees.

The actual target-valued difference between both sides vanishes without additional premises:

```lean
nativeGK5WDirectObstruction_refl :
  (nativeGK5WLeftDirectPhi e g h t ≪≫
    nativeGK5VAssocAtomIso e g h
      (nativeGK5DTreeComposite t)).symm ≪≫
    nativeGK5WRightDirectPhi e g h t = Iso.refl _
```

## Real proof construction

The only new Lean file is [PolygonNativeC60AQFullPentagonPhysicalNativeGK5WIndependentDirectTriplePhiCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5WIndependentDirectTriplePhiCoherence.lean), **421 lines**, 12 public audited declarations, with 1 internal equality-naturality helper and 2 structural factorization helpers. No preceding Lean file, hypothesis, theorem or history was modified.

The public declarations:

1. `nativeGK5WAtomComparison_natIso`: GK5Q's genuinely whole atomic comparator is natural with respect to an **arbitrary whole Mathlib NatIso** `α : R ≅ S`, not only equality-induced path NatIsos.
2. `nativeGK5WLeftTreeEq`: full threefold typed tree change equals the left-associated directly changed tree, by actual GK5Q tree equalities.
3. `nativeGK5WRightTreeEq`: separately proves the right-associated typed-tree equality.
4. `nativeGK5WLeftTreeIso`: real structural left whole NatIso induced by the left tree equality.
5. `nativeGK5WRightTreeIso`: independent right whole NatIso.
6. `nativeGK5WTreeAssociator_whole`: full left tree comparison followed by GK5V's evaluated-tree associator equals the right tree comparison.
7. `nativeGK5WLeftDirectPhi`: independently assembled direct GK5G recursive Phi for `(e.trans g).trans h`.
8. `nativeGK5WRightDirectPhi`: independently assembled direct GK5G recursive Phi for `e.trans (g.trans h)`.
9. `nativeGK5WLeftDirect_eq_recursive`: left direct Phi equals GK5V's left recursive three-stage Phi by GK5U twice and actual `ChangeTreeIso` equality-naturality under the third equivalence.
10. `nativeGK5WRightDirect_eq_recursive`: right direct Phi equals GK5V's right recursive route by GK5U on `(g,h)` and `(e,g.trans h)`, plus the genuinely arbitrary-whole-NatIso GK5Q atomic naturality square for `ChangeTreeIso e t`.
11. `nativeGK5WAllTrees_direct_assoc_whole`: the main direct/direct associativity theorem, combining both independent collapse proofs with GK5V's proven whole cocycle.
12. `nativeGK5WDirectObstruction_refl`: the genuine relative target whole NatIso automorphism is `Iso.refl` at every finite typed tree.

The **private** `nativeGK5WTreePhi_eqToIso_square` correctly moves the actually recursive `ChangeTreeIso` across an equality of complete, typed finite trees; after path induction, the only reflexivity simplification is for `eqToIso` and whiskering identities. No nontrivial equivalence unit/counit is strictified. Both factorization lemmas use actual `eqToIso_trans`.

## Lean4 full-file diagnosis and repair

The initial exact-source [CI #41402166599](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41402166599) failed at **line 369** of the single new Lean source. The nontrivial arbitrary-NatIso GK5Q comparison and all other declarations were elaborated, but `nativeGK5WRightDirect_eq_recursive` attempted:

```lean
simp only [Iso.trans_assoc]
rw [← hnatural]
```

The first tactic right-associated the entire chain of real whole NatIsos, so the target did **not** contain the contiguous subexpression `Theta ≪≫ ChangeIso` on which `hnatural` could rewrite. This was a **Lean elaboration/term-shape obstruction**, not a counterexample to the naturality theorem or a missing mathematical assumption. The failure also caused `sorryAx` to appear *temporarily in dependent declarations*, so this initial run was correctly treated as FAIL.

The final replacement applies `congrArg` to the certified **whole NatIso equality** `hnatural.symm` under the actual left/right surrounding whole NatIso pastes, then normalizes only `Iso.trans_assoc`:

```lean
simpa only [Iso.trans_assoc] using
  congrArg (fun β => (leftPrefix ≪≫ β) ≪≫ rightSuffix)
    hnatural.symm
```

Here `leftPrefix` and `rightSuffix` in this schematic extract are the exact, fully typed genuine subexpressions explicitly written in the committed Lean source. They are not opaque axioms or new assumptions. This preserves all actual nonstrict unit/counit and compositor terms.

The entire **421-line** changed file, its imports and the complete GK5G/H/Q/R/U/V proof interfaces were checked against fixed Lean v4.30.0-rc2 and pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; see upstream [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Iso.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean).

The subsequent exact-source [CI #41402574594](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41402574594) is terminal **SUCCESS**, Strict Lean **3844/3844**. All **12/12** public `#print axioms` depend only on **`propext`, `Classical.choice`, `Quot.sound`**, with **`sorryAx=0`, Lean errors/warnings = 0/0**. Independent Kuu, workflow integrity, Governance SUCCESS. Source/squash Git trees exactly match.

## Formal authority boundary and continuation

GK5W is for the fixed-universe genuine Mathlib pointwise equivalence families and GK5D's **finite** heterogeneously typed functor trees. It does not give strict equality of entire Mathlib equivalence records, original source-Q axioms, F45 unconditional faithfulness, raw F54/F55/P92B Type-valued higher cells, a global Gray category, or unrestricted hyperdescent.

Canonical theorem branch `main`, public root **107**, strict 空 centered, independent Kuu one presentation, append-only / tighten-only / overwrite-forbidden / same-root. Protected validation-only PR **#1558** remains Draft/open/unmerged.

**Next GK5X candidate:** four genuine composable pointwise equivalences have five parenthesizations. Prove the actual **pentagon coherence for all five *independent direct* recursive GK5G Phi values**, with genuine whole Mathlib NatIso associators and explicit pentagon edges; then separately combine with GK5F dependent index reindexing. Do not introduce raw high cells or identify nonstrict equivalence data.

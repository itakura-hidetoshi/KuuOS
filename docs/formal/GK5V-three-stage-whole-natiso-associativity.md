# F112-P94D3GK5V — Three genuine category-equivalence changes, whole NatIso triple associativity

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2939](https://github.com/itakura-hidetoshi/KuuOS/pull/2939) — MERGED  
**Final exact-source HEAD:** `10a660d4cf524e47a252cc12a3e183b54c3b4bd7`  
**Theorem squash/main SHA:** `d8c00f20f91f73731e051f4f790d9f004bf5edb6`  
**Matching exact-source/squash Git tree:** `05724aa16282a307c51e63da5a296550fe2269fe` — independently confirmed using GitHub Git commit objects.  
**Exact-source CI:** [#41400557979](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41400557979) — terminal SUCCESS; Strict Lean **3843/3843**; Independent Kuu, workflow integrity, governance **SUCCESS**.

## Definitive mathematical result and exact scope

The only changed theorem file is the new append-only [PolygonNativeC60AQFullPentagonPhysicalNativeGK5VTripleNatIsoAssociativity.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5VTripleNatIsoAssociativity.lean), **252 lines**. All previous Lean definitions and proof obligations are preserved, with no replacement, weakening or newly assumed hypothesis.

Given genuinely indexed Mathlib category equivalences

```lean
e : ∀ i : I, C i ≌ D i
g : ∀ i : I, D i ≌ E i
h : ∀ i : I, E i ≌ F i
```

the actual left- and right-associated composites `((e i).trans (g i)).trans (h i)` and `(e i).trans ((g i).trans (h i))` have **provably equal changed atom functors**, by the real Mathlib `Functor.assoc` laws for both their forward and chosen quasi-inverse functors. This does **not** assert that the complete `Equivalence` records or their nontrivial unit/counit data are definitionally equal.

The atomic triple cocycle is a **whole NatIso** identity:

```lean
nativeGK5VAtomCocycle_whole e g h R
```

It states that first comparing `e,g` and then `(e.trans g),h`, followed by the genuine left-to-right `eqToIso` associator, gives exactly the same Mathlib whole NatIso as first comparing `g,h` and then `e,(g.trans h)`. The proof uses actual `nativeGK5QAtomComparison` and `nativeGK5GChangeIso` on equality-induced NatIsos, not a fabricated strict equivalence equality.

The central all-finite-tree theorem is:

```lean
nativeGK5VAllTrees_assoc_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5VLeftPhi e g h t ≪≫
        nativeGK5VAssocAtomIso e g h
          (nativeGK5DTreeComposite t) =
      nativeGK5VRightPhi e g h t
```

Both recursive three-stage witnesses have the **same actual** `nativeGK5VThreeStageSequentialPhi` as their source: the ordered composition of the three genuine GK5G tree Phi witnesses, including all nonstrict unit/counit and compositor data. The differing bracketings concatenate the two actual GK5Q whole NatIso atomic comparisons in opposite orders. The result is the pentagon-like **three-stage associativity face** over all finite, heterogeneously typed GK5D binary trees, not only two or three atomic leaves.

`nativeGK5VLeftPhi_viaGK5U` further verifies that the left route's first pair genuinely collapses to GK5U's independently constructed **direct composite recursive Phi** (not merely an atomic equality): it uses `nativeGK5UAllTrees_unconditional e g t` and the real whole NatIso functoriality law `nativeGK5HChangeIso_trans`. This is the explicit link to certified GK5U.

**Precise remaining boundary:** GK5V does not establish equality of the complete left/right `Equivalence.trans` records, nor an independent new right-bracketed *direct* recursively constructed `Phi_(e.trans (g.trans h))` against a direct left-bracketed `Phi_((e.trans g).trans h)`. The three-stage theorem is the genuine **same sequential Phi plus two GK5Q-comparison route** coherence, with an explicit GK5U left collapse. Four-stage pentagon and full reindexing exchange remain separate targets. It does not prove raw F54/F55/P92B Type higher cells, original source-Q axioms, F45 faithfulness, global Gray, or unrestricted hyperdescent.

## The twelve public declarations and their scope

1. `nativeGK5VChangeAtom_assoc`: true atom functor associativity for both forward and inverse Mathlib functors.
2. `nativeGK5VAssocAtomIso`: actual whole atom associator `eqToIso`.
3. `nativeGK5VAtomCocycle_whole`: whole NatIso comparison cocycle for both three-stage bracketings.
4. `nativeGK5VChangeTree_assoc`: typed recursive tree association under true equivalence changes.
5. `nativeGK5VAssocTreeIso`: whole NatIso on evaluated typed-tree endpoints.
6. `nativeGK5VThreeStageSequentialPhi`: genuine threefold recursively assembled Phi with all real units.
7. `nativeGK5VLeftPhi`: left parenthesization through two actual GK5Q comparisons.
8. `nativeGK5VRightPhi`: right parenthesization through the other two comparisons.
9. `nativeGK5VAllTrees_assoc_whole`: unconditional all-finite-tree whole NatIso associativity coherence.
10. `nativeGK5VLeftPhi_viaGK5U`: genuine two-stage GK5U direct Phi collapse inside the triple left route.
11. `nativeGK5VUnit_assoc_whole`: typed unit instance.
12. `nativeGK5VPaste_assoc_whole`: arbitrary-depth binary-paste instance.

## Full-source Lean4 diagnosis and exact repair

The initial exact-source CI [#41400225737](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41400225737) compiled all other declarations but rejected the new file at **line 77** in the *private* `nativeGK5VChangeIso_eqToIso` helper. After `cases p`, Lean reported the remaining goal

```lean
Iso.refl ((h i).inverse ⋙ R ⋙ (h j).functor) =
  Iso.refl (nativeGK5GChangeAtom h R)
```

The cause is exactly a **missing definition in `simp only`**, not a mathematical counterexample: `nativeGK5GChangeAtom` expands to the displayed genuine conjugation functor but `simp only` does not unfold an unlisted name. Explicitly adding `nativeGK5GChangeAtom` to the same simplification list closes the goal. The original genuine quasi-inverses, GK5Q comparisons and Phi constructors remain unchanged. No `sorry`, `admit`, extra axiom, weakened premise or strictification was introduced.

All **252 lines** of the changed source, its imports, GK5G atom/tree and NatIso transports, GK5H iso functoriality, GK5Q atomic and tree comparisons, GK5R sequential/direct recursive Phi, GK5U unconditional whole NatIso theorem, and pinned Mathlib `Functor.assoc`/`EqToHom`/`Whiskering` API were inspected. The subsequent exact-source CI [#41400557979](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41400557979) is terminal SUCCESS. All **12/12** public `#print axioms` show only **`propext`, `Classical.choice`, `Quot.sound`**; **`sorryAx=0`**, changed Lean **errors/warnings=0/0**.

Pinned upstream references: [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean).

## Authority, governance, continuation

Fixed **Lean v4.30.0-rc2**, pinned **mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`**. Canonical `main`, public root107, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 center; independent Kuu remains a single presentation. Validation-only PR **#1558** stays Draft/open/unmerged. Docs-only sync runs the non-Lean checks while **skipping Strict Lean**.

**Next GK5W candidate:** upgrade the three-stage comparison from the shared actual sequential Phi to independent direct recursive left/right `Phi` values using genuine GK5Q naturality against arbitrary whole NatIso and GK5U on both parenthesizations; after that prove four-stage pentagon and GK5F reindexing interchange. Do not silently identify different `Equivalence` records.

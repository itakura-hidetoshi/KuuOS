# F112-P94D3GK5Z — Dependent index reclassification and transported genuine whole-NatIso direct-Φ pentagon

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2947](https://github.com/itakura-hidetoshi/KuuOS/pull/2947) — MERGED  
**Final theorem exact-source HEAD:** `3e87d8998596c810a4cc31cc544574c1ef5c478c`  
**Theorem squash/main SHA:** `18eeafd4a656b02a992feeb62f3481aa4c330371`  
**Exact-source/squash Git tree:** `39e17d0305f12b52bfdbf408d0f155e0baba610a` — exactly matching via independent GitHub Git commit object inspection.  
**Exact-source CI:** [#41411785125](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41411785125), **attempt 2 terminal SUCCESS**: Strict Lean **3847/3847**, Independent Kuu, Workflow integrity, Governance SUCCESS; first attempt was an infrastructure cache-restore failure, not an accepted Lean proof.

## Scope and genuine typed mathematical construction

Let `f : I → J` be any map of index sets, including **non-injective** maps. Fix genuinely indexed Mathlib categories `C,D,E,F,G : J → Cat` and four true equivalence families

```lean
e : ∀ j : J, C j ≌ D j
g : ∀ j : J, D j ≌ E j
h : ∀ j : J, E j ≌ F j
k : ∀ j : J, F j ≌ G j
```

and a genuinely dependent finite GK5D tree `t : NativeGK5DTypedTree (fun i : I => C (f i)) a b`. GK5F supplies an actual recursive `TreeReindex f`, which retains the original Mathlib category at each typed source and target but reclassifies all boundaries. GK5P proves the exact reindex/change exchange for one genuine equivalence. GK5Z composes that result **four times**:

```lean
nativeGK5ZFourTree_reindex :
  TreeReindex f G
    (FourTree (e ∘ f) (g ∘ f) (h ∘ f) (k ∘ f) t) =
  FourTree e g h k (TreeReindex f C t)
```

Here the displayed formula abbreviates the fully elaborated dependent Lean signature; the source file uses actual index lambdas and nonstrict Mathlib equivalences. `nativeGK5ZFourComposite_reindex` proves equality of the resulting **whole Mathlib composite functors** and `nativeGK5ZSourceIso` is its actual equality-induced **whole NatIso**, not a false strict equality of nontrivial equivalence data.

For each of the five parenthesizations P0..P4 from GK5X, `nativeGK5ZBracket0_reindex` through `Bracket4_reindex` prove the true family of composed Mathlib Equivalence.trans is preserved **pointwise** under f. Likewise `nativeGK5ZEdge01/12/23/04/43_reindex` proves that the actual whole associator NatIso at the **same genuine typed atom R : C(f i) ⥤ C(f j)** is identical under pullback. This is a carefully bounded literal equality: **it does not equate two NatIsos with untransported, propositionally equal but syntactically different evaluated-tree endpoints**. Such equality would violate Lean's index-family/universe typing.

The genuine I-indexed pullback whole Mathlib pentagon remains a theorem:

```lean
nativeGK5ZPullbackPentagon_whole
nativeGK5ZPullbackPentagon_natTrans
```

The three-edge path 01·12·23 and two-edge path 04·43 agree as **actual whole NatIso** and **whole NatTrans**, without any injectivity of f or strictifying unit/counit.

## Five genuine transported direct Phi comparisons and relative defects

GK5Y had certified five independently constructed **J-indexed direct recursive Phi** values `Phi0..Phi4` for all finite GK5D typed functor trees, with all five individual edge coherences and all five edge source-automorphism defects equal to identity.

GK5Z defines, for each q ∈ {0,...,4}, a new **whole NatIso**

```lean
nativeGK5ZTransportedPhi0
nativeGK5ZTransportedPhi1
nativeGK5ZTransportedPhi2
nativeGK5ZTransportedPhi3
nativeGK5ZTransportedPhi4
```

on the **original pulled-back fourfold changed-tree source**, as the actual `nativeGK5ZSourceIso` followed by the corresponding **independently constructed J-indexed GK5X direct recursive Phi** evaluated at `nativeGK5FTreeReindex f C t`. No two distinct chosen quasi-inverses, genuine units/counits or compositors are identified. These witnesses are not fabricated new inverses.

Their five genuine whole Mathlib NatIso edge equations are proved individually by precomposing GK5Y's certified five true direct-Phi edge squares with the equality-induced source comparison:

```lean
nativeGK5ZTransportedEdge01_whole
nativeGK5ZTransportedEdge12_whole
nativeGK5ZTransportedEdge23_whole
nativeGK5ZTransportedEdge04_whole
nativeGK5ZTransportedEdge43_whole
nativeGK5ZAllFiveEdges_reindex_whole
```

The five **actual source-valued whole NatIso defects** `TransportedDefect01/12/23/04/43` are defined separately, retaining the complete typed tree source and genuine endpoint Phi inverse. All five are proved **unconditionally** equal to `Iso.refl` by `nativeGK5ZTransportedDefectXX_refl` and the bundled `nativeGK5ZAllFiveDefects_reindex_refl`.

**Exact boundary:** The theorem constructs reindexed-source witnesses **by transporting the J-indexed direct Phi** along the genuine composite functor equality. It does **not** yet prove equality with a second, independently recursively assembled direct Phi made directly over the pulled-back **I-indexed** equivalence family. That is a separate genuinely nonstrict recursive-Phi comparison, not licensed by the structural `TreeReindex` equality alone. Nor does this claim complete equality of Equivalence.trans records or raw high cells.

## Complete new Lean source, diagnostics and verification

The only changed theorem file is [PolygonNativeC60AQFullPentagonPhysicalNativeGK5ZTypedIndexPentagonExchange.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ZTypedIndexPentagonExchange.lean), **640 lines**, **32 public declarations audited by `#print axioms`**. The prior theorem sources, assumptions and dependent interfaces remain untouched.

**Initial real elaboration failure:** In the first exact-source CI, multiple `nativeGK5DTreeComposite t` terms in the I-indexed pullback branch were elaborated against the J-indexed category family and index universe. The failing terms have the same underlying mathematical categories but `NativeGK5DTypedTree.{uI} (fun i => C(f i))` and `NativeGK5DTypedTree.{uJ} C` are not definitionally the same indexed types. The new source was reviewed as a whole, including GK5F/G/P/X/Y signatures, and the complete I-indexed source-family annotations `(C := fun x : I => C (f x))` and G-family annotations were supplied consistently throughout all affected whole-NatIso expressions.

**Second real mathematical/type boundary:** Attempting to assert a literal equality between an I-indexed pulled-back NatIso at `TreeComposite t` and a J-indexed NatIso at `TreeComposite(TreeReindex f C t)` remained ill typed: the functor arguments are propositionally equal via `nativeGK5FTreeComposite_reindex`, not definitionally interchangeable in arbitrary NatIso target types. This was repaired **without weakening the intended index exchange** by proving exact NatIso preservation for the **same typed atom** (which uses definitionally identical concrete categories), retaining separate bona fide whole EqToIso source transports for the changed whole tree, and deriving the pullback pentagon itself through GK5X's validated theorem. It never silently coerces two indexed trees, and never changes source/target universes.

**Infrastructure interruption:** The first attempt of final-source CI #41411785125 terminated during restoration of the validated parent/main Lake cache **before running the Lean check**; the associated job could not furnish a meaningful Lean compilation result. The failed jobs were rerun using GitHub Actions, preserving the **identical exact-source commit** `3e87d8998596c810a4cc31cc544574c1ef5c478c`. **Attempt 2** completed terminal SUCCESS.

**Final exact-source CI receipt:** Strict Lean **3847/3847 SUCCESS**; all **32/32 public `#print axioms`** report only `propext`, `Classical.choice`, `Quot.sound` (some need no axioms); **`sorryAx=0`**, changed Lean errors/warnings **0/0**; Independent Kuu SUCCESS; Workflow integrity SUCCESS; Governance SUCCESS. The exact-source Git tree was independently confirmed equal to the theorem squash Git tree `39e17d0305f12b52bfdbf408d0f155e0baba610a`. No `sorry`, `admit`, new axiom, weakened hypothesis or previous-source overwrite was used.

Pinned upstream Mathlib: [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean).

## Authority, governance and next formal research

Fixed **Lean v4.30.0-rc2**, pinned mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, canonical theorem branch **main**, public root **107**, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 centered, independent Kuu is one presentation; validation-only protected PR **#1558 remains Draft/open/unmerged**. Only the finite, fixed-universe GK5D typed functor-tree calculus is covered. No original source-Q axioms, unconditional F45 faithfulness, raw F54/F55/P92B Type-valued higher cells, global Gray restoration or unrestricted hyperdescent follow.

**Next GK5AA:** prove actual **whole recursive Φ** equality between GK5Z's source-transported five J-indexed direct Φ witnesses and the *separately recursively constructed* five I-indexed pullback Phi values, including true naturality under GK5F relabeling, arbitrary noninjective index maps, and all unit/atom/paste constructors. Use explicit type-correct whole EqToIso transport rather than definally identifying the universes. Then extend through index-map composition/reclassification naturality.

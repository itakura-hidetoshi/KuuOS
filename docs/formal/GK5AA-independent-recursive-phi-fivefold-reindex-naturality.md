# F112-P94D3GK5AA — True whole-NatIso naturality of recursively constructed Phi under arbitrary dependent index maps

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2949](https://github.com/itakura-hidetoshi/KuuOS/pull/2949) — MERGED  
**Final exact-source HEAD:** `f897f05521f9a22942f467b4f095a5bf5323206b`  
**Theorem squash SHA:** `337a6e73265a939e7621df4afb3d6ed2f2401907`  
**Exact-source Git tree:** `7a1d140b14be55482173f913667bb396446ef833`  
**Squash Git tree:** `51503cb71c01246306524bc6af4407f050a8c521`  
**Lean source blob SHA, identical before and after squash:** `3f28ef12dc77f456d232ac406eb4c8533a2aada2`. The two *whole repository* Git trees differ because main had concurrently gained the independently certified Qi v3.5 docs (#2951) before the GK5AA merge; a source-file blob comparison, not a false global-tree claim, certifies that the exact checked GK5AA Lean bytes were merged unchanged.
**Final exact-source CI:** [#41421856599](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41421856599) — terminal SUCCESS. Strict Lean **3848/3848**, Independent Kuu, workflow integrity and Governance SUCCESS.

## Mathematical theorem: genuinely independent recursive Phi versus transported Phi

For an *arbitrary*, including non-injective, index map `f : I → J`, let the indexed Mathlib categories be `C,D : J → Cat.{vC,uC}` and let `e : ∀ j : J, C j ≌ D j` be a genuine family of Mathlib equivalences. Each equivalence keeps its actual chosen inverse, nontrivial unit/counit and middle-unit compositor; GK5AA never replaces these by strict equality.

For **every finite heterogeneously typed GK5D functor tree** `t` over the pullback family `C ∘ f`, GK5AA constructs the true source and target whole functor equalities `nativeGK5AASingleSourceEq` and `nativeGK5AASingleTargetEq` using GK5F/GK5P's genuine reindex/change exchange. The theorem

```lean
nativeGK5AASinglePhi_reindex_whole :
  nativeGK5GChangeTreeIso (fun x => e (f x)) t ≪≫
    eqToIso (nativeGK5AASingleTargetEq f e t) =
  eqToIso (nativeGK5AASingleSourceEq f e t) ≪≫
    nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C t)
```

is a **whole Mathlib NatIso equality** comparing two *separately recursively constructed* Phi witnesses. It is not merely an equality of syntactic trees, objectwise components, or strict identifications of nontrivial equivalences. The proof is by real GK5D **unit/atom/paste structural induction**. Units use the genuine Mathlib equivalence `counitIso.symm`, while paste uses actual functor whiskerings and the middle-category `unitIso.symm` compositor.

### The previously missing five-independent-direct-Phi exchange is now proved

For the same arbitrary f, take true equivalence families `e, g, h, k` on J; GK5X/GK5Y constructed the five distinct actual parenthesizations `P0..P4` and their independently assembled whole direct recursive Phi. GK5Z had constructed a different set of witnesses, by **first building the direct Phi on J** and then transferring it along the whole EqToIso source comparison. GK5Z expressly did **not** prove that these were the Phi reconstructed directly over the pulled-back I-indexed equivalences.

GK5AA closes precisely that missing coherence square for **all five actual bracketings individually**, without a new hypothesis:

```lean
nativeGK5AAFourDirectPhi0_reindex_whole
nativeGK5AAFourDirectPhi1_reindex_whole
nativeGK5AAFourDirectPhi2_reindex_whole
nativeGK5AAFourDirectPhi3_reindex_whole
nativeGK5AAFourDirectPhi4_reindex_whole
nativeGK5AAAllFiveDirectPhi_reindex_whole
```

In mathematical shorthand, for each q = 0,1,2,3,4,

```text
Phi^I_direct(Pq, t) ≪≫ eqToIso(target-reindex-equality)
  = eqToIso(fourfold-source-equality) ≪≫
      Phi^J_direct(Pq, TreeReindex(f,t)).
```

The private `nativeGK5AAFourfoldPhiBridge` uses the already certified **single-equivalence recursive Phi naturality**, GK5Z's actual four-stage source equality, the two genuine GK5X full dependent-tree equality certificates for each Pq and the exact Mathlib `eqToIso_trans` groupoid law. Equality of two *proofs of the same typed tree-functor equality* is handled by Lean proof irrelevance, not an illicit identification of the I and J indexed tree types.

The public conjunction `nativeGK5AAAllFiveDirectPhi_reindex_whole` bundles five separately verified whole NatIso equalities. This strengthens GK5Z's **transported** five-edge pentagon to the five genuinely **independently recursive I-indexed direct Phi** values, still within the existing fixed-universe finite typed tree calculus.

## Full-file Lean4 diagnosis, pinned Mathlib API and repair

The sole theorem change is the new **455-line** file [PolygonNativeC60AQFullPentagonPhysicalNativeGK5AAIndependentPhiReindexNaturality.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AAIndependentPhiReindexNaturality.lean). Previous theorem files have not been edited. Source analysis included the complete changed file, GK5D's dependent constructors, GK5F's exact reindex, GK5G's real unit and middle-unit compositor, GK5P's change/reindex exchange, GK5X's five independently recursive Phi values, GK5Y's all-five pentagon and GK5Z's transported Phi.

The initial Lean failure exposed a missing explicit `C := fun i : I => C(f i)` family annotation and a nontrivial paste motive. Over-eager `rfl` or `simp_all` does not discharge an equality of independently built whole NatIsos. True horizontal composition naturality was formalized in the private `nativeGK5AAHorizontal_natural`; actual nonstrict compositor naturality in `nativeGK5AACompIso_natural`. A further private `nativeGK5AACompIso_index` proves equality of the genuine middle-unit compositor at the **same actual indexed categories** across I/J presentations, without asserting equivalence-record strictness.

The remaining paste equality then became the explicit composite of these two whole NatIso comparisons. Earlier source revisions failed because the source/target equality certificates (`hsource`, `htarget`) and locally bound genuine NatIso terms (`H0`, `H1`, `K0`, `K1`) required explicit alignment, and because a proof of `(H0 ≪≫ K0) ≪≫ eqToIso(PT) = eqToIso(PS) ≪≫ (H1 ≪≫ K1)` does not syntactically match a differently bracketed final goal until Mathlib **`Iso.trans_assoc`** is applied. The final repair explicitly normalized the whole composite, preserving all actual whiskerings, quasi-inverses, units and compositors. No statement or hypothesis was weakened.

The optional five-direct-Phi bridge initially failed only because `simp only [nativeGK5ZSourceIso, eqToIso_trans]` already discharged its proof-irrelevant whole EqToIso comparison, and a following redundant `exact` triggered Lean's `No goals to be solved` error. The surplus tactic was removed; no mathematical assumption was altered. Earlier failing CI runs with temporary dependent `sorryAx` were never accepted as theorem certification.

The fixed-source Mathlib API was independently checked, including [Iso.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean) and [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean). In the pinned `Iso.lean`, `Iso.trans_assoc` orients `(a ≪≫ b) ≪≫ c` to `a ≪≫ b ≪≫ c`. The pinned `EqToHom.lean` certifies `eqToIso p ≪≫ eqToIso q = eqToIso (p.trans q)`. Public Lean4 simplifier references were also consulted; `simp only` does not automatically include unrelated associativity lemmas.

**Final exact-source [CI #41421856599](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41421856599):** Strict Lean **3848/3848 SUCCESS**; all **9/9** public `#print axioms` report only `propext`, `Classical.choice`, `Quot.sound`; `sorryAx = 0`; changed-file Lean errors/warnings `0/0`; Independent Kuu, workflow integrity, Governance terminal SUCCESS. Final exact-source Lean file blob matches merged file exactly; the global source/squash Git tree difference is explained above by the independent Qi v3.5 main update.

## Formal authority, excluded claims and next research

Canonical `main` is the only theorem-bearing branch; Lean **v4.30.0-rc2**, pinned mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 centered with independent Kuu a presentation; protected PR **#1558** remains Draft/open/unmerged.

The GK5AA theorem is restricted to genuine Mathlib fixed-universe categories and all **finite** GK5D typed functor trees. No strict equality of complete nonstrict equivalence records, original source-Q axioms, unconditional F45 faithfulness, raw F54/F55/P92B Type-valued higher cells, global Gray reconstruction or arbitrary hyperdescent is asserted.

**Next GK5AB:** prove compositional naturality of the five independent direct Phi reindex squares under consecutive index maps `I → J → K`, with identity and composition and actual whole EqToIso boundary path independence; then connect the verified higher-fivefold comparison with the independent Qi v3.5 phase-index bridge without conflating presentation with strict 空.

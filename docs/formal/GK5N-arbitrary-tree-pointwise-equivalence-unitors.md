# F112-P94D3GK5N — Genuine arbitrary finite-subtree left and right unitor coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2923](https://github.com/itakura-hidetoshi/KuuOS/pull/2923) — MERGED  
**Theorem squash/main at merge:** `b5ed97010beecbada2c2d21955cc5d45cfbc8dfc`  
**Final exact-source HEAD:** `37503ddfc78c92e5236708ef33bd052d630bbae5`  
**Same source/squash Git tree:** `ebd6fc8276cc670807f84c02313c7d51af850b72`  
**Exact-source CI:** [#41368603907](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41368603907) — terminal SUCCESS.

## Canonical Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5NArbitraryTreeUnitors.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5NArbitraryTreeUnitors.lean)

The new source is append-only, imports GK5M, and does not rewrite existing theorem files. It retains true indexed Mathlib categories `C,D:I→Cat.{vC,uC}`, genuinely specified pointwise equivalences `e:∀i,C i≌D i`, recursively constructed nontrivial whole NatIso comparisons `Φ_t`, and actual GK5D unit/atom/paste trees and structural rewrite steps.

## Four certified public theorems

**1. `nativeGK5NLeft_unitLaw`:** For any true Mathlib functor `R:C_i⥤C_j`, the whole NatIso left unit triangle compares `(𝟭(D_i))⋙ChangeAtom(e,R)` to `ChangeAtom(e,R)`. The actual `ChangeUnitIso(e,i)` counit inverse and the nonstrict `ChangeCompIso(e,𝟭(C_i),R)` middle unit inverse cancel by the genuine pinned `(e i).inverse_counitInv_comp X` triangle after applying `(e j).functor.map∘R.map`. No strict inverse of an equivalence is postulated.

**2. `nativeGK5NRight_unitLaw`:** The whole NatIso right unit triangle for any `R`, using actual `(e j).counitInv_functor_comp`, `ChangeUnitIso(e,j)`, `ChangeCompIso(e,R,𝟭(C_j))`, and true Mathlib right unitor.

**3. `nativeGK5NLeftUnit_subtree`:** For every arbitrarily deep dependently typed finite subtree `a : NativeGK5DTypedTree C i j`, the actual GK5D leftUnit generator satisfies the GK5H/GK5J **whole NatIso** square, unconditionally:
```lean
NativeGK5JPathSquare e
  (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.leftUnit a))
```
A helper `nativeGK5NLeft_unitor_withPhi` transports the whole left unit triangle across any genuine (non-reflexive) `φ:S≅ChangeAtom(e,R)`, using true unitor naturality and `Functor.isoWhiskerLeft_trans_isoWhiskerRight`.

**4. `nativeGK5NRightUnit_subtree`:** The corresponding true GK5D rightUnit whole NatIso square for **every** finite subtree, using right unitor naturality and the genuine right triangle. It retains recursive `Φ_a`, rather than replacing it with identity.

These are genuine **whole** Mathlib NatIso equalities. They are not merely equations at a selected object or raw Type-valued higher cells.

## Exact-source proof and Lean elaboration log

- Source HEAD `37503ddfc78c92e5236708ef33bd052d630bbae5`; squash/main `b5ed97010beecbada2c2d21955cc5d45cfbc8dfc`; independently fetched matching Git tree `ebd6fc8276cc670807f84c02313c7d51af850b72`.
- [CI #41368603907](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41368603907): **Strict Lean 3835/3835**, Independent Kuu, workflow integrity, Governance terminal all **SUCCESS**.
- **4/4 public `#print axioms`** outputs contain only `propext`, `Classical.choice`, and `Quot.sound`. `sorryAx0`, new axioms0, modified Lean errors/warnings0/0. The private helper proofs are within the public theorem dependency audit.
- The first CI found an unproved left generic triangle component. Applying the actual `inverse_counitInv_comp` and mapping it through the two nested genuine functors solved the underlying mathematical equality. An independent second issue involved whole NatIso interchange associativity and a reversed final theorem equality; both were corrected without changing theorem statements. In subsequent CI, only the exact expression shape of mapped composition and the dependent endpoint of `map (𝟙)` remained. The final proof first certifies the fully typed mapped-identity equality, then normalizes `Functor.map_comp` explicitly. No hypothesis was weakened or historical source overwritten.
- Fixed Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, public root107, strict 空 center, independent Kuu one presentation, protected validation-only PR #1558 Draft/open/unmerged.

## Mathematical boundary and GK5O

GK5M unconditionally covers every actual **associator** generator; GK5N now unconditionally covers **both unitor** generators for every finite typed subtree. The two contextual whiskering generators `whiskerLeft` and `whiskerRight` still require a separate recursive coherence proof. Consequently GK5H `StepCompatible e` and unrestricted finite `PathCompatible e` are **not yet proved unconditionally** by GK5N.

**Next GK5O:** Starting from a certified square for each basic step `h`, prove the whole NatIso square after left or right whiskering by any fixed typed subtree, using real Mathlib `isoWhiskerRight_trans`, `isoWhiskerLeft_trans`, `isoWhiskerLeft_trans_isoWhiskerRight`, and certified GK5K/GK5L nonstrict compositor naturality. Then induct over all five actual GK5D step constructors, and only if it succeeds apply GK5H to conclude unconditional every-finite-path whole NatIso and whole NatTrans coherence. Source-Q category axioms, unconditional F45 faithfulness, raw F54/F55/P92B Type-valued high cells, global Gray/hyperdescent and arbitrary-universe chains remain out of scope.

This follow-up is documentation only; **Strict Lean must be SKIPPED**, with docs governance checked separately.

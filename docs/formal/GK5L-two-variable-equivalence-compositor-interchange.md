# F112-P94D3GK5L — Genuine two-variable pointwise-equivalence compositor interchange

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2919](https://github.com/itakura-hidetoshi/KuuOS/pull/2919) — MERGED  
**Theorem squash/main HEAD at merge:** `27c1a75b8f619ef3955191603e0ef45e507c00a2`  
**Final source HEAD:** `84af8d7e34c27b4938315947132afa01bcdc3d5b`  
**Matching source/squash Git tree:** `0d4be641f6c70a54ae75d7fc4c79f86adced80ac`  
**Exact-source CI:** [#41364028089](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41364028089) — terminal SUCCESS.

## Canonical Lean file

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5LTwoVariableCompositorNaturality.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5LTwoVariableCompositorNaturality.lean)

GK5L is one append-only Lean source. It imports GK5K and its inherited GK5D/GK5G/GK5H/GK5I/GK5J prerequisites. The ambient data remain *genuine* Mathlib indexed category families `C,D:I→Cat.{vC,uC}` and pointwise equivalences `e:∀i,C i≌D i`. The changed functor is `Change(R)=(e i).inverse⋙R⋙(e j).functor`, with a real nonstrict `ChangeCompIso(e,R,S)` containing the middle equivalence unitIso.symm.

## Three new whole-category results

### 1. Left argument genuine whole NatTrans naturality

For `α:R⟶T` and `S:C j⥤C k`, `nativeGK5LChangeCompNat_left` proves

```lean
Functor.whiskerRight (nativeGK5GChangeNat e α)
    (nativeGK5GChangeAtom e S) ≫
  (nativeGK5GChangeCompIso e T S).hom =
(nativeGK5GChangeCompIso e R S).hom ≫
  nativeGK5GChangeNat e (Functor.whiskerRight α S)
```

The key local step is the actual pinned Mathlib naturality of `(e j).unitIso.inv` at the genuine map `α.app ((e i).inverse.obj X)`. The proof applies the true `S.map` and `(e k).functor.map` to that naturality equation and retains every category boundary, rather than treating an equivalence as a strict inverse.

### 2. Left argument whole NatIso

`nativeGK5LChangeCompIso_left` lifts the first theorem to any true `α:R≅T`. It uses `Iso.ext`, Mathlib's `Functor.isoWhiskerRight_hom` and the GK5I genuine `ChangeIso.hom = ChangeNat` result; no component-only shortcut or unconstrained higher cell.

### 3. Both argument whole NatIso interchange

For any composable genuine `α:R≅T` and `β:S≅U`, `nativeGK5LChangeCompIso_both` establishes the full 2-variable square:

```lean
(Functor.isoWhiskerRight (nativeGK5GChangeIso e α)
    (nativeGK5GChangeAtom e S) ≪≫
  Functor.isoWhiskerLeft (nativeGK5GChangeAtom e T)
    (nativeGK5GChangeIso e β)) ≪≫
  nativeGK5GChangeCompIso e T U =
nativeGK5GChangeCompIso e R S ≪≫
  nativeGK5GChangeIso e
    (Functor.isoWhiskerRight α S ≪≫
      Functor.isoWhiskerLeft T β)
```

It is an exact WHOLE Mathlib NatIso equality. The Lean proof uses the previously certified GK5K right-variable theorem, the new left-variable theorem and GK5H's proven preservation of NatIso composition by category change. It explicitly pastes actual Iso witnesses; no additional axiom, no artificial filler, and no strictification of the middle unit is introduced.

## Verification

- The final source commit `84af8d7e34c27b4938315947132afa01bcdc3d5b` passed on its first PR run without Lean repair.
- Squash theorem commit `27c1a75b8f619ef3955191603e0ef45e507c00a2`; independently fetched source/squash matching Git tree `0d4be641f6c70a54ae75d7fc4c79f86adced80ac`.
- [CI #41364028089](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41364028089): **Strict Lean 3833/3833**, Independent Kuu core, workflow integrity, Governance terminal all **SUCCESS**.
- All three `#print axioms` outputs (3/3) depend only on `propext`, `Classical.choice`, `Quot.sound`, no `sorryAx`, no new axiom, changed Lean error/warning 0/0.
- Fixed Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, same public root107, protected PR #1558 Draft/open/unmerged. Strict 空 centered, independent Kuu one presentation, and original arbitrary chosen inverse Q distinguished from explicit inverse P by genuine κ; no global Gray or unrestricted hyperdescent.
- Documentation-only PR must SKIP Strict Lean and verify its own governance.

## Exact current boundary and proposed GK5M

GK5K and GK5L have now established nontrivial **binary compositor naturality in both genuine NatIso variables**, an ingredient required for lifting GK5I's three-atom associator case to arbitrary finite typed subtrees with actual recursively constructed comparisons `Φ_a,Φ_b,Φ_c`. However, **GK5L has not yet proved that arbitrary-subtree associator square**, either left/right unitor or the two contextual whiskering generator squares. Therefore GK5H/GK5J's all-path local-to-global/endpoint obstruction equivalences remain conditional; arbitrary-path unconditional naturality is NOT yet established.

Next GK5M: derive explicit compositor associativity/pseudofunctor hexagon from the certified GK5I three-atom theorem, use GK5L two-variable naturality to transport `Φ_a,Φ_b,Φ_c`, and prove the actual arbitrary-subtree associator square. Only after independent unitors and whiskering generator proofs can the full GK5H/GK5J obstruction be discharged. Raw source-Q category axioms, F45 faithfulness, arbitrary integer matrix reachability, original raw Type-valued F54/F55/P92B high cells, Gray, unrestricted hyperdescent and variable-universe arbitrary chains remain outside the proven scope.

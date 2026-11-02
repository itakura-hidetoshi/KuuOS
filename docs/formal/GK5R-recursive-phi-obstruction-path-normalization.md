# F112-P94D3GK5R — Genuine recursive Phi obstruction and finite typed path/leaf descent

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2931](https://github.com/itakura-hidetoshi/KuuOS/pull/2931) — MERGED  
**Exact-source HEAD:** `697ecf1aaed54adf31045cadfe596358e59e1691`  
**Theorem squash/main:** `8796e6287cb85a0a2cc6fbec1f2374b204e2c124`  
**Exact-source and squash Git tree:** `b6e884b99912661f13c5128945e55f5d8fcb1870` — identical by independent GitHub git/commits reads.  
**Exact-source CI:** [#41384592915](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41384592915) — terminal SUCCESS.

## Canonical append-only source and real categorical scope

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5RRecursivePhiObstruction.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5RRecursivePhiObstruction.lean) is a single new 305-line source; it imports certified GK5Q and pinned Mathlib's `Equivalence`, `Whiskering` and `Tactic`. Existing GK5D/GK5G/GK5H/GK5O/GK5Q source files are unchanged.

Fix the same indexed Mathlib category universe pair `C D E : I → Cat.{vC,uC}` and *genuine* pointwise equivalences `e : ∀ i, C i ≌ D i`, `g : ∀ i, D i ≌ E i`. Every finite tree `t` retains its real dependent source, target, binary pasting, and unit nodes.

The following are genuinely **different recursively assembled whole Mathlib NatIso values** sharing the same source and target:

1. `nativeGK5RSequentialCompositePhi e g t`: paste `Phi_g(ChangeTree_e(t))`, `ChangeIso_g(Phi_e(t))`, and the actual GK5Q `Theta_(Eval t)`.
2. `nativeGK5RDirectCompositePhi e g t`: paste GK5Q's *actual* `TreeComparison(e,g,t)` with `Phi_(e.trans g)(t)`.

GK5R does **not** assert these NatIso pastings are automatically equal. It defines their exact difference as a genuine **whole Mathlib NatIso automorphism of the common target functor**:

```lean
nativeGK5RPhiObstruction e g t :=
  (nativeGK5RSequentialCompositePhi e g t).symm ≪≫
    nativeGK5RDirectCompositePhi e g t
```

The target functor is `nativeGK5GChangeAtom (fun i => (e i).trans (g i)) (nativeGK5DTreeComposite t)`. This is a witness-level obstruction, not a proof-irrelevant Boolean and not a new raw source higher cell. Triviality precisely means equality of the two genuine recursive pastings.

## Twelve public declarations: real NatIso gluing and exact obstruction descent

1. `nativeGK5RSequentialPhi` — the genuine two-stage recursive Phi before GK5Q Theta, with whole GK5G witness data retained.
2. `nativeGK5RSequentialCompositePhi` — two-stage recursive Phi plus the actual Mathlib composition comparison.
3. `nativeGK5RDirectCompositePhi` — GK5Q whole tree comparison plus the direct composite-equivalence recursive Phi.
4. `nativeGK5RPhiObstruction` — the genuine target-endomorphism whole Mathlib NatIso difference.
5. `nativeGK5RSequentialPhi_path_square` — unconditional whole NatIso naturality for every finite proof-relevant GK5D path, by two genuine GK5O squares and `nativeGK5HChangeIso_trans`.
6. `nativeGK5RSequentialCompositePhi_path_square` — paste the preceding square with certified GK5Q `nativeGK5QAtomComparison_path_square`.
7. `nativeGK5RDirectCompositePhi_path_square` — paste GK5Q's true two-stage/composite finite-path square with GK5O for `e.trans g`.
8. `nativeGK5RPhiObstruction_path_square` — for **every** finite typed `q:a⇒b`, the obstruction is conjugated along the true `ChangeIso_(e.trans g)(PathIso q)`, as an equality of whole Mathlib NatIso witnesses.
9. `nativeGK5RPhiObstruction_refl_iff` — exact iff between `Omega_t = Iso.refl` and equality of the two actual recursive Phi pastings, by real Iso cancellation.
10. `nativeGK5RPhiObstruction_refl_iff_of_path` — the yes/no triviality of `Omega` is preserved **and reflected** along every actual finite typed path (both directions).
11. `nativeGK5RPhiObstruction_normalization_iff` — the same equivalence holds between any finite tree and its actual GK5D canonical right-associated normal form.
12. `nativeGK5RPhiObstruction_sameLeaves_iff` — any two trees with equal **ordered dependently typed full leaf words** have equivalent obstruction-triviality predicates, using the concrete GK5D constructed comparison path.

In formulas, write `Q(q) := ChangeIso_(e.trans g)(PathIso(q))` and `Omega_t := nativeGK5RPhiObstruction(e,g,t)`. GK5R certifies the whole NatIso equation

```lean
Q(q) ≪≫ Omega_b = Omega_a ≪≫ Q(q)
```

and its exact implication `Omega_a = Iso.refl ↔ Omega_b = Iso.refl`. This is a **pathwise obstruction descent** within the precise GK5D rewrite calculus. It establishes neither automatic vanishing nor a new external descent theory or global Gray reconstruction.

## Structural Lean4 proof analysis

The final changed Lean file was reviewed in full, including the authoritative imported GK5Q source, GK5G recursive `Phi`/equivalence action, GK5O whole-path naturality, GK5H `ChangeIso` composition law, GK5D actual finite path and normalization constructors, and pinned Mathlib's `Iso.trans_assoc`, `Iso.symm_self_id`, `Iso.self_symm_id`, `Iso.trans_refl`, `Iso.refl_trans` and `EqToHom` conventions.

- Genuine recursive `Phi` must not be silently replaced with a strict `eqToIso` comparison: the former includes actual equivalence unit/counit and compositor witnesses; the latter is GK5Q's structural tree comparison. Both are carried separately in the two NatIso pastings.
- `Iso.trans` (`≪≫`) is **right associative** and the two squares must be pasted with genuine `Iso.trans_assoc`, not by a `change` tactic requiring definitional equality.
- Mapping a compositional GK5O equation through `nativeGK5GChangeIso g` requires its certified `nativeGK5HChangeIso_trans`; this preserves the genuine whole NatIso boundaries and never assumes a strict inverse.
- The relative obstruction's conjugacy follows by an explicit small groupoid calculation using actual inverses, not by manufacturing a high cell. The stronger iff along a path uses cancellation by `Q(q).symm` on the correct side of a whole NatIso equation.
- Both additional descent results are **instances** of that pathwise iff, using existing GK5D normalization and same-leaves constructed paths. Their explicit dependent indices prohibit swapping unlike categories or reversing the full leaf order.
- No `sorry`, `admit`, extra axiom or weakened assumption; no original source file overwritten.

Upstream pinned reference: [Mathlib Iso](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean), [Whiskering](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [Equivalence](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean).

## Exact-source CI and authority receipt

The final source commit `697ecf1aaed54adf31045cadfe596358e59e1691` passed [CI #41384592915](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41384592915): **3839 / 3839 Strict Lean SUCCESS**, Independent Kuu/retained API SUCCESS, governance gate/audit summary SUCCESS. All **12/12** new public `#print axioms` reports contain exactly standard `propext`, `Classical.choice`, `Quot.sound`; **`sorryAx` 0**, changed Lean error/warning 0/0. The earlier nine-declaration source also passed [CI #41384258703](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41384258703) with Strict Lean 3839/3839.

The final source and squash commits share independent tree `b6e884b99912661f13c5128945e55f5d8fcb1870`. Lean **v4.30.0-rc2**; mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**; root **107**; same-root/append-only/tighten-only/overwrite-forbidden, strict 空 centered, independent Kuu one presentation. Validation-only PR #1558 protected Draft/open/unmerged.

## Precise next stage: GK5S candidate

GK5R proves that `Omega_t` is pathwise conjugate and that triviality is determined by the **full typed ordered leaf-word class**, not that `Omega_t` is always trivial. To close the stronger recursive-Phi composition comparison, separately derive genuine unit/counit and binary compositor compatibility at the GK5G `Phi` boundary; test canonical right-associated typed words without substituting structural GK5Q eqToIso for nontrivial witnesses. Any proof of universal triviality must come only after those genuine Mathlib comparisons are constructed.

No unconditional original F45 faithfulness, source-Q category axioms, raw F54/F55/P92B Type high cells, global Gray reconstruction, universe-varying arbitrary chains, or unrestricted hyperdescent is claimed. Docs-only follow-up must skip Strict Lean but pass independent Kuu and governance.

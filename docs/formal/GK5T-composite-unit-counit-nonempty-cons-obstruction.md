# F112-P94D3GK5T — Genuine composite counit/unit coherence and exact nonempty cons obstruction

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2935](https://github.com/itakura-hidetoshi/KuuOS/pull/2935) — MERGED  
**Final exact-source HEAD:** `99b0d90fec347b38e2ba04b9f9909f6d1589b58a`  
**Theorem squash/main:** `d6d83f63f4e5d72badf8d6b6ef7f65bd7435c3c4`  
**Identical source/squash Git tree:** `a018fb3ccbfa4631cf4c1cc40932486e5c73f9a0` (confirmed by independent GitHub git-commits API reads).  
**Final exact-source CI:** [#41389108271](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41389108271) — terminal SUCCESS, **Strict Lean 3841/3841**.

## New append-only Lean source and true category-theory scope

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5TUnitCounitCompositeCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5TUnitCounitCompositeCoherence.lean) is a new 276-line proof file; no older source was edited. It imports certified GK5S and pinned Mathlib Equivalence/Whiskering/Tactic.

Fix actual indexed Mathlib category families `C D E : I → Cat.{vC,uC}`, and genuine equivalences `e : ∀ i, C i ≌ D i`, `g : ∀ i, D i ≌ E i`. Their chosen inverses, unit/counit NatIsos and the non-strict GK5G binary compositor are not replaced by strict identities.

### 1. The genuine composite equivalence unit law — unconditional

`nativeGK5TUnitComparison_whole` establishes the ACTUAL whole Mathlib NatIso equality

```lean
(nativeGK5GChangeUnitIso g i ≪≫
  nativeGK5GChangeIso g (nativeGK5GChangeUnitIso e i)) ≪≫
    nativeGK5QAtomComparison e g (𝟭 (C i)) =
  nativeGK5GChangeUnitIso
    (fun k : I => (e k).trans (g k)) i
```

This directly uses Mathlib's actual `Equivalence.trans` structure: its inverse is `g.inverse ⋙ e.inverse`, its forward functor is `e.functor ⋙ g.functor`, and its counit is a genuine composite of the corresponding non-strict counits, not an assumed identity.

`nativeGK5TUnitTreeComparison_refl` separately proves that GK5Q's structural `eqToIso` for the unit **tree** is `Iso.refl`. This statement is not the claim that the equivalence's own counit/unit witness is trivial. Combining the two proves `nativeGK5TUnitPhi_compatible` and the unconditional `nativeGK5TAllUnits : NativeGK5SUnitCoherent e g`.

Thus the GK5S genuine unit/counit obstruction is **fully discharged** for the specified genuine indexed category families.

### 2. All empty-leaf and one-leaf finite typed presentations

Using GK5R's certified pathwise full-NatIso obstruction iff and GK5S's proven atomic coherence, GK5T proves `Omega_t = Iso.refl` for **every** actual typed tree whose complete ordered dependent leaf word is exactly `.cons R (.empty j)`. It separately instantiates real left/right unitor paths of an atomic tree, and proves that zero-leaf typed presentations have the same exact obstruction-triviality condition as `.unit i`. The now-proved unit law makes this condition unconditionally true on every zero-leaf tree.

Corresponding `nativeGK5TOneLeafPhi_compatible` and `nativeGK5TEmptyWordPhi_compatible` establish equality of the **two genuinely recursively constructed Phi pastings**, not just the Boolean status of an obstruction. Unit insertion and rebracketing remain actual proof-relevant GK5D paths; unrelated leaf words are not conflated.

### 3. The sharpest remaining necessary-and-sufficient criterion

The genuine right-associated canonical cons with empty typed tail is proved unconditionally: `nativeGK5TConsEmpty_compatible`. GK5T derives

```lean
NativeGK5SAllTreeCoherent e g ↔ NativeGK5SConsCoherent e g
```

and the equivalent universal obstruction-vanishing form, eliminating the former unit hypothesis entirely.

It then defines `NativeGK5TNonemptyConsCoherent e g` as a precise **Prop**, requiring the actual whole recursive Phi compatibility of

`paste (atom R) (TreeOfWord (cons S w))`

whenever the genuine tail `TreeOfWord (cons S w)` has the proved Phi equality. Both `R` and `S` are actual typed Mathlib functors and the dependent tail `w` retains every intermediate category.

`nativeGK5TCons_iff_nonempty` proves that the original GK5S cons condition is exactly equivalent to this **two-or-more actual atomic leaf** condition; its empty-tail constructor is discharged by the already proved right-unitor/atomic theorem.

Finally `nativeGK5TAllObstructions_iff_nonemptyCons` proves

```lean
(∀ {i j : I} (t : NativeGK5DTypedTree C i j),
   nativeGK5RPhiObstruction e g t = Iso.refl _) ↔
  NativeGK5TNonemptyConsCoherent e g
```

This is a **reduction theorem, not proof of the right-hand proposition**. The true non-strict binary/middle-compositor comparison for at least two atomic leaves remains the exact obstruction for GK5U. No unrestricted Gray reconstruction, source-Q category axiom, or raw high cell theorem is claimed.

## All 17 public `#print axioms` declarations

1. `nativeGK5TUnitComparison_whole`
2. `nativeGK5TUnitTreeComparison_refl`
3. `nativeGK5TUnitPhi_compatible`
4. `nativeGK5TAllUnits`
5. `nativeGK5TOneLeafObstruction_refl`
6. `nativeGK5TLeftUnitorAtom_refl`
7. `nativeGK5TRightUnitorAtom_refl`
8. `nativeGK5TEmptyWordObstruction_iff`
9. `nativeGK5TEmptyWordObstruction_refl`
10. `nativeGK5TConsEmpty_compatible`
11. `nativeGK5TAllTrees_iff_cons`
12. `nativeGK5TAllObstructions_iff_cons`
13. `NativeGK5TNonemptyConsCoherent`
14. `nativeGK5TCons_iff_nonempty`
15. `nativeGK5TAllObstructions_iff_nonemptyCons`
16. `nativeGK5TOneLeafPhi_compatible`
17. `nativeGK5TEmptyWordPhi_compatible`

These are audited whole NatIso theorems, exact propositions, and conditional if-and-only-if statements as typed. Merely defining `NativeGK5TNonemptyConsCoherent` does **not** certify that it holds.

## Full Lean4 elaboration analysis and structural repair

The full file, imports, existing GK5D/G/H/O/Q/R/S signatures, pinned Mathlib `Equivalence.trans`, `Whiskering.lean`, `EqToHom.lean`, and true `Iso` associativity/cancellation laws were inspected. The initial candidate did NOT compile entirely:

- **First exact-source CI [#41388380587](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41388380587):** The new `nativeGK5TUnitComparison_whole` itself passed its public axiom output with standard three axioms. However, `nativeGK5TUnitPhi_compatible` was missing an `eqToIso ⋯ ≪≫` factor on the right. `simp only` had not proved the GK5Q unit-tree comparison was reflexive. It is incorrect to force this by `change`, because it is an equality involving an actual `eqToIso`, not just a syntactic definitional change.
- **Second [CI #41388716053](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41388716053):** The new independent `nativeGK5TUnitTreeComparison_refl` discharges that genuine `eqToIso` using actual tree evaluation and Mathlib's `eqToIso_refl`. With this exact lemma in `simpa only`, the original true unit/counit whole NatIso equation closes the recursive `Phi` square. Strict Lean 3841/3841 SUCCESS, 9/9 public axiom checks standard three only, no `sorryAx`.
- **Final [CI #41389108271](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41389108271):** The eight additional tightly typed one/zero-leaf and remaining-obstruction theorems were added to the same NEW file without weakening any previous statement. Strict Lean **3841/3841 SUCCESS** and all **17/17** `#print axioms` show ONLY `propext`, `Classical.choice`, `Quot.sound`, `sorryAx` 0, changed Lean errors/warnings **0/0**. Independent Kuu core and governance terminal SUCCESS.

Final source `99b0d90fec347b38e2ba04b9f9909f6d1589b58a`, theorem squash `d6d83f63f4e5d72badf8d6b6ef7f65bd7435c3c4`, identical tree `a018fb3ccbfa4631cf4c1cc40932486e5c73f9a0`.

## Authority, fixed environment, and next proof boundary

Pinned Lean **v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, same-root/append-only/tighten-only/overwrite-forbidden. Strict 空 centered; independent Kuu is one presentation. Protected validation-only PR #1558 remains Draft/OPEN/unmerged.

**GK5U candidate:** prove the genuinely non-strict `NativeGK5TNonemptyConsCoherent e g`, starting from the explicit two-atom compositor square and extending it to `paste (atom R) (TreeOfWord (cons S w))` with the recursive tail `Phi`. Use actual middle equivalence unit/counit naturality and GK5K/GK5L's certified two-variable compositor laws, not structural `eqToIso` as a substitute. Only after that succeeds can the GK5T iff yield universal `Ω_t=Iso.refl`.

Docs-only PR must skip Strict Lean while independently passing selected Independent Kuu, workflow integrity, and governance checks.

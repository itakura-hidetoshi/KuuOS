# F112-P94D3GK5P — Typed index-relabeling / pointwise-equivalence exchange and finite-path naturality

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2927](https://github.com/itakura-hidetoshi/KuuOS/pull/2927) — MERGED  
**Authoritative main/theorem squash:** `ac063e7bef086288eb7728c761b3f9573bd2ad43`  
**Final exact-source HEAD:** `dfddaaf30139c60911f29115708eb83cabc308a4`  
**Source/squash Git tree:** `57ca56906655dd26014ea62ef9ffa514ea4cf023` (identical, GitHub git-commit API independently read).  
**Exact-source workflow:** [#41380573456](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41380573456) — terminal SUCCESS.

## New append-only source and import boundaries

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5PIndexChangeNaturality.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5PIndexChangeNaturality.lean) is one new source. Its imports explicitly reuse the certified GK5O unconditional path theorem and GK5F actual typed index-relabeling constructors, along with fixed Mathlib Equivalence, Whiskering and Tactic APIs. GK5D typed trees and paths, GK5G pointwise equivalence change, and GK5H local/global squares remain authoritative; no historical source is replaced.

Fix any map `f : I → J` (not necessarily injective), genuine Mathlib category families `C D : J → Cat.{vC,uC}`, and pointwise genuine category equivalences `e : ∀ j, C j ≌ D j`. GK5P proves strict equality **of dependently typed word/tree constructors**, using actual `nativeGK5FWordReindex`, `nativeGK5FTreeReindex` and `nativeGK5GChangeWord/Tree`:

```lean
nativeGK5FTreeReindex f D
    (nativeGK5GChangeTree (fun z : I => e (f z)) t) =
  nativeGK5GChangeTree e (nativeGK5FTreeReindex f C t)
```

The same identity holds for finite typed ordered words; the exact ordered-leaf image of the tree consequently commutes with the two operations. Every intermediate index and genuine Mathlib functor remains typed. A noninjective reclassification is allowed in this **forward** construction; no converse reflection of word equality is asserted.

## Eleven new publicly audited theorems

1. `nativeGK5PChangeWord_reindex`: exact typed word exchange.
2. `nativeGK5PChangeTree_reindex`: exact typed finite tree exchange.
3. `nativeGK5PChangeTreeLeaves_reindex`: preservation of the full ordered dependently typed leaf word across the exchange.
4. `nativeGK5PRelabeledPath_whole`: after GK5F's explicit real path reindexing, GK5O gives unconditional whole Mathlib NatIso path-square coherence under `e`.
5. `nativeGK5PRelabeledPath_natTrans`: the whole NatTrans hom equation for this path.
6. `nativeGK5PPullbackPath_whole`: the separately typed whole NatIso equation for the original path changed by `e ∘ f` on the pullback family.
7. `nativeGK5PPullbackPath_natTrans`: its whole NatTrans hom equation.
8. `nativeGK5PSequentialPath_whole`: after transporting a path by `e`, transporting that real path by `g : ∀ i, D i ≌ E i` remains unconditionally coherent as a whole NatIso.
9. `nativeGK5PSequentialPath_natTrans`: the same second-stage whole NatTrans square.
10. `nativeGK5PCompositePath_whole`: a genuine Mathlib composite equivalence `fun i => (e i).trans (g i)` also preserves all finite typed paths as whole NatIso squares.
11. `nativeGK5PCompositePath_natTrans`: its NatTrans hom version.

In every case the path and comparison isomorphisms are the **actual GK5D/GK5G whole Mathlib objects**, not an asserted high cell. GK5O discharges all finite-path naturality conditions without introducing new generator hypotheses.

**Important boundary:** GK5P does **not** identify the recursively pasted `Phi` for two successive equivalences strictly with the `Phi` of their Mathlib composite. These are individually proved path-squares; construction and coherence of a further non-strict comparison between the two routes remains a separate potential GK5Q task. Similarly, word/tree exchange does not assert strict equality of the underlying non-strict equivalence unit/counit compositors. No source-Q axioms, F45 unconditional faithfulness, original raw F54/F55/P92B Type high cells, global Gray reconstruction, or unbounded hyperdescent follows.

## Structural Lean4 diagnosis from exact-source CI

The initial two attempts failed in the **new** file; the entire 228-line final file, imports, GK5D/F/G/H/O dependent signatures, and pinned Mathlib Equivalence API were checked before the final correction.

- **Typed word induction, different index universes:** `rw [ih]` rewrote the recursive tail but left two heads `nativeGK5GChangeAtom (fun z => e (f z)) R` and `nativeGK5GChangeAtom e R`. They use different index-family *presentations* (I versus J), even though their genuine functor formula is definitionally the same after unfolding the **specified** action. The final `simp only [nativeGK5GChangeAtom]` proves the remaining exact equality; no arbitrary category equivalence is strictified.
- **Elaboration of pullback NatIso in the NatTrans formula:** the elaborator inferred the outer `J`-indexed family `C` for a `q` living in the `I`-indexed pullback family. Specifying only `(C := fun z : I => C (f z))` on `nativeGK5GChangeIso` was insufficient, since the nested `nativeGK5DPathIso q` also needed `(C := fun z : I => C (f z))`. The final corrected whole equation retains the original typed path and both real source/target functor categories.
- **Genuine equivalence composition:** pinned Mathlib `Equivalence.trans` is used directly; its bundled functor/inverse and coherence data are not replaced by a presumed strict inverse.
- No original theorem statement, assumption, universe restriction, or historical source was weakened. The new source had no `sorry` or `admit`, and final Lean warnings/errors were zero.

## CI and axiom receipt

- **Exact-source HEAD:** `dfddaaf30139c60911f29115708eb83cabc308a4`.
- **Theorem squash SHA:** `ac063e7bef086288eb7728c761b3f9573bd2ad43`.
- **Source/squash Git tree:** `57ca56906655dd26014ea62ef9ffa514ea4cf023` (identical).
- **Exact-source [CI #41380573456](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41380573456):** Strict Lean **3837/3837 SUCCESS**; Independent Kuu, Workflow consolidation integrity, Select impacted audit checks and Governance gate/audit summary all terminal SUCCESS.
- **11/11 public `#print axioms` checks:** only `propext`, `Classical.choice`, `Quot.sound`; **`sorryAx` 0**. No new axiom or Lean warnings/errors.
- Fixed Lean **v4.30.0-rc2**, pinned mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**; public root **107** preserved. Same-root/append-only/tighten-only/overwrite-forbidden. Strict 空 centered; independent Kuu is a presentation, never silently taken as a new authority. Protected PR #1558 was Draft/OPEN/unmerged during this verification.

## Next mathematically precise stage (GK5Q candidate)

Construct an **actual non-strict whole Mathlib NatIso** comparing the two successively conjugated functors with the single change along `e.trans g`, prove its unit/counit/compositor coherence and naturality in genuine whole NatIsos, then induct on typed finite trees to obtain a comparison between the two recursively assembled `Phi` values. Reuse GK5O's all-path theorem only after the actual comparison is defined. This is not yet a theorem or a CI-certified claim.

Docs synchronization is append-only; docs-only Strict Lean must be **SKIPPED** while governance/integrity checks are required.

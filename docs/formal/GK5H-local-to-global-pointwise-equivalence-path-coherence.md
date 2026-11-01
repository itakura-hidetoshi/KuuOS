# F112-P94D3GK5H — Exact local-to-global whole NatIso path coherence obstruction

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2911](https://github.com/itakura-hidetoshi/KuuOS/pull/2911) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `d8ac072dab926283dfd2117bad384993ceecab58`  
**Final theorem source HEAD:** `e5720da9e5908e58d78688dd7a0dda5ae396b86c`  
**Test-merge SHA:** `a37e8a54078ba797f420a48a1f9f15acd21c6d0a`  
**Matching source/test-merge Git tree:** `6d2e16da4f3a3f0686e724eab7eb8617958ed2ac`  
**Exact-source CI:** [#41351958262](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41351958262) — SUCCESS.

## Canonical source, predecessor and precise mathematical status

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5HLocalToGlobalPathCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5HLocalToGlobalPathCoherence.lean)

GK5G constructed a genuine whole Mathlib natural isomorphism `Φ_t` for every finite heterogeneous typed functor tree under pointwise Mathlib category equivalences `e : ∀ i, C i ≌ D i`. It transported actual proof-relevant GK5D associator/unitor/whiskering paths, and separately connected already changed paths to within-D-family GK5E chosen-inverse squares. **GK5G did not prove that the constructed `Φ` commutes with EVERY original structural path.**

GK5H now proves the **exact necessary-and-sufficient local-to-global criterion** for that further path naturality, plus the resulting full NatTrans square and specifically constructed normalization square **under explicitly stated local compatibility**. It does NOT prove that all local step squares hold without that compatibility assumption. Therefore unconditional all-path pseudonaturality remains a separate open proof obligation.

The original F45 source, genuinely attained old-AH, kernel-compatible full subcategory, GK4BM arbitrary chosen inverse `Q_T`, distinct GK4BP explicit inverse `P_T`, genuine GK4BQ comparison `κ_T`, and all GK4BT–GK5G theorem source files are unchanged. No strict equation `Q_T=P_T` is introduced. Only one new theorem source is added, with no existing Lean-file edits. Lean **v4.30.0-rc2**, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; 107 public roots; protected validation-only #1558 remains Draft/OPEN/unmerged.

## Actual local condition and full-path condition

For any genuine pointwise equivalences `e : ∀ i, C i ≌ D i` and any actual typed basic rewrite `s : NativeGK5DTypedStep C a b`, GK5H defines

`NativeGK5HStepCompatible e`

to mean **the following equality of whole Mathlib NatIso objects for EACH actual step**:

`StepIso(ChangeStep(e,s)) ≪≫ Φ_b = Φ_a ≪≫ ChangeIso(e,StepIso(s))`.

The basic constructors are exactly GK5D's real Mathlib associator, left/right unitor, and both whiskerings. The predicate is an explicit `Prop`; it is **not supplied as an axiom and not silently declared true**.

For every actual finite proof-relevant path `q : NativeGK5DTypedPath C a b`, define

`NativeGK5HPathCompatible e`

to mean the corresponding **whole NatIso** equality

`PathIso(ChangePath(e,q)) ≪≫ Φ_b = Φ_a ≪≫ ChangeIso(e,PathIso(q))`.

This is stronger than equating merely a scalar, a component, or the path labels; the comparison consists of actual whole Mathlib natural isomorphisms.

## Constructive exact descent/gluing

The most important theorem is

`nativeGK5HAllPaths_iff_localStep`:

`NativeGK5HPathCompatible e ↔ NativeGK5HStepCompatible e`.

**Local ⇒ global:** GK5H performs genuine structural induction over the GK5D proof-relevant finite path syntax.

- `refl`: uses the real whole Mathlib Iso left/right identity laws.
- `basic`: instantiates the stated local step compatibility, with the genuine GK5G path-change constructor.
- `reverse`: derives the reversed square by an explicitly proved Iso-groupoid identity `nativeGK5HReverseSquare`, retaining all four typed endpoints; `nativeGK5HChangeIso_symm` proves the pointwise-equivalence change respects true NatIso reversal.
- `trans`: glues the two induction squares using genuine Iso composition, `Iso.trans_assoc`, and the newly proved `nativeGK5HChangeIso_trans` preserving whole NatIso composition.

**Global ⇒ local:** apply the full path condition to each one-step proof-relevant `.basic s`, then use the concrete GK5D/GK5G constructor equations. No unverified free higher cell or arbitrary homotopy is assumed.

Thus **no path-level obstruction beyond the basic generators remains** once they are compatible. Conversely, any failure at a generator is an obstruction to arbitrary-path compatibility. The result does not itself construct a failing generator, nor prove there are none.

## Whole NatTrans and nonvacuous normalization

`nativeGK5HPathNatTrans_square_of_local` derives the precise **whole Mathlib NatTrans** equality for every actual finite path `q`, under the explicit `NativeGK5HStepCompatible e` assumption:

`PathIso(ChangePath(e,q)).hom ≫ Φ_b.hom = Φ_a.hom ≫ ChangeIso(e,PathIso(q)).hom`.

The proof takes `Iso.hom` of the already established **whole NatIso square**, then uses pinned Mathlib `Iso.trans_hom` for exact typing; no mere objectwise assertion is substituted.

`nativeGK5HNormalizePath_square` specializes the full NatIso square to GK5D's actually constructed canonical normalization path `nativeGK5DNormalizePath t` for every finite tree. This is nonvacuous reachability because GK5D constructs that path explicitly, not through an existence assumption.

## Lean4 elaboration history and correction

The initial exact-source compilation found three proof elaboration issues, with all math statements and other source declarations fixed:

1. After simp-normalization, `ChangeIso` preservation of NatIso composition retained a reflexive whole transformation equation; closed with an explicit `rfl`.
2. The reverse-square proof required true `Iso.trans_assoc` reassociation before rewriting the supplied local square. Introducing a precisely parenthesized intermediate equality repaired the mismatch.
3. The reflexive path case required applying the real right-unit law for whole NatIso, rather than assuming definitional identity. The final proof explicitly uses `Iso.trans_refl`.

A subsequent elaboration diagnostic showed that an *unused and underdetermined category typeclass* in the general reverse-square lemma blocked Lean's inference. The proof was tightened by dropping extraneous type variables and supplying the exact actual changed functor category `D i ⥤ D j` at the lemma call. None of these changes weakened any theorem or added axioms.

One CI attempt ended prematurely during parent Lake cache restoration, with no Lean compiler step; the GitHub Actions failed-job rerun completed and confirmed the same-source formal proof. This infrastructure interruption is not a Lean failure and is not represented as such.

## Exact-source certificate

- Theorem source `e5720da9e5908e58d78688dd7a0dda5ae396b86c`.
- Actual test-merge commit `a37e8a54078ba797f420a48a1f9f15acd21c6d0a`.
- Independent Git object inspections confirmed both have the **identical Git tree** `6d2e16da4f3a3f0686e724eab7eb8617958ed2ac`.
- [GitHub Actions #41351958262](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41351958262): **Strict Lean 3829/3829 SUCCESS**, **Independent Kuu SUCCESS**, **selected impact audit SUCCESS**, **Governance terminal SUCCESS**.
- **7 public audited theorems/definitions, 7 `#print axioms`**: only standard `propext`, `Classical.choice`, `Quot.sound`; **sorryAx = 0**, no new axioms, changed Lean error/warning **0/0**.
- Theorem squash/main at theorem merge `d8ac072dab926283dfd2117bad384993ceecab58`.
- Documentation follow-up is **docs-only**. Strict Lean must be **SKIPPED**, not rerun.

## Scope and next proof obligation

The exact criterion is for genuine Mathlib category equivalences at a fixed universe pair, finite typed functor trees, and actual associator/unitor/whiskering paths. **The unconditional truth of the basic-step compatibility predicate is still OPEN**; proving it requires real category-equivalence triangle identities, unit/counit naturality, associator coherence and interchange. GK5H does not assert cross-family strict chosen inverse `Q_{C i}=Q_{D i}`, unbounded changing universes, raw F54/F55/P92B high cells, source-Q laws, unconditional F45 faithfulness, global Gray, arbitrary integer-matrix attainability or hyperdescent.

A next GK5I (or GK5H continuation) can discharge each basic generator: associator, left/right unitor, and whiskered generators, using the *actual fixed pinned mathlib* APIs. Only **after that proof** can the already proved GK5H local-to-global theorem yield unconditional whole NatIso/whole NatTrans path naturality for all finite paths. Do not use the conditional result as if the local obstruction had already vanished.

Strict 空 remains the organizing center; independent Kuu remains one presentation. Append-only, same-root, and all authority boundaries remain unchanged.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

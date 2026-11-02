# F112-P94D3GK5Y — Unconditional whole NatIso coherence for all five genuine direct Phi pentagon edges

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2945](https://github.com/itakura-hidetoshi/KuuOS/pull/2945) — MERGED  
**Final exact-source HEAD:** `852abc541b2c825f9b7564c26c690d60b7b4571d`  
**Theorem squash/main SHA:** `6731a67cca6fd0b09184af1dd04311d38469bf13`  
**Matching exact-source/squash Git tree:** `c3d095159c97b71c8a683886cd3ca47532884915` — independently verified via GitHub Git commit objects.  
**Exact-source CI:** [#41408805373](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41408805373) — terminal SUCCESS: Strict Lean **3846/3846**, Independent Kuu, Governance SUCCESS.

## Mathematical result

For any genuinely indexed pointwise Mathlib equivalences e:C_i≌D_i, g:D_i≌E_i, h:E_i≌F_i, k:F_i≌G_i and any finite heterogeneously typed GK5D functor tree t, GK5X constructs five **independent direct recursive** genuine GK5G Phi witnesses, one for each actual Mathlib Equivalence.trans parenthesization. These witnesses retain the real chosen quasi-inverses, nontrivial unit/counit, middle-unit compositor and actual whiskering, not invented strict equalities.

The five genuine composite equivalences and the oriented pentagon edges are:

```text
P0 = (((e trans g) trans h) trans k)
P1 = ((e trans (g trans h)) trans k)
P2 = (e trans ((g trans h) trans k))
P3 = (e trans (g trans (h trans k)))
P4 = ((e trans g) trans (h trans k))

P0 -> P1 -> P2 -> P3
P0 -> P4 -> P3
```

Each actual whole NatIso edge Alpha_ij compares the **conjugation functors** of adjacent parenthesizations; it is EqToIso of a real Mathlib functor equality, not a claim that complete Equivalence records are equal. GK5X defined the true relative source-automorphism Delta_ij(t) := (Phi_i(t) ≪≫ Alpha_ij(TreeComposite t)) ≪≫ (Phi_j(t)).symm. Its prior theorem established only equality of products along both pentagon routes; it did not establish the separate edge identities.

GK5Y now proves **each of the five genuine defects independently equals Iso.refl with no added hypothesis**, and separately the five full whole NatIso squares Phi_i ≪≫ Alpha_ij = Phi_j. Main public theorems:

```lean
nativeGK5YAllFiveEdges_whole
nativeGK5YAllFiveDefects_refl :
  nativeGK5XDefect01 e g h k t = Iso.refl _ ∧
  nativeGK5XDefect12 e g h k t = Iso.refl _ ∧
  nativeGK5XDefect23 e g h k t = Iso.refl _ ∧
  nativeGK5XDefect04 e g h k t = Iso.refl _ ∧
  nativeGK5XDefect43 e g h k t = Iso.refl _
```

This genuinely strengthens GK5X from structural and relative-product pentagon coherence to **unconditional five-edge coherence** for the independently direct recursively constructed Phi values over all finite GK5D typed functor trees.

## Constructive proof strategy

The only changed theorem source is the new append-only [PolygonNativeC60AQFullPentagonPhysicalNativeGK5YDirectPhiFiveEdgeCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5YDirectPhiFiveEdgeCoherence.lean), **518 lines**; all older Lean files are untouched.

The private `nativeGK5YLiftThree` prefixes GK5W's actual triple direct-Phi associativity by a whole equality-induced NatIso of the correctly typed tree source, using genuine `eqToIso_trans`. It yields three local direct-Phi edge squares with grouped, actual Mathlib equivalences: edge12 for (e, g.trans h, k), edge04 for (e.trans g, h, k), and edge43 for (e, g, h.trans k). Their relative source-valued defects vanish by the actual `Iso.self_symm_id`.

The new private `nativeGK5YPostCoherent` proves the needed context principle: a coherent genuine recursive whole NatIso Phi comparison remains coherent after postcomposing with an arbitrary further real pointwise equivalence z. It combines `nativeGK5YChangeIso_eqToIso`, `nativeGK5YTreePhi_eqToIso_square`, `nativeGK5YPostAtomSquare`, actual GK5Q composition comparisons, GK5U's unconditional whole two-stage recursive-Phi equality and `nativeGK5HChangeIso_trans`. The result retains true nonstrict unit/counit/compositor and does not simply assert strict inverse equality.

Apply this postcontext principle to GK5W's (e,g,h) genuine triple associativity and the fourth true equivalence k: `nativeGK5YEdge01_whole` and `nativeGK5YDefect01_refl` follow.

Finally use GK5X's previously certified genuine `nativeGK5XDirectDefectPentagon_whole`, plus the four now trivially identified defects, to prove the fifth `nativeGK5YDefect23_refl`. Its true whole NatIso edge identity `nativeGK5YEdge23_whole` follows by composing with the final direct Phi inverse. The complete public five-edge and five-defect conjunctions are certified with no extra assumptions.

The **12 public declarations audited by #print axioms** are: `nativeGK5YEdge01_whole`, `nativeGK5YEdge12_whole`, `nativeGK5YEdge23_whole`, `nativeGK5YEdge04_whole`, `nativeGK5YEdge43_whole`, `nativeGK5YDefect01_refl`, `nativeGK5YDefect12_refl`, `nativeGK5YDefect23_refl`, `nativeGK5YDefect04_refl`, `nativeGK5YDefect43_refl`, `nativeGK5YAllFiveEdges_whole` and `nativeGK5YAllFiveDefects_refl`.

## Exact Lean4 diagnostics, full-file inspection and final repair

The full 518-line changed Lean file, its imports and the complete relevant GK5D/G/H/Q/R/U/V/W/X signatures were examined, together with pinned Mathlib EqToHom, Equivalence, Whiskering, Iso groupoid APIs. Earlier failing exact-source runs were not interpreted as certification.

- **Triple-pasting proof:** The genuine GK5W `LeftDirectPhi` and `RightDirectPhi` terms contain structural `LeftTreeIso` / `RightTreeIso` wrappers. Simplification without explicitly factoring the equality-induced NatIso could not rewrite `eqToIso(congrArg TreeComposite (p.trans q))` into the appropriate product. The final proof uses explicit `eqToIso_trans` on both branches followed by the certified GK5W whole NatIso identity.
- **Inversion direction:** For `iso ≪≫ iso.symm` the correct pinned Mathlib lemma is `Iso.self_symm_id`, not `Iso.symm_self_id`, which applies in the opposite order. Corrected in all three initial local edge defects.
- **True recursive postcontext:** The initial normalization required explicit factorization of GK5Q's tree comparison by `eqToIso_trans`, explicit unfolding of `nativeGK5RSequentialCompositePhi` / `nativeGK5RSequentialPhi` (instead of unjustified `rfl`), and actual `Iso.trans_assoc` for the nested whole NatIso pasting. The final proof uses `congrArg` on real NatIso values and typed local let names; no middle unit/counit is strictified. These were structural Lean elaboration issues, not mathematical counterexamples, and the statements were not weakened.
- **Final completion:** The earlier three edge theorems and the generic postcontext lemma were first separately Strict Lean checked. The added edges 01/23 and both global conjunctions then passed in the final exact-source CI.

**Final CI #41408805373:** Strict Lean **3846/3846 SUCCESS**, all **12/12 #print axioms** depend only on `propext`, `Classical.choice`, `Quot.sound`; `sorryAx = 0`; changed-file Lean errors/warnings **0/0**. Independent Kuu and Governance SUCCESS. Source and squash Git trees are independently identical.

Pinned references: [Equivalence.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Equivalence.lean), [EqToHom.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/EqToHom.lean), [Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean).

## Scope, canonical authority and next task

The result holds for a **fixed universe pair** and every finite GK5D heterogeneously typed functor tree, under genuine indexed Mathlib equivalences. It does **not** prove strict equality of full Mathlib Equivalence records, original source-Q category axioms, unconditional F45 faithfulness, raw F54/F55/P92B Type-valued higher cells, global Gray reconstruction or unrestricted hyperdescent.

Canonical main, Lean **v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public root **107**, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 center, independent Kuu one presentation; protected validation-only PR **#1558** stays Draft/open/unmerged.

**Next GK5Z:** Compare this fully coherent *five-edge direct-Phi pentagon* with GK5F's general dependent index reindexing, including non-injective index maps and genuine unit, atom and paste constructors. Afterward investigate arbitrary finite-length equivalence-associahedron coherence by constructive induction, with the same authority and scope boundaries.

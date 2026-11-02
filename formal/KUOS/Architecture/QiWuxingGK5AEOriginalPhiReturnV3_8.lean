import KUOS.Architecture.QiWuxingGK5ADFivePhaseHolonomyV3_7
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AEClosedEndpointWholePhiTransport
import Mathlib.Tactic

/-!
Qi v3.8 / F112-P94D3GK5AE — the original genuinely recursive
five Mathlib whole NatIso Phi values after five real Qi/C60 steps.

The concrete order-five index map is the ORIGINAL
FivefoldIndex = FivePhase = ZMod 5, with the physical C60
gauge and original slotNext / around Edge / Dart geometry.
An actual proof (fivefoldPhaseFiveIndex_id) transports
the pulled-back dependent category family and both indexed
tree endpoints; each of the five whole Phi returns with
the source and target EqToIso boundaries explicitly shown.

Separately certify the categorical pentagon and the ORIGINAL
last physical edge as a pair of typed presentations. Edges 04 and 43
have the reversed physical cyclic orientation. There is no equality
of physical Edge and categorical NatIso or lost higher source
proof history. No new filler, source-Q axiom or Gray reconstruction.

This architecture file consumes independent Kuu GK5AE, never
the reverse. Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6,
append-only, same public root107, protected #1558 untouched.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe vC uC

/-- Categorical oriented edges e04, e43 genuinely traverse the
PHYSICAL positive slot cycle backwards. This preserves the
two different orientations instead of a false common arrow. -/
theorem fivefoldPhaseTwoReversedEdges :
    fivefoldFrom .e04 = fivefoldFoot .e04 + 1 ∧
    fivefoldFrom .e43 = fivefoldFoot .e43 + 1 := by
  decide

section OriginalFivePhiCycle
variable (frame : NativeC60FivePhaseGauge) (v : Vertex)
variable {C D E F G : Slot → Cat.{vC,uC}}
variable (e₁ : ∀ s : Slot, C s ≌ D s)
variable (e₂ : ∀ s : Slot, D s ≌ E s)
variable (e₃ : ∀ s : Slot, E s ≌ F s)
variable (e₄ : ∀ s : Slot, F s ≌ G s)


/-- The actual P0 independently recursive whole NatIso
returns to the original C60 phase-indexed category family
after five real Qi steps with BOTH endpoint EqToIso boundaries. -/
theorem fivefoldPhysicalPhi0_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t) := by
  exact nativeGK5AEFourDirectPhi0_return_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
    fivefoldPhaseReindexOne fivefoldPhaseFiveIndex_id t


/-- The actual P1 independently recursive whole NatIso
returns to the original C60 phase-indexed category family
after five real Qi steps with BOTH endpoint EqToIso boundaries. -/
theorem fivefoldPhysicalPhi1_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t) := by
  exact nativeGK5AEFourDirectPhi1_return_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
    fivefoldPhaseReindexOne fivefoldPhaseFiveIndex_id t


/-- The actual P2 independently recursive whole NatIso
returns to the original C60 phase-indexed category family
after five real Qi steps with BOTH endpoint EqToIso boundaries. -/
theorem fivefoldPhysicalPhi2_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t) := by
  exact nativeGK5AEFourDirectPhi2_return_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
    fivefoldPhaseReindexOne fivefoldPhaseFiveIndex_id t


/-- The actual P3 independently recursive whole NatIso
returns to the original C60 phase-indexed category family
after five real Qi steps with BOTH endpoint EqToIso boundaries. -/
theorem fivefoldPhysicalPhi3_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t) := by
  exact nativeGK5AEFourDirectPhi3_return_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
    fivefoldPhaseReindexOne fivefoldPhaseFiveIndex_id t


/-- The actual P4 independently recursive whole NatIso
returns to the original C60 phase-indexed category family
after five real Qi steps with BOTH endpoint EqToIso boundaries. -/
theorem fivefoldPhysicalPhi4_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t) := by
  exact nativeGK5AEFourDirectPhi4_return_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
    fivefoldPhaseReindexOne fivefoldPhaseFiveIndex_id t

/-- All five separately recursively constructed nonstrict whole Phi
return squares on the ORIGINAL Qi FivePhase and real C60 chart. -/
theorem fivefoldPhysicalAllFivePhi_original_return_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    ((nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t)) ∧
    ((nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t)) ∧
    ((nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t)) ∧
    ((nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t)) ∧
    ((nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5AEClosedFiveTree fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) u)) (nativeGK5AEClosedFiveTree_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) fivefoldPhaseFiveIndex_id t)) ≪≫
      nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t)) := by
  exact ⟨fivefoldPhysicalPhi0_original_return_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalPhi1_original_return_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalPhi2_original_return_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalPhi3_original_return_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalPhi4_original_return_whole frame v e₁ e₂ e₃ e₄ t⟩

/-- The actual physical fifth-around-edge closure and original
Mathlib categorical pentagon are simultaneous, TYPED facts with
different morphism types, not an invented higher identification.
The 04/43 reversal is retained explicitly. -/
theorem fivefoldPhysicalCategoricalParallelEvidence
    (p : FivefoldIndex)
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    (edgeEndpoints (fivefoldSide frame v (p + 4)) =
      (nativeC60GaugeDart frame v (p + 4),
       nativeC60GaugeDart frame v p)) ∧
    ((fivefoldCategoricalEdge (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        .e01 (nativeGK5DTreeComposite t) ≪≫
      fivefoldCategoricalEdge (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        .e12 (nativeGK5DTreeComposite t)) ≪≫
      fivefoldCategoricalEdge (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        .e23 (nativeGK5DTreeComposite t) =
      fivefoldCategoricalEdge (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        .e04 (nativeGK5DTreeComposite t) ≪≫
      fivefoldCategoricalEdge (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        .e43 (nativeGK5DTreeComposite t)) ∧
    (fivefoldFrom .e04 = fivefoldFoot .e04 + 1 ∧
     fivefoldFrom .e43 = fivefoldFoot .e43 + 1) := by
  exact ⟨fivefoldPhaseLastPhysicalSide_closed frame v p,
    fivefoldCategoricalPentagon (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
      (nativeGK5DTreeComposite t),
    fivefoldPhaseTwoReversedEdges⟩

#print axioms fivefoldPhysicalPhi0_original_return_whole
#print axioms fivefoldPhysicalPhi1_original_return_whole
#print axioms fivefoldPhysicalPhi2_original_return_whole
#print axioms fivefoldPhysicalPhi3_original_return_whole
#print axioms fivefoldPhysicalPhi4_original_return_whole
#print axioms fivefoldPhysicalAllFivePhi_original_return_whole
#print axioms fivefoldPhysicalCategoricalParallelEvidence
#print axioms fivefoldPhaseTwoReversedEdges

end OriginalFivePhiCycle

end
end KUOS.Architecture.WuxingPentagonUnified

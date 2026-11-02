import KUOS.Architecture.QiWuxingPentagonUnifiedV3_5
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ACIdentityReindexPhiAction
import Mathlib.Tactic

/-!
Qi v3.6 / F112-P94D3GK5AC — SAME actual Qi FivePhase index
links a genuine C60 five-slot gauge and all five GK5 independent
recursive whole NatIso Φ under compositional typed reindexing.

This architecture-side bridge imports independent Kuu, NEVER the
reverse. Actual physical rotation slotNext is conjugate to Qi +1 by
the existing genuine fivefoldSlotEquiv; the typed index maps
(phase +1) then (physical chart) retain exact whole EqToIso
coherence from GK5AA/GK5AB, for all five actual equivalence
parenthesizations. GK5AC establishes the identity unit separately.

This does not identify C60 physical edges and categorical NatIsos
as the same morphisms. They share a proved phase/chart map and
dependent-index transport, not a fabricated raw higher cell.

Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, root107, protected #1558 Draft/open.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe vC uC

/-- Qi's very same phase carrier; +1 is its genuine cyclic successor. -/
def fivefoldPhaseReindexOne : FivefoldIndex → FivefoldIndex :=
  fun p => p + 1

/-- A genuine C60 pentagon chart intertwines physical slotNext with
the SAME Qi +1 phase reindexing map. -/
theorem fivefoldPhaseReindexOne_physical
    (frame : NativeC60FivePhaseGauge) (v : Vertex) :
    (fun p : FivefoldIndex =>
      fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)) =
    (fun p : FivefoldIndex =>
      slotNext (fivefoldSlotEquiv frame v p)) := by
  funext p
  exact (fivefoldSlot_successor frame v p).symm

/-- The physical chart's true inverse is a two-sided phase index
inverse; this is not an equality of raw higher-categorical cells. -/
theorem fivefoldPhaseGauge_roundtrip
    (frame : NativeC60FivePhaseGauge) (v : Vertex) :
    (fun p : FivefoldIndex =>
      (fivefoldSlotEquiv frame v).symm
        (fivefoldSlotEquiv frame v p)) =
      (id : FivefoldIndex → FivefoldIndex) := by
  funext p
  exact (fivefoldSlotEquiv frame v).symm_apply_apply p

/-- The true category family round-trip uses exactly the
Qi FivePhase/physical Slot equivalence, including all 5 phases. -/
theorem fivefoldPhaseGauge_categories_roundtrip
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (C : FivefoldIndex → Cat.{vC,uC}) :
    (fun p : FivefoldIndex =>
      C ((fivefoldSlotEquiv frame v).symm
        (fivefoldSlotEquiv frame v p))) = C := by
  funext p
  exact congrArg C ((fivefoldSlotEquiv frame v).symm_apply_apply p)

/-- A TRUE fully dependent typed tree reclassified by Qi +1 then by
the physical C60 slot chart equals its one-step composite relabeling. -/
theorem fivefoldPhaseStep_treeReindex_comp
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (C : Slot → Cat.{vC,uC})
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    nativeGK5FTreeReindex (fivefoldSlotEquiv frame v) C
      (nativeGK5FTreeReindex fivefoldPhaseReindexOne
        (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t) =
    nativeGK5FTreeReindex
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)) C t :=
  nativeGK5FTreeReindex_comp
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v) C t

section FivefoldPhasePhysicalPhi
variable (frame : NativeC60FivePhaseGauge) (v : Vertex)
variable {C D E F G : Slot → Cat.{vC,uC}}
variable (e₁ : ∀ s : Slot, C s ≌ D s)
variable (e₂ : ∀ s : Slot, D s ≌ E s)
variable (e₃ : ∀ s : Slot, E s ≌ F s)
variable (e₄ : ∀ s : Slot, F s ≌ G s)


/-- The P0 independently recursive whole NatIso Φ transports by
Qi's real phase successor then the C60 chart exactly as by their
composite, representing actual slotNext by fivefoldPhaseReindexOne_physical. -/
theorem fivefoldPhasePhysicalPhi0_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    ((nativeGK5XDirectPhi0
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket0
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi0
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t := by
  exact nativeGK5ABFourDirectPhi0_recursiveComp_whole
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v)
    e₁ e₂ e₃ e₄ t


/-- The P1 independently recursive whole NatIso Φ transports by
Qi's real phase successor then the C60 chart exactly as by their
composite, representing actual slotNext by fivefoldPhaseReindexOne_physical. -/
theorem fivefoldPhasePhysicalPhi1_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    ((nativeGK5XDirectPhi1
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket1
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi1
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t := by
  exact nativeGK5ABFourDirectPhi1_recursiveComp_whole
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v)
    e₁ e₂ e₃ e₄ t


/-- The P2 independently recursive whole NatIso Φ transports by
Qi's real phase successor then the C60 chart exactly as by their
composite, representing actual slotNext by fivefoldPhaseReindexOne_physical. -/
theorem fivefoldPhasePhysicalPhi2_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    ((nativeGK5XDirectPhi2
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket2
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi2
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t := by
  exact nativeGK5ABFourDirectPhi2_recursiveComp_whole
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v)
    e₁ e₂ e₃ e₄ t


/-- The P3 independently recursive whole NatIso Φ transports by
Qi's real phase successor then the C60 chart exactly as by their
composite, representing actual slotNext by fivefoldPhaseReindexOne_physical. -/
theorem fivefoldPhasePhysicalPhi3_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    ((nativeGK5XDirectPhi3
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket3
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi3
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t := by
  exact nativeGK5ABFourDirectPhi3_recursiveComp_whole
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v)
    e₁ e₂ e₃ e₄ t


/-- The P4 independently recursive whole NatIso Φ transports by
Qi's real phase successor then the C60 chart exactly as by their
composite, representing actual slotNext by fivefoldPhaseReindexOne_physical. -/
theorem fivefoldPhasePhysicalPhi4_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    ((nativeGK5XDirectPhi4
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket4
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi4
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t := by
  exact nativeGK5ABFourDirectPhi4_recursiveComp_whole
    fivefoldPhaseReindexOne (fivefoldSlotEquiv frame v)
    e₁ e₂ e₃ e₄ t

/-- All five nonstrict independent direct recursive Φ computations
share the actual Qi phase successor/C60 physical slotNext chart.
The source and target transport boundaries are genuine whole NatIsos. -/
theorem fivefoldPhasePhysicalAllFivePhi_comp_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        C (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) i j) :
    (((nativeGK5XDirectPhi0
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket0
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi0
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5XDirectPhi1
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket1
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi1
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5XDirectPhi2
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket2
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi2
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5XDirectPhi3
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket3
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi3
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5XDirectPhi4
      (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p)))
      (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldPhaseReindexOne
        (nativeGK5XBracket4
          (fun p : FivefoldIndex => e₁ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₂ (fivefoldSlotEquiv frame v p))
          (fun p : FivefoldIndex => e₃ (fivefoldSlotEquiv frame v p)) (fun p : FivefoldIndex => e₄ (fivefoldSlotEquiv frame v p))) t)) ≪≫
      eqToIso (nativeGK5AASingleTargetEq fivefoldSlotEquiv frame v
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
        (nativeGK5FTreeReindex fivefoldPhaseReindexOne
          (fun p : FivefoldIndex => C (fivefoldSlotEquiv frame v p)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp
          fivefoldPhaseReindexOne fivefoldSlotEquiv frame v C t)) =
    nativeGK5ZTransportedPhi4
      (fun p : FivefoldIndex =>
        fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne p))
      e₁ e₂ e₃ e₄ t) := by
  exact ⟨fivefoldPhasePhysicalPhi0_comp_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhasePhysicalPhi1_comp_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhasePhysicalPhi2_comp_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhasePhysicalPhi3_comp_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhasePhysicalPhi4_comp_whole frame v e₁ e₂ e₃ e₄ t⟩

#print axioms fivefoldPhasePhysicalAllFivePhi_comp_whole
#print axioms fivefoldPhasePhysicalPhi0_comp_whole
#print axioms fivefoldPhasePhysicalPhi1_comp_whole
#print axioms fivefoldPhasePhysicalPhi2_comp_whole
#print axioms fivefoldPhasePhysicalPhi3_comp_whole
#print axioms fivefoldPhasePhysicalPhi4_comp_whole

end FivefoldPhasePhysicalPhi

#print axioms fivefoldPhaseReindexOne_physical
#print axioms fivefoldPhaseGauge_roundtrip
#print axioms fivefoldPhaseGauge_categories_roundtrip
#print axioms fivefoldPhaseStep_treeReindex_comp

end
end KUOS.Architecture.WuxingPentagonUnified

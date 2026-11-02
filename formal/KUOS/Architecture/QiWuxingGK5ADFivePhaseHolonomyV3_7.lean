import KUOS.Architecture.QiWuxingGK5ACFivePhaseShiftCoherenceV3_6
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ADFiveStepIndexPhiHolonomy
import Mathlib.Tactic

/-!
Qi v3.7 / F112-P94D3GK5AD: the actual FivePhase = ZMod 5
five-step cyclic action, real C60 pentagon physical return,
and all five independently recursive whole Mathlib NatIso Phi
dependent-index transport squares.

This is downstream of independent Kuu. The original C60
Vertex/Slot/Edge/Dart and physical gauge remain unchanged.
There is no fabricated graph, no equality between physical
edges and categorical NatIsos, and no source-history collapse.
Five-step whole Phi squares retain source and target eqToIso.
No strictification of chosen inverse, unit/counit/compositor.

Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, 107 public roots, protected #1558 unchanged.
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

/-- The fifth genuine Qi +1 index reclassification is identity. -/
theorem fivefoldPhaseFiveIndex_id :
    nativeGK5ADFiveIndex fivefoldPhaseReindexOne =
      (id : FivefoldIndex → FivefoldIndex) := by
  funext p
  change p + 1 + 1 + 1 + 1 + 1 = p
  calc
    _ = p + (5 : FivefoldIndex) := by ring
    _ = p := by simp

/-- Five physical slotNext steps return the SAME C60 physical slot. -/
theorem fivefoldSlotNext_five (s : Slot) :
    slotNext (slotNext (slotNext (slotNext (slotNext s)))) = s := by
  cases s <;> decide

/-- Five actual phase steps are conjugate to five real physical
slotNext steps by the existing true C60 gauge. -/
theorem fivefoldPhaseFive_physical
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex) :
    fivefoldSlotEquiv frame v
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne p) =
    slotNext (slotNext (slotNext (slotNext
      (slotNext (fivefoldSlotEquiv frame v p))))) := by
  have h (x : FivefoldIndex) :
      fivefoldSlotEquiv frame v (fivefoldPhaseReindexOne x) =
        slotNext (fivefoldSlotEquiv frame v x) :=
    congrFun (fivefoldPhaseReindexOne_physical frame v) x
  simp only [nativeGK5ADFiveIndex, h]

/-- The true physical pentagon holonomy closes. -/
theorem fivefoldPhasePhysicalFive_closed
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex) :
    slotNext (slotNext (slotNext (slotNext
      (slotNext (fivefoldSlotEquiv frame v p))))) =
      fivefoldSlotEquiv frame v p := by
  calc
    _ = fivefoldSlotEquiv frame v
          (nativeGK5ADFiveIndex fivefoldPhaseReindexOne p) :=
        (fivefoldPhaseFive_physical frame v p).symm
    _ = fivefoldSlotEquiv frame v p := by
      rw [fivefoldPhaseFiveIndex_id]
      rfl

/-- The fifth ORIGINAL C60 around-edge returns from the fourth
phase dart to the first phase dart on the same physical pentagon. -/
theorem fivefoldPhaseLastPhysicalSide_closed
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex) :
    edgeEndpoints (fivefoldSide frame v (p + 4)) =
      (nativeC60GaugeDart frame v (p + 4),
       nativeC60GaugeDart frame v p) := by
  rw [fivefoldSide_endpoints frame v (p + 4)]
  have h : p + 4 + 1 = p := by
    calc
      _ = p + (5 : FivefoldIndex) := by ring
      _ = p := by simp
  rw [h]

/-- A single original gauge chart selects the same indexed category. -/
abbrev fivefoldPhaseCategory
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (C : Slot → Cat.{vC,uC}) : FivefoldIndex → Cat.{vC,uC} :=
  fun p => C (fivefoldSlotEquiv frame v p)

/-- The same chart transports the actual pointwise Mathlib equivalence. -/
abbrev fivefoldPhaseEquivalence
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    {C D : Slot → Cat.{vC,uC}}
    (e : ∀ s : Slot, C s ≌ D s) :
    ∀ p : FivefoldIndex,
      fivefoldPhaseCategory frame v C p ≌
        fivefoldPhaseCategory frame v D p :=
  fun p => e (fivefoldSlotEquiv frame v p)

/-- The genuine category family returns after five Qi steps. -/
theorem fivefoldPhaseFamilyFive_closed
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (C : Slot → Cat.{vC,uC}) :
    (fun p : FivefoldIndex =>
      fivefoldPhaseCategory frame v C
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne p)) =
      fivefoldPhaseCategory frame v C := by
  exact nativeGK5ADFiveFamily_closed
    fivefoldPhaseReindexOne
    (fivefoldPhaseCategory frame v C)
    fivefoldPhaseFiveIndex_id

/-- Five genuinely dependent typed-tree relabelings equal a
single actual composite relabeling on the original C60 chart. -/
theorem fivefoldPhaseTreeFive_reindex_eq
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (C : Slot → Cat.{vC,uC})
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun p : FivefoldIndex =>
        fivefoldPhaseCategory frame v C
          (nativeGK5ADFiveIndex fivefoldPhaseReindexOne p)) i j) :
    nativeGK5ADFiveTreeReindex
        fivefoldPhaseReindexOne
        (fivefoldPhaseCategory frame v C) t =
      nativeGK5FTreeReindex
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseCategory frame v C) t :=
  nativeGK5ADFiveTreeReindex_eq
    fivefoldPhaseReindexOne
    (fivefoldPhaseCategory frame v C) t

section FivefoldWholePhiHolonomy
variable (frame : NativeC60FivePhaseGauge) (v : Vertex)
variable {C D E F G : Slot → Cat.{vC,uC}}
variable (e₁ : ∀ s : Slot, C s ≌ D s)
variable (e₂ : ∀ s : Slot, D s ≌ E s)
variable (e₃ : ∀ s : Slot, E s ≌ F s)
variable (e₄ : ∀ s : Slot, F s ≌ G s)


/-- P0: a WHOLE genuine recursive NatIso on the original
C60 gauge family commutes with five real phase reclassifications,
with both actual equality-induced source/target transports. -/
theorem fivefoldPhysicalDirectPhi0_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    (nativeGK5XDirectPhi0
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) := by
  exact nativeGK5ADFiveDirectPhi0_reindex_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) fivefoldPhaseReindexOne t


/-- P1: a WHOLE genuine recursive NatIso on the original
C60 gauge family commutes with five real phase reclassifications,
with both actual equality-induced source/target transports. -/
theorem fivefoldPhysicalDirectPhi1_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    (nativeGK5XDirectPhi1
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) := by
  exact nativeGK5ADFiveDirectPhi1_reindex_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) fivefoldPhaseReindexOne t


/-- P2: a WHOLE genuine recursive NatIso on the original
C60 gauge family commutes with five real phase reclassifications,
with both actual equality-induced source/target transports. -/
theorem fivefoldPhysicalDirectPhi2_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    (nativeGK5XDirectPhi2
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) := by
  exact nativeGK5ADFiveDirectPhi2_reindex_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) fivefoldPhaseReindexOne t


/-- P3: a WHOLE genuine recursive NatIso on the original
C60 gauge family commutes with five real phase reclassifications,
with both actual equality-induced source/target transports. -/
theorem fivefoldPhysicalDirectPhi3_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    (nativeGK5XDirectPhi3
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) := by
  exact nativeGK5ADFiveDirectPhi3_reindex_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) fivefoldPhaseReindexOne t


/-- P4: a WHOLE genuine recursive NatIso on the original
C60 gauge family commutes with five real phase reclassifications,
with both actual equality-induced source/target transports. -/
theorem fivefoldPhysicalDirectPhi4_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    (nativeGK5XDirectPhi4
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) := by
  exact nativeGK5ADFiveDirectPhi4_reindex_whole
    (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) fivefoldPhaseReindexOne t

/-- All five separately recursively built genuine Mathlib whole Phi
agree between five successive real Qi/C60 typed reclassifications
and their one-shot composite. Order five is certified independently. -/
theorem fivefoldPhysicalAllFivePhi_five_whole
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree
      (fun x : FivefoldIndex => (fivefoldPhaseCategory frame v C) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) i j) :
    ((nativeGK5XDirectPhi0
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t))) ∧
    ((nativeGK5XDirectPhi1
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t))) ∧
    ((nativeGK5XDirectPhi2
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t))) ∧
    ((nativeGK5XDirectPhi3
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t))) ∧
    ((nativeGK5XDirectPhi4
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₁) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₂) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₃) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x))
      (fun x : FivefoldIndex => (fivefoldPhaseEquivalence frame v e₄) ((nativeGK5ADFiveIndex fivefoldPhaseReindexOne) x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex fivefoldPhaseReindexOne)
        (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄) s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t).symm)) ≪≫
      nativeGK5XDirectPhi4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄)
        (nativeGK5ADFiveTreeReindex fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 (fivefoldPhaseEquivalence frame v e₁) (fivefoldPhaseEquivalence frame v e₂) (fivefoldPhaseEquivalence frame v e₃) (fivefoldPhaseEquivalence frame v e₄))
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq fivefoldPhaseReindexOne (fivefoldPhaseCategory frame v C) t))) := by
  exact ⟨fivefoldPhysicalDirectPhi0_five_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalDirectPhi1_five_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalDirectPhi2_five_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalDirectPhi3_five_whole frame v e₁ e₂ e₃ e₄ t,
    fivefoldPhysicalDirectPhi4_five_whole frame v e₁ e₂ e₃ e₄ t⟩

#print axioms fivefoldPhysicalAllFivePhi_five_whole
#print axioms fivefoldPhysicalDirectPhi0_five_whole
#print axioms fivefoldPhysicalDirectPhi1_five_whole
#print axioms fivefoldPhysicalDirectPhi2_five_whole
#print axioms fivefoldPhysicalDirectPhi3_five_whole
#print axioms fivefoldPhysicalDirectPhi4_five_whole

end FivefoldWholePhiHolonomy

#print axioms fivefoldPhaseFiveIndex_id
#print axioms fivefoldSlotNext_five
#print axioms fivefoldPhaseFive_physical
#print axioms fivefoldPhasePhysicalFive_closed
#print axioms fivefoldPhaseLastPhysicalSide_closed
#print axioms fivefoldPhaseFamilyFive_closed
#print axioms fivefoldPhaseTreeFive_reindex_eq

end
end KUOS.Architecture.WuxingPentagonUnified

import KUOS.Architecture.QiWuxingGK5AHTypedNorthHistoryBridgeV4_1
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AIStructuralF55WholeCellBridge
import Mathlib.Tactic

/-!
Qi v4.2 / F112-P94D3GK5AI — actual north C60 physical
boundary, original F55 HIGHER-CELL proof history, structurally
translated P92B Type values and genuine GK5AF whole NatIso.

GK5AH/Qi v4.1 retained original F54 raw 2-Nat route histories.
Here the two DIFFERENT original F55 3-proof histories between
the SAME original F54 3-vs-2 pentagon routes are tested against:
 - the actual north C60 fifth around-edge Dart endpoints,
 - BOTH full original typed F54 source and target history fibers,
 - the actual P92B proof-existence quotient and its equality,
 - the genuinely independent Mathlib whole-NatIso 01;12;23=04;43,
 - a stronger TYPE-valued P92B structural 3-cell from GK5AI.

Adding physical endpoints, full F54 histories, P92B classes and
whole NatIso alone still forgets which F55 3-PROOF occurred.
The actual structurally translated TYPE-valued P92B comparison
distinguishes the two chosen F55 witnesses. Retaining the full
F55 proof in the typed whole-NatIso packet is injective.

The categorical 04 and 43 remain oppositely oriented relative
to the actual positive physical C60 cycle. No Edge=NatIso
equation, global F54-to-whole functor, unrestricted gluing, or
fabricated higher filler is introduced. The extra P92B
assocNaturality is NOT old F55 evidence.

Qi imports independent Kuu, never conversely. Append-only,
same public root107, no Gray. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide or new axioms.
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

/-- Real ORIGINAL physical C60 Dart endpoints together with the
full STRUCTURAL P92B Type-valued witness (not the existence
quotient) of the original F55 pentagon comparison. -/
def fivefoldGK5AIPhysicalStructuralP92Cell
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
    (cell : NativeGK5AINorthPentagonCells) :
    (Dart × Dart) ×
      NativeF55P92AssocComparison (.pentagon .north)
        northNativeF45PentagonLong northNativeF45PentagonShort :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    nativeGK5AIOriginalToP92Structural cell)

/-- Even with the SAME physical Dart pair and SAME original F54
start/end routes, the selected P92B Type-valued structural map
DISTINGUISHES the genuine original pentagon 3-proof from its
identity-postcomposed 3-proof. -/
theorem fivefoldGK5AIStructuralP92Proofs_distinct
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    fivefoldGK5AIPhysicalStructuralP92Cell frame p
      nativeGK5AGNorthOriginalCell ≠
    fivefoldGK5AIPhysicalStructuralP92Cell frame p
      nativeGK5AINorthPentagonWithIdentity := by
  intro h
  exact nativeGK5AINorthStructuralProofs_distinct
    (congrArg Prod.snd h)

section GenuineWhole
variable (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
variable {C D E F G : Slot → Cat.{vC,uC}}
variable (e₁ : ∀ s : Slot, C s ≌ D s)
variable (e₂ : ∀ s : Slot, D s ≌ E s)
variable (e₃ : ∀ s : Slot, E s ≌ F s)
variable (e₄ : ∀ s : Slot, F s ≌ G s)
variable {i j : FivefoldIndex}
variable (R : fivefoldPhaseCategory frame .north C i ⥤
  fivefoldPhaseCategory frame .north C j)

/-- Exactly the observable physical / original F54-boundary /
P92B-existence / whole-NatIso data. The two proof fields live in
Prop and therefore CANNOT carry the original F55 Type-valued
3-PROOF HISTORY, despite being derived from its real P92B map. -/
structure FivefoldGK5AITruncatedThreeCellBoundary where
  physicalDarts : Dart × Dart
  sourceHistory : NativeGK5AHNorthHistoryFiber
  targetHistory : NativeGK5AHNorthHistoryFiber
  sourceClass : NativeGK5AHNorthP92Classes
  wholeNatIso : FivefoldGK5AGNorthWhole frame e₁ e₂ e₃ e₄ R
  originalClassComparison :
    nativeGK5AGNorthP92Class northNativeF45PentagonLong =
      nativeGK5AGNorthP92Class northNativeF45PentagonShort
  categoricalWholeComparison :
    nativeGK5AFLongPath
      (fivefoldPhaseEquivalence frame .north e₁)
      (fivefoldPhaseEquivalence frame .north e₂)
      (fivefoldPhaseEquivalence frame .north e₃)
      (fivefoldPhaseEquivalence frame .north e₄) R =
    nativeGK5AFShortPath
      (fivefoldPhaseEquivalence frame .north e₁)
      (fivefoldPhaseEquivalence frame .north e₂)
      (fivefoldPhaseEquivalence frame .north e₃)
      (fivefoldPhaseEquivalence frame .north e₄) R

/-- The P92B quotient-equality evidence really is derived from
the input F55 proof via GK5AI's structural translation; the
full proof term is intentionally not stored in this truncated
physical/categorical observation. -/
def fivefoldGK5AITruncatedThreeCellReadout
    (cell : NativeGK5AINorthPentagonCells) :
    FivefoldGK5AITruncatedThreeCellBoundary frame e₁ e₂ e₃ e₄ R where
  physicalDarts := fivefoldGK5AGNorthPhysicalFifthDarts frame p
  sourceHistory := nativeGK5AHEmbed northNativeF45PentagonLong
  targetHistory := nativeGK5AHEmbed northNativeF45PentagonShort
  sourceClass := nativeGK5AGNorthP92Class northNativeF45PentagonLong
  wholeNatIso := nativeGK5AFLongPath
    (fivefoldPhaseEquivalence frame .north e₁)
    (fivefoldPhaseEquivalence frame .north e₂)
    (fivefoldPhaseEquivalence frame .north e₃)
    (fivefoldPhaseEquivalence frame .north e₄) R
  originalClassComparison :=
    nativeF55P92AssocRouteClass_eq_of_cell _ _
      (nativeGK5AIOriginalToP92Structural cell)
  categoricalWholeComparison :=
    nativeGK5AFPaths_whole
      (fivefoldPhaseEquivalence frame .north e₁)
      (fivefoldPhaseEquivalence frame .north e₂)
      (fivefoldPhaseEquivalence frame .north e₃)
      (fivefoldPhaseEquivalence frame .north e₄) R

/-- Two distinct ORIGINAL F55 3-CELL proof histories yield
identical genuine C60 physical boundaries, complete F54 endpoint
histories, P92B quotient data, and whole Mathlib NatIso comparison.
Even the actual quotient and whole Eq certificates are unchanged
by proof irrelevance. -/
theorem fivefoldGK5AITruncatedThreeCell_two_equal :
    fivefoldGK5AITruncatedThreeCellReadout
      frame p e₁ e₂ e₃ e₄ R nativeGK5AGNorthOriginalCell =
    fivefoldGK5AITruncatedThreeCellReadout
      frame p e₁ e₂ e₃ e₄ R
        nativeGK5AINorthPentagonWithIdentity := by
  rfl

/-- A concrete and unconditional HIGHER-CELL history
nonfaithfulness obstruction for this precise physical/P92B/whole
readout, stronger than GK5AH's RAW F54 object obstruction. -/
theorem fivefoldGK5AITruncatedThreeCell_not_injective :
    ¬ Function.Injective
      (fivefoldGK5AITruncatedThreeCellReadout
        frame p e₁ e₂ e₃ e₄ R) := by
  intro hinj
  apply nativeGK5AINorthTwoOriginalCells_distinct
  apply hinj
  exact fivefoldGK5AITruncatedThreeCell_two_equal
    frame p e₁ e₂ e₃ e₄ R

/-- No left inverse can reconstruct original F55 proof HISTORY
from the genuine physical endpoints and selected 0-truncated
P92B/whole-NatIso boundary readout, even retaining BOTH complete
original F54 source and target route values. -/
theorem fivefoldGK5AINoTruncatedThreeCellRecovery :
    ¬ ∃ recover :
        FivefoldGK5AITruncatedThreeCellBoundary
          frame e₁ e₂ e₃ e₄ R → NativeGK5AINorthPentagonCells,
      ∀ cell : NativeGK5AINorthPentagonCells,
        recover (fivefoldGK5AITruncatedThreeCellReadout
          frame p e₁ e₂ e₃ e₄ R cell) = cell := by
  rintro ⟨recover, hreturn⟩
  apply fivefoldGK5AITruncatedThreeCell_not_injective
    frame p e₁ e₂ e₃ e₄ R
  intro x y hxy
  exact (hreturn x).symm.trans
    ((congrArg recover hxy).trans (hreturn y))

/-- The actual physical Dart pair together with the FULL
proof-relevant GK5AI F55/P92B/whole-NatIso packet is injective
on the original F55 3-cell proof terms, without identifying
physical C60 Edges with categorical whole NatIso values. -/
def fivefoldGK5AIPhysicalProofRelevantWholePacket
    (cell : NativeGK5AINorthPentagonCells) :
    (Dart × Dart) ×
      NativeGK5AIOriginalWholeCellPacket
        (fivefoldPhaseEquivalence frame .north e₁)
        (fivefoldPhaseEquivalence frame .north e₂)
        (fivefoldPhaseEquivalence frame .north e₃)
        (fivefoldPhaseEquivalence frame .north e₄) R :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    nativeGK5AILocalWholePacket
      (fivefoldPhaseEquivalence frame .north e₁)
      (fivefoldPhaseEquivalence frame .north e₂)
      (fivefoldPhaseEquivalence frame .north e₃)
      (fivefoldPhaseEquivalence frame .north e₄) R cell)

theorem fivefoldGK5AIPhysicalProofRelevantWhole_injective :
    Function.Injective
      (fivefoldGK5AIPhysicalProofRelevantWholePacket
        frame p e₁ e₂ e₃ e₄ R) := by
  intro x y hxy
  exact nativeGK5AILocalWholePacket_injective
    (fivefoldPhaseEquivalence frame .north e₁)
    (fivefoldPhaseEquivalence frame .north e₂)
    (fivefoldPhaseEquivalence frame .north e₃)
    (fivefoldPhaseEquivalence frame .north e₄) R
      (congrArg Prod.snd hxy)

/-- The categorical edges 04 and 43 remain REVERSED against
the real positive C60 Dart orientation, alongside the separate
proof-term distinctions. This is a truly physical source
obstruction, not an invented physical-to-NatIso higher filler. -/
theorem fivefoldGK5AIStructuralAndOrientationWitnesses :
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) ∧
    (fivefoldGK5AIPhysicalStructuralP92Cell frame p
      nativeGK5AGNorthOriginalCell ≠
     fivefoldGK5AIPhysicalStructuralP92Cell frame p
      nativeGK5AINorthPentagonWithIdentity) ∧
    (fivefoldGK5AITruncatedThreeCellReadout
      frame p e₁ e₂ e₃ e₄ R nativeGK5AGNorthOriginalCell =
     fivefoldGK5AITruncatedThreeCellReadout
      frame p e₁ e₂ e₃ e₄ R
        nativeGK5AINorthPentagonWithIdentity) := by
  exact ⟨(fivefoldGK5AFBothReverseObstructions frame .north).1,
    (fivefoldGK5AFBothReverseObstructions frame .north).2,
    fivefoldGK5AIStructuralP92Proofs_distinct frame p,
    fivefoldGK5AITruncatedThreeCell_two_equal
      frame p e₁ e₂ e₃ e₄ R⟩

#print axioms fivefoldGK5AITruncatedThreeCellReadout
#print axioms fivefoldGK5AITruncatedThreeCell_two_equal
#print axioms fivefoldGK5AITruncatedThreeCell_not_injective
#print axioms fivefoldGK5AINoTruncatedThreeCellRecovery
#print axioms fivefoldGK5AIPhysicalProofRelevantWhole_injective
#print axioms fivefoldGK5AIStructuralAndOrientationWitnesses
end GenuineWhole

#print axioms fivefoldGK5AIStructuralP92Proofs_distinct

end
end KUOS.Architecture.WuxingPentagonUnified

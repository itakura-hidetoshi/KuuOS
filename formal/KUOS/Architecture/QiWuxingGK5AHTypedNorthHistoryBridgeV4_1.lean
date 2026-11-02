import KUOS.Architecture.QiWuxingGK5AGOriginalNorthHistoryDescentV4_0
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AHTypedHistoryComparisonInterface
import Mathlib.Tactic

/-!
Qi v4.1 / F112-P94D3GK5AH — genuine C60 physical orientation
with original Type-valued history-sensitive comparison fibers.

Uses existing common FivefoldIndex = ZMod 5 and FivePhase gauge,
the actual north C60 fifth physical Edge/Dart endpoints, and the
independent-Kuu GK5AH full F54-shaped (two-Nat, two-category) route
fiber with the ORIGINAL F55 3-cell and its selected P92B image.

Storing the original full history fiber alongside physical darts is
injective; retaining ONLY physical darts and the P92B class is not,
and has no full-history recovery.  Conditional matched whole NatIso
readouts are also nonfaithful. The true reversed physical directions
of the categorical 04 and 43 edges are independently retained.

No physical Edge equals a Mathlib NatIso; no hypothetical higher
filler, historical KUOS-F54 equivalence, or unbounded descent is
asserted. Qi imports independent Kuu, not conversely. Append-only,
same public root107. Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Original north C60 physical fifth edge AND the FULL Kuu GK5AH
F54-history fiber, not the lossy comparison class alone. -/
def fivefoldGK5AHNorthPhysicalHistoryFiber
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
    (route : NativeGK5AGNorthHistory) :
    (Dart × Dart) × NativeGK5AHNorthHistoryFiber :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    nativeGK5AHEmbed route)

/-- The REAL C60 physical Dart boundary does not collapse the
fully tagged original dependent route history. -/
theorem fivefoldGK5AHNorthPhysicalFiber_injective
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    Function.Injective (fivefoldGK5AHNorthPhysicalHistoryFiber frame p) := by
  intro r s h
  exact nativeGK5AHEmbed_injective (congrArg Prod.snd h)

/-- Forgetting raw F54 history in favor of its P92B class is a
separate, deliberately lossy physical observation. -/
def fivefoldGK5AHNorthPhysicalP92Readout
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
    (fiber : NativeGK5AHNorthHistoryFiber) :
    (Dart × Dart) × NativeGK5AHNorthP92Classes :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p, fiber.comparisonClass)

/-- Actual 3-vs-2 north pentagon paths differ as full histories,
but have the same real physical Dart endpoints and P92B class. -/
theorem fivefoldGK5AHNorthPhysicalP92_not_injective
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    ¬ Function.Injective (fivefoldGK5AHNorthPhysicalP92Readout frame p) := by
  intro hinj
  apply nativeGK5AHNorthFibers_distinct
  apply hinj
  apply Prod.ext
  · rfl
  · exact nativeGK5AHOriginalComparison_classes_equal
      nativeGK5AHNorthOriginalComparison

/-- There cannot be a section restoring the original GK5AH
full history fiber from the real physical Dart/P92B readout. -/
theorem fivefoldGK5AHNorthNoPhysicalP92FiberRecovery
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    ¬ ∃ recover :
        ((Dart × Dart) × NativeGK5AHNorthP92Classes) →
          NativeGK5AHNorthHistoryFiber,
      ∀ route : NativeGK5AGNorthHistory,
        recover (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
          nativeGK5AGNorthP92Class route) = nativeGK5AHEmbed route := by
  rintro ⟨recover, hreturn⟩
  apply nativeGK5AHNorthNoP92FiberRetraction
  refine ⟨fun cls => recover
    (fivefoldGK5AGNorthPhysicalFifthDarts frame p, cls), ?_⟩
  intro route
  exact hreturn route

/-- One actual north C60 fifth physical closure, one ORIGINAL
Type-valued F55 3-cell across unequal history fibers, their
selected P92B class equality and BOTH correct reversed physical
categorical 04/43 directions, as separate typed presentations. -/
theorem fivefoldGK5AHTypedNorthOrientationEvidence
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame p =
      (nativeC60GaugeDart frame .north (p + 4),
       nativeC60GaugeDart frame .north p)) ∧
    Nonempty (NativeGK5AHOriginalComparison
      (nativeGK5AHEmbed northNativeF45PentagonLong)
      (nativeGK5AHEmbed northNativeF45PentagonShort)) ∧
    (nativeGK5AHEmbed northNativeF45PentagonLong ≠
      nativeGK5AHEmbed northNativeF45PentagonShort) ∧
    ((nativeGK5AHEmbed northNativeF45PentagonLong).comparisonClass =
      (nativeGK5AHEmbed northNativeF45PentagonShort).comparisonClass) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  exact ⟨fivefoldPhaseLastPhysicalSide_closed_kernel frame .north p,
    ⟨nativeGK5AHNorthOriginalComparison⟩,
    nativeGK5AHNorthFibers_distinct,
    nativeGK5AHOriginalComparison_classes_equal
      nativeGK5AHNorthOriginalComparison,
    (fivefoldGK5AFBothReverseObstructions frame .north).1,
    (fivefoldGK5AFBothReverseObstructions frame .north).2⟩

section ConditionalWholeNatIso
variable (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
variable {C D E F G : Slot → Cat.{vC,uC}}
variable (e₁ : ∀ s : Slot, C s ≌ D s)
variable (e₂ : ∀ s : Slot, D s ≌ E s)
variable (e₃ : ∀ s : Slot, E s ≌ F s)
variable (e₄ : ∀ s : Slot, F s ≌ G s)
variable {i j : FivefoldIndex}
variable (R : fivefoldPhaseCategory frame .north C i ⥤
  fivefoldPhaseCategory frame .north C j)

/-- CONDITIONED bridge to the actual GK5AF Mathlib whole NatIso
category carrier, not a fabricated physical map or higher filler. -/
abbrev FivefoldGK5AHNorthWholeCandidate :=
  NativeGK5AHWholeCandidate
    (fivefoldPhaseEquivalence frame .north e₁)
    (fivefoldPhaseEquivalence frame .north e₂)
    (fivefoldPhaseEquivalence frame .north e₃)
    (fivefoldPhaseEquivalence frame .north e₄) R

/-- Real physical Dart pair, actual P92B class and a CONDITIONALLY
provided path-matched categorical whole NatIso readout. -/
def fivefoldGK5AHNorthPhysicalP92WholeReadout
    (candidate : FivefoldGK5AHNorthWholeCandidate frame e₁ e₂ e₃ e₄ R)
    (fiber : NativeGK5AHNorthHistoryFiber) :
    (Dart × Dart) × (NativeGK5AHNorthP92Classes ×
      FivefoldGK5AGNorthWhole frame e₁ e₂ e₃ e₄ R) :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    (fiber.comparisonClass, candidate.interpret fiber))

/-- Adding real physical endpoints to a selected P92B and matched
whole-NatIso pair still cannot recover original history uniquely. -/
theorem fivefoldGK5AHNorthPhysicalP92Whole_not_injective
    (candidate : FivefoldGK5AHNorthWholeCandidate frame e₁ e₂ e₃ e₄ R) :
    ¬ Function.Injective
      (fivefoldGK5AHNorthPhysicalP92WholeReadout
        frame p e₁ e₂ e₃ e₄ R candidate) := by
  intro hinj
  have hpair :
      ¬ Function.Injective
        (fun x : NativeGK5AHNorthHistoryFiber =>
          (x.comparisonClass, candidate.interpret x)) :=
    nativeGK5AHWholeCandidate_joint_not_injective
      (fivefoldPhaseEquivalence frame .north e₁)
      (fivefoldPhaseEquivalence frame .north e₂)
      (fivefoldPhaseEquivalence frame .north e₃)
      (fivefoldPhaseEquivalence frame .north e₄) R candidate
  apply hpair
  intro x y hxy
  apply hinj
  apply Prod.ext
  · rfl
  · exact hxy

/-- No unconditional physical/NatIso filler is introduced:
recoverability is blocked only for the explicitly matched
interpretation candidate and its specified readout. -/
theorem fivefoldGK5AHNorthNoPhysicalP92WholeRecovery
    (candidate : FivefoldGK5AHNorthWholeCandidate frame e₁ e₂ e₃ e₄ R) :
    ¬ ∃ recover :
        ((Dart × Dart) × (NativeGK5AHNorthP92Classes ×
          FivefoldGK5AGNorthWhole frame e₁ e₂ e₃ e₄ R)) →
            NativeGK5AHNorthHistoryFiber,
      ∀ fiber : NativeGK5AHNorthHistoryFiber,
        recover (fivefoldGK5AHNorthPhysicalP92WholeReadout
          frame p e₁ e₂ e₃ e₄ R candidate fiber) = fiber := by
  rintro ⟨recover, hreturn⟩
  apply fivefoldGK5AHNorthPhysicalP92Whole_not_injective
    frame p e₁ e₂ e₃ e₄ R candidate
  intro x y hxy
  exact (hreturn x).symm.trans
    ((congrArg recover hxy).trans (hreturn y))

#print axioms fivefoldGK5AHNorthPhysicalP92Whole_not_injective
#print axioms fivefoldGK5AHNorthNoPhysicalP92WholeRecovery
end ConditionalWholeNatIso

#print axioms fivefoldGK5AHNorthPhysicalFiber_injective
#print axioms fivefoldGK5AHNorthPhysicalP92_not_injective
#print axioms fivefoldGK5AHNorthNoPhysicalP92FiberRecovery
#print axioms fivefoldGK5AHTypedNorthOrientationEvidence

end
end KUOS.Architecture.WuxingPentagonUnified

import KUOS.Architecture.QiWuxingGK5AIPhysicalThreeCellHistoryV4_2
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AJFourCellComparisonReflection
import Mathlib.Tactic

/-!
Qi v4.3 / F112-P94D3GK5AJ — actual north C60 physical
fifth-around-edge Dart endpoints and precise source/selected
P77/P93 four-cell reflection gate.

The genuine physical C60 fifth-around-edge Dart pair is appended
to the existing independently reconstructed F54-shaped source
4-cell quotient, with actual original F55 nine-constructor
Type-valued witness histories and structural selected P92B
3-cell mapping from GK5AI/GK5AJ.

Prove: attaching the physical fifth-edge boundary does NOT
automatically make the P77→P93 4-cell comparison reflective:
physical injectivity iff the EXACT original typed P77 four-cell
reflection condition, already established by GK5AJ.

The distinct original 3-proof terms of the true C60 pentagon
are still different before four-cell truncation, but the actual
source P77 right-unit four-cell and P93 selected four-cell prove
their 4-cell quotient classes equal. The resulting physical
Dart × P93 4-cell class readout cannot recover the original
3-proof term. It is a certified local higher-history loss,
not a general obstruction to faithful proof-relevant fillers.

The genuine north C60 fifth-edge closure and both reversed
physical directions of categorical 04/43 are kept as separate
typed evidence from the P77/P93 4-cell witnesses. No Edge=NatIso,
old frozen KUOS F54 equivalence, unrestricted gluing, Gray, or
P92B extra naturality attributed to old F55.

Append-only/tighten-only, independent Kuu -> Qi only,
public root107, strict 空 authority boundary preserved.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

private def fivefoldGK5AJNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AJNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The ACTUAL original north-C60 P77 four-cell source-classes,
indexed by full typed original F54 long-3 and short-2 routes. -/
abbrev FivefoldGK5AJNorthRawFourClasses :=
  NativeF55RawVerticalFourClasses
    fivefoldGK5AJNorthFirst fivefoldGK5AJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort

/-- Chosen P93C four-cell classes of the GENUINE mapped selected
P92B Type-valued F55 3-cell comparison proofs. -/
abbrev FivefoldGK5AJNorthP93FourClasses :=
  NativeF55P93AssocFourClasses
    fivefoldGK5AJNorthFirst fivefoldGK5AJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort

/-- Original physical C60 edge endpoints and the ACTUAL
4-cell-class translation between the independently reconstructed
original P77 and chosen P93 presentations. The first component
is a true C60 boundary, not a categorical NatIso. -/
def fivefoldGK5AJNorthPhysicalFourClassMap
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    FivefoldGK5AJNorthRawFourClasses →
      (Dart × Dart) × FivefoldGK5AJNorthP93FourClasses :=
  fun q => (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    nativeGK5AJFourClassMap fivefoldGK5AJNorthFirst
      fivefoldGK5AJNorthLast northNativeF45PentagonLong
      northNativeF45PentagonShort q)

/-- Precise physical descent/reflection necessary AND SUFFICIENT
condition: attaching the REAL north C60 Dart endpoints supplies
no unearned extra source-four-cell reflection.
No reflection hypothesis is asserted to be satisfied. -/
theorem fivefoldGK5AJNorthPhysicalFourClass_injective_iff_reflect
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    Function.Injective (fivefoldGK5AJNorthPhysicalFourClassMap frame p) ↔
      (∀ f g : NativeGK5AINorthPentagonCells,
        Nonempty (NativeF55P93AssocFourCell
          (nativeGK5AIOriginalToP92Structural f)
          (nativeGK5AIOriginalToP92Structural g)) →
        Nonempty (NativeF55RawVerticalFourCell
          fivefoldGK5AJNorthFirst fivefoldGK5AJNorthLast f g)) := by
  have hphysical :
      Function.Injective (fivefoldGK5AJNorthPhysicalFourClassMap frame p) ↔
      Function.Injective
        (nativeGK5AJFourClassMap fivefoldGK5AJNorthFirst
          fivefoldGK5AJNorthLast northNativeF45PentagonLong
          northNativeF45PentagonShort) := by
    constructor
    · intro hinj x y hxy
      apply hinj
      apply Prod.ext
      · rfl
      · exact hxy
    · intro hinj x y hxy
      exact hinj (congrArg Prod.snd hxy)
  exact hphysical.trans
    (nativeGK5AJFourClassInjective_iff_reflect
      fivefoldGK5AJNorthFirst fivefoldGK5AJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)

/-- Real north C60 physical pairing does not change the original
signed pentagon/square/odd-phase shadow readout along the
actual P77-to-P93 four-cell quotient structural map. -/
theorem fivefoldGK5AJNorthPhysicalFourShadow_commutes
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
    (q : FivefoldGK5AJNorthRawFourClasses) :
    nativeF55P93AssocFourToShadow fivefoldGK5AJNorthFirst
      fivefoldGK5AJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (fivefoldGK5AJNorthPhysicalFourClassMap frame p q).2 =
    nativeF55RawVerticalFourToShadow fivefoldGK5AJNorthFirst
      fivefoldGK5AJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q :=
  nativeGK5AJFourClassShadow_commutes fivefoldGK5AJNorthFirst
    fivefoldGK5AJNorthLast northNativeF45PentagonLong
    northNativeF45PentagonShort q

/-- Forgetting the original F55 THREE-proof tree and retaining
only physical C60 Dart endpoints plus P93 four-cell quotient. -/
def fivefoldGK5AJNorthOriginalThreeProofReadout
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex)
    (f : NativeGK5AINorthPentagonCells) :
    (Dart × Dart) × FivefoldGK5AJNorthP93FourClasses :=
  (fivefoldGK5AGNorthPhysicalFifthDarts frame p,
    nativeF55P93AssocFourClass fivefoldGK5AJNorthFirst
      fivefoldGK5AJNorthLast
      (nativeGK5AIOriginalToP92Structural f))

/-- Actual original pentagon and its original F55 right-unit
postcomposition are DIFFERENT Type-valued three-proofs but
the true P93 four-cell equates the two selected four-classes.
No original 3-proof term identity is asserted. -/
theorem fivefoldGK5AJNorthThreeProofReadout_not_injective
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    ¬ Function.Injective
      (fivefoldGK5AJNorthOriginalThreeProofReadout frame p) := by
  intro hinj
  apply nativeGK5AINorthTwoOriginalCells_distinct
  apply hinj
  apply Prod.ext
  · rfl
  · exact (nativeGK5AJNorthOriginalAndSelectedFourClasses_equal).2.symm

/-- The north C60 fifth-edge Dart closure, an original P77
four-cell between the two distinct true F55 pentagon 3-proofs,
its genuinely selected P93C image, and the physically reversed
categorical 04/43 orientations all coexist as DIFFERENT types.
No physical-to-NatIso higher filler is fabricated. -/
theorem fivefoldGK5AJNorthRealFourCellAndOrientation
    (frame : NativeC60FivePhaseGauge) (p : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame p =
      (nativeC60GaugeDart frame .north (p + 4),
       nativeC60GaugeDart frame .north p)) ∧
    Nonempty (NativeF55RawVerticalFourCell
      fivefoldGK5AJNorthFirst fivefoldGK5AJNorthLast
      nativeGK5AINorthPentagonWithIdentity
      nativeGK5AGNorthOriginalCell) ∧
    Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity)
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell)) ∧
    (nativeGK5AGNorthOriginalCell ≠ nativeGK5AINorthPentagonWithIdentity) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  exact ⟨fivefoldPhaseLastPhysicalSide_closed_kernel frame .north p,
    ⟨nativeGK5AJNorthOriginalRightUnitFour⟩,
    ⟨nativeGK5AJNorthMappedRightUnitFour⟩,
    nativeGK5AINorthTwoOriginalCells_distinct,
    (fivefoldGK5AFBothReverseObstructions frame .north).1,
    (fivefoldGK5AFBothReverseObstructions frame .north).2⟩

#print axioms fivefoldGK5AJNorthPhysicalFourClassMap
#print axioms fivefoldGK5AJNorthPhysicalFourClass_injective_iff_reflect
#print axioms fivefoldGK5AJNorthPhysicalFourShadow_commutes
#print axioms fivefoldGK5AJNorthOriginalThreeProofReadout
#print axioms fivefoldGK5AJNorthThreeProofReadout_not_injective
#print axioms fivefoldGK5AJNorthRealFourCellAndOrientation

end
end KUOS.Architecture.WuxingPentagonUnified

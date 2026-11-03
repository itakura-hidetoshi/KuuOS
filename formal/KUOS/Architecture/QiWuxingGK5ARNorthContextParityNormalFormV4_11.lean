import KUOS.Architecture.QiWuxingGK5AQNorthP89P94ReflectionObstructionV4_10
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ARContextUnitParityNormalForm
import Mathlib.Tactic

/-!
Qi v4.11 / F112-P94D3GK5AR — genuinely typed north C60 context
primitive parity rigidity, with original physical P89→P94A
reflection obstruction kept independent.

GK5AR proves a fully proof-relevant two-coordinate ZMod2
endpoint-difference law for ALL 19 actual P94A four-cell constructors,
and consequently parity rigidity of each new context-unit
primitive across all certificates with the same typed endpoints.
Apply to the SAME two original north F45 stages previously used by
Qi v4.8/v4.9, with genuine original F54 dual Nat route histories.
For any north left normalization countLeft is ODD/countRight EVEN;
for any north right normalization countLeft EVEN/countRight ODD;
for any horizontal normalization both context counts are EVEN.
The original independent GK5AO/GK5AP lower bounds >=1 remain.

Also retain Qi v4.10's EXACT conditional original P89→P94A
nonreflection bad-pair criterion on the same physical north sector
without promoting it into an unconditional noninjectivity theorem.
The real fifth-around Dart pair, reversed 04/43 categorical arrows,
and GK5AN unconditional higher structural lift remain separate.

Original P89/P93/P94A, physical C60, whole NatIso and signed odd
shadow all untouched. Independent Kuu -> Qi only, strict 空
authority, append-only, public root107, #1558 Draft/open.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide/added axioms/Gray/global gluing.
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

private def fivefoldGK5ARNorthFirstUnit :=
  nativeF54P92UnitRoute northNativeF45FirstStage

private def fivefoldGK5ARNorthSecondUnit :=
  nativeF54P92UnitRoute northNativeF45SecondStage

private def fivefoldGK5ARNorthLeftRaw :=
  NativeF55P92AssocComparison.leftContext
    (.refl fivefoldGK5ARNorthFirstUnit)
    northNativeF45SecondStage

private def fivefoldGK5ARNorthLeftIdent :=
  NativeF55P92AssocComparison.refl
    (.leftContext fivefoldGK5ARNorthFirstUnit northNativeF45SecondStage)

private def fivefoldGK5ARNorthRightRaw :=
  NativeF55P92AssocComparison.rightContext
    northNativeF45FirstStage
    (.refl fivefoldGK5ARNorthSecondUnit)

private def fivefoldGK5ARNorthRightIdent :=
  NativeF55P92AssocComparison.refl
    (.rightContext northNativeF45FirstStage fivefoldGK5ARNorthSecondUnit)

private def fivefoldGK5ARNorthHorizontalRaw :=
  (NativeF55P92AssocComparison.refl fivefoldGK5ARNorthFirstUnit).horizontal
    (NativeF55P92AssocComparison.refl fivefoldGK5ARNorthSecondUnit)

private def fivefoldGK5ARNorthHorizontalIdent :=
  NativeF55P92AssocComparison.refl
    (nativeF54P90HorizontalRoute
      fivefoldGK5ARNorthFirstUnit fivefoldGK5ARNorthSecondUnit)

/-- Every actual left north context normalization certificate has
positive left count AND precise (odd left, even right) count grade. -/
theorem fivefoldGK5ARNorthLeft_exactGrade
    (w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthLeftRaw fivefoldGK5ARNorthLeftIdent) :
    (1 ≤ w.gk5apLeftUnitCount) ∧
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 1) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  have h := nativeGK5ARLeftContextUnit_exactParity
    fivefoldGK5ARNorthFirstUnit northNativeF45SecondStage w
  exact ⟨nativeGK5APLeftContextUnit_requires_primitive
      fivefoldGK5ARNorthFirstUnit northNativeF45SecondStage w,
    h.1, h.2⟩

/-- Every actual right north context normalization has
positive right count AND precise (even left, odd right) count. -/
theorem fivefoldGK5ARNorthRight_exactGrade
    (w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthRightRaw fivefoldGK5ARNorthRightIdent) :
    (1 ≤ w.gk5apRightUnitCount) ∧
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 1) := by
  have h := nativeGK5ARRightContextUnit_exactParity
    northNativeF45FirstStage fivefoldGK5ARNorthSecondUnit w
  exact ⟨nativeGK5APRightContextUnit_requires_primitive
      northNativeF45FirstStage fivefoldGK5ARNorthSecondUnit w,
    h.1, h.2⟩

/-- Every actual horizontal identity four-cell certificate retains
GK5AO's nonzero horizontalUnit count and has EVEN left/right
context-unit counts. Horizontal count parity is not asserted. -/
theorem fivefoldGK5ARNorthHorizontal_exactGrade
    (w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthHorizontalRaw
      fivefoldGK5ARNorthHorizontalIdent) :
    (1 ≤ w.gk5aoHorizontalUnitCount) ∧
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  have h := nativeGK5ARHorizontalUnit_contextParity_even
    fivefoldGK5ARNorthFirstUnit fivefoldGK5ARNorthSecondUnit w
  exact ⟨nativeGK5AOHorizontalUnit_requires_primitive
      fivefoldGK5ARNorthFirstUnit fivefoldGK5ARNorthSecondUnit w,
    h.1, h.2⟩

/-- The SAME true north C60 physical fifth-around source exhibits
all three selected unit parity grades while the EXACT potential
P89→P94A reflection obstruction remains a separate conditional
iff, independent of the physical frame or Dart index. -/
theorem fivefoldGK5ARNorthPhysicalGradedReflection
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthLeftRaw fivefoldGK5ARNorthLeftIdent,
      (1 ≤ w.gk5apLeftUnitCount) ∧
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 1) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0)) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthRightRaw fivefoldGK5ARNorthRightIdent,
      (1 ≤ w.gk5apRightUnitCount) ∧
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 1)) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5ARNorthHorizontalRaw fivefoldGK5ARNorthHorizontalIdent,
      (1 ≤ w.gk5aoHorizontalUnitCount) ∧
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
       (nativeC60GaugeDart frame .north (i + 4),
        nativeC60GaugeDart frame .north i)) ∧
    Nonempty FivefoldGK5ANP94NorthFullBoundary ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hreflect, hclosed, hrepair, h04, h43⟩
  exact ⟨hreflect,
    fivefoldGK5ARNorthLeft_exactGrade,
    fivefoldGK5ARNorthRight_exactGrade,
    fivefoldGK5ARNorthHorizontal_exactGrade,
    hclosed, hrepair, h04, h43⟩

#print axioms fivefoldGK5ARNorthLeft_exactGrade
#print axioms fivefoldGK5ARNorthRight_exactGrade
#print axioms fivefoldGK5ARNorthHorizontal_exactGrade
#print axioms fivefoldGK5ARNorthPhysicalGradedReflection

end
end KUOS.Architecture.WuxingPentagonUnified

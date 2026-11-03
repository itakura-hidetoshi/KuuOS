import KUOS.Architecture.QiWuxingGK5BDNorthP77LocalSeamDescentV4_23
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BESignedOriginalGradeObstruction
import Mathlib.Tactic

/-!
Qi v4.24 / F112-P94D3GK5BE — true north C60 inverse primitive
with unsigned original-wrapper count ONE but signed-original
grade +1 versus -1, and the exact P77-negative orbit.

GK5BE independently proved signed ORIGINAL-wrapper grade is
preserved by all sixteen P93C and all nineteen P94A four-cell
constructors. This Qi presentation imports that proof rather
than treating a physical phase or a numerical shadow as a new
four-cell witness.

The actual north C60 pentagon p has a positive reflexive seam
and P77-unit-extended positive class. The original inverse
F55.symm p has equal unsigned wrapper count ONE at raw and phi
endpoints but its phi signed grade is MINUS one, so the chosen
P94A original→phi direct seam does not exist. A genuine P77
one-step right-identity word extends this negative class to a
nontrivial composite without changing its dependent F54 indices.

Positive and negative P77 source classes are kept at their
different genuinely reversed F54 route endpoint pairs; we do
not equate them. Original P89 BadPair and physical fivefold
Dart orientation are independent of this selected P94A
signed-grade obstruction.

No global original-to-phi bridge, GK5BA constructor kit,
unconditional P89 injectivity/noninjectivity, all-P94A
normalization, identity seam or Gray reconstruction.

Strict 空 authority, independent Kuu→Qi, original F54
two-Nat/two-category/Blocks and Type-valued proof histories,
public root107, protected PR #1558 Draft/open.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; no sorry, admit, native_decide, new axioms.
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

private def fivefoldGK5BENorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BENorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Actual inverse source F55 three-proof at reversed north
long/short original F54 route endpoints. -/
def fivefoldGK5BENorthInverseSource :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonShort northNativeF45PentagonLong :=
  .symm nativeGK5AGNorthOriginalCell

/-- True F55 source inverse followed by a true original RIGHT
identity in the NORTH long route, not the selected P92B refl. -/
def fivefoldGK5BENorthInverseRightUnitSource :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonShort northNativeF45PentagonLong :=
  .trans fivefoldGK5BENorthInverseSource
    (.ident northNativeF45PentagonLong)

/-- The two TRUE north inverse source proof terms are related
by a genuine one-step P77 four-cell, reversed rightUnit, not by
raw syntax equality or a stronger unavailable trans shell. -/
def fivefoldGK5BENorthInverseRightUnitWord :
    NativeGK5BDP77Word fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      fivefoldGK5BENorthInverseSource
      fivefoldGK5BENorthInverseRightUnitSource :=
  .snoc .nil (.symm (.rightUnit fivefoldGK5BENorthInverseSource))

/-- A full genuinely typed P77 class equality connects the
inverse primitive to its original right-identity extension. -/
theorem fivefoldGK5BENorthInverseRightUnit_same_P77_class :
    nativeF55RawVerticalFourClass
      fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      fivefoldGK5BENorthInverseSource =
    nativeF55RawVerticalFourClass
      fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      fivefoldGK5BENorthInverseRightUnitSource :=
  (nativeGK5BDWord_iff_same_P77_class
    fivefoldGK5BENorthInverseSource
    fivefoldGK5BENorthInverseRightUnitSource).mp
      ⟨fivefoldGK5BENorthInverseRightUnitWord⟩

/-- Both endpoints have exactly the SAME GK5BB UNSIGNED
wrapper count ONE for the original inverse primitive.
The new signed grade is different, so no direct P94A seam. -/
theorem fivefoldGK5BENorthInverse_equal_unsigned_no_seam :
    (NativeF55P92AssocComparison.original
      fivefoldGK5BENorthInverseSource).gk5bbOriginalCount =
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BENorthInverseSource).gk5bbOriginalCount ∧
    ¬ Nonempty (nativeGK5AZSeamAt fivefoldGK5BENorthInverseSource) :=
  nativeGK5BENorthInverse_count_one_but_no_seam

/-- The original F55 inverse plus right identity STILL has
equal unsigned wrapper counts, but its source P77 class is
seam-NEGATIVE by the independent signed grade obstruction. -/
theorem fivefoldGK5BENorthInverseRightUnit_count_equal_no_seam :
    (NativeF55P92AssocComparison.original
      fivefoldGK5BENorthInverseRightUnitSource).gk5bbOriginalCount =
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BENorthInverseRightUnitSource).gk5bbOriginalCount ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BENorthInverseRightUnitSource) := by
  constructor
  · rfl
  · exact nativeGK5BENorthInverseP77Word_no_seam
      fivefoldGK5BENorthInverseRightUnitWord

/-- The signed selected phi grade is precisely MINUS one on
this actual reversed NORTH source, even after original right
unit insertion. This is not a signed physical C60 charge. -/
theorem fivefoldGK5BENorthInverseRightUnit_phi_signed :
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BENorthInverseRightUnitSource).gk5beSignedCount = -1 := rfl

/-- The negative local-seam property descends to the TRUE P77
quotient class in the reversed F54 slot, via GK5BD Quotient.lift. -/
theorem fivefoldGK5BENorthInverseRightUnit_class_negative :
    ¬ nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      northNativeF45PentagonShort northNativeF45PentagonLong
      (nativeF55RawVerticalFourClass
        fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
        fivefoldGK5BENorthInverseRightUnitSource) :=
  fivefoldGK5BENorthInverseRightUnit_count_equal_no_seam.2

/-- Positive pentagon source and its doubly right-unit
extension coexist with a negative reverse-pentagon source
and its inverse right-unit P77 class; they occupy their
genuinely DIFFERENT typed F54 route slots. -/
theorem fivefoldGK5BENorthPositiveAndNegative_orbits :
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
        fivefoldGK5BDNorthDoubleRightUnit) ∧
    ¬ nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
      northNativeF45PentagonShort northNativeF45PentagonLong
      (nativeF55RawVerticalFourClass
        fivefoldGK5BENorthFirst fivefoldGK5BENorthLast
        fivefoldGK5BENorthInverseRightUnitSource) :=
  ⟨fivefoldGK5BDNorthDoubleRightUnit_class_positive,
   fivefoldGK5BENorthInverseRightUnit_class_negative⟩

/-- Even with real physical NORTH fivefold gauge and P94A's
new signed-grade obstruction, the original P89 reflection
problem remains the preexisting conditional BadPair criterion. -/
theorem fivefoldGK5BENorthPhysicalSignedAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BENorthInverseRightUnitSource) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, _, _⟩
  exact ⟨fivefoldGK5BENorthInverseRightUnit_count_equal_no_seam.2,
    hClosed, hIff⟩

#print axioms fivefoldGK5BENorthInverseSource
#print axioms fivefoldGK5BENorthInverseRightUnitSource
#print axioms fivefoldGK5BENorthInverseRightUnitWord
#print axioms fivefoldGK5BENorthInverseRightUnit_same_P77_class
#print axioms fivefoldGK5BENorthInverse_equal_unsigned_no_seam
#print axioms fivefoldGK5BENorthInverseRightUnit_count_equal_no_seam
#print axioms fivefoldGK5BENorthInverseRightUnit_phi_signed
#print axioms fivefoldGK5BENorthInverseRightUnit_class_negative
#print axioms fivefoldGK5BENorthPositiveAndNegative_orbits
#print axioms fivefoldGK5BENorthPhysicalSignedAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

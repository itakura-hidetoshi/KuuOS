import KUOS.Architecture.QiWuxingGK5BENorthSignedSeamObstructionV4_24
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFDoubleInversionWeightObstruction
import Mathlib.Tactic

/-!
Qi v4.25 / F112-P94D3GK5BF — the SAME genuine north C60
F54 long→short Hom contains both a positive original pentagon
P77 four-cell class and a strictly negative DOUBLE-INVERSE
original F55 proof class. BOTH satisfy GK5BB N(phi)=1 AND
GK5BE S(phi)=+1. The GK5BF inversion-depth weight W differs.

Construct an actual ORIGINAL F55 right-identity extension
of the double inverse and a genuine finite one-step P77
four-cell certificate. The extension is still negative and
still passes BOTH old numerical necessary tests, whereas
the new P94A-sound weight W(phi)=4 is an actual obstruction.
The positive and negative P77 classes are PROVABLY UNEQUAL
even though they share the same dependent F54 endpoints.

This is NOT a proof of the sufficiency of N=S=W=1, nor an
identification of physical gauge orientation with the
P92B Type-valued inverse-depth counter. Conditional original
P89 BadPair and genuine north fifth Dart closure remain
independent and retain their original directions.

Strict 空 authority; independent Kuu→Qi. Original F54
two-Nat/two-category/Blocks/F55 Type histories maintained,
public root107, protected PR #1558 Draft/OPEN/unmerged.
Lean v4.30.0-rc2 and pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, no Gray, sorry, admit, native_decide,
new axioms or unconditional global GK5AY seam.
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

private def fivefoldGK5BFNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BFNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The actual original source double inversion p↦p⁻¹↦p
returns to the SAME original F54 long→short endpoint pair. -/
def fivefoldGK5BFNorthDoubleInverseSource :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  nativeGK5BFNorthDoubleInverse

/-- An actual ORIGINAL F55 right unit is inserted after the
original double inverse. The selected P92B refl is NOT a
separate original source identity witness here. -/
def fivefoldGK5BFNorthDoubleInverseRightUnit :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  .trans fivefoldGK5BFNorthDoubleInverseSource
    (.ident northNativeF45PentagonShort)

/-- A real source P77 right-unit four-cell, reversed to form
one finite certificate step FROM the double inverse source
to its original F55 right-unit extension. -/
def fivefoldGK5BFNorthDoubleInverseRightUnitWord :
    NativeGK5BDP77Word
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      fivefoldGK5BFNorthDoubleInverseSource
      fivefoldGK5BFNorthDoubleInverseRightUnit :=
  .snoc .nil (.symm (.rightUnit fivefoldGK5BFNorthDoubleInverseSource))

/-- Actual original source P77 quotient class equality, not
the (false) assertion of raw F55 three-proof syntax equality. -/
theorem fivefoldGK5BFNorthDoubleInverseUnit_same_P77_class :
    nativeF55RawVerticalFourClass
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      fivefoldGK5BFNorthDoubleInverseSource =
    nativeF55RawVerticalFourClass
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      fivefoldGK5BFNorthDoubleInverseRightUnit :=
  (nativeGK5BDWord_iff_same_P77_class
    fivefoldGK5BFNorthDoubleInverseSource
    fivefoldGK5BFNorthDoubleInverseRightUnit).mp
    ⟨fivefoldGK5BFNorthDoubleInverseRightUnitWord⟩

/-- Even after one REAL ORIGINAL F55 right-unit insertion,
the selected structural phi still satisfies the two old
necessary constraints but FAILS the stronger new weight gate. -/
theorem fivefoldGK5BFNorthDoubleInverseUnit_three_values :
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5beSignedCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bfInverseDepthWeight = 4 :=
  ⟨rfl, rfl, rfl⟩

/-- Proof-relevant P77 transport refutes every direct chosen
P94A seam for the original double-inverse right-unit extension.
It never constructs the impossible raw trans decomposition shell. -/
theorem fivefoldGK5BFNorthDoubleInverseUnit_no_seam :
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) :=
  nativeGK5BFNorthDoubleInverseP77Word_no_seam
    fivefoldGK5BFNorthDoubleInverseRightUnitWord

/-- Both original source classes inhabit the exact same true
north F54 Hom, but the positive primitive is provably NOT
P77-equivalent to the double-inverse right-unit source. -/
theorem fivefoldGK5BFNorthPrimitive_ne_double_inverse_unit_class :
    nativeF55RawVerticalFourClass
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      nativeGK5AGNorthOriginalCell ≠
    nativeF55RawVerticalFourClass
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      fivefoldGK5BFNorthDoubleInverseRightUnit := by
  intro heq
  apply nativeGK5BFNorthPrimitive_ne_double_inverse_P77_class
  exact heq.trans fivefoldGK5BFNorthDoubleInverseUnit_same_P77_class.symm

/-- The WEAK joint N=S=1 quotient gate is true at both genuine
north C60 classes. Actual seam existence is true at the original
pentagon class and false at the right-unit double-inverse class. -/
theorem fivefoldGK5BFNorthSameFiber_weak_gate_seam_split :
    nativeGK5BFCountSignedOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    nativeGK5BFCountSignedOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) ∧
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    ¬ nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) :=
  ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩,
    ⟨.refl _⟩, fivefoldGK5BFNorthDoubleInverseUnit_no_seam⟩

/-- On the same original F54 Hom, GK5BF's strictly refined
three-condition predicate is true at the source primitive
but false at the original right-unit double-inverse class. -/
theorem fivefoldGK5BFNorthThreeGate_separates_classes :
    nativeGK5BFThreeGatesOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    ¬ nativeGK5BFThreeGatesOnP77Class
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  constructor
  · exact ⟨⟨rfl, rfl⟩, rfl⟩
  · intro h
    have hw := h.2
    change (4 : Nat) = 1 at hw
    omega

/-- Local positive and negative P77-class phenomena do NOT
repair a global GK5AY seam, which remains impossible at the
same inhabited north source/target F54 slot by GK5BB. -/
theorem fivefoldGK5BFNorthLocal_split_but_global_no :
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) ∧
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BFNorthFirst fivefoldGK5BFNorthLast) :=
  ⟨⟨.refl _⟩,
   fivefoldGK5BFNorthDoubleInverseUnit_no_seam,
   nativeGK5BBNorthNoGlobalSeam⟩

/-- The TRUE physical north C60 fifth-around gauge and the
old original P89 class-reflection obstruction coexist with
the new strictly stronger P94A inverse-depth proof obstruction;
no numerical gauge-to-four-cell reflection is asserted. -/
theorem fivefoldGK5BFNorthPhysicalAndDoubleInverseObstruction
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, _, _⟩
  exact ⟨fivefoldGK5BFNorthDoubleInverseUnit_no_seam,
    hClosed, hIff⟩

#print axioms fivefoldGK5BFNorthDoubleInverseSource
#print axioms fivefoldGK5BFNorthDoubleInverseRightUnit
#print axioms fivefoldGK5BFNorthDoubleInverseRightUnitWord
#print axioms fivefoldGK5BFNorthDoubleInverseUnit_same_P77_class
#print axioms fivefoldGK5BFNorthDoubleInverseUnit_three_values
#print axioms fivefoldGK5BFNorthDoubleInverseUnit_no_seam
#print axioms fivefoldGK5BFNorthPrimitive_ne_double_inverse_unit_class
#print axioms fivefoldGK5BFNorthSameFiber_weak_gate_seam_split
#print axioms fivefoldGK5BFNorthThreeGate_separates_classes
#print axioms fivefoldGK5BFNorthLocal_split_but_global_no
#print axioms fivefoldGK5BFNorthPhysicalAndDoubleInverseObstruction

end
end KUOS.Architecture.WuxingPentagonUnified

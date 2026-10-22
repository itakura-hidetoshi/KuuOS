import Kuu.F112.PolygonNativeF55PentagonChargeTransportDescentP73
import Mathlib.Tactic.Omega

/-!
# F112-P74 — necessary and sufficient descent of signed linear charges

P73 proved that P68 squareOnly comparison witnesses have zero
pentagon charge, and that the ORIGINAL integer pentagon coordinate
does descend to P71's genuine higher-arrow transport quotient.
The original signed exchange-square charge need not descend.

This file classifies ALL integer-linear combinations of the two
original signed F55 generator charges on a fixed transport quotient
that admits a genuine unit exchange-square witness (square charge +1).
For coefficients a,b in Int, the source readout
    a * pentagonCharge + b * squareCharge
descends on that transport quotient IF AND ONLY IF b = 0.

The necessity proof uses only the actual P71 transport relation,
P73 pentagon invariance and an exhibited unit square-charge shift.
The sufficiency proof constructs the function using the genuine P73
quotient pentagon-charge readout.

The ORIGINAL top C60 north hexagon disjoint square is such a witness:
identity raw charge (0,0) becomes (0,1) under an explicit, typed
representative change, even though source and target quotient route
classes have not changed.

The result is a classification for this chosen integer-linear
observer family and specifically the P71 transport quotient. It
does not claim that every possible witness-graded higher-categorical
observable or a strict 3/n category must have this form.

No Gray, sorry, admit, added axioms or discarded legacy theorem roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A chosen integer-linear evaluation on the TWO original
SIGNED F55 generator charges. The independent odd parity remains
a separate coordinate and is not silently reconstructed. -/
def NativeF55HigherArrowOverClasses.signedLinearCharge
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    (pentCoeff squareCoeff : Int) : Int :=
  pentCoeff * arrow.raw.nativeShadow.1.1 +
    squareCoeff * arrow.raw.nativeShadow.1.2

/-- When the exchange-square coefficient vanishes, any multiple
of the pentagon charge has a genuine well-defined readout on
EVERY fixed source/target P71 higher transport quotient. -/
def nativeF55HigherTransportLinearPentagonCharge
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last)
    (pentCoeff : Int) :
    NativeF55HigherTransportClasses first last source target → Int :=
  fun z => pentCoeff *
    nativeF55HigherTransportPentagonCharge first last source target z

/-- Exact factorization of any integer multiple of pentagon charge.
Neither a square coefficient nor the C60 phase enters this function. -/
theorem nativeF55HigherTransportLinearPentagonCharge_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last)
    (pentCoeff : Int)
    (arrow : NativeF55HigherArrowOverClasses first last source target) :
    nativeF55HigherTransportLinearPentagonCharge
      first last source target pentCoeff
      (nativeF55HigherTransportClass first last source target arrow) =
      arrow.signedLinearCharge pentCoeff 0 := by
  change pentCoeff *
    nativeF55HigherTransportPentagonCharge first last source target
      (nativeF55HigherTransportClass first last source target arrow) =
        pentCoeff * arrow.raw.nativeShadow.1.1 +
          (0 : Int) * arrow.raw.nativeShadow.1.2
  rw [nativeF55HigherTransportPentagonCharge_spec]
  simp

/-- Exact iff-classification of integer-linear F55 signed charge
readouts whenever there is a genuine P71-related representative
change that increases the original signed square charge by ONE.

The sufficiency direction is constructive via P73's quotient
readout; the necessity direction applies the SAME chosen readout
to the two actual related F55 higher arrows. Nothing about raw
term equality or a full quotient 3-category is assumed. -/
theorem nativeF55HigherTransport_linearDescends_iff_squareCoeff_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last)
    (f g : NativeF55HigherArrowOverClasses first last source target)
    (h : NativeF55HigherTransportRel first last source target f g)
    (hSquare : g.raw.nativeShadow.1.2 =
      f.raw.nativeShadow.1.2 + (1 : Int))
    (pentCoeff squareCoeff : Int) :
    (∃ readout : NativeF55HigherTransportClasses first last source target → Int,
      ∀ arrow : NativeF55HigherArrowOverClasses first last source target,
        readout (nativeF55HigherTransportClass first last source target arrow) =
          arrow.signedLinearCharge pentCoeff squareCoeff) ↔
      squareCoeff = 0 := by
  constructor
  · rintro ⟨readout, hreadout⟩
    have hclass :
        nativeF55HigherTransportClass first last source target f =
          nativeF55HigherTransportClass first last source target g :=
      (nativeF55HigherTransportClass_eq_iff first last source target f g).2 h
    have hlin :
        f.signedLinearCharge pentCoeff squareCoeff =
          g.signedLinearCharge pentCoeff squareCoeff := by
      calc
        f.signedLinearCharge pentCoeff squareCoeff =
            readout (nativeF55HigherTransportClass first last source target f) :=
          (hreadout f).symm
        _ = readout (nativeF55HigherTransportClass first last source target g) :=
          congrArg readout hclass
        _ = g.signedLinearCharge pentCoeff squareCoeff := hreadout g
    have hp :
        f.raw.nativeShadow.1.1 = g.raw.nativeShadow.1.1 :=
      NativeF55HigherTransportRel.pentagon_eq h
    change pentCoeff * f.raw.nativeShadow.1.1 +
        squareCoeff * f.raw.nativeShadow.1.2 =
      pentCoeff * g.raw.nativeShadow.1.1 +
        squareCoeff * g.raw.nativeShadow.1.2 at hlin
    rw [← hp, hSquare, mul_add, mul_one] at hlin
    omega
  · intro hz
    refine ⟨nativeF55HigherTransportLinearPentagonCharge
      first last source target pentCoeff, ?_⟩
    intro arrow
    rw [hz]
    exact nativeF55HigherTransportLinearPentagonCharge_spec
      first last source target pentCoeff arrow

/-- Original physical north C60 identity has zero signed exchange
charge, independently of any numerical comparison-based quotient. -/
theorem northHexagonNativeIdentityHigherArrow_squareCharge_zero :
    northHexagonNativeIdentityHigherArrowOverClasses.raw.nativeShadow.1.2 =
      (0 : Int) := rfl

/-- The ACTUAL original top C60 six-sector comparison square shifts
the selected signed exchange-square coordinate to ONE. This is the
original Type-valued raw disjoint-square witness from P54/F55. -/
theorem northHexagonNativeIdentityTransportedHigherArrow_squareCharge_one :
    northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow.1.2 =
      (1 : Int) := by
  change
    ((0 : KuuNativeF55Shadow) +
      ((0 : KuuNativeF55Shadow) +
        northHexagonNativeF55SquareCell.nativeShadow)).1.2 = (1 : Int)
  rw [northHexagonNativeF55SquareCell_shadow]
  rfl

/-- This genuine C60 pair satisfies the EXACT one-square-shift
hypothesis of the general P74 classification theorem. -/
theorem northHexagonNativeIdentityTransport_squareCharge_increment :
    northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow.1.2 =
      northHexagonNativeIdentityHigherArrowOverClasses.raw.nativeShadow.1.2 +
        (1 : Int) := by
  rw [northHexagonNativeIdentityTransportedHigherArrow_squareCharge_one]
  rfl

#print axioms NativeF55HigherArrowOverClasses.signedLinearCharge
#print axioms nativeF55HigherTransportLinearPentagonCharge
#print axioms nativeF55HigherTransportLinearPentagonCharge_spec
#print axioms nativeF55HigherTransport_linearDescends_iff_squareCoeff_zero
#print axioms northHexagonNativeIdentityHigherArrow_squareCharge_zero
#print axioms northHexagonNativeIdentityTransportedHigherArrow_squareCharge_one
#print axioms northHexagonNativeIdentityTransport_squareCharge_increment

end
end Kuu.F112.Physical

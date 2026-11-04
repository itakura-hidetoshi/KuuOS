import KUOS.Architecture.QiWuxingGK5BMNorthIntegralNatLiftV4_32
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BNFiniteDivisibilityCertificates
import Mathlib.Tactic

/-!
Qi v4.33 — TRUE NORTH C60 finite integer denominator
and cleared-numerator divisibility certificates.

The independent GK5BN's exact FINITE support tests are
transported to original north F54/F55 typed evidence, original
P77 quotient's DESCENDED polynomial value, true primitive and
double-inverse, and actual chosen P92B loops.

An arbitrary finite integer-valued observation table is NOT
claimed to imply integral monomial coefficients: such a claim
would be false. The cleared-numerator test explicitly requires
a proven exact identity d * Q = map(N), where d ≠ 0.
No source Type-valued proof is inferred from coefficients, and
no unconditional P94A four-cell, P89 reflection or global seam.

Strict 空 authority, independent Kuu → Qi; real F54 two Nat /
two categories / Blocks and F55 Type proof history retained.
Preserve root107; #1558 stays draft/open/unmerged.
Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or GK5BA kit.
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

private def fivefoldGK5BNNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BNNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- EXACT finite rational denominator gate for any north
interpolation data, without assumptions that source samples
are integer-valued or represent original F55 evidence. -/
theorem fivefoldGK5BNNorthRationalData_integral_iff_finiteDenominators
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k ∈ (nativeGK5BLRationalInterpolant sites values).support,
      ((nativeGK5BLRationalInterpolant sites values).coeff k).den = 1) :=
  nativeGK5BNInterpolant_integral_iff_finiteDenominators sites values

/-- A finite explicit noninteger denominator on a north
rational observation polynomial rules out any Int[X] lift. -/
theorem fivefoldGK5BNNorthRationalData_nontrivialDenominator_obstructs
    (sites : Finset Int) (values : Int → Rat)
    (k : Nat)
    (hk : k ∈ (nativeGK5BLRationalInterpolant sites values).support)
    (hden : ((nativeGK5BLRationalInterpolant sites values).coeff k).den ≠ 1) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites values :=
  nativeGK5BNNoIntegralLift_of_denominator _ k hk hden

/-- Exact north interpolation integrality iff the NONZERO
coefficients of a witnessed integral numerator are divisible by
its nonzero integer clearing scalar. Both numerator and
clearing equality are supplied as evidence. -/
theorem fivefoldGK5BNNorthRationalData_scaled_iff_finiteDivisibility
    (sites : Finset Int) (values : Int → Rat)
    (N : Polynomial Int) (d : Int) (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) *
       nativeGK5BLRationalInterpolant sites values =
       N.map (Int.castRingHom Rat)) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
       nativeGK5BLRationalInterpolant sites values) ↔
      (∀ k ∈ N.support, d ∣ N.coeff k) :=
  nativeGK5BNInterpolant_scaled_iff_finiteDivisibility
    sites values N d hd hscale

/-- A failed integer numerator divisibility test obstructs
integral north rational interpolation, CONDITIONED on a
certified clearing identity. -/
theorem fivefoldGK5BNNorthRationalData_scaled_notDvd_obstructs
    (sites : Finset Int) (values : Int → Rat)
    (N : Polynomial Int) (d : Int) (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) *
       nativeGK5BLRationalInterpolant sites values =
       N.map (Int.castRingHom Rat))
    (k : Nat) (hnot : ¬ d ∣ N.coeff k) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
       nativeGK5BLRationalInterpolant sites values :=
  nativeGK5BNScaled_noIntegralLift_of_notDvd N _ d hd hscale k hnot

/-- EVERY actually typed original north F55 three-proof
yields a finite reduced denominator-one certificate of its
reconstructed polynomial VALUE; not a new Type witness. -/
theorem fivefoldGK5BNNorthOriginalSource_finiteDenominators
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int =>
        (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant sites
        (fun z : Int =>
          (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNFiniteDenominators_of_natLift _
    (fivefoldGK5BMNorthSource_natLift f d sites hsize hdegree)

/-- TRUE original north F55/P77 source quotient class:
finite denominator-one certificate for the DESCENDED Int[X]
polynomial VALUE only, never an identification of source
Type-valued P77 equivalence classes. -/
theorem fivefoldGK5BNNorthOriginalP77_finiteDenominators
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BNNorthFirst fivefoldGK5BNNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BNNorthFirst fivefoldGK5BNNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class
        fivefoldGK5BNNorthFirst fivefoldGK5BNNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant sites
        (fun z : Int => (((nativeGK5BGPolyOnP77Class
          fivefoldGK5BNNorthFirst fivefoldGK5BNNorthLast
          northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNP77FiniteDenominators
    fivefoldGK5BNNorthFirst fivefoldGK5BNNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q d sites hsize hdegree

/-- The actual original north primitive's rational interpolant
on the canonical three integer sites has finite denominator one. -/
theorem fivefoldGK5BNNorthPrimitive_threeSite_finiteDenominators :
    ∀ k ∈ (nativeGK5BLRationalInterpolant
      (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant
        (nativeGK5BKIntegerGrid 2)
        (fun z : Int => (((nativeGK5AIOriginalToP92Structural
          nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNFiniteDenominators_of_natLift _
    fivefoldGK5BMNorthPrimitive_threeSite_natLift

/-- The genuine north double inverse with F55 right identity
likewise has finite denominator one, without asserting a
local original-to-phi seam. -/
theorem fivefoldGK5BNNorthDoubleInverse_threeSite_finiteDenominators :
    ∀ k ∈ (nativeGK5BLRationalInterpolant
      (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant
        (nativeGK5BKIntegerGrid 2)
        (fun z : Int => (((nativeGK5AIOriginalToP92Structural
          fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNFiniteDenominators_of_natLift _
    fivefoldGK5BMNorthDoubleInverse_threeSite_natLift

/-- Both genuine north P92B endomorphism-loop rational
interpolants on four integer sites have finite denominator one;
they remain distinct genuine P92B source histories. -/
theorem fivefoldGK5BNNorthTripleLoops_fourSite_finiteDenominators :
    (∀ k ∈ (nativeGK5BLRationalInterpolant
      ({(-1 : Int), 0, 1, 2} : Finset Int)
      (fun z : Int =>
        ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant
        ({(-1 : Int), 0, 1, 2} : Finset Int)
        (fun z : Int =>
          ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1) ∧
    (∀ k ∈ (nativeGK5BLRationalInterpolant
      ({(-1 : Int), 0, 1, 2} : Finset Int)
      (fun z : Int =>
        ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant
        ({(-1 : Int), 0, 1, 2} : Finset Int)
        (fun z : Int =>
          ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1) := by
  constructor
  · exact nativeGK5BNFiniteDenominators_of_natLift _
      fivefoldGK5BMNorthTripleLoops_fourSite_natLifts.1
  · exact nativeGK5BNFiniteDenominators_of_natLift _
      fivefoldGK5BMNorthTripleLoops_fourSite_natLifts.2

/-- Original C60 physical fifth-around closure and
conditional P89 reflection remain orthogonal to finite
coefficient certificates and local seam existence. -/
theorem fivefoldGK5BNNorthPhysicalAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    (¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) :=
  fivefoldGK5BMNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BNNorthRationalData_integral_iff_finiteDenominators
#print axioms fivefoldGK5BNNorthRationalData_nontrivialDenominator_obstructs
#print axioms fivefoldGK5BNNorthRationalData_scaled_iff_finiteDivisibility
#print axioms fivefoldGK5BNNorthRationalData_scaled_notDvd_obstructs
#print axioms fivefoldGK5BNNorthOriginalSource_finiteDenominators
#print axioms fivefoldGK5BNNorthOriginalP77_finiteDenominators
#print axioms fivefoldGK5BNNorthPrimitive_threeSite_finiteDenominators
#print axioms fivefoldGK5BNNorthDoubleInverse_threeSite_finiteDenominators
#print axioms fivefoldGK5BNNorthTripleLoops_fourSite_finiteDenominators
#print axioms fivefoldGK5BNNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

import KUOS.Architecture.QiWuxingGK5BNNorthFiniteDivisibilityV4_33
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BOForwardDifferenceFactorial
import Mathlib.Tactic

/-!
Qi v4.34 / F112-P94D3GK5BO — TRUE NORTH C60
Gregory–Newton / FINITE FACTORIAL DIFFERENCE CERTIFICATES.

The genuine north F54/F55 Type-valued source witnesses and
actual original P77 source quotient are retained. Only their
already-descended polynomial VALUES receive independent
factorial forward-difference certificates, transported from
the true GK5BJ nonnegative depth coefficients via GK5BM.

An arbitrary rational sample table satisfies the finite
criterion exactly when its actual Lagrange interpolant admits
an Int[X] source. Integer-valued data alone does not assert
monomial integrality. The finite cutoff Q_{≤k} is essential.

True physical fifth Dart north closure, conditional original
P89 source-reflection, and original-to-phi local seams remain
independent of coefficient certificates. No Type-valued
inverse, new P94A four-cell, universal GK5AY seam, or Gray.

Strict 空 authority; independent Kuu→Qi; original F54
two Nat/two categories/Blocks and F55 Type proof history.
Append-only root107, protected #1558 Draft/open/unmerged,
pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, GK5BA kit, or
unconditional P89 reflection / W=1→seam sufficiency.
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

private def fivefoldGK5BONorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BONorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Every rational north observation polynomial has an
Int[X] coefficient source precisely when its finitely many
truncated factorial forward differences pass integer tests.
No unproved source Type-valued lift is asserted. -/
theorem fivefoldGK5BONorthRationalData_integral_iff_factorial
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Int,
       P.map (Int.castRingHom Rat) =
         nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k ∈ (nativeGK5BLRationalInterpolant sites values).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant sites values) k) k) :=
  nativeGK5BOInterpolant_integral_iff_factorialDifferences sites values

/-- The Gregory–Newton integer-grid formula for the actual
rational Lagrange interpolant, with NO assumption about
coefficient integrality or Type-valued original witnesses. -/
theorem fivefoldGK5BONorthRationalData_newtonGrid
    (sites : Finset Int) (values : Int → Rat) (n : Nat) :
    (nativeGK5BLRationalInterpolant sites values).eval (n : Rat) =
      ∑ k ∈ Finset.range (n + 1),
        (n.choose k : Rat) *
          nativeGK5BOForwardAtZero
            (nativeGK5BLRationalInterpolant sites values) k :=
  nativeGK5BONewtonGrid _ n

/-- One failing factorial witness is an obstruction for
any claimed integer-coefficient north interpolation. -/
theorem fivefoldGK5BONorthRationalData_factorialObstruction
    (sites : Finset Int) (values : Int → Rat) (k : Nat)
    (hk : k ∈ (nativeGK5BLRationalInterpolant sites values).support)
    (hnot : ¬ ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
      nativeGK5BOForwardAtZero
        (nativeGK5BOCutoff
          (nativeGK5BLRationalInterpolant sites values) k) k) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites values :=
  nativeGK5BONoIntegralLift_of_factorialObstruction _ k hk hnot

/-- Every genuine original true north F55 three-proof f gives
a finitely checked factorial difference certificate for the
reconstructed polynomial of its genuine P92B structural image. -/
theorem fivefoldGK5BONorthOriginalSource_factorialDifferences
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int =>
        (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant sites
              (fun z : Int =>
                (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    (fivefoldGK5BMNorthSource_natLift f d sites hsize hdegree)

/-- True north original F55/P77 source class q gives
factorial-difference certificates for its DESCENDED polynomial
VALUE; original source quotient classes are not identified. -/
theorem fivefoldGK5BONorthP77_factorialDifferences
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BONorthFirst fivefoldGK5BONorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BONorthFirst fivefoldGK5BONorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class
        fivefoldGK5BONorthFirst fivefoldGK5BONorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant sites
              (fun i : Int => (((nativeGK5BGPolyOnP77Class
                fivefoldGK5BONorthFirst fivefoldGK5BONorthLast
                northNativeF45PentagonLong northNativeF45PentagonShort q).eval i : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    (fivefoldGK5BMNorthP77_natLift q d sites hsize hdegree)

/-- The actual primitive original north pentagon has a true
factorial difference polynomial certificate on {0,1,2}. -/
theorem fivefoldGK5BONorthPrimitive_threeSite_factorial :
    ∀ k ∈ (nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
              (fun z : Int => (((nativeGK5AIOriginalToP92Structural
                nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    fivefoldGK5BMNorthPrimitive_threeSite_natLift

/-- The genuine north double inverse together with its
original F55 right unit has the separate three-site certificate. -/
theorem fivefoldGK5BONorthDoubleInverse_threeSite_factorial :
    ∀ k ∈ (nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
              (fun z : Int => (((nativeGK5AIOriginalToP92Structural
                fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    fivefoldGK5BMNorthDoubleInverse_threeSite_natLift

/-- Each of the two ACTUAL chosen P92B north endomorphism loops
has its own factorial difference certificate on four sites;
coincidences of old three-point observations are not promoted
to identifications of these original distinct proof histories. -/
theorem fivefoldGK5BONorthTripleLoops_fourSite_factorial :
    (∀ k ∈ (nativeGK5BLRationalInterpolant
      ({(-1 : Int), 0, 1, 2} : Finset Int)
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant
              ({(-1 : Int), 0, 1, 2} : Finset Int)
              (fun i : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval i : Int) : Rat))) k) k) ∧
    (∀ k ∈ (nativeGK5BLRationalInterpolant
      ({(-1 : Int), 0, 1, 2} : Finset Int)
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant
              ({(-1 : Int), 0, 1, 2} : Finset Int)
              (fun i : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval i : Int) : Rat))) k) k) := by
  constructor
  · exact nativeGK5BOFactorialDifferences_of_natLift _
      fivefoldGK5BMNorthTripleLoops_fourSite_natLifts.1
  · exact nativeGK5BOFactorialDifferences_of_natLift _
      fivefoldGK5BMNorthTripleLoops_fourSite_natLifts.2

/-- Finite factorial certificates do not collapse the original
true north physical fifth-around gauge or conditional P89
source-map reflection and existing positive/negative local seams. -/
theorem fivefoldGK5BONorthPhysicalAndP89Boundary
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
  fivefoldGK5BNNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BONorthRationalData_integral_iff_factorial
#print axioms fivefoldGK5BONorthRationalData_newtonGrid
#print axioms fivefoldGK5BONorthRationalData_factorialObstruction
#print axioms fivefoldGK5BONorthOriginalSource_factorialDifferences
#print axioms fivefoldGK5BONorthP77_factorialDifferences
#print axioms fivefoldGK5BONorthPrimitive_threeSite_factorial
#print axioms fivefoldGK5BONorthDoubleInverse_threeSite_factorial
#print axioms fivefoldGK5BONorthTripleLoops_fourSite_factorial
#print axioms fivefoldGK5BONorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

import KUOS.Architecture.QiWuxingGK5BKNorthFiniteSampleRigidityV4_30
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BLLagrangeInterpolation
import Mathlib.Tactic

/-!
Qi v4.31 / F112-P94D3GK5BL — constructive Lagrange reconstruction
of genuine NORTH C60 P92B and original F55/P77 proof histories.

Independent GK5BL maps true integer-site observations into Rat[X]
and reconstructs the rational embedding of the actual Int[X]
inversion-depth polynomial when the true natDegree bound is known.

For EVERY original North F54 long→short F55 proof, the
interpolant recovers the structural chosen P92B polynomial and
EVERY Nat inverse-depth source-wrapper count. The same holds
on actual original P77 source FOUR-CELL QUOTIENTS, but only
for descended polynomial values, never for source quotient
class equality or Type-valued four-cell witnesses.

Concrete tests: the positive primitive P=1 and genuine original
double-inverse-with-right-unit P=X^2 are recovered at three
integer sites. Two REAL chosen P92B NORTH endomorphism loops
A=X^3+2 and B=2X^2+X agree at the OLD three scalar sites
{-1,1,2}; therefore their 3-site rational interpolants AGREE
but do not recover both degree-three polynomials. At the
four-site certificate {-1,0,1,2} their interpolants differ,
witnessing the independent GK5BL degree-bound requirement.

No arbitrary rational interpolation is assumed integral or
nonnegative. Neither integrality nor nonnegative coefficient
evidence implies a genuine original F55 Type witness, a chosen
P94A four-cell, GK5AY global seam or P89 unconditional reflection.
The physical NORTH fifth-Dart C60 gauge remains separate.
Strict 空, independent Kuu→Qi, original F54 two-Nat,
two-category/Blocks and Type-valued F55 proof history preserved.
Append-only root107, #1558 Draft/open/unmerged, pinned Lean
v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms/sorry/admit/native_decide/Gray restoration.
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

private def fivefoldGK5BLNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BLNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Actual F55 source witnesses at TRUE NORTH F54 endpoints:
the integer evaluation values reconstruct a REAL Rat[X]
polynomial whose coefficients are the original Int[X] embedding. -/
theorem fivefoldGK5BLNorthSource_rational_reconstruct
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat)) =
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.map
      (Int.castRingHom Rat) :=
  (nativeGK5AIOriginalToP92Structural f).gk5blInterpolate_genuine
    d sites hsize hdegree

/-- Every recovered rational coefficient equals the true
Nat-valued source wrapper count at that chosen inversion depth. -/
theorem fivefoldGK5BLNorthSource_rational_natCoeff
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d)
    (k : Nat) :
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k =
        ((nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k : Rat) :=
  (nativeGK5AIOriginalToP92Structural f).gk5blInterpolate_natCoeff
    d sites hsize hdegree k

/-- On true original NORTH source P77 4-cell quotient classes,
the interpolated Rat[X] value is the rational image of the
genuine descended Int[X] polynomial. NOT equality of classes. -/
theorem fivefoldGK5BLNorthP77_rational_reconstruct
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class
        fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat)) =
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).map
        (Int.castRingHom Rat) :=
  nativeGK5BLRationalInterpolant_recovers_P77
    fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q d sites hsize hdegree

/-- Every recovered original NORTH P77 rational coefficient
is the exact descended Nat-valued proof-occurrence certificate. -/
theorem fivefoldGK5BLNorthP77_rational_natCoeff
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d)
    (k : Nat) :
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class
        fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat))).coeff k =
      (nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q : Rat) :=
  nativeGK5BLRationalInterpolant_recovers_P77_natCoeff
    fivefoldGK5BLNorthFirst fivefoldGK5BLNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q d sites hsize hdegree k

/-- The actual primitive and original double inverse plus F55
right unit, both degree≤2, are constructively recovered
from the canonical THREE integer sites {0,1,2}. -/
theorem fivefoldGK5BLNorthPrimitiveDouble_reconstruct_three :
    nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat)) =
      (1 : Polynomial Rat) ∧
    nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
      (fun z : Int => (((nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat)) =
      (Polynomial.X : Polynomial Rat) ^ 2 := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthPrimitiveDouble_degree_le_two
  constructor
  · rw [nativeGK5BLRationalInterpolant_recovers_int
        (nativeGK5AIOriginalToP92Structural
          nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial
        2 (nativeGK5BKIntegerGrid 2) (nativeGK5BKIntegerGrid_card 2) ha]
    rw [fivefoldGK5BGNorthPrimitive_full_poly]
    simp
  · rw [nativeGK5BLRationalInterpolant_recovers_int
        (nativeGK5AIOriginalToP92Structural
          fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial
        2 (nativeGK5BKIntegerGrid 2) (nativeGK5BKIntegerGrid_card 2) hb]
    rw [fivefoldGK5BGNorthDoubleInverseUnit_full_poly]
    simp

/-- EXACTLY the three old scalar sites -1,1,2:
they are distinct but insufficient for degree-three
reconstruction in the genuine selected loop example. -/
private def fivefoldGK5BLOldThreeSites : Finset Int :=
  {(-1 : Int), 1, 2}

/-- These genuinely different selected north P92B proof
polynomials give the SAME constructed degree<3 interpolant
at the three old N,S,W observation sites. -/
theorem fivefoldGK5BLNorthTripleLoops_oldThree_interpolants_equal :
    nativeGK5BLRationalInterpolant fivefoldGK5BLOldThreeSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat)) =
    nativeGK5BLRationalInterpolant fivefoldGK5BLOldThreeSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat)) := by
  change Lagrange.interpolate fivefoldGK5BLOldThreeSites
      (fun z : Int => (z : Rat))
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat)) =
    Lagrange.interpolate fivefoldGK5BLOldThreeSites
      (fun z : Int => (z : Rat))
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))
  apply Lagrange.interpolate_eq_of_values_eq_on
  intro z hz
  change z ∈ ({(-1 : Int), 1, 2} : Finset Int) at hz
  simp only [Finset.mem_insert, Finset.mem_singleton] at hz
  rcases hz with hneg | hone | htwo
  · subst z
    exact congrArg (fun t : Int => (t : Rat))
      fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing.1
  · subst z
    exact congrArg (fun t : Int => (t : Rat))
      fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing.2.1
  · subst z
    exact congrArg (fun t : Int => (t : Rat))
      fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing.2.2.1

/-- Four actual integer sites include zero, which is a
provably independent observation for the north loop pair. -/
private def fivefoldGK5BLFourSites : Finset Int :=
  {(-1 : Int), 0, 1, 2}

theorem fivefoldGK5BLFourSites_card :
    fivefoldGK5BLFourSites.card = 4 := by
  decide

theorem fivefoldGK5BLFourSites_has_zero :
    (0 : Int) ∈ fivefoldGK5BLFourSites := by
  simp [fivefoldGK5BLFourSites]

/-- With the fourth integer observation, constructive
interpolants separate two real selected P92B north loops.
Their old scalar values N=3,S=1,W=10 had agreed. -/
theorem fivefoldGK5BLNorthTripleLoops_four_interpolants_ne :
    nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat)) ≠
    nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat)) := by
  intro h
  have heq := congrArg (fun P : Polynomial Rat => P.eval (0 : Rat)) h
  change
    (nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))).eval
        (0 : Rat) =
    (nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))).eval
        (0 : Rat) at heq
  rw [nativeGK5BLRationalInterpolant_eval_node
        fivefoldGK5BLFourSites
        (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))
        0 fivefoldGK5BLFourSites_has_zero,
      nativeGK5BLRationalInterpolant_eval_node
        fivefoldGK5BLFourSites
        (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))
        0 fivefoldGK5BLFourSites_has_zero] at heq
  have hh : fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (0 : Int) =
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (0 : Int) := by
    exact_mod_cast heq
  exact fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing.2.2.2 hh

/-- The original selected north loops also reconstruct their
exact rational-embedded degree-three polynomials from the
four distinct sites {-1,0,1,2}. -/
theorem fivefoldGK5BLNorthTripleLoops_four_recover :
    nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat)) =
      fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.map (Int.castRingHom Rat) ∧
    nativeGK5BLRationalInterpolant fivefoldGK5BLFourSites
      (fun z : Int => ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat)) =
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.map (Int.castRingHom Rat) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  constructor
  · exact nativeGK5BLRationalInterpolant_recovers_int
      fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial
      3 fivefoldGK5BLFourSites fivefoldGK5BLFourSites_card ha
  · exact nativeGK5BLRationalInterpolant_recovers_int
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial
      3 fivefoldGK5BLFourSites fivefoldGK5BLFourSites_card hb

/-- Preserves original genuine north physical fifth-Dart closure,
positive/negative local seam boundary and the conditional
P89 BadPair reflection. No numerical sample creates a seam. -/
theorem fivefoldGK5BLNorthPhysicalAndAuthorityBoundary
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
  fivefoldGK5BKNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BLNorthSource_rational_reconstruct
#print axioms fivefoldGK5BLNorthSource_rational_natCoeff
#print axioms fivefoldGK5BLNorthP77_rational_reconstruct
#print axioms fivefoldGK5BLNorthP77_rational_natCoeff
#print axioms fivefoldGK5BLNorthPrimitiveDouble_reconstruct_three
#print axioms fivefoldGK5BLNorthTripleLoops_oldThree_interpolants_equal
#print axioms fivefoldGK5BLFourSites_card
#print axioms fivefoldGK5BLFourSites_has_zero
#print axioms fivefoldGK5BLNorthTripleLoops_four_interpolants_ne
#print axioms fivefoldGK5BLNorthTripleLoops_four_recover
#print axioms fivefoldGK5BLNorthPhysicalAndAuthorityBoundary

end
end KUOS.Architecture.WuxingPentagonUnified

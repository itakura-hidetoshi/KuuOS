import KUOS.Architecture.QiWuxingGK5BLNorthLagrangeReconstructionV4_31
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BMIntegralNatLiftCertificates
import Mathlib.Tactic

/-!
Qi v4.32 / F112-P94D3GK5BM — exact rational interpolant
integer/Nat coefficient lifting boundaries at genuine NORTH C60.

Independent Kuu GK5BM proves:
Rat[X] lies in the Int[X] coefficient image exactly when ALL
coefficients are integer casts; it lies in the Nat[X] image
exactly when ALL coefficients are integral AND nonnegative.
These are actual constructive finite-support monomial lifts.

On the true original north F54 long→short Hom, every genuine
F55 source proof has a Nat[X] coefficient lift of the GK5BL
rational interpolant, using its real nonnegative GK5BJ depth
counts. A Nat[X] coefficient lift exists also for every TRUE
original P77 source four-cell quotient polynomial VALUE.
No equality of original Type-valued F55 sources or P77 classes
is inferred from equality of rational coefficients.

The actual primitive and double inverse with true F55 right
unit recover Nat-lifted polynomial VALUES on {0,1,2}. The
actual chosen north P92B endomorphism loops A=X³+2 and
B=2X²+X each recover Nat-lifted values on {-1,0,1,2}.
These are not original-to-phi seam counterexamples.

As a control, the rational polynomial -X has a negative
coefficient and NO Nat[X] lift; arbitrary rational data need
not meet the north P92B positive-coefficient certificate.

Physical fifth-around north gauge and P89 BadPair reflection
remain distinct and conditional. No W=1→local seam, no global
GK5AY seam, GK5BA kit, P94A normal form, Gray or P89
unconditional faithfulness. Strict 空 authority, independent
Kuu→Qi, true original F54 two-Nat/two-category/Blocks and
F55 Type histories retained. Append-only public root107,
protected #1558 Draft/open/unmerged; fixed Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide.
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

private def fivefoldGK5BMNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BMNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The GK5BL rational interpolation of EVERY original true
north F55 source is the image of SOME Nat[X] polynomial,
without assuming a new F55 Type-valued witness. -/
theorem fivefoldGK5BMNorthSource_natLift
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites
        (fun z : Int =>
          (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z : Int) : Rat)) :=
  (nativeGK5AIOriginalToP92Structural f).gk5bmInterpolant_natLift
    d sites hsize hdegree

/-- Its rational coefficients are separately integral and
nonnegative, with an ACTUAL Nat witness at every depth. -/
theorem fivefoldGK5BMNorthSource_integral_nonneg
    (f : NativeGK5AINorthPentagonCells)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d)
    (k : Nat) :
    (∃ z : Int, (z : Rat) =
      (nativeGK5BLRationalInterpolant sites
        (fun i : Int =>
          (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval i : Int) : Rat))).coeff k) ∧
    0 ≤ (nativeGK5BLRationalInterpolant sites
      (fun i : Int =>
        (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval i : Int) : Rat))).coeff k := by
  exact (nativeGK5BMNatLift_iff_integral_nonneg _).1
    (fivefoldGK5BMNorthSource_natLift f d sites hsize hdegree) k

/-- Every true original NORTH P77 quotient polynomial VALUE
admits the genuine Nat coefficient lift; no conclusion about
equality of distinct original P77 classes is asserted. -/
theorem fivefoldGK5BMNorthP77_natLift
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BMNorthFirst fivefoldGK5BMNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BMNorthFirst fivefoldGK5BMNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites
        (fun z : Int => (((nativeGK5BGPolyOnP77Class
          fivefoldGK5BMNorthFirst fivefoldGK5BMNorthLast
          northNativeF45PentagonLong northNativeF45PentagonShort q).eval z : Int) : Rat)) :=
  nativeGK5BMInterpolant_P77_natLift
    fivefoldGK5BMNorthFirst fivefoldGK5BMNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q d sites hsize hdegree

/-- An arbitrary rational sample family over NORTH integer
sites satisfies the Nat[X] certificate precisely when EVERY
interpolated coefficient is integral and nonnegative. -/
theorem fivefoldGK5BMNorthRationalData_nat_iff
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Nat,
      P.map (Nat.castRingHom Rat) =
        nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k : Nat,
      (∃ z : Int, (z : Rat) =
        (nativeGK5BLRationalInterpolant sites values).coeff k) ∧
        0 ≤ (nativeGK5BLRationalInterpolant sites values).coeff k) :=
  nativeGK5BMInterpolant_nat_iff sites values

/-- The actual original primitive has a Nat[X] lifted
interpolant at the canonical three integer sites {0,1,2}. -/
theorem fivefoldGK5BMNorthPrimitive_threeSite_natLift :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
        (fun z : Int => (((nativeGK5AIOriginalToP92Structural
          nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z : Int) : Rat)) :=
  fivefoldGK5BMNorthSource_natLift
    nativeGK5AGNorthOriginalCell 2 (nativeGK5BKIntegerGrid 2)
    (nativeGK5BKIntegerGrid_card 2)
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1

/-- The true original double inverse with right F55 identity
also admits an independently typed Nat[X] coefficient lift. -/
theorem fivefoldGK5BMNorthDoubleInverse_threeSite_natLift :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid 2)
        (fun z : Int => (((nativeGK5AIOriginalToP92Structural
          fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z : Int) : Rat)) :=
  fivefoldGK5BMNorthSource_natLift
    fivefoldGK5BFNorthDoubleInverseRightUnit 2
    (nativeGK5BKIntegerGrid 2) (nativeGK5BKIntegerGrid_card 2)
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2

/-- Two true chosen NORTH P92B endo loops have Nat[X] lifts
of their separately reconstructed rational degree-three
polynomials on the old three sites PLUS zero. -/
theorem fivefoldGK5BMNorthTripleLoops_fourSite_natLifts :
    (∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant
        ({(-1 : Int), 0, 1, 2} : Finset Int)
        (fun z : Int =>
          ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z : Int) : Rat))) ∧
    (∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant
        ({(-1 : Int), 0, 1, 2} : Finset Int)
        (fun z : Int =>
          ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z : Int) : Rat))) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  have hs : ({(-1 : Int), 0, 1, 2} : Finset Int).card = 4 := by decide
  constructor
  · exact fivefoldGK5BGNorthTripleLoopA.gk5bmInterpolant_natLift
      3 ({(-1 : Int), 0, 1, 2} : Finset Int) hs ha
  · exact fivefoldGK5BGNorthTripleLoopB.gk5bmInterpolant_natLift
      3 ({(-1 : Int), 0, 1, 2} : Finset Int) hs hb

/-- The concrete nonpositive rational polynomial -X has a
negative depth-one coefficient and NO Nat polynomial source.
This is only a rational DATA counterexample, not a source
F55 proof or a P94A seam counterexample. -/
theorem fivefoldGK5BMNegativeX_no_natLift :
    ¬ ∃ P : Polynomial Nat,
      P.map (Nat.castRingHom Rat) = -(Polynomial.X : Polynomial Rat) := by
  apply nativeGK5BMNoNatLift_of_negative_coeff
    (-(Polynomial.X : Polynomial Rat)) 1
  norm_num

/-- Original C60 authority remains independent: existing
positive/negative local seams, true physical fifth-Dart closure,
and only CONDITIONAL P89 source-map reflection. -/
theorem fivefoldGK5BMNorthPhysicalAndP89Boundary
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
  fivefoldGK5BLNorthPhysicalAndAuthorityBoundary frame i

#print axioms fivefoldGK5BMNorthSource_natLift
#print axioms fivefoldGK5BMNorthSource_integral_nonneg
#print axioms fivefoldGK5BMNorthP77_natLift
#print axioms fivefoldGK5BMNorthRationalData_nat_iff
#print axioms fivefoldGK5BMNorthPrimitive_threeSite_natLift
#print axioms fivefoldGK5BMNorthDoubleInverse_threeSite_natLift
#print axioms fivefoldGK5BMNorthTripleLoops_fourSite_natLifts
#print axioms fivefoldGK5BMNegativeX_no_natLift
#print axioms fivefoldGK5BMNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

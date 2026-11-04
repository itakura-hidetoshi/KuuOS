import KUOS.Architecture.QiWuxingGK5BPNorthRawStirlingV4_35
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BQSignedStirlingDivisibility
import Mathlib.Tactic

/-!
Qi v4.36 / F112-P94D3GK5BQ — TRUE NORTH C60
SIGNED MATHLIB STIRLING / RAW INTEGER DIVISIBILITY CERTIFICATES.

Independent GK5BQ proves the true falling factorial coefficients
are (-1)^(k-j) Nat.stirlingFirst k j for j≤k. It also
constructs actual integer numerators from raw integer samples
and proves Int[X] realization iff all are divisible by d!.

On the true original north F54 two-Nat/two-category/Blocks
geometry, original F55 Type-valued witnesses are INPUT ONLY.
The original true F55/P77 quotient supplies its independently
descended integer polynomial VALUE, never quotient equality.
Original primitive, double inverse with genuine F55 right unit,
and chosen two P92B loops have separate certificates.

The original fifth-around physical C60 gauge, positive/negative
original-phi local seams, and conditional P89 BadPair reflection
are kept independent of numerical coefficient tests. No new
original F55 Type source, P94A four-cell, universal GK5AY seam,
GK5BA kit, unconditional P89 reflection, Gray or W=1→seam.

Strict 空; independent Kuu→Qi; public root107 append-only.
Protected PR #1558 Draft/open/unmerged. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry/admit/native_decide.
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

private def fivefoldGK5BQNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BQNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The ACTUAL pinned Nat.stirlingFirst formula, not merely
a suggestive name: the coefficient s(k,j) of the original
integer falling factorial is its correctly signed count. -/
theorem fivefoldGK5BQNorthSignedStirling_formula
    (k j : Nat) (hj : j ≤ k) :
    nativeGK5BPSignedFirst k j =
      (-1 : Int) ^ (k - j) * (Nat.stirlingFirst k j : Int) :=
  nativeGK5BQSignedFirst_eq_natStirling k j hj

/-- Every raw integer observation table has a complete,
necessary and sufficient d!-DIVISIBILITY criterion for an
actual Int[X] Newton coefficient lift. -/
theorem fivefoldGK5BQNorthRaw_integerLift_iff_divisible
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values) :=
  nativeGK5BQNewton_integral_iff_divisible d values

/-- The same EXACT finite test for GK5BL's actual Lagrange
interpolant, on the genuine canonical integer site set. -/
theorem fivefoldGK5BQNorthLagrange_integerLift_iff_divisible
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values) :=
  nativeGK5BQLagrange_integral_iff_divisible d values

/-- Single failed original integer-numerator divisibility
test is an OBSTRUCTION to Int[X] coefficient realization,
not evidence for a P89 or original-phi seam obstruction. -/
theorem fivefoldGK5BQNorthRaw_notDivisible_obstructs
    (d : Nat) (values : Nat → Int)
    (j : Nat) (hj : j ∈ Finset.range (d + 1))
    (hnot : ¬ (d.factorial : Int) ∣
      nativeGK5BQClearedNumerator d j values) :
    ¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat)) :=
  nativeGK5BQNoIntegerLift_of_notDvd d values j hj hnot

/-- An ACTUAL integer polynomial P and a true degree bound
force the explicit factorial divisibility certificate for
its own finite raw integer observations, using Qi v4.35
source reconstruction and independent GK5BQ equivalence. -/
theorem fivefoldGK5BQIntegerSource_divisibility
    (P : Polynomial Int) (d : Nat) (hdegree : P.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j
        (fun n : Nat => P.eval (n : Int)) := by
  apply (nativeGK5BQNewton_integral_iff_divisible d
    (fun n : Nat => P.eval (n : Int))).1
  apply (nativeGK5BPNewton_integral_iff_rawStirling d
    (fun n : Nat => ((P.eval (n : Int) : Int) : Rat))).2
  exact fivefoldGK5BPIntegerSource_rawStirling P d hdegree

/-- Every real original NORTH F55 source, through its existing
true P92B structural image's Int polynomial depth value, has
an ACTUAL raw integer sample divisible-numerator certificate. -/
theorem fivefoldGK5BQNorthOriginalF55_divisibility
    (f : NativeGK5AINorthPentagonCells) (d : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j
        (fun n : Nat =>
          (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval
            (n : Int)) :=
  fivefoldGK5BQIntegerSource_divisibility
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial d hdegree

/-- Every true original F55/P77 source quotient supplies a
divisibility certificate for its already DESCENDED Int[X]
polynomial VALUE; no identification of source Type classes. -/
theorem fivefoldGK5BQNorthP77_divisibility
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BQNorthFirst fivefoldGK5BQNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BQNorthFirst fivefoldGK5BQNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j
        (fun n : Nat => (nativeGK5BGPolyOnP77Class
          fivefoldGK5BQNorthFirst fivefoldGK5BQNorthLast
          northNativeF45PentagonLong northNativeF45PentagonShort q).eval
            (n : Int)) :=
  fivefoldGK5BQIntegerSource_divisibility
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BQNorthFirst fivefoldGK5BQNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d hdegree

/-- Actual north primitive P=1: an original Type witness
and true 3-observation d!=2 divisibility certificate. -/
theorem fivefoldGK5BQNorthPrimitive_threeSite_divisibility :
    ∀ j ∈ Finset.range (2 + 1),
      ((2 : Nat).factorial : Int) ∣ nativeGK5BQClearedNumerator 2 j
        (fun n : Nat =>
          (nativeGK5AIOriginalToP92Structural
            nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (n : Int)) :=
  fivefoldGK5BQNorthOriginalF55_divisibility
    nativeGK5AGNorthOriginalCell 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1

/-- Actual north double inverse WITH original F55 right unit:
a different true Type source and distinct 3-observation test. -/
theorem fivefoldGK5BQNorthDoubleInverse_threeSite_divisibility :
    ∀ j ∈ Finset.range (2 + 1),
      ((2 : Nat).factorial : Int) ∣ nativeGK5BQClearedNumerator 2 j
        (fun n : Nat =>
          (nativeGK5AIOriginalToP92Structural
            fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
              (n : Int)) :=
  fivefoldGK5BQNorthOriginalF55_divisibility
    fivefoldGK5BFNorthDoubleInverseRightUnit 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2

/-- Two actual chosen north P92B endo loops with respective
polynomials X³+2 and 2X²+X each pass the new 4-observation
d!=6 finite test on {0,1,2,3}. Existing source histories
are NOT identified by this arithmetic property. -/
theorem fivefoldGK5BQNorthTripleLoops_fourSite_divisibility :
    (∀ j ∈ Finset.range (3 + 1),
      ((3 : Nat).factorial : Int) ∣ nativeGK5BQClearedNumerator 3 j
        (fun n : Nat =>
          fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (n : Int))) ∧
    (∀ j ∈ Finset.range (3 + 1),
      ((3 : Nat).factorial : Int) ∣ nativeGK5BQClearedNumerator 3 j
        (fun n : Nat =>
          fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (n : Int))) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  exact ⟨fivefoldGK5BQIntegerSource_divisibility
           fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial 3 ha,
         fivefoldGK5BQIntegerSource_divisibility
           fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial 3 hb⟩

/-- Original physical fifth-around north gauge and conditional
P89 BadPair reflection remain INDEPENDENT from arithmetic
divisibility, as do original positive/negative local seams. -/
theorem fivefoldGK5BQNorthPhysicalAndP89Boundary
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
  fivefoldGK5BPNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BQNorthSignedStirling_formula
#print axioms fivefoldGK5BQNorthRaw_integerLift_iff_divisible
#print axioms fivefoldGK5BQNorthLagrange_integerLift_iff_divisible
#print axioms fivefoldGK5BQNorthRaw_notDivisible_obstructs
#print axioms fivefoldGK5BQIntegerSource_divisibility
#print axioms fivefoldGK5BQNorthOriginalF55_divisibility
#print axioms fivefoldGK5BQNorthP77_divisibility
#print axioms fivefoldGK5BQNorthPrimitive_threeSite_divisibility
#print axioms fivefoldGK5BQNorthDoubleInverse_threeSite_divisibility
#print axioms fivefoldGK5BQNorthTripleLoops_fourSite_divisibility
#print axioms fivefoldGK5BQNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

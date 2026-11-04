import KUOS.Architecture.QiWuxingGK5BQNorthSignedStirlingV4_36
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BRPrimePowerLocalGlobal
import Mathlib.Tactic

/-!
Qi v4.37 / F112-P94D3GK5BR — TRUE NORTH C60
PRIME-POWER LOCAL / GLOBAL FACTORIAL CERTIFICATES.

Independent GK5BR upgrades true integer raw observation
factorial divisibility to the finite family of actual maximal
prime-power congruences, including zero and negative numerators.
Here the local-to-global integer coefficient lift applies to
original north F55 structural polynomial VALUES and original
F55/P77 descended polynomial VALUES. No quotient class or
Type-valued source is reconstructed by arithmetic alone.

The actual north primitive and distinct double-inverse plus
original F55 right unit both pass their own finite prime-power
checks yet possess OPPOSITE original-phi local seam verdicts.
Two genuine independently selected P92B loops likewise pass
their separate d=3 finite prime-power tests. Fifth-around
physical C60 gauge and conditional original P89 BadPair
reflection remain independent from the arithmetic certificate.

Strict 空; independent Kuu→Qi; F54 two-Nat/two-category/
Blocks and original F55 Type histories retained. No new F55
source, P94A four-cell, universal GK5AY seam, unconditional
P89 reflection, GK5BA kit, Gray, or W=1→seam.
Append-only public root107; #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

private def fivefoldGK5BRNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BRNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The original north factorial exponent is the pinned
Mathlib p-adic valuation at every ACTUAL prime p. -/
theorem fivefoldGK5BRNorthFactorial_primeExponent
    (d p : Nat) (hp : p.Prime) :
    (d.factorial).factorization p = padicValNat p d.factorial :=
  nativeGK5BRFactorial_exponent_eq_padic d p hp

/-- For arbitrary original integer raw values, the single
global Int[X] Newton lift is equivalent to all genuinely
finite p-power local certificates of its GK5BQ numerators. -/
theorem fivefoldGK5BRNorthRaw_integerLift_iff_primePower
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p) :=
  nativeGK5BRNewton_integral_iff_primePower d values

/-- The exact same local-to-global arithmetic descent
holds for the ACTUAL GK5BL Lagrange interpolant on
canonical original integer observation sites. -/
theorem fivefoldGK5BRNorthLagrange_integerLift_iff_primePower
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p) :=
  nativeGK5BRLagrange_integral_iff_primePower d values

/-- A fully executable finite arithmetic presentation:
one original integer source polynomial exists exactly when
all actual numerators vanish modulo each prime-power factor. -/
theorem fivefoldGK5BRNorthRaw_integerLift_iff_congruences
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BQClearedNumerator d j values %
          ((p ^ ((d.factorial).factorization p) : Nat) : Int) = 0) :=
  nativeGK5BRNewton_integral_iff_congruences d values

/-- The absence of a global integer coefficient source is
exactly witnessed by some finite pair of coefficient index
and ACTUAL prime factor with a failed local p-power test.
This is NOT an original-phi seam obstruction. -/
theorem fivefoldGK5BRNorthRaw_noLift_iff_localFailure
    (d : Nat) (values : Nat → Int) :
    (¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∃ j ∈ Finset.range (d + 1),
      ∃ p ∈ (d.factorial).primeFactors,
        ¬ nativeGK5BRPrimeLocal d j values p) :=
  nativeGK5BRNoIntegerLift_iff_exists_localFailure d values

/-- Every ACTUAL integer polynomial source with its
degree bound has all prime-power local certificates for
its true finite integer observations. -/
theorem fivefoldGK5BRIntegerSource_primeLocal
    (P : Polynomial Int) (d : Nat) (hdegree : P.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j
          (fun n : Nat => P.eval (n : Int)) p := by
  intro j hj
  exact (nativeGK5BRFactorial_dvd_iff_finiteLocal d j
    (fun n : Nat => P.eval (n : Int))).1
      (fivefoldGK5BQIntegerSource_divisibility P d hdegree j hj)

/-- Each real original F55 north Type-valued witness has
a true P92B structural image whose Int polynomial depth
VALUE carries the finite local prime-power certificates.
Arithmetic does not reconstruct that original Type witness. -/
theorem fivefoldGK5BRNorthOriginalF55_primeLocal
    (f : NativeGK5AINorthPentagonCells) (d : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval
              (n : Int)) p :=
  fivefoldGK5BRIntegerSource_primeLocal
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial d hdegree

/-- Each genuine original F55/P77 class supplies only
its already DESCENDED integer polynomial VALUE for this
test. No raw Type-valued quotient equality is deduced. -/
theorem fivefoldGK5BRNorthP77_primeLocal
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BRNorthFirst fivefoldGK5BRNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BRNorthFirst fivefoldGK5BRNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j
          (fun n : Nat => (nativeGK5BGPolyOnP77Class
            fivefoldGK5BRNorthFirst fivefoldGK5BRNorthLast
            northNativeF45PentagonLong northNativeF45PentagonShort q).eval
              (n : Int)) p :=
  fivefoldGK5BRIntegerSource_primeLocal
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BRNorthFirst fivefoldGK5BRNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d hdegree

/-- The genuine north primitive F55 source has all
prime-power conditions at its own canonical three sites. -/
theorem fivefoldGK5BRNorthPrimitive_threeSite_primeLocal :
    ∀ j ∈ Finset.range (2 + 1),
      ∀ p ∈ ((2 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (n : Int)) p :=
  fivefoldGK5BRNorthOriginalF55_primeLocal
    nativeGK5AGNorthOriginalCell 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1

/-- The genuine north DOUBLE inverse with original F55
RIGHT UNIT separately has its own degree-two prime-power
certificate; it is a different Type source from primitive. -/
theorem fivefoldGK5BRNorthDoubleInverse_threeSite_primeLocal :
    ∀ j ∈ Finset.range (2 + 1),
      ∀ p ∈ ((2 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
                (n : Int)) p :=
  fivefoldGK5BRNorthOriginalF55_primeLocal
    fivefoldGK5BFNorthDoubleInverseRightUnit 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2

/-- Two distinct actually selected P92B north loops
(X^3+2 and 2X^2+X) have separate complete prime-power
certificates at the exact four sites {0,1,2,3}. -/
theorem fivefoldGK5BRNorthTripleLoops_fourSite_primeLocal :
    (∀ j ∈ Finset.range (3 + 1),
      ∀ p ∈ ((3 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 3 j
          (fun n : Nat =>
            fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (n : Int)) p) ∧
    (∀ j ∈ Finset.range (3 + 1),
      ∀ p ∈ ((3 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 3 j
          (fun n : Nat =>
            fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (n : Int)) p) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  exact ⟨fivefoldGK5BRIntegerSource_primeLocal
           fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial 3 ha,
         fivefoldGK5BRIntegerSource_primeLocal
           fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial 3 hb⟩

/-- MATHEMATICALLY IMPORTANT AUTHORITY BOUNDARY:
both real north F55 sources satisfy their OWN finite
local arithmetic tests, although one has an actual
original-phi local seam and the other provably does NOT.
Hence arithmetic prime-power gluing alone cannot be
identified with a true F55/P94A structural seam. -/
theorem fivefoldGK5BRNorthBothLocalButOppositeSeams
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (∀ j ∈ Finset.range (2 + 1),
      ∀ p ∈ ((2 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (n : Int)) p) ∧
    (∀ j ∈ Finset.range (2 + 1),
      ∀ p ∈ ((2 : Nat).factorial).primeFactors,
        nativeGK5BRPrimeLocal 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
                (n : Int)) p) ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hyes, hno, _, _⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨fivefoldGK5BRNorthPrimitive_threeSite_primeLocal,
    fivefoldGK5BRNorthDoubleInverse_threeSite_primeLocal, hyes, hno⟩

/-- The ACTUAL original north fifth-around C60 physical
gauge and conditional P89 BadPair reflection still come
from their unchanged Type-valued theorems, not from any
integer prime-power certificate. -/
theorem fivefoldGK5BRNorthPhysicalAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  obtain ⟨_, _, hphysical, hreflection⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨hphysical, hreflection⟩

#print axioms fivefoldGK5BRNorthFactorial_primeExponent
#print axioms fivefoldGK5BRNorthRaw_integerLift_iff_primePower
#print axioms fivefoldGK5BRNorthLagrange_integerLift_iff_primePower
#print axioms fivefoldGK5BRNorthRaw_integerLift_iff_congruences
#print axioms fivefoldGK5BRNorthRaw_noLift_iff_localFailure
#print axioms fivefoldGK5BRIntegerSource_primeLocal
#print axioms fivefoldGK5BRNorthOriginalF55_primeLocal
#print axioms fivefoldGK5BRNorthP77_primeLocal
#print axioms fivefoldGK5BRNorthPrimitive_threeSite_primeLocal
#print axioms fivefoldGK5BRNorthDoubleInverse_threeSite_primeLocal
#print axioms fivefoldGK5BRNorthTripleLoops_fourSite_primeLocal
#print axioms fivefoldGK5BRNorthBothLocalButOppositeSeams
#print axioms fivefoldGK5BRNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

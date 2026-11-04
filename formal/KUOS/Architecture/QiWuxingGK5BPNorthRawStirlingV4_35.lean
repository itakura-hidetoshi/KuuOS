import KUOS.Architecture.QiWuxingGK5BONorthFactorialDifferenceV4_34
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BPRawNewtonStirling
import Mathlib.Tactic

/-!
Qi v4.35 — genuine NORTH C60 RAW observations / Newton
signed first-kind Stirling certificates.

For the first time this sequence reads ONLY integer-indexed
observations of real original typed F55/P92B histories, rather
than assuming original monomial coefficients are supplied as
reconstruction inputs. Independent GK5BP proves an exact
rational Newton interpolation and a finite signed-Stirling
coefficient-lift criterion. A true original F55/P77 quotient
class is used only to supply its genuinely DESCENDED Int[X]
polynomial value; equality of such values never identifies
source Type-valued P77 classes.

The north primitive (P=1), genuine double inverse plus original
F55 right unit (P=X²), and chosen P92B loops A=X³+2 and
B=2X²+X are checked on the canonical nonnegative integer
grids {0,1,2} and {0,1,2,3}; the latter is a NEW grid, not the
old {-1,0,1,2} four-point Lagrange set.

Physical fifth-around C60 gauge and conditional P89 BadPair
reflection remain independent, as do the original-phi local
seam existence/obstruction results. No new Type-valued F55
source, P94A four-cell, universal GK5AY seam, GK5BA kit,
unconditional P89 reflection or Gray restoration.

Strict 空 authority; independent Kuu→Qi; original F54
two Nat/two categories/Blocks and F55 Type history retained.
Append-only root107, #1558 Draft/open/unmerged, pinned
Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

private def fivefoldGK5BPNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BPNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The finite raw signed-Stirling integrality certificate.
Only finite observations values(0),...,values(d), their genuine
forward differences, and signed falling-factorial coefficients
appear, not coefficients of an unknown original source. -/
def fivefoldGK5BPRawStirlingCertificate
    (d : Nat) (values : Nat → Rat) : Prop :=
  ∀ j ∈ Finset.range (d + 1), ∃ z : Int,
    (z : Rat) =
      ∑ k ∈ Finset.range (d + 1),
        (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
          (nativeGK5BPSignedFirst k j : Rat)

/-- Raw north integer-indexed observation data have a genuine
Int[X] Newton polynomial source IFF the FINITE signed-Stirling
certificate holds. This does not realize source Type witnesses. -/
theorem fivefoldGK5BPNorthRaw_iff_integerPolynomial
    (d : Nat) (values : Nat → Rat) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d values) ↔
        fivefoldGK5BPRawStirlingCertificate d values :=
  nativeGK5BPNewton_integral_iff_rawStirling d values

/-- The same necessary-and-sufficient certificate applies to
the ACTUAL GK5BL rational Lagrange interpolant of raw north
observations on the canonical integer grid. -/
theorem fivefoldGK5BPNorthLagrange_iff_rawStirling
    (d : Nat) (values : Nat → Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
        (fun z : Int => values z.toNat)) ↔
          fivefoldGK5BPRawStirlingCertificate d values :=
  nativeGK5BPLagrange_integral_iff_rawStirling d values

/-- For an actual Int[X] polynomial of degree ≤d, its
observed integer-indexed values supply the raw signed-Stirling
finite certificate, by actual Lagrange recovery. This theorem
does NOT assume that arbitrary raw values admit Int[X] lifts. -/
theorem fivefoldGK5BPIntegerSource_rawStirling
    (P : Polynomial Int) (d : Nat) (hdegree : P.natDegree ≤ d) :
    fivefoldGK5BPRawStirlingCertificate d
      (fun n : Nat => ((P.eval (n : Int) : Int) : Rat)) := by
  apply (fivefoldGK5BPNorthLagrange_iff_rawStirling d
    (fun n : Nat => ((P.eval (n : Int) : Int) : Rat))).1
  refine ⟨P, ?_⟩
  have hdata :
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
          (fun z : Int => ((P.eval (z.toNat : Int) : Int) : Rat)) =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
          (fun z : Int => ((P.eval z : Int) : Rat)) := by
    apply Lagrange.interpolate_eq_of_values_eq_on
    intro z hz
    change z ∈ (Finset.range (d + 1)).image
      (fun k : Nat => (k : Int)) at hz
    rcases Finset.mem_image.mp hz with ⟨k, hk, hzk⟩
    subst z
    simp
  rw [hdata]
  exact (nativeGK5BLRationalInterpolant_recovers_int P d
    (nativeGK5BKIntegerGrid d) (nativeGK5BKIntegerGrid_card d) hdegree).symm

/-- Genuine ORIGINAL north F55 source f: its true integer
P92B depth polynomial evaluations at 0,...,d pass the
complete finite signed-Stirling integrality certificate. -/
theorem fivefoldGK5BPNorthOriginalF55_rawStirling
    (f : NativeGK5AINorthPentagonCells) (d : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    fivefoldGK5BPRawStirlingCertificate d
      (fun n : Nat =>
        (((nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval
          (n : Int) : Int) : Rat)) :=
  fivefoldGK5BPIntegerSource_rawStirling
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial d hdegree

/-- A genuine ORIGINAL F55/P77 four-cell quotient q has the
same finite raw observation certificate for its DESCENDED
polynomial value, not a newly reconstructed Type proof/class. -/
theorem fivefoldGK5BPNorthP77_rawStirling
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BPNorthFirst fivefoldGK5BPNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BPNorthFirst fivefoldGK5BPNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    fivefoldGK5BPRawStirlingCertificate d
      (fun n : Nat => (((nativeGK5BGPolyOnP77Class
        fivefoldGK5BPNorthFirst fivefoldGK5BPNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q).eval
          (n : Int) : Int) : Rat)) :=
  fivefoldGK5BPIntegerSource_rawStirling
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BPNorthFirst fivefoldGK5BPNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d hdegree

/-- True original north primitive P=1 has the raw
three-integer-observation signed-Stirling certificate. -/
theorem fivefoldGK5BPNorthPrimitive_rawStirling :
    fivefoldGK5BPRawStirlingCertificate 2
      (fun n : Nat =>
        (((nativeGK5AIOriginalToP92Structural
          nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval
          (n : Int) : Int) : Rat)) :=
  fivefoldGK5BPNorthOriginalF55_rawStirling
    nativeGK5AGNorthOriginalCell 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1

/-- True original north double inverse WITH real right F55
identity has an independent raw 3-site certificate. -/
theorem fivefoldGK5BPNorthDoubleInverse_rawStirling :
    fivefoldGK5BPRawStirlingCertificate 2
      (fun n : Nat =>
        (((nativeGK5AIOriginalToP92Structural
          fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
          (n : Int) : Int) : Rat)) :=
  fivefoldGK5BPNorthOriginalF55_rawStirling
    fivefoldGK5BFNorthDoubleInverseRightUnit 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2

/-- The two genuinely chosen north P92B endomorphism loops
each have a separately typed raw four-observation certificate
on the NEW grid {0,1,2,3}, not an original-to-phi seam claim. -/
theorem fivefoldGK5BPNorthTripleLoops_rawStirling :
    fivefoldGK5BPRawStirlingCertificate 3
      (fun n : Nat =>
        ((fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval
          (n : Int) : Int) : Rat)) ∧
    fivefoldGK5BPRawStirlingCertificate 3
      (fun n : Nat =>
        ((fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval
          (n : Int) : Int) : Rat)) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  exact ⟨fivefoldGK5BPIntegerSource_rawStirling
           fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial 3 ha,
         fivefoldGK5BPIntegerSource_rawStirling
           fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial 3 hb⟩

/-- The coefficient/arithmetic observation layer remains
separate from the TRUE physical north C60 fifth-gauge closure,
existing original positive/negative seams and conditional
original P89 BadPair source-reflection obstruction. -/
theorem fivefoldGK5BPNorthPhysicalAndP89Boundary
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
  fivefoldGK5BONorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BPNorthRaw_iff_integerPolynomial
#print axioms fivefoldGK5BPNorthLagrange_iff_rawStirling
#print axioms fivefoldGK5BPIntegerSource_rawStirling
#print axioms fivefoldGK5BPNorthOriginalF55_rawStirling
#print axioms fivefoldGK5BPNorthP77_rawStirling
#print axioms fivefoldGK5BPNorthPrimitive_rawStirling
#print axioms fivefoldGK5BPNorthDoubleInverse_rawStirling
#print axioms fivefoldGK5BPNorthTripleLoops_rawStirling
#print axioms fivefoldGK5BPNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

import KUOS.Architecture.QiWuxingGK5BSNorthCRTGluingV4_38
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BTNoncoprimeCRTOverlapObstruction
import Mathlib.Tactic

/-!
Qi v4.39 — genuine north C60 noncoprime CRT overlap.
Independent GK5BT proves exact gcd compatibility and lcm
gluing. Here only existing original F55 / P77 polynomial
VALUES are observed. Genuine Type sources, quotient classes,
P94A four-cells, original seams, and conditional P89
reflection are never inferred from numeric congruences.
Strict 空, independent Kuu→Qi; F54 two-Nat/two-category/
Blocks and original F55 Type history unchanged. Public
root107, #1558 Draft/open, pinned Lean 4.30.0-rc2 and
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry, admit, native_decide, GK5BA kit, Gray.
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

private def fivefoldGK5BTNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage
private def fivefoldGK5BTNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Original integer polynomial observations with every
actual GK5BQ cleared numerator having ZERO overlap-glue
class for m,n. This is a numeric predicate, not F55 Type. -/
abbrev fivefoldGK5BTNorthCRTZero
    (P : Polynomial Int) (d m n : Nat) : Prop :=
  ∀ j ∈ Finset.range (d + 1),
    (nativeGK5BTOverlapGlue m n
      (nativeGK5BTObservedNumeratorAbs d j
        (fun k : Nat => P.eval (k : Int)) % m)
      (nativeGK5BTObservedNumeratorAbs d j
        (fun k : Nat => P.eval (k : Int)) % n)
      (nativeGK5BTObserved_overlapCompatible m n d j
        (fun k : Nat => P.eval (k : Int)))) ≡ 0 [MOD Nat.lcm m n]

/-- Genuine necessary/sufficient noncoprime local gluing. -/
theorem fivefoldGK5BTNorthOverlap_iff_exists_global
    (m n a b : Nat) :
    nativeGK5BTOverlapCompatible m n a b ↔
      ∃ x : Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n] :=
  nativeGK5BTOverlap_iff_exists_gluing m n a b

/-- Precise gcd-overlap obstruction, not a seam obstruction. -/
theorem fivefoldGK5BTNorthNoGlue_iff_obstruction
    (m n a b : Nat) :
    (¬ ∃ x : Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n]) ↔
      ¬ nativeGK5BTOverlapCompatible m n a b :=
  nativeGK5BTNoGluing_iff_overlapObstruction m n a b

/-- Every global solution is unique modulo lcm(m,n). -/
theorem fivefoldGK5BTNorthOverlap_gluing_iff_lcm
    (m n a b x : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b) :
    (x ≡ a [MOD m] ∧ x ≡ b [MOD n]) ↔
      x ≡ nativeGK5BTOverlapGlue m n a b h [MOD Nat.lcm m n] :=
  nativeGK5BTOverlap_compatible_iff_mod_lcm m n a b x h

/-- Normalized genuine glued residue is below lcm. -/
theorem fivefoldGK5BTNorthOverlap_normalized
    (m n a b : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b)
    (hm : m ≠ 0) (hn : n ≠ 0) :
    nativeGK5BTOverlapGlue m n a b h < Nat.lcm m n :=
  nativeGK5BTOverlapGlue_lt_lcm m n a b h hm hn

/-- Concrete failure: gcd(4,6)=2 distinguishes 1 from 2. -/
theorem fivefoldGK5BTNorthConcrete_overlapFails :
    ¬ ∃ x : Nat, x ≡ 1 [MOD 4] ∧ x ≡ 2 [MOD 6] := by
  apply nativeGK5BTNoGluing_of_gcdResidueMismatch 4 6 1 2
  norm_num [Nat.gcd]

/-- Concrete success: x=9 is the unique normalized
simultaneous representative for 1 mod 4 and 3 mod 6. -/
theorem fivefoldGK5BTNorthConcrete_overlapGlued :
    nativeGK5BTOverlapGlue 4 6 1 3 (by decide) = 9 := by
  symm
  apply nativeGK5BTOverlapGlue_eq_of_lt_lcm 4 6 1 3 9
    (by decide) (by decide) (by decide) (by decide) (by decide)

/-- Observed residue pair of the actual signed numerator's
natAbs always agrees on gcd, including negative samples. -/
theorem fivefoldGK5BTNorthRaw_overlapCompatible
    (m n d j : Nat) (values : Nat → Int) :
    nativeGK5BTOverlapCompatible m n
      (nativeGK5BTObservedNumeratorAbs d j values % m)
      (nativeGK5BTObservedNumeratorAbs d j values % n) :=
  nativeGK5BTObserved_overlapCompatible m n d j values

/-- The observed glue equals the original absolute integer
numerator modulo the actual lcm(m,n). -/
theorem fivefoldGK5BTNorthRaw_glueEqOriginal
    (m n d j : Nat) (values : Nat → Int) :
    nativeGK5BTObservedNumeratorAbs d j values ≡
      nativeGK5BTOverlapGlue m n
        (nativeGK5BTObservedNumeratorAbs d j values % m)
        (nativeGK5BTObservedNumeratorAbs d j values % n)
        (nativeGK5BTObserved_overlapCompatible m n d j values)
      [MOD Nat.lcm m n] :=
  nativeGK5BTObserved_glue_eq_original_mod_lcm m n d j values

/-- Exactly the original SIGNED integer divisibility test. -/
theorem fivefoldGK5BTNorthRaw_glueZero_iff_lcmDvd
    (m n d j : Nat) (values : Nat → Int) :
    (nativeGK5BTOverlapGlue m n
      (nativeGK5BTObservedNumeratorAbs d j values % m)
      (nativeGK5BTObservedNumeratorAbs d j values % n)
      (nativeGK5BTObserved_overlapCompatible m n d j values))
        ≡ 0 [MOD Nat.lcm m n] ↔
    ((Nat.lcm m n : Nat) : Int) ∣
      nativeGK5BQClearedNumerator d j values :=
  nativeGK5BTObserved_glue_zero_iff_lcmDvd m n d j values

/-- Original true integer polynomial P: if lcm(m,n)|d!,
then all genuine cleared-numerator overlap glues vanish.
No unsupported unconditional integrality claim for
arbitrary moduli or invented F55 source is made. -/
theorem fivefoldGK5BTIntegerSource_overlapZero
    (P : Polynomial Int) (d m n : Nat)
    (hdegree : P.natDegree ≤ d)
    (hlcm : Nat.lcm m n ∣ d.factorial) :
    fivefoldGK5BTNorthCRTZero P d m n := by
  intro j hj
  apply (nativeGK5BTObserved_glue_zero_iff_lcmDvd m n d j
    (fun k : Nat => P.eval (k : Int))).2
  exact (Int.natCast_dvd_natCast.mpr hlcm).trans
    (fivefoldGK5BQIntegerSource_divisibility P d hdegree j hj)

/-- Actual F55 Type source supplies its existing P92B
integer depth polynomial VALUE; numeric CRT does not
reconstruct Type-valued source history. -/
theorem fivefoldGK5BTNorthOriginalF55_overlapZero
    (f : NativeGK5AINorthPentagonCells) (d m n : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d)
    (hlcm : Nat.lcm m n ∣ d.factorial) :
    fivefoldGK5BTNorthCRTZero
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial d m n :=
  fivefoldGK5BTIntegerSource_overlapZero
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial
    d m n hdegree hlcm

/-- Actual F55/P77 class contributes solely its already
descended polynomial VALUE; no quotient-class identity. -/
theorem fivefoldGK5BTNorthP77_overlapZero
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BTNorthFirst fivefoldGK5BTNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d m n : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BTNorthFirst fivefoldGK5BTNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d)
    (hlcm : Nat.lcm m n ∣ d.factorial) :
    fivefoldGK5BTNorthCRTZero
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BTNorthFirst fivefoldGK5BTNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q)
      d m n :=
  fivefoldGK5BTIntegerSource_overlapZero
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BTNorthFirst fivefoldGK5BTNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d m n hdegree hlcm

/-- Genuine north primitive P=1, extended to the four
sites {0,1,2,3}, passes overlapping m=2,n=6 CRT. -/
theorem fivefoldGK5BTNorthPrimitive_fourSite_overlapZero :
    fivefoldGK5BTNorthCRTZero
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial 3 2 6 := by
  apply fivefoldGK5BTNorthOriginalF55_overlapZero
  · exact le_trans
      fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1 (by omega)
  · decide

/-- Distinct north double inverse+true F55 right unit
P=X² also passes the same four-site arithmetic test. -/
theorem fivefoldGK5BTNorthDoubleInverse_fourSite_overlapZero :
    fivefoldGK5BTNorthCRTZero
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial
      3 2 6 := by
  apply fivefoldGK5BTNorthOriginalF55_overlapZero
  · exact le_trans
      fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2 (by omega)
  · decide

/-- Two genuinely selected P92B north loops P=X³+2
and Q=2X²+X pass separate four-site overlap tests. -/
theorem fivefoldGK5BTNorthTripleLoops_fourSite_overlapZero :
    fivefoldGK5BTNorthCRTZero
      fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial 3 2 6 ∧
    fivefoldGK5BTNorthCRTZero
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial 3 2 6 := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  exact ⟨fivefoldGK5BTIntegerSource_overlapZero
           fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial
           3 2 6 ha (by decide),
         fivefoldGK5BTIntegerSource_overlapZero
           fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial
           3 2 6 hb (by decide)⟩

/-- Original structural obstruction is independent of
true numeric noncoprime CRT: BOTH genuine original F55
sources have zero arithmetic glues at m=2,n=6, but the
primitive original-phi seam exists and the double-inverse
original-phi seam provably does not. -/
theorem fivefoldGK5BTNorthBothOverlapZeroButOppositeSeams
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    fivefoldGK5BTNorthCRTZero
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial 3 2 6 ∧
    fivefoldGK5BTNorthCRTZero
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial
      3 2 6 ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hyes, hno, _, _⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨fivefoldGK5BTNorthPrimitive_fourSite_overlapZero,
    fivefoldGK5BTNorthDoubleInverse_fourSite_overlapZero, hyes, hno⟩

/-- Fifth-around north C60 gauge and conditional P89
BadPair reflection remain independently Type-validated. -/
theorem fivefoldGK5BTNorthPhysicalAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) :=
  fivefoldGK5BRNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BTNorthOverlap_iff_exists_global
#print axioms fivefoldGK5BTNorthNoGlue_iff_obstruction
#print axioms fivefoldGK5BTNorthOverlap_gluing_iff_lcm
#print axioms fivefoldGK5BTNorthOverlap_normalized
#print axioms fivefoldGK5BTNorthConcrete_overlapFails
#print axioms fivefoldGK5BTNorthConcrete_overlapGlued
#print axioms fivefoldGK5BTNorthRaw_overlapCompatible
#print axioms fivefoldGK5BTNorthRaw_glueEqOriginal
#print axioms fivefoldGK5BTNorthRaw_glueZero_iff_lcmDvd
#print axioms fivefoldGK5BTIntegerSource_overlapZero
#print axioms fivefoldGK5BTNorthOriginalF55_overlapZero
#print axioms fivefoldGK5BTNorthP77_overlapZero
#print axioms fivefoldGK5BTNorthPrimitive_fourSite_overlapZero
#print axioms fivefoldGK5BTNorthDoubleInverse_fourSite_overlapZero
#print axioms fivefoldGK5BTNorthTripleLoops_fourSite_overlapZero
#print axioms fivefoldGK5BTNorthBothOverlapZeroButOppositeSeams
#print axioms fivefoldGK5BTNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

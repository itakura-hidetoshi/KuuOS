import KUOS.Architecture.QiWuxingGK5BHNorthUnitPolynomialGateV4_27
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BIDepthCoefficientDescent
import Mathlib.Tactic

/-!
Qi v4.28 / F112-P94D3GK5BI — actual NORTH C60 source-Hom
application of the verified independent Kuu coefficient certificates.

For EVERY true north F54 long→short source F55 3-proof f,
the structural P92B translation's inversion-depth coefficients
are nonnegative and have finite support. The exact coefficient
values descend as Int, not merely Prop, on ACTUAL original P77
source four-cell quotient classes.

At the same true north F54 Hom:
* source primitive has a_0 = 1 and a positive local P94A seam;
* source double inverse plus genuine F55 right unit has a_0 = 0
  and no local seam;
* their actual original P77 classes differ by this depth-zero
  coefficient, independently of evaluating at scalar 1,-1,2.

For real chosen P92B north endomorphism loops, old N/S/W values
agree (3,1,10), yet a_0 differs: 2 versus 0. The independent
GK5BI coefficient obstruction therefore forbids a selected
P94A four-cell. These endo loops are NOT original-to-phi seams.

Physical fifth-Dart closure and the P89 BadPair/reflection
conditional iff remain independent. There is NO implication
W=1 -> seam, GK5AY universal seam, GK5BA kit, general P94A
normal form, Gray restoration or unconditional P89 reflection.

Strict 空, independent Kuu→Qi, same F54 two-Nat/two-category/
Blocks typed history and actual F55 Type witnesses. Append-only,
same public root107, protected #1558 Draft/open/unmerged.
Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms/sorry/admit/native_decide.
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

private def fivefoldGK5BINorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BINorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Every original north source's chosen phi has nonnegative
coefficients at ALL finite inversion depths k. -/
theorem fivefoldGK5BINorthSource_coeff_nonneg
    (f : NativeGK5AINorthPentagonCells) (k : Nat) :
    0 ≤ (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k :=
  (nativeGK5AIOriginalToP92Structural f).gk5biCoeff_nonneg k

/-- Each true north original source has finite inversion-depth
support, even when its original typed F55 history is arbitrary. -/
theorem fivefoldGK5BINorthSource_coeff_finite
    (f : NativeGK5AINorthPentagonCells) :
    ∃ S : Finset Nat, ∀ k : Nat, k ∉ S →
      (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k = 0 :=
  (nativeGK5AIOriginalToP92Structural f).gk5biFinite_support

/-- Every genuinely descended north P77 source coefficient
is nonnegative; no raw proof-term collapse is assumed. -/
theorem fivefoldGK5BINorthP77Class_coeff_nonneg
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (k : Nat) :
    0 ≤ nativeGK5BICoeffOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort k q :=
  nativeGK5BICoeffOnP77Class_nonneg
    fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q k

/-- The TRUE north P77 source-class coefficient support is
finite, not a conjectural finite cover of all F54 sources. -/
theorem fivefoldGK5BINorthP77Class_finite
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort) :
    ∃ S : Finset Nat, ∀ k : Nat, k ∉ S →
      nativeGK5BICoeffOnP77Class
        fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q = 0 :=
  nativeGK5BICoeffOnP77Class_finite_support
    fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q

/-- The primitive positive north source has exactly one
original wrapper at inversion depth ZERO. -/
theorem fivefoldGK5BINorthPrimitive_coeff_zero :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5biDepthCoefficient 0 = 1 := by
  change ((nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial).coeff 0 = 1
  rw [fivefoldGK5BGNorthPrimitive_full_poly]
  simp

/-- The genuine source double inverse WITH original F55 right
identity extension has NO depth-zero wrapper; all evidence
occurs at depth TWO, as certified by the source P77 witness. -/
theorem fivefoldGK5BINorthDoubleInverseUnit_coeff_zero :
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5biDepthCoefficient 0 = 0 := by
  change ((nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial).coeff 0 = 0
  rw [fivefoldGK5BGNorthDoubleInverseUnit_full_poly]
  simp

/-- The same genuine dependent north F54 Hom has positive and
negative P77 classes separated by the SINGLE depth-zero coefficient. -/
theorem fivefoldGK5BINorthP77_classes_coeff_zero :
    nativeGK5BICoeffOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0
      (nativeF55RawVerticalFourClass
        fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
        nativeGK5AGNorthOriginalCell) = 1 ∧
    nativeGK5BICoeffOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0
      (nativeF55RawVerticalFourClass
        fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) = 0 := by
  constructor
  · simpa only [nativeGK5BICoeffOnP77Class_mk] using
      fivefoldGK5BINorthPrimitive_coeff_zero
  · simpa only [nativeGK5BICoeffOnP77Class_mk] using
      fivefoldGK5BINorthDoubleInverseUnit_coeff_zero

/-- One coefficient already proves these ACTUAL source P77
classes distinct. We do not infer raw F55 proof inequality. -/
theorem fivefoldGK5BINorthP77_classes_ne :
    (nativeF55RawVerticalFourClass
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      nativeGK5AGNorthOriginalCell) ≠
    (nativeF55RawVerticalFourClass
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  intro h
  have heq := congrArg
    (nativeGK5BICoeffOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0) h
  rw [fivefoldGK5BINorthP77_classes_coeff_zero.1,
    fivefoldGK5BINorthP77_classes_coeff_zero.2] at heq
  norm_num at heq

/-- On genuine NORTH chosen P92B loops, the depth-ZERO counts
are exactly 2 and 0, even though N=3,S=1,W=10 for BOTH.
These are actual typed endo-three-proofs, not numerical shadows. -/
theorem fivefoldGK5BINorthTripleLoops_coeff_zero :
    fivefoldGK5BGNorthTripleLoopA.gk5biDepthCoefficient 0 = 2 ∧
    fivefoldGK5BGNorthTripleLoopB.gk5biDepthCoefficient 0 = 0 := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BGNorthTripleLoop_polynomials
  constructor
  · change fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.coeff 0 = 2
    rw [ha]
    norm_num [Polynomial.coeff_add, Polynomial.coeff_X_pow]
  · change fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.coeff 0 = 0
    rw [hb]
    norm_num [Polynomial.coeff_add, Polynomial.coeff_X_pow]

/-- The sole depth-zero coefficient separates two selected
proofs with identical N/S/W, giving a P94A obstruction by GK5BI. -/
theorem fivefoldGK5BINorthTripleLoops_no_P94_by_coeff_zero :
    ¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA fivefoldGK5BGNorthTripleLoopB) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BINorthTripleLoops_coeff_zero
  have hne :
      fivefoldGK5BGNorthTripleLoopA.gk5biDepthCoefficient 0 ≠
        fivefoldGK5BGNorthTripleLoopB.gk5biDepthCoefficient 0 := by
    rw [ha, hb]
    norm_num
  exact nativeGK5BINoP94_of_coeff_ne 0 hne

/-- Explicit north-C60 counterexample: all old scalar grades
are equal, yet a single coefficient differs, preventing P94A. -/
theorem fivefoldGK5BINorthTripleLoops_scalar_blind_spot :
    (fivefoldGK5BGNorthTripleLoopA.gk5bbOriginalCount =
      fivefoldGK5BGNorthTripleLoopB.gk5bbOriginalCount) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5beSignedCount =
      fivefoldGK5BGNorthTripleLoopB.gk5beSignedCount) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5bfInverseDepthWeight =
      fivefoldGK5BGNorthTripleLoopB.gk5bfInverseDepthWeight) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5biDepthCoefficient 0 ≠
      fivefoldGK5BGNorthTripleLoopB.gk5biDepthCoefficient 0) ∧
    ¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA fivefoldGK5BGNorthTripleLoopB) := by
  obtain ⟨hn, hs, hw⟩ := fivefoldGK5BGNorthTripleLoop_equal_old_grades
  obtain ⟨ha, hb⟩ := fivefoldGK5BINorthTripleLoops_coeff_zero
  have hne :
      fivefoldGK5BGNorthTripleLoopA.gk5biDepthCoefficient 0 ≠
        fivefoldGK5BGNorthTripleLoopB.gk5biDepthCoefficient 0 := by
    rw [ha, hb]
    norm_num
  exact ⟨hn, hs, hw, hne, fivefoldGK5BINorthTripleLoops_no_P94_by_coeff_zero⟩

/-- All descended coefficients jointly reconstruct the full
polynomial on actual north source P77 classes. -/
theorem fivefoldGK5BINorthP77_all_coeff_iff_poly
    (q₁ q₂ : NativeF55RawVerticalFourClasses
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort) :
    (∀ k : Nat,
      nativeGK5BICoeffOnP77Class
        fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₁ =
      nativeGK5BICoeffOnP77Class
        fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₂) ↔
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₁ =
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₂ :=
  nativeGK5BICoeffOnP77Class_all_iff_poly
    fivefoldGK5BINorthFirst fivefoldGK5BINorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q₁ q₂

/-- Source P77 classification, local seam boundary, physical
north fifth-Dart gauge, and conditional P89 reflection coexist
without identifying their proof authority layers. -/
theorem fivefoldGK5BINorthPhysicalBoundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    (¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5BGNorthSameFiber_local_split with ⟨hYes, hNo, _, _, _⟩
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, _, _⟩
  exact ⟨hYes, hNo, hClosed, hIff⟩

#print axioms fivefoldGK5BINorthSource_coeff_nonneg
#print axioms fivefoldGK5BINorthSource_coeff_finite
#print axioms fivefoldGK5BINorthP77Class_coeff_nonneg
#print axioms fivefoldGK5BINorthP77Class_finite
#print axioms fivefoldGK5BINorthPrimitive_coeff_zero
#print axioms fivefoldGK5BINorthDoubleInverseUnit_coeff_zero
#print axioms fivefoldGK5BINorthP77_classes_coeff_zero
#print axioms fivefoldGK5BINorthP77_classes_ne
#print axioms fivefoldGK5BINorthTripleLoops_coeff_zero
#print axioms fivefoldGK5BINorthTripleLoops_no_P94_by_coeff_zero
#print axioms fivefoldGK5BINorthTripleLoops_scalar_blind_spot
#print axioms fivefoldGK5BINorthP77_all_coeff_iff_poly
#print axioms fivefoldGK5BINorthPhysicalBoundary

end
end KUOS.Architecture.WuxingPentagonUnified

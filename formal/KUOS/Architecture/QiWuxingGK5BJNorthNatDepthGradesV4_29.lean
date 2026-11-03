import KUOS.Architecture.QiWuxingGK5BINorthCoefficientDescentV4_28
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BJNatDepthWeightedSums
import Mathlib.Tactic

/-!
Qi v4.29 / F112-P94D3GK5BJ — actual NORTH C60 Nat depth
coefficient certificates and finite N/S/W weighted grade formulas.

For every TRUE north-C60 F54 long→short original F55 source
f, the original-to-selected P92B structural presentation phi(f)
has genuine nonnegative Nat occurrence counts b_k, finite
support, a natDegree maximal-depth upper bound, and
N=sum b_k, S=sum (-1)^k*b_k, W=sum 2^k*b_k.

The NAT coefficients descend through the original P77 source
four-cell quotient; they reconstruct the true descended Int[X]
polynomial and vanish beyond its natDegree. We do NOT identify
raw original F55 Type-valued proof terms or introduce a numeric
shadow of P77.

At the same original F54 Hom, the north primitive has b_0=1,
while the original double inverse PLUS genuine F55 right unit
has b_0=0. These yield distinct actual source-P77 classes.
For genuine selected north P92B endomorphism loops A and B,
the original scalar grades N=3,S=1,W=10 coincide while the
single b_0 is 2 vs 0, obstructing P94A. These loops are NOT
original-to-phi seam counterexamples.

Fifth-around physical C60 gauge and P89 BadPair reflection
remain the old conditional statements. No implication W=1 to
local seam existence, no universal GK5AY seam, GK5BA kit,
all-P94A normalization, unconditional P89 reflection, Gray.
Strict 空 authority; independent Kuu→Qi; true F54 two-Nat /
two-category / Blocks indices and F55 Type history preserved.
Append-only root107, #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2 and mathlib
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

private def fivefoldGK5BJNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BJNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Every actual north-F54 original source has an exact Nat
unweighted finite occurrence count, recovering GK5BB N. -/
theorem fivefoldGK5BJNorthSource_N_finite_sum
    (f : NativeGK5AINorthPentagonCells) :
    (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount =
      ∑ k ∈ (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.support,
        (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k :=
  (nativeGK5AIOriginalToP92Structural f).gk5bjN_finite_sum

/-- Every actual north source's signed GK5BE grade is the
finite alternating sum of true Nat depth counts. -/
theorem fivefoldGK5BJNorthSource_S_finite_sum
    (f : NativeGK5AINorthPentagonCells) :
    (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount =
      ∑ k ∈ (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.support,
        ((nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k : Int) *
          (-1 : Int) ^ k :=
  (nativeGK5AIOriginalToP92Structural f).gk5bjS_finite_sum

/-- The physical source's GK5BF weight is a finite NATURAL
sum weighted by 2^k, not a signed cancellation. -/
theorem fivefoldGK5BJNorthSource_W_finite_sum
    (f : NativeGK5AINorthPentagonCells) :
    (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight =
      ∑ k ∈ (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.support,
        (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k * 2 ^ k :=
  (nativeGK5AIOriginalToP92Structural f).gk5bjW_finite_sum

/-- Explicit true inversion-depth upper bound for every
original north F54/F55 source, with no finite-generation axiom. -/
theorem fivefoldGK5BJNorthSource_natDepth_bound
    (f : NativeGK5AINorthPentagonCells) (k : Nat)
    (hk : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree < k) :
    (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k = 0 :=
  (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepth_bound k hk

/-- All TRUE north P77 classes have a Nat-valued quotient lift
compatible with the Int-valued coefficients constructed in GK5BI. -/
theorem fivefoldGK5BJNorthP77_natCoeff_cast
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (k : Nat) :
    (nativeGK5BJNatCoeffOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort k q : Int) =
      nativeGK5BICoeffOnP77Class
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q :=
  nativeGK5BJNatCoeffOnP77Class_cast
    fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q k

/-- Every source-P77 Nat coefficient vanishes above the
natDegree of the ACTUAL descended Polynomial Int. -/
theorem fivefoldGK5BJNorthP77_natDepth_bound
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (k : Nat)
    (hk : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree < k) :
    nativeGK5BJNatCoeffOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort k q = 0 :=
  nativeGK5BJNatCoeffOnP77Class_bound
    fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q k hk

/-- Genuine north source-P77 Nat coefficients recover the full
Int[X] polynomial by finite weighted sum for ANY integer x. -/
theorem fivefoldGK5BJNorthP77_nat_finite_eval
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (x : Int) :
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).eval x =
    ∑ k ∈ (nativeGK5BGPolyOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).support,
      (nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q : Int) * x ^ k :=
  nativeGK5BJNatCoeffOnP77Class_eval
    fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q x

/-- The total family of TRUE north P77 Nat coefficients is
equivalent to equality of the full descended polynomial. -/
theorem fivefoldGK5BJNorthP77_nat_all_iff_poly
    (q₁ q₂ : NativeF55RawVerticalFourClasses
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort) :
    (∀ k : Nat,
      nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₁ =
      nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₂) ↔
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₁ =
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₂ :=
  nativeGK5BJNatCoeffOnP77Class_all_iff_poly
    fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q₁ q₂

/-- Genuine north original primitive has exactly ONE Nat
wrapper occurrence at depth zero. -/
theorem fivefoldGK5BJNorthPrimitive_natCoeff_zero :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bjNatDepthCoefficient 0 = 1 := by
  have h := fivefoldGK5BINorthPrimitive_coeff_zero
  change ((nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5biDepthCoefficient 0).toNat = 1
  rw [h]
  rfl

/-- Genuine north original double inverse plus F55 right unit
has NO Nat wrapper at depth zero. -/
theorem fivefoldGK5BJNorthDoubleInverseUnit_natCoeff_zero :
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bjNatDepthCoefficient 0 = 0 := by
  have h := fivefoldGK5BINorthDoubleInverseUnit_coeff_zero
  change ((nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5biDepthCoefficient 0).toNat = 0
  rw [h]
  rfl

/-- On TRUE north F54 source-P77 classes, the depth-zero
NAT values are respectively 1 and 0. -/
theorem fivefoldGK5BJNorthP77Nat_classes_zero :
    nativeGK5BJNatCoeffOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0
      (nativeF55RawVerticalFourClass
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        nativeGK5AGNorthOriginalCell) = 1 ∧
    nativeGK5BJNatCoeffOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0
      (nativeF55RawVerticalFourClass
        fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) = 0 := by
  constructor
  · change (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bjNatDepthCoefficient 0 = 1
    exact fivefoldGK5BJNorthPrimitive_natCoeff_zero
  · change (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bjNatDepthCoefficient 0 = 0
    exact fivefoldGK5BJNorthDoubleInverseUnit_natCoeff_zero

/-- One genuinely Nat-valued quotient coefficient already
separates two TRUE source P77 classes within the same F54 Hom. -/
theorem fivefoldGK5BJNorthP77Nat_classes_ne :
    (nativeF55RawVerticalFourClass
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      nativeGK5AGNorthOriginalCell) ≠
    (nativeF55RawVerticalFourClass
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  intro h
  have hh := congrArg
    (nativeGK5BJNatCoeffOnP77Class
      fivefoldGK5BJNorthFirst fivefoldGK5BJNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort 0) h
  rw [fivefoldGK5BJNorthP77Nat_classes_zero.1,
    fivefoldGK5BJNorthP77Nat_classes_zero.2] at hh
  omega

/-- Two true selected north P92B endo loops have the same
three scalar grades but different Nat depth-zero coefficients. -/
theorem fivefoldGK5BJNorthTripleLoops_natCoeff_zero :
    fivefoldGK5BGNorthTripleLoopA.gk5bjNatDepthCoefficient 0 = 2 ∧
    fivefoldGK5BGNorthTripleLoopB.gk5bjNatDepthCoefficient 0 = 0 := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BINorthTripleLoops_coeff_zero
  constructor
  · change (fivefoldGK5BGNorthTripleLoopA.gk5biDepthCoefficient 0).toNat = 2
    rw [ha]
    rfl
  · change (fivefoldGK5BGNorthTripleLoopB.gk5biDepthCoefficient 0).toNat = 0
    rw [hb]
    rfl

/-- The single Nat depth-zero discrepancy is a P94A four-cell
obstruction on genuine selected P92B north endomorphisms. -/
theorem fivefoldGK5BJNorthTripleLoops_noP94_natCoeff :
    ¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA fivefoldGK5BGNorthTripleLoopB) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BJNorthTripleLoops_natCoeff_zero
  have hne :
      fivefoldGK5BGNorthTripleLoopA.gk5bjNatDepthCoefficient 0 ≠
        fivefoldGK5BGNorthTripleLoopB.gk5bjNatDepthCoefficient 0 := by
    rw [ha, hb]
    omega
  rintro ⟨w⟩
  exact hne (w.gk5bjNatCoeff_sound 0)

/-- A genuine north primitive positive seam and a double
inverse-unit negative seam coexist with the physical fifth-Dart
C60 gauge and ONLY conditional old P89 source reflection. -/
theorem fivefoldGK5BJNorthPhysicalAndProofBoundary
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
  fivefoldGK5BINorthPhysicalBoundary frame i

#print axioms fivefoldGK5BJNorthSource_N_finite_sum
#print axioms fivefoldGK5BJNorthSource_S_finite_sum
#print axioms fivefoldGK5BJNorthSource_W_finite_sum
#print axioms fivefoldGK5BJNorthSource_natDepth_bound
#print axioms fivefoldGK5BJNorthP77_natCoeff_cast
#print axioms fivefoldGK5BJNorthP77_natDepth_bound
#print axioms fivefoldGK5BJNorthP77_nat_finite_eval
#print axioms fivefoldGK5BJNorthP77_nat_all_iff_poly
#print axioms fivefoldGK5BJNorthPrimitive_natCoeff_zero
#print axioms fivefoldGK5BJNorthDoubleInverseUnit_natCoeff_zero
#print axioms fivefoldGK5BJNorthP77Nat_classes_zero
#print axioms fivefoldGK5BJNorthP77Nat_classes_ne
#print axioms fivefoldGK5BJNorthTripleLoops_natCoeff_zero
#print axioms fivefoldGK5BJNorthTripleLoops_noP94_natCoeff
#print axioms fivefoldGK5BJNorthPhysicalAndProofBoundary

end
end KUOS.Architecture.WuxingPentagonUnified

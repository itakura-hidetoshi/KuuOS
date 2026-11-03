import KUOS.Architecture.QiWuxingGK5BJNorthNatDepthGradesV4_29
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BKFiniteSampleRigidity
import Mathlib.Tactic

/-!
Qi v4.30 / F112-P94D3GK5BK — TRUE NORTH C60 finite-sample
rigidity for typed F54/F55/P92B/P77 original histories.

Import MERGED independent GK5BK (root-count proof) without
changing the direction of Kuu→Qi proof authority. A finite set
of d+1 distinct integer evaluations reconstructs the ENTIRE
depth polynomial and all Nat depth coefficients when both
genuine proofs' natDegree bounds are ≤d.

For original north F54 long→short source P77 classes, the same
finite-sample observation theorem holds on independently
descended Polynomial Int VALUES. It does not identify the
source classes or construct a P94A 4-cell.

The true north primitive P=1 and the original double inverse
with a TRUE original F55 right unit P=X² have degree≤2. Every
three distinct integer samples separate these two values.
The chosen NORTH P92B endomorphism loops A=X³+2 and
B=2X²+X have degree≤3; ANY four distinct integer samples
separate them. Their three old evaluations at (-1,1,2) agree
(N=3,S=1,W=10), while evaluation at zero differs (2 versus 0).
This explicitly illustrates why the fourth independent
observation is needed for the degree-three generic theorem.

Original F55 source Type-valued proof history and P77 classes
remain separate from chosen P92B four-cell comparisons. Physical
C60 fifth-Dart closure and P89 BadPair conditional reflection
are not inferred from numerical values.
No W=1→local seam, no global GK5AY seam or GK5BA kit, no P94A
normal form, Gray or unconditional P89 faithfulness.
Strict 空, independent Kuu→Qi, append-only public root107,
protected #1558 Draft/open/unmerged, Lean v4.30.0-rc2,
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

private def fivefoldGK5BKNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BKNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Any d+1 distinct integer observations recover ALL Nat
inverse-depth counts of two actual north original F55 proofs
whose structural P92B depth polynomials have degree≤d. -/
theorem fivefoldGK5BKNorthSource_finiteSamples_natCoeffs
    (f g : NativeGK5AINorthPentagonCells)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : (nativeGK5AIOriginalToP92Structural g).gk5bgDepthPolynomial.natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval z =
        (nativeGK5AIOriginalToP92Structural g).gk5bgDepthPolynomial.eval z) :
    ∀ k : Nat,
      (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k =
        (nativeGK5AIOriginalToP92Structural g).gk5bjNatDepthCoefficient k :=
  ((nativeGK5AIOriginalToP92Structural f).gk5bkFinite_eval_iff_natCoeffs
    (nativeGK5AIOriginalToP92Structural g) d samples hsize hf hg).1 heval

/-- For all TRUE north source-P77 4-cell quotient classes, the
finite data determines the entire DESCENDED polynomial value,
not equality of the underlying F55 quotient classes. -/
theorem fivefoldGK5BKNorthP77_finiteSamples_poly
    (q₁ q₂ : NativeF55RawVerticalFourClasses
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hq₁ : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₂).natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q₁).eval z =
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q₂).eval z) :
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₁ =
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₂ :=
  nativeGK5BKFinite_eval_P77_poly
    fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q₁ q₂ d samples hsize hq₁ hq₂ heval

/-- Equality at d+1 finite values is EQUIVALENT to equality
of all true Nat depth counts on the original north P77 classes. -/
theorem fivefoldGK5BKNorthP77_finiteSamples_iff_natCoeffs
    (q₁ q₂ : NativeF55RawVerticalFourClasses
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hq₁ : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q₂).natDegree ≤ d) :
    (∀ z ∈ samples,
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q₁).eval z =
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q₂).eval z) ↔
    (∀ k : Nat,
      nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₁ =
      nativeGK5BJNatCoeffOnP77Class
        fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort k q₂) :=
  nativeGK5BKFinite_eval_P77_iff_natCoeffs
    fivefoldGK5BKNorthFirst fivefoldGK5BKNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort
    q₁ q₂ d samples hsize hq₁ hq₂

/-- The two actual original north F54 source proofs have
depth polynomials of degree≤2: P_primitive=1, P_inverseUnit=X². -/
theorem fivefoldGK5BKNorthPrimitiveDouble_degree_le_two :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.natDegree ≤ 2 ∧
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.natDegree ≤ 2 := by
  constructor
  · rw [fivefoldGK5BGNorthPrimitive_full_poly]
    compute_degree!
  · rw [fivefoldGK5BGNorthDoubleInverseUnit_full_poly]
    compute_degree!

/-- The two TRUE original north source proofs are visibly
different at the INTEGER sampling point zero (1 versus 0). -/
theorem fivefoldGK5BKNorthPrimitiveDouble_eval_zero :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (0 : Int) = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (0 : Int) = 0 := by
  constructor
  · rw [fivefoldGK5BGNorthPrimitive_full_poly]
    simp
  · rw [fivefoldGK5BGNorthDoubleInverseUnit_full_poly]
    simp

/-- Even an adversarial choice of THREE distinct integer sites
detects this actual positive/negative north source difference
because their polynomial degrees are at most two. -/
theorem fivefoldGK5BKNorthPrimitiveDouble_any_three_sample_distinguish
    (samples : Finset Int) (hsize : samples.card = 3) :
    ∃ z ∈ samples,
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval z ≠
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval z := by
  obtain ⟨hdegA, hdegB⟩ := fivefoldGK5BKNorthPrimitiveDouble_degree_le_two
  have hne :
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bjNatDepthCoefficient 0 ≠
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bjNatDepthCoefficient 0 := by
    rw [fivefoldGK5BJNorthPrimitive_natCoeff_zero,
      fivefoldGK5BJNorthDoubleInverseUnit_natCoeff_zero]
    omega
  exact (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bkExists_sample_diff_of_natCoeff_ne
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit)
      2 samples (by simpa using hsize) hdegA hdegB 0 hne

/-- The two TRUE selected north endomorphism depth polynomials
have upper degree THREE. They are not original-to-phi seams. -/
theorem fivefoldGK5BKNorthTripleLoops_degree_le_three :
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.natDegree ≤ 3 ∧
    fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.natDegree ≤ 3 := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BGNorthTripleLoop_polynomials
  constructor
  · rw [ha]
    compute_degree!
  · rw [hb]
    compute_degree!

/-- A SINGLE Nat coefficient obstruction at depth zero forces
some disagreement at EVERY set of four distinct integer sites
for these two genuine degree-three north P92B endomorphisms. -/
theorem fivefoldGK5BKNorthTripleLoops_any_four_samples_distinguish
    (samples : Finset Int) (hsize : samples.card = 4) :
    ∃ z ∈ samples,
      fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z ≠
        fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z := by
  obtain ⟨hdegA, hdegB⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  obtain ⟨hca, hcb⟩ := fivefoldGK5BJNorthTripleLoops_natCoeff_zero
  have hne :
      fivefoldGK5BGNorthTripleLoopA.gk5bjNatDepthCoefficient 0 ≠
        fivefoldGK5BGNorthTripleLoopB.gk5bjNatDepthCoefficient 0 := by
    rw [hca, hcb]
    omega
  exact fivefoldGK5BGNorthTripleLoopA.gk5bkExists_sample_diff_of_natCoeff_ne
    fivefoldGK5BGNorthTripleLoopB 3 samples (by simpa using hsize)
    hdegA hdegB 0 hne

/-- The genuine selected north loop pair is BLIND at exactly
the old three scalar evaluations -1,1,2, but SPLITS at 0. -/
theorem fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing :
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (-1 : Int) =
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (-1 : Int) ∧
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (1 : Int) =
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (1 : Int) ∧
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (2 : Int) =
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (2 : Int) ∧
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (0 : Int) ≠
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (0 : Int) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BGNorthTripleLoop_polynomials
  constructor
  · rw [ha, hb]
    norm_num
  constructor
  · rw [ha, hb]
    norm_num
  constructor
  · rw [ha, hb]
    norm_num
  · rw [ha, hb]
    norm_num

/-- A concrete set of FOUR different integer observations:
the legacy -1,1,2 scalar probes plus the separating point 0. -/
private def fivefoldGK5BKFourIntegerSamples : Finset Int :=
  {(-1 : Int), 0, 1, 2}

theorem fivefoldGK5BKFourIntegerSamples_card :
    fivefoldGK5BKFourIntegerSamples.card = 4 := by
  decide

/-- The four-site certificate distinguishes the genuine north
loop pair even though its three old scalar probes agree. -/
theorem fivefoldGK5BKNorthTripleLoops_four_sample_certificate :
    ∃ z ∈ fivefoldGK5BKFourIntegerSamples,
      fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval z ≠
        fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval z := by
  refine ⟨(0 : Int), ?_, ?_⟩
  · simp [fivefoldGK5BKFourIntegerSamples]
  · exact fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing.2.2.2

/-- The proof-theoretic boundary is unchanged: original
positive seam, double-inverse-unit negative seam, physical north
fifth-Dart closure, and P89 reflection only conditional. -/
theorem fivefoldGK5BKNorthPhysicalAndP89Boundary
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
  fivefoldGK5BJNorthPhysicalAndProofBoundary frame i

#print axioms fivefoldGK5BKNorthSource_finiteSamples_natCoeffs
#print axioms fivefoldGK5BKNorthP77_finiteSamples_poly
#print axioms fivefoldGK5BKNorthP77_finiteSamples_iff_natCoeffs
#print axioms fivefoldGK5BKNorthPrimitiveDouble_degree_le_two
#print axioms fivefoldGK5BKNorthPrimitiveDouble_eval_zero
#print axioms fivefoldGK5BKNorthPrimitiveDouble_any_three_sample_distinguish
#print axioms fivefoldGK5BKNorthTripleLoops_degree_le_three
#print axioms fivefoldGK5BKNorthTripleLoops_any_four_samples_distinguish
#print axioms fivefoldGK5BKNorthTripleLoops_three_blind_one_distinguishing
#print axioms fivefoldGK5BKFourIntegerSamples_card
#print axioms fivefoldGK5BKNorthTripleLoops_four_sample_certificate
#print axioms fivefoldGK5BKNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified

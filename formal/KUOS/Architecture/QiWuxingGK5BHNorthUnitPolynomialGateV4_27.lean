import KUOS.Architecture.QiWuxingGK5BGNorthPolynomialSeamV4_26
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BHUnitPolynomialWeightOne
import Mathlib.Tactic

/-!
Qi v4.27 / F112-P94D3GK5BH — source-typed NORTH C60
application of GK5BH's ALL-P92B threshold rigidity:

  P_phi(f)(X)=1  iff  W(phi(f))=1,
  W(phi(f))=1  => N(phi(f))=S(phi(f))=1.

For the TRUE north C60 long→short F54 Hom, the genuine
P77 source quotient three-gate criterion is exactly the
constant-polynomial criterion, but neither is proven sufficient
to construct a P94A original-to-phi local seam.

The original north pentagon and its right-unit extension
have weight one and actual positive direct seams. The
original double inverse plus a genuine F55 right identity
has weight FOUR and NO seam; its negative P77 class remains
distinct at EXACTLY the same original F54 endpoints.

The genuine north P92B endomorphism-loop pair from Qi v4.26
has equal old scalar values N=3, S=1, W=10 but different
polynomials and no P94A comparison. Its values W=10 place
it OUTSIDE the unit-threshold local seam gate, so full
polynomial strictness for arbitrary comparisons does NOT
contradict the theorem P=1 iff W=1.

True physical fifth-around C60 gauge and the original P89
BadPair conditional reflection statement remain separate.
No general W=1 -> seam, no GK5AY global seam, GK5BA kit,
global P94A normalization, unconditional original P89
faithfulness/nonfaithfulness or Gray restoration.

Strict 空 authority, independent Kuu→Qi, genuine F54
two-Nat/two-category/Blocks and F55 proof histories retained.
Append-only, root107, protect #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit or native_decide.
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

private def fivefoldGK5BHNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BHNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- At EVERY TRUE original north-C60 F55 source with these
dependent long/short endpoint indices, the chosen full
polynomial is one exactly at inversion weight one. -/
theorem fivefoldGK5BHNorthPhi_poly_iff_weight
    (f : NativeGK5AINorthPentagonCells) :
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial = 1 ↔
    (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight = 1 :=
  (nativeGK5AIOriginalToP92Structural f).gk5bhPoly_one_iff_weight_one

/-- The SAME condition descends to an actual P77-source
four-cell quotient class, not just to a numerical shadow. -/
theorem fivefoldGK5BHNorthClass_threeGates_iff_poly
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort) :
    nativeGK5BFThreeGatesOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q ↔
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q = 1 :=
  nativeGK5BHThree_gates_class_iff_poly_one
    fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort q

/-- The true original north pentagon PLUS original right F55
identity carries weight one at its selected structural phi;
unsigned and signed grades one therefore follow automatically.
The independently constructed local P94A direct seam exists. -/
theorem fivefoldGK5BHNorthRightUnit_weight_one_and_seam :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AINorthPentagonWithIdentity).gk5bfInverseDepthWeight = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AINorthPentagonWithIdentity).gk5beSignedCount = 1 ∧
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) := by
  have hw :
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity).gk5bfInverseDepthWeight = 1 := rfl
  obtain ⟨hn, hs⟩ :=
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AINorthPentagonWithIdentity).gk5bhWeight_one_implies_N_S hw
  exact ⟨hw, hn, hs, ⟨nativeGK5BCNorthRightIdentityDirectSeam⟩⟩

/-- The genuine north primitive's class passes all three
numerical local gates and really has a seam; the genuine
double-inversion-right-unit class does NOT pass the W gate
and is locally negative, at the SAME F54 source/target. -/
theorem fivefoldGK5BHNorthPositiveNegative_class_boundary :
    nativeGK5BFThreeGatesOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    ¬ nativeGK5BFThreeGatesOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) ∧
    ¬ nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) :=
  ⟨fivefoldGK5BFNorthThreeGate_separates_classes.1,
   ⟨.refl _⟩,
   fivefoldGK5BFNorthThreeGate_separates_classes.2,
   fivefoldGK5BFNorthDoubleInverseUnit_no_seam⟩

/-- Both genuine selected north-C60 P92B loops share the
OLD scalar observations but each has W=10, not the
unit threshold W=1 used in the local original-to-phi gate. -/
theorem fivefoldGK5BHNorthTripleLoops_outside_unit_gate :
    fivefoldGK5BGNorthTripleLoopA.gk5bfInverseDepthWeight = 10 ∧
    fivefoldGK5BGNorthTripleLoopB.gk5bfInverseDepthWeight = 10 ∧
    (¬ fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial = 1) ∧
    (¬ fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial = 1) := by
  have ha : fivefoldGK5BGNorthTripleLoopA.gk5bfInverseDepthWeight = 10 := rfl
  have hb : fivefoldGK5BGNorthTripleLoopB.gk5bfInverseDepthWeight = 10 := rfl
  refine ⟨ha, hb, ?_, ?_⟩
  · intro hp
    have hw := (fivefoldGK5BGNorthTripleLoopA.gk5bhPoly_one_iff_weight_one).1 hp
    rw [ha] at hw
    omega
  · intro hp
    have hw := (fivefoldGK5BGNorthTripleLoopB.gk5bhPoly_one_iff_weight_one).1 hp
    rw [hb] at hw
    omega

/-- The genuine north selected loop pair remains a concrete
counterexample to completeness of scalar-equality observations
for arbitrary P94A comparison even though W=1 exactly
detects polynomial=1. These are NOT local F55 original-to-phi
seams and we do not create one. -/
theorem fivefoldGK5BHNorthTripleLoop_scalar_blindness :
    (fivefoldGK5BGNorthTripleLoopA.gk5bbOriginalCount =
      fivefoldGK5BGNorthTripleLoopB.gk5bbOriginalCount) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5beSignedCount =
      fivefoldGK5BGNorthTripleLoopB.gk5beSignedCount) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5bfInverseDepthWeight =
      fivefoldGK5BGNorthTripleLoopB.gk5bfInverseDepthWeight) ∧
    (fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial ≠
      fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial) ∧
    ¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA fivefoldGK5BGNorthTripleLoopB) := by
  obtain ⟨hn, hs, hw⟩ := fivefoldGK5BGNorthTripleLoop_equal_old_grades
  exact ⟨hn, hs, hw,
    nativeGK5BGTriple_poly_ne northNativeF45PentagonShort,
    fivefoldGK5BGNorthTripleLoop_no_P94⟩

/-- Source P77 classification and physical fifth-around
north gauge coexist. The old original P89 BadPair reflection
remains conditional, never inferred from Polynomial Int. -/
theorem fivefoldGK5BHNorthPhysicalBoundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BHNorthFirst fivefoldGK5BHNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, _, _⟩
  exact ⟨⟨.refl _⟩, hClosed, hIff⟩

#print axioms fivefoldGK5BHNorthPhi_poly_iff_weight
#print axioms fivefoldGK5BHNorthClass_threeGates_iff_poly
#print axioms fivefoldGK5BHNorthRightUnit_weight_one_and_seam
#print axioms fivefoldGK5BHNorthPositiveNegative_class_boundary
#print axioms fivefoldGK5BHNorthTripleLoops_outside_unit_gate
#print axioms fivefoldGK5BHNorthTripleLoop_scalar_blindness
#print axioms fivefoldGK5BHNorthPhysicalBoundary

end
end KUOS.Architecture.WuxingPentagonUnified

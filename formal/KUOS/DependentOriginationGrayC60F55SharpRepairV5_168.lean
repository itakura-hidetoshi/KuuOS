import KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167

namespace KUOS.DependentOriginationGrayC60F55SharpRepairV5_168

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 5000000
noncomputable section

/-!
# F59-F20 / v5.168 — sharpen the true F55 target repair from 31 to 27 edges

F59-F19 constructed the canonical flat repair of original ninety
F55 square generators with a provable 31-edge upper bound. Here we
DO NOT postulate a new geometry or an optimization heuristic.

Instead evaluate the exact original F59-F16 59-edge root paths as
an integer signed path-degree function. Evaluate the canonical Gray
repair on each of the original ninety one-edge generators; since the
F55 square generator has second integer charge exactly one, its
nonzero support is kernel-decidable by pure integral arithmetic.

The exact changed set is:
  • all 12 slot-s4 pentagon around edges;
  • 5 upper-ring cross edges;
  • 5 lower-ring cross edges;
  • 5 shifted cross edges.
Exactly TWENTY-SEVEN original incidence edges are changed.
ALL 59 primal-tree edges and ALL FIVE south spokes are untouched.

This sharpens the EXPLICIT constructed correction to exactly 27
without claiming global support-minimality among all conceivable
spanning trees and repairs. The companion theorem unit examines
whether this target-level repair lifts to ORIGINAL F55 source words.
-/

/-- Signed number of original F55 generator steps along the
F59-F16 actual 59-tree root path to a given genuine C60 dart. -/
def c60F20OriginalTreePathDegree (d : IcosahedralDart) : ℤ :=
  ((c60F16PrimalPathList d).map Prod.snd).sum

/-- Exact integer correction coefficient on every original C60
physical edge, using the ORIGINAL source/target dart ordering. -/
def c60F20OriginalTreeCorrectionDegree
    (e : TruncatedIcosahedralEdge) : ℤ :=
  c60F20OriginalTreePathDegree (truncatedIcosahedralEdgeEndpoints e).2 -
    c60F20OriginalTreePathDegree (truncatedIcosahedralEdgeEndpoints e).1 - 1

/-- A genuine edge list sent through the UNIFORM original F55
braided target is just its total signed integer weight times the
original F55 square 3-cell. -/
theorem c60F20UniformSignedEdgeList
    (l : List (TruncatedIcosahedralEdge × ℤ)) :
    c60F19OriginalF55EdgeCochain
      ((l.map (fun p =>
        (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum) =
      (l.map Prod.snd).sum • originalF55BraidedSquareGenerator := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, map_add]
      rw [ih]
      have hp :
          c60F19OriginalF55EdgeCochain
            (Finsupp.single p.1 p.2) =
              p.2 • originalF55BraidedSquareGenerator := by
        simp [c60F19OriginalF55EdgeCochain,
          c60F18GrayEdgeCochain, c60F19UniformF55EdgeLabels]
      rw [hp, add_smul]

/-- Evaluation of the ACTUAL original F55 edge field on the
F59-F16 primal path is exactly its signed path-degree multiple. -/
theorem c60F20OriginalF55PathValue
    (d : IcosahedralDart) :
    c60F19OriginalF55EdgeCochain (c60F16PrimalPath d) =
      c60F20OriginalTreePathDegree d •
        originalF55BraidedSquareGenerator :=
  c60F20UniformSignedEdgeList (c60F16PrimalPathList d)

/-- Every ORIGINAL genuine single edge generator evaluates to
exactly the F55 braided generator (no independent edge datum). -/
theorem c60F20OriginalF55SingleEdge
    (e : TruncatedIcosahedralEdge) :
    c60F19OriginalF55EdgeCochain
      (Finsupp.single e (1 : ℤ)) =
        originalF55BraidedSquareGenerator := by
  simp [c60F19OriginalF55EdgeCochain,
    c60F18GrayEdgeCochain, c60F19UniformF55EdgeLabels]

/-- EXPLICIT algebraic formula for the F59-F19 repaired edge values
in terms of original F59-F16 integer root paths. -/
theorem c60F20CanonicalCorrection_edgeFormula
    (e : TruncatedIcosahedralEdge) :
    c60F19CanonicalTreeCorrection
      (Finsupp.single e (1 : ℤ)) =
      c60F20OriginalTreeCorrectionDegree e •
        originalF55BraidedSquareGenerator := by
  change c60F19OriginalF55EdgeCochain
      (c60F16PrimalPathLift
        (c60IntegralBoundaryOne
          (Finsupp.single e (1 : ℤ)))) -
      c60F19OriginalF55EdgeCochain
        (Finsupp.single e (1 : ℤ)) = _
  rw [c60IntegralBoundaryOne_singleEdge]
  simp only [one_smul, c60IntegralEdgeBoundaryChain]
  rw [map_sub, c60F16PrimalPathLift_single,
    c60F16PrimalPathLift_single]
  simp only [one_smul]
  rw [map_sub, c60F20OriginalF55PathValue,
    c60F20OriginalF55PathValue, c60F20OriginalF55SingleEdge]
  simp only [c60F20OriginalTreeCorrectionDegree,
    sub_smul, one_smul]

/-- The original native F55 braided square has infinite
additive order because its second INTEGER generator charge is one,
although its independent exchange phase is only mod two. -/
theorem c60F20OriginalGeneratorNonzeroScalar_iff (n : ℤ) :
    n • originalF55BraidedSquareGenerator ≠ 0 ↔ n ≠ 0 := by
  constructor
  · intro h hn
    subst n
    exact h (zero_smul ℤ originalF55BraidedSquareGenerator)
  · intro hn hzero
    have hc := congrArg
      (fun g : GradedThreeCell 0 0 => g.charge.2) hzero
    change (n • originalF55BraidedSquareGenerator).charge.2 =
      (0 : GradedThreeCell 0 0).charge.2 at hc
    rw [c60F19OriginalF55Scalar_secondCharge] at hc
    have hh : n = 0 := by
      simpa using hc
    exact hn hh

/-- The exact changed-edge set, based on real original C60 edge
families: 12 terminal pentagonal around edges + three 5-edge
icosahedral cross families. No synthetic combinatorial edges. -/
def c60F20IsChangedEdge : TruncatedIcosahedralEdge → Bool
  | .around a => decide (a.slot = .s4)
  | .cross (.upperRing _) => true
  | .cross (.lowerRing _) => true
  | .cross (.crossShifted _) => true
  | _ => false

/-- All ninety real physical edge correction coefficients are
nonzero EXACTLY in the four stated edge families. Kernel-checked
finite arithmetic on F59-F16 original paths, not native_decide. -/
theorem c60F20CorrectionDegree_support_certificate :
    ∀ e : TruncatedIcosahedralEdge,
      c60F20OriginalTreeCorrectionDegree e ≠ 0 ↔
        c60F20IsChangedEdge e = true := by
  decide

/-- Real combinatorial cardinality of precisely the changed
families (12 pentagon-closing edges + 5+5+5 cross edges). -/
theorem c60F20ChangedPhysicalEdge_card :
    (Finset.univ.filter (fun e =>
      c60F20IsChangedEdge e = true)).card = 27 := by
  decide

/-- The actual Gray coefficientwise support of F59-F19's
CANONICAL corrected edge cochain coincides with the kernel
certified 27-member physical edge set. -/
theorem c60F20CorrectionSupport_exact :
    c60F19CanonicalTreeCorrectionSupport =
      Finset.univ.filter (fun e =>
        c60F20IsChangedEdge e = true) := by
  classical
  apply Finset.ext
  intro e
  simp only [c60F19CanonicalTreeCorrectionSupport,
    Finset.mem_filter, Finset.mem_univ, true_and]
  rw [c60F20CanonicalCorrection_edgeFormula,
    c60F20OriginalGeneratorNonzeroScalar_iff]
  exact c60F20CorrectionDegree_support_certificate e

/-- EXACT sharp support of the EXPLICIT canonical flat repair:
27 original C60 physical F55 square edges, not merely <=31. -/
theorem c60F20CanonicalCorrectionSupport_card_eq27 :
    c60F19CanonicalTreeCorrectionSupport.card = 27 := by
  rw [c60F20CorrectionSupport_exact]
  exact c60F20ChangedPhysicalEdge_card

/-- The actual F55 canonical repair leaves every one of the FIVE
south-spoke edges unchanged, not just the single south tree link. -/
theorem c60F20AllSouthSpokeSquares_preserved :
    ∀ i : IcosahedralRingIndex,
      c60F19CanonicalTreeCorrection
        (Finsupp.single
          (.cross (.southSpoke i)) (1 : ℤ)) = 0 := by
  have hz :
      ∀ i : IcosahedralRingIndex,
        c60F20OriginalTreeCorrectionDegree
          (.cross (.southSpoke i)) = 0 := by decide
  intro i
  rw [c60F20CanonicalCorrection_edgeFormula, hz i, zero_smul]

#print axioms c60F20UniformSignedEdgeList
#print axioms c60F20OriginalF55PathValue
#print axioms c60F20OriginalF55SingleEdge
#print axioms c60F20CanonicalCorrection_edgeFormula
#print axioms c60F20OriginalGeneratorNonzeroScalar_iff
#print axioms c60F20CorrectionDegree_support_certificate
#print axioms c60F20ChangedPhysicalEdge_card
#print axioms c60F20CorrectionSupport_exact
#print axioms c60F20CanonicalCorrectionSupport_card_eq27
#print axioms c60F20AllSouthSpokeSquares_preserved

end
end KUOS.DependentOriginationGrayC60F55SharpRepairV5_168

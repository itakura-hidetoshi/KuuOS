import KUOS.DependentOriginationGrayC60BraidedProjectionDescentV5_180

namespace KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60NonneutralDefectDoubleCountV5_178
open KUOS.DependentOriginationGrayC60BraidedProjectionDescentV5_180
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F33 / v5.181 — complete genuine C60 braided flat-repair classification

Unlike F59-F32's non-braided parity projection, the correction here
takes place entirely in the original INDEPENDENT neutral Gray 3-cell
group, retaining the independent exchange-phase coordinate.

For the actual 90-edge physical field B_ab constructed in F59-F32
and ANY integer-linear edge cochain K, all 32 signed 5/6-gon face
curvatures vanish iff K = d Phi - B_ab for an actual C60 vertex
potential Phi.  The previously proved real 59-edge spanning tree
constructs a canonical Phi and a correction supported in at most
31 of the original edges, with no artificially added cells.

Changing B_ab merely by a vertex gauge cannot kill the actual
odd/odd north-pentagon curvature.  The constructive *edge*
correction does kill all 32 face curvatures, without parity projection.

Caution: preserving all independent target phases does NOT imply
that the flat corrected field lifts to an original typed F55
PresentedCell.  In fact, the tree-preserving odd/odd correction
retains a source-incompatible phase on an actual tree edge.
A full source Gray 3-functor, Stage-II omega, and historical/medical
interpretations are not identified by this construction.
-/

/-- The original independent native Gray 3-cell field, linearized
on the original ninety C60 edges; no parity projection occurs. -/
def c60F33BraidedEdgeCochain (a b : ZMod 2) :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F18GrayEdgeCochain (c60F32BraidedRepairedEdge a b)

/-- COMPLETE classification of ALL additional actual-C60 edge
corrections.  This is the real H¹ contracting-homotopy equivalence,
not a postulated flatness condition or a quotient of raw F55 cells. -/
theorem c60F33CompleteFlatCorrectionClassification
    (a b : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (c60F33BraidedEdgeCochain a b + k).comp
        c60IntegralBoundaryTwo = 0 ↔
      ∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        k = phi.comp c60IntegralBoundaryOne -
          c60F33BraidedEdgeCochain a b := by
  constructor
  · intro hflat
    obtain ⟨phi, hphi⟩ :=
      (c60F18ClosedEdgeIffVertexPotential
        (c60F33BraidedEdgeCochain a b + k)).mp hflat
    refine ⟨phi, ?_⟩
    calc
      k = (c60F33BraidedEdgeCochain a b + k) -
          c60F33BraidedEdgeCochain a b := by abel
      _ = phi.comp c60IntegralBoundaryOne -
          c60F33BraidedEdgeCochain a b := by rw [hphi]
  · rintro ⟨phi, rfl⟩
    have h :
        c60F33BraidedEdgeCochain a b +
          (phi.comp c60IntegralBoundaryOne -
            c60F33BraidedEdgeCochain a b) =
          phi.comp c60IntegralBoundaryOne := by abel
    rw [h]
    exact c60F18Coboundary_squared_zero phi

/-- Every original Z-linear C60 edge cochain is reconstructed from
its values on the actual ninety single-edge chain generators. -/
theorem c60F33ReconstructActualEdgeCochain
    (label : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F18GrayEdgeCochain
      (fun e => label (Finsupp.single e (1 : ℤ))) = label := by
  apply Finsupp.lhom_ext
  intro e z
  have hs :
      (Finsupp.single e z : C60IntegralOneChains) =
        z • (Finsupp.single e (1 : ℤ)) := by simp
  rw [hs, map_smul, map_smul]
  simp [c60F18GrayEdgeCochain]

/-- Evaluate any additional cochain on every real physical edge. -/
def c60F33CorrectedEdgeGrade (a b : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0)
    (e : TruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  (c60F33BraidedEdgeCochain a b + k) (Finsupp.single e (1 : ℤ))

theorem c60F33CorrectedGrade_realizes_cochain
    (a b : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F18GrayEdgeCochain (c60F33CorrectedEdgeGrade a b k) =
      c60F33BraidedEdgeCochain a b + k :=
  c60F33ReconstructActualEdgeCochain _

/-- FACEWISE version: all original twelve pentagons and twenty
hexagons are flat exactly for the classified affine corrections. -/
theorem c60F33All32Flat_iff_completeCorrection
    (a b : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (∀ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace (c60F33CorrectedEdgeGrade a b k) face = 0) ↔
      ∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        k = phi.comp c60IntegralBoundaryOne -
          c60F33BraidedEdgeCochain a b := by
  constructor
  · intro hfaces
    obtain ⟨phi, hphi⟩ :=
      (c60WangBiGlobalFlatIffVertexDescent
        (c60F33CorrectedEdgeGrade a b k)).mp hfaces
    rw [c60F33CorrectedGrade_realizes_cochain] at hphi
    apply (c60F33CompleteFlatCorrectionClassification a b k).mp
    exact (c60F18ClosedEdgeIffVertexPotential _).mpr ⟨phi, hphi⟩
  · intro h
    have hflat :=
      (c60F33CompleteFlatCorrectionClassification a b k).mpr h
    obtain ⟨phi, hphi⟩ :=
      (c60F18ClosedEdgeIffVertexPotential _).mp hflat
    apply (c60WangBiGlobalFlatIffVertexDescent _).mpr
    rw [c60F33CorrectedGrade_realizes_cochain]
    exact ⟨phi, hphi⟩

/-- Vertex coboundaries have ZERO curvature on every original C60
oriented face.  In particular adding a vertex gauge to a curved
field cannot change any face holonomy. -/
theorem c60F33VertexGauge_preserves_allFaceCurvature
    (a b : ZMod 2)
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (c60F33BraidedEdgeCochain a b +
      phi.comp c60IntegralBoundaryOne).comp c60IntegralBoundaryTwo =
    (c60F33BraidedEdgeCochain a b).comp c60IntegralBoundaryTwo := by
  apply LinearMap.ext
  intro chain
  simp only [LinearMap.comp_apply, LinearMap.add_apply,
    c60IntegralBoundaryOne_boundaryTwo_apply_zero, map_zero, add_zero]

/-- The true north-pentagon odd/odd curvature remains nonzero even
after an ARBITRARY vertex gauge change, directly on its original
signed geometric five-edge boundary chain. -/
theorem c60F33OddOddNorthPentagon_noGaugeCancellation
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (c60F33BraidedEdgeCochain 1 1 +
      phi.comp c60IntegralBoundaryOne)
        (c60IntegerFaceBoundaryChain (.aroundVertex .north)) ≠ 0 := by
  have hcurved :
      c60F33BraidedEdgeCochain 1 1
        (c60IntegerFaceBoundaryChain (.aroundVertex .north)) ≠ 0 := by
    change c60F18GrayEdgeCochain
      (c60F32BraidedRepairedEdge 1 1)
        (c60IntegerFaceBoundaryChain (.aroundVertex .north)) ≠ 0
    rw [← c60F18SignedGrayFacePasting_eq]
    exact c60F32OddOddNorthPentagon_nonflat
  simpa only [LinearMap.add_apply, LinearMap.comp_apply,
    c60IntegralBoundaryOne_eachOrientedFace_zero, map_zero,
    add_zero] using hcurved

theorem c60F33OddOddVertexGauge_neverFlat
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (c60F33BraidedEdgeCochain 1 1 +
      phi.comp c60IntegralBoundaryOne).comp c60IntegralBoundaryTwo ≠ 0 := by
  intro hflat
  have hbefore :
      (c60F33BraidedEdgeCochain 1 1).comp c60IntegralBoundaryTwo = 0 := by
    rw [← c60F33VertexGauge_preserves_allFaceCurvature 1 1 phi]
    exact hflat
  obtain ⟨vertexGauge, hEq⟩ :=
    (c60F18ClosedEdgeIffVertexPotential _).mp hbefore
  exact c60F32OddOddBraided_no_vertexDescent ⟨vertexGauge, hEq⟩

/-- Canonical retained-phase vertex potential, using the ALREADY
CERTIFIED primal 59-edge C60 tree, not any artificial C60 topology. -/
def c60F33TreePotential (a b : ZMod 2) :
    C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  (c60F33BraidedEdgeCochain a b).comp c60F16PrimalPathLift

/-- The canonical independent-braiding correction lives in the
original neutral Gray 3-cell group; NO projection or phase quotient. -/
def c60F33TreeCorrection (a b : ZMod 2) :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  (c60F33TreePotential a b).comp c60IntegralBoundaryOne -
    c60F33BraidedEdgeCochain a b

theorem c60F33TreeCorrected_eq_exactPotential (a b : ZMod 2) :
    c60F33BraidedEdgeCochain a b + c60F33TreeCorrection a b =
      (c60F33TreePotential a b).comp c60IntegralBoundaryOne := by
  unfold c60F33TreeCorrection
  abel

theorem c60F33TreeCorrection_all32_flat (a b : ZMod 2) :
    (c60F33BraidedEdgeCochain a b +
      c60F33TreeCorrection a b).comp c60IntegralBoundaryTwo = 0 := by
  rw [c60F33TreeCorrected_eq_exactPotential]
  exact c60F18Coboundary_squared_zero (c60F33TreePotential a b)

/-- Primal-tree preservation for the NEW independent-braiding
cochain, not an unproved transfer of the old EXACTLY-27 F55 count. -/
theorem c60F33TreeCorrection_zero_on_tree
    (a b : ZMod 2) (e : TruncatedIcosahedralEdge)
    (he : c60F19IsPrimalTreeEdge e = true) :
    c60F33TreeCorrection a b
      (Finsupp.single e (1 : ℤ)) = 0 := by
  have hface : c60F16FaceFill e = 0 := by
    simp [c60F16FaceFill, c60F19TreeEdge_noDualFill e he]
  have hpath := c60F16BasisContractingIdentity e
  rw [hface, map_zero, zero_add] at hpath
  have hboundary :
      c60IntegralBoundaryOne (Finsupp.single e (1 : ℤ)) =
        c60IntegralEdgeBoundaryChain e := by
    rw [c60IntegralBoundaryOne_singleEdge]
    simp
  change
    c60F33BraidedEdgeCochain a b
      (c60F16PrimalPathLift
        (c60IntegralBoundaryOne (Finsupp.single e (1 : ℤ)))) -
      c60F33BraidedEdgeCochain a b
        (Finsupp.single e (1 : ℤ)) = 0
  rw [hboundary, hpath, sub_self]

/-- The real physical support of the NEW tree correction. -/
noncomputable def c60F33TreeCorrectionSupport (a b : ZMod 2) :
    Finset TruncatedIcosahedralEdge := by
  classical
  exact Finset.univ.filter (fun e =>
    c60F33TreeCorrection a b (Finsupp.single e (1 : ℤ)) ≠ 0)

/-- Sharp universal 59-tree complement bound: no more than
THIRTY-ONE of the ninety genuine physical edges can be modified.
No claim of exactly 27 for independent braiding is made. -/
theorem c60F33TreeCorrectionSupport_card_le31 (a b : ZMod 2) :
    (c60F33TreeCorrectionSupport a b).card ≤ 31 := by
  classical
  have hs :
      c60F33TreeCorrectionSupport a b ⊆
        Finset.univ.filter (fun e => c60F19IsPrimalTreeEdge e = false) := by
    intro e he
    simp only [c60F33TreeCorrectionSupport,
      Finset.mem_filter, Finset.mem_univ, true_and] at he
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    cases h : c60F19IsPrimalTreeEdge e with
    | false => rfl
    | true =>
        exact (he (c60F33TreeCorrection_zero_on_tree a b e h)).elim
  calc
    (c60F33TreeCorrectionSupport a b).card ≤
      (Finset.univ.filter
        (fun e => c60F19IsPrimalTreeEdge e = false)).card :=
          Finset.card_le_card hs
    _ = 31 := c60F19PrimalTreeComplement_card

/-- A genuinely phase-retaining, flat, completely edge-indexed
original C60 field; all ninety edge values remain full Gray cells. -/
def c60F33TreeRepairedEdgeGrade (a b : ZMod 2)
    (e : TruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  c60F33CorrectedEdgeGrade a b (c60F33TreeCorrection a b) e

theorem c60F33TreeRepairedGrade_realizes_cochain (a b : ZMod 2) :
    c60F18GrayEdgeCochain (c60F33TreeRepairedEdgeGrade a b) =
      (c60F33TreePotential a b).comp c60IntegralBoundaryOne := by
  calc
    c60F18GrayEdgeCochain (c60F33TreeRepairedEdgeGrade a b) =
        c60F33BraidedEdgeCochain a b + c60F33TreeCorrection a b :=
      c60F33CorrectedGrade_realizes_cochain a b _
    _ = (c60F33TreePotential a b).comp c60IntegralBoundaryOne :=
      c60F33TreeCorrected_eq_exactPotential a b

/-- NON-PROJECTED genuine full Gray 3-cell face descent, one
identity on each of the twelve pentagons and twenty hexagons. -/
theorem c60F33TreeRepairedGrade_all32_flat
    (a b : ZMod 2) (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace (c60F33TreeRepairedEdgeGrade a b) face = 0 := by
  have h := (c60WangBiGlobalFlatIffVertexDescent
    (c60F33TreeRepairedEdgeGrade a b)).mpr
    ⟨c60F33TreePotential a b,
      c60F33TreeRepairedGrade_realizes_cochain a b⟩
  exact h face

/-- The independent phase is NOT discarded on the spanning tree:
the original field is preserved exactly on all 59 tree edges. -/
theorem c60F33TreeRepairedGrade_on_tree
    (a b : ZMod 2) (e : TruncatedIcosahedralEdge)
    (he : c60F19IsPrimalTreeEdge e = true) :
    c60F33TreeRepairedEdgeGrade a b e =
      c60F32BraidedRepairedEdge a b e := by
  change (c60F33BraidedEdgeCochain a b +
      c60F33TreeCorrection a b) (Finsupp.single e (1 : ℤ)) =
    c60F32BraidedRepairedEdge a b e
  rw [LinearMap.add_apply,
    c60F33TreeCorrection_zero_on_tree a b e he, add_zero]
  simp [c60F33BraidedEdgeCochain, c60F18GrayEdgeCochain]

/-- Tree-preserving FLATNESS does not, on odd/odd braiding, imply
membership in the original F55 source-image compatible subgroup. -/
theorem c60F33OddOddTreeRepaired_not_sourcePhaseLocked
    (e : TruncatedIcosahedralEdge)
    (he : c60F19IsPrimalTreeEdge e = true) :
    c60F33TreeRepairedEdgeGrade 1 1 e ∉ c60F55PhaseLocked := by
  have hdefect :
      c60F29PhaseDefect (c60F33TreeRepairedEdgeGrade 1 1 e) = 1 := by
    rw [c60F33TreeRepairedGrade_on_tree 1 1 e he,
      c60F32BraidedRepaired_defect]
    simp
  intro hmem
  change (c60F33TreeRepairedEdgeGrade 1 1 e).phase =
    ((c60F33TreeRepairedEdgeGrade 1 1 e).charge.2 : ZMod 2) at hmem
  have hzero :
      c60F29PhaseDefect (c60F33TreeRepairedEdgeGrade 1 1 e) = 0 := by
    simp [c60F29PhaseDefect, hmem]
  rw [hdefect] at hzero
  exact (by decide : (1 : ZMod 2) ≠ 0) hzero

/-- An explicit original north-tree physical edge carries a
flat but source-incompatible independent odd/odd exchange phase. -/
theorem c60F33OddOddNorthTreeEdge_not_sourcePhaseLocked :
    c60F33TreeRepairedEdgeGrade 1 1 (.around ⟨.north, .s0⟩) ∉
      c60F55PhaseLocked := by
  apply c60F33OddOddTreeRepaired_not_sourcePhaseLocked
  decide

/-- Actual Mathlib Wang Bi 64-chart natural transformation, using
all physical C60 edges and their 360 local corner indices, with
the complete independent neutral Gray coefficients still present. -/
def c60F33TreeRepairedWangBiAtlas (a b : ZMod 2)
    (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor :=
  c60WangBiGlobalGradedAtlas side (c60F33TreeRepairedEdgeGrade a b)

/-- Four-corner chart naturality for the genuinely flat, retained
braiding; this is transport of supplied symbols, NOT inference
of traditional meaning from the Gray exchange phase. -/
theorem c60F33TreeRepairedWangBiAtlas_natural
    (a b : ZMod 2) (frame₁ frame₂ : WangBiFrame)
    (f : frame₁ ⟶ frame₂)
    (side : C60DartSideGauge) (corner : C60ActualSquareCorner) :
    (wangBiChartArrow frame₁ frame₂ f
        (c60GaugeGradedLabel frame₁ side
          (c60F33TreeRepairedEdgeGrade a b) corner).1,
      (c60GaugeGradedLabel frame₁ side
        (c60F33TreeRepairedEdgeGrade a b) corner).2) =
      c60GaugeGradedLabel frame₂ side
        (c60F33TreeRepairedEdgeGrade a b) corner :=
  c60GaugeGradedLabel_natural frame₁ frame₂ f side
    (c60F33TreeRepairedEdgeGrade a b) corner

/-- 王弼 temporal semantics remains an independently given input;
the natural flat repair makes no identification of 意 with a phase. -/
theorem c60F33TreeRepairedTemporalRead_transport
    {T M : Type*}
    (frame₁ frame₂ : WangBiFrame) (f : frame₁ ⟶ frame₂)
    (reading : WangBiTemporalReading T M)
    (side : C60DartSideGauge)
    (corner : C60ActualSquareCorner) (t : T) :
    c60GaugeTemporalRead frame₂
      (wangBiFrameTransport frame₁ frame₂ f reading) side corner t =
    c60GaugeTemporalRead frame₁ reading side corner t :=
  c60F32WangBiTemporalRead_transport frame₁ frame₂ f reading side corner t

#print axioms c60F33CompleteFlatCorrectionClassification
#print axioms c60F33ReconstructActualEdgeCochain
#print axioms c60F33CorrectedGrade_realizes_cochain
#print axioms c60F33All32Flat_iff_completeCorrection
#print axioms c60F33VertexGauge_preserves_allFaceCurvature
#print axioms c60F33OddOddNorthPentagon_noGaugeCancellation
#print axioms c60F33OddOddVertexGauge_neverFlat
#print axioms c60F33TreeCorrected_eq_exactPotential
#print axioms c60F33TreeCorrection_all32_flat
#print axioms c60F33TreeCorrection_zero_on_tree
#print axioms c60F33TreeCorrectionSupport_card_le31
#print axioms c60F33TreeRepairedGrade_realizes_cochain
#print axioms c60F33TreeRepairedGrade_all32_flat
#print axioms c60F33TreeRepairedGrade_on_tree
#print axioms c60F33OddOddTreeRepaired_not_sourcePhaseLocked
#print axioms c60F33OddOddNorthTreeEdge_not_sourcePhaseLocked
#print axioms c60F33TreeRepairedWangBiAtlas
#print axioms c60F33TreeRepairedWangBiAtlas_natural
#print axioms c60F33TreeRepairedTemporalRead_transport

end
end KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181

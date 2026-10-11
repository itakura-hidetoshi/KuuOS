import KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
import KUOS.DependentOriginationGrayC60F55SharpRepairV5_168

namespace KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F26 / v5.174 — genuine C60 32-face Wang Bi / F55 global Gray descent

F59-F23/25 gave an actual Mathlib Category/Functor/NatTrans on
the original C60 real-flag geometry, including an explicit DART
side gauge correcting adjacent-flag symbolic gluing on 12 physical
Wuxing pentagons and 20 六氣 hexagons.

F59-F18/20 INDEPENDENTLY proved the actual INTEGER C60 chain
contraction, signed 32-face Gray curvature, complete H¹/H²
descent and a 27-edge canonical repair of the ORIGINAL F55
braided target 3-cell field.

This unit connects the two layers WITHOUT changing physical
geometry and WITHOUT claiming an all-source universal Gray
3-functor. The signed, ORIENTED 32-face surface curvature is
not the UNSIGNED sum of 5/6 square labels in each face.

It establishes:
1. A native Cat 2-dimensional Wang Bi chart atlas with arbitrary
   F55-valued real-edge grades, faithful in the supplied grades.
2. Compatibility between multiple chart changes and native
   categorical vertical composition / Gray braiding grade data.
3. ALL 32 physical signed pentagon/hexagon face holonomies
   cancel in the genuine Gray target for ANY original edge field.
   This is δ²=0, not an assertion that each local face is flat.
4. Exact H¹ descent criterion, local original F55 nonflatness and
   globally exact H² obstruction zero.
5. A CONSTRUCTIVE flat 90-edge graded atlas, changing exactly
   27 original F55 labels. All 63 other physical labels retain
   the original nontrivial F55 generator.
6. Explicit separation of a vertex-side Wang Bi symbol gauge
   from the independent F55 edge correction and the historical
   temporal meaning assigned by an external reading.

The full source F55 PresentedCell -> nontrivial ambient Gray
3-functor, global source 3-cell whiskering and Stage-II omega
identification remain distinct obligations.
-/

/-- The genuine original oriented 5- or 6-edge F55-target holonomy,
not the unsigned boundary length or a synthetic quadrilateral. -/
def c60WangBiSignedGrayFace
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : TruncatedIcosahedralSeedFace) : GradedThreeCell 0 0 :=
  c60F18SignedGrayFacePasting grade face

/-- Genuine oriented global Gray 3-cell on the 32 ORIGINAL
C60 physical faces, all of which come from actual integer
boundaries of the 60-90-32 cellular chain complex. -/
def c60WangBiSignedGraySurface
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    GradedThreeCell 0 0 :=
  ∑ face : TruncatedIcosahedralSeedFace,
    c60WangBiSignedGrayFace grade face

/-- The COMPLETE degree-two Gray obstruction is the native
signed-face holonomy evaluated on the original H₂ fundamental
surface. The extra exchange phase is retained separately. -/
def c60WangBiGraySurfaceObstruction
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    GradedThreeCell 0 0 :=
  c60F18GraySurfaceObstruction
    (c60WangBiSignedGrayFace grade)

/-- A genuine full C60 cellular identity: for ARBITRARY
edge-dependent nontrivial braided Gray 3-cells, the complete
ORIENTED 32-face sum vanishes because every physical edge's
signed total coefficient cancels. This does not impose local
flatness nor erase the individual original F55 generator phase. -/
theorem c60WangBiSignedGraySurface_zero
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60WangBiSignedGraySurface grade = 0 := by
  unfold c60WangBiSignedGraySurface c60WangBiSignedGrayFace
  calc
    (∑ face : TruncatedIcosahedralSeedFace,
        c60F18SignedGrayFacePasting grade face) =
      ∑ face : TruncatedIcosahedralSeedFace,
        c60F18GrayEdgeCochain grade
          (c60IntegerFaceBoundaryChain face) := by
            apply Finset.sum_congr rfl
            intro face _
            exact c60F18SignedGrayFacePasting_eq grade face
    _ = c60F18GrayEdgeCochain grade
          c60IntegerFullSurfaceBoundaryChain := by
            simp [c60IntegerFullSurfaceBoundaryChain, map_sum]
    _ = 0 := by
          rw [c60IntegerFullSurfaceBoundaryChain_zero, map_zero]

/-- H² global obstruction is zero as a typed native Gray
3-cell for EVERY real physical C60 edge assignment. -/
theorem c60WangBiGraySurfaceObstruction_zero
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60WangBiGraySurfaceObstruction grade = 0 := by
  rw [c60WangBiGraySurfaceObstruction,
      c60F18GraySurfaceObstruction_eq_sum]
  exact c60WangBiSignedGraySurface_zero grade

/-- This is actual native categorical identity of the whole
32-face composite, not only projection to the F58 integer charge. -/
theorem c60WangBiNativeGraySurface_identity
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60WangBiSignedGraySurface grade =
      (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit) := by
  rw [c60WangBiSignedGraySurface_zero grade]
  rfl

/-- Local 3-cell compositions of any two actual C60 signed
face holonomies satisfy native categorical interchange at
neutral grading; this is a consequence of the ORIGINAL native
braided target, not a proof-only invented 2-cell. -/
theorem c60WangBiNativeFaceInterchange
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face₁ face₂ : TruncatedIcosahedralSeedFace) :
    (c60WangBiSignedGrayFace grade face₁ ≫
       c60WangBiSignedGrayFace grade face₂ :
         GrayGrade.unit ⟶ GrayGrade.unit) =
    (c60WangBiSignedGrayFace grade face₂ ≫
       c60WangBiSignedGrayFace grade face₁ :
         GrayGrade.unit ⟶ GrayGrade.unit) := by
  rw [← grayNeutral_add_eq_native_comp,
    ← grayNeutral_add_eq_native_comp, add_comm]

/-- The actual 3-cell associator coherence for three real
signed pentagon/hexagon Gray face holonomies in the native
neutral-grade endomorphism category. -/
theorem c60WangBiNativeFaceTripleCoherence
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (f g h : TruncatedIcosahedralSeedFace) :
    ((c60WangBiSignedGrayFace grade f ≫
        c60WangBiSignedGrayFace grade g) ≫
        c60WangBiSignedGrayFace grade h :
          GrayGrade.unit ⟶ GrayGrade.unit) =
    (c60WangBiSignedGrayFace grade f ≫
        (c60WangBiSignedGrayFace grade g ≫
          c60WangBiSignedGrayFace grade h) :
          GrayGrade.unit ⟶ GrayGrade.unit) :=
  Category.assoc _ _ _

/-- An actual physical C60 graded Mathlib natural transformation
is available for EVERY edge-dependent F55 3-cell assignment,
including both the original curved and repaired flat fields. -/
def c60WangBiGlobalGradedAtlas
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor :=
  c60GaugeGradedNatTrans side grade

/-- The chart atlas is FAITHFUL in all ninety original
edge grades: evaluating at any physical four-flag corner
recovers the exact independent F55 Gray 3-cell, including
its integer generator charge and ZMod2 exchange phase. -/
theorem c60WangBiGlobalGradedAtlas_faithful
    (a : WangBiFrame) (side : C60DartSideGauge)
    {w z : TruncatedIcosahedralEdge → GradedThreeCell 0 0}
    (h : c60WangBiGlobalGradedAtlas side w =
      c60WangBiGlobalGradedAtlas side z) : w = z := by
  funext e
  have hApp := congrArg
    (fun η : c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor => η.app a) h
  have hEdge := congrArg
    (fun arrow : c60ActualCornerFunctor.obj a ⟶ c60GradedSixYaoFunctor.obj a =>
      (TypeCat.homEquiv arrow) (e, (false, false))) hApp
  exact congrArg Prod.snd hEdge

/-- Any three consecutive changes of Wang Bi charts are
coherent on the WHOLE actual C60 geometric flag AND the
nontrivial, independently supplied F55 edge 3-cell.
This is equality of genuine functorial action, not a claim
that Yang/Yin labels are absolute. -/
theorem c60WangBiGlobalFourChartCoherence
    (a b c d : WangBiFrame) (f : a ⟶ b) (g : b ⟶ c)
    (h : c ⟶ d) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (corner : C60ActualSquareCorner) :
    (wangBiChartArrow c d h
      (wangBiChartArrow b c g
        (wangBiChartArrow a b f
          (c60GaugeGradedLabel a side grade corner).1)),
      (c60GaugeGradedLabel a side grade corner).2) =
      c60GaugeGradedLabel d side grade corner := by
  have ht :=
    c60GaugeGradedLabel_natural a d ((f ≫ g) ≫ h) side grade corner
  rw [wangBiFourChartCoherence a b c d
    (c60GaugeGradedLabel a side grade corner).1 f g h] at ht
  exact ht

/-- A native target Gray 3-cell's vertical composition is
compatible with the genuine Wang Bi local six-Yao chart:
the square's six-Yao is unchanged by higher composition, while
the independent F55 grade is composed categorically. -/
theorem c60WangBiGlobalNativeGradeComposition
    (a : WangBiFrame) (side : C60DartSideGauge)
    (w z : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (corner : C60ActualSquareCorner) :
    ((c60GaugeGradedLabel a side w corner).2 ≫
      (c60GaugeGradedLabel a side z corner).2 :
      GrayGrade.unit ⟶ GrayGrade.unit) =
    (c60GaugeGradedLabel a side
      (fun e => w e + z e) corner).2 :=
  (grayNeutral_add_eq_native_comp (w corner.1) (z corner.1)).symm

/-- A concrete chart / native 3-cell INTERCHANGE SQUARE,
valid at all 360 actual corners: chart transport commutes
with categorical composition of the independent edge grades. -/
theorem c60WangBiGlobalChartNativeInterchange
    (a b : WangBiFrame) (f : a ⟶ b)
    (side : C60DartSideGauge)
    (w z : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (corner : C60ActualSquareCorner) :
    (wangBiChartArrow a b f (c60GaugeGradedLabel a side w corner).1,
      ((c60GaugeGradedLabel a side w corner).2 ≫
        (c60GaugeGradedLabel a side z corner).2 :
          GrayGrade.unit ⟶ GrayGrade.unit)) =
      c60GaugeGradedLabel b side (fun e => w e + z e) corner := by
  rw [c60WangBiGlobalNativeGradeComposition a side w z corner]
  exact c60GaugeGradedLabel_natural a b f side
    (fun e => w e + z e) corner

/-- EXACT H¹ criterion in the corrected Wang Bi atlas:
all original signed pentagon/hexagon target 3-cell curvature
values vanish iff the original real 90-edge grade cochain
comes from a single global vertex Gray potential. -/
theorem c60WangBiGlobalFlatIffVertexDescent
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∀ face : TruncatedIcosahedralSeedFace,
        c60WangBiSignedGrayFace grade face = 0) ↔
      ∃ vertexGauge : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        c60F18GrayEdgeCochain grade =
          vertexGauge.comp c60IntegralBoundaryOne := by
  constructor
  · intro hflat
    exact c60F18GrayFaceFlatness_descends grade hflat
  · rintro ⟨vertexGauge, hEq⟩ face
    have hCochain := (c60F18ClosedEdgeIffVertexPotential
      (c60F18GrayEdgeCochain grade)).mpr ⟨vertexGauge, hEq⟩
    have hFace := LinearMap.congr_fun hCochain
      (Finsupp.single face (1 : ℤ))
    change c60F18GrayEdgeCochain grade
      (c60IntegralBoundaryTwo
        (Finsupp.single face (1 : ℤ))) = 0 at hFace
    rw [c60IntegralBoundaryTwo_singleFace] at hFace
    exact (c60F18SignedGrayFacePasting_eq grade face).trans hFace

/-- The ORIGINAL all-ninety actual F55 square field is a valid
and chart-natural Wang Bi global atlas, but its oriented north
pentagon curvature is GENUINELY nonzero. The global H²
cancellation alone does not imply local H¹ descent. -/
theorem c60WangBiOriginalF55NorthFace_nonflat :
    c60WangBiSignedGrayFace c60F19UniformF55EdgeLabels
      (.aroundVertex .north) ≠ 0 :=
  c60F19NorthPentagon_curvature_nonzero

/-- A canonical constructive global COCHAIN correction built
from the original 59-edge physical C60 spanning tree, not an
abstract existence theorem or an altered C60 edge set. -/
def c60WangBiFlatRepairedCochain :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F19OriginalF55EdgeCochain + c60F19CanonicalTreeCorrection

/-- All actual 32 oriented pentagonal/hexagonal faces have
zero signed curvature after the canonical F55 tree correction. -/
theorem c60WangBiFlatRepairedCochain_flat :
    c60WangBiFlatRepairedCochain.comp
      c60IntegralBoundaryTwo = 0 :=
  c60F19CanonicalTreeCorrection_flat

/-- Define a genuine corrected edge-indexed 3-cell ATLAS
by evaluating the existing canonical corrected linear cochain
on each of the ninety ORIGINAL physical edge generators. -/
def c60WangBiRepairedEdgeGrade
    (e : TruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  c60WangBiFlatRepairedCochain (Finsupp.single e (1 : ℤ))

/-- Every actual repaired edge is the SAME original F55
generator plus the explicit signed correction computed from
the original C60 spanning tree. No external edge is added. -/
theorem c60WangBiRepairedEdgeGrade_formula
    (e : TruncatedIcosahedralEdge) :
    c60WangBiRepairedEdgeGrade e =
      originalF55BraidedSquareGenerator +
        c60F20OriginalTreeCorrectionDegree e •
          originalF55BraidedSquareGenerator := by
  unfold c60WangBiRepairedEdgeGrade c60WangBiFlatRepairedCochain
  rw [LinearMap.add_apply,
    c60F20OriginalF55SingleEdge,
    c60F20CanonicalCorrection_edgeFormula]

/-- ORIGINAL nonzero F55 square data is unchanged on every
physical edge outside the explicitly determined set of 27
genuinely modified C60 edges. -/
theorem c60WangBiRepairedEdgeGrade_preserved
    (e : TruncatedIcosahedralEdge)
    (he : c60F20IsChangedEdge e = false) :
    c60WangBiRepairedEdgeGrade e =
      originalF55BraidedSquareGenerator := by
  have hzero : c60F20OriginalTreeCorrectionDegree e = 0 := by
    by_contra hn
    have hc := (c60F20CorrectionDegree_support_certificate e).mp hn
    simp [he] at hc
  rw [c60WangBiRepairedEdgeGrade_formula, hzero, zero_smul, add_zero]

/-- The actual original F55 target atlas and the corrected
global atlas differ at exactly the ORIGINAL 27 real C60
edge positions: 12 closing pentagon edges and 15 original
hexagon-link cross edges. -/
theorem c60WangBiRepairedEdgeGrade_changed_iff
    (e : TruncatedIcosahedralEdge) :
    c60WangBiRepairedEdgeGrade e ≠
        originalF55BraidedSquareGenerator ↔
      c60F20IsChangedEdge e = true := by
  rw [c60WangBiRepairedEdgeGrade_formula]
  have hbase := c60F20OriginalGeneratorNonzeroScalar_iff
    (c60F20OriginalTreeCorrectionDegree e)
  have hchanged := c60F20CorrectionDegree_support_certificate e
  constructor
  · intro h
    apply hchanged.mp
    intro hz
    apply h
    rw [hz, zero_smul, add_zero]
  · intro h
    have hn : c60F20OriginalTreeCorrectionDegree e ≠ 0 :=
      hchanged.mpr h
    have hs := hbase.mpr hn
    intro heq
    have hz :
        c60F20OriginalTreeCorrectionDegree e •
          originalF55BraidedSquareGenerator = 0 := by
      calc
        _ = originalF55BraidedSquareGenerator +
            c60F20OriginalTreeCorrectionDegree e •
              originalF55BraidedSquareGenerator -
            originalF55BraidedSquareGenerator := by abel
        _ = 0 := by rw [heq, sub_self]
    exact hs hz

/-- The exact set of physically changed F55-square edge grades.
The independently typed graded F55 target is noncomputable, so its
DecidablePred is obtained locally rather than adding an axiom. -/
noncomputable def c60WangBiRepairedChangedSupport :
    Finset TruncatedIcosahedralEdge := by
  classical
  exact Finset.univ.filter (fun e =>
    c60WangBiRepairedEdgeGrade e ≠ originalF55BraidedSquareGenerator)

/-- Exactly TWENTY-SEVEN of the ninety physical F55 3-cell
edge grades actually change; the remaining SIXTY-THREE
are all original nontrivial braided square generators. -/
theorem c60WangBiRepairedEdgeGrade_changed_card :
    c60WangBiRepairedChangedSupport.card = 27 := by
  classical
  have hs :
      c60WangBiRepairedChangedSupport =
      Finset.univ.filter (fun e =>
        c60F20IsChangedEdge e = true) := by
    ext e
    simp only [c60WangBiRepairedChangedSupport,
      Finset.mem_filter, Finset.mem_univ, true_and]
    exact c60WangBiRepairedEdgeGrade_changed_iff e
  rw [hs]
  exact c60F20ChangedPhysicalEdge_card

/-- The REPAIRED actual C60 edge grades admit a genuine
Wang Bi 64-symbol × F55 graded Mathlib natural transformation
in all 360 edge-local flags of the physically unchanged C60. -/
def c60WangBiRepairedGlobalAtlas
    (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor :=
  c60WangBiGlobalGradedAtlas side c60WangBiRepairedEdgeGrade

/-- For all chosen side gauges and Wang Bi chart morphisms,
the repaired nontrivial F55 3-cell labels transport naturally
without forgetting any of their 0/1/Int charge components. -/
theorem c60WangBiRepairedGlobalAtlas_natural
    (a b : WangBiFrame) (f : a ⟶ b)
    (side : C60DartSideGauge) (c : C60ActualSquareCorner) :
    (wangBiChartArrow a b f
        (c60GaugeGradedLabel a side c60WangBiRepairedEdgeGrade c).1,
      (c60GaugeGradedLabel a side c60WangBiRepairedEdgeGrade c).2) =
      c60GaugeGradedLabel b side c60WangBiRepairedEdgeGrade c :=
  c60GaugeGradedLabel_natural a b f side c60WangBiRepairedEdgeGrade c

/-- Exact surface cancellation applies in particular to the
new 27-edge corrected high-dimensional C60 Wang Bi atlas,
independently of every supplied temporal interpretation. -/
theorem c60WangBiRepairedSurface_globalZero :
    c60WangBiSignedGraySurface c60WangBiRepairedEdgeGrade = 0 :=
  c60WangBiSignedGraySurface_zero c60WangBiRepairedEdgeGrade

#print axioms c60WangBiSignedGraySurface_zero
#print axioms c60WangBiGraySurfaceObstruction_zero
#print axioms c60WangBiNativeGraySurface_identity
#print axioms c60WangBiNativeFaceInterchange
#print axioms c60WangBiNativeFaceTripleCoherence
#print axioms c60WangBiGlobalGradedAtlas
#print axioms c60WangBiGlobalGradedAtlas_faithful
#print axioms c60WangBiGlobalFourChartCoherence
#print axioms c60WangBiGlobalNativeGradeComposition
#print axioms c60WangBiGlobalChartNativeInterchange
#print axioms c60WangBiGlobalFlatIffVertexDescent
#print axioms c60WangBiOriginalF55NorthFace_nonflat
#print axioms c60WangBiFlatRepairedCochain_flat
#print axioms c60WangBiRepairedEdgeGrade_formula
#print axioms c60WangBiRepairedEdgeGrade_preserved
#print axioms c60WangBiRepairedEdgeGrade_changed_iff
#print axioms c60WangBiRepairedEdgeGrade_changed_card
#print axioms c60WangBiRepairedGlobalAtlas
#print axioms c60WangBiRepairedGlobalAtlas_natural
#print axioms c60WangBiRepairedSurface_globalZero

end
end KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174

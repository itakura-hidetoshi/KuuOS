import KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165
import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
import KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

namespace KUOS.DependentOriginationGrayC60CochainDescentV5_166

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162
open KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
open KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 3000000
noncomputable section

/-!
# F59-F18 / v5.166 — exact C60 cochain descent and Gray-square obstruction

F59-F15, F16 and F17 established strict integral cellular chain
contractions for the REAL original C60: sixty darts, ninety signed
edges and thirty-two oriented pentagon/hexagon faces.

We now DUALIZE those proven chain identities to ANY integer-linear
coefficient group (including the genuine neutral-grade braided Gray
3-cell endomorphism group, whose addition equals native composition).

1. A signed edge cochain is flat on every actual pentagonal/hexagonal
   face iff it descends to a vertex potential; the vertex potential
   is unique up to a root-dependent constant.
2. A signed face cochain comes from actual edge cochains iff its
   evaluation on the oriented all-32-face fundamental cycle vanishes.
   That evaluation is the COMPLETE degree-two descent obstruction.
3. Apply these results to independently supplied Gray 3-cell labels
   on all ninety original C60 incidence squares, respecting negative
   signs from genuine oriented face boundaries.

This is a theorem about the actual INTEGRAL CELLULAR COCHAIN COMPLEX
and the existing independent F59 braided Gray *target*. It is NOT a
claim that an arbitrary original F55 3-cell assignment is locally
flat, a global Gray 3-functor, an S² homeomorphism, or an identity
with the historically distinct Stage-II omega.
-/

section Universal
variable {A : Type*} [AddCommGroup A]

/-- A true integer-linear C60 vertex gauge differentiates to an
edge cochain using the ORIGINAL edge-to-dart differential. -/
def c60F18VertexCoboundary
    (potential : C60IntegralZeroChains →ₗ[ℤ] A) :
    C60IntegralOneChains →ₗ[ℤ] A :=
  potential.comp c60IntegralBoundaryOne

/-- A true integer-linear edge cochain differentiates to a face
cochain using the ORIGINAL oriented pentagon/hexagon boundary. -/
def c60F18EdgeCoboundary
    (edgeLabel : C60IntegralOneChains →ₗ[ℤ] A) :
    C60IntegralTwoChains →ₗ[ℤ] A :=
  edgeLabel.comp c60IntegralBoundaryTwo

/-- Square-zero in cochains follows from the ACTUAL integer
C60 cellular identity d₁ ∘ d₂ = 0. -/
theorem c60F18Coboundary_squared_zero
    (potential : C60IntegralZeroChains →ₗ[ℤ] A) :
    c60F18EdgeCoboundary
      (c60F18VertexCoboundary potential) = 0 := by
  apply LinearMap.ext
  intro x
  change potential
    (c60IntegralBoundaryOne (c60IntegralBoundaryTwo x)) = 0
  rw [c60IntegralBoundaryOne_boundaryTwo_apply_zero, map_zero]

/-- Exact C60 H¹ DESCENT: every integer-linear assignment to actual
edges with zero oriented face holonomy comes from a vertex gauge.
Proof uses the REAL degree-one contracting identity from F59-F16. -/
theorem c60F18FlatEdgeCochain_descends
    (edgeLabel : C60IntegralOneChains →ₗ[ℤ] A)
    (hflat : edgeLabel.comp c60IntegralBoundaryTwo = 0) :
    edgeLabel =
      (edgeLabel.comp c60F16PrimalPathLift).comp c60IntegralBoundaryOne := by
  apply LinearMap.ext
  intro x
  have hc := LinearMap.congr_fun c60F16ContractingIdentity x
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at hc
  have hz := LinearMap.congr_fun hflat (c60F16FaceFillLift x)
  simp only [LinearMap.comp_apply, LinearMap.zero_apply] at hz
  change edgeLabel x =
    edgeLabel (c60F16PrimalPathLift (c60IntegralBoundaryOne x))
  calc
    edgeLabel x =
        edgeLabel (c60IntegralBoundaryTwo (c60F16FaceFillLift x) +
          c60F16PrimalPathLift (c60IntegralBoundaryOne x)) :=
      congrArg edgeLabel hc.symm
    _ = edgeLabel (c60F16PrimalPathLift (c60IntegralBoundaryOne x)) := by
      rw [map_add, hz, zero_add]

/-- FACE-WISE PENTAGON/HEXAGON COMPATIBILITY is equivalent to the
existence of a global integral-linear vertex potential. -/
theorem c60F18ClosedEdgeIffVertexPotential
    (edgeLabel : C60IntegralOneChains →ₗ[ℤ] A) :
    edgeLabel.comp c60IntegralBoundaryTwo = 0 ↔
      ∃ potential : C60IntegralZeroChains →ₗ[ℤ] A,
        edgeLabel = potential.comp c60IntegralBoundaryOne := by
  constructor
  · intro hflat
    exact ⟨edgeLabel.comp c60F16PrimalPathLift,
      c60F18FlatEdgeCochain_descends edgeLabel hflat⟩
  · rintro ⟨potential, rfl⟩
    exact c60F18Coboundary_squared_zero potential

/-- An integral vertex potential with identically zero gradient
factors through the F59-F15 augmentation: its only freedom is the
constant value at the actual north-spoke root dart. -/
theorem c60F18ZeroGradient_factorsAugmentation
    (potential : C60IntegralZeroChains →ₗ[ℤ] A)
    (hzero : potential.comp c60IntegralBoundaryOne = 0) :
    potential =
      (potential.comp c60RootEmbedding).comp
        c60IntegralVertexAugmentation := by
  apply LinearMap.ext
  intro x
  have hc := LinearMap.congr_fun c60VertexPathLift_homotopy x
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at hc
  have hz := LinearMap.congr_fun hzero (c60VertexPathLift x)
  simp only [LinearMap.comp_apply, LinearMap.zero_apply] at hz
  change potential x =
    potential (c60RootEmbedding (c60IntegralVertexAugmentation x))
  calc
    potential x = potential
        (c60IntegralBoundaryOne (c60VertexPathLift x) +
          c60RootEmbedding (c60IntegralVertexAugmentation x)) :=
      congrArg potential hc.symm
    _ = potential
        (c60RootEmbedding (c60IntegralVertexAugmentation x)) := by
      rw [map_add, hz, zero_add]

/-- COMPLETE H² NORMAL FORM: any actual C60 face cochain splits
as an exact edge coboundary plus its ONE global surface component.
This is the DUAL of F59-F17's genuine 32-face contraction. -/
theorem c60F18FaceCochainNormalForm
    (faceLabel : C60IntegralTwoChains →ₗ[ℤ] A) :
    faceLabel =
      (faceLabel.comp c60F16FaceFillLift).comp c60IntegralBoundaryTwo +
      (faceLabel.comp c60F17FundamentalSurfaceEmbedding).comp
        c60F17NorthFaceCoefficient := by
  apply LinearMap.ext
  intro x
  have hc := LinearMap.congr_fun c60F17TwoChainReconstruction x
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at hc
  change faceLabel x =
    faceLabel (c60F16FaceFillLift (c60IntegralBoundaryTwo x)) +
      faceLabel (c60F17FundamentalSurfaceEmbedding
        (c60F17NorthFaceCoefficient x))
  calc
    faceLabel x = faceLabel
      (c60F16FaceFillLift (c60IntegralBoundaryTwo x) +
        c60F17FundamentalSurfaceEmbedding
          (c60F17NorthFaceCoefficient x)) :=
      congrArg faceLabel hc.symm
    _ = _ := map_add _ _ _

/-- The exact global 2-cochain obstruction is its value on the
ACTUAL oriented sum of the thirty-two C60 pentagons and hexagons. -/
def c60F18SurfaceObstruction
    (faceLabel : C60IntegralTwoChains →ₗ[ℤ] A) : A :=
  faceLabel c60IntegralFundamentalSurfaceChain

/-- Universal pentagon/hexagon FACE DESCENT CRITERION: a specified
integral face cochain comes from some actual signed edge cochain
if and only if its complete surface obstruction vanishes. -/
theorem c60F18FaceDescent_iff_surfaceObstruction_zero
    (faceLabel : C60IntegralTwoChains →ₗ[ℤ] A) :
    (∃ edgeLabel : C60IntegralOneChains →ₗ[ℤ] A,
      faceLabel = edgeLabel.comp c60IntegralBoundaryTwo) ↔
    c60F18SurfaceObstruction faceLabel = 0 := by
  constructor
  · rintro ⟨edgeLabel, rfl⟩
    change edgeLabel
      (c60IntegralBoundaryTwo c60IntegralFundamentalSurfaceChain) = 0
    rw [c60IntegralBoundaryTwo_fundamental_zero, map_zero]
  · intro hzero
    refine ⟨faceLabel.comp c60F16FaceFillLift, ?_⟩
    apply LinearMap.ext
    intro x
    have hc := LinearMap.congr_fun c60F17TwoChainReconstruction x
    simp only [LinearMap.add_apply, LinearMap.comp_apply,
      LinearMap.id_apply] at hc
    have hfund :
        faceLabel
          (c60F17FundamentalSurfaceEmbedding
            (c60F17NorthFaceCoefficient x)) = 0 := by
      rw [c60F17FundamentalSurfaceEmbedding,
        LinearMap.toSpanSingleton_apply, map_smul]
      change faceLabel c60IntegralFundamentalSurfaceChain = 0 at hzero
      rw [hzero, smul_zero]
    change faceLabel x =
      faceLabel (c60F16FaceFillLift (c60IntegralBoundaryTwo x))
    calc
      faceLabel x = faceLabel
        (c60F16FaceFillLift (c60IntegralBoundaryTwo x) +
          c60F17FundamentalSurfaceEmbedding
            (c60F17NorthFaceCoefficient x)) :=
        congrArg faceLabel hc.symm
      _ = faceLabel (c60F16FaceFillLift
            (c60IntegralBoundaryTwo x)) := by
        rw [map_add, hfund, add_zero]

end Universal

/-! ## Genuine neutral-grade F59 braided Gray 3-cell coefficients -/

/-- Extend independent labels on ALL original ninety C60 edge squares
into a ℤ-linear cochain valued in the ACTUAL neutral-grade F59
braided Gray 3-cell endomorphism group. Addition here agrees with
native Gray categorical composition by grayNeutral_add_eq_native_comp. -/
def c60F18GrayEdgeCochain
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  Finsupp.linearCombination ℤ w

/-- The corresponding signed pentagon/hexagon face pasting is an
ACTUAL integer-coefficient product of the original oriented
C60 incidence-square edge labels; reverse edges use additive
inverse (native inverse Gray 3-cell). -/
def c60F18SignedGrayFacePasting
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : TruncatedIcosahedralSeedFace) : GradedThreeCell 0 0 :=
  ((c60IntegerOrientedFaceBoundary face).map
    (fun p => p.2 • w p.1)).sum

/-- Identifies the original real cyclic signed face pasting with
the ACTUAL integral C60 cellular boundary evaluated in the F59
native braided Gray endomorphism group. -/
theorem c60F18SignedGrayFacePasting_eq
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : TruncatedIcosahedralSeedFace) :
    c60F18SignedGrayFacePasting w face =
      c60F18GrayEdgeCochain w (c60IntegerFaceBoundaryChain face) := by
  rw [c60IntegerFaceBoundaryChain_asSignedList]
  change ((c60IntegerOrientedFaceBoundary face).map
      (fun p => p.2 • w p.1)).sum =
    c60F18GrayEdgeCochain w
      ((c60IntegerOrientedFaceBoundary face).map
        (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum
  induction (c60IntegerOrientedFaceBoundary face) with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, map_add]
      rw [ih]
      simp [c60F18GrayEdgeCochain]

/-- If the original signed Gray 3-cell composites vanish on all
TWELVE pentagons and TWENTY hexagons, the labels on all ninety
original F55-type incidence squares descend to a true vertex gauge.
No assumption of local flatness is manufactured. -/
theorem c60F18GrayFaceFlatness_descends
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (hfaces : ∀ face : TruncatedIcosahedralSeedFace,
      c60F18SignedGrayFacePasting w face = 0) :
    ∃ vertexGauge : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayEdgeCochain w =
        vertexGauge.comp c60IntegralBoundaryOne := by
  apply (c60F18ClosedEdgeIffVertexPotential
    (c60F18GrayEdgeCochain w)).mp
  apply Finsupp.lhom_ext
  intro face z
  change c60F18GrayEdgeCochain w
    (c60IntegralBoundaryTwo (Finsupp.single face z)) = 0
  calc
    _ = c60F18GrayEdgeCochain w
        (z • c60IntegerFaceBoundaryChain face) := by
        simp [c60IntegralBoundaryTwo]
    _ = z • c60F18GrayEdgeCochain w
        (c60IntegerFaceBoundaryChain face) := by rw [map_smul]
    _ = 0 := by
      rw [← c60F18SignedGrayFacePasting_eq, hfaces face, smul_zero]

/-- Genuine Gray-valued C60 face labels, one on each of its
thirty-two original pentagonal/hexagonal faces. -/
def c60F18GrayFaceCochain
    (w : TruncatedIcosahedralSeedFace → GradedThreeCell 0 0) :
    C60IntegralTwoChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  Finsupp.linearCombination ℤ w

/-- A face-label assignment has a complete global Gray
obstruction: its actual charge and exchange phase are carried
by the oriented sum of the ORIGINAL 32 C60 faces. -/
def c60F18GraySurfaceObstruction
    (w : TruncatedIcosahedralSeedFace → GradedThreeCell 0 0) :
    GradedThreeCell 0 0 :=
  c60F18SurfaceObstruction (c60F18GrayFaceCochain w)

/-- The surface obstruction is literally the native Gray sum
of the thirty-two physical face labels, NOT an unrelated
freestanding formal global charge. -/
theorem c60F18GraySurfaceObstruction_eq_sum
    (w : TruncatedIcosahedralSeedFace → GradedThreeCell 0 0) :
    c60F18GraySurfaceObstruction w =
      ∑ face : TruncatedIcosahedralSeedFace, w face := by
  simp [c60F18GraySurfaceObstruction,
    c60F18SurfaceObstruction, c60F18GrayFaceCochain,
    c60IntegralFundamentalSurfaceChain]

/-- COMPLETENESS OF C60 GRAY DESCENT: an arbitrary original
pentagon/hexagon Gray face-label cochain is integrable as signed
90-edge square labels EXACTLY when the original oriented
global surface Gray 3-cell obstruction vanishes. -/
theorem c60F18GrayFaceIntegrable_iff_globalObstruction_zero
    (w : TruncatedIcosahedralSeedFace → GradedThreeCell 0 0) :
    (∃ squareEdgeCochain :
        C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayFaceCochain w =
        squareEdgeCochain.comp c60IntegralBoundaryTwo) ↔
      c60F18GraySurfaceObstruction w = 0 :=
  c60F18FaceDescent_iff_surfaceObstruction_zero
    (c60F18GrayFaceCochain w)

/-- All degree-two Gray descent obstructions vanish precisely
when both the original integer generator charge and independent
braided exchange-phase components vanish. -/
theorem c60F18GrayObstruction_components_zero_iff
    (w : TruncatedIcosahedralSeedFace → GradedThreeCell 0 0) :
    c60F18GraySurfaceObstruction w = 0 ↔
      (c60F18GraySurfaceObstruction w).charge = (0, 0) ∧
      (c60F18GraySurfaceObstruction w).phase = 0 := by
  constructor
  · intro h
    rw [h]
    exact ⟨rfl, rfl⟩
  · rintro ⟨hc, hp⟩
    apply GradedThreeCell.ext
    · exact hc
    · exact hp

#print axioms c60F18Coboundary_squared_zero
#print axioms c60F18FlatEdgeCochain_descends
#print axioms c60F18ClosedEdgeIffVertexPotential
#print axioms c60F18ZeroGradient_factorsAugmentation
#print axioms c60F18FaceCochainNormalForm
#print axioms c60F18FaceDescent_iff_surfaceObstruction_zero
#print axioms c60F18SignedGrayFacePasting_eq
#print axioms c60F18GrayFaceFlatness_descends
#print axioms c60F18GraySurfaceObstruction_eq_sum
#print axioms c60F18GrayFaceIntegrable_iff_globalObstruction_zero
#print axioms c60F18GrayObstruction_components_zero_iff

end
end KUOS.DependentOriginationGrayC60CochainDescentV5_166

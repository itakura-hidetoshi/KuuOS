import KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204

namespace KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F55-B / v5.204: full local mixed categorical equivalence
# coexists with the honest original-F55 lifting/descent obstruction

The new F55-A establishes FULLY FAITHFUL, objectwise bijective
transport between F47 FOUR-BOUNDARY mixed categories of both
original physical faces for every genuine C60 edge.

That transport alone is NOT a globally flat gauge on the real
C60 vertex-edge-face complex. Here we prove two explicit no-go
results while RETAINING the independent actual F54 original
disjoint-square 2-cell boundaries:
  (i) for each of all 90 edges and either original incident face,
      NO genuine raw ORIGINAL nine-constructor F55 PresentedCell
      on the ACTUAL two F54 rotation-square routes can serve as the
      mixed comparison making F43/F52 face interchange equal the
      genuine original F55 source square;
  (ii) the source original F55 all-edge rotation-square field
      cannot arise as an exact vertex-gauge despite the existence
      of all 90 full-faithful mixed face-choice comparison functors.
The new comparison Δ=(0,1;0) is necessarily ADJOINED to F47,
its north signed five-edge curvature is second charge -5,
and its phase remains zero. No global descent is inferred.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualOriginalF54Rotations
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- A STRONGER geometrically indexed original-source NO-GO:
at any real C60 edge and either actual neighboring pentagon /
hexagon, the new F47 comparison cannot be replaced by ANY
original F55 nine-constructor 3-arrow between the SAME original
F54 square-left-first and square-right-first rotation routes.

This is not just a failure to choose one convenient primitive;
the theorem quantifies over every original freely generated word
with the EXACT source and target rotation paths. -/
theorem c60F55EveryActualMixedReceiver_noOriginalF55Cell
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge side).rotationStep := by
  rintro ⟨cell, heq⟩
  have hunique :=
    (c60F54ActualOriginalF43F55_uniqueReceiver
      t₁ t₂ left right edge side (c60F55SourceNative cell)).mp heq
  have hmem := c60F55SourceNative_mem cell
  rw [hunique] at hmem
  exact c60F54ActualCalibration_notOriginalF55 hmem

/-- Every locally mixed fully faithful face-choice source
functor still coexists with a GLOBAL ORIGINAL-C60 no-vertex-
gauge obstruction: the genuine original F55 rotation field
cannot be a coboundary of any original C60 vertex potential.

The conclusion is stronger than a nonzero target phase. The
north pentagon has a nonzero second INTEGER curvature charge. -/
theorem c60F55EveryActualFaceChoice_fullyFaithful_but_noVertexGauge
    (side : Bool) :
    (∀ (edge : TruncatedIcosahedralEdge),
      ∀ (X Y : C60F47BoundaryPoint
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge false)),
        Function.Bijective
          (fun (f : X ⟶ Y) =>
            (c60F48ActualEdgeFaceChoiceFunctor
              t₁ t₂ left right edge).map f)) ∧
    ¬ ∃ φ : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayEdgeCochain
        (c60F48OriginalRotationField t₁ t₂ left right side) =
          φ.comp c60IntegralBoundaryOne := by
  constructor
  · intro edge X Y
    exact c60F55ActualEdgeFaceChoice_isFullyFaithful
      t₁ t₂ left right edge (X := X) (Y := Y)
  · exact c60F48MixedOriginalF55_noVertexGauge
      t₁ t₂ left right side

/-- The exact real north pentagon exhibits the obstruction
through the second independent F58 integer generator charge,
not through a loose analogy between pentagon and square. -/
theorem c60F55ActualNewComparison_northChargeAndPhase
    (side : Bool) :
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).charge.2 = (-5 : ℤ) ∧
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).phase = (0 : ZMod 2) := by
  exact ⟨c60F54ActualCalibration_northSecondCharge
      t₁ t₂ left right side,
    c60F54ActualCalibration_northPhaseZero
      t₁ t₂ left right side⟩

/-- Full source no-lift is independent of the physically
chosen side, including actual north and hexagon incident
faces. The explicit side quantifier makes this a uniform
180-site no-go rather than just one north-face example. -/
theorem c60F55AllNinetyBothFaces_noOriginalLift :
    ∀ edge : TruncatedIcosahedralEdge, ∀ side : Bool,
      ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge side).rotationStep := by
  intro edge side
  exact c60F55EveryActualMixedReceiver_noOriginalF55Cell
    t₁ t₂ left right edge side

#print axioms c60F55EveryActualMixedReceiver_noOriginalF55Cell
#print axioms c60F55EveryActualFaceChoice_fullyFaithful_but_noVertexGauge
#print axioms c60F55ActualNewComparison_northChargeAndPhase
#print axioms c60F55AllNinetyBothFaces_noOriginalLift

end ActualOriginalF54Rotations
end
end KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204

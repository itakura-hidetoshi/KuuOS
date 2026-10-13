import KUOS.DependentOriginationC60PhysicalGradedNerveSquareV5_216
import KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205
import Mathlib.AlgebraicTopology.SimplicialSet.Nerve

namespace KUOS.DependentOriginationC60PhysicalFaceNerveIsoV5_217

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215
open KUOS.DependentOriginationC60PhysicalGradedNerveSquareV5_216
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.217: genuine category equivalence of the two original physical C60 face presentations.

For each real edge, the full-native-kernel F47 mixed source categories
have original, independently typed F42 and F54/F55 contexts. Existing
roundtrip natural isomorphisms construct an actual Mathlib category
equivalence with coherent triangle. The forward native nerve action
is bijective on each typed Hom and commutes with the complete F49
Gray observation in EVERY simplicial degree (by merged v5.216).

A categorical equivalence of nerves is NOT asserted to be a strict
simplicial isomorphism. The raw original F55 delta nonlift and
north-pentagon curvature remain nonzero obstructions.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualPhysicalEdge

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

/-- The source-level face-change and reverse face-change functors
compose to the identity on all original F47 four-tag Hom quotients. -/

/-- The original physical adjacent-face source comparison and its reverse
compose to an actual typed Mathlib natural isomorphism, not a new source axiom. -/
def c60PhysicalFaceChange_forward_reverse_NatIso
    (edge : TruncatedIcosahedralEdge) :
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge) ⋙
      (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge) ≅
    𝟭 (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)) := by
  let B₀ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false
  let B₁ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true
  have hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep :=
    c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge
  have hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep := rfl
  exact c60F56MixedTransport_roundTripNatIso B₀ B₁ hface hrot

/-- The second face's original F42 boundary stays separately typed. -/
def c60PhysicalFaceChange_reverse_forward_NatIso
    (edge : TruncatedIcosahedralEdge) :
    (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge) ⋙
      (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge) ≅
    𝟭 (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)) := by
  let B₀ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false
  let B₁ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true
  have hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep :=
    c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge
  have hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep := rfl
  exact c60F56MixedTransport_roundTripNatIso B₁ B₀ hface.symm hrot.symm

/-- Mathlib upgrades genuine inverse source NatIso to a coherent
category equivalence, with its adjoint triangle law. -/
def c60PhysicalFaceChangeEquivalence
    (edge : TruncatedIcosahedralEdge) :
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) ≌
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) :=
  CategoryTheory.Equivalence.mk
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge)
    (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge)
    (c60PhysicalFaceChange_forward_reverse_NatIso
      t₁ t₂ left right edge).symm
    (c60PhysicalFaceChange_reverse_forward_NatIso
      t₁ t₂ left right edge)

@[simp] theorem c60PhysicalFaceChangeEquivalence_functor
    (edge : TruncatedIcosahedralEdge) :
    (c60PhysicalFaceChangeEquivalence t₁ t₂ left right edge).functor =
      c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge := rfl

/-- Nerve of the genuine source inverse face-choice functor. -/
def c60PhysicalReverseFaceChoiceNerveMap
    (edge : TruncatedIcosahedralEdge) :
    c60PhysicalMixedThreeNerve t₁ t₂ left right edge true ⟶
      c60PhysicalMixedThreeNerve t₁ t₂ left right edge false :=
  CategoryTheory.nerveMap
    (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge)

/-- Actual face-change nerve edge action is bijective on every typed
four-boundary 3-Hom, by the EXISTING proved original full-faithfulness. -/
theorem c60PhysicalFaceChoiceNerveMap_hom_bijective
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        CategoryTheory.nerve.homEquiv
          ((CategoryTheory.nerve.edgeMk f).map
            (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge))) := by
  have hEq :
      (fun (f : X ⟶ Y) =>
        CategoryTheory.nerve.homEquiv
          ((CategoryTheory.nerve.edgeMk f).map
            (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge))) =
      (fun (f : X ⟶ Y) =>
        (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map f) := by
    funext f
    exact c60PhysicalFaceChoiceNerveMap_edges t₁ t₂ left right edge f
  rw [hEq]
  exact c60F55ActualEdgeFaceChoice_isFullyFaithful t₁ t₂ left right edge

/-- The actual equivalence's FORWARD nerve map preserves the full
Int×Int / ZMod 2 original C60 grading in every simplicial dimension. -/
theorem c60PhysicalFaceChangeEquivalence_gradedNerve
    (edge : TruncatedIcosahedralEdge) :
    CategoryTheory.nerveMap
        (c60PhysicalFaceChangeEquivalence
          t₁ t₂ left right edge).functor ≫
      c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge true =
      c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge false := by
  rw [c60PhysicalFaceChangeEquivalence_functor]
  exact c60PhysicalFaceChoice_gradedNerve_square
    t₁ t₂ left right edge

#print axioms c60PhysicalFaceChange_forward_reverse_NatIso
#print axioms c60PhysicalFaceChange_reverse_forward_NatIso
#print axioms c60PhysicalFaceChangeEquivalence
#print axioms c60PhysicalFaceChoiceNerveMap_hom_bijective
#print axioms c60PhysicalFaceChangeEquivalence_gradedNerve

end ActualPhysicalEdge
end KUOS.DependentOriginationC60PhysicalFaceNerveIsoV5_217

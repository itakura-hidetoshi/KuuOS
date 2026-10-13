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
open KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215
open KUOS.DependentOriginationC60PhysicalGradedNerveSquareV5_216
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000

/-!
# v5.217: genuine physical C60 adjacent-face simplicial isomorphism

On each original physical edge, its two DISTINCT adjacent original faces
have separately typed F42 paths and independent original F54/F55 trees.
The existing F48 face choice functor and F55 original-face reverse functor
preserve the four boundary tags and the full native Int×Int / ZMod 2 evaluation.

Their roundtrips are equal to identities on the F47 COMPLETE-NATIVE-KERNEL
quotient by actual source rigidity and the existing v5.205 cocycle theorems.
This upgrades the v5.216 strict commuting *square* to an actual isomorphism
of the corresponding native Mathlib simplicial nerves, which also commutes
with the complete native Gray grading.

This is not a raw unquotiented F42/F54/F55 Gray-3 category equivalence,
a nontrivial complete-Segal equivalence, or effective C60 global hyperdescent.
The original nonzero north-pentagon curvature / F55 delta non-lift persist.
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
theorem c60PhysicalFaceChange_forward_reverse
    (edge : TruncatedIcosahedralEdge) :
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge) ⋙
      (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge) =
    𝟭 (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)) := by
  apply CategoryTheory.Functor.ext
  · intro X Y f
    cases X <;> cases Y
    all_goals
      simpa [c60F56RoundTripHomCast] using
        (c60F56EveryActualEdgeFaceChange_roundTrip
          t₁ t₂ left right edge f)
  · intro X
    cases X <;> rfl

/-- The reverse-first transport is likewise the actual identity on
every F47 tagged Hom; source and target are not silently collapsed. -/
theorem c60PhysicalFaceChange_reverse_forward
    (edge : TruncatedIcosahedralEdge) :
    (c60F55ActualEdgeFaceChoiceReverseFunctor t₁ t₂ left right edge) ⋙
      (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge) =
    𝟭 (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)) := by
  let B₀ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false
  let B₁ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true
  have hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep :=
    c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge
  have hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep := rfl
  apply CategoryTheory.Functor.ext
  · intro X Y f
    cases X <;> cases Y
    all_goals
      simpa [c60F56RoundTripHomCast,
        c60F55ActualEdgeFaceChoiceReverseFunctor,
        c60F48ActualEdgeFaceChoiceFunctor] using
        (c60F56MixedTransport_roundTrip_map B₁ B₀
          hface.symm hrot.symm f)
  · intro X
    cases X <;> rfl

/-- Real two-face equivalence as an ISOMORPHISM of the actual
original tagged F47 source categories bundled as Mathlib Cat. -/
def c60PhysicalFaceChangeCatIso
    (edge : TruncatedIcosahedralEdge) :
    Cat.of (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)) ≅
    Cat.of (C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)) where
  hom := (c60F48ActualEdgeFaceChoiceFunctor
    t₁ t₂ left right edge).toCatHom
  inv := (c60F55ActualEdgeFaceChoiceReverseFunctor
    t₁ t₂ left right edge).toCatHom
  hom_inv_id := by
    apply Cat.Hom.ext
    change (c60F48ActualEdgeFaceChoiceFunctor
      t₁ t₂ left right edge) ⋙
      (c60F55ActualEdgeFaceChoiceReverseFunctor
        t₁ t₂ left right edge) = 𝟭 _
    exact c60PhysicalFaceChange_forward_reverse t₁ t₂ left right edge
  inv_hom_id := by
    apply Cat.Hom.ext
    change (c60F55ActualEdgeFaceChoiceReverseFunctor
      t₁ t₂ left right edge) ⋙
      (c60F48ActualEdgeFaceChoiceFunctor
        t₁ t₂ left right edge) = 𝟭 _
    exact c60PhysicalFaceChange_reverse_forward t₁ t₂ left right edge

/-- Apply the genuine pinned-Mathlib nerve functor to the physical
two-face source isomorphism: the actual simplicial nerves are isomorphic. -/
def c60PhysicalFaceChangeNerveIso
    (edge : TruncatedIcosahedralEdge) :
    c60PhysicalMixedThreeNerve t₁ t₂ left right edge false ≅
      c60PhysicalMixedThreeNerve t₁ t₂ left right edge true :=
  CategoryTheory.nerveFunctor.mapIso
    (c60PhysicalFaceChangeCatIso t₁ t₂ left right edge)

/-- The isomorphism is the ACTUAL already constructed face-choice
simplicial map, not just an abstract existence assertion. -/
theorem c60PhysicalFaceChangeNerveIso_hom
    (edge : TruncatedIcosahedralEdge) :
    (c60PhysicalFaceChangeNerveIso
      t₁ t₂ left right edge).hom =
      c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge := by
  rfl

/-- The isomorphic two nerves are compatible with the
FULL original F47-to-F49 native Gray-graded simplicial observation. -/
theorem c60PhysicalFaceChangeNerveIso_graded
    (edge : TruncatedIcosahedralEdge) :
    (c60PhysicalFaceChangeNerveIso t₁ t₂ left right edge).hom ≫
      c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge true =
      c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge false := by
  rw [c60PhysicalFaceChangeNerveIso_hom]
  exact c60PhysicalFaceChoice_gradedNerve_square
    t₁ t₂ left right edge

#print axioms c60PhysicalFaceChange_forward_reverse
#print axioms c60PhysicalFaceChange_reverse_forward
#print axioms c60PhysicalFaceChangeCatIso
#print axioms c60PhysicalFaceChangeNerveIso
#print axioms c60PhysicalFaceChangeNerveIso_graded

end ActualPhysicalEdge
end KUOS.DependentOriginationC60PhysicalFaceNerveIsoV5_217

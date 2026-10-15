import Mathlib.AlgebraicTopology.SimplicialSet.Nerve
import KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215
import KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204

namespace KUOS.DependentOriginationC60PhysicalGradedNerveSquareV5_216

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000

/-!
# C60 all-physical-edge simplicial grading square, v5.216

For each of the 90 actual physical C60 edges and its two DIFFERENT
incident polygon faces, F48 gives the original typed face-change
functor on the four-boundary F47 full-native-kernel quotient.
V5.215 constructs the two ordinary nerves and their maps to the F49
Gray-graded envelope.

This file strengthens coexistence of those constructions to a single
**strictly commuting simplicial square**.  It records the complete
native integer-pair charge and independent ZMod2 phase, not merely
the parity projection.  Equality holds in ALL simplicial degrees
because it arises from equality of genuine Mathlib source functors.

This is NOT a raw F42/F54/F55 syntactic equivalence or a proof of
global C60 hyperdescent; the F55 delta no-lift and nonzero physical
curvature remain distinct obstructions.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section PhysicalNativeSquare

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

/-- At each real edge the ACTUAL face-choice functor is compatible with
the complete F47 native Gray evaluation, as an equality of whole functors. -/
theorem c60PhysicalFaceChoice_gradedFunctor_square
    (edge : TruncatedIcosahedralEdge) :
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge) ⋙
      (c60F47MixedGrayFunctor
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)) =
    c60F47MixedGrayFunctor
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) := by
  let B₀ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false
  let B₁ := c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true
  have hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep := by
    exact c60F58PhysicalTwoFaces_sameOriginalF43
      t₁ t₂ left right edge
  have hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep := by
    rfl
  apply CategoryTheory.Functor.ext
  · intro X Y f
    simpa [c60F48ActualEdgeFaceChoiceFunctor, c60F47MixedGrayFunctor,
      B₀, B₁] using
      (c60F48MixedBoundaryTransportFunctor_fullNative B₀ B₁
        hface hrot f)
  · intro X
    rfl

/-- The ORIGINAL C60 physical side-choice nerve and the source-to-graded
nerve realization form one strict commuting square of genuine simplicial
maps, rather than only pointwise agreement of a chosen 3-cell charge. -/
theorem c60PhysicalFaceChoice_gradedNerve_square
    (edge : TruncatedIcosahedralEdge) :
    (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge) ≫
      (c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge true) =
    c60PhysicalMixedToOriginalGradedNerve
      t₁ t₂ left right edge false := by
  let F := c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge
  let G₀ := c60F47MixedGrayFunctor
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
  let G₁ := c60F47MixedGrayFunctor
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
  have hFunctor : F ⋙ G₁ = G₀ :=
    c60PhysicalFaceChoice_gradedFunctor_square t₁ t₂ left right edge
  change CategoryTheory.nerveMap F ≫ CategoryTheory.nerveMap G₁ =
    CategoryTheory.nerveMap G₀
  have hNerveComp : CategoryTheory.nerveMap F ≫
      CategoryTheory.nerveMap G₁ =
      CategoryTheory.nerveMap (F ⋙ G₁) := by
    simpa only [CategoryTheory.nerveFunctor_map,
      Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor] using
      (CategoryTheory.nerveFunctor.map_comp F.toCatHom G₁.toCatHom).symm
  calc
    CategoryTheory.nerveMap F ≫ CategoryTheory.nerveMap G₁ =
        CategoryTheory.nerveMap (F ⋙ G₁) := hNerveComp
    _ = CategoryTheory.nerveMap G₀ := congrArg CategoryTheory.nerveMap hFunctor

/-- The square commutes at *every* simplicial dimension, hence also for
all original F47 mixed composable histories, not just dimension one. -/
theorem c60PhysicalFaceChoice_gradedNerve_allDegrees
    (edge : TruncatedIcosahedralEdge) (k : Nat)
    (simplex : (c60PhysicalMixedThreeNerve
      t₁ t₂ left right edge false).obj (Opposite.op ⦋k⦌)) :
    ConcreteCategory.hom
      (((c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge) ≫
          (c60PhysicalMixedToOriginalGradedNerve
            t₁ t₂ left right edge true)).app (Opposite.op ⦋k⦌)) simplex =
    ConcreteCategory.hom
      ((c60PhysicalMixedToOriginalGradedNerve
        t₁ t₂ left right edge false).app (Opposite.op ⦋k⦌)) simplex := by
  rw [c60PhysicalFaceChoice_gradedNerve_square t₁ t₂ left right edge]
  rfl

#print axioms c60PhysicalFaceChoice_gradedFunctor_square
#print axioms c60PhysicalFaceChoice_gradedNerve_square
#print axioms c60PhysicalFaceChoice_gradedNerve_allDegrees

end PhysicalNativeSquare
end KUOS.DependentOriginationC60PhysicalGradedNerveSquareV5_216

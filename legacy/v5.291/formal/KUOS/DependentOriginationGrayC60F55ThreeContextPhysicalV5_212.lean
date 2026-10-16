import KUOS.DependentOriginationGrayC60F55ThreeOriginalRightBeckChevalleyV5_212

namespace KUOS.DependentOriginationGrayC60F55ThreeContextPhysicalV5_212

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
open KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212
open KUOS.DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212
open KUOS.DependentOriginationGrayC60F55ThreeOriginalRightBeckChevalleyV5_212
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.212 / F59-F61-B4: THREE-context BC at ALL real C60 incidences

Specialize BOTH independently original LEFT and RIGHT F42 path/F54
tree three-context BC associativity comparisons to EVERY true
90-edge/2-incident-polygon C60 physical source patch.

The two different original face-loop base darts are preserved.
No invented C60 quadrilateral, original F55 tenth constructor,
global vertex-gauge descent, or raw F42/F54 word identification
is inferred from this local F47 higher BC coherence.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineC60Incidence
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

/-- All 90 real edges meet two genuinely distinct physical C60 faces. -/
theorem c60F63PhysicalAdjacentFaces_distinct
    (edge : TruncatedIcosahedralEdge) :
    c60F48AdjacentRealFace edge false ≠
      c60F48AdjacentRealFace edge true :=
  c60F48BothRealFaces_distinct edge

-- Keep all original F54 trees and their genuine rotation witnesses as
-- source parameters even where quotient transport erases a dependency.
include t₁ t₂ left right

/-- All real C60 physical edges: three independently based ORIGINAL
F42 LEFT paths and three original F54/F55 later trees, with the
two different source BC parenthesizations equal as actual F47 NatIso. -/
theorem c60F63PhysicalLeftThreeBC_coherent
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ endpoint₀ endpoint₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ (c60F58OriginalPhysicalFaceBase edge false))
    (prior₁ : Quiver.Path u₁ (c60F58OriginalPhysicalFaceBase edge true))
    (middle₀ : Quiver.Path z₀ u₀) (middle₁ : Quiver.Path z₁ u₁)
    (outer₀ : Quiver.Path endpoint₀ z₀) (outer₁ : Quiver.Path endpoint₁ z₁)
    {k₁ l₁ k₂ l₂ k₃ l₃ : Nat}
    {mc md me : Blocks a b} {pc pd pe : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd)
    (later₃ : OriginalF45BracketTree k₃ l₃ md pd me pe) :
    c60F63OriginalLeftThreeBC_firstPair
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
      rfl
      (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
      (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
      prior₀ prior₁ middle₀ middle₁ outer₀ outer₁
      later₁ later₂ later₃ =
    c60F63OriginalLeftThreeBC_lastPair
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
      rfl
      (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
      (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
      prior₀ prior₁ middle₀ middle₁ outer₀ outer₁
      later₁ later₂ later₃ := by
  exact c60F63OriginalLeftThreeBC_coherent
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    prior₀ prior₁ middle₀ middle₁ outer₀ outer₁
    later₁ later₂ later₃

/-- All real C60 physical edges: three independently based ORIGINAL
F42 RIGHT suffixes with their three original F54/F55 earlier trees.
The two nonstrict source BC pastings are equal in the F47 four-tag
full-native-kernel category, with both real incident face bases intact. -/
theorem c60F63PhysicalRightThreeBC_coherent
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ endpoint₀ endpoint₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge false) u₀)
    (suffix₁ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge true) u₁)
    (middle₀ : Quiver.Path u₀ z₀) (middle₁ : Quiver.Path u₁ z₁)
    (outer₀ : Quiver.Path z₀ endpoint₀) (outer₁ : Quiver.Path z₁ endpoint₁)
    {k₁ l₁ k₂ l₂ k₃ l₃ : Nat}
    {mc md me : Blocks a b} {pc pd pe : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc)
    (earlier₃ : OriginalF45BracketTree k₃ l₃ me pe md pd) :
    c60F63OriginalRightThreeBC_firstPair
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
      rfl
      (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
      (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
      suffix₀ suffix₁ middle₀ middle₁ outer₀ outer₁
      earlier₁ earlier₂ earlier₃ =
    c60F63OriginalRightThreeBC_lastPair
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
      rfl
      (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
      (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
      suffix₀ suffix₁ middle₀ middle₁ outer₀ outer₁
      earlier₁ earlier₂ earlier₃ := by
  exact c60F63OriginalRightThreeBC_coherent
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    suffix₀ suffix₁ middle₀ middle₁ outer₀ outer₁
    earlier₁ earlier₂ earlier₃

#print axioms c60F63PhysicalAdjacentFaces_distinct
#print axioms c60F63PhysicalLeftThreeBC_coherent
#print axioms c60F63PhysicalRightThreeBC_coherent

end GenuineC60Incidence
end
end KUOS.DependentOriginationGrayC60F55ThreeContextPhysicalV5_212

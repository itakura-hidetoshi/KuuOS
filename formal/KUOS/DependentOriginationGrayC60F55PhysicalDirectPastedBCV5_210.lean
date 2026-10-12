import KUOS.DependentOriginationGrayC60F55DirectPastedPhysicalV5_210

namespace KUOS.DependentOriginationGrayC60F55PhysicalDirectPastedBCV5_210

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
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209
open KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209
open KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210
open KUOS.DependentOriginationGrayC60F55DirectPastedPhysicalV5_210
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.210 / F59-F60-C: REAL 90-edge C60 physical direct-pasted
# original-source LEFT/RIGHT Beck–Chevalley higher coherence

Unlike a symbolic square or a fictitious C60 quadrilateral, this
instantiates both original-context source NatIso comparisons on EVERY
genuine physical C60 edge, with its TWO truly incident original
pentagon/hexagon faces, independently based original F42 physical
face loops, and the SAME separately typed old F54/F55 square routes.

Both natural-isomorphism equalities hold within the adjoined full-native
F47 four-boundary source 3-Hom quotient. The new mixed correction
Delta=(0,1;0) is still not an old F55 PresentedCell, and the old F55
physical north pentagon remains nonflat; no unrestricted geometric
descent or complete unquotiented original Gray 3-category is asserted.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealPhysicalIncidences
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

/-- No invented face: the TWO actual polygons incident at any physical
edge are genuinely different and their original incidence is
certified by F58. -/
theorem c60F61PhysicalTwoOriginalFaces_distinct
    (edge : TruncatedIcosahedralEdge) :
    c60F48AdjacentRealFace edge false ≠
      c60F48AdjacentRealFace edge true :=
  (c60F58PhysicalBothFacesAndFlags t₁ t₂ left right edge).1

/-- For EACH of the ninety real C60 edges, LEFT direct original
F42/F54 Beck–Chevalley and two-stage original-source pasted BC
ARE the SAME actual NatIso after exact source F60 normalization.
The two genuine original polygon base darts remain independent. -/
theorem c60F61PhysicalLeftDirectBC_eq_pastedBC
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ (c60F58OriginalPhysicalFaceBase edge false))
    (prior₁ : Quiver.Path u₁ (c60F58OriginalPhysicalFaceBase edge true))
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    c60F61LeftDirectBCNormalizedNatIso
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        prior₀ prior₁ outer₀ outer₁ later₁ later₂ =
    c60F61LeftPastedBCNormalizedNatIso
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        prior₀ prior₁ outer₀ outer₁ later₁ later₂ :=
  c60F61LeftDirectBC_eq_pastedBC
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    prior₀ prior₁ outer₀ outer₁ later₁ later₂

/-- RIGHT independently typed original F42 suffix paths based at
the two different real C60 polygon vertices, and the independent
old F54/F55 earlier-context trees, yield the same source NatIso
under direct or two-successive Beck–Chevalley construction. -/
theorem c60F61PhysicalRightDirectBC_eq_pastedBC
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge false) u₀)
    (suffix₁ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge true) u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    c60F61RightDirectBCNormalizedNatIso
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂ =
    c60F61RightPastedBCNormalizedNatIso
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂ :=
  c60F61RightDirectBC_eq_pastedBC
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂

#print axioms c60F61PhysicalTwoOriginalFaces_distinct
#print axioms c60F61PhysicalLeftDirectBC_eq_pastedBC
#print axioms c60F61PhysicalRightDirectBC_eq_pastedBC

end RealPhysicalIncidences
end
end KUOS.DependentOriginationGrayC60F55PhysicalDirectPastedBCV5_210

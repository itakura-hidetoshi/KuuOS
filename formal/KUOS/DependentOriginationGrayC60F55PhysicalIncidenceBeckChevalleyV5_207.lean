import KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207

namespace KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.207 / F59-F58-B: every genuine C60 edge × its TWO original faces
# original F42/F54 contextual Beck–Chevalley SOURCE natural isomorphisms

This physically instantiates the abstract F58-A Beck–Chevalley
3-Hom source coherences on the genuine 90 C60 unoriented edges and
the EXACT two incident pentagon/hexagon physical polygon faces.
Crucially each actual original F42 FACE LOOP has its OWN initial
dart! The two original path contexts are independently typed; no
invented common basepoint or third incident polygon is used.

The SAME actual independently supplied F54 rotations are preserved
before context, and their typed originals are separately whiskered
after applying the F42 real Quiver.Paths. The commuting squares
are Mathlib NatIso IN THE ADJOINED F47 mixed four-boundary source
category, not mere Gray target equations or global raw F42/F54/F55
source identification. The independently nontrivial original-F55
nine-constructor Δ no-lift remains valid for both physical faces
after arbitrary legitimate left and right original contexts.
-/

/-- Genuine original base vertex of the actual pentagonal or
hexagonal closed C60 face path incident to a physical edge.
The two face choices generally have DIFFERENT source darts. -/
def c60F58OriginalPhysicalFaceBase
    (edge : TruncatedIcosahedralEdge) (side : Bool) : IcosahedralDart :=
  (c60F41PhysicalFaceBoundaryLoop (c60F48AdjacentRealFace edge side)).1

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealPhysicalC60F54
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

/-- Exactly the F47 four-boundary source frame carrying
one genuine original F42 face interchange and the same
independently typed original F54/F55 rotation-square cell. -/
def c60F58PhysicalMixedFrame
    (edge : TruncatedIcosahedralEdge) (side : Bool) :=
  c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side

/-- The actual original F43 interchanger (rather than merely a
constructed target grade) has the same COMPLETE image for BOTH
distinct physical incident faces. -/
theorem c60F58PhysicalTwoFaces_sameOriginalF43
    (edge : TruncatedIcosahedralEdge) :
    c60F44FaceThreeEval
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false).faceStep =
    c60F44FaceThreeEval
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true).faceStep := by
  change c60F44FaceThreeEval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false).faceStep =
    c60F44FaceThreeEval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true).faceStep
  rw [c60F48EveryRealEdgeFaceStep_native,
    c60F48EveryRealEdgeFaceStep_native]

/-- The unchanged old F54/F55 source rotation 3-arrow is
literally the same separately typed ORIGINAL rotation square
on both physical sides, not an adjoined new F55 arrow. -/
theorem c60F58PhysicalTwoFaces_sameOriginalF55
    (edge : TruncatedIcosahedralEdge) :
    c60F44OriginalF55Eval
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false).rotationStep =
    c60F44OriginalF55Eval
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true).rotationStep := rfl

/-- New F56 mixed source face-choice on the actual two real
incident polygons, with full original F43/F55 provenance. -/
def c60F58PhysicalFaceChoice
    (edge : TruncatedIcosahedralEdge) :
    C60F47BoundaryPoint
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false) ⥤
    C60F47BoundaryPoint
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge true) :=
  c60F56ContextMixedFunctor
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)

/-- The two real adjacent C60 polygons, NOT a fictitious
physical four-sided face, are distinct and each corner
of the actual four-flag incidence carrier is certified. -/
theorem c60F58PhysicalBothFacesAndFlags
    (edge : TruncatedIcosahedralEdge) :
    c60F48AdjacentRealFace edge false ≠
      c60F48AdjacentRealFace edge true ∧
    (∀ i j : Bool,
      truncatedDartOnSeedFace
        ((c60F46PhysicalFourFlagSquare edge).vertex i)
        ((c60F46PhysicalFourFlagSquare edge).face j)) := by
  constructor
  · exact c60F48BothRealFaces_distinct edge
  · intro i j
    exact c60F46PhysicalFourFlagSquare_allFourIncidences edge i j

/-- For every real physical edge, the TWO different based
original C60 face loops admit independently chosen left prior
paths. They yield a Beck–Chevalley NATURAL ISO between original
face choice and the genuine F42/F54 LEFT-context operation. -/
def c60F58PhysicalLeftBeckChevalleyNatIso
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ (c60F58OriginalPhysicalFaceBase edge false))
    (prior₁ : Quiver.Path u₁ (c60F58OriginalPhysicalFaceBase edge true))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :
    (c60F56OriginalLeftMixedContextFunctor
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      prior₀ later) ⋙
      (c60F58LeftAfterFaceChoice
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        prior₀ prior₁ later) ≅
    (c60F58PhysicalFaceChoice t₁ t₂ left right edge) ⋙
      (c60F56OriginalLeftMixedContextFunctor
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        prior₁ later) :=
  c60F58LeftFaceContext_NatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    prior₀ prior₁ later

/-- Completely independently typed RIGHT suffix paths based at
the two different original F42 face-loop darts also have a genuine
F47 source-level Beck–Chevalley natural isomorphism. -/
def c60F58PhysicalRightBeckChevalleyNatIso
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge false) u₀)
    (suffix₁ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge true) u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :
    (c60F56OriginalRightMixedContextFunctor
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
      suffix₀ earlier) ⋙
      (c60F58RightAfterFaceChoice
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        rfl
        (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
        (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
        suffix₀ suffix₁ earlier) ≅
    (c60F58PhysicalFaceChoice t₁ t₂ left right edge) ⋙
      (c60F56OriginalRightMixedContextFunctor
        (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
        suffix₁ earlier) :=
  c60F58RightFaceContext_NatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    suffix₀ suffix₁ earlier

/-- The ORIGINAL nine-constructor F55 PresentedCell system
cannot realize the ADJOINED new F47 comparison after either
originally based physical F42 left context. In particular the
actual independent original F54 square-left/right 2-boundaries
are preserved and their type is NOT identified with F42. -/
theorem c60F58PhysicalLeftContext_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u : IcosahedralDart}
    (prior : Quiver.Path u (c60F58OriginalPhysicalFaceBase edge side))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55LeftContextFunctor later).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
      ((c60F45F55LeftContextFunctor later).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F47WhiskerLeft
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          prior later).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerLeft
              (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
              prior later).rotationStep :=
  c60F57OriginalLeftContext_noOriginalF55Lift
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    prior later

/-- The no-lift equally survives each genuinely typed original
F42 right suffix with independently typed original F54 earlier
tree; it applies to BOTH actual physical incident faces. -/
theorem c60F58PhysicalRightContext_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u : IcosahedralDart}
    (suffix : Quiver.Path (c60F58OriginalPhysicalFaceBase edge side) u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55RightContextFunctor earlier).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
      ((c60F45F55RightContextFunctor earlier).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F47WhiskerRight
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          suffix earlier).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerRight
              (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
              suffix earlier).rotationStep :=
  c60F57OriginalRightContext_noOriginalF55Lift
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    suffix earlier

#print axioms c60F58PhysicalTwoFaces_sameOriginalF43
#print axioms c60F58PhysicalTwoFaces_sameOriginalF55
#print axioms c60F58PhysicalFaceChoice
#print axioms c60F58PhysicalBothFacesAndFlags
#print axioms c60F58PhysicalLeftBeckChevalleyNatIso
#print axioms c60F58PhysicalRightBeckChevalleyNatIso
#print axioms c60F58PhysicalLeftContext_noOriginalF55Delta
#print axioms c60F58PhysicalRightContext_noOriginalF55Delta

end RealPhysicalC60F54
end
end KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
